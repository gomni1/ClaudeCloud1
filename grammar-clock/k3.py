"""K3: the stochastic clock, harness (H1, H2, P1-P3) and sizes (SPEC K3).  Usage: python k3.py [harness|sizes]"""
import json
import os
import sys
import time

import numpy as np
from scipy.stats import chisquare

from clock import core

EV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
CAP = 3 * 3600.0
GRID = [10, 25, 50, 100, 200, 400, 800, 1600, 3200]


def cpu():
    return time.process_time()


def nearest_C_dev(samp4, X):
    """For each sample, |c_C - c_C,det| at the nearest orbit point (4-dim Euclidean)."""
    O = X.T  # (npts, 4)
    out = np.empty(len(samp4))
    for a in range(0, len(samp4), 500):
        S = samp4[a:a + 500].astype(float)
        d2 = ((S[:, None, :] - O[None, :, :]) ** 2).sum(-1)
        j = d2.argmin(1)
        out[a:a + 500] = np.abs(S[:, 0] - O[j, 0])
    return out


def h1():
    tg, X, cdet = core.det_cycle()
    n0, N = core.n_start(1e5, X[:, 0])
    r = core.run_clock(1e5, n0, core.seed_of(1, 0), t_max=2 * core.T_DET, max_ticks=1, nsp=4)
    s = r["samp"]
    dev = nearest_C_dev(s, X)
    per = float(r["ticks"][0]) if len(r["ticks"]) else np.nan
    ok = bool(dev.max() <= 0.01 * core.DELTA and abs(per - 247.53) / 247.53 <= 0.01)
    return dict(name="H1 drift", omega=1e5, N=N, max_dev_C=float(dev.max()), bound=0.01 * core.DELTA, period=per,
                period_rel_err=abs(per - 247.53) / 247.53, events=r["events"], passed=ok)


def h2(om, n_chains=16, n_events=10 ** 7, n_burn=10 ** 6):
    e = core.exact_stationary(om)
    tg, X, cdet = core.det_cycle()
    n0, N = core.n_start(om, X[:, 0])
    H = [core.hist_chain(om, core.seed_of(2, om, j), n_burn, n_events, n0) for j in range(n_chains)]
    pooled = np.sum(H, axis=0)
    a, b = np.sum(H[:8], axis=0), np.sum(H[8:], axis=0)
    tv_ex, tv_half = core.tv(pooled, e["pi_C"]), core.tv(a, b)
    return dict(name="H2 exact", omega=om, N=N, n_states=e["n_states"], tv_pooled_exact=tv_ex,
                tv_half_half=tv_half, events_per_chain=n_events, passed=bool(tv_ex <= tv_half))


def p1():
    rng = np.random.default_rng(31102026)
    out = []
    for cv in (0.05, 0.30):
        shape = 1 / cv ** 2
        iv = rng.gamma(shape, 247.53 / shape, 10 ** 4)
        st = core.tick_stats(np.concatenate([[0], np.cumsum(iv)]))
        out.append(dict(cv_true=cv, cv_est=st["cv"], ncoh_true=1 / cv ** 2, ncoh_est=st["ncoh"],
                        passed=bool(abs(st["cv"] - cv) / cv <= 0.05 and abs(st["ncoh"] * cv ** 2 - 1) <= 0.10)))
    return dict(name="P1 renewal", cases=out, passed=all(c["passed"] for c in out))


def slope(oms, cvs):
    return float(np.polyfit(np.log(oms), np.log(cvs), 1)[0])


def boot_slope(oms, ivs, n=2000, seed=31102026):
    rng = np.random.default_rng(seed)
    sl = []
    for _ in range(n):
        cvs = []
        for iv in ivs:
            s = rng.choice(iv, len(iv))
            cvs.append(s.std(ddof=1) / s.mean())
        sl.append(slope(oms, cvs))
    return [float(np.percentile(sl, 2.5)), float(np.percentile(sl, 97.5))]


