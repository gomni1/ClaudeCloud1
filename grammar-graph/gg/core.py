"""grammar-graph core: rule constants, well-mixed references, graph classes, ctypes wrappers of csrc/gg.c,
tracker and analysis (SPEC.md).  Graph builders are combinatorial; no coordinates anywhere."""
import ctypes
import json
import math
import os
import random
import subprocess

import numba as nb
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "csrc", "gg.c")
LIB = os.path.join(ROOT, "csrc", "libgg.so")
EVID = os.path.join(ROOT, "evidence")

K0 = np.array([1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
               0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678,
               0.17271135353305755, 0.10361090436515946, 6.769536427560776])
USE = np.array([0, 1, 2, 3, 4, 5, 6, 8, 9])  # k9 (idx 7), k12 (idx 10) unused
M, KR, KC = 8, 2, 4
T0 = 6.3524
DT_FRAME, TAU = 0.4, 0.6
T_RUN = 300 * T0
NFRAMES = int(T_RUN / DT_FRAME + 1e-9)          # 4764
F_WIN0 = int(math.ceil(50 * T0 / DT_FRAME))      # first window frame index f (t=(f+1)*0.4 > 50 T0) -> 794
LONG = 20 * T0                                   # 127.048
LAMS = [0.0, 0.006, 0.02]


def seed_of(*a):
    import zlib
    a = [zlib.crc32(x.encode()) if isinstance(x, str) else int(x) for x in a]
    return int(np.random.default_rng([1112026, *a]).integers(0, 2 ** 63))


def k_of(lam):
    k = K0.copy()
    ln = np.log(K0[USE])
    k[USE] = np.exp((1 - lam) * ln + lam * ln.mean())
    return k


def Fj(x, j, m=M):
    x = np.asarray(x, float)
    return sum(math.comb(m, i) * x ** i * (1 - x) ** (m - i) for i in range(j, m + 1))


# ---------------- well-mixed mean field ----------------
def rhs(z, k):
    c, v, l, p = z
    fr, fc = Fj(c, KR), Fj(c, KC)
    dc = -(k[0] + k[1] + k[5]) * c - k[9] * c * fc + (k[8] + k[2] * fr) * v + k[4] * l
    dv = (k[1] + k[9] * fc) * c - (k[8] + k[2] * fr) * v + k[3] * l + k[6] * p
    dl = k[0] * c - (k[3] + k[4]) * l
    dp = k[5] * c - k[6] * p
    return np.array([dc, dv, dl, dp])


def balance(lam, guess=(0.0812, 0.6332, 0.1801)):
    k = k_of(lam)
    g = lambda y: rhs([y[0], y[1], y[2], 1 - y[0] - y[1] - y[2]], k)[:3]  # noqa: E731
    y = fsolve(g, guess, xtol=1e-12)
    return np.array([y[0], y[1], y[2], 1 - y.sum()])


def jac_eigs(lam):
    k, z = k_of(lam), balance(lam)
    red = lambda y: rhs([y[0], y[1], y[2], 1 - sum(y)], k)[:3]  # noqa: E731
    J, h = np.zeros((3, 3)), 1e-7
    for j in range(3):
        e = np.zeros(3); e[j] = h
        J[:, j] = (red(z[:3] + e) - red(z[:3] - e)) / (2 * h)
    return np.linalg.eigvals(J)


def cycle(lam, t_relax=3000.0):
    """Attractor of the ODE started near the balance. Returns dict with period, ranges, s_c, s_v (None if
    the orbit decays to the balance)."""
    k, z0 = k_of(lam), balance(lam)
    f = lambda t, z: rhs(z, k)  # noqa: E731
    s = solve_ivp(f, (0, t_relax), z0 + np.array([0.01, -0.01, 0, 0]), method="LSODA", rtol=1e-10, atol=1e-13)
    z1 = s.y[:, -1]
    s2 = solve_ivp(f, (0, 200), z1, method="LSODA", rtol=1e-11, atol=1e-14, dense_output=True)
    tt = np.linspace(0, 200, 400001)
    C = s2.sol(tt)[0]
    up = np.nonzero((C[:-1] < z0[0]) & (C[1:] >= z0[0]))[0]
    if len(up) < 3 or C.max() - C.min() < 1e-6:
        return None
    tc = tt[up] + (z0[0] - C[up]) / (C[up + 1] - C[up]) * (tt[1] - tt[0])
    per = float(np.mean(np.diff(tc[-6:])))
    g = np.linspace(tc[-2], tc[-2] + per, 200000, endpoint=False)
    X = s2.sol(g)
    return dict(period=per, c_range=[float(X[0].min()), float(X[0].max())],
                v_range=[float(X[1].min()), float(X[1].max())], s_c=float(X[0].std()), s_v=float(X[1].std()),
                winds=winds_round(X[0], X[1], z0[0], z0[1]))


