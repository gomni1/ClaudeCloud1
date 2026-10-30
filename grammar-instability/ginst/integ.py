"""Integration and end-state classification (SPEC §4, M2).

Production integrator: Shampine-Reichelt ode23s (L-stable Rosenbrock 2(3)) in numba with the
analytic Jacobian.  Poincare stage: scipy Radau at rtol 1e-10."""
import math

import numpy as np
from numba import njit
from scipy.integrate import solve_ivp

from .model import J_np, dim, f_np, jac, rhs

D23 = 1.0 / (2.0 + math.sqrt(2.0))
E32 = 6.0 + math.sqrt(2.0)


@njit(cache=True)
def _lu_solve(Wm, b, n):
    """Solve Wm x = b (small dense, partial pivoting); Wm is overwritten."""
    x = b.copy()
    piv = np.arange(n)
    for i in range(n):
        p = i
        for j in range(i + 1, n):
            if abs(Wm[j, i]) > abs(Wm[p, i]):
                p = j
        if p != i:
            for k in range(n):
                t = Wm[i, k]
                Wm[i, k] = Wm[p, k]
                Wm[p, k] = t
            t = x[i]
            x[i] = x[p]
            x[p] = t
        d = Wm[i, i]
        if d == 0.0:
            d = 1e-300
        for j in range(i + 1, n):
            f = Wm[j, i] / d
            if f != 0.0:
                for k in range(i, n):
                    Wm[j, k] -= f * Wm[i, k]
                x[j] -= f * x[i]
    for i in range(n - 1, -1, -1):
        s = x[i]
        for k in range(i + 1, n):
            s -= Wm[i, k] * x[k]
        x[i] = s / Wm[i, i] if Wm[i, i] != 0.0 else s / 1e-300
    return x


@njit(cache=True)
def ode23s(y0, par, t_end, rtol, atol, stable, stop_tol, max_steps):
    """Integrate to t_end.  stable: (k, n) array of stable balances for the early stop.
    Returns (y, t, status, nsteps); status 0 = reached t_end, 1 = early stop at a stable balance,
    2 = step limit, 3 = non-finite or strongly negative state, 4 = step size underflow."""
    n = y0.shape[0]
    y = y0.copy()
    t = 0.0
    F0 = np.empty(n)
    rhs(y, par, F0)
    Jm = np.empty((n, n))
    W = np.empty((n, n))
    nrm = 0.0
    for i in range(n):
        nrm = max(nrm, abs(F0[i]) / (atol + rtol * abs(y[i])))
    h = min(t_end, 0.01 / max(nrm, 1e-300)) if nrm > 0 else t_end * 1e-6
    h = max(h, 1e-12 * t_end)
    F1 = np.empty(n)
    F2 = np.empty(n)
    ytmp = np.empty(n)
    steps = 0
    scale = 0.0
    for i in range(n):
        scale = max(scale, abs(y0[i]))
    while t < t_end:
        if steps >= max_steps:
            return y, t, 2, steps
        if t + h > t_end:
            h = t_end - t
        jac(y, par, Jm)
        for i in range(n):
            for j in range(n):
                W[i, j] = (1.0 if i == j else 0.0) - h * D23 * Jm[i, j]
        k1 = _lu_solve(W.copy(), F0, n)
        for i in range(n):
            ytmp[i] = y[i] + 0.5 * h * k1[i]
        rhs(ytmp, par, F1)
        r = F1 - k1
        k2 = _lu_solve(W.copy(), r, n) + k1
        ynew = y + h * k2
        rhs(ynew, par, F2)
        r3 = F2 - E32 * (k2 - F1) - 2.0 * (k1 - F0)
        k3 = _lu_solve(W.copy(), r3, n)
        err = 0.0
        ok = True
        for i in range(n):
            e = h / 6.0 * (k1[i] - 2.0 * k2[i] + k3[i])
            sc = atol + rtol * max(abs(y[i]), abs(ynew[i]))
            v = abs(e) / sc
            if not np.isfinite(v) or not np.isfinite(ynew[i]):
                ok = False
            err = max(err, v)
        steps += 1
        if ok and err <= 1.0:
            t += h
            for i in range(n):
                y[i] = ynew[i]
                F0[i] = F2[i]
                scale = max(scale, abs(y[i]))
            if par[18] == 0.0:  # positivity guard for the grammar only
                for i in range(n):
                    if y[i] < -1e-9 * max(scale, 1e-300):
                        return y, t, 3, steps
            # early stop near a stable balance
            for b in range(stable.shape[0]):
                d2 = 0.0
                b2 = 0.0
                for i in range(n):
                    d2 += (y[i] - stable[b, i]) ** 2
                    b2 += stable[b, i] ** 2
                if b2 > 0 and math.sqrt(d2) <= stop_tol * math.sqrt(b2):
                    return y, t, 1, steps
            fac = 0.8 * err ** (-1.0 / 3.0) if err > 0 else 5.0
            h *= min(5.0, max(0.2, fac))
        else:
            if not ok:
                h *= 0.1
            else:
                h *= max(0.1, 0.8 * err ** (-1.0 / 3.0))
            if h < 1e-14 * max(t_end, 1.0) * 1e-6:
                return y, t, 4, steps
    return y, t, 0, steps


