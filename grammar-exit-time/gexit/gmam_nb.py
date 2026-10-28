"""numba kernel for the gMAM local geometric action (same algorithm as gmam.local_action).

Models: 0 = grammar MA, 1 = grammar TH, 2 = immigration-death (1 copy), 3 = (2 copies)."""
import numpy as np
from numba import njit

from . import model

KV = model.KVEC.copy()


@njit(cache=True)
def _rates(mid, x, k, r, dr):
    """Fill rates r[R] and gradients dr[R, d] at x."""
    dr[:, :] = 0.0
    if mid == 0 or mid == 1:
        c, v, l, p = x[0], x[1], x[2], x[3]
        r[0] = k[0] * c; dr[0, 0] = k[0]
        r[1] = k[1] * c; dr[1, 0] = k[1]
        r[3] = k[3] * l; dr[3, 2] = k[3]
        r[4] = k[4] * l; dr[4, 2] = k[4]
        r[5] = k[5] * c; dr[5, 0] = k[5]
        r[6] = k[6] * p; dr[6, 3] = k[6]
        r[7] = k[7] * p; dr[7, 3] = k[7]
        r[8] = k[8] * v; dr[8, 1] = k[8]
        r[10] = k[10]
        if mid == 0:
            r[2] = k[2] * v * c; dr[2, 0] = k[2] * v; dr[2, 1] = k[2] * c
            r[9] = k[9] * c * c; dr[9, 0] = 2 * k[9] * c
        else:
            s = c + v
            if s > 0:
                xx = c / s
                dxc = v / (s * s)
                dxv = -c / (s * s)
            else:
                xx = 0.0
                dxc = 0.0
                dxv = 0.0
            r[2] = k[2] * v * xx * xx
            dr[2, 0] = k[2] * v * 2 * xx * dxc
            dr[2, 1] = k[2] * xx * xx + k[2] * v * 2 * xx * dxv
            r[9] = k[9] * c * xx * xx
            dr[9, 0] = k[9] * xx * xx + k[9] * c * 2 * xx * dxc
            dr[9, 1] = k[9] * c * 2 * xx * dxv
    elif mid == 2:
        r[0] = 1.0
        r[1] = x[0]; dr[1, 0] = 1.0
    else:
        r[0] = 1.0
        r[1] = 1.0
        r[2] = x[0]; dr[2, 0] = 1.0
        r[3] = x[1]; dr[3, 1] = 1.0


@njit(cache=True)
def _solve(A, b, out):
    """Gaussian elimination with partial pivoting, small dense systems."""
    n = b.shape[0]
    M = A.copy()
    y = b.copy()
    for i in range(n):
        p = i
        for j in range(i + 1, n):
            if abs(M[j, i]) > abs(M[p, i]):
                p = j
        if p != i:
            for kk in range(n):
                t = M[i, kk]; M[i, kk] = M[p, kk]; M[p, kk] = t
            t = y[i]; y[i] = y[p]; y[p] = t
        piv = M[i, i]
        if piv == 0.0:
            piv = 1e-300
        for j in range(i + 1, n):
            f = M[j, i] / piv
            if f != 0.0:
                for kk in range(i, n):
                    M[j, kk] -= f * M[i, kk]
                y[j] -= f * y[i]
    for i in range(n - 1, -1, -1):
        s = y[i]
        for kk in range(i + 1, n):
            s -= M[i, kk] * out[kk]
        d = M[i, i]
        if d == 0.0:
            d = 1e-300
        out[i] = s / d


@njit(cache=True)
def _hparts(r, nu, th, E, Hth, Hthth):
    R, d = nu.shape
    H = 0.0
    for a in range(d):
        Hth[a] = 0.0
        for b in range(d):
            Hthth[a, b] = 0.0
    for q in range(R):
        z = 0.0
        for a in range(d):
            z += th[a] * nu[q, a]
        if z > 700.0:
            z = 700.0
        e = np.exp(z)
        E[q] = e
        H += r[q] * (e - 1.0)
        re = r[q] * e
        for a in range(d):
            if nu[q, a] != 0.0:
                Hth[a] += re * nu[q, a]
                for b in range(d):
                    Hthth[a, b] += re * nu[q, a] * nu[q, b]
    return H


@njit(cache=True)
def _Honly(r, nu, th):
    R, d = nu.shape
    H = 0.0
    for q in range(R):
        z = 0.0
        for a in range(d):
            z += th[a] * nu[q, a]
        if z > 700.0:
            z = 700.0
        H += r[q] * (np.exp(z) - 1.0)
    return H


