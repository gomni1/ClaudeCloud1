"""Assemble RESULTS.md tables from evidence/ (no simulation).  Usage: python make_results.py > tables.md"""
import gzip
import json
import os
from collections import defaultdict

EV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
PR4 = os.path.join(os.path.dirname(EV), "..", "grammar-instability", "evidence", "m2_draws.jsonl.gz")


def jl(fn):
    p = os.path.join(EV, fn)
    if os.path.exists(p):
        for l in open(p):
            yield json.loads(l)
    p += ".gz"
    if os.path.exists(p):
        for l in gzip.open(p, "rt"):
            yield json.loads(l)


def k1():
    rows = defaultdict(lambda: dict(n=0, cap=0, unres=0, hits=0, cycles=[]))
    for r in jl("k1_records.jsonl"):
        key = (r["sub"], r["level"])
        R = rows[key]
        R["n"] += 1
        R["cap"] += bool(r.get("capped"))
        R["unres"] += bool(r.get("n_unresolved"))
        ver = [v for v in r.get("verify", []) if v["verified"]]
        if ver:
            v = ver[0]
            R["hits"] += 1
            R["cycles"].append(dict(i=r["i"], m=r["m"], kr=r["kr"], kc=r["kc"], span=r["span"],
                                    period=v["periods"]["Radau"]["period"], C=v["C_range"],
                                    n_ver=len(ver), n_per=r["n_periodic"], moduli=v["nontrivial"]))
    k1c = defaultdict(lambda: dict(draws=0, cap=0, starts=0, kinds=defaultdict(int), hits=[]))
    for r in jl("k1c_records.jsonl"):
        key = (r.get("src"), r["level"])
        R = k1c[key]
        R["draws"] += 1
        R["cap"] += bool(r.get("capped"))
        for it in r.get("second", []):
            R["starts"] += 1
            k = it["second"]["kind"]
            R["kinds"][k] += 1
            if it.get("verify", {}).get("verified"):
                R["hits"].append(dict(i=r["i"], m=r["m"], kr=r["kr"], kc=r["kc"], span=r["span"],
                                      period=it["verify"]["periods"]["Radau"]["period"], C=it["verify"]["C_range"]))
    pr4 = defaultdict(lambda: dict(n=0, unres=0, hits=0))
    with gzip.open(PR4, "rt") as f:
        for l in f:
            r = json.loads(l)
            if r["den"] != "tot":
                continue
            R = pr4[r["level"]]
            R["n"] += 1
            R["unres"] += bool(r["n_unresolved"])
            R["hits"] += bool(r["n_periodic"])
    return rows, k1c, pr4


