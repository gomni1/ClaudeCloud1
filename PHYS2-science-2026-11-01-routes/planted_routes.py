"""Routes test planted checks P1, P2, P3 (SPEC §8).

All must pass before the results count.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyse_routes import mwu
from sim_routes import run_one_record, scan_states, seed_rng
from driver_routes import K, TOL, BALANCE, TARGETV, SEED_BASE

N_REP = 50
N_SAMP = 3000


def p1(seed=11):
    """Known small shift on the 1/8 lattice: the test must detect it."""
    rng = np.random.default_rng(SEED_BASE + seed)
    ps = []
    for _ in range(N_REP):
        up = rng.binomial(8, 0.35, N_SAMP) / 8.0
        dn = rng.binomial(8, 0.38, N_SAMP) / 8.0
        ps.append(mwu(up, dn)[1])
    ps = np.array(ps)
    n_ok = int((ps < 0.05).sum())
    return dict(check="P1", n_rep=N_REP, n_detect=n_ok, frac=n_ok / N_REP,
                median_p=float(np.median(ps)), passed=bool(n_ok >= 0.9 * N_REP))


def p2(seed=22):
    """Identical lattice distributions with heavy ties: the test must not fire."""
    rng = np.random.default_rng(SEED_BASE + seed)
    ps = []
    for _ in range(N_REP):
        up = rng.binomial(8, 0.35, N_SAMP) / 8.0
        dn = rng.binomial(8, 0.35, N_SAMP) / 8.0
        ps.append(mwu(up, dn)[1])
    ps = np.array(ps)
    n_ok = int((ps >= 0.05).sum())
    return dict(check="P2", n_rep=N_REP, n_nonsig=n_ok, frac=n_ok / N_REP,
                median_p=float(np.median(ps)), passed=bool(n_ok >= 0.9 * N_REP))


def p3(n_runs=200, Omega=10, cap=400_000, seed=90000):
    """Recompute delta and the passage flag from stored paths on real runs."""
    seed_rng(np.int64(SEED_BASE + seed))
    recC = np.empty(cap, np.int64); recL = np.empty(cap, np.int64)
    bad_delta = bad_flag = 0
    used = 0
    n_D = 0
    while used < n_runs:
        d = "up" if used % 2 == 0 else "down"
        c, v, l, p = BALANCE[d]
        dd, vv, ns, ok = run_one_record(int(c * Omega), int(v * Omega), int(l * Omega),
                                        int(p * Omega), float(Omega), K, TARGETV[d],
                                        TOL, 10_000_000, recC, recL)
        if not ok:
            continue
        used += 1
        n_D += int(vv)
        d2, v2 = scan_states(recC[:ns], recL[:ns], float(Omega))
        bad_delta += int(d2 != dd)
        bad_flag += int(v2 != vv)
    return dict(check="P3", n_runs=used, delta_mismatches=bad_delta,
                flag_mismatches=bad_flag, n_visited_D=n_D,
                passed=bool(bad_delta == 0 and bad_flag == 0 and used == n_runs))


def main():
    out = [p1(), p2(), p3()]
    json.dump(out, open(os.path.join(HERE, "planted_routes.json"), "w"), indent=1)
    print("P1 %s  detected in %d/%d replicates (median p = %.2e)" %
          ("PASS" if out[0]["passed"] else "FAIL", out[0]["n_detect"], N_REP, out[0]["median_p"]))
    print("P2 %s  p >= 0.05 in %d/%d replicates (median p = %.3f)" %
          ("PASS" if out[1]["passed"] else "FAIL", out[1]["n_nonsig"], N_REP, out[1]["median_p"]))
    print("P3 %s  %d runs rescanned, %d delta and %d flag mismatches" %
          ("PASS" if out[2]["passed"] else "FAIL", out[2]["n_runs"],
           out[2]["delta_mismatches"], out[2]["flag_mismatches"]))
    print("ALL PLANTED PASS:", all(r["passed"] for r in out))
    return out


if __name__ == "__main__":
    main()