@njit(cache=True)
def local_action(mid, k, nu, X, Y, TH0, LAM0, tol):
    M, d = X.shape
    R = nu.shape[0]
    ell = np.zeros(M)
    TH = np.zeros((M, d))
    LAM = np.zeros(M)
    GX = np.zeros((M, d))
    status = np.zeros(M, np.int64)
    r = np.zeros(R)
    dr = np.zeros((R, d))
    E = np.zeros(R)
    Hth = np.zeros(d)
    Hthth = np.zeros((d, d))
    A = np.zeros((d, d))
    g = np.zeros(d)
    step = np.zeros(d)
    tn = np.zeros(d)
    tmp = np.zeros(d)
    for i in range(M):
        x = X[i]
        y = Y[i]
        ny = 0.0
        for a in range(d):
            ny += y[a] * y[a]
        if ny < 1e-300:
            continue
        _rates(mid, x, k, r, dr)
        th = TH0[i].copy()
        lam = LAM0[i]
        if not (lam > 0.0):
            # Gaussian start: A = sum r nu nu^T, b = sum r nu
            for a in range(d):
                g[a] = 0.0
                for b in range(d):
                    A[a, b] = 1e-14 if a == b else 0.0
            for q in range(R):
                for a in range(d):
                    g[a] += r[q] * nu[q, a]
                    for b in range(d):
                        A[a, b] += r[q] * nu[q, a] * nu[q, b]
            _solve(A, g, step)  # A^-1 b
            _solve(A, y, tmp)  # A^-1 y
            bAb = 0.0
            yAy = 0.0
            for a in range(d):
                bAb += g[a] * step[a]
                yAy += y[a] * tmp[a]
            lam = np.sqrt(max(bAb, 0.0) / max(yAy, 1e-300))
            if lam < 1e-12:
                lam = 1e-12
            for a in range(d):
                th[a] = lam * tmp[a] - step[a]
        mu = np.log(lam)
        lo = -np.inf
        hi = np.inf
        ok = False
        for it in range(200):
            lam = np.exp(mu)
            # inner Newton on f = H - lam <th, y>
            for kk in range(100):
                H = _hparts(r, nu, th, E, Hth, Hthth)
                sc = 1.0
                gn = 0.0
                for a in range(d):
                    g[a] = Hth[a] - lam * y[a]
                    gn += g[a] * g[a]
                    sc += abs(Hth[a]) + lam * abs(y[a])
                if np.sqrt(gn) <= 1e-11 * sc:
                    break
                for a in range(d):
                    tmp[a] = -g[a]
                _solve(Hthth, tmp, step)
                f = H
                slope = 0.0
                for a in range(d):
                    f -= lam * th[a] * y[a]
                    slope += g[a] * step[a]
                t = 1.0
                for ls in range(60):
                    for a in range(d):
                        tn[a] = th[a] + t * step[a]
                    fn = _Honly(r, nu, tn)
                    for a in range(d):
                        fn -= lam * tn[a] * y[a]
                    if np.isfinite(fn) and fn <= f + 1e-4 * t * slope + 1e-15 * abs(f):
                        break
                    t *= 0.5
                smax = 0.0
                tmax = 0.0
                for a in range(d):
                    smax = max(smax, abs(t * step[a]))
                    tmax = max(tmax, abs(th[a]))
                    th[a] = tn[a]
                if smax <= 1e-15 * (1.0 + tmax):
                    break
            H = _hparts(r, nu, th, E, Hth, Hthth)
            Hs = 0.0
            for q in range(R):
                Hs += r[q] * (E[q] + 1.0)
            if abs(H) <= tol * Hs:
                ok = True
                break
            if H < 0:
                lo = max(lo, mu)
            else:
                hi = min(hi, mu)
            if hi - lo <= 1e-14 * (1.0 + abs(mu)) and abs(H) <= 1e-8 * Hs:
                ok = True
                break
            _solve(Hthth, y, tmp)
            yHy = 0.0
            for a in range(d):
                yHy += y[a] * tmp[a]
            dG = lam * lam * yHy
            if dG > 0 and np.isfinite(dG):
                mn = mu - H / dG
            else:
                mn = mu + 2.0 if H < 0 else mu - 2.0
            both = np.isfinite(lo) and np.isfinite(hi)
            if both:
                if mn <= lo or mn >= hi or not np.isfinite(mn):
                    mn = 0.5 * (lo + hi)
            elif H < 0:
                mn = min(max(mn, mu), mu + 2.0)
            else:
                mn = max(min(mn, mu), mu - 2.0)
            mu = mn
        lam = np.exp(mu)
        if not ok:
            H = _hparts(r, nu, th, E, Hth, Hthth)
            Hs = 0.0
            for q in range(R):
                Hs += r[q] * (E[q] + 1.0)
            status[i] = 0 if abs(H) <= 1e-8 * Hs else 1
        else:
            _hparts(r, nu, th, E, Hth, Hthth)
        s = 0.0
        for a in range(d):
            s += th[a] * y[a]
            TH[i, a] = th[a]
        ell[i] = s
        LAM[i] = lam
        # dl/dx = -H_x / lam, H_x = sum_q (E_q - 1) dr_q
        for a in range(d):
            hx = 0.0
            for q in range(R):
                hx += (E[q] - 1.0) * dr[q, a]
            GX[i, a] = -hx / lam
    return ell, TH, LAM, GX, status
