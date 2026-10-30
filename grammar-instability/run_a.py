"""Task A stages (SPEC): planted, m2, adaptive, m3, m4.  Usage: python run_a.py STAGE ...

Run under `taskset -c 2,3` while task C builds (at most half the cores)."""
import gzip
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from ginst import m2, m3, model, planted

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")
LOG = os.path.join(EV, "run_log.txt")
H = 3600.0
BUDGET = dict(m2=3.5 * H, adaptive=0.5 * H, m3=1.0 * H)
N_DRAWS = 100_000
CHUNK = 100
WORKERS = 2


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
    if isinstance(o, complex):
        return [o.real, o.imag]
    raise TypeError(type(o))


def save(name, obj):
    json.dump(obj, open(os.path.join(EV, name), "w"), default=conv, indent=1)


def stage_planted():
    out = {}
    for f in (planted.pfa1, planted.pfa2, planted.pfa3, planted.pfa4):
        t0 = time.process_time()
        out[f.__name__] = f()
        out[f.__name__]["cpu"] = time.process_time() - t0
        log("%s pass=%s" % (f.__name__, out[f.__name__]["pass_"]))
    save("planted.json", out)


def stage_m2():
    path = os.path.join(EV, "m2_draws.jsonl.gz")
    cpu = 0.0
    done = 0
    counts = {}
    hits = []
    t0 = time.time()
    with gzip.open(path, "wt") as fz, ProcessPoolExecutor(WORKERS) as ex:
        chunks = [list(range(i, min(i + CHUNK, N_DRAWS))) for i in range(0, N_DRAWS, CHUNK)]
        it = iter(chunks)
        pending = []
        for _ in range(2 * WORKERS):
            c = next(it, None)
            if c is not None:
                pending.append(ex.submit(m2.process_chunk, c))
        stop = False
        while pending:
            fut = pending.pop(0)
            for rec in fut.result():
                fz.write(json.dumps(rec, default=conv) + "\n")
                cpu += rec["cpu"]
                done += 1
                key = "%s-%s" % (rec["level"], rec["den"])
                c = counts.setdefault(key, dict(draws=0, balance=0, periodic=0, unresolved=0, draws_with_periodic=0,
                                                draws_with_unresolved=0, multistable=0))
                c["draws"] += 1
                c["balance"] += rec["n_balance"]
                c["periodic"] += rec["n_periodic"]
                c["unresolved"] += rec["n_unresolved"]
                c["draws_with_periodic"] += rec["n_periodic"] > 0
                c["draws_with_unresolved"] += rec["n_unresolved"] > 0
                c["multistable"] += rec["n_stable"] > 1
                if rec["n_periodic"]:
                    hits.append(rec)
            fz.flush()
            if done % 2000 < CHUNK:
                log("m2 done=%d cpu=%.0fs wall=%.0fs counts=%s" % (done, cpu, time.time() - t0, counts))
            if cpu >= BUDGET["m2"]:
                stop = True
            if not stop:
                c = next(it, None)
                if c is not None:
                    pending.append(ex.submit(m2.process_chunk, c))
    save("m2_summary.json", dict(draws=done, cpu=cpu, wall=time.time() - t0, counts=counts, budget_stop=done < N_DRAWS,
                                 periodic_draws=[dict((k, h[k]) for k in ("i", "level", "den", "k", "m", "kr", "kc", "T",
                                                                            "runs")) for h in hits]))
    log("m2 finished: draws=%d cpu=%.0fs counts=%s" % (done, cpu, counts))


def load_draws():
    with gzip.open(os.path.join(EV, "m2_draws.jsonl.gz"), "rt") as f:
        return [json.loads(l) for l in f]