def winds_round(c, v, cs, vs):
    a = np.unwrap(np.arctan2(v - vs, c - cs))
    return float((a[-1] - a[0]) / (2 * np.pi))


def hopf_lambda(lo=0.0, hi=0.05):
    g = lambda lam: jac_eigs(lam).real.max()  # noqa: E731
    if g(lo) * g(hi) > 0:
        return None
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def refs(lam):
    """(c*, v*, s_c, s_v) per SPEC section 3, cached in evidence/refs.json."""
    path = os.path.join(EVID, "refs.json")
    R = json.load(open(path)) if os.path.exists(path) else {}
    key = f"{lam:.6f}"
    if key not in R:
        z = balance(lam)
        cy = cycle(lam)
        cy0 = cycle(0.0)
        use = cy if cy is not None else cy0
        R[key] = dict(lam=lam, balance=z.tolist(), cycle=cy, s_c=use["s_c"], s_v=use["s_v"],
                      s_from="own cycle" if cy is not None else "lam=0 cycle (past Hopf)")
        os.makedirs(EVID, exist_ok=True)
        json.dump(R, open(path, "w"), indent=1)
    r = R[key]
    return r["balance"][0], r["balance"][1], r["s_c"], r["s_v"]


# ---------------- graphs (combinatorial) ----------------
def csr(N, edges):
    e = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    a = np.concatenate([e[:, 0], e[:, 1]]); b = np.concatenate([e[:, 1], e[:, 0]])
    o = np.lexsort((b, a))
    a, b = a[o], b[o]
    off = np.zeros(N + 1, np.int32)
    np.add.at(off, a + 1, 1)
    return np.cumsum(off).astype(np.int32), b.astype(np.int32)


def graph_S(N, seed):
    rng = random.Random(seed)
    F = [(0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)]
    for v in range(4, N):
        f = rng.randrange(len(F))
        a, b, c = F[f]
        F[f] = (a, b, v); F.append((b, c, v)); F.append((c, a, v))
    F = [list(x) for x in F]
    # edge structures
    eid, EV, EF, FE = {}, [], [], [[0, 0, 0] for _ in F]
    for fi, fc in enumerate(F):
        for s in range(3):
            a, b = fc[s], fc[(s + 1) % 3]
            key = (a, b) if a < b else (b, a)
            if key not in eid:
                eid[key] = len(EV); EV.append(list(key)); EF.append([fi, -1])
            else:
                EF[eid[key]][1] = fi
            FE[fi][s] = eid[key]
    deg = [0] * N
    for a, b in EV:
        deg[a] += 1; deg[b] += 1
    E = len(EV)
    acc = 0
    for _ in range(20 * E):
        e = rng.randrange(E)
        f1, f2 = EF[e]
        s1 = FE[f1].index(e); s2 = FE[f2].index(e)
        u, v, a = F[f1][s1], F[f1][(s1 + 1) % 3], F[f1][(s1 + 2) % 3]
        b = F[f2][(s2 + 2) % 3]
        if deg[u] <= 3 or deg[v] <= 3 or ((a, b) if a < b else (b, a)) in eid:
            continue
        e_va, e_au = FE[f1][(s1 + 1) % 3], FE[f1][(s1 + 2) % 3]
        e_ub, e_bv = FE[f2][(s2 + 1) % 3], FE[f2][(s2 + 2) % 3]
        F[f1] = [a, u, b]; FE[f1] = [e_au, e_ub, e]
        F[f2] = [b, v, a]; FE[f2] = [e_bv, e_va, e]
        EF[e_ub][EF[e_ub].index(f2)] = f1
        EF[e_va][EF[e_va].index(f1)] = f2
        del eid[(u, v) if u < v else (v, u)]
        key = (a, b) if a < b else (b, a)
        eid[key] = e; EV[e] = list(key)
        deg[u] -= 1; deg[v] -= 1; deg[a] += 1; deg[b] += 1
        acc += 1
    F = np.array(F, np.int32)
    off, nbr = csr(N, EV)
    return dict(name="S", N=N, off=off, nbr=nbr, tri=F, surface=True, flips_accepted=acc, flips_tried=20 * E)


