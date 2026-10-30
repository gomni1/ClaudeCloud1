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
    # both integrators start 1% of a period downstream of x0; the section stays the one through x0
    x1 = solve_ivp(f, (0, 0.01 * period_guess), np.array(x0, float), method="Radau", rtol=1e-12, atol=1e-15,
                   jac=lambda t, z: model.J_np(z, par)).y[:, -1]
    for meth in ("LSODA", "Radau"):
        cr = integ.poincare(np.array(x0), par, 50 * period_guess, balances=[], max_cross=12, rtol=1e-10, method=meth,
                            x_start=x1)
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


# ---------------------------------------------------------------- the 200-site ring (SPEC §6), vectorised
# verify_lattice above (harness commit) took max |FFT_10| over roles and fitted the rate over the first
# 20% of the run, into the saturated regime.  verify_ring implements the SPEC's measure instead: the
# projection of FFT mode 10 onto the leading eigenvector (left-eigenvector coefficient), with the rate
# fitted over the window in which that coefficient grows 10-fold.  Replaced before any ring was run.
from numba import njit
import scipy.sparse as sp
from .model import rhs as _rhs, jac as _jac


@njit(cache=True)
def _ring_f(z, par, ns, nsite, kD, out):
    tmp = np.empty(ns)
    for i in range(nsite):
        _rhs(z[i * ns:(i + 1) * ns], par, tmp)
        ip = (i + 1) % nsite
        im = (i - 1) % nsite
        for r in range(ns):
            out[i * ns + r] = tmp[r] + kD[r] * (z[ip * ns + r] - 2.0 * z[i * ns + r] + z[im * ns + r])


@njit(cache=True)
def _ring_blocks(z, par, ns, nsite, out):
    Jm = np.empty((ns, ns))
    for i in range(nsite):
        _jac(z[i * ns:(i + 1) * ns], par, Jm)
        out[i] = Jm


def _leading(M, kind):
    lam, V = np.linalg.eig(M)
    W = np.linalg.inv(V)
    sc = np.max(np.abs(lam))
    cplx = np.abs(lam.imag) > 1e-9 * sc
    idx = np.where(cplx if kind == "osc" else ~cplx)[0]
    if len(idx) == 0:
        return lam, None, None
    k = idx[np.argmax(lam.real[idx])]
    return lam, k, W[k]


def _classify_pattern(ts, Z, n_sites, ns, x_bal):
    X = Z.reshape(n_sites, ns, -1)
    a = X[:, :, -1]
    b = X[:, :, int(0.9 * (Z.shape[1] - 1))]
    scale = np.max(np.abs(a))
    if not np.all(np.isfinite(a)) or scale > 1e6 * np.max(np.abs(x_bal)):
        return "unbounded"
    spread = np.max(a.max(axis=0) - a.min(axis=0)) / max(np.max(np.abs(x_bal)), 1e-300)
    if spread < 1e-6:
        return "homogeneous"
    if np.max(np.abs(a - b)) <= 1e-4 * scale:
        return "stationary"
    shifts = [np.max(np.abs(np.roll(b, s, axis=0) - a)) for s in range(1, n_sites)]
    if min(shifts) <= 1e-2 * scale:
        return "travelling wave (shift %d sites over the last 10%% of the run)" % (1 + int(np.argmin(shifts)))
    return "time-dependent, not a rigid travel (standing wave or irregular)"


