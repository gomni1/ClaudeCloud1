"""Phase, winding, defects, tracks and synchrony.

Phase and amplitude come from each site's own ensemble -- no spatial smoothing.
A triangle's winding is (1/2pi) times the sum of its three wrapped phase
differences and lies in {-1,0,+1}; a defect is a triangle with winding != 0.
Hop distance between two triangles is the least graph hop distance between a
vertex of one and a vertex of the other.
"""
import numpy as np
from numba import njit

TWO_PI = 2.0 * np.pi


@njit(cache=True)
def windings(phase, tri, out):
    """Winding of every triangle for one frame."""
    for t in range(tri.shape[0]):
        a = phase[tri[t, 0]]; b = phase[tri[t, 1]]; c = phase[tri[t, 2]]
        s = 0.0
        for d in (b - a, c - b, a - c):
            while d > np.pi:
                d -= TWO_PI
            while d <= -np.pi:
                d += TWO_PI
            s += d
        out[t] = np.int8(round(s / TWO_PI))
    return out


@njit(cache=True)
def match_frames(cur_tri, cur_sign, nxt_tri, nxt_sign, nb_ptr, nb_idx, pos_of,
                 match_c, match_n):
    """Strict same-sign matching within hop distance 2, unique in both directions.

    pos_of[t] is the index of a next-frame defect on triangle t, or -1.
    A pair is accepted only when each is the other's single candidate.
    """
    nc = cur_tri.shape[0]; nn = nxt_tri.shape[0]
    cand = np.full(nc, -1, np.int32)
    ncand = np.zeros(nc, np.int32)
    ndeg = np.zeros(nn, np.int32)
    for i in range(nc):
        t = cur_tri[i]
        for k in range(nb_ptr[t], nb_ptr[t + 1]):
            j = pos_of[nb_idx[k]]
            if j >= 0 and nxt_sign[j] == cur_sign[i]:
                ncand[i] += 1
                cand[i] = j
                ndeg[j] += 1
    for i in range(nc):
        match_c[i] = -1
    for j in range(nn):
        match_n[j] = -1
    for i in range(nc):
        if ncand[i] == 1:
            j = cand[i]
            if ndeg[j] == 1:
                match_c[i] = j
                match_n[j] = i
    return 0


@njit(cache=True)
def tri_hop(tri, D, a, b):
    """Least hop distance between the vertex sets of triangles a and b."""
    m = 127
    for u in range(3):
        for v in range(3):
            d = D[tri[a, u], tri[b, v]]
            if d < m:
                m = d
    return m


def build_tri_neighbourhood(tri, D, radius=2):
    """For each triangle, the triangles within `radius` hops, as a CSR list."""
    nT = tri.shape[0]
    N = D.shape[0]
    inc = [[] for _ in range(N)]
    for t in range(nT):
        for u in tri[t]:
            inc[u].append(t)
    ptr = np.zeros(nT + 1, np.int64)
    rows = []
    for t in range(nT):
        near = np.unique(np.concatenate([np.where(D[u] <= radius)[0] for u in tri[t]]))
        cand = set()
        for u in near:
            cand.update(inc[u])
        r = np.array(sorted(cand), np.int32)
        rows.append(r)
        ptr[t + 1] = ptr[t] + r.size
    return ptr, np.concatenate(rows)


def synchrony(phase):
    return float(abs(np.exp(1j * phase).mean()))


def period_stats(ph, dt_rec):
    """Mean period and its coefficient of variation from one phase series."""
    u = np.unwrap(np.asarray(ph, float))
    if u[-1] < u[0]:
        u = -u
    lo = np.ceil(u[0] / TWO_PI); hi = np.floor(u[-1] / TWO_PI)
    if hi - lo < 2:
        return np.nan, np.nan, 0
    lv = np.arange(lo, hi + 1) * TWO_PI
    idx = np.searchsorted(u, lv)
    ts = []
    for L, i in zip(lv, idx):
        if 0 < i < len(u):
            f = (L - u[i - 1]) / (u[i] - u[i - 1])
            ts.append((i - 1 + f) * dt_rec)
    iv = np.diff(np.array(ts))
    if iv.size < 2:
        return np.nan, np.nan, 0
    return float(iv.mean()), float(iv.std(ddof=1) / iv.mean()), int(iv.size)


class Tracker:
    """Incremental defect tracks across frames."""

    def __init__(self, keep_frames):
        self.keep = keep_frames      # keep trajectories at least this long
        self.active = {}             # next-frame defect index -> track dict
        self.done = []
        self.births = []             # (frame, triangle, sign)
        self.deaths = []

    def start(self, frame, tris, signs, amps):
        self.active = {}
        for i, (t, s) in enumerate(zip(tris, signs)):
            self.active[i] = dict(start=frame, sign=int(s), tri=[int(t)],
                                  amp=float(amps[i]), n=1)

    def step(self, frame, cur_tris, cur_signs, nxt_tris, nxt_signs, nxt_amps,
             match_c, match_n):
        new_active = {}
        for i, tr in self.active.items():
            j = match_c[i]
            if j >= 0:
                tr['tri'].append(int(nxt_tris[j]))
                tr['amp'] += float(nxt_amps[j]); tr['n'] += 1
                new_active[j] = tr
            else:
                self._retire(tr)
                self.deaths.append((frame, int(cur_tris[i]), int(cur_signs[i])))
        for j in range(len(nxt_tris)):
            if match_n[j] < 0:
                new_active[j] = dict(start=frame + 1, sign=int(nxt_signs[j]),
                                     tri=[int(nxt_tris[j])], amp=float(nxt_amps[j]), n=1)
                self.births.append((frame + 1, int(nxt_tris[j]), int(nxt_signs[j])))
        self.active = new_active

    def _retire(self, tr):
        L = len(tr['tri'])
        if L >= self.keep:
            self.done.append(tr)
        else:
            self.done.append(dict(start=tr['start'], sign=tr['sign'], tri=None,
                                  length=L, amp=tr['amp'], n=tr['n']))

    def finish(self):
        for tr in self.active.values():
            self._retire(tr)
        self.active = {}
        for tr in self.done:
            if 'length' not in tr:
                tr['length'] = len(tr['tri'])
        return self.done
