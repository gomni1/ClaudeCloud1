"""G1 harness (SPEC section 5): H1, H2, H3, P1, P2, P3.  Writes evidence/g1.json."""
import itertools
import json
import math
import os
import random
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.stats import chi2

from gg.core import (EVID, F_WIN0, KC, KR, LONG, NFRAMES, T0, Fj, cpu_s, csr, detect, graph_S, init_roles, k_of,
                     planted_sphere, run_graph, run_lumped, seed_of, track)


# ---------------- H1 ----------------
def h1(N=10000, periods=130, discard=30, seed=None):
    seed = seed_of("H1") if seed is None else seed
    dt = 0.05
    X, ev = run_lumped(N, 0.0, seed, periods * T0, dt)
    c = X[:, 0] / N
    t = (np.arange(len(c)) + 1) * dt
    c, t = c[t > discard * T0], t[t > discard * T0]
    up, armed = [], False
    for j in range(1, len(c)):
        if c[j] < 0.0768:
            armed = True
        elif armed and c[j - 1] < 0.0868 <= c[j]:
            up.append(j)
            armed = False
    per = float(np.mean(np.diff(t[up])))
    cm = np.convolve(c, np.ones(5) / 5, mode="same")
    mins = [cm[a:b].min() for a, b in zip(up[:-1], up[1:])]
    maxs = [cm[a:b].max() for a, b in zip(up[:-1], up[1:])]
    lo, hi = float(np.mean(mins)), float(np.mean(maxs))
    ok = abs(per - 6.3524) <= 0.03 * 6.3524 and abs(lo - 0.0545) <= 0.1 * 0.0545 and abs(hi - 0.119) <= 0.1 * 0.119
    return dict(period=per, n_cycles=len(up) - 1, range=[lo, hi], events=ev, PASS=bool(ok))


# ---------------- H2 ----------------
def four_state_pi(k):
    Q = np.zeros((4, 4))
    Q[0, 2], Q[0, 1], Q[0, 3] = k[0], k[1], k[5]
    Q[1, 0] = k[8]
    Q[2, 1], Q[2, 0] = k[3], k[4]
    Q[3, 1] = k[6]
    np.fill_diagonal(Q, -Q.sum(1))
    A = np.vstack([Q.T, np.ones(4)])
    return np.linalg.lstsq(A, np.r_[np.zeros(4), 1.0], rcond=None)[0]


def h2_test(counts, N, pi):
    n = counts.sum(0).astype(float)
    tot = n.sum()
    exp = tot * pi
    x2 = float(((n - exp) ** 2 / exp).sum())
    p = float(chi2.sf(x2, 3))
    se = np.sqrt(pi * (1 - pi) / tot)
    z = (n / tot - pi) / se
    return dict(fractions=(n / tot).tolist(), exact=pi.tolist(), chi2=x2, p=p, z=z.tolist(),
                PASS=bool(p >= 0.001 and np.all(np.abs(z) <= 4)))


def h2(g, N=10000):
    k = k_of(0.0).copy()
    k[2] = 0.0
    k[9] = 0.0
    pi = four_state_pi(k)
    r = run_graph(g, 0.0, seed_of("H2", "S"), t_max=2050, dt=50, fields=False, k=k)
    cg = r["gcount"][1:41]  # t = 100, ..., 2050
    X, _ = run_lumped(N, 0.0, seed_of("H2", "K"), 2050, 50, k=k)
    ck = X[1:41]
    a, b = h2_test(cg, N, pi), h2_test(ck, N, pi)
    return dict(S=a, K=b, n_snap=int(len(cg)), PASS=bool(a["PASS"] and b["PASS"]))


# ---------------- H3 ----------------
def octahedron():
    E = [(a, b) for a in range(6) for b in range(a + 1, 6) if b != (a ^ 1)]
    off, nbr = csr(6, E)
    return dict(name="oct", N=6, off=off, nbr=nbr, tri=None, surface=False)


def exact_oct(k):
    g = octahedron()
    N, off, nbr = 6, g["off"], g["nbr"]
    S = 4 ** N
    rows, cols, vals = [], [], []
    for s in range(S):
        r = [(s >> (2 * i)) & 3 for i in range(N)]
        for i in range(N):
            nc = sum(r[nbr[e]] == 0 for e in range(off[i], off[i + 1]))
            x = nc / (off[i + 1] - off[i])
            if r[i] == 0:
                tr = [(2, k[0]), (1, k[1] + k[9] * Fj(x, KC)), (3, k[5])]
            elif r[i] == 1:
                tr = [(0, k[8] + k[2] * Fj(x, KR))]
            elif r[i] == 2:
                tr = [(1, k[3]), (0, k[4])]
            else:
                tr = [(1, k[6])]
            for rn, rate in tr:
                s2 = s - (r[i] << (2 * i)) + (rn << (2 * i))
                rows.append(s); cols.append(s2); vals.append(float(rate))
    Q = sparse.csr_matrix((vals, (rows, cols)), shape=(S, S))
    Q = Q - sparse.diags(np.asarray(Q.sum(1)).ravel())
    A = Q.T.tolil()
    A[0, :] = np.ones(S)
    b = np.zeros(S); b[0] = 1.0
    p = spsolve(A.tocsr(), b)
    st = np.array([[((s >> (2 * i)) & 3) for i in range(N)] for s in range(S)])
    fr = np.stack([(st == q).mean(1) for q in range(4)], 1)
    return np.r_[p @ fr, p @ fr[:, 0] ** 2]


