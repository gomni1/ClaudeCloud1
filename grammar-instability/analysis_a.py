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
    counts = collections.defaultdict(lambda: collections.Counter())
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
                c = counts[key]
                c["draws"] += 1
                c["cpu"] += r["cpu"]
                c["balance"] += r["n_balance"]
                c["periodic"] += r["n_periodic"]
                c["unresolved"] += r["n_unresolved"]
                c["draws_with_periodic"] += r["n_periodic"] > 0
                c["draws_with_unresolved"] += r["n_unresolved"] > 0
                c["draws_all_unresolved"] += r["n_unresolved"] == len(r["kinds"])
                c["multistable"] += r["n_stable"] > 1
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
        if not s2:  # M2 stopped under the H-cyc stop rule before writing its summary
            A["M2"] = dict(draws=sum(c["draws"] for c in counts.values()), counts={k: dict(v) for k, v in counts.items()},
                           stop="H-cyc stop rule (SPEC 7): periodic hit at draw 12051 verified by M4")
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
    if m3:
        # M3 oscillatory hits: is the leading 'complex' eigenvalue at (D, s*) a genuine pair, or two real
        # eigenvalues at their collision (|Im| at roundoff)?  Uses the D and s* M4 would use.
        from ginst import m2 as _m2, model as _model
        rows = []
        for fl in m3["flagged"]:
            det, job = fl["detail"], fl["job"]
            if not det["osc_hit"]:
                continue
            src = max(("random", "two_class"), key=lambda nm: det[nm]["osc"]["Gamma"])
            r = det[src]["osc"]
            s_star = r["s_ref"] if ("s_ref" in r and r["Gamma"] > r["Gamma_grid"]) else r["s"]
            d = dict(job)
            d.setdefault("law", "TH")
            J = _model.J_np(np.array(job["b"]), _m2.par_of(d))
            ev = np.linalg.eigvals(J - s_star * np.diag(r["D"]))
            c = ev[np.abs(ev.imag) > 1e-9 * np.abs(ev).max()]
            lead = c[np.argmax(c.real)] if len(c) else None
            rows.append(dict(i=fl["i"], level=fl["level"], den=fl["den"], is_P=fl["is_P"], Gamma=r["Gamma"],
                             im_over_re=None if lead is None else float(abs(lead.imag) / max(abs(lead.real), 1e-300)),
                             stat_hit_too=bool(det["stat_hit"])))
        A["M3_osc_hits"] = rows
        A["M3_osc_hits_genuine_pair"] = sum(1 for r in rows if r["im_over_re"] is not None and r["im_over_re"] > 1e-3)
        A["M3_osc_hits_at_P_balances"] = sum(1 for r in rows if r["is_P"])
    m4c = load("m4_cycle.json") or {}
    m4l = load("m4_lattice.json") or {}
    m4 = dict(cycle_verified=m4c.get("cycle_verified"), stationary_verified=m4l.get("stationary_verified"),
              oscillatory_verified=m4l.get("oscillatory_verified"))
    A["M4"] = dict(m4, cycle_hits=[dict(i=h["draw"]["i"], level=h["draw"]["level"], den=h["draw"]["den"],
                                        **{k: h["verification"][k] for k in ("periods", "agree", "nontrivial_moduli",
                                                                             "verified")}) for h in m4c.get("hits", [])],
                   lattice=m4l.get("runs"))
    # statuses (SPEC §7)
    pf = A["planted"]
    cov_ok = bool(s2) and not s2.get("budget_stop", True)
    A["H-cyc"] = dict(
        status="killed" if m4.get("cycle_verified") else
        ("underdetermined" if not (cov_ok and pf.get("pfa1") and pf.get("pfa2")) else "survived"),
        periodic_end_states=sum(v["periodic"] for v in A["M2"]["counts"].values()),
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
