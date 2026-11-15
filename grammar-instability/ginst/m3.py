"""M3: mobility instability tests at a stable balance (SPEC §5)."""
import itertools
import math

import mpmath as mp
import numpy as np

S_GRID = np.logspace(-5, 5, 201)
RHO_GRID = np.logspace(-4, 4, 81)
RNG_SEED = 515


def random_D(n=4, count=200, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    return 10.0 ** rng.uniform(-4, 4, size=(count, n))


def two_class_D(n=4, which=1):
    out = np.ones((len(RHO_GRID), n))
    out[:, which] = RHO_GRID
    return out


def principal_minors(M, closed=False, mp_digits=50):
    """All principal minors of M (proper ones only when closed); 50-digit recompute when ill-conditioned."""
    n = M.shape[0]
    res = {}
    used_mp = False
    sizes = range(1, n) if closed else range(1, n + 1)
    for r in sizes:
        for S in itertools.combinations(range(n), r):
            sub = M[np.ix_(S, S)]
            v = float(np.linalg.det(sub))
            scale = float(np.prod(np.abs(sub).sum(axis=1)))
            if abs(v) < 1e-10 * scale:
                mp.mp.dps = mp_digits
                v = float(mp.det(mp.matrix(sub.tolist())))
                used_mp = True
            res[S] = v
    return res, used_mp


def pmatrix_test(J, closed=False):
    mins, used_mp = principal_minors(-J, closed)
    neg = {"".join("CVLP"[i] for i in S): v for S, v in mins.items() if not v > 0}
    return dict(is_P=not neg, failing=neg, min_minor=float(min(mins.values())), used_mp=used_mp)


def _eig_grid(J, Ds, s_grid):
    """eigenvalues of J - s D for every D (rows of Ds) and s: shape (nD, ns, n)."""
    M = J[None, None, :, :] - s_grid[None, :, None, None] * (Ds[:, None, :, None] * np.eye(J.shape[0])[None, None])
    return np.linalg.eigvals(M)


def _scan(J, Ds, s_grid, scale):
    ev = _eig_grid(J, Ds, s_grid)
    cplx = np.abs(ev.imag) > 1e-9 * scale
    re_c = np.where(cplx, ev.real, -np.inf).max(axis=2)
    re_r = np.where(~cplx, ev.real, -np.inf).max(axis=2)
    return re_c, re_r


def _golden_max(fun, lo, hi, iters=80):
    """Maximise fun over [lo, hi] (log s)."""
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = fun(c), fun(d)
    for _ in range(iters):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = fun(d)
    x = c if fc > fd else d
    return x, max(fc, fd)


def _refine(J, D, ls0, kind, scale):
    dls = (np.log(S_GRID[1]) - np.log(S_GRID[0]))

    def fun(ls):
        ev = np.linalg.eigvals(J - math.exp(ls) * np.diag(D))
        c = np.abs(ev.imag) > 1e-9 * scale
        sel = ev.real[c] if kind == "osc" else ev.real[~c]
        return float(sel.max()) if len(sel) else -np.inf

    x, v = _golden_max(fun, ls0 - dls, ls0 + dls)
    return dict(s=math.exp(x), value=v)


def mobility_tests(J, closed=False, n_random=200, two_class_index=1):
    n = J.shape[0]
    scale = float(np.max(np.abs(np.linalg.eigvals(J))))
    thr = 1e-9 * scale
    pm = pmatrix_test(J, closed)
    Dr = random_D(n, n_random)
    Dt = two_class_D(n, two_class_index)
    out = dict(pmatrix=pm, scale=scale)
    for name, Ds in (("random", Dr), ("two_class", Dt)):
        re_c, re_r = _scan(J, Ds, S_GRID, scale)
        iD, iS = np.unravel_index(np.argmax(re_c), re_c.shape)
        G = float(re_c[iD, iS])
        rec = dict(Gamma_grid=G, D=Ds[iD].tolist(), s=float(S_GRID[iS]))
        if np.isfinite(G):
            rf = _refine(J, Ds[iD], math.log(S_GRID[iS]), "osc", scale)
            rec.update(Gamma=max(G, rf["value"]), s_ref=rf["s"])
        else:
            rec["Gamma"] = G
        rec["osc_hit"] = bool(rec["Gamma"] > thr)
        jD, jS = np.unravel_index(np.argmax(re_r), re_r.shape)
        R = float(re_r[jD, jS])
        rec_s = dict(maxre_real_grid=R, D=Ds[jD].tolist(), s=float(S_GRID[jS]))
        if np.isfinite(R) and R > -np.inf:
            rf = _refine(J, Ds[jD], math.log(S_GRID[jS]), "stat", scale)
            rec_s.update(maxre_real=max(R, rf["value"]), s_ref=rf["s"])
        else:
            rec_s["maxre_real"] = R
        rec_s["stat_hit"] = bool(rec_s["maxre_real"] > thr)
        out[name] = dict(osc=rec, stat=rec_s)
        if name == "two_class" and rec_s["stat_hit"]:
            out["critical_rho"] = critical_ratio(J, two_class_index, scale)
    out["osc_hit"] = out["random"]["osc"]["osc_hit"] or out["two_class"]["osc"]["osc_hit"]
    out["stat_hit"] = out["random"]["stat"]["stat_hit"] or out["two_class"]["stat"]["stat_hit"]
    return out


def max_real_over_s(J, D, scale):
    re_c, re_r = _scan(J, D[None, :], S_GRID, scale)
    i = int(np.argmax(re_r[0]))
    best = float(re_r[0, i])
    if np.isfinite(best):
        best = max(best, _refine(J, D, math.log(S_GRID[i]), "stat", scale)["value"])
    return best


def critical_ratio(J, which, scale, rel=1e-6):
    """Bisection on rho for the stationary-instability boundary of D = diag(1,..,rho,..,1)."""
    n = J.shape[0]

    def D_of(rho):
        D = np.ones(n)
        D[which] = rho
        return D

    vals = [max_real_over_s(J, D_of(r), scale) for r in RHO_GRID]
    unstable = [v > 1e-9 * scale for v in vals]
    idx = [i for i in range(1, len(RHO_GRID)) if unstable[i] != unstable[i - 1]]
    if not idx:
        return dict(found=False)
    i = idx[0]
    lo, hi = math.log(RHO_GRID[i - 1]), math.log(RHO_GRID[i])
    ulo = unstable[i - 1]
    while hi - lo > rel:
        mid = 0.5 * (lo + hi)
        um = max_real_over_s(J, D_of(math.exp(mid)), scale) > 1e-9 * scale
        if um == ulo:
            lo = mid
        else:
            hi = mid
    return dict(found=True, rho_c=math.exp(0.5 * (lo + hi)), unstable_above=not ulo)
