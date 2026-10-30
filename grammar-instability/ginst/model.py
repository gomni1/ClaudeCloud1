"""Grammar model on one level: rates, analytic Jacobian, balances, stability (SPEC §1).

A parameter vector `par` (float64) packs everything the numba kernels need:
  par[0:11]  k1 k2 k3 k5 k6 k7 k8 k9 k10 k11 k12
  par[11]    law      (0 = MA, 1 = TH)
  par[12]    den      (0 = cv, 1 = tot)
  par[13]    level    (1 = open, 0 = closed)
  par[14]    m, par[15] kr, par[16] kc
  par[17]    T        (closed level total)
  par[18]    model id (0 = grammar, 1 = Brusselator, 2 = linear focus, used by the planted tests)
  par[19:21] extra parameters for the planted models
"""
import math

import numpy as np
from numba import njit
from scipy.optimize import brentq
from scipy.special import comb

ASTRA = np.array([2.0, 9.0, 47.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 13.0, 0.5])
NPAR = 21


def make_par(k, law="TH", den="cv", level="open", m=2, kr=2, kc=2, T=1.0, model=0, extra=(0.0, 0.0)):
    p = np.zeros(NPAR)
    p[0:11] = k
    p[11] = {"MA": 0, "TH": 1}[law]
    p[12] = {"cv": 0, "tot": 1}[den]
    p[13] = {"open": 1, "closed": 0}[level]
    p[14], p[15], p[16], p[17], p[18] = m, kr, kc, T, model
    p[19], p[20] = extra
    return p


@njit(cache=True)
def binom(n, k):
    if k < 0 or k > n:
        return 0.0
    r = 1.0
    for i in range(1, k + 1):
        r = r * (n - k + i) / i
    return r


@njit(cache=True)
def F_tail(x, m, j):
    """Pr[Bin(m, x) >= j] and its derivative in x."""
    if x <= 0.0:
        return (1.0 if j <= 0 else 0.0), (m * binom(m - 1, j - 1) if j == 1 else 0.0)
    if x >= 1.0:
        return (1.0 if j <= m else 0.0), (m * binom(m - 1, j - 1) if j == m else 0.0)
    s = 0.0
    for i in range(j, m + 1):
        s += binom(m, i) * x ** i * (1.0 - x) ** (m - i)
    d = m * binom(m - 1, j - 1) * x ** (j - 1) * (1.0 - x) ** (m - j) if j >= 1 else 0.0
    return s, d


@njit(cache=True)
def g_and_grad(y, par, grad):
    """g = k10 V + r3 - r11 and its gradient in (C, V, L, P)."""
    C, V, L, P = y[0], y[1], y[2], y[3]
    k3, k10, k11 = par[2], par[8], par[9]
    grad[0] = 0.0
    grad[1] = 0.0
    grad[2] = 0.0
    grad[3] = 0.0
    if par[11] == 0.0:  # MA
        g = k10 * V + k3 * V * C - k11 * C * C
        grad[0] = k3 * V - 2.0 * k11 * C
        grad[1] = k10 + k3 * C
        return g
    m, kr, kc = int(par[14]), int(par[15]), int(par[16])
    if par[12] == 0.0:
        den = C + V
    else:
        den = C + V + L + P
    if den > 0.0:
        x = C / den
    else:
        x = 0.0
    Fr, dFr = F_tail(x, m, kr)
    Fc, dFc = F_tail(x, m, kc)
    g = k10 * V + k3 * V * Fr - k11 * C * Fc
    # dg/dx
    gx = k3 * V * dFr - k11 * C * dFc
    if den > 0.0:
        dxdC = (den - C) / (den * den)
        dxdo = -C / (den * den)
    else:
        dxdC = 0.0
        dxdo = 0.0
    grad[0] = -k11 * Fc + gx * dxdC
    grad[1] = k10 + k3 * Fr + gx * dxdo
    if par[12] == 1.0:
        grad[2] = gx * dxdo
        grad[3] = gx * dxdo
    return g


@njit(cache=True)
def rhs(y, par, out):
    mid = par[18]
    if mid == 1.0:  # Brusselator dx = a - (b+1) x + x^2 y, dy = b x - x^2 y
        a, b = par[19], par[20]
        out[0] = a - (b + 1.0) * y[0] + y[0] * y[0] * y[1]
        out[1] = b * y[0] - y[0] * y[0] * y[1]
        return
    if mid == 2.0:  # linear focus dz = (-eps + i) z
        eps = par[19]
        out[0] = -eps * y[0] - y[1]
        out[1] = y[0] - eps * y[1]
        return
    k1, k2, k5, k6, k7, k8, k9, k12 = par[0], par[1], par[3], par[4], par[5], par[6], par[7], par[10]
    o = par[13]
    grad = np.empty(4)
    g = g_and_grad(y, par, grad)
    C, L, P = y[0], y[2], y[3]
    out[0] = -(k1 + k2 + k7) * C + k6 * L + g
    out[1] = k2 * C + k5 * L + k8 * P - g + o * k12
    out[2] = k1 * C - (k5 + k6) * L
    out[3] = k7 * C - (k8 + o * k9) * P


