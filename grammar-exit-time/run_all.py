"""Run every measurement of SPEC.md and write evidence/*.json.

Stages are resumable: a stage whose evidence file exists is skipped unless named
with --force.  Usage: python run_all.py [stage ...] [--force]"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

from gexit import master, model, planted, series, sim, stats

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")
LOG = os.path.join(EV, "run_log.txt")
H = 3600.0

BUDGET = dict(D=1.75 * H, series=2.0 * H, D0_max=0.5 * H, R1=0.75 * H, M3=0.5 * H, M5=0.25 * H)
M1_GRID = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128]
M3_GRID = [4 * 2 ** j for j in range(11)]


def log(msg):
    line = "%s %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def ev_path(name):
    return os.path.join(EV, name + ".json")


def save(name, obj):
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (complex, np.complexfloating)):
            return [float(o.real), float(o.imag)]
        raise TypeError(type(o))

    tmp = ev_path(name) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, default=conv, separators=(",", ":"))
    os.replace(tmp, ev_path(name))


def load(name):
    with open(ev_path(name)) as f:
        return json.load(f)


def spec_hash():
    return hashlib.sha256(open(os.path.join(HERE, "SPEC.md"), "rb").read()).hexdigest()


# ---------------------------------------------------------------- M0
def stage_m0():
    out = dict(A=model.A_CONST)
    bma = model.balance_ma()
    out["MA_balance"] = bma.tolist()
    out["MA_residual"] = float(np.abs(model.drift(bma, "MA")).max())
    out["MA_eigs"] = [complex(z) for z in np.linalg.eigvals(model.jacobian(bma, "MA"))]
    ths = model.balances_th()
    out["TH_cubic_roots"] = sorted(float(r.real) for r in np.roots(model.th_cubic()))
    out["TH_balances"] = [b.tolist() for b in ths]
    out["TH_residuals"] = [float(np.abs(model.drift(b, "TH")).max()) for b in ths]
    out["TH_eigs"] = [[complex(z) for z in np.linalg.eigvals(model.jacobian(b, "TH"))] for b in ths]
    out["S_minus_A_identity_max_err"] = float(max(abs(model.S_minus_A(y) - (y - 2) * (y - 3) * (y - 4) / (1 + y) ** 2)
                                                  for y in np.linspace(0.01, 20, 2001)))
    out["lambda_slow"] = {s: complex(model.lambda_slow(model.BAL[s], model.LAW_OF[s])) for s in ("MA", "TH2", "TH4")}
    out["t_burn"] = {s: model.burn_in_time(s) for s in ("MA", "TH2", "TH4")}
    # drift check (a): C propensities reproduce f(n / Omega)
    rng = np.random.default_rng(1)
    da = {}
    for law, mdl in (("MA", "MA"), ("TH", "TH"), ("R1", "MAC")):
        for om in (10, 1000):
            worst = 0.0
            worst_r1 = 0.0
            for _ in range(1000):
                n = rng.integers(0, 4 * om, size=4)
                a = sim.propensities(mdl, om, n)
                f_ssa = a @ model.NU / om
                f_ode = model.drift(n / om, "MA" if law == "R1" else law)
                if law == "R1":
                    expected = f_ode - model.KVEC[9] * (n[0] / om) / om * model.NU[9]
                    worst_r1 = max(worst_r1, float(np.abs(f_ssa - expected).max() / (1 + np.abs(f_ode).max())))
                    worst = max(worst, float(np.abs(f_ssa - f_ode).max()))
                else:
                    worst = max(worst, float(np.abs(f_ssa - f_ode).max() / (1 + np.abs(f_ode).max())))
            da["%s_Omega%d" % (law, om)] = dict(max_dev=worst, r1_identity_err=worst_r1)
    out["drift_check_a"] = da
    # drift check (b): one trajectory at Omega = 1e5 versus the ODE
    x0 = np.array([0.5, 1.0, 1.5, 1.0])
    times = np.array([0.5, 1.0, 2.0, 5.0])
    db = {}
    om = 1e5
    for law in ("MA", "TH"):
        traj, ev = sim.run_traj(law, om, model.round_half_up(om * x0), times, sim.seed_for("M0", law))
        sol = model.integrate(x0, law, 5.0, t_eval=times)
        dev = np.abs(traj / om - sol.y.T).max(axis=1)
        db[law] = dict(times=times.tolist(), ssa=(traj / om).tolist(), ode=sol.y.T.tolist(), max_dev=dev.tolist(),
                       passed=bool(dev.max() <= 0.02))
    out["drift_check_b"] = db
    # attraction and cycle check
    att = {}
    for law in ("MA", "TH"):
        stab = [bma] if law == "MA" else [ths[0], ths[2]]
        ends, fails = [], []
        for i in range(200):
            x = rng.uniform(0, 3, 4)
            sol = model.integrate(x, law, 3000.0)
            e = sol.y[:, -1]
            d = min(float(np.linalg.norm(e - b)) for b in stab)
            ends.append(d)
            if d > 1e-6:
                fails.append(dict(x0=x.tolist(), end=e.tolist(), dist=d))
        which = None
        if law == "TH":
            which = dict(v2=0, v4=0)
        att[law] = dict(n=200, max_dist=max(ends), n_not_converged=len(fails), not_converged=fails)
    out["attraction"] = att
    out["sustained_cycle_seen"] = any(att[l]["n_not_converged"] for l in att)
    save("m0", out)
    log("M0 done: lambda_slow %s, t_b %s, drift(b) %s, attraction %s" % (
        out["lambda_slow"], out["t_burn"], {k: v["passed"] for k, v in db.items()},
        {k: v["n_not_converged"] for k, v in att.items()}))


# ---------------------------------------------------------------- M1 / R1
def m1_arm(start, target, mdl=None):
    law = model.LAW_OF[start]
    return series.Arm(target, mdl or law, lambda om, s=start: model.start_counts(s, om), target,
                      model.burn_in_time(start))


def stage_m1(start):
    name = "M1_%s" % start
    res = {}
    sD = series.run_series(name + "_D", [m1_arm(start, "D")], M1_GRID, BUDGET["D"], log=log)
    res["D"] = sD
    save(name, res)
    b0 = min(BUDGET["D0_max"], BUDGET["series"] - sD["spent"])
    sD0 = series.run_series(name + "_D0", [m1_arm(start, "D0")], M1_GRID, b0, log=log)
    res["D0"] = sD0
    res["t_burn"] = model.burn_in_time(start)
    save(name, res)


def stage_r1():
    s = series.run_series("R1_MAC_D", [m1_arm("MA", "D", mdl="MAC")], M1_GRID, BUDGET["R1"], log=log)
    s["t_burn"] = model.burn_in_time("MA")
    save("R1", s)


# ---------------------------------------------------------------- M3 / M5
def m3_arms():
    up = series.Arm("Sup", "TH", lambda om: model.start_counts("TH2", om), "VGE", 0.0, ta_fn=lambda om: 4 * om)
    dn = series.Arm("Sdown", "TH", lambda om: model.start_counts("TH4", om), "VLE", 0.0, ta_fn=lambda om: 2 * om)
    return [up, dn]


def stage_m3():
    s = series.run_series("M3", m3_arms(), M3_GRID, BUDGET["M3"], cap_mult=100.0, log=log)
    save("M3", s)


def stage_m5():
    m3 = load("M3")
    ok = []
    for sz in m3["sizes"]:
        if sz["status"] == "fitted" and all(len(sz["arms"][a]["time"]) >= 300 for a in ("Sup", "Sdown")):
            ok.append(sz)
    sel = ok[-3:]
    tb = model.burn_in_time("TH2")
    plan = []
    for sz in sel:
        om = sz["Omega"]
        Tu = sum(sz["arms"]["Sup"]["time"]) / (len(sz["arms"]["Sup"]["time"]) - sum(sz["arms"]["Sup"]["cens"]))
        Td = sum(sz["arms"]["Sdown"]["time"]) / (len(sz["arms"]["Sdown"]["time"]) - sum(sz["arms"]["Sdown"]["cens"]))
        sim_time = sum(sz["arms"]["Sup"]["time"]) + sum(sz["arms"]["Sdown"]["time"])
        rate = sz["cpu"] / sim_time  # CPU-s per unit simulated time
        plan.append(dict(Omega=om, T_up=Tu, T_down=Td, t_total=400 * max(Tu, Td), rate=rate))
    proj = sum(p["rate"] * (tb + p["t_total"]) for p in plan)
    scale = 1.0
    if proj > BUDGET["M5"]:
        scale = (BUDGET["M5"] - sum(p["rate"] * tb for p in plan)) / sum(p["rate"] * p["t_total"] for p in plan)
    log("M5 plan %s projected %.0f s, scale %.3f" % ([(p["Omega"], round(p["t_total"])) for p in plan], proj, scale))
    tasks = []
    for p in plan:
        om = p["Omega"]
        p["t_total_run"] = p["t_total"] * scale
        tasks.append(dict(model="TH", omega=om, n0=model.start_counts("TH2", om), t_burn=tb, t_total=p["t_total_run"],
                          seed=sim.seed_for("M5", om), nmax=8 * om, nblocks=20, lo=2 * om, hi=4 * om))
    res = sim.map_batches(tasks, fn=sim.run_hist)
    out = dict(scale=scale, projected_cpu=proj, t_burn=tb, sizes=[])
    for p, r in zip(plan, res):
        om = p["Omega"]
        h = r["hist"]
        tot = h.sum(axis=1, keepdims=True)
        pb = h / tot  # per-block pmf
        pm = h.sum(axis=0) / h.sum()

        def dw(a, b, pmf):
            with np.errstate(divide="ignore"):
                return -np.log(pmf[..., a] / pmf[..., b]) / om

        up_b = dw(3 * om, 2 * om, pb)
        dn_b = dw(3 * om, 4 * om, pb)
        out["sizes"].append(dict(Omega=om, plan=p, n_switch=r["n_switch"], cpu=r["cpu"], events=r["events"],
                                 pi_2=float(pm[2 * om]), pi_3=float(pm[3 * om]), pi_4=float(pm[4 * om]),
                                 dW_up=float(dw(3 * om, 2 * om, pm)), dW_down=float(dw(3 * om, 4 * om, pm)),
                                 dW_up_se=float(np.std(up_b, ddof=1) / math.sqrt(len(up_b))),
                                 dW_down_se=float(np.std(dn_b, ddof=1) / math.sqrt(len(dn_b))),
                                 pmf=pm.tolist()))
    save("M5", out)
    log("M5 done: %s" % [(s["Omega"], s["dW_up"], s["dW_down"], s["n_switch"]) for s in out["sizes"]])


# ---------------------------------------------------------------- M6
def stage_m6():
    exact_file = ev_path("m6_exact")
    if os.path.exists(exact_file):
        exact = load("m6_exact")
    else:
        exact = []
        for start in ("MA", "TH2", "TH4"):
            for om in (2, 3, 4):
                n0 = model.start_counts(start, om)
                r = master.converged_mfpt(model.LAW_OF[start], om, n0, log=log)
                r.update(start=start, Omega=om, n0=n0.tolist())
                exact.append(r)
        save("m6_exact", exact)
    rows = []
    for e in exact:
        start, om = e["start"], e["Omega"]
        n0 = model.start_counts(start, om)
        T_ref = e["T"] if e["converged"] else e["levels"][-1]["T"]
        tasks = [dict(model=model.LAW_OF[start], omega=om, n0=n0, target="D", t_burn=0.0, cap=1e6 * T_ref,
                      nruns=250, seed=sim.seed_for("M6", start, om, b)) for b in range(8)]
        res = sim.map_batches(tasks)
        t = np.concatenate([r["time"] for r in res])
        c = np.concatenate([r["cens"] for r in res])
        mean = float(t.mean())
        se = float(t.std(ddof=1) / math.sqrt(len(t)))
        z = (mean - T_ref) / se
        rows.append(dict(start=start, Omega=om, converged=e["converged"], T_exact=T_ref,
                         T_levels=[l["T"] for l in e["levels"]], states=[l["states"] for l in e["levels"]],
                         residuals=[l["residual"] for l in e["levels"]], n=len(t), censored=int(c.sum()),
                         T_sim=mean, se=se, z=z, agree_3se=bool(abs(z) <= 3),
                         z_levels=[(mean - l["T"]) / se for l in e["levels"]],
                         cpu=float(sum(r["cpu"] for r in res))))
        log("M6 %s Omega=%d exact=%.6g (%s) sim=%.6g +- %.3g z=%.2f" % (start, om, T_ref,
                                                                       "converged" if e["converged"] else "UNCONVERGED",
                                                                       mean, se, z))
    save("M6", dict(rows=rows))


# ---------------------------------------------------------------- planted
def stage_planted():
    out = {}
    s1 = planted.run_pf1(log=log)
    out["PF1_series"] = s1
    s2 = planted.run_pf2(log=log)
    out["PF2_series"] = s2
    out["PF3"] = planted.run_pf3()
    log("PF3 %s" % {k: v for k, v in out["PF3"].items()})
    out["PF4"] = planted.run_pf4()
    log("PF4 %s" % out["PF4"])
    out["PF1_exact"] = [planted.pf1_exact(om) for om in planted.PF1_GRID]
    out["PF2_exact"] = {om: planted.pf2_exact(om) for om in planted.PF2_GRID}
    save("planted", out)


STAGES = dict(m0=stage_m0, planted=stage_planted, m1_MA=lambda: stage_m1("MA"), m1_TH2=lambda: stage_m1("TH2"),
              m1_TH4=lambda: stage_m1("TH4"), r1=stage_r1, m3=stage_m3, m5=stage_m5, m6=stage_m6)
FILES = dict(m0="m0", planted="planted", m1_MA="M1_MA", m1_TH2="M1_TH2", m1_TH4="M1_TH4", r1="R1", m3="M3",
             m5="M5", m6="M6")


def main(argv):
    os.makedirs(EV, exist_ok=True)
    force = "--force" in argv
    names = [a for a in argv if not a.startswith("--")] or list(STAGES)
    log("run_all start: stages %s; SPEC sha256 %s" % (names, spec_hash()))
    for n in names:
        if os.path.exists(ev_path(FILES[n])) and not force:
            log("skip %s (evidence exists)" % n)
            continue
        t0 = time.time()
        log("stage %s start" % n)
        STAGES[n]()
        log("stage %s done in %.0f s" % (n, time.time() - t0))


if __name__ == "__main__":
    main(sys.argv[1:])