def stage_adaptive():
    recs = load_draws()
    n = len(recs)
    k = max(1, int(round(0.005 * n)))
    by_d = sorted([r for r in recs if np.isfinite(r["delta_rel"])], key=lambda r: r["delta_rel"])
    by_w = sorted(recs, key=lambda r: -r["omega"])
    sel_d, sel_w = by_d[:k], by_w[:k]
    starts = sel_d[:10] + [r for r in sel_w if r["i"] not in {s["i"] for s in sel_d[:10]}][:10]
    t0 = time.process_time()
    with ProcessPoolExecutor(WORKERS) as ex:
        results = list(ex.map(m2.nm_run, [dict((kk, r[kk]) for kk in ("i", "level", "den", "k", "m", "kr", "kc", "T",
                                                                       "law")) for r in starts]))
    # follow-up integrations at near-marginal points
    follow = []
    for res, base in zip(results, starts):
        for lp in res["low_points"][:3]:
            d = dict((kk, base[kk]) for kk in ("i", "level", "den", "m", "kr", "kc", "law"))
            d["k"] = (10.0 ** np.array(lp["x"][:11])).tolist()
            d["T"] = float(10.0 ** lp["x"][11]) if base["level"] == "closed" else base["T"]
            rec = m2.process(d)
            follow.append(dict(i=base["i"], f=lp["f"], kinds=rec["kinds"], n_periodic=rec["n_periodic"],
                               k=d["k"], T=d["T"], runs=rec.get("runs")))
    save("adaptive.json", dict(selected=dict(by_delta=[r["i"] for r in sel_d], by_omega=[r["i"] for r in sel_w]),
                               nm_starts=[r["i"] for r in starts], results=results, follow_up=follow,
                               cpu_parent=time.process_time() - t0))
    log("adaptive done: best f=%s" % [round(r["f_best"], 8) for r in results])


