"""Part B driver: one (direction, Omega) cell under a CPU-time budget (SPEC §4)."""
import os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim_b import run_batch, seed_rng

K = np.array((2, 9, 47, 1, 1, 1, 1, 1, 1, 13, 0.5), dtype=np.float64)
TOL = 0.25
MAX_EVENTS = 10_000_000
BLOCK = 500
RUN_GUARD = 2_000_000          # resource guard, far above the required 2000

BALANCE = {"up": (1.0, 2.0, 1.0, 0.5), "down": (1.0, 4.0, 1.0, 0.5)}
TARGETV = {"up": 4.0, "down": 2.0}


def run_cell(direction, Omega, budget_cpu_s=180.0, min_runs=2000, seed=777):
    c, v, l, p = BALANCE[direction]
    nC0 = int(round(c * Omega)); nV0 = int(round(v * Omega))
    nL0 = int(round(l * Omega)); nP0 = int(round(p * Omega))
    seed_rng(np.int64(seed))

    vis = np.empty(BLOCK, np.int64); dl = np.empty(BLOCK, np.float64)
    evs = np.empty(BLOCK, np.int64); ok = np.empty(BLOCK, np.int64)
    tm = np.empty(BLOCK, np.float64)

    V, D, E, T, n_cap = [], [], [], [], 0
    cpu0 = time.process_time()
    n_done = 0
    while True:
        used = time.process_time() - cpu0
        if n_done >= min_runs and (used >= budget_cpu_s or n_done >= RUN_GUARD):
            break
        run_batch(BLOCK, nC0, nV0, nL0, nP0, float(Omega), K, TARGETV[direction],
                  TOL, MAX_EVENTS, vis, dl, evs, ok, tm)
        good = ok == 1
        n_cap += int((~good).sum())
        V.append(vis[good].copy()); D.append(dl[good].copy())
        E.append(evs[good].copy()); T.append(tm[good].copy())
        n_done += int(good.sum())
    cpu = time.process_time() - cpu0

    V = np.concatenate(V); D = np.concatenate(D)
    E = np.concatenate(E); T = np.concatenate(T)
    npass = int(V.sum())
    nonp = D[V == 0]
    return dict(direction=direction, Omega=int(Omega), n_runs=int(V.size),
                n_capped=int(n_cap), cpu_s=float(cpu), seed=int(seed),
                n_passed_D=npass, passage_fraction=float(npass / V.size),
                n_nonpassing=int(nonp.size),
                median_delta_nonpassing=float(np.median(nonp)) if nonp.size else float("nan"),
                mean_delta_nonpassing=float(nonp.mean()) if nonp.size else float("nan"),
                delta_quantiles={str(q): float(np.quantile(nonp, q))
                                 for q in (0.1, 0.25, 0.5, 0.75, 0.9)} if nonp.size else {},
                delta_hist_counts=np.bincount(
                    np.rint(nonp * Omega).astype(np.int64), minlength=1).tolist(),
                mean_events=float(E.mean()), mean_model_time=float(T.mean()))


def _job(a):
    return run_cell(*a)
