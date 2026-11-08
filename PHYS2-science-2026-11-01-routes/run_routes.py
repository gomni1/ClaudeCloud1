"""Routes test production runs (SPEC §4). Run AFTER the SPEC freeze.

Omega in {8,10,12,16} x direction in {up,down}; per cell, 3000 non-passing runs
or 5 CPU-minutes, whichever comes first. Fresh seed base 5000000.
"""
import os, sys, json, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from driver_routes import _job, run_cell, SIZES, DIRS, BUDGET, MIN_NONPASSING, cell_seed


def main():
    run_cell("up", 8, budget_cpu_s=0.1, min_nonpassing=1)      # warm the JIT cache
    jobs = [(d, Om, BUDGET, MIN_NONPASSING, cell_seed(d, Om)) for d in DIRS for Om in SIZES]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, jobs))
    json.dump(res, open(os.path.join(HERE, "production_routes.json"), "w"))
    # raw delta arrays, stored losslessly as integer lattice levels
    np.savez_compressed(
        os.path.join(HERE, "evidence_routes.npz"),
        **{f"{r['direction']}_{r['Omega']}_levels": np.array(r["levels"], np.int32)
           for r in res},
        **{f"{r['direction']}_{r['Omega']}_visitD": np.array(r["visitD"], np.int8)
           for r in res},
        Omegas=np.array(SIZES), seed_base=np.array([5_000_000]))
    print("wall %.1fs  cpu %.1fs" % (time.time() - t0, sum(r["cpu_s"] for r in res)))
    for r in res:
        print("%-4s Om=%2d runs=%6d nonpass=%6d capped=%d passD=%.4f cpu=%6.1f budget_hit=%s"
              % (r["direction"], r["Omega"], r["n_runs"], r["n_nonpassing"],
                 r["n_capped"], r["passage_fraction"], r["cpu_s"], r["budget_hit"]))
    return res


if __name__ == "__main__":
    main()