def m3_sub(i):
    """Every tenth draw of each variant (draws are round-robin over the four variants, so i % 10 == 0
    would select the two open variants only)."""
    return (i // 4) % 10 == 0


def m3_balance_jobs(recs):
    jobs = []
    seen = set()
    for r in recs:
        seen.add(r["i"])
        if not m3_sub(r["i"]):
            continue
        for b in r["bal"]:
            if b["stable"]:
                jobs.append(dict(src="TH", i=r["i"], level=r["level"], den=r["den"], k=r["k"], m=r["m"], kr=r["kr"],
                                 kc=r["kc"], T=r["T"], b=b["b"]))
    # M2 stopped early under the H-cyc stop rule; the remaining subsample draws get M2 step 1 (balances
    # and their stability) only, so that M3 covers the planned 10^5-draw subsample.
    for i in range(N_DRAWS):
        if i in seen or not m3_sub(i):
            continue
        d = m2.draw_params(i)
        for rb in model.classify_balances(m2.par_of(d)):
            if rb["stable"]:
                jobs.append(dict(src="TH", i=i, level=d["level"], den=d["den"], k=d["k"], m=d["m"], kr=d["kr"],
                                 kc=d["kc"], T=d["T"], b=rb["b"].tolist(), m2_ran=False))
    for i in range(2000):
        d = m2.draw_params(10_000_000 + i, law="MA")
        d["level"] = "open" if i < 1000 else "closed"
        d["den"] = "cv"
        par = m2.par_of(d)
        for rb in model.classify_balances(par):
            if rb["stable"]:
                jobs.append(dict(src="MA", i=d["i"], level=d["level"], den="cv", k=d["k"], m=d["m"], kr=d["kr"], kc=d["kc"],
                                 T=d["T"], b=rb["b"].tolist(), law="MA"))
    return jobs


def m3_job(job):
    t0 = time.process_time()
    d = dict(job)
    d.setdefault("law", "TH")
    par = m2.par_of(d)
    J = model.J_np(np.array(job["b"]), par)
    res = m3.mobility_tests(J, closed=(job["level"] == "closed"))
    out = dict(src=job["src"], i=job["i"], level=job["level"], den=job["den"], is_P=res["pmatrix"]["is_P"],
               min_minor=res["pmatrix"]["min_minor"], failing=res["pmatrix"]["failing"], used_mp=res["pmatrix"]["used_mp"],
               Gamma_random=res["random"]["osc"]["Gamma"], Gamma_two=res["two_class"]["osc"]["Gamma"],
               stat_random=res["random"]["stat"]["maxre_real"], stat_two=res["two_class"]["stat"]["maxre_real"],
               osc_hit=res["osc_hit"], stat_hit=res["stat_hit"], scale=res["scale"], cpu=time.process_time() - t0)
    if res["osc_hit"] or res["stat_hit"] or not res["pmatrix"]["is_P"]:
        out["detail"] = res
        out["job"] = job
    return out


def stage_m3():
    recs = load_draws()
    jobs = m3_balance_jobs(recs)
    del recs
    log("m3 jobs=%d" % len(jobs))
    out = []
    cpu = 0.0
    with ProcessPoolExecutor(WORKERS) as ex:
        for r in ex.map(m3_job, jobs, chunksize=20):
            out.append(r)
            cpu += r["cpu"]
            if cpu > BUDGET["m3"]:
                log("m3 budget stop at %d of %d" % (len(out), len(jobs)))
                break
    summ = {}
    for r in out:
        key = "%s-%s-%s" % (r["src"], r["level"], r["den"])
        s = summ.setdefault(key, dict(balances=0, not_P=0, osc_hits=0, stat_hits=0, used_mp=0, max_Gamma_rel=-np.inf))
        s["balances"] += 1
        s["not_P"] += not r["is_P"]
        s["osc_hits"] += r["osc_hit"]
        s["stat_hits"] += r["stat_hit"]
        s["used_mp"] += r["used_mp"]
        g = max(r["Gamma_random"], r["Gamma_two"]) / r["scale"]
        s["max_Gamma_rel"] = max(s["max_Gamma_rel"], g)
    save("m3_summary.json", dict(n_jobs=len(jobs), n_done=len(out), cpu=cpu, summary=summ,
                                 flagged=[r for r in out if "detail" in r]))
    with gzip.open(os.path.join(EV, "m3_balances.jsonl.gz"), "wt") as f:
        for r in out:
            f.write(json.dumps({k: v for k, v in r.items() if k not in ("detail", "job")}, default=conv) + "\n")
    log("m3 done: %s" % summ)


def stage_m4cyc():
    """M4 for the periodic M2 end states (SPEC §6); one verification per draw, from its first periodic run."""
    from scipy.integrate import solve_ivp
    from ginst import m4
    out = []
    for r in load_draws():
        if not r["n_periodic"]:
            continue
        t0 = time.process_time()
        run = next(u for u in r["runs"] if u["class"]["kind"] == "periodic")
        d = dict((k, r[k]) for k in ("i", "level", "den", "k", "m", "kr", "kc", "T", "law"))
        par = m2.par_of(d)
        x0 = np.array(run["class"]["point"])
        v = m4.verify_cycle(par, x0, run["class"]["period"])
        n_triv = 2 if r["level"] == "closed" else 1
        mods = np.array(v["moduli"])
        nontriv = np.sort(mods[np.argsort(np.abs(mods - 1.0))[n_triv:]])[::-1]
        v["nontrivial_moduli"] = nontriv.tolist()
        v["verified"] = bool(v["agree"] and np.all(nontriv < 1 - 1e-6))
        v["unstable"] = bool(np.any(nontriv > 1.0))
        # orbit over one period: coordinate ranges and the conserved total
        T = v["periods"]["Radau"]["period"]
        sol = solve_ivp(lambda t, z: model.f_np(z, par), (0, T), x0, method="Radau", rtol=1e-10, atol=1e-14,
                        jac=lambda t, z: model.J_np(z, par), dense_output=True)
        ys = sol.sol(np.linspace(0, T, 2001))
        v["orbit_min"] = ys.min(axis=1).tolist()
        v["orbit_max"] = ys.max(axis=1).tolist()
        v["total_range"] = [float(ys.sum(axis=0).min()), float(ys.sum(axis=0).max())]
        v["closure_rel"] = float(np.linalg.norm(sol.y[:, -1] - x0) / np.linalg.norm(x0))
        v["exact_rates"] = ["%.17g" % x for x in r["k"]]
        v["exact_T"] = "%.17g" % r["T"]
        v["cpu"] = time.process_time() - t0
        out.append(dict(draw=d, balances=r["bal"], m2_periods=[u["class"].get("period") for u in r["runs"]],
                        start_point=x0.tolist(), verification=v))
        log("m4cyc draw %d: verified=%s periods=%s nontrivial=%s" % (r["i"], v["verified"], v["periods"], v["nontrivial_moduli"]))
    save("m4_cycle.json", dict(hits=out, cycle_verified=any(h["verification"]["verified"] for h in out)))


def stage_m4ring():
    """M4 ring for the M3 hits (SPEC §6).  Hits are taken in M3 job order; for each claim the first verified
    hit stops that claim's verification (stop rule, SPEC §7).  M4 CPU cap for the ring: 0.5 h."""
    from ginst import m4
    m3s = json.load(open(os.path.join(EV, "m3_summary.json")))
    runs = []
    done = dict(stat=False, osc=False)
    cpu = 0.0
    for fl in m3s["flagged"]:
        det, job = fl["detail"], fl["job"]
        for kind in ("stat", "osc"):
            if done[kind] or not det[kind + "_hit"] or cpu > 0.5 * H:
                continue
            # the D and s of the larger of the random-D and two-class hits
            key = "maxre_real" if kind == "stat" else "Gamma"
            src = max(("random", "two_class"), key=lambda nm: det[nm][kind][key])
            r = det[src][kind]
            d = dict(job)
            d.setdefault("law", "TH")
            par = m2.par_of(d)
            # s*: the refined point if refinement improved on the grid, else the grid point
            s_star = r["s_ref"] if ("s_ref" in r and r[key] > r[key + "_grid" if kind == "stat" else "Gamma_grid"]) else r["s"]
            v = m4.verify_ring(par, job["b"], r["D"], s_star, kind)
            cpu += v["cpu"]
            row = dict(src=job["src"], i=job["i"], level=job["level"], den=job["den"], is_P=fl["is_P"], D_from=src,
                       exact_rates=["%.17g" % x for x in job["k"]], exact_T="%.17g" % job["T"], m=job["m"],
                       kr=job["kr"], kc=job["kc"], balance=job["b"], **v)
            runs.append(row)
            log("m4ring %s draw %d %s-%s: verified=%s pred=%.4g meas=%s pattern=%s cpu=%.0f" % (
                kind, job["i"], job["level"], job["den"], v["verified"], v["predicted_rate"] or 0.0, v["measured_rate"],
                v.get("pattern"), v["cpu"]))
            if v["verified"]:
                done[kind] = True
            save("m4_lattice.json", dict(runs=runs, cpu=cpu,
                                         stationary_verified=any(x["verified"] and x["kind"] == "stat" and not x["is_P"]
                                                                 for x in runs),
                                         oscillatory_verified=any(x["verified"] and x["kind"] == "osc" for x in runs)))
        if (done["stat"] and done["osc"]) or cpu > 0.5 * H:
            break
    log("m4ring done: cpu=%.0f stat=%s osc=%s" % (cpu, done["stat"], done["osc"]))


STAGES = dict(m4ring=stage_m4ring, planted=stage_planted, m2=stage_m2, adaptive=stage_adaptive, m3=stage_m3, m4cyc=stage_m4cyc)

if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    for s in sys.argv[1:]:
        log("stage %s start" % s)
        STAGES[s]()
        log("stage %s done" % s)
