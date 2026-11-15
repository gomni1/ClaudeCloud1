"""Geometric minimum action method (SPEC §5, M4; Heymann and Vanden-Eijnden 2008).

H(x, theta) = sum_r r_r(x) (exp(<theta, nu_r>) - 1).
Local geometric action l(x, y) = sup{<theta, y> : H(x, theta) <= 0}, solved by damped
Newton on grad_theta H = lam * y, H = 0 (lam > 0).  Discrete action
S_N = sum_i l((phi_i + phi_{i+1})/2, phi_{i+1} - phi_i), minimised by L-BFGS-B with
periodic reparametrisation to equal Euclidean arclength."""
import numpy as np
from scipy.optimize import minimize

from . import gmam_nb, model

LOWER = 1e-12


class Network:
    def __init__(self, rates, rate_grads, nu, nb_id=None):
        self.rates, self.rate_grads, self.nu = rates, rate_grads, np.asarray(nu, float)
        self.dim = self.nu.shape[1]
        self.nb_id = nb_id  # model id of the numba kernel (gmam_nb), or None for numpy only

    def parts(self, x, th, grads=False):
        r = self.rates(x)  # (M, R)
        E = np.exp(np.clip(th @ self.nu.T, -700, 700))  # (M, R)
        rE = r * E
        H = np.sum(r * (E - 1.0), axis=1)
        Hth = rE @ self.nu
        Hthth = np.einsum("mr,ri,rj->mij", rE, self.nu, self.nu)
        if not grads:
            return H, Hth, Hthth
        Hx = np.einsum("mr,mrj->mj", E - 1.0, self.rate_grads(x))
        return H, Hth, Hthth, Hx


def grammar(law):
    return Network(lambda x: model.rates(x, law), lambda x: model.rate_grads(x, law), model.NU,
                   nb_id={"MA": 0, "TH": 1}[law])


def immigration_death(dim=1):
    """dim independent copies of 0 -> X (rate 1), X -> 0 (rate x)."""
    nu = np.vstack([np.eye(dim), -np.eye(dim)])

    def rates(x):
        return np.concatenate([np.ones_like(x), x], axis=-1)

    def rate_grads(x):
        g = np.zeros(x.shape[:-1] + (2 * dim, dim))
        for i in range(dim):
            g[..., dim + i, i] = 1.0
        return g

    return Network(rates, rate_grads, nu, nb_id={1: 2, 2: 3}.get(dim))


class InnerFailure(RuntimeError):
    pass


def _theta_of_lam(net, x, y, lam, th, tol=1e-13, maxit=200):
    """argmin_theta H(x, theta) - lam <theta, y> (strictly convex), damped Newton."""
    x1 = x[None]
    for _ in range(maxit):
        H, Hth, Hthth = net.parts(x1, th[None])
        f = H[0] - lam * th @ y
        g = Hth[0] - lam * y
        if np.linalg.norm(g) <= tol * (1.0 + np.abs(Hth[0]).sum() + abs(lam) * np.abs(y).sum()):
            return th
        try:
            step = -np.linalg.solve(Hthth[0], g)
        except np.linalg.LinAlgError:
            step = -np.linalg.lstsq(Hthth[0], g, rcond=None)[0]
        t = 1.0
        for _ls in range(60):
            thn = th + t * step
            Hn = net.parts(x1, thn[None])[0][0]
            fn = Hn - lam * thn @ y
            if np.isfinite(fn) and fn <= f + 1e-4 * t * (g @ step):
                break
            t *= 0.5
        th = thn
    return th


def _nested(net, x, y, th, lam):
    """Robust fallback: g(lam) = H(theta(lam)) is increasing in lam > 0; root in log lam."""
    from scipy.optimize import brentq

    cache = {"th": th.copy()}

    def g(loglam):
        t = _theta_of_lam(net, x, y, np.exp(loglam), cache["th"].copy())
        cache["th"] = t
        return net.parts(x[None], t[None])[0][0]

    a = np.log(lam) if lam > 0 else 0.0
    ga = g(a)
    b, gb = a, ga
    step = 1.0
    for _ in range(200):
        if (ga < 0) != (gb < 0):
            break
        if gb < 0:
            b += step
        else:
            b -= step
        step *= 1.5
        gb = g(b)
    else:
        raise InnerFailure("could not bracket lambda")
    lo, hi = (a, b) if a < b else (b, a)
    root = brentq(g, lo, hi, xtol=1e-14, rtol=4 * np.finfo(float).eps, maxiter=500)
    lam = np.exp(root)
    th = _theta_of_lam(net, x, y, lam, cache["th"].copy())
    return th, lam