def main():
    rows, k1c, pr4 = k1()
    print("### K1 table (per sub-run and level)\n")
    print("| Sub-run | Level | Draws run | Unresolved (any start) | CPU-capped | Verified cycles | Fraction | 95% bound if none |")
    print("|---|---|---|---|---|---|---|---|")
    for (s, lv), R in sorted(rows.items()):
        frac = R["hits"] / R["n"]
        print("| %s | %s | %d | %d | %d | %d | %.2e | %s |" % (s, lv, R["n"], R["unres"], R["cap"], R["hits"], frac,
                                                              "%.1e" % (3 / R["n"]) if not R["hits"] else "-"))
    print("\nCycles found:\n")
    print("| Sub-run | Draw | Level | m | kr | kc | Span | Period | C range | starts periodic / verified | nontrivial moduli |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for (s, lv), R in sorted(rows.items()):
        for c in R["cycles"]:
            print("| %s | %d | %s | %d | %d | %d | %.2f | %.4f | [%.3f, %.3f] | %d / %d | %s |" % (
                s, c["i"], lv, c["m"], c["kr"], c["kc"], c["span"], c["period"], c["C"][0], c["C"][1], c["n_per"],
                c["n_ver"], ", ".join("%.1e" % x for x in c["moduli"])))
    print("\n### Census (all-neighbours variants, PR 4 draws 0-41099 + K1a draws 41100-99999)\n")
    print("| Level | PR 4 draws | PR 4 cycles | K1a draws | K1a cycles | Total draws | Total cycles | Fraction |")
    print("|---|---|---|---|---|---|---|---|")
    for lv in ("closed", "open"):
        a = rows.get(("K1a", lv), dict(n=0, hits=0))
        n, h = pr4[lv]["n"] + a["n"], pr4[lv]["hits"] + a["hits"]
        print("| %s | %d | %d | %d | %d | %d | %d | %.1e |" % (lv, pr4[lv]["n"], pr4[lv]["hits"], a["n"], a["hits"], n, h,
                                                               h / n))
    print("\n### K1c second pass\n")
    print("| Source | Level | Draws processed | CPU-capped draws | Starts re-integrated | Outcome of the second pass | Verified cycles |")
    print("|---|---|---|---|---|---|---|")
    for (s, lv), R in sorted(k1c.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        print("| %s | %s | %d | %d | %d | %s | %s |" % (s, lv, R["draws"], R["cap"], R["starts"],
                                                       ", ".join("%s %d" % kv for kv in sorted(R["kinds"].items())),
                                                       "; ".join("draw %d (m=%d kr=%d kc=%d span %.2f period %.3f)" % (
                                                           h["i"], h["m"], h["kr"], h["kc"], h["span"], h["period"])
                                                                 for h in R["hits"]) or "0"))
    sm = os.path.join(EV, "k1_summary.json")
    if os.path.exists(sm):
        print("\nK1 summary: `%s`" % json.dumps(json.load(open(sm))))

    print("\n### K2 continuation\n")
    print("| Branch | Points | Parameter range | Period range | End | Span at end | Type | CPU-s |")
    print("|---|---|---|---|---|---|---|---|")
    for fn in sorted(os.listdir(EV)):
        if fn.startswith("k2_") and fn.endswith(".json") and not fn.startswith("k2_start"):
            r = json.load(open(os.path.join(EV, fn)))
            if "points" not in r or "classification" not in r:
                continue
            P = r["points"]
            ps = [q["p"] for q in P]
            pers = [q["period"] for q in P]
            print("| %s | %d | [%.6g, %.6g] | [%.4g, %.4g] | %s at p = %.6g | %.3f | %s | %.0f |" % (
                r["name"], len(P), min(ps), max(ps), min(pers), max(pers), r["end_reason"], P[-1]["p"],
                P[-1]["span"], r["classification"].get("type"), r["cpu_s"]))

    print("\n### K3 sizes\n")
    print("| Omega | N | Ticks | Tbar | CV | N_coh | Stalls | Stall rate / period | Visits to D | Events | CPU-s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in json.load(open(os.path.join(EV, "k3_sizes.json"))):
        if "ticks" not in r:
            print("| %d | %d | not run: %s |" % (r["omega"], r["N"], r.get("skipped")))
            continue
        print("| %d | %d | %d | %.2f | %.4f | %.2f | %d | %.3g | %d | %.3g | %.1f |" % (
            r["omega"], r["N"], r["ticks"], r["Tbar"], r["cv"], r["ncoh"], r["stalls"], r["stall_rate"],
            r["dvisits"], r["events"], r["cpu_s"]))
    print("\n### Harness\n")
    print("| Check | Key numbers | Pass | CPU-s |")
    print("|---|---|---|---|")
    for r in json.load(open(os.path.join(EV, "k3_harness.json")))["results"]:
        keys = {k: v for k, v in r.items() if k not in ("name", "passed", "cpu_s", "rows", "cases")}
        if "cases" in r:
            keys = [(c["cv_true"], round(c["cv_est"], 4), round(c["ncoh_est"], 2)) for c in r["cases"]]
        if "rows" in r:
            keys = dict(slope_all=round(r["slope_all"], 3),
                        cv=[(q["omega"], round(q["cv"], 3), round(q["ncoh"], 2)) for q in r["rows"]])
        print("| %s | `%s` | %s | %.1f |" % (r["name"], json.dumps(keys, default=float), r["passed"], r["cpu_s"]))


if __name__ == "__main__":
    main()
