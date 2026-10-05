"""Run the predeclared experiment and write results/results.json and results/tables.md.

Usage:  PYTHONPATH=src python3 -m phys2_order.run
"""

import json
import os
import sys
import time

from .dynamics import ARMS, SYNC
from .relabel import GROUPS, LABELED, POSITIONAL, apply_buggy_reversal
from .stages import (
    MODES, STAGE1_CADENCES, STAGE2_CADENCES, run_stage, sequential_orders,
)
from .words import check_anchors

ARM_NAMES = [a.name for a in ARMS]
REFRACTORY = [a for a in ARM_NAMES if a != "CONTROL"]
PRECHECK = {"(MASK,PAUSE)": 40, "(PAUSE,PAUSE)": 0, "CONTROL": 0}
SOURCE_DOC_MP = 55


def sched_name(s):
    return "SYNC" if s == SYNC else "SEQ" + "".join("ABC"[i] for i in s)


def key(r):
    return (r["word"], r["phases"])


def aggregate(rows, cadences):
    """counts[sched][arm][group][mode][n] = [count, total]"""
    out = {}
    for r in rows:
        s = sched_name(r["schedule"])
        for (g, m), v in r["ineq"].items():
            cell = (out.setdefault(s, {}).setdefault(r["arm"], {})
                    .setdefault(g, {}).setdefault(m, {})
                    .setdefault(r["n"], [0, 0]))
            cell[0] += int(v)
            cell[1] += 1
    return out


def index(rows):
    """idx[sched][arm][(word, phases)] = row"""
    idx = {}
    for r in rows:
        idx.setdefault(sched_name(r["schedule"]), {}).setdefault(r["arm"], {})[key(r)] = r
    return idx


def differential(idx, cadences):
    """Configurations inequivalent under an arm but not under CONTROL, and vice versa."""
    out = {}
    for s, by_arm in idx.items():
        ctl = by_arm["CONTROL"]
        for arm, rs in by_arm.items():
            for g in GROUPS:
                for m in MODES:
                    for n in cadences:
                        a_only = c_only = both = tot = 0
                        for k, r in rs.items():
                            if r["n"] != n:
                                continue
                            tot += 1
                            x = r["ineq"][(g, m)]
                            y = ctl[k]["ineq"][(g, m)]
                            a_only += x and not y
                            c_only += y and not x
                            both += x and y
                        (out.setdefault(s, {}).setdefault(arm, {}).setdefault(g, {})
                         .setdefault(m, {}))[n] = {"arm_only": a_only,
                                                   "control_only": c_only,
                                                   "both": both, "total": tot}
    return out


def kinds(rows):
    """Split inequivalent configurations into 'fired sets differ' and
    'same fired set, terminal state differs' (labeled mode, G1)."""
    out = {}
    for r in rows:
        if not r["ineq"][("G1", LABELED)]:
            continue
        s = sched_name(r["schedule"])
        nf1, nf2 = sum(r["out1"].fired), sum(r["out2"].fired)
        kind = "fired_count_differs" if nf1 != nf2 else "same_count_terminal_or_labels_differ"
        c = out.setdefault(s, {}).setdefault(r["arm"], {}).setdefault(r["n"], {})
        c[kind] = c.get(kind, 0) + 1
    return out


def flips(idx, ref="SYNC"):
    """Configuration-level verdict flips of each sequential order relative to SYNC."""
    out = {}
    base = idx[ref]
    for s, by_arm in idx.items():
        if s == ref:
            continue
        for arm, rs in by_arm.items():
            for g in GROUPS:
                for m in MODES:
                    up = down = 0
                    for k, r in rs.items():
                        x = base[arm][k]["ineq"][(g, m)]
                        y = r["ineq"][(g, m)]
                        up += y and not x
                        down += x and not y
                    (out.setdefault(s, {}).setdefault(arm, {}).setdefault(g, {}))[m] = {
                        "became_inequivalent": up, "became_equivalent": down}
    return out


def total(counts, sched, arm, g, m, ns):
    c = t = 0
    for n in ns:
        a, b = counts[sched][arm][g][m][n]
        c += a
        t += b
    return c, t


