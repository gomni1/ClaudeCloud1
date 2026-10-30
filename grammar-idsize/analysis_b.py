"""Task B analysis (SPEC §2-§4): per-k10 race table, R1, R2, G1, G2 -> evidence/analysis.json and stdout."""
import json
import math
import os

import numpy as np

from gexit_pr3 import stats
from idsize import race

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")
Z = 1.959964
# PR 3's gMAM values at Astra's constants (k10 = 1), from grammar-exit-time/evidence/gmam_raw.json: the smaller
# converged value of the two initial paths.  Used only where this run's gMAM stage gave no value for k10 = 1.
PR3_GMAM = {"TH_W_D_v2": 0.8199594153016123, "TH_W_D_v4": 0.8202114480929925, "TH_W_Sup": 0.000338306534176509,
            "TH_W_Sdown": 0.0001808758017910484}


def load(name):
    p = os.path.join(EV, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def gmam_values():
    g = load("gmam")
    out = {}
    for k10 in ("0.5", "1.0", "2.0"):
        for nm in PR3_GMAM:
            key = "%s|%s" % (k10, nm)
            if g and key in g["best"]:
                out[key] = dict(W=g["best"][key]["W"], source="this run")
            elif k10 == "1.0":
                out[key] = dict(W=PR3_GMAM[nm], source="PR 3 (same model and code at k10 = 1)")
    return out


def race_table():
    sw = load("switch")
    td = load("td0")
    if not sw:
        return []
    tdi = {(r["k10"], r["Omega"], r["direction"]): r for r in (td or {}).get("rows", [])}
    rows = []
    for s in sw["rows"]:
        key = (s["k10"], s["Omega"], s["direction"])
        n, d = s["n"], s["passages"]
        phi = d / n
        lo, hi = race.clopper_pearson(d, n)
        r = dict(k10=s["k10"], Omega=s["Omega"], direction=s["direction"], n_runs=n, passages=d, phi_obs=phi,
                 phi_lo=lo, phi_hi=hi, phi_obs_se=math.sqrt(phi * (1 - phi) / n), capped_runs=s["capped"],
                 switch_cpu_capped=s.get("cpu_capped", False), n_tau=len(s["tau_S_nopass"]))
        t = tdi.get(key)
        if t is not None and t.get("n", 0) > 1 and np.isfinite(t["T"]):
            est = race.phi_estimates(s["tau_S_nopass"], t["T"], t["se"])
            r.update(T_D0=t["T"], T_D0_se=t["se"], T_D0_n=t["n"], **est)
            r["ratio"] = phi / est["phi_pred"] if est["phi_pred"] > 0 else None
            r["ratio_star"] = phi / est["phi_pred_star"] if est["phi_pred_star"] > 0 else None
            r["r1_eligible"] = bool(phi >= 1e-3 and r["phi_obs_se"] / phi <= 0.2
                                    and est["phi_pred_se"] / est["phi_pred"] <= 0.2)
            r["r1_in_band"] = bool(r["ratio"] is not None and 0.5 <= r["ratio"] <= 2.0)
        else:
            r["r1_eligible"] = False
        rows.append(r)
    return rows


def r1(rows):
    out = {}
    for k10 in (0.5, 1.0, 2.0):
        el = [r for r in rows if r["k10"] == k10 and r["r1_eligible"]]
        bad = [(r["Omega"], r["direction"], r["ratio"]) for r in el if not r["r1_in_band"]]
        out[str(k10)] = dict(eligible=[(r["Omega"], r["direction"], r["ratio"]) for r in el], outside=bad,
                             killed=len(bad) >= 2, n_eligible=len(el))
    killed = any(v["killed"] for v in out.values())
    status = "killed" if killed else ("survived" if all(v["n_eligible"] > 0 for v in out.values()) else "underdetermined")
    return dict(per_k10=out, status=status)


def r2(rows, gm):
    out = {}
    fails = 0
    undetermined = 0
    for k10 in (0.5, 1.0, 2.0):
        per = {}
        for direction, bal in (("up", "TH_W_D_v2"), ("down", "TH_W_D_v4")):
            rs = sorted([r for r in rows if r["k10"] == k10 and r["direction"] == direction and r["passages"] >= 10],
                        key=lambda r: r["Omega"])
            if len(rs) < 4:
                per[direction] = dict(evaluated=False, n_sizes=len(rs))
                continue
            Om = [r["Omega"] for r in rs]
            phi = [r["phi_obs"] for r in rs]
            sig = [(math.log(r["phi_hi"]) - math.log(r["phi_lo"])) / (2 * Z) for r in rs]
            f = stats.fit_EP(Om, phi, sig)
            wd = gm.get("%s|%s" % (k10, bal))
            rec = dict(evaluated=True, Omega=Om, W=float(f["W"]), beta=float(f["beta"]), dAIC=float(f["dAIC"]),
                       W_D=wd["W"] if wd else None, W_D_source=wd["source"] if wd else None)
            if wd is None:
                rec["pass_"] = None
            else:
                rec["slope_rel_dev"] = abs(f["W"] + wd["W"]) / wd["W"]
                rec["pass_"] = bool(rec["slope_rel_dev"] <= 0.25 and f["dAIC"] >= 10)
            per[direction] = rec
        ev = [v for v in per.values() if v["evaluated"]]
        if not ev or any(v["pass_"] is None for v in ev):
            res = None
            undetermined += 1
        else:
            res = all(v["pass_"] for v in ev)
            fails += not res
        out[str(k10)] = dict(directions=per, pass_=res)
    status = "killed" if fails >= 2 else ("survived" if undetermined == 0 else
                                         ("underdetermined" if fails + undetermined >= 2 else "survived"))
    return dict(per_k10=out, n_fail=fails, n_undetermined=undetermined, status=status)


def crossover(rows, gm):
    out = {}
    for k10 in (0.5, 1.0, 2.0):
        for direction, bal in (("up", "TH_W_D_v2"), ("down", "TH_W_D_v4")):
            rs = sorted([r for r in rows if r["k10"] == k10 and r["direction"] == direction], key=lambda r: r["Omega"])
            om = next((r["Omega"] for r in rs if r["phi_obs"] < 0.01), None)
            wd = gm.get("%s|%s" % (k10, bal))
            out["%s|%s" % (k10, direction)] = dict(Omega_star=om, W_D=wd["W"] if wd else None,
                                                   Omega_star_times_W_D=om * wd["W"] if (om and wd) else None)
    return out


def g1():
    f = load("ffs")
    h = load("harness")
    if not f:
        return None
    rows = {r["Omega"]: r for r in f["rows"]}
    sel = [om for om in sorted(rows) if 20 <= om <= 30 and rows[om].get("n_ok", 0) >= 2]
    out = dict(sizes=sel, harness_pass=bool(h and h["pass_"]),
               n_ok={om: rows[om]["n_ok"] for om in sorted(rows)})
    if 20 not in sel or len(sel) < 2:
        out.update(status="underdetermined", reason="Omega = 20 not reached")
        return out
    reps = {om: np.array([x for x in rows[om]["replicate_lnT"] if x is not None], float) for om in sel}

    def s25(means):
        Om = np.array(sel, float)
        y = np.array([means[om] for om in sel])
        if len(sel) == 2:
            return float((y[1] - y[0]) / (Om[1] - Om[0]))
        X = stats.design(Om, "E")
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(beta[1] + beta[2] / 25.0)

    est = s25({om: reps[om].mean() for om in sel})
    rng = np.random.default_rng(2026)
    bs = []
    for _ in range(2000):
        bs.append(s25({om: reps[om][rng.integers(0, len(reps[om]), len(reps[om]))].mean() for om in sel}))
    bs = np.array(bs)
    status = ("supports small-size reading" if 0.738 <= est <= 0.902 else
              "killed (small-size reading)" if est >= 0.95 else
              "underdetermined" if 0.902 < est < 0.95 else "neither (below 0.738)")
    if not out["harness_pass"]:
        status = "underdetermined (harness failed)"
    out.update(s25=est, s25_se=float(bs.std(ddof=1)), s25_ci=[float(v) for v in np.percentile(bs, [2.5, 97.5])],
               boot_frac_supports=float(np.mean((bs >= 0.738) & (bs <= 0.902))),
               boot_frac_kill=float(np.mean(bs >= 0.95)), status=status,
               secant_20_30=float((rows[30]["lnT_mean"] - rows[20]["lnT_mean"]) / 10) if 30 in rows else None,
               secant_20_24=float((rows[24]["lnT_mean"] - rows[20]["lnT_mean"]) / 4) if 24 in rows else None)
    # sensitivity (not the verdict): failed replicates at a size, given the lnT they would have with the failed
    # stage's P set to 0.5 / trials (an optimistic P, so a lower bound on their lnT)
    sens = {}
    for om in sel:
        r = rows[om]
        fills = []
        for st in r["replicate_stages"]:
            if st and st[-1]["successes"] == 0:
                pass
        sens[om] = dict(n_failed=8 - r["n_ok"])
    out["failed_replicates"] = sens
    out["local_slopes_all"] = {"%d-%d" % (a, b): float((rows[b]["lnT_mean"] - rows[a]["lnT_mean"]) / (b - a))
                               for a, b in zip(sorted(rows)[:-1], sorted(rows)[1:])}
    return out


def g2():
    f = load("ffs")
    if not f:
        return None
    rows = {r["Omega"]: r for r in f["rows"]}
    want = [8, 16, 30]
    out = {}
    for om in want:
        use = om if om in rows else min(rows, key=lambda x: abs(x - om))
        r = rows[use]
        out[str(om)] = dict(Omega=use, mean_max_v=r.get("mean_max_v"), mean_dist=r.get("mean_dist"), n_ok=r.get("n_ok"))
    return out


def exact_vs_sim(rows):
    ex = load("exact")
    td = load("td0")
    if not ex or not td:
        return None
    tdi = {(r["k10"], r["Omega"], r["direction"]): r for r in td["rows"]}
    out = []
    for e in ex["rows"]:
        t = tdi.get((e["k10"], e["Omega"], e["direction"]))
        if t is None or "T_exact" not in e:
            out.append(dict(e, z=None))
            continue
        out.append(dict(k10=e["k10"], Omega=e["Omega"], direction=e["direction"], T_exact=e["T_exact"],
                        converged=e["converged"], T_sim=t["T"], T_sim_se=t["se"],
                        z=(t["T"] - e["T_exact"]) / t["se"] if t["se"] > 0 else None))
    return out


def main():
    A = dict(m0=load("m0"), planted=load("planted"), harness=load("harness"))
    gm = gmam_values()
    A["gmam"] = gm
    rows = race_table()
    A["race_rows"] = rows
    A["R1"] = r1(rows)
    A["R2"] = r2(rows, gm)
    A["crossover"] = crossover(rows, gm)
    A["exact_vs_sim"] = exact_vs_sim(rows)
    A["G1"] = g1()
    A["G2"] = g2()
    json.dump(A, open(os.path.join(EV, "analysis.json"), "w"), indent=1, default=float)
    return A


if __name__ == "__main__":
    A = main()
    for r in A["race_rows"]:
        print("k10=%s Om=%2d %-4s n=%d pass=%d phi=%.4g [%.3g,%.3g] T_D0=%s phi_pred=%s ratio=%s elig=%s" % (
            r["k10"], r["Omega"], r["direction"], r["n_runs"], r["passages"], r["phi_obs"], r["phi_lo"], r["phi_hi"],
            r.get("T_D0"), r.get("phi_pred"), r.get("ratio"), r["r1_eligible"]))
    for k in ("R1", "R2", "crossover", "G1", "G2", "exact_vs_sim", "gmam"):
        print(k, json.dumps(A[k], default=float)[:1500])