@njit(cache=True)
def jac(y, par, J):
    mid = par[18]
    if mid == 1.0:
        a, b = par[19], par[20]
        J[0, 0] = -(b + 1.0) + 2.0 * y[0] * y[1]
        J[0, 1] = y[0] * y[0]
        J[1, 0] = b - 2.0 * y[0] * y[1]
        J[1, 1] = -y[0] * y[0]
        return
    if mid == 2.0:
        eps = par[19]
        J[0, 0] = -eps
        J[0, 1] = -1.0
        J[1, 0] = 1.0
        J[1, 1] = -eps
        return
    k1, k2, k5, k6, k7, k8, k9 = par[0], par[1], par[3], par[4], par[5], par[6], par[7]
    o = par[13]
    grad = np.empty(4)
    g_and_grad(y, par, grad)
    for i in range(4):
        for j in range(4):
            J[i, j] = 0.0
    J[0, 0] = -(k1 + k2 + k7)
    J[0, 2] = k6
    J[1, 0] = k2
    J[1, 2] = k5
    J[1, 3] = k8
    J[2, 0] = k1
    J[2, 2] = -(k5 + k6)
    J[3, 0] = k7
    J[3, 3] = -(k8 + o * k9)
    for j in range(4):
        J[0, j] += grad[j]
        J[1, j] -= grad[j]


def dim(par):
    return 2 if par[18] in (1.0, 2.0) else 4


def f_np(y, par):
    out = np.empty(dim(par))
    rhs(np.asarray(y, float), par, out)
    return out


def J_np(y, par):
    n = dim(par)
    Jm = np.empty((n, n))
    jac(np.asarray(y, float), par, Jm)
    return Jm


# ------------------------------------------------------------------ balances
def consts(par):
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = par[:11]
    a = k1 + k2 + k7
    A = k2 + k7 + k1 * k5 / (k5 + k6)
    return a, A


def _F_poly(m, j, base, one_plus):
    """sum_{i>=j} C(m,i) * base^(m-i)  as numpy poly (lowest degree first), with base and one_plus polys."""
    P = np.zeros(1)
    for i in range(j, m + 1):
        term = comb(m, i, exact=False) * np.polynomial.polynomial.polypow(base, m - i)
        P = np.polynomial.polynomial.polyadd(P, term)
    return P


def _real_roots_in(poly_lo_first, lo, hi, fun):
    """Real roots in (lo, hi): polynomial roots plus a sign-change scan of fun, Newton-polished on fun."""
    cands = []
    c = np.trim_zeros(np.asarray(poly_lo_first, float), "b")
    if len(c) > 1:
        for z in np.polynomial.polynomial.polyroots(c):
            if abs(z.imag) <= 1e-6 * max(1.0, abs(z.real)) and lo < z.real < hi:
                cands.append(z.real)
    if np.isfinite(hi):
        grid = lo + (hi - lo) * np.linspace(0, 1, 4001)[1:-1]
    else:
        u = np.linspace(0, 1, 4001)[1:-1]
        grid = lo + u / (1 - u)
    vals = np.array([fun(t) for t in grid])
    fin = vals[np.isfinite(vals)]
    scale = max(1.0, float(np.max(np.abs(fin)))) if len(fin) else 1.0
    for i in range(len(grid) - 1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] < 0:
            try:
                cands.append(brentq(fun, grid[i], grid[i + 1], xtol=1e-15, rtol=4e-16, maxiter=200))
            except ValueError:
                pass
    out = []
    for r in sorted(cands):
        for _ in range(30):
            h = 1e-7 * max(1e-12, abs(r))
            d = (fun(r + h) - fun(r - h)) / (2 * h)
            if d == 0 or not np.isfinite(d):
                break
            r_new = r - fun(r) / d
            if not (lo < r_new < hi):
                break
            done = abs(r_new - r) <= 1e-15 * max(1.0, abs(r))
            r = r_new
            if done:
                break
        if abs(fun(r)) > 1e-9 * scale:
            continue
        if all(abs(r - q) > 1e-9 * max(1.0, abs(q)) for q in out):
            out.append(r)
    return out


def _S_poly(m, kr, kc, k3, k10, k11, A, q):
    """(1+y+q)^m * (S(y) - A) as a polynomial in y (lowest degree first)."""
    P = np.polynomial.polynomial
    base = np.array([q, 1.0])
    onep = np.array([1.0 + q, 1.0])
    Pm = P.polypow(onep, m)
    Y = np.array([0.0, 1.0])
    poly = P.polyadd(k10 * P.polymul(Y, Pm), k3 * P.polymul(Y, _F_poly(m, kr, base, onep)))
    poly = P.polysub(poly, k11 * _F_poly(m, kc, base, onep))
    return P.polysub(poly, A * Pm)


