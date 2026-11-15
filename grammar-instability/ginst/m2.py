"""M2: cycle search under TH (SPEC §4)."""
import gzip
import json
import time

import numpy as np
from scipy.optimize import minimize

from . import integ, model

VARIANTS = (("open", "cv"), ("closed", "cv"), ("open", "tot"), ("closed", "tot"))
SEED = 30102026


def draw_params(i, law="TH"):
    rng = np.random.default_rng([SEED, i])
    level, den = VARIANTS[i % 4]
    k = 10.0 ** rng.uniform(-3, 3, 11)
    m = int(rng.integers(2, 13))
    kr, kc = (int(v) for v in rng.integers(1, m + 1, 2))
    T = float(10.0 ** rng.uniform(-1, 2))
    return dict(i=i, level=level, den=den, k=k.tolist(), m=m, kr=kr, kc=kc, T=T, law=law)


def par_of(d):
    return model.make_par(np.array(d["k"]), d["law"], d["den"], d["level"], d["m"], d["kr"], d["kc"], d["T"])


def rates_in_use(d):
    k = np.array(d["k"])
    if d["level"] == "closed":
        k = np.delete(k, [7, 10])  # k9, k12 unused
    if d["law"] == "MA":
        pass
    return k


def scores(bals, closed):
    """delta_rel and omega over stable balances."""
    drel, om = np.inf, 0.0
    for r in bals:
        if not r["stable"]:
            continue
        ev = r["eig"]
        mx = np.max(np.abs(ev))
        drel = min(drel, -np.max(ev.real) / mx if mx > 0 else np.inf)
        cpx = ev[np.abs(ev.imag) > 1e-12 * mx]
        if len(cpx):
            om = max(om, float(np.max(np.abs(cpx.imag) / np.abs(cpx.real))))
    return float(drel), float(om)


def starts_for(d, bals, rng):
    if d["level"] == "closed":
        w = rng.dirichlet(np.ones(4), size=8)
        return w * d["T"]
    big = max(bals, key=lambda r: np.linalg.norm(r["b"]))["b"] if bals else np.ones(4)
    s = float(np.mean(big))
    return s * 10.0 ** rng.uniform(-2, 2, size=(8, 4))


def process(d):
    t0 = time.process_time()
    par = par_of(d)
    bals = model.classify_balances(par)
    rng = np.random.default_rng([SEED, d["i"], 7])
    starts = starts_for(d, bals, rng)
    t_end = 1e3 / float(np.min(rates_in_use(d)))
    stable = [r["b"] for r in bals if r["stable"]]
    allb = [r["b"] for r in bals]
    runs = integ.run_starts(par, starts, allb, stable, t_end)
    drel, om = scores(bals, d["level"] == "closed")
    kinds = [r["class"]["kind"] for r in runs]
    rec = dict(d)
    rec.update(n_bal=len(bals), n_stable=len(stable),
               bal=[dict(b=r["b"].tolist(), stable=r["stable"], maxre=float(np.max(r["eig"].real)),
                         eig=[[float(z.real), float(z.imag)] for z in r["eig"]]) for r in bals],
               kinds=kinds, n_balance=kinds.count("balance"), n_periodic=kinds.count("periodic"),
               n_unresolved=kinds.count("unresolved"), max_steps=max(r["steps"] for r in runs),
               delta_rel=drel, omega=om, t_end=t_end, cpu=time.process_time() - t0)
    if rec["n_periodic"] or rec["n_unresolved"]:
        rec["runs"] = runs
    return rec


def process_chunk(idx):
    return [process(draw_params(i)) for i in idx]


def nm_objective(x, base):
    d = dict(base)
    d["k"] = (10.0 ** x[:11]).tolist()
    if d["level"] == "closed":
        d["T"] = float(10.0 ** x[11])
    par = par_of(d)
    try:
        bals = model.classify_balances(par)
    except Exception:
        return 1.0
    stab = [r for r in bals if r["stable"]]
    if not stab:
        return 1.0
    best = 1.0
    for r in stab:
        ev = r["eig"]
        mx = np.max(np.abs(ev))
        best = min(best, -np.max(ev.real) / mx)
    return float(best)


def nm_run(base, maxfev=1000):
    x0 = np.log10(np.array(base["k"]))
    if base["level"] == "closed":
        x0 = np.append(x0, np.log10(base["T"]))
    hist = []

    def f(x):
        v = nm_objective(x, base)
        hist.append((v, x.copy()))
        return v

    res = minimize(f, x0, method="Nelder-Mead", options=dict(maxfev=maxfev, xatol=1e-10, fatol=1e-14))
    hist.sort(key=lambda t: t[0])
    best_v, best_x = hist[0]
    return dict(i=base["i"], f0=float(hist and nm_objective(x0, base)), f_best=float(best_v), x_best=best_x.tolist(),
                nfev=len(hist), low_points=[dict(f=float(v), x=xx.tolist()) for v, xx in hist if v <= 1e-6][:20])
