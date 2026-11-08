"""Routes test driver: one (direction, Omega) cell (SPEC §4).

Generation stops as soon as EITHER at least 3000 switching runs that did not
visit D have completed, OR the 5-CPU-minute budget is spent -- whichever comes
first. Runs are generated in blocks of 100 and every completed run of every
block is kept, so the non-passing count may slightly exceed 3000; keeping the
whole block is unbiased because runs are i.i.d.
"""
import os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim_routes import run_batch, seed_rng

K = np.array((2, 9, 47, 1, 1, 1, 1, 1, 1, 13, 0.5), dtype=np.float64)
TOL = 0.25
MAX_EVENTS = 10_000_000
BLOCK = 100
MIN_NONPASSING = 3000
BUDGET = 300.0
SEED_BASE = 5_000_000          # declared in SPEC §4; disjoint from all earlier work

BALANCE = {"up": (1.0, 2.0, 1.0, 0.5), "down": (1.0, 4.0, 1.0, 0.5)}
TARGETV = {"up": 4.0, "down": 2.0}
SIZES = [8, 10, 12, 16]
DIRS = ["up", "down"]


def cell_seed(direction, Omega):
    return SEED_BASE + 1000 * DIRS.index(direction) + SIZES.index(Omega)


def run_cell(direction, Omega, budget_cpu_s=BUDGET, min_nonpassing=MIN_NONPASSING,
             seed=None):
    if seed is None:
        seed = cell_seed(direction, Omega)
    c, v, l, p = BALANCE[direction]
    n0 = (int(round(c * Omega)), int(round(v * Omega)),
          int(round(l * Omega)), int(round(p * Omega)))
    seed_rng(np.int64(seed))

    vis = np.empty(BLOCK, np.int64); dl = np.empty(BLOCK, np.float64)
    evs = np.empty(BLOCK, np.int64); ok = np.empty(BLOCK, np.int64)
    tm = np.empty(BLOCK, np.float64)

    V, D, E = [], [], []
    n_cap = 0
    n_nonpassing = 0
    cpu0 = time.process_time()
    while n_nonpassing < min_nonpassing and (time.process_time() - cpu0) < budget_cpu_s:
        run_batch(BLOCK, n0[0], n0[1], n0[2], n0[3], float(Omega), K,
                  TARGETV[direction], TOL, MAX_EVENTS, vis, dl, evs, ok, tm)
        good = ok == 1
        n_cap += int((~good).sum())
        V.append(vis[good].copy()); D.append(dl[good].copy()); E.append(evs[good].copy())
        n_nonpassing += int((vis[good] == 0).sum())
    cpu = time.process_time() - cpu0

    V = np.concatenate(V); D = np.concatenate(D); E = np.concatenate(E)
    # delta lives on the lattice k/Omega; store the integer level k losslessly
    lev = np.rint(D * Omega).astype(np.int32)
    assert np.allclose(lev / Omega, D), "delta is not on the 1/Omega lattice"
    return dict(direction=direction, Omega=int(Omega), seed=int(seed),
                n_runs=int(V.size), n_capped=int(n_cap),
                n_passed_D=int(V.sum()),
                passage_fraction=float(V.sum() / V.size),
                n_nonpassing=int((V == 0).sum()),
                cpu_s=float(cpu), mean_events=float(E.mean()),
                budget_hit=bool(cpu >= budget_cpu_s),
                levels=lev.tolist(), visitD=V.astype(np.int8).tolist())


def _job(a):
    return run_cell(*a)