def balances(par):
    """All balances with C, V, L, P > 0."""
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = par[:11]
    law = "MA" if par[11] == 0 else "TH"
    den = "cv" if par[12] == 0 else "tot"
    open_ = par[13] == 1
    m, kr, kc, T = int(par[14]), int(par[15]), int(par[16]), par[17]
    a, A = consts(par)
    out = []
    if open_:
        Cs = k12 * (k8 + k9) / (k7 * k9)
        Ls = k1 * Cs / (k5 + k6)
        Ps = k12 / k9
        if law == "MA":
            V = (A * Cs + k11 * Cs * Cs) / (k10 + k3 * Cs)
            return [np.array([Cs, V, Ls, Ps])]
        q = (Ls + Ps) / Cs if den == "tot" else 0.0

        def S(y):
            x = 1.0 / (1.0 + y + q)
            Fr = F_tail(x, m, kr)[0]
            Fc = F_tail(x, m, kc)[0]
            return k10 * y + k3 * y * Fr - k11 * Fc - A

        poly = _S_poly(m, kr, kc, k3, k10, k11, A, q)
        for y in _real_roots_in(poly, 0.0, np.inf, S):
            out.append(np.array([Cs, y * Cs, Ls, Ps]))
        return out
    # closed level
    l_ = k1 / (k5 + k6)
    p_ = k7 / k8
    qc = l_ + p_
    if law == "MA":
        aa = -(k3 * (1 + qc) + k11)
        bb = k3 * T - k10 * (1 + qc) - A
        cc = k10 * T
        disc = bb * bb - 4 * aa * cc
        for Cr in ((-bb - math.sqrt(disc)) / (2 * aa), (-bb + math.sqrt(disc)) / (2 * aa)):
            V = T - Cr * (1 + qc)
            if Cr > 0 and V > 0:
                out.append(np.array([Cr, V, l_ * Cr, p_ * Cr]))
        return out
    if den == "cv":
        def S(y):
            x = 1.0 / (1.0 + y)
            return k10 * y + k3 * y * F_tail(x, m, kr)[0] - k11 * F_tail(x, m, kc)[0] - A

        poly = _S_poly(m, kr, kc, k3, k10, k11, A, 0.0)
        for y in _real_roots_in(poly, 0.0, np.inf, S):
            Cr = T / (1 + qc + y)
            out.append(np.array([Cr, y * Cr, l_ * Cr, p_ * Cr]))
        return out
    cmax = 1.0 / (1.0 + qc)

    def G(c):
        return (1 - c * (1 + qc)) * (k10 + k3 * F_tail(c, m, kr)[0]) - c * (k11 * F_tail(c, m, kc)[0] + A)

    # polynomial in c: F_j(c) = sum_{i>=j} C(m,i) c^i (1-c)^(m-i)
    def Fc_poly(j):
        P = np.zeros(1)
        for i in range(j, m + 1):
            t = comb(m, i, exact=False) * np.polynomial.polynomial.polymul(
                np.polynomial.polynomial.polypow([0.0, 1.0], i),
                np.polynomial.polynomial.polypow([1.0, -1.0], m - i))
            P = np.polynomial.polynomial.polyadd(P, t)
        return P

    pa = np.array([1.0, -(1 + qc)])
    poly = np.polynomial.polynomial.polymul(pa, np.polynomial.polynomial.polyadd([k10], k3 * Fc_poly(kr)))
    poly = np.polynomial.polynomial.polysub(
        poly, np.polynomial.polynomial.polymul([0.0, 1.0],
                                               np.polynomial.polynomial.polyadd([A], k11 * Fc_poly(kc))))
    for c in _real_roots_in(poly, 0.0, cmax, G):
        Cr = c * T
        out.append(np.array([Cr, T - Cr * (1 + qc), l_ * Cr, p_ * Cr]))
    return out


def reduced_jacobian(J):
    """Closed level: (C, V, L) with P = T - C - V - L."""
    return J[:3, :3] - J[:3, 3:4]


def eigs_at(b, par):
    J = J_np(b, par)
    if par[13] == 0 and par[18] == 0:
        return np.linalg.eigvals(reduced_jacobian(J)), J
    return np.linalg.eigvals(J), J


def classify_balances(par):
    out = []
    for b in balances(par):
        ev, J = eigs_at(b, par)
        stable = bool(np.all(ev.real < 0))
        out.append(dict(b=b, eig=ev, J=J, stable=stable, residual=float(np.abs(f_np(b, par)).max())))
    return out
