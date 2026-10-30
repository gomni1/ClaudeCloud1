# Copied from grammar-exit-time/gexit/ (PR 3, gomni1/ClaudeCloud1#3) for task grammar-idsize; changes are marked "idsize:".
"""Deterministic grammar: rates, gradients, drift, balances, Jacobians (SPEC §1)."""
import numpy as np
from scipy.integrate import solve_ivp

# (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12)
KVEC = np.array([2.0, 9.0, 47.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 13.0, 0.5])
k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = KVEC

# reaction order r1 r2 r3 r5 r6 r7 r8 r9 r10 r11 r12; species (c, v, l, p)
REACTIONS = ["1", "2", "3", "5", "6", "7", "8", "9", "10", "11", "12"]
NU = np.array([
    [-1, 0, 1, 0],
    [-1, 1, 0, 0],
    [1, -1, 0, 0],
    [0, 1, -1, 0],
    [1, 0, -1, 0],
    [-1, 0, 0, 1],
    [0, 1, 0, -1],
    [0, 0, 0, -1],
    [1, -1, 0, 0],
    [-1, 1, 0, 0],
    [0, 1, 0, 0],
], dtype=float)

LAWS = ("MA", "TH")


def set_k(kvec):
    """idsize: replace the rate constants in place (module globals, KVEC, and the gMAM kernel copy)."""
    global k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12, A_CONST
    KVEC[:] = np.asarray(kvec, float)
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = KVEC
    A_CONST = k2 + k7 + k1 * k5 / (k5 + k6)
    BAL["MA"] = balance_ma()
    try:
        from . import gmam_nb
        gmam_nb.KV[:] = KVEC
    except ImportError:
        pass
A_CONST = k2 + k7 + k1 * k5 / (k5 + k6)  # = 11


def rates(x, law):
    """Deterministic rates r_r(x), shape (..., 11)."""
    x = np.asarray(x, dtype=float)
    c, v, l, p = x[..., 0], x[..., 1], x[..., 2], x[..., 3]
    out = np.empty(x.shape[:-1] + (11,))
    out[..., 0] = k1 * c
    out[..., 1] = k2 * c
    out[..., 3] = k5 * l
    out[..., 4] = k6 * l
    out[..., 5] = k7 * c
    out[..., 6] = k8 * p
    out[..., 7] = k9 * p
    out[..., 8] = k10 * v
    out[..., 10] = k12
    if law == "MA":
        out[..., 2] = k3 * v * c
        out[..., 9] = k11 * c * c
    elif law == "TH":
        s = c + v
        xx = np.where(s > 0, c / np.where(s > 0, s, 1.0), 0.0)
        out[..., 2] = k3 * v * xx ** 2
        out[..., 9] = k11 * c * xx ** 2
    else:
        raise ValueError(law)
    return out


def rate_grads(x, law):
    """d r_r / d x_j, shape (..., 11, 4)."""
    x = np.asarray(x, dtype=float)
    c, v = x[..., 0], x[..., 1]
    g = np.zeros(x.shape[:-1] + (11, 4))
    g[..., 0, 0] = k1
    g[..., 1, 0] = k2
    g[..., 3, 2] = k5
    g[..., 4, 2] = k6
    g[..., 5, 0] = k7
    g[..., 6, 3] = k8
    g[..., 7, 3] = k9
    g[..., 8, 1] = k10
    if law == "MA":
        g[..., 2, 0] = k3 * v
        g[..., 2, 1] = k3 * c
        g[..., 9, 0] = 2 * k11 * c
    else:
        s = c + v
        ok = s > 0
        ss = np.where(ok, s, 1.0)
        xx = np.where(ok, c / ss, 0.0)
        dxc = np.where(ok, v / ss ** 2, 0.0)
        dxv = np.where(ok, -c / ss ** 2, 0.0)
        g[..., 2, 0] = k3 * v * 2 * xx * dxc
        g[..., 2, 1] = k3 * xx ** 2 + k3 * v * 2 * xx * dxv
        g[..., 9, 0] = k11 * xx ** 2 + k11 * c * 2 * xx * dxc
        g[..., 9, 1] = k11 * c * 2 * xx * dxv
    return g


def drift(x, law):
    return rates(x, law) @ NU


def jacobian(x, law):
    return np.einsum("rj,ri->ij", rate_grads(x, law), NU)


def balance_ma():
    c = k12 * (k8 + k9) / (k7 * k9)
    l = k1 * c / (k5 + k6)
    p = k12 / k9
    v = (A_CONST * c + k11 * c * c) / (k10 + k3 * c)
    return np.array([c, v, l, p])


def th_cubic():
    """Coefficients of k10*y*(1+y)^2 + k3*y - k11 - A*(1+y)^2 (balance condition times (1+y)^2)."""
    # k10*y*(1+2y+y^2) = k10*y^3 + 2k10*y^2 + k10*y
    return np.array([k10, 2 * k10 - A_CONST, k10 + k3 - 2 * A_CONST, -k11 - A_CONST])


def balances_th():
    """All TH balances, sorted by v; c* = 1 from the P equation and conservation."""
    c = k12 * (k8 + k9) / (k7 * k9)
    l = k1 * c / (k5 + k6)
    p = k12 / k9
    roots = np.roots(th_cubic())
    ys = np.sort(roots[np.abs(roots.imag) < 1e-9].real)
    return [np.array([c, y * c, l, p]) for y in ys if y > 0]


def S_minus_A(y):
    return k10 * y + (k3 * y - k11) / (1 + y) ** 2 - A_CONST


BAL = {"MA": balance_ma(), "TH2": np.array([1.0, 2.0, 1.0, 0.5]),
       "TH3": np.array([1.0, 3.0, 1.0, 0.5]), "TH4": np.array([1.0, 4.0, 1.0, 0.5])}
LAW_OF = {"MA": "MA", "TH2": "TH", "TH4": "TH", "TH3": "TH"}


def lambda_slow(x, law):
    ev = np.linalg.eigvals(jacobian(x, law))
    return ev[np.argmin(np.abs(ev.real))]


def burn_in_time(start):
    return 10.0 / abs(lambda_slow(BAL[start], LAW_OF[start]).real)


def integrate(x0, law, t_end, t_eval=None, rtol=1e-10, atol=1e-12):
    return solve_ivp(lambda t, y: drift(y, law), (0.0, t_end), np.asarray(x0, float),
                     method="LSODA", rtol=rtol, atol=atol, t_eval=t_eval)


def round_half_up(x):
    return np.floor(np.asarray(x, float) + 0.5).astype(np.int64)


def start_counts(start, omega):
    return round_half_up(omega * BAL[start])
