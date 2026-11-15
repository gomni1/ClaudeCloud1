"""Part B production runs (SPEC §4). Run AFTER the SPEC freeze.

Omega in {8,10,12} x direction in {up, down}; per cell at least 2000 completed
switching runs, generation continuing to a 3 CPU-minute budget.
"""
import os, sys, json, time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from driver_b import _job, run_cell

SIZES = [8, 10, 12]
DIRS = ["up", "down"]
BUDGET = 180.0


def main():
    run_cell("up", 8, budget_cpu_s=0.1, min_runs=2, seed=1)      # warm the JIT cache
    jobs = [(d, Om, BUDGET, 2000, 31000 + 100 * di + si)
            for di, d in enumerate(DIRS) for si, Om in enumerate(SIZES)]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(_job, jobs))
    json.dump(res, open(os.path.join(HERE, "production_B.json"), "w"))
    print("wall %.1fs cpu %.1fs" % (time.time() - t0, sum(r["cpu_s"] for r in res)))
    for r in res:
        print("%-4s Om=%2d runs=%7d capped=%d passD=%.4f med_delta_nonpass=%.4f n_nonpass=%7d" %
              (r["direction"], r["Omega"], r["n_runs"], r["n_capped"],
               r["passage_fraction"], r["median_delta_nonpassing"], r["n_nonpassing"]))


if __name__ == "__main__":
    main()