def h3(t_max=2e5, nbatch=50):
    k = k_of(0.0)
    g = octahedron()
    ex = exact_oct(k)
    r = run_graph(g, 0.0, seed_of("H3"), t_max=t_max, dt=t_max, fields=False, nbatch=nbatch)
    tw = r["tw"]
    bm = tw[:, 1:] / tw[:, :1]
    mean = tw[:, 1:].sum(0) / tw[:, 0].sum()
    se = bm.std(0, ddof=1) / np.sqrt(nbatch)
    z = (mean - ex) / se
    return dict(names=["c", "v", "l", "p", "c^2"], sim=mean.tolist(), exact=ex.tolist(), se=se.tolist(),
                z=z.tolist(), events=r["events"], PASS=bool(np.all(np.abs(z) <= 4)))


# ---------------- planted fields ----------------
def vortex_phase(P, pts):
    """pts: list of (x, y, s) in the grid labels; returns phases on all vertices (apex = circular mean of boundary)."""
    n = P["n"]
    ii, jj = np.meshgrid(np.arange(n + 1), np.arange(n + 1), indexing="ij")
    phi = np.zeros((n + 1) ** 2 + 1)
    g = np.zeros((n + 1, n + 1))
    for x, y, s in pts:
        g += s * np.arctan2(jj - y, ii - x)
    phi[:-1] = g.ravel()
    bph = phi[P["boundary"]]
    phi[-1] = math.atan2(np.sin(bph).mean(), np.cos(bph).mean())
    return phi, arc_span(bph)


def arc_span(a):
    a = np.sort(np.mod(a, 2 * np.pi))
    gaps = np.diff(np.r_[a, a[0] + 2 * np.pi])
    return float(2 * np.pi - gaps.max())


def L_face(n, i, j):
    return 2 * (i * n + j)


def U_face(n, i, j):
    return 2 * (i * n + j) + 1


def p1(n_random=20, seed=None):
    P = planted_sphere(60)
    n = P["n"]
    rng = random.Random(seed_of("P1") if seed is None else seed)
    configs = [[(15, 15, 1), (45, 30, 1), (20, 45, 1), (30, 15, -1), (45, 45, -1), (15, 30, -1)]]
    redraws = 0
    while len(configs) < 1 + n_random:
        m = [2, 4, 6][(len(configs) - 1) % 3]
        cells = []
        while len(cells) < m:
            c = (rng.randint(12, 47), rng.randint(12, 47))
            if all(math.hypot(c[0] - d[0], c[1] - d[1]) >= 10 for d in cells):
                cells.append(c)
        cfg = [(a, b, 1 if q < m // 2 else -1) for q, (a, b) in enumerate(cells)]
        phi, span = vortex_phase(P, [(a + 2 / 3, b + 1 / 3, s) for a, b, s in cfg])
        if span >= np.pi:
            redraws += 1
            continue
        configs.append(cfg)
    res = []
    for cfg in configs:
        phi, span = vortex_phase(P, [(a + 2 / 3, b + 1 / 3, s) for a, b, s in cfg])
        w = detect(P["tri"], phi)
        exp = np.zeros(len(P["tri"]), np.int8)
        for a, b, s in cfg:
            exp[L_face(n, a, b)] = s
        res.append(dict(n_vortex=len(cfg), exact_match=bool(np.array_equal(w, exp)), total_w=int(w.sum()),
                        boundary_span=span, n_detected=int(np.count_nonzero(w))))
    # identity on random fields too
    rng2 = np.random.default_rng(seed_of("P1", "id"))
    idv = sum(int(detect(P["tri"], rng2.uniform(-np.pi, np.pi, P["N"])).sum() != 0) for _ in range(200))
    ok = all(r["exact_match"] and r["total_w"] == 0 for r in res) and idv == 0
    return dict(configs=res, redraws=redraws, identity_violations_random=idv, PASS=bool(ok))


def frames_to_run(tri, phis):
    dl, sl, cnt, tw = [], [], [0], []
    for phi in phis:
        w = detect(tri, phi)
        nz = np.nonzero(w)[0]
        dl.append(nz.astype(np.int32)); sl.append(w[nz]); cnt.append(len(nz)); tw.append(int(w.sum()))
    return dict(doff=np.cumsum(cnt).astype(np.int64), dtri=np.concatenate(dl), dsgn=np.concatenate(sl),
                totw=np.array(tw))


def p2_on(g, label, nframes=NFRAMES - F_WIN0, reps=3):
    out = []
    dens = []
    for rep in range(reps):
        rng = np.random.default_rng(seed_of("P2", label, rep))
        run = frames_to_run(g["tri"], (rng.uniform(-np.pi, np.pi, g["N"]) for _ in range(nframes)))
        tr = track(g, run, f0=0, f1=nframes)
        d = np.diff(run["doff"]) / len(g["tri"])
        dens.append(d)
        out.append(dict(longest=float(tr["life"].max()), n_tracks=int(len(tr["start"])),
                        has_long=bool(tr["life"].max() >= LONG - 1e-9),
                        identity_violations=int(np.count_nonzero(run["totw"]))))
    d = np.concatenate(dens)
    mean, se = float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d)))
    n_long = sum(o["has_long"] for o in out)
    ok = abs(mean - 0.25) <= 4 * se and n_long < 2 and all(o["identity_violations"] == 0 for o in out)
    return dict(reps=out, density=mean, se=se, expected=0.25, z=(mean - 0.25) / se, d1_reps_with_long=n_long,
                d1_criterion="FAILS" if n_long < 2 else "passes", PASS=bool(ok))