def graph_R(N, d, seed):
    rng = random.Random(seed)
    while True:
        stubs = [v for v in range(N) for _ in range(d)]
        adj = [set() for _ in range(N)]
        ok = True
        while stubs:
            n = len(stubs)
            found = False
            for _ in range(200):
                i, j = rng.randrange(n), rng.randrange(n)
                a, b = stubs[i], stubs[j]
                if i != j and a != b and b not in adj[a]:
                    found = True
                    break
            if not found:  # exhaustive check for any admissible pair
                cand = [(i, j) for i in range(n) for j in range(i + 1, n)
                        if stubs[i] != stubs[j] and stubs[j] not in adj[stubs[i]]]
                if not cand:
                    ok = False
                    break
                i, j = cand[rng.randrange(len(cand))]
                a, b = stubs[i], stubs[j]
            adj[a].add(b); adj[b].add(a)
            for x in sorted((i, j), reverse=True):
                stubs[x] = stubs[-1]; stubs.pop()
        if ok:
            break
    edges = [(a, b) for a in range(N) for b in adj[a] if a < b]
    off, nbr = csr(N, edges)
    return dict(name="R", N=N, off=off, nbr=nbr, tri=None, surface=False)


def graph_C(N, kk, p, seed, name):
    rng = random.Random(seed)
    adj = [set() for _ in range(N)]
    edges = []
    for i in range(N):
        for j in range(1, kk + 1):
            a, b = i, (i + j) % N
            adj[a].add(b); adj[b].add(a); edges.append([a, b])
    if p > 0:
        for idx in range(len(edges)):
            if rng.random() < p:
                a, b = edges[idx]
                choices = None
                while True:
                    w = rng.randrange(N)
                    if w != a and w not in adj[a]:
                        break
                    if choices is None and len(adj[a]) > N - 3:
                        raise RuntimeError("saturated")
                adj[a].discard(b); adj[b].discard(a)
                adj[a].add(w); adj[w].add(a)
                edges[idx] = [a, w]
    off, nbr = csr(N, edges)
    return dict(name=name, N=N, off=off, nbr=nbr, tri=None, surface=False)


def planted_sphere(n=60):
    """n x n grid of cells on labels (i, j), diagonal (i,j)-(i+1,j+1), plus an apex joined to the boundary."""
    vid = lambda i, j: i * (n + 1) + j  # noqa: E731
    apex = (n + 1) ** 2
    F = []
    for i in range(n):
        for j in range(n):
            F.append((vid(i, j), vid(i + 1, j), vid(i + 1, j + 1)))      # L(i, j)
            F.append((vid(i, j), vid(i + 1, j + 1), vid(i, j + 1)))      # U(i, j)
    bd = [(i, 0) for i in range(n)] + [(n, j) for j in range(n)] + [(i, n) for i in range(n, 0, -1)] + \
         [(0, j) for j in range(n, 0, -1)]
    for q in range(len(bd)):  # boundary traversed counter-clockwise; apex faces close the sphere
        a, b = vid(*bd[q]), vid(*bd[(q + 1) % len(bd)])
        F.append((b, a, apex))
    F = np.array(F, np.int32)
    E = set()
    for a, b, c in F:
        for x, y in ((a, b), (b, c), (c, a)):
            E.add((min(x, y), max(x, y)))
    N = apex + 1
    off, nbr = csr(N, sorted(E))
    return dict(name="planted", N=N, off=off, nbr=nbr, tri=F, surface=True, n=n, boundary=[vid(*x) for x in bd],
                apex=apex)