def p2():
    rows = []
    for om in (100, 400, 1600, 6400):
        n0 = [om, int(1.8 * om)]
        r0 = core.run_clock(om, n0, core.seed_of(3, om, 0), t_max=2050, max_ticks=10 ** 6, model_id=core.M_BR,
                            k=np.array([1.0, 1.8]), cmid=1.0, cdrop=-1.0)
        x = r0["samp"][int(50 / 0.05):, 0]
        sd = float(x.std())
        r = core.run_clock(om, r0["n_end"][:2], core.seed_of(3, om, 1), t_max=1e5, max_ticks=1000,
                           model_id=core.M_BR, k=np.array([1.0, 1.8]), cmid=1.0, cdrop=1.0 - sd)
        st = core.tick_stats(r["ticks"])
        rows.append(dict(omega=om, sd=sd, ticks=len(r["ticks"]), **st))
    oms = [r["omega"] for r in rows if r["ticks"] >= 200]
    cvs = [r["cv"] for r in rows if r["ticks"] >= 200]
    sl = slope(oms, cvs)
    n_filtered = sum(1 for r in rows if r["ticks"] >= 200 and r["ncoh"] >= 3)
    return dict(name="P2 Brusselator quasi-cycles", rows=rows, slope_all=sl, n_sizes_s1_filter=n_filtered,
                s1_fails=bool(not (-0.65 <= sl <= -0.35)), passed=bool(not (-0.65 <= sl <= -0.35)))


def p3():
    tg, X, cdet = core.det_cycle()
    rng = np.random.default_rng(31102026)
    dt = 0.05
    Tbar = 250.0
    # scripted: 40 normal periods of exactly Tbar, with stalls after ticks 5, 17, 30 and a censored final stall
    script = {5: (0.30, 9.0), 17: (0.72, 6.5), 30: (0.115, 12.0)}
    ticks, t = [0.0], 0.0
    for j in range(40):
        t += Tbar * script[j][1] if j in script else Tbar
        ticks.append(t)
    t_end = ticks[-1] + 7.0 * Tbar
    script[len(ticks) - 1] = (0.55, None)
    ng = int(t_end / dt) + 1
    tt = np.arange(ng) * dt
    last = np.searchsorted(ticks, tt, side="right") - 1
    ph = (tt - np.array(ticks)[last]) / Tbar
    c = cdet[((ph % 1.0) * len(cdet)).astype(int) % len(cdet)].astype(np.float32)
    want = []
    for j, (phs, _) in sorted(script.items()):
        a = ticks[j]
        je = int(np.ceil((a + phs * Tbar) / dt - 1e-9))
        b = ticks[j + 1] if j + 1 < len(ticks) else t_end
        c[je:int(b / dt)] = 5.0
        want.append(round((je * dt - a) / Tbar, 9))
    st = core.stalls(np.array(ticks), t_end, c, dt, Tbar, cdet)
    got = [round(s["phase"], 9) for s in st]
    ok = len(st) == len(script) and got == want and sum(s["censored"] for s in st) == 1
    _ = rng
    return dict(name="P3 scripted stalls", n_expected=len(script), n_found=len(st), phases_expected=want,
                phases_found=got, passed=bool(ok))


def harness():
    c0 = cpu()
    res = []
    for f in (p1, p3, h1, lambda: h2(5), lambda: h2(10), p2):
        t = cpu()
        r = f()
        r["cpu_s"] = cpu() - t
        res.append(r)
        json.dump(res, open(os.path.join(EV, "k3_harness.json"), "w"), indent=1, default=float)
    return dict(results=res, all_passed=all(r["passed"] for r in res), cpu_s=cpu() - c0)