def main(outdir="results"):
    t0 = time.time()
    anchors = check_anchors()
    print("anchors OK", file=sys.stderr)

    s1 = run_stage(1, schedules=(SYNC,) + sequential_orders(2))
    print("stage 1 done %.0fs" % (time.time() - t0), file=sys.stderr)
    s2 = run_stage(2, schedules=(SYNC,) + sequential_orders(3))
    print("stage 2 done %.0fs" % (time.time() - t0), file=sys.stderr)

    c1, c2 = aggregate(s1, STAGE1_CADENCES), aggregate(s2, STAGE2_CADENCES)
    i1, i2 = index(s1), index(s2)

    # informational: does a buggy reversal change any SYNC count?
    b1 = aggregate(run_stage(1, apply_fn=apply_buggy_reversal, groups=("G2",)),
                   STAGE1_CADENCES)
    b2 = aggregate(run_stage(2, apply_fn=apply_buggy_reversal, groups=("G2",)),
                   STAGE2_CADENCES)

    def changed(good, bad):
        diffs = []
        for arm in ARM_NAMES:
            for m in MODES:
                for n, v in bad["SYNC"][arm]["G2"][m].items():
                    if v != good["SYNC"][arm]["G2"][m][n]:
                        diffs.append([arm, m, n, good["SYNC"][arm]["G2"][m][n], v])
        return diffs

    # minimal cadence with a handed configuration (Stage 2)
    minimal = {}
    for s in c2:
        for arm in ARM_NAMES:
            for g in GROUPS:
                for m in MODES:
                    ns = [n for n in STAGE2_CADENCES if c2[s][arm][g][m][n][0] > 0]
                    minimal.setdefault(s, {}).setdefault(arm, {}).setdefault(g, {})[m] = (
                        min(ns) if ns else None)
    d2 = differential(i2, STAGE2_CADENCES)
    minimal_diff = {}
    for s in d2:
        for arm in ARM_NAMES:
            for g in GROUPS:
                for m in MODES:
                    ns = [n for n in STAGE2_CADENCES if d2[s][arm][g][m][n]["arm_only"] > 0]
                    minimal_diff.setdefault(s, {}).setdefault(arm, {}).setdefault(g, {})[m] = (
                        min(ns) if ns else None)

    precheck = {}
    for arm in ARM_NAMES:
        for m in MODES:
            precheck.setdefault(arm, {})[m] = total(c1, "SYNC", arm, "G1", m, (3, 4, 5))

    # unseen region: everything except Stage 1 / SYNC / G1 / n=3..5 / labeled+positional
    unseen = {}
    for arm in ARM_NAMES:
        c = t = 0
        for st, cc, cads in ((1, c1, STAGE1_CADENCES), (2, c2, STAGE2_CADENCES)):
            for s in cc:
                for g in GROUPS:
                    for n in cads:
                        if st == 1 and s == "SYNC" and g == "G1" and n <= 5:
                            continue
                        a, b = cc[s][arm][g][LABELED][n]
                        c += a
                        t += b
        unseen[arm] = [c, t]

    # Stage 3 verdicts: zero / nonzero summed over cadences, per schedule
    verdicts = {}
    for label, cc, cads in (("stage1", c1, STAGE1_CADENCES), ("stage2", c2, STAGE2_CADENCES)):
        for arm in ARM_NAMES:
            for g in GROUPS:
                for m in MODES:
                    v = {s: total(cc, s, arm, g, m, cads)[0] > 0 for s in cc}
                    verdicts.setdefault(label, {}).setdefault(arm, {}).setdefault(g, {})[m] = {
                        "by_schedule": v,
                        "schedule_dependent": len(set(v.values())) > 1}
    for arm in ARM_NAMES:
        for g in GROUPS:
            for m in MODES:
                v = {s: sum(d2[s][arm][g][m][n]["arm_only"] for n in STAGE2_CADENCES) > 0
                     for s in d2}
                verdicts.setdefault("stage2_S2DIFF", {}).setdefault(arm, {}).setdefault(g, {})[m] = {
                    "by_schedule": v,
                    "schedule_dependent": len(set(v.values())) > 1}

    res = {
        "status": "SANDBOX/DRAFT",
        "stage3_verdicts": verdicts,
        "anchors": anchors,
        "stage1_counts": c1,
        "stage2_counts": c2,
        "stage2_differential_vs_control": d2,
        "stage2_minimal_cadence": minimal,
        "stage2_minimal_cadence_arm_only": minimal_diff,
        "stage1_kinds": kinds(s1),
        "stage2_kinds": kinds(s2),
        "stage1_flips_vs_sync": flips(i1),
        "stage2_flips_vs_sync": flips(i2),
        "precheck_region": precheck,
        "unseen_region_labeled": unseen,
        "buggy_reversal_count_changes": {"stage1": changed(c1, b1),
                                         "stage2": changed(c2, b2)},
        "stage1_inequivalent_configs_SYNC_G1_labeled": {
            arm: sorted("%s d=%d" % (r["word"], r["phases"][1]) for r in s1
                        if r["arm"] == arm and r["schedule"] == SYNC
                        and r["ineq"][("G1", LABELED)] and r["n"] <= 5)
            for arm in ARM_NAMES},
        "runtime_seconds": round(time.time() - t0, 1),
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)
    with open(os.path.join(outdir, "tables.md"), "w") as f:
        f.write(render(res))
    print("done %.0fs" % (time.time() - t0), file=sys.stderr)
    return res


