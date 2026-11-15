"""Checks N0-N4 of SPEC.md (SHA-256 cc7ac93a...eb09) with revision R1 (RUN.md).

SANDBOX/DRAFT. Rate vector order follows grammar-instability/ginst/model.py:
k = [k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12]   (indices 0..10)
State y = (C, V, L, P).
Usage: python -I checks.py [N0|N1|N2|N3|N4|all]
"""
import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

RTOL, ATOL = 1e-9, 1e-12
I1, I2, I3, I5, I6, I7, I8, I9, I10, I11, I12 = range(11)


def F_tail(x, m, j):
    """Pr[Bin(m, x) >= j]."""
    if j <= 0:
        return 1.0
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0 if j <= m else 0.0
    return sum(math.comb(m, i) * x ** i * (1.0 - x) ** (m - i) for i in range(j, m + 1))


def make_rhs(k, law, m=2, kr=1, kc=1, o=1):
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = k
    lossC = k1 + k2 + k7
    rep = 2.0 * lossC + 1.0

    def f(t, y):
        C, V, L, P = y
        T = C + V + L + P
        x = C / T if T > 0 else 0.0
        create = 0.0
        if law == "TH":
            rho = k3 * F_tail(x, m, kr)
            rel = k11 * C * F_tail(x, m, kc)
        elif law == "MA":
            rho, rel = k3 * C, 0.0
        elif law == "SA":
            rho, rel = k3 * C * C, 0.0
        elif law == "PLANT_C2":  # declared planted: creation without using Void
            rho, rel, create = 0.0, 0.0, k3 * C * C
        elif law == "PLANT_REP":  # R1 planted: replication faster than all Contact losses
            rho, rel, create = 0.0, 0.0, rep * C
        else:
            raise ValueError(law)
        g = (k10 + rho) * V - rel
        return [-lossC * C + k6 * L + g + create,
                k2 * C + k5 * L + k8 * P - g + o * k12,
                k1 * C - (k5 + k6) * L,
                k7 * C - (k8 + o * k9) * P]
    return f


def exit_times(k):
    """w with w^T (-A0) = 1^T, A0 = open-level compartmental matrix with rho = 0 (columns = from)."""
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = k
    A = np.zeros((4, 4))
    A[:, 0] = [-(k1 + k2 + k7), k2, k1, k7]
    A[:, 1] = [k10, -k10, 0, 0]
    A[:, 2] = [k6, k5, -(k5 + k6), 0]
    A[:, 3] = [0, k8, 0, -(k8 + k9)]
    return np.linalg.solve(-A.T, np.ones(4))


# ---------------- N0: harness against PR 7's clocks ----------------
def draw_b(i):
    rng = np.random.default_rng([31102026, i])
    level = "open" if i % 2 == 0 else "closed"
    k = 10.0 ** rng.uniform(-1, 1, 11)
    m = int(rng.integers(2, 13))
    kr, kc = (int(v) for v in rng.integers(1, m + 1, 2))
    T = float(10.0 ** rng.uniform(-1, 2))
    return dict(i=i, level=level, k=k, m=m, kr=kr, kc=kc, T=T)


def period_of(sol_t, C):
    """Mean interval between upward crossings of the mean in the second half."""
    h = len(C) // 2
    t, c = sol_t[h:], C[h:]
    mu = c.mean()
    up = np.nonzero((c[:-1] < mu) & (c[1:] >= mu))[0]
    if len(up) < 3:
        return float("nan"), float(c.max() - c.min()), float(mu)
    tc = t[up] + (mu - c[up]) / (c[up + 1] - c[up]) * (t[up + 1] - t[up])
    return float(np.diff(tc).mean()), float(c.max() - c.min()), float(mu)


def run_clock(d, k=None, t_end=600.0, y0=None):
    k = d["k"] if k is None else k
    o = 1 if d["level"] == "open" else 0
    f = make_rhs(k, "TH", d["m"], d["kr"], d["kc"], o)
    if y0 is None:
        y0 = np.full(4, d["T"] / 4.0) if o == 0 else np.array([0.5, 0.5, 0.5, 0.5])
    tt = np.linspace(0, t_end, 60001)
    s = solve_ivp(f, (0, t_end), y0, method="LSODA", rtol=RTOL, atol=ATOL, t_eval=tt)
    return s


