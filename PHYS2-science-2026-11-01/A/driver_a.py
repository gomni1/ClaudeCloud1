"""Part A driver: runs one (model, Omega) cell under a CPU-time budget."""
import os, sys, time
import numpy as np
from numba import njit
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models_a import MODELS, get_cycle, initial_counts
from sim_a import run_chunk

CHUNK = 400_000


@njit(cache=True)
def _seed(s):
    np.random.seed(s)
    return np.random.random()


def run_cell(name, Omega, R, budget_cpu_s, max_exits=2000, seed=12345,
             burn_periods=20.0, exit_log_cap=200_000):
    """Simulate one cell. Burn-in is excluded from the CPU budget."""
    M = MODELS[name]
    T, cyc, sig = get_cycle(name)
    invsig = (1.0 / sig).astype(np.float64)
    cycS = (cyc / sig).astype(np.float64)
    binom = np.array([comb(M["m"], i) for i in range(M["m"] + 1)], dtype=np.float64)
    kk = np.array(M["k"], dtype=np.float64)
    is_open = 1.0 if M["level"] == "open" else 0.0

    n = initial_counts(M, Omega, cyc)
    aux = np.zeros(4)
    occ = np.zeros(10); occ_armed = np.zeros(10); exits = np.zeros(10)
    elog = np.zeros(exit_log_cap)

    _seed(np.int64(seed))

    t_burn = burn_periods * T
    # --- burn-in (not timed, not accumulated) ---
    while aux[0] < t_burn:
        ev, _ = run_chunk(n, aux, kk, M["m"], M["kr"], M["kc"], is_open, float(Omega),
                          binom, cycS, invsig, R, t_burn, occ, occ_armed, exits,
                          elog, CHUNK, 10**9)
        if ev == 0:
            break
    t_start_sim = aux[0]

    # --- timed production ---
    cpu0 = time.process_time()
    n_ev = 0
    while True:
        used = time.process_time() - cpu0
        if used >= budget_cpu_s or aux[3] >= max_exits:
            break
        rem = int(max_exits - aux[3])
        ev, _ = run_chunk(n, aux, kk, M["m"], M["kr"], M["kc"], is_open, float(Omega),
                          binom, cycS, invsig, R, t_burn, occ, occ_armed, exits,
                          elog, CHUNK, rem)
        n_ev += ev
        if ev == 0:
            break
    cpu_used = time.process_time() - cpu0

    n_exit = int(aux[3])
    return dict(model=name, Omega=int(Omega), R=float(R), T=T,
                sim_time=float(aux[0] - t_start_sim),
                periods=float((aux[0] - t_start_sim) / T),
                events=int(n_ev), cpu_s=float(cpu_used),
                n_exits=n_exit,
                exits=exits.tolist(), occ=occ.tolist(), occ_armed=occ_armed.tolist(),
                occ_total=float(occ.sum()),
                exit_phases=elog[:min(n_exit, exit_log_cap)].tolist(),
                final_counts=n.tolist(), seed=int(seed))


def _job(args):
    return run_cell(*args)