def check_surface(g):
    """Each directed edge exactly once (consistent orientation), Euler characteristic 2, simple graph."""
    F = g["tri"]
    d = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    key = d[:, 0].astype(np.int64) * g["N"] + d[:, 1]
    E = len(g["nbr"]) // 2
    return dict(directed_unique=bool(len(np.unique(key)) == len(key)), euler=int(g["N"] - E + len(F)),
                min_deg=int(np.diff(g["off"]).min()))


@nb.njit(cache=True)
def _triangles(N, off, nbr):
    out = []
    for i in range(N):
        for e in range(off[i], off[i + 1]):
            j = nbr[e]
            if j <= i:
                continue
            # common neighbours k > j (sorted lists)
            p, q = off[i], off[j]
            while p < off[i + 1] and q < off[j + 1]:
                a, b = nbr[p], nbr[q]
                if a == b:
                    if a > j:
                        out.append((i, j, a))
                    p += 1; q += 1
                elif a < b:
                    p += 1
                else:
                    q += 1
    return out


def triangles(g):
    if g.get("tri") is not None:
        return g["tri"]
    t = _triangles(g["N"], g["off"], g["nbr"])
    return np.array(t, np.int32).reshape(-1, 3)


@nb.njit(cache=True)
def _bfs_stats(N, off, nbr):
    dist = np.full(N, -1, np.int64)
    q = np.empty(N, np.int64)
    ballsum = np.zeros(N + 1, np.float64)  # sum over sources of number of vertices at exactly distance r
    diam = 0
    for s in range(N):
        dist[:] = -1
        dist[s] = 0
        h, t = 0, 1
        q[0] = s
        while h < t:
            u = q[h]; h += 1
            for e in range(off[u], off[u + 1]):
                w = nbr[e]
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q[t] = w; t += 1
        for x in range(t):
            ballsum[dist[q[x]]] += 1
        if dist[q[t - 1]] > diam:
            diam = dist[q[t - 1]]
    return diam, ballsum


@nb.njit(cache=True)
def _clustering(N, off, nbr):
    tot = 0.0
    mark = np.zeros(N, np.int64) - 1
    for i in range(N):
        d = off[i + 1] - off[i]
        if d < 2:
            continue
        for e in range(off[i], off[i + 1]):
            mark[nbr[e]] = i
        links = 0
        for e in range(off[i], off[i + 1]):
            j = nbr[e]
            for f in range(off[j], off[j + 1]):
                if mark[nbr[f]] == i:
                    links += 1
        tot += links / (d * (d - 1.0))
    return tot / N


