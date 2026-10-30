"""Task A analysis: coverage, outcomes and claim statuses (SPEC §7) -> evidence/analysis.json and stdout tables."""
import collections
import gzip
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")


def load(name):
    p = os.path.join(EV, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    A = {}
    pl = load("planted.json")
    A["planted"] = {k: v.get("pass_") for k, v in (pl or {}).items()}
    m01 = load("m0_m1.json")
    if m01:
        A["M0"] = {k: v.get("holds") for k, v in m01["M0"].items()}
        A["M1"] = dict(MA_open_all_positive=m01["M1"]["MA_open"]["all_positive"],
                       TH_open_cv_all_positive_for_h_pos=m01["M1"]["TH_open_cv"]["all_positive_for_h_positive"])
    s2 = load("m2_summary.json")
    A["M2"] = s2 and {k: v for k, v in s2.items() if k != "periodic_draws"}
    notes = collections.Counter()
    var_notes = collections.defaultdict(collections.Counter)
    unresolved_draws = collections.Counter()
    nbal = collections.Counter()
    n_unstable_only = collections.Counter()
    path = os.path.join(EV, "m2_draws.jsonl.gz")
    if os.path.exists(path):
        with gzip.open(path, "rt") as f:
            for line in f:
                r = json.loads(line)
                key = "%s-%s" % (r["level"], r["den"])
                nbal[(key, r["n_bal"], r["n_stable"])] += 1
                if r["n_stable"] == 0:
                    n_unstable_only[key] += 1
                for run in r.get("runs", []):
                    c = run["class"]
                    if c["kind"] == "unresolved":
                        note = c.get("note") or c.get("reason") or "section stage"
                        note = note.split(":")[0]
                        notes[note] += 1
                        var_notes[key][note] += 1
        A["M2_unresolved_notes"] = dict(notes)
        A["M2_unresolved_notes_by_variant"] = {k: dict(v) for k, v in var_notes.items()}
        A["M2_balance_structure"] = {"%s n_bal=%d n_stable=%d" % k: v for k, v in sorted(nbal.items())}
        A["M2_no_stable_balance"] = dict(n_unstable_only)
    ad = load("adaptive.json")
    if ad:
        A["adaptive"] = dict(best_f=[r["f_best"] for r in ad["results"]], nfev=sum(r["nfev"] for r in ad["results"]),
                             follow_up_periodic=sum(f["n_periodic"] for f in ad["follow_up"]),
                             follow_up_n=len(ad["follow_up"]))
    m3 = load("m3_summary.json")
    if m3:
        A["M3"] = dict(n_jobs=m3["n_jobs"], n_done=m3["n_done"], cpu=m3["cpu"], summary=m3["summary"],
                       n_flagged=len(m3["flagged"]),
                       flagged=[{k: v for k, v in f.items() if k in ("src", "i", "level", "den", "is_P", "failing",
                                                                       "osc_hit", "stat_hit", "Gamma_random",
                                                                       "Gamma_two", "scale")} for f in m3["flagged"]])
    m4 = load("m4.json")
    A["M4"] = m4
    # statuses (SPEC §7)
    cyc_hits = (s2 or {}).get("periodic_draws", []) if s2 else []
    pf = A["planted"]
    cov_ok = bool(s2) and not s2.get("budget_stop", True)
    A["H-cyc"] = dict(
        status="killed" if (m4 and m4.get("cycle_verified")) else
        ("underdetermined" if not (cov_ok and pf.get("pfa1") and pf.get("pfa2")) else "survived"),
        periodic_end_states=sum(v["periodic"] for v in (s2 or {}).get("counts", {}).values()) if s2 else None,
        coverage_complete=cov_ok)
    stat_hits = sum(v["stat_hits"] for v in (m3 or {}).get("summary", {}).values()) if m3 else None
    osc_hits = sum(v["osc_hits"] for v in (m3 or {}).get("summary", {}).values()) if m3 else None
    m3_complete = bool(m3) and m3["n_done"] == m3["n_jobs"]
    A["H-mob-stat"] = dict(
        status="killed" if (m4 and m4.get("stationary_verified")) or (A.get("M1") and not A["M1"]["MA_open_all_positive"])
        else ("underdetermined" if not (m3_complete and pf.get("pfa3")) else "survived"), stat_hits=stat_hits)
    A["H-mob-osc"] = dict(status="killed" if (m4 and m4.get("oscillatory_verified")) else
                          ("underdetermined" if not (m3_complete and pf.get("pfa4")) else "survived"), osc_hits=osc_hits)
    json.dump(A, open(os.path.join(EV, "analysis.json"), "w"), indent=1, default=str)
    return A


if __name__ == "__main__":
    A = main()
    print(json.dumps(A, indent=1, default=str)[:6000])
