# Copied from grammar-exit-time/gexit/ (PR 3, gomni1/ClaudeCloud1#3) for task grammar-idsize; changes are marked "idsize:".
"""Planted failures PF1-PF4 (SPEC §9): exact comparators and harness runs."""
import math

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.stats import poisson

from . import series, sim, stats

PF1_GRID = [2, 4, 6, 8, 10, 12]
PF2_GRID = [8, 12, 16, 20, 24, 32, 48, 64]
PF1_TBURN = 10.0


def _id_trunc(om):
    return int(om + 40 * math.sqrt(om) + 60)


def pf1_exact(om):
    """Immigration-death, target n = 0.  1/lambda0 of the generator restricted to n >= 1,
    checked against sum_n q_n T_n with birth-death sums T_n."""
    N = _id_trunc(om)
    n = np.arange(1, N + 1, dtype=float)
    birth = np.full(N, float(om))
    birth[-1] = 0.0  # truncation: birth suppressed at N
    diag = birth + n
    # symmetrise the reversible chain: off-diagonal sqrt(b_n d_{n+1})
    off = np.sqrt(birth[:-1] * n[1:])
    w, v = eigh_tridiagonal(diag, off, select="i", select_range=(0, 0))
    lam0 = float(w[0])
    # QSD: left eigenvector q = v * sqrt(pi) up to normalisation (pi = detailed-balance weights)
    logpi = n * math.log(om) - np.array([math.lgamma(k + 1) for k in n])
    q = np.abs(v[:, 0]) * np.exp(0.5 * (logpi - logpi.max()))
    q /= q.sum()
    # birth-death sums with pi = Poisson(om): tau_k = P(X >= k) / (k pi_k)
    pk = poisson.pmf(n, om)
    tail = poisson.sf(n - 1, om)
    tau = tail / (n * pk)
    Tn = np.cumsum(tau)
    T_sum = float(np.sum(q * Tn))
    pi0 = poisson.pmf(np.arange(0, N + 1), om)
    T_pois = float(np.sum(pi0[1:] * Tn))  # from Poisson start (0 contributes 0)
    return dict(Omega=om, T_qsd=1.0 / lam0, lambda0=lam0, T_sum=T_sum, T_from_poisson=T_pois,
                T1=float(Tn[0]), truncation=N)


def pf2_exact(om):
    """Neutral drift: MFPT from n = om/2 to n <= om/4 or n >= 3om/4 (birth-death chain)."""
    lo, hi = om // 4, 3 * om // 4
    states = np.arange(lo + 1, hi)
    r = states * (om - states) / om  # each direction
    m = len(states)
    A = np.zeros((m, m))
    for i in range(m):
        A[i, i] = 2 * r[i]
        if i > 0:
            A[i, i - 1] = -r[i]
        if i < m - 1:
            A[i, i + 1] = -r[i]
    T = np.linalg.solve(A, np.ones(m))
    return float(T[np.flatnonzero(states == om // 2)[0]])


def arm_pf1():
    return series.Arm("X0", "ID", lambda om: [om, 0, 0, 0], "X0", PF1_TBURN)


def arm_pf2():
    return series.Arm("XOUT", "ND", lambda om: [om // 2, om - om // 2, 0, 0], "XOUT", 0.0,
                      ta_fn=lambda om: om // 4, tb_fn=lambda om: 3 * om // 4)


def run_pf1(log=print):
    return series.run_series("PF1", [arm_pf1()], PF1_GRID, budget=math.inf, fixed=True, log=log)


def run_pf2(log=print):
    return series.run_series("PF2", [arm_pf2()], PF2_GRID, budget=math.inf, fixed=True, log=log)


def run_pf3(om=8, n=1000, frac=0.3):
    ex = pf1_exact(om)["T_qsd"]
    cap = ex * math.log(1.0 / frac)
    tasks = [dict(model="ID", omega=om, n0=[om, 0, 0, 0], target="X0", t_burn=PF1_TBURN, cap=cap,
                  nruns=n // 8, seed=sim.seed_for("PF3", om, b)) for b in range(8)]
    res = sim.map_batches(tasks)
    t = np.concatenate([r["time"] for r in res])
    c = np.concatenate([r["cens"] for r in res]).astype(bool)
    T, S, d = stats.mle(t, c)
    lo, hi = stats.chi2_interval(S, d)
    naive = float(t.mean())
    return dict(Omega=om, cap=cap, T_exact=ex, n=len(t), censored=int(c.sum()), cens_frac=float(c.mean()),
                T_mle=T, chi2_lo=lo, chi2_hi=hi, naive_mean=naive,
                pass_mle=bool(lo <= ex <= hi), pass_naive_low=bool(naive < ex and naive < lo),
                cpu=float(sum(r["cpu"] for r in res)))


def run_pf4(n=1000, k=4, B=10000):
    rng = np.random.default_rng(sim.seed_for("PF4") % 2**32)
    x = rng.gamma(k, 1.0 / k, size=n)
    r = stats.lilliefors_exp(x, B=B, rng=sim.seed_for("PF4", "boot") % 2**32)
    r["pass"] = bool(r["p"] < 0.01)
    return r


def evaluate_pf1(s, B=2000):
    sizes = series.fitted_sizes(s, "X0")
    f = stats.f1(sizes, B=B, rng=sim.seed_for("F1", "PF1") % 2**32)
    rows = []
    for (om, t, c), T in zip(sizes, f["T"]):
        ex = pf1_exact(om)
        S, d = float(np.sum(t)), int((~c).sum())
        lo, hi = stats.chi2_interval(S, d)
        blo, bhi = stats.chi2_interval(S, d, level=1 - 0.05 / 6)
        rows.append(dict(Omega=om, T_hat=T, chi2_lo=lo, chi2_hi=hi, T_exact=ex["T_qsd"], T_sum=ex["T_sum"],
                         covered=bool(lo <= ex["T_qsd"] <= hi), covered_bonferroni=bool(blo <= ex["T_qsd"] <= bhi),
                         bonf_lo=blo, bonf_hi=bhi))
    return dict(fit=f, rows=rows, pass_W=bool(abs(f["W"] - 1.0) <= 0.05),
                pass_coverage=all(r["covered"] for r in rows),
                pass_coverage_bonferroni=all(r["covered_bonferroni"] for r in rows))


def evaluate_pf2(s, B=2000):
    sizes = series.fitted_sizes(s, "XOUT")
    f = stats.f1(sizes, B=B, rng=sim.seed_for("F1", "PF2") % 2**32)
    rows = [dict(Omega=om, T_hat=T, T_exact=pf2_exact(om), cv=float(np.std(t, ddof=1) / np.mean(t)))
            for (om, t, c), T in zip(sizes, f["T"])]
    return dict(fit=f, rows=rows, pass_=bool(f["k1_any"]))
