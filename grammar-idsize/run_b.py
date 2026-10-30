"""Task B stages (SPEC): m0, planted, gmam, switch, td0, exact, harness, ffs.  Usage: python run_b.py STAGE ...

Each stage writes evidence/<stage>.json; run_log.txt records progress."""
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from idsize import family, ffs, planted, race

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")
PR3 = os.path.join(os.path.dirname(HERE), "grammar-exit-time", "evidence")
LOG = os.path.join(EV, "run_log.txt")
WORKERS = int(os.environ.get("IDSIZE_WORKERS", "2"))
H = 3600.0


def log(msg):
    with open(LOG, "a") as f:
        f.write("%s %s\n" % (time.strftime("%H:%M:%S"), msg))


def conv(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


def save(name, obj):
    json.dump(obj, open(os.path.join(EV, name + ".json"), "w"), default=conv, indent=1)


def load(name):
    p = os.path.join(EV, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


# ------------------------------------------------------------------ stages
def stage_m0():
    save("m0", family.m0())


def stage_planted():
    out = dict(PF5=planted.pf5(), PF6=planted.pf6())
    log("PF5 pass=%s PF6 pass=%s" % (out["PF5"]["pass_"], out["PF6"]["pass_"]))
    save("planted", out)


def _gmam_item(args):
    k10, item = args
    from gexit_pr3 import m4 as pm4, gmam
    family.use(k10)
    t0 = time.process_time()
    net = gmam.grammar("TH")
    phi0 = pm4.polyline(item["init_pts"], 50)
    r = gmam.gmam(net, item["start"], item["end"], item["free"], phi_init=phi0, log=lambda m: None,
                  label="%s/%s" % (item["name"], item["init"]))
    return dict(k10=k10, name=item["name"], init=item["init"], converged=r.get("converged"), W=r.get("W"), N=r.get("N"),
                reason=r.get("reason"), end=r["path"][-1] if r.get("path") else None, cpu=time.process_time() - t0,
                path=r.get("path") if item["name"] == "TH_W_D_v2" else None)


def stage_gmam():
    from gexit_pr3 import m4 as pm4
    items = [it for it in pm4.items() if it["law"] == "TH" and it["name"] in ("TH_W_D_v2", "TH_W_D_v4", "TH_W_Sup",
                                                                             "TH_W_Sdown")]
    jobs = [(k10, it) for k10 in family.K10S for it in items]
    with ProcessPoolExecutor(WORKERS) as ex:
        res = list(ex.map(_gmam_item, jobs))
    best = {}
    for r in res:
        key = "%s|%s" % (r["k10"], r["name"])
        if r["converged"] and (key not in best or r["W"] < best[key]["W"]):
            best[key] = r
    save("gmam", dict(runs=[{k: v for k, v in r.items() if k != "path"} for r in res],
                      best={k: dict(W=v["W"], init=v["init"], N=v["N"], end=v["end"]) for k, v in best.items()}))
    log("gmam done: %s" % {k: round(v["W"], 6) for k, v in best.items()})


def _switch_job(args):
    k10, om, direction = args
    sw = race.switching_runs(k10, om, direction)
    return dict(k10=k10, Omega=om, direction=direction, n=len(sw["times"]), passages=int(sw["secD"].sum()),
                capped=int(sw["cens"].sum()), cpu=sw["cpu"],
                tau_S_nopass=sw["times"][(~sw["secD"]) & (~sw["cens"])].tolist())


def stage_switch():
    jobs = [(k10, om, d) for k10 in family.K10S for om in race.SIZES for d in ("up", "down")]
    out = []
    with ProcessPoolExecutor(WORKERS) as ex:
        for r in ex.map(_switch_job, jobs):
            out.append(r)
            log("switch k10=%s Omega=%d %s n=%d passages=%d cpu=%.0f" % (r["k10"], r["Omega"], r["direction"], r["n"],
                                                                        r["passages"], r["cpu"]))
    save("switch", dict(rows=out))


def _td0_job(args):
    k10, om, direction, cap = args
    return dict(k10=k10, Omega=om, direction=direction, **race.td0_runs(k10, om, direction, cpu_cap=cap))


def stage_td0():
    # Budget 1.5 CPU-h over 54 (k10, Omega, direction) cells: 900 s cap per cell is the SPEC value;
    # the smaller sizes finish far below it.
    jobs = [(k10, om, d, 900.0) for k10 in family.K10S for om in race.SIZES for d in ("up", "down")]
    out = []
    spent = 0.0
    with ProcessPoolExecutor(WORKERS) as ex:
        for r in ex.map(_td0_job, jobs):
            out.append(r)
            spent += r["cpu"]
            log("td0 k10=%s Omega=%d %s T=%.4g se=%.3g n=%d cpu=%.0f spent=%.0f" % (
                r["k10"], r["Omega"], r["direction"], r["T"], r["se"], r["n"], r["cpu"], spent))
    save("td0", dict(rows=out, spent=spent))


def _exact_job(args):
    k10, om, direction = args
    from gexit_pr3 import master, m6_supp
    family.use(k10)
    n0 = race.start_counts(om, 2 if direction == "up" else 4)
    t0 = time.process_time()
    try:
        base = master.converged_mfpt("TH", om, n0, log=lambda m: None)
        caps = base["levels"][-1]["caps"]
        sup = m6_supp.refine("TH", om, n0, caps, log=lambda m: None)
        T = sup["T"]
        conv_ = sup["converged"] or base["converged"]
    except Exception as e:  # noqa: BLE001
        return dict(k10=k10, Omega=om, direction=direction, error=str(e), cpu=time.process_time() - t0)
    return dict(k10=k10, Omega=om, direction=direction, T_exact=T, converged=bool(conv_), caps=sup.get("caps"),
                frozen_rule_converged=bool(base["converged"]), cpu=time.process_time() - t0)


def stage_exact():
    jobs = [(k10, om, d) for k10 in family.K10S for om in (2, 3, 4) for d in ("up", "down")]
    with ProcessPoolExecutor(WORKERS) as ex:
        out = list(ex.map(_exact_job, jobs))
    save("exact", dict(rows=out))


def pr3_T(series, om):
    d = json.load(open(os.path.join(PR3, series + ".json")))["D"]
    for s in d["sizes"]:
        if s["Omega"] == om and s.get("status") == "fitted":
            t = np.asarray(s["arms"]["D"]["time"])
            c = np.asarray(s["arms"]["D"]["cens"], bool)
            S, dd = t.sum(), int((~c).sum())
            from gexit_pr3 import stats
            lo, hi = stats.chi2_interval(S, dd)
            T = S / dd
            return T, T * (math.log(hi) - math.log(lo)) / (2 * 1.959964)
    return None, None


def gmam_path():
    g = json.load(open(os.path.join(PR3, "gmam_raw.json")))
    best = min((r for r in g if r["name"] == "TH_W_D_v2" and r.get("converged")), key=lambda r: r["W"])
    return np.array(best["path"])


def _ffs_job(args):
    model, om, seed = args
    from gexit_pr3 import model as pm
    if model == "TH":
        family.use(1.0)
        k = family.kvec(1.0)
        tb = pm.burn_in_time("TH2")
        path = gmam_path()
    else:
        pm.set_k(pm.KVEC)
        k = np.array([2.0, 9.0, 47.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 13.0, 0.5])
        tb = pm.burn_in_time("MA")
        path = None
    n0 = race.start_counts(om, 2) if model == "TH" else np.array([om, int(math.floor(om / 2 + 0.5)), om,
                                                                    int(math.floor(om / 2 + 0.5))], np.int64)
    r = ffs.run_size(model, om, k, n0, tb, seed, path=path)
    r["t_burn"] = tb
    r["replicates"] = [{kk: vv for kk, vv in rep.items()} for rep in r["replicates"]]
    return r


def stage_harness():
    jobs = [("TH", om, 1000 + om) for om in (8, 10, 12)] + [("MA", om, 2000 + om) for om in (6, 8, 10)]
    out = []
    with ProcessPoolExecutor(WORKERS) as ex:
        for (model, om, _), r in zip(jobs, ex.map(_ffs_job, jobs)):
            ser = "M1_TH2" if model == "TH" else "M1_MA"
            T3, se3 = pr3_T(ser, om)
            comb = math.sqrt(r.get("T_se", float("inf")) ** 2 + se3 ** 2)
            z = (r["T"] - T3) / comb if "T" in r else None
            row = dict(model=model, Omega=om, T_ffs=r.get("T"), T_ffs_se=r.get("T_se"), T_pr3=T3, T_pr3_se=se3, z=z,
                       pass_=bool(z is not None and abs(z) <= 2), cpu=r["cpu"], n_ok=r["n_ok"],
                       interfaces=r["replicates"][0].get("interfaces"))
            out.append(row)
            log("harness %s Omega=%d T_ffs=%s T_pr3=%.4g z=%s" % (model, om, r.get("T"), T3, z))
    pf1 = planted.pf1_ffs()
    log("harness PF1 via FFS: %s" % [(r["Omega"], r["T_ffs"], r["T_exact"], r["rel_err"]) for r in pf1["rows"]])
    save("harness", dict(rows=out, pf1=pf1, pass_=bool(all(r["pass_"] for r in out) and pf1["pass_"])))


def stage_ffs():
    h = load("harness")
    sizes = (8, 10, 12, 14, 16, 20, 24, 30)
    out = []
    spent = 0.0
    for om in sizes:
        if spent > 2.5 * H:
            log("ffs budget stop before Omega=%d" % om)
            break
        r = _ffs_job(("TH", om, 3000 + om))
        spent += r["cpu"]
        row = {k: v for k, v in r.items() if k != "replicates"}
        row["replicate_lnT"] = [rep.get("lnT") for rep in r["replicates"]]
        row["replicate_stages"] = [rep.get("stages") for rep in r["replicates"]]
        row["interfaces"] = r["replicates"][0].get("interfaces")
        out.append(row)
        save("ffs", dict(rows=out, spent=spent, harness_pass=h["pass_"] if h else None))
        log("ffs Omega=%d T=%s lnT_se=%s cpu=%.0f spent=%.0f" % (om, row.get("T"), row.get("lnT_se"), r["cpu"], spent))


STAGES = dict(m0=stage_m0, planted=stage_planted, gmam=stage_gmam, switch=stage_switch, td0=stage_td0,
              exact=stage_exact, harness=stage_harness, ffs=stage_ffs)

if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    for s in sys.argv[1:]:
        log("stage %s start" % s)
        t0 = time.time()
        STAGES[s]()
        log("stage %s done in %.0f s" % (s, time.time() - t0))