def local_action(net, x, y, th0=None, lam0=None, tol=1e-12, maxit=120):
    """Vectorised over segments.  Returns l, theta, lam (lam = 0 where y = 0).

    For fixed lam, theta(lam) minimises the convex H - lam <theta, y> (damped Newton);
    G(mu) = H(theta(e^mu)) is increasing in mu = log lam, and its root is found by
    Newton steps in mu safeguarded by a bracket."""
    M, d = y.shape
    zero = np.linalg.norm(y, axis=1) < 1e-300
    th = np.zeros((M, d)) if th0 is None else th0.copy()
    lam = np.zeros(M) if lam0 is None else lam0.copy()
    cold = ~zero & ((lam <= 0) | (th0 is None))
    idx = np.flatnonzero(cold)
    if len(idx):  # cold start from the quadratic (Gaussian) approximation
        r = net.rates(x[idx])
        b = r @ net.nu
        A = np.einsum("mr,ri,rj->mij", r, net.nu, net.nu) + 1e-14 * np.eye(d)
        Ainv_b = np.linalg.solve(A, b[..., None])[..., 0]
        Ainv_y = np.linalg.solve(A, y[idx][..., None])[..., 0]
        lq = np.sqrt(np.maximum(np.sum(b * Ainv_b, 1), 0) / np.maximum(np.sum(y[idx] * Ainv_y, 1), 1e-300))
        lq = np.maximum(lq, 1e-12)
        th[idx] = lq[:, None] * Ainv_y - Ainv_b
        lam[idx] = lq
    th[zero] = 0.0
    lam[zero] = 0.0
    ids = np.flatnonzero(~zero)
    mu = np.full(M, -np.inf)
    mu[ids] = np.log(lam[ids])
    lo = np.full(M, -np.inf)
    hi = np.full(M, np.inf)
    active = ids.copy()
    for _ in range(maxit):
        if len(active) == 0:
            break
        xa, ya = x[active], y[active]
        la = np.exp(mu[active])
        ta = th[active]
        # inner: minimise f = H - lam <theta, y>
        stalled = np.zeros(len(active), bool)
        for _k in range(100):
            H, Hth, Hthth = net.parts(xa, ta)
            g = Hth - la[:, None] * ya
            sc = 1.0 + np.abs(Hth).sum(1) + la * np.abs(ya).sum(1)
            gdone = (np.linalg.norm(g, axis=1) <= 1e-11 * sc) | stalled
            if np.all(gdone):
                break
            step = -np.linalg.solve(Hthth + 1e-300 * np.eye(d), g[..., None])[..., 0]
            step[gdone] = 0.0
            f = H - la * np.sum(ta * ya, 1)
            slope = np.sum(g * step, 1)
            t = np.ones(len(active))
            for _ls in range(60):
                tn = ta + t[:, None] * step
                Hn = net.parts(xa, tn)[0]
                fn = Hn - la * np.sum(tn * ya, 1)
                bad = ~np.isfinite(fn) | (fn > f + 1e-4 * t * slope + 1e-15 * np.abs(f))
                if not np.any(bad):
                    break
                t = np.where(bad, 0.5 * t, t)
            dstep = t[:, None] * step
            stalled |= np.abs(dstep).max(1) <= 1e-15 * (1.0 + np.abs(ta).max(1))
            ta = ta + dstep
        H, Hth, Hthth = net.parts(xa, ta)
        th[active] = ta
        r = net.rates(xa)
        Hscale = np.sum(r * (np.exp(np.clip(ta @ net.nu.T, -700, 700)) + 1.0), 1)
        done = np.abs(H) <= tol * Hscale
        # bracket update and safeguarded Newton step in mu
        m_a = mu[active]
        neg = H < 0
        lo[active] = np.where(neg, np.maximum(lo[active], m_a), lo[active])
        hi[active] = np.where(~neg, np.minimum(hi[active], m_a), hi[active])
        # float resolution: a collapsed bracket with |H| small on the scale of its terms is converged
        collapsed = (hi[active] - lo[active]) <= 1e-14 * (1.0 + np.abs(m_a))
        done |= collapsed & (np.abs(H) <= 1e-8 * Hscale)
        Hi_y = np.linalg.solve(Hthth + 1e-300 * np.eye(d), ya[..., None])[..., 0]
        dG = la * la * np.sum(ya * Hi_y, 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            mn = m_a - H / dG
        l_a, h_a = lo[active], hi[active]
        both = np.isfinite(l_a) & np.isfinite(h_a)
        mn = np.where(~np.isfinite(mn), np.where(neg, m_a + 2.0, m_a - 2.0), mn)
        mn = np.where(both & ((mn <= l_a) | (mn >= h_a)), 0.5 * (l_a + h_a), mn)
        mn = np.where(~both & neg, np.minimum(mn, m_a + 2.0), mn)
        mn = np.where(~both & ~neg, np.maximum(mn, m_a - 2.0), mn)
        mn = np.where(~both & neg, np.maximum(mn, m_a), mn)
        mn = np.where(~both & ~neg, np.minimum(mn, m_a), mn)
        mu[active] = np.where(done, m_a, mn)
        active = active[~done]
    if len(active):
        H = net.parts(x[active], th[active])[0]
        r = net.rates(x[active])
        Hscale = np.sum(r * (np.exp(np.clip(th[active] @ net.nu.T, -700, 700)) + 1.0), 1)
        if np.all(np.abs(H) <= 1e-8 * Hscale):
            active = active[:0]
    if len(active):
        raise InnerFailure("inner solve did not converge on %d segments (max |H| %.2e)" % (len(active),
                                                                                         np.abs(H).max()))
    lam = np.where(zero, 0.0, np.exp(mu))
    ell = np.sum(th * y, axis=1)
    return ell, th, lam


class Path:
    """Discrete path with fixed start, end partially free (mask), interior free."""

    def __init__(self, net, start, end, end_free, lower=LOWER, kappa=1.0):
        self.kappa = kappa  # spacing penalty during L-BFGS; the reported action never includes it
        self.net = net
        self.start = np.asarray(start, float)
        self.end = np.asarray(end, float)
        self.end_free = np.asarray(end_free, bool)
        self.lower = lower
        self.cache = None

    def unpack(self, z, N):
        d = self.net.dim
        phi = np.empty((N + 1, d))
        phi[0] = self.start
        phi[1:N] = z[: (N - 1) * d].reshape(N - 1, d)
        phi[N] = self.end
        phi[N, self.end_free] = z[(N - 1) * d:]
        return phi

    def pack(self, phi):
        return np.concatenate([phi[1:-1].ravel(), phi[-1, self.end_free]])

    def action(self, phi, warm=True):
        """Returns per-segment l, theta, lam and dl/dx at the midpoints."""
        mid = 0.5 * (phi[1:] + phi[:-1])
        dif = phi[1:] - phi[:-1]
        th0 = lam0 = None
        if warm and self.cache is not None and self.cache[0].shape == dif.shape:
            th0, lam0 = self.cache
        if self.net.nb_id is not None:
            if th0 is None:
                th0, lam0 = np.zeros_like(dif), np.zeros(len(dif))
            ell, th, lam, gx, status = gmam_nb.local_action(self.net.nb_id, gmam_nb.KV, self.net.nu,
                                                             np.ascontiguousarray(mid), np.ascontiguousarray(dif),
                                                             np.ascontiguousarray(th0), np.ascontiguousarray(lam0),
                                                             1e-12)
            if np.any(status):
                raise InnerFailure("inner solve did not converge on %d segments" % int(np.sum(status)))
        else:
            ell, th, lam = local_action(self.net, mid, dif, th0, lam0)
            _, _, _, Hx = self.net.parts(mid, th, grads=True)
            # grad_theta H = lam * y, so the multiplier on H is 1/lam and dl/dx = -H_x / lam
            safe = lam > 0
            gx = np.where(safe[:, None], -Hx / np.where(safe, lam, 1.0)[:, None], 0.0)
        self.cache = (th, lam)
        return ell, th, lam, gx

    def fun_grad(self, z, N):
        phi = self.unpack(z, N)
        try:
            ell, th, lam, gx = self.action(phi)
        except InnerFailure:
            self.cache = None
            ell, th, lam, gx = self.action(phi, warm=False)
        g = np.zeros_like(phi)
        g[:-1] += 0.5 * gx - th
        g[1:] += 0.5 * gx + th
        S = float(ell.sum())
        if self.kappa > 0:
            # equal-arclength constraint as a penalty: kappa * sum (s_i / mean(s) - 1)^2
            d = phi[1:] - phi[:-1]
            sl = np.linalg.norm(d, axis=1)
            sb = sl.mean()
            u = sl / sb - 1.0
            S += self.kappa * float(np.sum(u * u))
            dP_ds = self.kappa * (2 * u / sb - np.sum(2 * u * sl) / (sb * sb * len(sl)))
            unit = d / np.maximum(sl, 1e-300)[:, None]
            g[1:] += dP_ds[:, None] * unit
            g[:-1] -= dP_ds[:, None] * unit
        grad = np.concatenate([g[1:-1].ravel(), g[-1, self.end_free]])
        return S, grad

    def bounds(self, N):
        d = self.net.dim
        b = [(self.lower, None)] * ((N - 1) * d)
        b += [(self.lower, None)] * int(self.end_free.sum())
        return b


def reparam(phi, N):
    seg = np.linalg.norm(np.diff(phi, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    s /= s[-1]
    u = np.linspace(0, 1, N + 1)
    return np.column_stack([np.interp(u, s, phi[:, j]) for j in range(phi.shape[1])])


def minimise_level(path, phi0, N, rtol=1e-9, max_cycles=400, inner_iter=3000):
    phi = reparam(phi0, N)
    path.cache = None
    S_prev = None
    hist = []
    for cyc in range(max_cycles):
        z0 = path.pack(phi)
        res = minimize(path.fun_grad, z0, args=(N,), jac=True, method="L-BFGS-B", bounds=path.bounds(N),
                       options=dict(maxiter=inner_iter, maxcor=30, ftol=1e-15, gtol=1e-12))
        phi = reparam(path.unpack(res.x, N), N)
        # endpoint fixed coordinates stay exact; interior bounds re-applied
        phi[1:-1] = np.maximum(phi[1:-1], path.lower)
        path.cache = None
        S = float(path.action(phi, warm=False)[0].sum())
        hist.append(S)
        if S_prev is not None and abs(S - S_prev) <= rtol * abs(S):
            return phi, S, cyc + 1, hist
        S_prev = S
    return phi, S, max_cycles, hist


def gmam(net, start, end, end_free, phi_init=None, N0=50, Nmax=3200, rel=0.01, log=print, label=""):
    path = Path(net, start, end, end_free)
    if phi_init is None:
        phi_init = np.linspace(0, 1, N0 + 1)[:, None] * (np.asarray(end) - np.asarray(start)) + start
    levels = []
    phi = phi_init
    N = N0
    while N <= Nmax:
        try:
            phi, S, cycles, hist = minimise_level(path, phi, N)
        except InnerFailure as e:
            levels.append(dict(N=N, error=str(e)))
            log("  gMAM %s N=%d inner failure: %s" % (label, N, e))
            return dict(converged=False, levels=levels, reason="inner failure", path=phi.tolist())
        levels.append(dict(N=N, S=S, cycles=cycles, end=phi[-1].tolist()))
        log("  gMAM %s N=%d S=%.8g cycles=%d end=%s" % (label, N, S, cycles, np.round(phi[-1], 6)))
        if len(levels) >= 2 and abs(levels[-1]["S"] - levels[-2]["S"]) / abs(levels[-1]["S"]) < rel:
            return dict(converged=True, W=S, N=N, levels=levels, path=phi.tolist())
        N *= 2
    return dict(converged=False, levels=levels, reason="no 1%% convergence by N=%d" % Nmax, path=phi.tolist())