def _cell(v):
    c, t = v
    return "%d/%d (%.1f%%)" % (c, t, 100.0 * c / t) if t else "-"


def render(res):
    L = ["# Tables (generated by phys2_order.run) — SANDBOX/DRAFT", ""]
    for stage, key_, cads in ((1, "stage1_counts", STAGE1_CADENCES),
                              (2, "stage2_counts", STAGE2_CADENCES)):
        counts = res[key_]
        word = "order-inequivalent" if stage == 1 else "handed"
        for m in MODES:
            for s in counts:
                L.append("## Stage %d, %s, %s signature: %s configurations"
                         % (stage, s, m, word))
                L.append("")
                L.append("| arm | group | " + " | ".join("n=%d" % n for n in cads)
                         + " | all |")
                L.append("|---|---|" + "---|" * (len(cads) + 1))
                for arm in ARM_NAMES:
                    for g in GROUPS:
                        row = [_cell(counts[s][arm][g][m][n]) for n in cads]
                        row.append(_cell(total(counts, s, arm, g, m, cads)))
                        L.append("| %s | %s | %s |" % (arm, g, " | ".join(row)))
                L.append("")
    L.append("## Stage 2 differential vs CONTROL (labeled): arm-only / control-only / both")
    L.append("")
    d2 = res["stage2_differential_vs_control"]
    for s in d2:
        L.append("### %s" % s)
        L.append("")
        L.append("| arm | group | " + " | ".join("n=%d" % n for n in STAGE2_CADENCES) + " |")
        L.append("|---|---|" + "---|" * len(STAGE2_CADENCES))
        for arm in REFRACTORY:
            for g in GROUPS:
                cells = []
                for n in STAGE2_CADENCES:
                    v = d2[s][arm][g][LABELED][n]
                    cells.append("%d / %d / %d" % (v["arm_only"], v["control_only"], v["both"]))
                L.append("| %s | %s | %s |" % (arm, g, " | ".join(cells)))
        L.append("")
    L.append("## Stage 3 verdicts (nonzero summed over cadences), labeled / positional")
    L.append("")
    for label, by_arm in res["stage3_verdicts"].items():
        scheds = sorted(by_arm["CONTROL"]["G1"][LABELED]["by_schedule"])
        scheds.remove("SYNC")
        scheds = ["SYNC"] + scheds
        L.append("### %s" % label)
        L.append("")
        L.append("| arm | group | " + " | ".join(scheds) + " | schedule-dependent |")
        L.append("|---|---|" + "---|" * (len(scheds) + 1))
        for arm in ARM_NAMES:
            for g in GROUPS:
                cells = []
                for s in scheds:
                    v = by_arm[arm][g]
                    cells.append("%s / %s" % (
                        "nonzero" if v[LABELED]["by_schedule"][s] else "zero",
                        "nonzero" if v[POSITIONAL]["by_schedule"][s] else "zero"))
                dep = "%s / %s" % ("YES" if by_arm[arm][g][LABELED]["schedule_dependent"] else "no",
                                   "YES" if by_arm[arm][g][POSITIONAL]["schedule_dependent"] else "no")
                L.append("| %s | %s | %s | %s |" % (arm, g, " | ".join(cells), dep))
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