def N0():
    out = {}
    for i, target in ((19387, 6.352), (33538, 4.844)):
        d = draw_b(i)
        s = run_clock(d)
        per, amp, mu = period_of(s.t, s.y[0])
        h = len(s.t) // 2
        out[i] = dict(level=d["level"], m=d["m"], kr=d["kr"], kc=d["kc"], T=d["T"], period=per,
                      Cmin=float(s.y[0][h:].min()), Cmax=float(s.y[0][h:].max()), target=target,
                      pass_=bool(abs(per - target) <= 0.01))
    out["pass"] = all(v["pass_"] for kk, v in out.items() if kk != "pass")
    return out


# ---------------- N1: bound under any recruitment law ----------------
def n1_draw(i, law):
    rng = np.random.default_rng([6112026, 1, i])
    k = 10.0 ** rng.uniform(-2, 2, 11)
    k[I11] = 0.0
    m = int(rng.integers(2, 13))
    kr = int(rng.integers(1, m + 1))
    starts = 10.0 ** rng.uniform(-2, 2, size=(4, 1)) * rng.dirichlet(np.ones(4), size=4) * 4
    return k, m, kr, starts


def n1_one(args):
    i, law = args
    k, m, kr, starts = n1_draw(i, law)
    w = exit_times(k)
    wmax, wV = float(w.max()), float(w[1])
    rates = np.delete(k, [I11])
    t_end = min(200.0 / rates.min(), 2e5)
    f = make_rhs(k, law, m, kr, 1, 1)
    res = []
    for y0 in starts:
        B = max(float(w @ y0), wmax * wV * k[I12])
        tt = np.linspace(0, t_end, 2001)
        try:
            s = solve_ivp(f, (0, t_end), y0, method="LSODA", rtol=RTOL, atol=ATOL, t_eval=tt)
            ok = s.success and s.y.shape[1] == len(tt) and np.all(np.isfinite(s.y))
        except Exception:
            ok = False
            s = None
        if not ok:
            res.append(dict(done=False, viol=None))
            continue
        wy = w @ s.y
        viol = bool(np.any(wy > B * (1 + 1e-6) + 1e-9))
        h = len(tt) // 2
        pin = (k[I8] + k[I9]) * k[I12] / (k[I7] * k[I9])
        res.append(dict(done=True, viol=viol, ratio_max=float(wy.max() / B),
                        meanC_over_pin=float(s.y[0][h:].mean() / pin),
                        relswing=float((s.y[0][h:].max() - s.y[0][h:].min()) / max(s.y[0][h:].mean(), 1e-300))))
    return dict(i=i, law=law, m=m, kr=kr, t_end=t_end, runs=res)


def N1(workers=8):
    laws = ["TH", "MA", "SA"]
    jobs = [(i, laws[i % 3]) for i in range(600)]
    planted = [(1000 + i, "PLANT_REP") for i in range(200)] + [(2000 + i, "PLANT_C2") for i in range(200)]
    with Pool(workers) as p:
        main = p.map(n1_one, jobs, chunksize=4)
        pl = p.map(n1_one, planted, chunksize=4)
    summ = {}
    for law in laws:
        rr = [r for d in main if d["law"] == law for r in d["runs"]]
        done = [r for r in rr if r["done"]]
        summ[law] = dict(runs=len(rr), completed=len(done), not_completed=len(rr) - len(done),
                         violations=sum(r["viol"] for r in done),
                         max_ratio=max(r["ratio_max"] for r in done),
                         cycling_runs=sum(r["relswing"] > 1e-3 for r in done),
                         meanC_over_pin_range=[min(r["meanC_over_pin"] for r in done),
                                               max(r["meanC_over_pin"] for r in done)])
    for law in ("PLANT_REP", "PLANT_C2"):
        ds = [d for d in pl if d["law"] == law]
        flagged = sum(any((not r["done"]) or r["viol"] for r in d["runs"]) for d in ds)
        summ[law] = dict(draws=len(ds), flagged=flagged, rate=flagged / len(ds))
    summ["kill"] = any(summ[l]["violations"] > 0 for l in laws)
    summ["planted_pass"] = summ["PLANT_REP"]["rate"] >= 0.95
    return summ


