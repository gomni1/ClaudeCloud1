"""Part B planted checks P1, P2 and the end-to-end consistency check (SPEC §7)."""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim_b import scan_states, run_one_record, seed_rng
from driver_b import K, TOL, BALANCE, TARGETV

# Scripted paths: (nC sequence, nL sequence, Omega, expected delta, expected visitD)
SCRIPTS = [
    # plain descent to a positive floor of 2 counts, Omega = 8 -> delta = 0.25
    ([8, 6, 4, 2, 3, 8], [8, 5, 2, 0, 1, 8], 8, None, 0),
    # touches dissolution exactly once
    ([8, 4, 0, 1, 8], [8, 3, 0, 2, 8], 8, 0.0, 1),
    # starts already in D
    ([0, 1, 5, 10], [0, 1, 3, 10], 10, 0.0, 1),
    # floor of 1 count at Omega = 10 -> delta = 0.1
    ([10, 5, 1, 2, 10], [10, 4, 0, 1, 10], 10, 0.1, 0),
    # monotone, minimum at the end state
    ([12, 10, 8, 6], [12, 9, 7, 3], 12, 0.75, 0),
    # minimum of 3 counts at Omega = 12 -> delta = 0.25
    ([12, 2, 1, 12], [12, 2, 2, 12], 12, 0.25, 0),
]


def expected(script):
    nC, nL, Om, dec, _ = script
    s = [a + b for a, b in zip(nC, nL)]
    return min(s) / Om, int(any(v == 0 for v in s))


def p1_p2():
    rows = []
    for sc in SCRIPTS:
        nC = np.array(sc[0], np.int64); nL = np.array(sc[1], np.int64); Om = float(sc[2])
        d_got, v_got = scan_states(nC, nL, Om)
        d_exp, v_exp = expected(sc)
        if sc[3] is not None:
            assert abs(d_exp - sc[3]) < 1e-12, "script table disagrees with itself"
        assert v_exp == sc[4], "script table disagrees with itself"
        rows.append(dict(Omega=sc[2], delta_expected=d_exp, delta_got=float(d_got),
                         visitD_expected=v_exp, visitD_got=int(v_got),
                         delta_exact=bool(d_got == d_exp), visitD_exact=bool(v_got == v_exp)))
    d_ok = all(r["delta_exact"] for r in rows)
    v_ok = all(r["visitD_exact"] for r in rows)

    # P1 also requires the *median* over a scripted set to be recovered exactly
    deltas_exp = np.array([r["delta_expected"] for r in rows])
    deltas_got = np.array([r["delta_got"] for r in rows])
    med_ok = bool(np.median(deltas_exp) == np.median(deltas_got))

    # P2 also requires exact passage counts over the scripted set
    cnt_exp = int(sum(r["visitD_expected"] for r in rows))
    cnt_got = int(sum(r["visitD_got"] for r in rows))

    p1 = dict(check="P1", n_scripts=len(rows), all_deltas_exact=d_ok,
              median_expected=float(np.median(deltas_exp)),
              median_got=float(np.median(deltas_got)), median_exact=med_ok,
              passed=bool(d_ok and med_ok), rows=rows)
    p2 = dict(check="P2", n_scripts=len(rows), all_flags_exact=v_ok,
              passage_count_expected=cnt_exp, passage_count_got=cnt_got,
              passed=bool(v_ok and cnt_exp == cnt_got))
    return p1, p2


def p3_consistency(n_runs=400, Omega=10, cap=400_000, seed=4242):
    """End-to-end: streaming delta/flag inside the simulation loop must equal a
    rescan of the recorded path."""
    seed_rng(np.int64(seed))
    recC = np.empty(cap, np.int64); recL = np.empty(cap, np.int64)
    bad = 0; n_used = 0; n_D = 0
    for i in range(n_runs):
        d = "up" if i % 2 == 0 else "down"
        c, v, l, p = BALANCE[d]
        dd, vv, ns, ok = run_one_record(int(c * Omega), int(v * Omega), int(l * Omega),
                                        int(p * Omega), float(Omega), K, TARGETV[d],
                                        TOL, 10_000_000, recC, recL)
        if not ok:
            continue
        n_used += 1
        d2, v2 = scan_states(recC[:ns], recL[:ns], float(Omega))
        if (d2 != dd) or (v2 != vv):
            bad += 1
        n_D += int(vv)
    return dict(check="E2E", n_runs_used=n_used, mismatches=bad, n_visited_D=n_D,
                passed=bool(bad == 0 and n_used > 0))


def main():
    p1, p2 = p1_p2()
    e2e = p3_consistency()
    out = [p1, p2, e2e]
    json.dump(out, open(os.path.join(HERE, "planted_B.json"), "w"), indent=1)
    print("P1", "PASS" if p1["passed"] else "FAIL",
          "medians %.6f vs %.6f, all deltas exact: %s" %
          (p1["median_expected"], p1["median_got"], p1["all_deltas_exact"]))
    print("P2", "PASS" if p2["passed"] else "FAIL",
          "passage counts %d vs %d, all flags exact: %s" %
          (p2["passage_count_expected"], p2["passage_count_got"], p2["all_flags_exact"]))
    print("E2E", "PASS" if e2e["passed"] else "FAIL",
          "%d runs rescanned, %d mismatches, %d visited D" %
          (e2e["n_runs_used"], e2e["mismatches"], e2e["n_visited_D"]))
    print("ALL PLANTED PASS:", all(r["passed"] for r in out))
    return out


if __name__ == "__main__":
    main()