def p3():
    P = planted_sphere(60)
    n = P["n"]

    def path(k, sgn):
        if sgn > 0:
            return (L_face(n, 14 + k // 2, 20), (14 + k // 2 + 2 / 3, 20 + 1 / 3)) if k % 2 == 0 else \
                (U_face(n, 15 + (k - 1) // 2, 20), (15 + (k - 1) // 2 + 1 / 3, 20 + 2 / 3))
        return (L_face(n, 46 - k // 2, 26), (46 - k // 2 + 2 / 3, 26 + 1 / 3)) if k % 2 == 0 else \
            (U_face(n, 46 - (k - 1) // 2, 26), (46 - (k - 1) // 2 + 1 / 3, 26 + 2 / 3))
    phis, plan = [], []
    mind = 1e9
    for f in range(320):
        fp, xp = path(f // 5, 1)
        fm, xm = path(f // 5, -1)
        mind = min(mind, math.hypot(xp[0] - xm[0], xp[1] - xm[1]))
        phi, _ = vortex_phase(P, [(xp[0], xp[1], 1), (xm[0], xm[1], -1)])
        phis.append(phi); plan.append((fp, fm))
    run = frames_to_run(P["tri"], phis)
    tr = track(P, run, f0=0, f1=320)
    ok_faces = True
    swaps = 0
    for f in range(320):
        a, b = run["doff"][f], run["doff"][f + 1]
        got = {int(s): (int(t), int(tr["tid"][i])) for i, t, s in zip(range(a, b), run["dtri"][a:b], run["dsgn"][a:b])}
        if b - a != 2 or got.get(1, (None,))[0] != plan[f][0] or got.get(-1, (None,))[0] != plan[f][1]:
            ok_faces = False
        else:
            if tr["sign"][got[1][1]] != 1 or tr["sign"][got[-1][1]] != -1:
                swaps += 1
    nt = len(tr["start"])
    ok = ok_faces and nt == 2 and np.all(tr["start"] == 0) and np.all(tr["end"] == 319) and swaps == 0 and \
        np.all(tr["life"] >= LONG - 1e-9) and np.count_nonzero(run["totw"]) == 0
    return dict(n_tracks=int(nt), lifetimes=tr["life"].tolist(), on_planted_faces=bool(ok_faces), swaps=swaps,
                min_pair_distance=mind, PASS=bool(ok))


def main():
    c0 = cpu_s()
    out = {}
    path = os.path.join(EVID, "g1.json")
    gS = graph_S(10000, seed_of("S", 0))
    steps = [("H1", lambda: h1()), ("H2", lambda: h2(gS)), ("H3", lambda: h3()), ("P1", lambda: p1()),
             ("P2_planted", lambda: p2_on(planted_sphere(60), "planted")), ("P2_S", lambda: p2_on(gS, "S")),
             ("P3", lambda: p3())]
    for name, fn in steps:
        c = cpu_s()
        out[name] = fn()
        out[name]["cpu_s"] = cpu_s() - c
        print(name, out[name]["PASS"], {k: v for k, v in out[name].items() if k not in ("configs", "reps")},
              flush=True)
        json.dump(out, open(path, "w"), indent=1)
    out["P2"] = dict(PASS=bool(out["P2_planted"]["PASS"] and out["P2_S"]["PASS"]))
    out["harness_PASS"] = all(out[x]["PASS"] for x in ("H1", "H2", "H3", "P1", "P2", "P3"))
    out["cpu_s_total"] = cpu_s() - c0
    json.dump(out, open(path, "w"), indent=1)
    print("HARNESS", out["harness_PASS"], "cpu", out["cpu_s_total"])


if __name__ == "__main__":
    main()