def graph_stats(g):
    N, off, nbr = g["N"], g["off"], g["nbr"]
    diam, shell = _bfs_stats(N, off, nbr)
    Mr = np.cumsum(shell[:diam + 1]) / N
    rs = np.arange(2, diam // 2 + 1)
    dg = float(np.polyfit(np.log(rs), np.log(Mr[rs]), 1)[0]) if len(rs) >= 2 else None
    return dict(N=int(N), mean_degree=float(len(nbr) / N), clustering=float(_clustering(N, off, nbr)),
                diameter=int(diam), d_g=dg, d_g_radii=[int(rs[0]), int(rs[-1])] if len(rs) else None,
                ball_sizes=Mr[:min(diam, 12) + 1].tolist())


@nb.njit(cache=True)
def _balls(N, off, nbr, r):
    dist = np.full(N, -1, np.int64)
    q = np.empty(N, np.int64)
    cnt = np.zeros(N + 1, np.int64)
    out = []
    for s in range(N):
        dist[s] = 0
        h, t = 0, 1
        q[0] = s
        while h < t:
            u = q[h]; h += 1
            if dist[u] == r:
                continue
            for e in range(off[u], off[u + 1]):
                w = nbr[e]
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q[t] = w; t += 1
        cnt[s + 1] = t
        for x in range(t):
            out.append(q[x])
            dist[q[x]] = -1
    return np.cumsum(cnt), out


def balls(g, r):
    key = f"ball{r}"
    if key not in g:
        o, idx = _balls(g["N"], g["off"], g["nbr"], r)
        g[key] = (o.astype(np.int32), np.array(idx, np.int32))
    return g[key]


def ftab(g):
    deg = np.diff(g["off"])
    toff = np.zeros(g["N"], np.int32)
    FR, FC, start = [], [], {}
    for d in np.unique(deg):
        start[d] = len(FR)
        x = np.arange(d + 1) / d if d > 0 else np.zeros(1)
        FR += list(Fj(x, KR)); FC += list(Fj(x, KC))
    for i, d in enumerate(deg):
        toff[i] = start[d]
    return toff, np.array(FR, float), np.array(FC, float)


# ---------------- C library ----------------
_L = None
_d = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
_i32 = np.ctypeslib.ndpointer(dtype=np.int32, flags="C_CONTIGUOUS")
_i64 = np.ctypeslib.ndpointer(dtype=np.int64, flags="C_CONTIGUOUS")
_i8 = np.ctypeslib.ndpointer(dtype=np.int8, flags="C_CONTIGUOUS")
_u8 = np.ctypeslib.ndpointer(dtype=np.uint8, flags="C_CONTIGUOUS")


def lib():
    global _L
    if _L is None:
        if not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
            subprocess.check_call(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, SRC, "-lm"])
        L = ctypes.CDLL(LIB)
        c = ctypes
        vp = c.c_void_p
        L.gg_run_graph.restype = c.c_int
        L.gg_run_graph.argtypes = [c.c_int, _i32, _i32, _i32, _d, _d, _d, _i8, c.c_double, c.c_double, c.c_double,
                                   c.c_uint64, _i32, _i32, c.c_int, vp, c.c_double, c.c_double, c.c_double,
                                   c.c_double, c.c_int, _i32, vp, vp, c.c_int, vp, vp, c.c_double, _d, c.c_int, vp]
        L.gg_run_lumped.restype = c.c_int
        L.gg_run_lumped.argtypes = [c.c_int, _d, _d, _d, _i64, c.c_double, c.c_double, c.c_int, c.c_uint64, _i32, _d]
        L.gg_detect.restype = None
        L.gg_detect.argtypes = [c.c_int, _i32, _d, _i8]
        L.gg_ndef.restype = c.c_int64
        L.gg_copy_defects.argtypes = [_i32, _i8]
        L.gg_free_defects.restype = None
        _L = L
    return _L


def _p(a):
    return None if a is None else a.ctypes.data


def detect(tri, phi):
    w = np.zeros(len(tri), np.int8)
    lib().gg_detect(len(tri), np.ascontiguousarray(tri, np.int32), np.ascontiguousarray(phi, float), w)
    return w


def init_roles(N, lam, seed):
    z = balance(lam)
    rng = np.random.default_rng(seed)
    return rng.choice(4, size=N, p=z / z.sum()).astype(np.int8)


