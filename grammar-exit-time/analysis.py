"""Evaluate SPEC §7-§9 from evidence/*.json and write evidence/analysis.json."""
import json
import math
import os
import sys

import numpy as np
from scipy.stats import spearmanr

from gexit import m4, planted, series, sim, stats

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")
B_FIT = 2000
B_LILLIE = 10000


def load(name):
    p = os.path.join(EV, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def m2_tests(s, arm, min_exits=1000):
    out = []
    for sz in s["sizes"]:
        r = sz["arms"].get(arm)
        if r is None:
            continue
        t = np.asarray(r["time"])
        c = np.asarray(r["cens"], bool)
        x = t[~c]
        if len(x) >= min_exits:
            res = stats.lilliefors_exp(x, B=B_LILLIE, rng=sim.seed_for("M2", s["name"], arm, sz["Omega"]) % 2**32)
            res["Omega"] = sz["Omega"]
            out.append(res)
    return out


def fit_series(s, arm, tag):
    sizes = series.fitted_sizes(s, arm)
    rows = series.summarize_series(s, arm)
    out = dict(rows=rows, n_fitted=len(sizes), spent=s["spent"], budget=s["budget"], stop_reason=s["stop_reason"])
    if len(sizes) >= 4:
        out["fit"] = stats.f1(sizes, B=B_FIT, rng=sim.seed_for("F1", tag) % 2**32)
    oms = [z[0] for z in sizes]
    out["sufficient"] = bool(len(sizes) >= 6 and oms and max(oms) / min(oms) >= 4)
    out["M2"] = m2_tests(s, arm)
    return out


def preasymptotic(fit, Wg):
    """SPEC §7 F2: both conditions needed to call the sizes pre-asymptotic."""
    Om = np.array(fit["Omega"])
    sc = np.array(fit["local_slopes_beta_corrected"])
    mid = 0.5 * (Om[1:] + Om[:-1])
    if len(sc) < 3:
        return dict(allowed=False, reason="too few slopes")
    rho, p = spearmanr(mid, sc)
    toward = np.sign(Wg - fit["W"])
    cond1 = bool(p < 0.05 and np.sign(rho) == toward)
    cond2 = bool(abs(sc[-1] - Wg) < abs(fit["W"] - Wg))
    return dict(rho=float(rho), p=float(p), last_corrected_slope=float(sc[-1]), cond1=cond1, cond2=cond2,
                allowed=cond1 and cond2)


def main():
    A = {}
    pl = load("planted")
    if pl:
        e1 = planted.evaluate_pf1(pl["PF1_series"], B=B_FIT)
        e2 = planted.evaluate_pf2(pl["PF2_series"], B=B_FIT)
        A["PF1"] = dict(W=e1["fit"]["W"], W_lo=e1["fit"]["W_lo"], W_hi=e1["fit"]["W_hi"], beta=e1["fit"]["beta"],
                        dAIC=e1["fit"]["dAIC"], pass_W=e1["pass_W"], pass_coverage=e1["pass_coverage"],
                        pass_coverage_bonferroni=e1["pass_coverage_bonferroni"], rows=e1["rows"],
                        W_fit_to_exact=stats.fit_EP(e1["fit"]["Omega"], [r["T_exact"] for r in e1["rows"]],
                                                    e1["fit"]["sigma_ln"])["W"])
        A["PF2"] = dict(W=e2["fit"]["W"], W_lo=e2["fit"]["W_lo"], W_hi=e2["fit"]["W_hi"], beta=e2["fit"]["beta"],
                        dAIC=e2["fit"]["dAIC"], triggers=e2["fit"]["k1_triggers"], pass_=e2["pass_"], rows=e2["rows"])
        A["PF3"] = pl["PF3"]
        A["PF4"] = pl["PF4"]
    g = load("gmam_raw")
    G = m4.collect(g) if g else {}
    A["gMAM"] = G

    def gW(name):
        return G.get(name, {}).get("W")

    WSu, WSd = gW("TH_W_Sup"), gW("TH_W_Sdown")
    if WSu is not None and WSd is not None:
        U2, U4 = max(0.0, WSd - WSu), max(0.0, WSu - WSd)
        for tg in ("D", "D0"):
            a, b = gW("TH_W_%s_v2" % tg), gW("TH_W_%s_v4" % tg)
            if a is not None and b is not None:
                A["W_%s_eff" % tg] = min(U2 + a, U4 + b)
    # M1 series, R1
    M1 = {}
    for start in ("MA", "TH2", "TH4"):
        d = load("M1_" + start)
        if not d:
            continue
        M1[start] = {}
        for tg in ("D", "D0"):
            if tg in d:
                M1[start][tg] = fit_series(d[tg], tg, "M1_%s_%s" % (start, tg))
    A["M1"] = M1
    r1 = load("R1")
    if r1:
        A["R1"] = fit_series(r1, "D", "R1")
        if "MA" in M1 and "fit" in A["R1"] and "fit" in M1["MA"]["D"]:
            fa, fb = M1["MA"]["D"]["fit"], A["R1"]["fit"]
            A["R1"]["overlap"] = bool(fa["W_lo"] <= fb["W_hi"] and fb["W_lo"] <= fa["W_hi"])
            Ta = dict(zip(fa["Omega"], fa["T"]))
            A["R1"]["T_ratio"] = {str(o): T / Ta[o] for o, T in zip(fb["Omega"], fb["T"]) if o in Ta}
    # F2
    gm_for = dict(MA="MA_W_%s", TH2="TH_W_%s_v2", TH4="TH_W_%s_v4")
    F2 = {}
    for start, dd in M1.items():
        for tg, rr in dd.items():
            Wg = gW(gm_for[start] % tg)
            if "fit" not in rr or Wg is None:
                continue
            Wf = rr["fit"]["W"]
            row = dict(W_fit=Wf, W_lo=rr["fit"]["W_lo"], W_hi=rr["fit"]["W_hi"], W_gmam=Wg,
                       rel_gap=(Wf - Wg) / Wg, consistent=bool(abs(Wf - Wg) / Wg <= 0.25))
            if not row["consistent"]:
                row["preasymptotic"] = preasymptotic(rr["fit"], Wg)
            if start.startswith("TH") and ("W_%s_eff" % tg) in A:
                We = A["W_%s_eff" % tg]
                row["W_eff"] = We
                row["rel_gap_eff"] = (Wf - We) / We
            F2["%s_%s" % (start, tg)] = row
    A["F2"] = F2
    # M3, M5
    m3 = load("M3")
    if m3:
        M3 = {}
        for arm in ("Sup", "Sdown"):
            rows = []
            for sz in m3["sizes"]:
                r = sz["arms"].get(arm)
                if r is None or not len(r["time"]):
                    continue
                t = np.asarray(r["time"])
                c = np.asarray(r["cens"], bool)
                x = t[~c]
                rows.append(dict(Omega=sz["Omega"], status=sz["status"], n=len(t), censored=int(c.sum()),
                                 mean=float(x.mean()), se=float(x.std(ddof=1) / math.sqrt(len(x))),
                                 cv=float(x.std(ddof=1) / x.mean()), mle=float(t.sum() / len(x)),
                                 secD_frac=float(np.mean(r["secD"])), cpu=r["cpu"]))
            sizes = series.fitted_sizes(m3, arm)
            fit = stats.f1(sizes, B=B_FIT, rng=sim.seed_for("F1", "M3", arm) % 2**32) if len(sizes) >= 4 else None
            M3[arm] = dict(rows=rows, fit=fit, M2=m2_tests(m3, arm), spent=m3["spent"], stop_reason=m3["stop_reason"])
            if fit:
                M3[arm]["exponential_regime"] = not fit["k1_any"]
        A["M3"] = M3
    m5 = load("M5")
    if m5:
        out = dict(sizes=[{k: v for k, v in s.items() if k != "pmf"} for s in m5["sizes"]], scale=m5["scale"])
        for key in ("up", "down"):
            om = np.array([s["Omega"] for s in m5["sizes"]], float)
            y = np.array([s["dW_" + key] for s in m5["sizes"]])
            se = np.array([s["dW_%s_se" % key] for s in m5["sizes"]])
            if len(om) >= 2 and np.all(np.isfinite(y)):
                X = np.column_stack([np.ones_like(om), 1 / om])
                w = 1 / np.maximum(se, 1e-300) ** 2
                beta, _, _ = stats.wls(X, y, w)
                cov = np.linalg.inv(X.T @ (X * w[:, None]))
                out["dW_%s_inf" % key] = float(beta[0])
                out["dW_%s_inf_se" % key] = float(math.sqrt(cov[0, 0]))
            Wg = WSu if key == "up" else WSd
            if Wg is not None and ("dW_%s_inf" % key) in out:
                out["rel_gap_%s" % key] = (out["dW_%s_inf" % key] - Wg) / Wg
                out["consistent_%s" % key] = bool(abs(out["rel_gap_%s" % key]) <= 0.25)
        A["M5"] = out
    m6 = load("M6")
    if m6:
        A["M6"] = m6["rows"]
    # K1
    K1 = {}
    for start in ("MA", "TH2", "TH4"):
        rr = M1.get(start, {}).get("D")
        if rr is None:
            K1[start] = dict(status="not run")
            continue
        if not rr["sufficient"] or "fit" not in rr:
            K1[start] = dict(status="underdetermined", reason="fewer than 6 fitted sizes or span < 4",
                             n_fitted=rr["n_fitted"])
            continue
        f = rr["fit"]
        K1[start] = dict(status="killed" if f["k1_any"] else "survived", triggers=f["k1_triggers"], W=f["W"],
                         W_lo=f["W_lo"], W_hi=f["W_hi"], dAIC=f["dAIC"], n_sizes=f["n_sizes"], span=f["span"])
    st = [v["status"] for v in K1.values()]
    criteria = "killed" if "killed" in st else ("underdetermined" if any(s != "survived" for s in st) else "survived")
    harness_ok = bool(A.get("PF1", {}).get("pass_W")) and bool(A.get("PF2", {}).get("pass_"))
    A["K1"] = dict(per_series=K1, criteria_verdict=criteria, harness_ok=harness_ok,
                   status=criteria if harness_ok else "underdetermined (harness)")
    # K2
    K2 = {}
    for start in ("MA", "TH2", "TH4"):
        rr = M1.get(start, {}).get("D")
        if rr is None or not rr["M2"]:
            K2[start] = dict(status="underdetermined", reason="no size with >= 1000 uncensored exits")
            continue
        t = rr["M2"][-1]
        K2[start] = dict(status="killed" if t["p"] < 0.01 else "survived", Omega=t["Omega"], p=t["p"], D=t["D"],
                         cv=t["cv"], n=t["n"])
    st = [v["status"] for v in K2.values()]
    k2 = "killed" if "killed" in st else ("underdetermined" if any(s != "survived" for s in st) else "survived")
    if not A.get("PF4", {}).get("pass"):
        k2 = "underdetermined (harness)" if k2 != "killed" else k2
    A["K2"] = dict(per_series=K2, status=k2)
    # K3
    WD2, WD4 = gW("TH_W_D_v2"), gW("TH_W_D_v4")
    k3 = dict(W_Sup=WSu, W_Sdown=WSd, W_D_v2=WD2, W_D_v4=WD4, sources={})
    if None not in (WD2, WD4):
        WD = min(WD2, WD4)
        k3["sources"]["W_D"] = "gMAM"
    else:
        fits = [M1.get(s, {}).get("D", {}).get("fit", {}).get("W") for s in ("TH2", "TH4")]
        fits = [f for f in fits if f is not None]
        WD = min(fits) if fits else None
        k3["sources"]["W_D"] = "fitted TH D series"
    WS = {}
    for key, v, arm in (("up", WSu, "Sup"), ("down", WSd, "Sdown")):
        if v is not None:
            WS[key] = v
            k3["sources"]["W_S" + key] = "gMAM"
        elif A.get("M3", {}).get(arm, {}).get("exponential_regime"):
            WS[key] = A["M3"][arm]["fit"]["W"]
            k3["sources"]["W_S" + key] = "M3 fitted slope"
        elif ("dW_%s_inf" % key) in A.get("M5", {}):
            WS[key] = A["M5"]["dW_%s_inf" % key]
            k3["sources"]["W_S" + key] = "M5 dW(inf)"
    if WD is None or len(WS) < 2:
        k3["status"] = "underdetermined"
    else:
        k3["W_D_min"] = WD
        k3["W_S_max"] = max(WS.values())
        k3["status"] = "killed" if max(WS.values()) >= WD else "survived"
        k3["margin_ratio"] = WD / max(WS.values())
    A["K3"] = k3
    if None not in (WD2, WD4, WSu, WSd):
        A["ratios"] = dict(WD_v2_over_WSup=WD2 / WSu, WD_v4_over_WSdown=WD4 / WSd,
                           WD_min_over_WS_max=min(WD2, WD4) / max(WSu, WSd))
    json.dump(A, open(os.path.join(EV, "analysis.json"), "w"), indent=1, default=float)
    return A


if __name__ == "__main__":
    A = main()
    for k in ("K1", "K2", "K3"):
        print(k, json.dumps(A.get(k), default=float)[:1500])
