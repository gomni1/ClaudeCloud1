"""Part 1: switching runs, T_D^0 runs, phi_obs and phi_pred (SPEC §2)."""
import math
import time

import numpy as np
from scipy.stats import beta

from gexit_pr3 import sim
from . import family

SIZES = (2, 3, 4, 5, 6, 8, 10, 12, 16)


def start_counts(om, v):
    return np.array([om, v * om, om, int(math.floor(om / 2 + 0.5))], np.int64)


def clopper_pearson(d, n, level=0.95):
    a = 1 - level
    lo = beta.ppf(a / 2, d, n - d + 1) if d > 0 else 0.0
    hi = beta.ppf(1 - a / 2, d + 1, n - d) if d < n else 1.0
    return float(lo), float(hi)


def switching_runs(k10, om, direction, max_pass=50, max_runs=1_000_000, seed=0):
    """Runs until max_pass passages through D or max_runs runs.  Returns times, secD flags, censoring."""
    k = family.kvec(k10)
    v0, tgt, ta = (2, "VGE", 4 * om) if direction == "up" else (4, "VLE", 2 * om)
    n0 = start_counts(om, v0)
    times, secd, cens = [], [], []
    cpu = 0.0
    batch = 2000
    b = 0
    Tm = 10.0
    while sum(secd) < max_pass and len(times) < max_runs:
        nr = min(batch, max_runs - len(times))
        r = sim.run_exits(dict(model="TH", omega=om, n0=n0, target=tgt, ta=ta, t_burn=0.0, cap=1e4 * Tm, nruns=nr,
                               seed=sim.seed_for("idsize-switch", k10, om, direction, seed, b), k=k))
        times += r["time"].tolist()
        secd += r["secD"].tolist()
        cens += r["cens"].tolist()
        cpu += r["cpu"]
        b += 1
        t = np.asarray(times)
        c = np.asarray(cens, bool)
        Tm = max(Tm, float(t[~c].mean())) if (~c).any() else Tm
        batch = min(200_000, batch * 2)
    return dict(times=np.asarray(times), secD=np.asarray(secd, bool), cens=np.asarray(cens, bool), cpu=cpu)


def td0_runs(k10, om, direction, cpu_cap=900.0, rel_se=0.05, min_runs=400, seed=0):
    """Mean first-passage time to D from the same start, no burn-in.  Stops only between batches
    (no run is ever cut short), with batch sizes set from the measured cost per run."""
    k = family.kvec(k10)
    v0 = 2 if direction == "up" else 4
    n0 = start_counts(om, v0)
    times, cens = [], []
    cpu = 0.0
    b = 0
    Tm = 1e3
    nr = 4
    while True:
        r = sim.run_exits(dict(model="TH", omega=om, n0=n0, target="D", t_burn=0.0, cap=1e6 * Tm, nruns=nr,
                               seed=sim.seed_for("idsize-td0", k10, om, direction, seed, b), k=k))
        times += r["time"].tolist()
        cens += r["cens"].tolist()
        cpu += r["cpu"]
        b += 1
        t = np.asarray(times)
        Tm = float(t.mean())
        se = float(t.std(ddof=1) / math.sqrt(len(t))) if len(t) > 1 else float("inf")
        if (len(t) >= min_runs and se / Tm <= rel_se) or cpu >= cpu_cap:
            break
        per_run = cpu / len(t)
        nr = int(max(1, min(5000, 0.5 * (cpu_cap - cpu) / max(per_run, 1e-9), 2 * len(t))))
    t = np.asarray(times)
    return dict(T=float(t.mean()), se=float(t.std(ddof=1) / math.sqrt(len(t))) if len(t) > 1 else float("nan"),
                n=len(t), censored=int(np.sum(cens)), cpu=cpu)


def phi_estimates(tau_S, T, T_se, B=2000, seed=0):
    """phi_pred (brief's estimator) and phi_pred* (inverse-weighted), with bootstrap SEs."""
    tau_S = np.asarray(tau_S, float)
    rng = np.random.default_rng(seed)

    def est(ts, Td):
        e = np.exp(-ts / Td)
        p1 = 1.0 - e.mean()
        p2 = 1.0 - 1.0 / np.exp(ts / Td).mean()
        return p1, p2

    p1, p2 = est(tau_S, T)
    n = len(tau_S)
    bs1, bs2 = [], []
    for _ in range(B):
        ts = tau_S[rng.integers(0, n, n)]
        Td = T + T_se * rng.standard_normal() if T_se > 0 else T
        Td = max(Td, 1e-12)
        a, b_ = est(ts, Td)
        bs1.append(a)
        bs2.append(b_)
    return dict(phi_pred=float(p1), phi_pred_se=float(np.std(bs1, ddof=1)), phi_pred_star=float(p2),
                phi_pred_star_se=float(np.std(bs2, ddof=1)))


def summarize(sw, td):
    d = int(sw["secD"].sum())
    n = len(sw["secD"])
    phi = d / n
    lo, hi = clopper_pearson(d, n)
    tau = sw["times"][(~sw["secD"]) & (~sw["cens"])]
    est = phi_estimates(tau, td["T"], td["se"])
    se_obs = math.sqrt(phi * (1 - phi) / n) if n else float("nan")
    return dict(n_runs=n, passages=d, phi_obs=phi, phi_lo=lo, phi_hi=hi, phi_obs_se=se_obs,
                tau_S_mean=float(tau.mean()) if len(tau) else float("nan"), n_tau=len(tau),
                capped=int(sw["cens"].sum()), T_D0=td["T"], T_D0_se=td["se"], T_D0_n=td["n"], **est)