def run_graph(g, lam, seed, t_max=T_RUN, dt=DT_FRAME, fields=True, k=None, roles=None, chg=False, snaps=(),
              nbatch=0, max_cpu=0.0, ref=None):
    N = g["N"]
    k = k_of(lam) if k is None else k
    toff, FR, FC = ftab(g)
    role = init_roles(N, lam, seed + 1) if roles is None else np.array(roles, np.int8)
    nf = int(t_max / dt + 1e-9)
    if fields:
        bo, bi = balls(g, 2)
        tri = np.ascontiguousarray(triangles(g), np.int32)
        cs, vs, sc, sv = refs(lam) if ref is None else ref
    else:
        bo, bi = np.arange(N + 1, dtype=np.int32), np.arange(N, dtype=np.int32)
        tri = np.zeros((0, 3), np.int32)
        cs, vs, sc, sv = 0.0, 0.0, 1.0, 1.0
    gcount = np.zeros(nf * 4, np.int32)
    fstat = np.zeros(nf * 5) if fields else None
    nbyte = (N + 7) // 8
    chga = np.zeros(nf * nbyte, np.uint8) if chg else None
    snapf = np.array(sorted(snaps), np.int32)
    snap = np.zeros(len(snapf) * N, np.uint8) if len(snapf) else None
    tw = np.zeros(6 * max(nbatch, 1)) if nbatch else None
    stats = np.zeros(5)
    L = lib()
    L.gg_run_graph(N, g["off"], g["nbr"], toff, FR, FC, np.ascontiguousarray(k, float), role, float(t_max), float(dt),
                   TAU, seed, bo, bi, len(tri), _p(tri), cs, vs, sc, sv, nf, gcount, _p(fstat), _p(chga), len(snapf),
                   _p(snapf), _p(snap), float(max_cpu), stats, int(nbatch), _p(tw))
    nd = L.gg_ndef()
    dtri = np.zeros(nd, np.int32); dsgn = np.zeros(nd, np.int8)
    if nd:
        L.gg_copy_defects(dtri, dsgn)
    L.gg_free_defects()
    out = dict(gcount=gcount.reshape(nf, 4), events=int(stats[0]), frames=int(stats[1]), aborted=bool(stats[2]),
               t_end=float(stats[4]), role_end=role, ntri=len(tri))
    if fields:
        fs = fstat.reshape(nf, 5)
        doff = np.concatenate([[0], np.cumsum(fs[:, 4].astype(np.int64))])
        out.update(fstat=fs, doff=doff, dtri=dtri, dsgn=dsgn)
    if chg:
        out["chg"] = chga.reshape(nf, nbyte)
    if snap is not None:
        out["snap"] = snap.reshape(len(snapf), N)
        out["snapf"] = snapf
    if nbatch:
        out["tw"] = tw.reshape(nbatch, 6)
    return out


def run_lumped(N, lam, seed, t_max, dt, k=None, n0=None):
    k = k_of(lam) if k is None else k
    if n0 is None:
        r = init_roles(N, lam, seed + 1)
        n0 = np.bincount(r, minlength=4)
    x = np.arange(N) / (N - 1)
    FRt, FCt = Fj(x, KR), Fj(x, KC)
    ns = int(t_max / dt + 1e-9)
    out = np.zeros(ns * 4, np.int32)
    st = np.zeros(3)
    lib().gg_run_lumped(N, FRt, FCt, np.ascontiguousarray(k, float), np.array(n0, np.int64), float(t_max), float(dt),
                        ns, seed, out, st)
    return out.reshape(ns, 4), int(st[0])


# ---------------- tracking and analysis (SPEC section 4, 6) ----------------
@nb.njit(cache=True)
def _cands(N, tri, bo, bi, d_from, s_from, d_to, s_to, head, nxt, who):
    """For each defect in d_from: the unique same-sign defect in d_to within D <= r (r encoded in the ball),
    -1 if none, -2 if more than one."""
    nto = len(d_to)
    k = 0
    for x in range(nto):
        for c in range(3):
            v = tri[d_to[x], c]
            nxt[k] = head[v]; head[v] = k; who[k] = x; k += 1
    res = np.full(len(d_from), -1, np.int64)
    for y in range(len(d_from)):
        first = -1
        amb = False
        for c in range(3):
            u = tri[d_from[y], c]
            for e in range(bo[u], bo[u + 1]):
                w = bi[e]
                h = head[w]
                while h >= 0:
                    x = who[h]
                    if s_to[x] == s_from[y]:
                        if first == -1:
                            first = x
                        elif x != first:
                            amb = True
                            break
                    h = nxt[h]
                if amb:
                    break
            if amb:
                break
        res[y] = -2 if amb else first
    for x in range(nto):
        for c in range(3):
            head[tri[d_to[x], c]] = -1
    return res


