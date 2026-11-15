"""Part A production grid (SPEC §7, §8). Run AFTER the SPEC freeze.

Omega in {50,100,200,400,800}; per cell: 2000 exits or 2 CPU-minutes.
R = 0.75 for both models (SPEC §9, pilot-selected).
Cells are independent processes; the CPU budget is measured inside each.
"""
import os, sys, json, time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from driver_a import _job, run_cell

R_SEL = {"A1": 0.75, "A2": 0.75}
SIZES = [50, 100, 200, 400, 800]
BUDGET = 120.0
MAX_EXITS = 2000


def main():
    # warm the numba on-disk cache once so JIT time is not charged to any cell
    run_cell("A1", 50, 0.75, budget_cpu_s=0.2, max_exits=1, seed=1)
    jobs = []
    for mi, nm in enumerate(("A1", "A2")):
        for si, Om in enumerate(SIZES):
            jobs.append((nm, Om, R_SEL[nm], BUDGET, MAX_EXITS, 20000 + 100 * mi + si))
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=10) as ex:
        res = list(ex.map(_job, jobs))
    out = os.path.join(HERE, "production_raw.json")
    json.dump(res, open(out, "w"))
    print("wall %.1fs cpu %.1fs -> %s" % (time.time() - t0, sum(r["cpu_s"] for r in res), out))
    for r in res:
        print("%s Om=%4d exits=%5d periods=%9.1f occ=%10.2f cpu=%6.1f" %
              (r["model"], r["Omega"], r["n_exits"], r["periods"], r["occ_total"], r["cpu_s"]))


if __name__ == "__main__":
    main()