def verify_ring(par, x_bal, D, s_star, kind, n_sites=200, seed=3, cpu_cap=600.0):
    import time as _t
    c0 = _t.process_time()
    x_bal = np.asarray(x_bal, float)
    ns = len(x_bal)
    D = np.asarray(D, float)
    J = model.J_np(x_bal, par)
    lam, k, w = _leading(J - s_star * np.diag(D), kind)
    if k is None or lam[k].real <= 0:
        return dict(kind=kind, s_star=s_star, D=D.tolist(), verified=False, predicted_rate=None, measured_rate=None,
                    note="no %s eigenvalue with Re > 0 at s*" % ("complex" if kind == "osc" else "real"),
                    eig_at_s_star=[[float(z.real), float(z.imag)] for z in lam], cpu=_t.process_time() - c0)
    pred = float(lam[k].real)
    kappa = s_star / (2 * (1 - math.cos(2 * math.pi * 10 / n_sites)))
    kD = kappa * D
    # fastest growth over all ring modes, for the record
    sj = [2 * kappa * (1 - math.cos(2 * math.pi * j / n_sites)) for j in range(n_sites // 2 + 1)]
    gj = [float(np.max(np.linalg.eigvals(J - s * np.diag(D)).real)) for s in sj]
    lap = sp.diags([np.ones(n_sites - 1), -2 * np.ones(n_sites), np.ones(n_sites - 1)], [-1, 0, 1], format="lil")
    lap[0, n_sites - 1] = 1.0
    lap[n_sites - 1, 0] = 1.0
    Ldiff = sp.kron(lap.tocsr(), sp.diags(kD)).tocsr()
    blocks = np.empty((n_sites, ns, ns))

    def f(t, z):
        out = np.empty_like(z)
        _ring_f(z, par, ns, n_sites, kD, out)
        return out

    def jacf(t, z):
        _ring_blocks(z, par, ns, n_sites, blocks)
        return (sp.block_diag(list(blocks), format="csr") + Ldiff).tocsc()

    rng = np.random.default_rng(seed)
    X0 = (np.tile(x_bal, (n_sites, 1)) * (1 + 0.01 * rng.uniform(-1, 1, (n_sites, ns)))).ravel()
    atol = 1e-12 * np.max(np.abs(x_bal))

    def coeff(Z):
        X = Z.reshape(n_sites, ns, -1) - x_bal[None, :, None]
        return np.abs(w @ np.fft.fft(X, axis=0)[10])

    # phase 1: linear window, to 6/pred (the coefficient grows ~400-fold if linear)
    t1 = 6.0 / pred
    ts1 = np.linspace(0, t1, 241)
    s1 = solve_ivp(f, (0, t1), X0, method="Radau", rtol=1e-8, atol=atol, jac=jacf, t_eval=ts1)
    c = coeff(s1.y)
    rec = dict(kind=kind, s_star=s_star, D=D.tolist(), kappa=kappa, predicted_rate=pred,
               eig_at_s_star=[[float(z.real), float(z.imag)] for z in lam], fastest_ring_mode=int(np.argmax(gj)),
               fastest_ring_rate=float(np.max(gj)), status1=int(s1.status), c0=float(c[0]))
    hit = np.where(c >= 10 * c[0])[0]
    if len(hit) and s1.status == 0:
        i10 = int(hit[0])
        tt, lc = s1.t[:i10 + 1], np.log(c[:i10 + 1])
        rate = float(np.polyfit(tt, lc, 1)[0])
        rec.update(t_10x=float(s1.t[i10]), measured_rate=rate, grew_10x=True)
    else:
        rec.update(grew_10x=False, measured_rate=None)
    rec["rate_within_20pct"] = bool(rec["measured_rate"] is not None and abs(rec["measured_rate"] - pred) <= 0.2 * pred)
    rec["verified"] = bool(rec["grew_10x"] and rec["rate_within_20pct"])
    # phase 2: on to 50 e-folding times, in chunks, under a CPU cap; report what the pattern saturates to
    t, z, done = float(s1.t[-1]), s1.y[:, -1], s1.status == 0
    t_end = 50.0 / pred
    last = None
    while done and t < t_end - 1e-12 * t_end:
        if _t.process_time() - c0 > cpu_cap:
            rec["phase2_note"] = "CPU cap at t = %.4g of %.4g" % (t, t_end)
            break
        tn = min(t_end, t + 5.0 / pred)
        s2 = solve_ivp(f, (t, tn), z, method="Radau", rtol=1e-8, atol=atol, jac=jacf,
                       t_eval=np.linspace(t, tn, 21))
        if s2.status != 0:
            rec["phase2_note"] = "integration failure at t = %.4g: %s" % (s2.t[-1], s2.message)
            last = s2
            break
        t, z, last = float(s2.t[-1]), s2.y[:, -1], s2
    if last is not None:
        rec["t_reached"] = float(last.t[-1])
        rec["pattern"] = _classify_pattern(last.t, last.y, n_sites, ns, x_bal)
        Xf = last.y[:, -1].reshape(n_sites, ns)
        rec["final_min"] = Xf.min(axis=0).tolist()
        rec["final_max"] = Xf.max(axis=0).tolist()
    rec["cpu"] = _t.process_time() - c0
    return rec