# ---------------- N2: no seeding, no Contact -> Void grows without bound ----------------
def N2():
    out = {}
    for law in ("TH", "MA"):
        errs = []
        for i in range(20):
            rng = np.random.default_rng([6112026, 2, i])
            k = 10.0 ** rng.uniform(-2, 2, 11)
            k[I11] = 0.0
            k[I10] = 0.0
            m = int(rng.integers(2, 13))
            kr = int(rng.integers(1, m + 1))
            V0 = float(10.0 ** rng.uniform(-2, 2))
            f = make_rhs(k, law, m, kr, 1, 1)
            s = solve_ivp(f, (0, 100.0), [0.0, V0, 0.0, 0.0], method="LSODA", rtol=RTOL, atol=ATOL)
            errs.append(abs(s.y[1, -1] - (V0 + 100 * k[I12])) / (V0 + 100 * k[I12]))
        out[law] = dict(max_rel_err=float(max(errs)), pass_=bool(max(errs) <= 1e-8))
    return out


# ---------------- N3: balance count ----------------
def roots_on_grid(fun, grid):
    vals = np.array([fun(z) for z in grid])
    roots = []
    for j in range(len(grid) - 1):
        a, b = vals[j], vals[j + 1]
        if a == 0.0:
            roots.append(float(grid[j]))
        elif a * b < 0:
            roots.append(brentq(fun, grid[j], grid[j + 1], xtol=1e-14 * abs(grid[j + 1]), rtol=1e-14))
    if vals[-1] == 0.0:
        roots.append(float(grid[-1]))
    return roots


def n3_draw(i, level):
    rng = np.random.default_rng([6112026, 3, 0 if level == "open" else 1, i])
    k = 10.0 ** rng.uniform(-2, 2, 11)
    k[I11] = 0.0
    m = int(rng.integers(2, 13))
    kr = int(rng.integers(1, m + 1))
    return k, m, kr


def n3_one(args):
    i, level = args
    k, m, kr = n3_draw(i, level)
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = k
    D = k2 + k7 + k1 * k5 / (k5 + k6)
    if level == "open":
        Cs = (k8 + k9) * k12 / (k7 * k9)
        Ls = k1 * Cs / (k5 + k6)
        Ps = k12 / k9
        s = Cs + Ls + Ps
        fun = lambda V: (k10 + k3 * F_tail(Cs / (s + V), m, kr)) * V - D * Cs  # noqa: E731
        grid = np.geomspace(1e-12 * s, 1e12 * s, 4000)
        r = roots_on_grid(fun, grid)
        bal = [dict(C=Cs, V=v, L=Ls, P=Ps) for v in r]
    else:
        c = 1 + k1 / (k5 + k6) + k7 / k8
        fun = lambda x: D * x - (k10 + k3 * F_tail(x, m, kr)) * (1 - c * x)  # noqa: E731
        grid = np.geomspace(1e-12, 1.0, 4000) / c
        r = roots_on_grid(fun, grid)
        bal = [dict(x=x) for x in r]
    return dict(i=i, level=level, m=m, kr=kr, k=k.tolist(), n=len(r), bal=bal)


def N3(workers=8):
    # planted
    pr = roots_on_grid(lambda x: (x - 0.2) * (x - 0.5) * (x - 0.8), np.geomspace(1e-12, 1.0, 4000))
    planted_ok = len(pr) == 3
    jobs = [(i, lv) for lv in ("open", "closed") for i in range(5000)]
    with Pool(workers) as p:
        res = p.map(n3_one, jobs, chunksize=50)
    summ = dict(planted_roots=pr, planted_pass=planted_ok)
    example = None
    for lv in ("open", "closed"):
        r1 = [d for d in res if d["level"] == lv and d["kr"] == 1]
        r2 = [d for d in res if d["level"] == lv and d["kr"] >= 2]
        cnt2 = {}
        for d in r2:
            cnt2[d["n"]] = cnt2.get(d["n"], 0) + 1
        summ[lv] = dict(kr1_draws=len(r1), kr1_not_one=sum(d["n"] != 1 for d in r1),
                        kr1_counts=sorted({d["n"] for d in r1}),
                        kr2_draws=len(r2), kr2_count_hist=cnt2,
                        kr2_share_three=sum(d["n"] == 3 for d in r2) / max(len(r2), 1))
        if lv == "open" and example is None:
            three = [d for d in r2 if d["n"] == 3]
            if three:
                example = min(three, key=lambda d: max(d["k"]) / min(v for v in d["k"] if v > 0))
    summ["example_open_three"] = example
    summ["kill"] = summ["open"]["kr1_not_one"] > 0 or summ["closed"]["kr1_not_one"] > 0
    return summ


