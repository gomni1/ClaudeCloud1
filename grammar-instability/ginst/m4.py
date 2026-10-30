"""M4: verification of hits (SPEC §6)."""
import math

import numpy as np
from scipy.integrate import solve_ivp

from . import integ, model


def verify_cycle(par, x0, period_guess):
    """LSODA and Radau at rtol 1e-10; Floquet multipliers from the monodromy matrix."""
    n = model.dim(par)
    f = lambda t, z: model.f_np(z, par)
    out = {}
    for meth in ("LSODA", "Radau"):
        cr = integ.poincare(np.array(x0), par, 50 * period_guess, balances=[], max_cross=12, rtol=1e-10)
        out[meth] = dict(period=float(np.mean(np.diff(cr["times"][-6:]))) if len(cr["times"]) >= 6 else None)
    # monodromy over one period from a point on the cycle
    T = out["Radau"]["period"]

    def var(t, z):
        x = z[:n]
        Phi = z[n:].reshape(n, n)
        return np.concatenate([model.f_np(x, par), (model.J_np(x, par) @ Phi).ravel()])

    z0 = np.concatenate([np.array(x0, float), np.eye(n).ravel()])
    sol = solve_ivp(var, (0, T), z0, method="Radau", rtol=1e-10, atol=1e-14)
    mult = np.linalg.eigvals(sol.y[n:, -1].reshape(n, n))
    pL, pR = out["LSODA"]["period"], out["Radau"]["period"]
    agree = pL is not None and pR is not None and abs(pL - pR) / pR <= 1e-6
    mods = np.sort(np.abs(mult))[::-1]
    return dict(periods=out, agree=bool(agree), multipliers=[[float(z.real), float(z.imag)] for z in mult],
                moduli=mods.tolist())


def verify_lattice(f_sites, J, D, s_star, x_bal, n_sites=200, seed=3):
    """Ring of n_sites compartments: dX_i = f(X_i) + kappa D (X_{i+1} - 2 X_i + X_{i-1})."""
    kappa = s_star / (2 * (1 - math.cos(2 * math.pi * 10 / n_sites)))
    ns = len(x_bal)
    rng = np.random.default_rng(seed)
    X0 = (np.tile(x_bal, (n_sites, 1)) * (1 + 0.01 * rng.uniform(-1, 1, (n_sites, ns)))).ravel()
    ev = np.linalg.eigvals(J - s_star * np.diag(D))
    growth = float(np.max(ev.real))
    t_end = 50.0 / growth

    def rhs(t, z):
        X = z.reshape(n_sites, ns)
        lap = np.roll(X, 1, 0) - 2 * X + np.roll(X, -1, 0)
        return (f_sites(X) + kappa * lap * D[None, :]).ravel()

    ts = np.linspace(0, t_end, 101)
    sol = solve_ivp(rhs, (0, t_end), X0, method="Radau", rtol=1e-8, atol=1e-12, t_eval=ts)
    amps = []
    for k in range(sol.y.shape[1]):
        X = sol.y[:, k].reshape(n_sites, ns) - x_bal[None, :]
        amps.append(float(np.abs(np.fft.fft(X, axis=0)[10]).max()))
    amps = np.array(amps)
    i1 = int(np.argmax(amps > 10 * amps[0])) if np.any(amps > 10 * amps[0]) else None
    rate = math.log(amps[min(20, len(amps) - 1)] / amps[0]) / ts[min(20, len(amps) - 1)] if amps[0] > 0 else None
    Xf = sol.y[:, -1].reshape(n_sites, ns)
    return dict(kappa=kappa, predicted_growth=growth, measured_initial_rate=rate, grew_10x=i1 is not None,
                rate_within_20pct=bool(rate is not None and abs(rate - growth) / growth <= 0.2),
                final_range=[float(Xf[:, j].max() - Xf[:, j].min()) for j in range(ns)], status=int(sol.status))
