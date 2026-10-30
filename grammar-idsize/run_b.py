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
    k10, om, direction, cap = args
    sw = race.switching_runs(k10, om, direction, cpu_cap=cap)
    return dict(k10=k10, Omega=om, direction=direction, n=len(sw["times"]), passages=int(sw["secD"].sum()),
                capped=int(sw["cens"].sum()), cpu=sw["cpu"], cpu_capped=sw["cpu_capped"], cpu_share=cap,
                tau_S_nopass=sw["times"][(~sw["secD"]) & (~sw["cens"])].tolist())


def levelled(stage, fn, cap_total, per_job_max=None):
    """SPEC §5 budget: sizes in increasing order, all (k10, direction) cells of a size together, each cell
    capped at an equal share of the remaining stage budget (and at per_job_max); stop when it is spent."""
    out, spent = [], 0.0
    with ProcessPoolExecutor(WORKERS) as ex:
        for om in race.SIZES:
            remaining = cap_total - spent
            cells = [(k10, om, d) for k10 in family.K10S for d in ("up", "down")]
            if remaining <= 0.02 * cap_total:
                log("%s budget stop before Omega=%d (spent %.0f s)" % (stage, om, spent))
                break
            share = remaining / len(cells)
            if per_job_max is not None:
                share = min(share, per_job_max)
            for r in ex.map(fn, [c + (share,) for c in cells]):
                out.append(r)
                spent += r["cpu"]
                log("%s k10=%s Omega=%d %s %s cpu=%.0f spent=%.0f" % (
                    stage, r["k10"], r["Omega"], r["direction"],
                    {k: r[k] for k in ("n", "passages", "T", "se", "cpu_capped") if k in r}, r["cpu"], spent))
            save(stage, dict(rows=out, spent=spent, cap=cap_total))
    return out, spent


def stage_switch():
    levelled("switch", _switch_job, 1.5 * H)


def _td0_job(args):
    k10, om, direction, cap = args
    return dict(k10=k10, Omega=om, direction=direction, **race.td0_runs(k10, om, direction, cpu_cap=cap))


def stage_td0():
    # 900 CPU-s per cell is the SPEC value; 54 cells could take 13.5 h, so the 1.5 CPU-h stage cap binds:
    # sizes in increasing order, each cell at most min(900 s, its share of the remaining budget).
    levelled("td0", _td0_job, 1.5 * H, per_job_max=900.0)


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
    """Sizes in increasing order, saved after every job; no new job starts once the 0.5 CPU-h cap is spent."""
    jobs = [(k10, om, d) for om in (2, 3, 4) for k10 in family.K10S for d in ("up", "down")]
    out, spent = [], 0.0
    with ProcessPoolExecutor(WORKERS) as ex:
        it = iter(jobs)
        pending = [ex.submit(_exact_job, j) for j in [next(it) for _ in range(WORKERS)]]
        while pending:
            r = pending.pop(0).result()
            out.append(r)
            spent += r["cpu"]
            log("exact k10=%s Omega=%d %s T=%s conv=%s cpu=%.0f spent=%.0f" % (
                r["k10"], r["Omega"], r["direction"], r.get("T_exact"), r.get("converged"), r["cpu"], spent))
            save("exact", dict(rows=out, spent=spent, cap=0.5 * H))
            j = next(it, None)
            if j is not None and spent < 0.5 * H:
                pending.append(ex.submit(_exact_job, j))
            elif j is not None:
                log("exact budget stop before %s" % (j,))
                it = iter(())


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


_POOL = None


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
    r = ffs.run_size(model, om, k, n0, tb, seed, path=path, mapper=_POOL.map if _POOL is not None else map)
    r["t_burn"] = tb
    r["replicates"] = [{kk: vv for kk, vv in rep.items()} for rep in r["replicates"]]
    return r


def stage_harness():
    jobs = [("TH", om, 1000 + om) for om in (8, 10, 12)] + [("MA", om, 2000 + om) for om in (6, 8, 10)]
    global _POOL
    out = []
    _POOL = ProcessPoolExecutor(WORKERS)
    if True:
        for (model, om, _), r in zip(jobs, map(_ffs_job, jobs)):
            ser = "M1_TH2" if model == "TH" else "M1_MA"
            T3, se3 = pr3_T(ser, om)
            comb = math.sqrt(r.get("T_se", float("inf")) ** 2 + se3 ** 2)
            z = (r["T"] - T3) / comb if "T" in r else None
            row = dict(model=model, Omega=om, T_ffs=r.get("T"), T_ffs_se=r.get("T_se"), T_pr3=T3, T_pr3_se=se3, z=z,
                       pass_=bool(z is not None and abs(z) <= 2), cpu=r["cpu"], n_ok=r["n_ok"],
                       interfaces=r["replicates"][0].get("interfaces"))
            out.append(row)
            log("harness %s Omega=%d T_ffs=%s T_pr3=%.4g z=%s" % (model, om, r.get("T"), T3, z))
    pf1 = planted.pf1_ffs(mapper=_POOL.map)
    _POOL.shutdown()
    log("harness PF1 via FFS: %s" % [(r["Omega"], r["T_ffs"], r["T_exact"], r["rel_err"]) for r in pf1["rows"]])
    save("harness", dict(rows=out, pf1=pf1, pass_=bool(all(r["pass_"] for r in out) and pf1["pass_"])))


def stage_ffs():
    global _POOL
    _POOL = ProcessPoolExecutor(WORKERS)
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