def stability(k, m, kr, y, o=1):
    f = make_rhs(np.array(k), "TH", m, kr, 1, o)
    y = np.array(y, float)
    J = np.zeros((4, 4))
    for j in range(4):
        h = 1e-7 * max(abs(y[j]), 1e-8)
        yp, ym = y.copy(), y.copy()
        yp[j] += h
        ym[j] -= h
        J[:, j] = (np.array(f(0, yp)) - np.array(f(0, ym))) / (2 * h)
    return np.linalg.eigvals(J)


# ---------------- N4: lag ----------------
def N4():
    viol = 0
    worst = 0.0
    for i in range(300):
        rng = np.random.default_rng([6112026, 4, i])
        k = 10.0 ** rng.uniform(-2, 2, 11)
        k[I11] = 0.0
        k[I1] = 0.0
        k[I7] = 0.0
        m = int(rng.integers(2, 13))
        kr = int(rng.integers(1, m + 1))
        T = float(10.0 ** rng.uniform(-1, 2))
        C0 = T * float(rng.uniform(0.0, 1.0))
        f = make_rhs(k, "TH", m, kr, 1, 0)
        rates = np.delete(k, [I1, I7, I9, I11, I12])
        t_end = min(200.0 / rates.min(), 2e5)
        tt = np.linspace(0, t_end, 2001)
        s = solve_ivp(f, (0, t_end), [C0, T - C0, 0.0, 0.0], method="LSODA", rtol=RTOL, atol=ATOL, t_eval=tt)
        dC = np.array([f(0, s.y[:, j])[0] for j in range(s.y.shape[1])])
        sc = max(np.abs(dC).max(), 1e-300)
        z = dC / sc
        big = z[np.abs(z) > 1e-8]
        changes = int(np.sum(np.sign(big[1:]) != np.sign(big[:-1])))
        if changes > 0:
            viol += 1
        worst = max(worst, changes)
    out = dict(draws=300, draws_with_sign_change=viol, kill=viol > 0)
    # exploratory: which delayed route the moderate-rate clocks use (k11 = 0)
    expl = {}
    for i in (19387, 33538):
        d = draw_b(i)
        for idx, name in ((I1, "k1 (route through L)"), (I7, "k7 (route through P)")):
            rows = []
            for sc_ in (1.0, 0.3, 0.1, 0.03, 0.01):
                k = d["k"].copy()
                k[I11] = 0.0
                k[idx] *= sc_
                s = run_clock(d, k=k, t_end=1500.0)
                n = len(s.t)
                a1 = np.ptp(s.y[0][int(0.6 * n):int(0.8 * n)])
                a2 = np.ptp(s.y[0][int(0.8 * n):])
                mu = s.y[0][int(0.8 * n):].mean()
                per, _, _ = period_of(s.t, s.y[0])
                cyc = bool(a2 / mu > 1e-3 and a2 > 0.5 * a1)
                rows.append(dict(scale=sc_, cycle=cyc, rel_amp=float(a2 / mu), period=per if cyc else None))
            expl[f"{i} ({d['level']}) {name}"] = rows
    out["exploratory"] = expl
    return out


def conv(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, complex):
        return [o.real, o.imag]
    raise TypeError(type(o))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = ["N0", "N1", "N2", "N3", "N4"] if which == "all" else [which]
    for name in todo:
        t0 = time.time()
        r = globals()[name]()
        r["_seconds"] = round(time.time() - t0, 1)
        json.dump(r, open(f"result_{name}.json", "w"), indent=1, default=conv)
        print(name, json.dumps(r, default=conv)[:3000], flush=True)
        if name == "N0" and not r["pass"]:
            print("N0 failed: harness does not reproduce PR 7; stopping.")
            break
