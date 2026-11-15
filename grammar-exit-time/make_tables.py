"""Print the markdown tables used in RESULTS.md from evidence/analysis.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "evidence", "analysis.json")))


def g(x, f="%.4g"):
    return "—" if x is None else (f % x)


def series_table(title, rr):
    print("\n**%s** (spent %.0f of %.0f CPU-s; stop: %s)\n" % (title, rr["spent"], rr["budget"], rr["stop_reason"]))
    m2 = {t["Omega"]: t for t in rr["M2"]}
    print("| Ω | status | n | exits | censored | T̂ | 95% χ² interval | bootstrap interval | CV | restarts | "
          "acceptance | M2 p |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rr["rows"]:
        if "T" not in r:
            print("| %s | %s | — | — | — | — | — | — | — | — | — | — |" % (r["Omega"], r["status"]))
            continue
        t = m2.get(r["Omega"])
        print("| %s | %s | %d | %d | %d | %s | [%s, %s] | [%s, %s] | %.2f | %d | %s | %s |" % (
            r["Omega"], r["status"], r["n"], r["d"], r["censored"], g(r["T"]), g(r["chi2_lo"]), g(r["chi2_hi"]),
            g(r["boot_lo"]), g(r["boot_hi"]), r["cv"], r["restarts"], g(r.get("acceptance"), "%.3g"),
            g(t["p"], "%.3g") if t else "—"))
    if "fit" in rr:
        f = rr["fit"]
        print("\nF1: W = %.4f [%.4f, %.4f], β = %.3f, ΔAIC = %.1f, %d sizes, span %.1f; K1 triggers: %s" % (
            f["W"], f["W_lo"], f["W_hi"], f["beta"], f["dAIC"], f["n_sizes"], f["span"], f["k1_triggers"]))
        print("Local slopes: %s" % ", ".join("%.3f" % s for s in f["local_slopes"]))
        print("Residuals of E: %s" % ", ".join("%+.3f" % s for s in f["resid_E"]))


for start in ("MA", "TH2", "TH4"):
    for tg in ("D", "D0"):
        rr = A.get("M1", {}).get(start, {}).get(tg)
        if rr:
            series_table("M1 %s, target %s" % (start, tg), rr)
if "R1" in A:
    series_table("R1 (MA, combinatorial reaction 11), target D", A["R1"])
    print("\nR1 overlap with MA: %s; T̂_R1/T̂_MA: %s" % (A["R1"].get("overlap"), {
        k: round(v, 3) for k, v in A["R1"].get("T_ratio", {}).items()}))

print("\n**gMAM**\n")
print("| item | W | converged | initial path | N | runs |")
print("|---|---|---|---|---|---|")
for n, v in A.get("gMAM", {}).items():
    runs = "; ".join("%s: %s (N=%s)%s" % (r["init"], g(r["W"], "%.5g"), r["N"], "" if r["converged"] else
                                           " FAILED " + str(r["reason"])) for r in v["runs"])
    best = [r for r in v["runs"] if r["init"] == v["init"]]
    print("| %s | %s | %s | %s | %s | %s |" % (n, g(v["W"], "%.5g"), v["converged"], v["init"],
                                               best[0]["N"] if best else "—", runs))
for k in ("W_D_eff", "W_D0_eff"):
    if k in A:
        print("\n%s = %.5g" % (k, A[k]))

print("\n**F2**\n")
for k, v in A.get("F2", {}).items():
    print("- %s: %s" % (k, json.dumps(v, default=float)))

if "M3" in A:
    for arm in ("Sup", "Sdown"):
        m = A["M3"][arm]
        print("\n**M3 %s** (spent %.0f CPU-s; stop: %s)\n" % (arm, m["spent"], m["stop_reason"]))
        m2 = {t["Omega"]: t for t in m["M2"]}
        print("| Ω | n | censored | mean | SE | CV | via D | M2 p |")
        print("|---|---|---|---|---|---|---|---|")
        for r in m["rows"]:
            t = m2.get(r["Omega"])
            print("| %d | %d | %d | %.4g | %.3g | %.2f | %.3f | %s |" % (r["Omega"], r["n"], r["censored"], r["mean"],
                                                                     r["se"], r["cv"], r["secD_frac"],
                                                                     g(t["p"], "%.3g") if t else "—"))
        if m.get("fit"):
            f = m["fit"]
            print("\nF1 (diagnostic): W = %.3g [%.3g, %.3g], β = %.3f, ΔAIC = %.1f, triggers %s" % (
                f["W"], f["W_lo"], f["W_hi"], f["beta"], f["dAIC"], f["k1_triggers"]))
if "M5" in A:
    print("\n**M5**\n")
    for s in A["M5"]["sizes"]:
        print("- Ω=%d: ΔW↑ = %.4g ± %.2g, ΔW↓ = %.4g ± %.2g, switches %d, run length %.4g" % (
            s["Omega"], s["dW_up"], s["dW_up_se"], s["dW_down"], s["dW_down_se"], s["n_switch"],
            s["plan"]["t_total_run"]))
    print("- extrapolated: %s" % {k: v for k, v in A["M5"].items() if k != "sizes"})
if "M6" in A:
    print("\n**M6**\n")
    print("| start | Ω | converged | levels (T) | states | exact | simulator | SE | z |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in A["M6"]:
        print("| %s | %d | %s | %s | %s | %.6g | %.5g | %.3g | %+.2f |" % (
            r["start"], r["Omega"], r["converged"], ", ".join("%.6g" % t for t in r["T_levels"]),
            ", ".join(str(s) for s in r["states"]), r["T_exact"], r["T_sim"], r["se"], r["z"]))
for k in ("PF1", "PF2", "PF3", "PF4"):
    if k in A:
        print("\n%s: %s" % (k, json.dumps({a: b for a, b in A[k].items() if a != "rows"}, default=float)))
for k in ("K1", "K2", "K3", "ratios"):
    print("\n%s: %s" % (k, json.dumps(A.get(k), default=float)))