@nb.njit(cache=True)
def _track(N, tri, bo, bi, doff, dtri, dsgn, f0, f1):
    """Mutual-unique same-sign tracking over frames f0..f1-1. Returns per-defect track id (-1 outside window)
    and per-track (start, end, sign)."""
    nd = len(dtri)
    tid = np.full(nd, -1, np.int64)
    maxk = 1
    for f in range(f0, f1):
        maxk = max(maxk, 3 * (doff[f + 1] - doff[f]))
    head = np.full(N, -1, np.int64)
    nxt = np.empty(maxk, np.int64)
    who = np.empty(maxk, np.int64)
    ts = []
    te = []
    tsg = []
    for i in range(doff[f0], doff[f0 + 1]):
        tid[i] = len(ts); ts.append(f0); te.append(f0); tsg.append(dsgn[i])
    for f in range(f0, f1 - 1):
        a0, a1, b0, b1 = doff[f], doff[f + 1], doff[f + 1], doff[f + 2]
        A, SA, B, SB = dtri[a0:a1], dsgn[a0:a1], dtri[b0:b1], dsgn[b0:b1]
        ca = _cands(N, tri, bo, bi, A, SA, B, SB, head, nxt, who)
        cb = _cands(N, tri, bo, bi, B, SB, A, SA, head, nxt, who)
        for x in range(b1 - b0):
            y = cb[x]
            if y >= 0 and ca[y] == x:
                t = tid[a0 + y]
                tid[b0 + x] = t
                te[t] = f + 1
            else:
                tid[b0 + x] = len(ts); ts.append(f + 1); te.append(f + 1); tsg.append(dsgn[b0 + x])
    return tid, np.array(ts, np.int64), np.array(te, np.int64), np.array(tsg, np.int64)


def track(g, run, f0=None, f1=None):
    f0 = F_WIN0 if f0 is None else f0
    f1 = len(run["doff"]) - 1 if f1 is None else f1
    bo, bi = balls(g, 2)
    tri = np.ascontiguousarray(triangles(g), np.int64)
    tid, ts, te, tsg = _track(g["N"], tri, bo, bi, run["doff"], run["dtri"], run["dsgn"], f0, f1)
    return dict(tid=tid, start=ts, end=te, sign=tsg, f0=f0, f1=f1, life=(te - ts) * DT_FRAME)


@nb.njit(cache=True)
def _pairing(N, tri, bo, bi, ev_f, ev_t, ev_s, foff, fmin, fmax):
    """For events sorted by frame: paired if an opposite-sign event at frame f-1..f+1 has D <= r (ball r)."""
    ne = len(ev_f)
    paired = np.zeros(ne, np.bool_)
    head = np.full(N, -1, np.int64)
    nxt = np.empty(9 * ne + 3, np.int64)
    who = np.empty(9 * ne + 3, np.int64)
    for f in range(fmin, fmax + 1):
        e0, e1 = foff[f - fmin], foff[f - fmin + 1]
        if e1 == e0:
            continue
        lo = foff[max(f - 1, fmin) - fmin]
        hi = foff[min(f + 1, fmax) - fmin + 1]
        k = 0
        for x in range(lo, hi):
            for c in range(3):
                v = tri[ev_t[x], c]
                nxt[k] = head[v]; head[v] = k; who[k] = x; k += 1
        for y in range(e0, e1):
            found = False
            for c in range(3):
                u = tri[ev_t[y], c]
                for e in range(bo[u], bo[u + 1]):
                    h = head[bi[e]]
                    while h >= 0:
                        if ev_s[who[h]] == -ev_s[y]:
                            found = True
                            break
                        h = nxt[h]
                    if found:
                        break
                if found:
                    break
            paired[y] = found
        for x in range(lo, hi):
            for c in range(3):
                head[tri[ev_t[x], c]] = -1
    return paired


def pairing(g, run, tr):
    """D3: births (non-left-censored starts) and deaths (non-right-censored ends)."""
    bo, bi = balls(g, 3)
    tri = np.ascontiguousarray(triangles(g), np.int64)
    first = {}
    last = {}
    tid = tr["tid"]
    idx = np.nonzero(tid >= 0)[0]
    # defect index -> frame
    fr = np.searchsorted(run["doff"], idx, side="right") - 1
    for i, f in zip(idx, fr):
        t = tid[i]
        if t not in first:
            first[t] = (f, run["dtri"][i])
        last[t] = (f, run["dtri"][i])
    ev = []  # (frame, tri, sign, kind)
    for t in range(len(tr["start"])):
        if tr["start"][t] > tr["f0"]:
            ev.append((first[t][0], first[t][1], tr["sign"][t], 0))
        if tr["end"][t] < tr["f1"] - 1:
            ev.append((last[t][0], last[t][1], tr["sign"][t], 1))
    if not ev:
        return dict(births=0, deaths=0, births_paired=0, deaths_paired=0)
    ev = np.array(sorted(ev), np.int64)
    fmin, fmax = int(ev[0, 0]), int(ev[-1, 0])
    foff = np.searchsorted(ev[:, 0], np.arange(fmin, fmax + 2))
    p = _pairing(g["N"], tri, bo, bi, ev[:, 0], ev[:, 1], ev[:, 2], foff, fmin, fmax)
    b, d = ev[:, 3] == 0, ev[:, 3] == 1
    return dict(births=int(b.sum()), deaths=int(d.sum()), births_paired=int(p[b].sum()),
                deaths_paired=int(p[d].sum()))