def sizes(cap_left):
    tg, X, cdet = core.det_cycle()
    rows, ivs = [], {}
    c0 = cpu()
    for om in GRID:
        left = cap_left - (cpu() - c0)
        n0, N = core.n_start(om, X[:, 0])
        t = cpu()
        pr = core.run_clock(om, n0, core.seed_of(4, om, 0), t_max=1e9, max_ticks=10 ** 6, max_events=10 ** 6)
        cpu_ev = (cpu() - t) / max(pr["events"], 1)
        ev_rate = pr["events"] / pr["t_end"]
        proj = 1000 * core.T_DET * ev_rate * cpu_ev
        row = dict(omega=om, N=N, proj_cpu_s=proj, ev_per_time=ev_rate)
        if proj * 0.2 > left:
            row["skipped"] = "projection exceeds remaining cap"
            rows.append(row)
            continue
        t = cpu()
        r = core.run_clock(om, n0, core.seed_of(4, om, 1), t_max=4000 * core.T_DET, max_ticks=1000,
                           max_cpu=left)
        row["cpu_s"] = cpu() - t
        st = core.tick_stats(r["ticks"])
        ivs[om] = np.diff(r["ticks"])
        sl = core.stalls(r["ticks"], r["t_end"], r["samp"][:, 0], r["dt_s"], st["mean"], cdet) \
            if len(r["ticks"]) >= 2 else []
        periods = r["t_end"] / st["mean"] if st["n_int"] >= 2 else np.nan
        row.update(ticks=len(r["ticks"]), Tbar=st["mean"], cv=st["cv"], ncoh=st["ncoh"], stalls=len(sl),
                   stall_rate=len(sl) / periods if periods == periods else np.nan, periods=periods,
                   stall_phases=[s["phase"] for s in sl], stall_gaps=[s["gap"] for s in sl],
                   dvisits=r["dvisits"], events=r["events"], t_end=r["t_end"], aborted=r["aborted"])
        rows.append(row)
        json.dump(rows, open(os.path.join(EV, "k3_sizes.json"), "w"), indent=1, default=float)
        np.savez_compressed(os.path.join(EV, "k3_intervals.npz"), **{str(k): v for k, v in ivs.items()})
    return rows, ivs


def claims(rows, ivs):
    run = [r for r in rows if "ticks" in r]
    fit = [r for r in run if r["ticks"] >= 200 and r["ncoh"] >= 3]
    out = {}
    if len(fit) >= 3:
        oms = [r["omega"] for r in fit]
        sl = slope(oms, [r["cv"] for r in fit])
        ci = boot_slope(oms, [ivs[o] for o in oms])
        out["S1"] = dict(sizes=oms, slope=sl, boot95=ci,
                         verdict="holds" if -0.65 <= sl <= -0.35 else "killed")
    else:
        out["S1"] = dict(sizes=[r["omega"] for r in fit], verdict="underdetermined")
    om_star = [r["omega"] for r in run if r["ncoh"] >= 10]
    out["S2"] = dict(omega_star=om_star[0] if om_star else None)
    st = [r for r in run if r["stalls"] > 0]
    if len(st) < 2:
        out["S3"] = dict(verdict="underdetermined", sizes=[r["omega"] for r in st])
    else:
        bad = []
        for a, b in zip(st, st[1:]):
            se = np.hypot(np.sqrt(a["stalls"]) / a["periods"], np.sqrt(b["stalls"]) / b["periods"])
            if b["stall_rate"] - a["stall_rate"] > 2 * se:
                bad.append([a["omega"], b["omega"]])
        v = "killed" if bad else ("holds" if st[-1]["stall_rate"] < st[0]["stall_rate"] else "not shown")
        out["S3"] = dict(verdict=v, rates={r["omega"]: r["stall_rate"] for r in st}, violations=bad)
    best = max(run, key=lambda r: r["stalls"]) if run else None
    if best and best["stalls"] >= 50:
        ph = np.array([p for p in best["stall_phases"] if p == p]) % 1.0
        obs = np.bincount(np.minimum((ph * 5).astype(int), 4), minlength=5)
        p = float(chisquare(obs).pvalue)
        out["S4"] = dict(omega=best["omega"], n=int(len(ph)), bins=obs.tolist(), p=p,
                         verdict="phase-structured" if p < 0.05 else "killed (part 3)")
    else:
        out["S4"] = dict(verdict="underdetermined", max_stalls=best["stalls"] if best else 0)
    return out


if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    c0 = cpu()
    if "harness" in sys.argv:
        h = harness()
        json.dump(h, open(os.path.join(EV, "k3_harness.json"), "w"), indent=1, default=float)
        print("harness all_passed", h["all_passed"], "cpu", h["cpu_s"], flush=True)
    if "sizes" in sys.argv:
        used = json.load(open(os.path.join(EV, "k3_harness.json")))["cpu_s"]
        rows, ivs = sizes(CAP - used)
        cl = claims(rows, ivs)
        json.dump(cl, open(os.path.join(EV, "k3_claims.json"), "w"), indent=1, default=float)
        print(json.dumps(cl, default=float)[:1500], flush=True)