def _near(x, balances, tol):
    """Relative distance to a balance (absolute when the balance is the origin)."""
    for b in balances:
        nb = np.linalg.norm(b)
        if np.linalg.norm(x - b) < tol * (nb if nb > 0 else 1.0):
            return True
    return False


def poincare(x0, par, t_max, balances=(), max_cross=200, rtol=1e-10, atol_scale=1e-14, chunk=10):
    """Section through x0 normal to f(x0), crossed along f(x0); integrated in chunks of crossings.

    Stops early once three consecutive returns agree within 1e-7 (periodic), or once the state is
    within 1e-8 of a balance (it cannot become periodic there)."""
    f0 = f_np(x0, par)
    nf = np.linalg.norm(f0)
    if nf == 0 or not np.isfinite(nf):
        return dict(crossings=[], times=[], status="stationary")
    nvec = f0 / nf
    s = max(np.abs(x0).max(), 1e-300)

    def sec(t, x):
        return float(np.dot(x - x0, nvec))

    sec.direction = 1.0
    sec.terminal = chunk
    crossings, times = [], []
    t_now, x = 0.0, np.array(x0, float)
    note = "max crossings or time"
    while t_now < t_max and len(crossings) < max_cross:
        sol = solve_ivp(lambda t, z: f_np(z, par), (t_now, t_max), x, method="Radau", rtol=rtol,
                        atol=atol_scale * s, jac=lambda t, z: J_np(z, par), events=sec)
        for tt, xx in zip(sol.t_events[0], sol.y_events[0]):
            if tt - t_now <= 1e-12 * max(t_max, 1.0) or (times and tt - times[-1] <= 1e-12 * max(t_max, 1.0)):
                continue
            crossings.append(np.array(xx))
            times.append(float(tt))
        t_now, x = float(sol.t[-1]), sol.y[:, -1].copy()
        if sol.status == -1:
            note = "integration failure"
            break
        if _periodic_index(crossings) is not None:
            note = "periodic"
            break
        if _near(x, balances, 1e-8):
            note = "reached a balance after t_end"
            break
        if sol.status == 0:  # reached t_max
            break
    return dict(crossings=crossings, times=times, note=note)


def _rel_returns(cr):
    rel = []
    for k in range(len(cr) - 1):
        nk = np.linalg.norm(cr[k])
        rel.append(np.linalg.norm(cr[k + 1] - cr[k]) / nk if nk > 0 else np.inf)
    return rel


def _periodic_index(cr):
    rel = _rel_returns(cr)
    for k in range(len(rel) - 2):
        if rel[k] < 1e-7 and rel[k + 1] < 1e-7 and rel[k + 2] < 1e-7:
            return k
    return None


def classify_end(xe, par, balances, t_end, rtol_p=1e-10, max_cross=200):
    """'balance' | 'periodic' | 'unresolved' with details (SPEC §4)."""
    if _near(xe, balances, 1e-8):
        return dict(kind="balance")
    pc = poincare(xe, par, 10.0 * t_end, balances=balances, max_cross=max_cross, rtol=rtol_p)
    cr, tm = pc["crossings"], pc["times"]
    k = _periodic_index(cr)
    if k is not None:
        rel = _rel_returns(cr)
        period = float(np.mean(np.diff(tm[k:k + 4])))
        return dict(kind="periodic", period=period, n_cross=len(cr), point=cr[k + 3].tolist(), rel=rel[k:k + 3])
    rel = _rel_returns(cr)
    return dict(kind="unresolved", n_cross=len(cr), last_rel=rel[-3:], note=pc.get("note"))


def run_starts(par, starts, balances, stable, t_end, rtol=1e-7, atol_scale=1e-12, max_steps=2_000_000):
    out = []
    s = max(np.mean(np.abs(starts), axis=0).max(), 1e-300)
    st = np.array(stable, float).reshape(-1, dim(par)) if len(stable) else np.zeros((0, dim(par)))
    for x0 in starts:
        y, t, status, nsteps = ode23s(np.array(x0, float), par, float(t_end), rtol, atol_scale * s, st, 1e-12,
                                      max_steps)
        rec = dict(status=int(status), steps=int(nsteps), t=float(t))
        if status in (2, 3, 4):
            rec["class"] = dict(kind="unresolved", reason={2: "step limit", 3: "invalid state", 4: "step underflow"}[status])
        elif status == 1:
            rec["class"] = dict(kind="balance")
        else:
            rec["class"] = classify_end(y, par, balances, t_end)
        rec["end"] = y.tolist()
        out.append(rec)
    return out
