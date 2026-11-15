"""Combinatorial graph construction. No coordinates are used anywhere.

S  : random triangulated sphere -- tetrahedron, vertex insertion into uniformly
     chosen faces up to N, then 20*E random edge flips (multi-edges and degree
     below 3 rejected). Faces are kept consistently oriented throughout, which
     is what makes the total winding identically zero (harness H3).
R  : random 8-regular graph (pairing model, repaired by double-edge swaps).
C5 : ring of N sites joined to the 4 nearest on each side, Watts-Strogatz
     rewiring 0.05.

For S the triangle set is the 2N-4 oriented faces of the triangulation. R and
C5 are not surfaces, so for them the triangle set is every 3-clique.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


# ---------------------------------------------------------------- sphere ----
def build_sphere(N, seed=0):
    rng = np.random.default_rng(seed)
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)]   # oriented tetrahedron
    adj = {i: set() for i in range(4)}
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            adj[a].add(b); adj[b].add(a)
    nv = 4
    while nv < N:
        fi = int(rng.integers(len(faces)))
        a, b, c = faces[fi]
        d = nv; nv += 1
        adj[d] = {a, b, c}
        for u in (a, b, c):
            adj[u].add(d)
        faces[fi] = (a, b, d)
        faces.append((b, c, d)); faces.append((c, a, d))

    # edge -> the two oriented faces carrying it
    def build_edge_map(faces):
        em = {}
        for i, f in enumerate(faces):
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                em[(a, b)] = i
        return em
    em = build_edge_map(faces)
    E = 3 * N - 6
    n_flip = 20 * E
    done = 0
    attempts = 0
    while done < n_flip and attempts < 40 * n_flip:
        attempts += 1
        fi = int(rng.integers(len(faces)))
        f = faces[fi]
        e = int(rng.integers(3))
        a, b = f[e], f[(e + 1) % 3]
        c = f[(e + 2) % 3]
        fj = em.get((b, a))
        if fj is None:
            continue
        g = faces[fj]
        d = [x for x in g if x not in (a, b)]
        if len(d) != 1:
            continue
        d = d[0]
        if d == c or d in adj[c]:
            continue                      # would create a multi-edge
        if len(adj[a]) <= 3 or len(adj[b]) <= 3:
            continue                      # would drop a degree below 3
        # quad boundary b->c, c->a, a->d, d->b ; swap diagonal a-b for c-d
        faces[fi] = (c, a, d)
        faces[fj] = (c, d, b)
        adj[a].discard(b); adj[b].discard(a)
        adj[c].add(d); adj[d].add(c)
        for ff in (fi, fj):
            t = faces[ff]
            for u, v in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                em[(u, v)] = ff
        em.pop((a, b), None); em.pop((b, a), None)
        done += 1
    assert done == n_flip, f"only {done}/{n_flip} flips accepted"

    # orientation check: every directed edge carried exactly once
    seen = set()
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            assert (a, b) not in seen, "orientation is not consistent"
            seen.add((a, b))
    assert len(faces) == 2 * N - 4, (len(faces), 2 * N - 4)
    return adj_to_csr(adj, N), np.array(faces, dtype=np.int32)


# ------------------------------------------------------------- 8-regular ----
def build_regular(N, deg=8, seed=0):
    rng = np.random.default_rng(seed)
    stubs = np.repeat(np.arange(N), deg)
    rng.shuffle(stubs)
    edges = stubs.reshape(-1, 2)
    E = edges.shape[0]

    def bad(edges):
        s = set(); b = []
        for i, (u, v) in enumerate(edges):
            if u == v or (min(u, v), max(u, v)) in s:
                b.append(i)
            else:
                s.add((min(u, v), max(u, v)))
        return b, s
    for _ in range(400):
        b, s = bad(edges)
        if not b:
            break
        for i in b:
            for _ in range(200):
                j = int(rng.integers(E))
                if j == i:
                    continue
                u1, v1 = edges[i]; u2, v2 = edges[j]
                nu, nv = (u1, v2), (u2, v1)
                if nu[0] == nu[1] or nv[0] == nv[1]:
                    continue
                k1 = (min(nu), max(nu)); k2 = (min(nv), max(nv))
                if k1 in s or k2 in s or k1 == k2:
                    continue
                edges[i] = nu; edges[j] = nv
                break
    b, _ = bad(edges)
    assert not b, f"{len(b)} bad edges remain"
    adj = {i: set() for i in range(N)}
    for u, v in edges:
        adj[u].add(int(v)); adj[v].add(int(u))
    return adj_to_csr(adj, N), None


# -------------------------------------------------------------- WS ring ----
def build_ring(N, k_side=4, p=0.05, seed=0):
    rng = np.random.default_rng(seed)
    adj = {i: set() for i in range(N)}
    edges = []
    for i in range(N):
        for d in range(1, k_side + 1):
            j = (i + d) % N
            adj[i].add(j); adj[j].add(i); edges.append([i, j])
    for e in edges:
        if rng.random() < p:
            u, v = e
            for _ in range(100):
                w = int(rng.integers(N))
                if w != u and w not in adj[u]:
                    adj[u].discard(v); adj[v].discard(u)
                    adj[u].add(w); adj[w].add(u)
                    break
    return adj_to_csr(adj, N), None


# ------------------------------------------------------------- utilities ----
def adj_to_csr(adj, N):
    indptr = np.zeros(N + 1, np.int32)
    for i in range(N):
        indptr[i + 1] = indptr[i] + len(adj[i])
    indices = np.empty(indptr[-1], np.int32)
    for i in range(N):
        indices[indptr[i]:indptr[i + 1]] = sorted(adj[i])
    return indptr, indices


def all_triangles(indptr, indices):
    """Every 3-clique, each once, as an (n,3) int32 array."""
    N = len(indptr) - 1
    nb = [set(indices[indptr[i]:indptr[i + 1]].tolist()) for i in range(N)]
    out = []
    for u in range(N):
        for v in nb[u]:
            if v <= u:
                continue
            for w in nb[u] & nb[v]:
                if w > v:
                    out.append((u, v, w))
    return np.array(out, dtype=np.int32)


def metrics(indptr, indices, name, ball_frac=0.5):
    """N, mean degree, mean local clustering, diameter, and the growth exponent
    d_g from mean ball size against hop radius."""
    N = len(indptr) - 1
    deg = np.diff(indptr)
    nb = [set(indices[indptr[i]:indptr[i + 1]].tolist()) for i in range(N)]
    cl = []
    for i in range(N):
        d = deg[i]
        if d < 2:
            cl.append(0.0); continue
        links = sum(1 for a in nb[i] for b in nb[i] if a < b and b in nb[a])
        cl.append(2.0 * links / (d * (d - 1)))
    A = csr_matrix((np.ones(len(indices)), indices, indptr), shape=(N, N))
    D = shortest_path(A, method='D', unweighted=True, directed=False)
    diam = int(D[np.isfinite(D)].max())
    rs = np.arange(1, diam + 1)
    ball = np.array([float((D <= r).sum()) / N for r in rs])
    keep = ball <= ball_frac * N
    if keep.sum() >= 3:
        d_g = float(np.polyfit(np.log(rs[keep]), np.log(ball[keep]), 1)[0])
    else:
        d_g = float('nan')
    return dict(name=name, N=N, mean_degree=float(deg.mean()),
                min_degree=int(deg.min()), max_degree=int(deg.max()),
                clustering=float(np.mean(cl)), diameter=diam, d_g=d_g,
                ball_radii=rs.tolist(), ball_sizes=ball.tolist(),
                n_fit=int(keep.sum()))
