"""Planted failures PF5, PF6 and PF1 via FFS (SPEC §3, §4)."""
import math

import numpy as np

from gexit_pr3 import planted as pr3planted
from gexit_pr3 import stats
from . import ffs, race

PF6 = dict(W1=1.0, W2=0.82, lnA1=3.6, lnA2=0.0)
PF6_SIZES = (8, 10, 12, 14, 16, 20, 24, 30)


def pf5(n=100_000, seed=5):
    rows = []
    ok = True
    for a, b in ((1.0, 10.0), (1.0, 100.0), (1.0, 1000.0)):
        rng = np.random.default_rng([seed, int(b)])
        tS = rng.exponential(a, n)
        tD = rng.exponential(b, n)
        passed = tD < tS
        tau = tS[~passed]
        est = race.phi_estimates(tau, b, 0.0, B=500, seed=seed)
        phi = a / (a + b)
        exp_pred = phi / (1 + phi)
        z1 = (est["phi_pred"] - exp_pred) / est["phi_pred_se"]
        z2 = (est["phi_pred_star"] - phi) / est["phi_pred_star_se"]
        good = abs(z1) <= 2 and abs(z2) <= 2
        ok &= good
        rows.append(dict(a=a, b=b, phi_exact=phi, phi_pred_expectation=exp_pred, phi_obs=float(passed.mean()), **est,
                         z_pred=z1, z_star=z2, bias_pred_vs_phi=(est["phi_pred"] - phi) / phi, pass_=bool(good)))
    return dict(rows=rows, pass_=bool(ok))


def pf6_rates(om):
    r1 = math.exp(PF6["lnA1"] - PF6["W1"] * om)
    r2 = math.exp(PF6["lnA2"] - PF6["W2"] * om)
    return r1, r2


def pf6(n=1000, seed=6):
    rng = np.random.default_rng(seed)
    Ts, sig = [], []
    for om in PF6_SIZES:
        r1, r2 = pf6_rates(om)
        t = rng.exponential(1.0 / (r1 + r2), n)
        S, d = t.sum(), n
        lo, hi = stats.chi2_interval(S, d)
        Ts.append(S / d)
        sig.append((math.log(hi) - math.log(lo)) / (2 * 1.959964))
    win = []
    for i in range(1, len(PF6_SIZES) - 1):
        om3 = PF6_SIZES[i - 1:i + 2]
        f = stats.fit_EP(om3, Ts[i - 1:i + 2], sig[i - 1:i + 2])
        mid = PF6_SIZES[i]
        win.append(dict(center=mid, slope=float(f["W"] + f["beta"] / mid)))
    sl = {w["center"]: w["slope"] for w in win}
    # exact local slope of ln(1/(r1+r2)) is (W1 r1 + W2 r2)/(r1 + r2)
    exact = {om: (PF6["W1"] * pf6_rates(om)[0] + PF6["W2"] * pf6_rates(om)[1]) / sum(pf6_rates(om))
             for om in PF6_SIZES}
    through = sl.get(16, 0) > 0.91 > sl.get(24, 1)
    ok = bool(through and sl.get(12, 0) >= 0.95 and sl.get(24, 1) <= 0.90)
    return dict(sizes=list(PF6_SIZES), T=Ts, windows=win, exact_local_slope=exact, crossover_exact=20.0, pass_=ok)


def pf1_ffs(sizes=(20, 30), seed=11, replicates=8, mapper=map):
    rows = []
    ok = True
    for om in sizes:
        ex = pr3planted.pf1_exact(om)["T_qsd"]
        r = ffs.run_size("ID", om, np.zeros(11), np.array([om, 0, 0, 0], np.int64), 10.0, seed * 1000 + om,
                         replicates=replicates, basin_mult=1.0, mapper=mapper)
        rel = abs(r["T"] - ex) / ex if "T" in r else None
        good = rel is not None and rel <= 0.10
        ok &= good
        rows.append(dict(Omega=om, T_ffs=r.get("T"), T_se=r.get("T_se"), T_exact=ex, rel_err=rel, pass_=bool(good),
                         n_ok=r["n_ok"], cpu=r["cpu"], interfaces=r["replicates"][0].get("interfaces")))
    return dict(rows=rows, pass_=bool(ok))