@nb.njit(cache=True)
def _msbfs(N, off, nbr, src):
    dist = np.full(N, -1, np.int64)
    q = np.empty(N, np.int64)
    t = 0
    for s in src:
        if dist[s] < 0:
            dist[s] = 0; q[t] = s; t += 1
    h = 0
    while h < t:
        u = q[h]; h += 1
        for e in range(off[u], off[u + 1]):
            w = nbr[e]
            if dist[w] < 0:
                dist[w] = dist[u] + 1; q[t] = w; t += 1
    return dist


def long_tracks(g, run, tr):
    """Per long track: triangle sequence, MSD contributions, replacement fraction."""
    tri = triangles(g)
    out = []
    lags = np.unique(np.round(np.geomspace(1, 318, 20)).astype(int))
    for t in np.nonzero(tr["life"] >= LONG - 1e-9)[0]:
        idx = np.nonzero(tr["tid"] == t)[0]
        seq = run["dtri"][idx]
        cache = {}

        def D(a, b):
            if a not in cache:
                cache[a] = _msbfs(g["N"], g["off"], g["nbr"], tri[a].astype(np.int64))
            return int(cache[a][tri[b]].min())
        msd = {}
        for n in lags:
            if n < len(seq):
                vals = [D(int(seq[i]), int(seq[i + n])) ** 2 for i in range(len(seq) - n)]
                msd[int(n)] = (float(np.sum(vals)), len(vals))
        rep = None
        if "chg" in run:
            bo, bi = balls(g, 2)
            B = np.unique(np.concatenate([bi[bo[v]:bo[v + 1]] for v in tri[seq[0]]]))
            a, b = int(tr["start"][t]), int(tr["end"][t])
            bits = np.bitwise_or.reduce(run["chg"][a + 1:b + 1], axis=0)
            changed = (bits[B >> 3] >> (B & 7)) & 1
            rep = float(changed.mean())
        out.append(dict(track=int(t), sign=int(tr["sign"][t]), start=int(tr["start"][t]), end=int(tr["end"][t]),
                        life=float(tr["life"][t]), n_unique_tri=len(set(seq.tolist())), msd=msd, replacement=rep,
                        censored=bool(tr["start"][t] == tr["f0"] or tr["end"][t] == tr["f1"] - 1)))
    return out


def summarize(g, run, lam, f0=None):
    f0 = F_WIN0 if f0 is None else f0
    fs = run["fstat"][f0:]
    gc = run["gcount"][f0:] / g["N"]
    cs, vs, sc, sv = refs(lam)
    ntri = run["ntri"]
    return dict(A=float(gc[:, 0].std() / sc), Rbar=float(fs[:, 0].mean()), mean_c=float(gc[:, 0].mean()),
                mean_v=float(gc[:, 1].mean()), density=float((fs[:, 4] / max(ntri, 1)).mean()) if ntri else 0.0,
                defect_frames=int(fs[:, 4].sum()), amp_def_sum=float(fs[:, 2].sum()),
                amp_all_sum=float(fs[:, 1].sum()), n_win_frames=int(len(fs)), ntri=int(ntri),
                identity_violations_allframes=int(np.count_nonzero(run["fstat"][:, 3])), events=run["events"],
                aborted=run["aborted"])


def cpu_s():
    import resource
    a = resource.getrusage(resource.RUSAGE_SELF)
    b = resource.getrusage(resource.RUSAGE_CHILDREN)
    return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime
