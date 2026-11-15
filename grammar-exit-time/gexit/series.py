"""Series runner: pilot, burn-in feasibility, budget and grid extension (SPEC §3, §4, §6)."""
import math
import time

import numpy as np

from . import sim, stats

N_FULL, N_RED = 1000, 300
PILOT_EXITS, PILOT_ATTEMPTS, PILOT_CPU = 16, 2_000_000, 360.0
BATCH_TARGET_CPU = 20.0
MAX_BATCH_RUNS = 250


def t_proj(fitted, om):
    """SPEC §4: projected mean used for the cap before 10 exits are recorded at a size."""
    if not fitted:
        return 1000.0
    if len(fitted) == 1:
        o, T = fitted[-1]
        return 3.0 * T * math.exp(3.0 * (om - o))
    (o1, T1), (o2, T2) = fitted[-2], fitted[-1]
    lnT = math.log(T2) + (math.log(T2) - math.log(T1)) / (o2 - o1) * (om - o2)
    return 3.0 * math.exp(lnT)


def cost_proj(costs, om):
    """SPEC §6 rule 1: log-linear extrapolation in Omega of CPU-s per exit, floored."""
    (o1, c1), (o2, c2) = costs[-2], costs[-1]
    proj = c2 * math.exp((math.log(c2) - math.log(c1)) / (o2 - o1) * (om - o2))
    return max(proj, c2 * om / o2)


class Arm:
    def __init__(self, name, mdl, n0_fn, target, t_burn, ta_fn=None, tb_fn=None, k=None):
        self.name, self.mdl, self.n0_fn, self.target, self.t_burn = name, mdl, n0_fn, target, t_burn
        self.ta_fn = ta_fn or (lambda om: 0)
        self.tb_fn = tb_fn or (lambda om: 0)
        self.k = k

    def task(self, om, cap, nruns, seed, max_attempts=0, max_cpu=0.0):
        t = dict(model=self.mdl, omega=om, n0=np.asarray(self.n0_fn(om), np.int64), target=self.target,
                 ta=int(self.ta_fn(om)), tb=int(self.tb_fn(om)), t_burn=self.t_burn, cap=cap, nruns=nruns,
                 seed=seed, max_attempts=max_attempts, max_cpu=max_cpu)
        if self.k is not None:
            t["k"] = self.k
        return t


class Acc:
    """Accumulated runs of one arm at one size."""

    def __init__(self):
        self.time, self.cens, self.restarts, self.events, self.secD, self.cap = [], [], [], [], [], []
        self.cpu = 0.0
        self.attempts = 0
        self.failed_events = 0.0
        self.all_events = 0.0
        self.batches = 0
        self.aborted = 0

    def add(self, r, cap):
        self.time += r["time"].tolist()
        self.cens += r["cens"].tolist()
        self.restarts += r["restarts"].tolist()
        self.events += r["events"].tolist()
        self.secD += r["secD"].tolist()
        self.cap += [cap] * len(r["time"])
        self.cpu += r["cpu"]
        self.attempts += r["attempts"]
        self.failed_events += r["failed_events"]
        self.all_events += r["all_events"]
        self.batches += 1
        self.aborted = max(self.aborted, r["aborted"])

    @property
    def exits(self):
        return int(len(self.cens) - sum(self.cens))

    def mle(self):
        if self.exits == 0:
            return math.inf
        return float(np.sum(self.time) / self.exits)

    def record(self):
        return dict(time=self.time, cens=self.cens, restarts=self.restarts, events=self.events,
                    secD=self.secD, cap=self.cap, cpu=self.cpu, attempts=self.attempts,
                    failed_events=self.failed_events, all_events=self.all_events, batches=self.batches)


def run_series(name, arms, grid, budget, cap_mult=10.0, workers=4, log=print, fixed=False,
               n_full=N_FULL, n_red=N_RED, stop_after_reduced=2):
    """Run a series over grid with the SPEC §6 extension rule.  fixed=True runs every
    size at n_full exits with no budget rule (planted failures)."""
    spent = 0.0
    sizes = []
    fitted = {a.name: [] for a in arms}  # (Omega, T_hat) of fitted sizes, per arm
    costs = []  # (Omega, CPU-s per exit, summed over arms) of fitted sizes
    reduced = 0
    stop_reason = "grid exhausted"
    for om in grid:
        t0 = time.time()
        rec = dict(Omega=om, arms={})
        if not fixed and len(costs) >= 2:
            proj = cost_proj(costs, om)
            rec["projected_cpu_per_exit"] = proj
            if spent + n_red * proj > budget:
                stop_reason = "projection: spent %.0f + 300 x %.3g s > budget %.0f s" % (spent, proj, budget)
                log("[%s] stop before Omega=%s: %s" % (name, om, stop_reason))
                break
        tp = {a.name: t_proj(fitted[a.name], om) for a in arms}
        rec["T_proj"] = tp
        acc = {a.name: Acc() for a in arms}
        # ---- pilot: 4 batches of 4 runs per arm, attempts and CPU split across them
        tasks, keys = [], []
        for a in arms:
            cap = cap_mult * tp[a.name]
            for b in range(4):
                tasks.append(a.task(om, cap, PILOT_EXITS // 4, sim.seed_for(name, a.name, om, "pilot", b),
                                    max_attempts=PILOT_ATTEMPTS // 4,
                                    max_cpu=0.0 if fixed else PILOT_CPU / 4 / len(arms)))
                keys.append((a.name, cap))
        for (an, cap), r in zip(keys, sim.map_batches(tasks)):
            acc[an].add(r, cap)
        pilot_cpu = sum(acc[a.name].cpu for a in arms)
        spent += pilot_cpu
        rec["pilot"] = {a.name: dict(exits=acc[a.name].exits, cpu=acc[a.name].cpu, attempts=acc[a.name].attempts,
                                     failed_frac=(acc[a.name].failed_events / acc[a.name].all_events
                                                  if acc[a.name].all_events else 0.0),
                                     aborted=acc[a.name].aborted) for a in arms}
        short = [a.name for a in arms if acc[a.name].exits < PILOT_EXITS]
        if short:
            ff = max(rec["pilot"][an]["failed_frac"] for an in short)
            if ff > 0.5:
                rec["status"] = "burn-in infeasible"
                rec["acceptance"] = {a.name: (acc[a.name].exits / acc[a.name].attempts if acc[a.name].attempts else 0)
                                     for a in arms}
                rec["arms"] = {a.name: acc[a.name].record() for a in arms}
                rec["cpu"] = pilot_cpu
                sizes.append(rec)
                log("[%s] Omega=%s burn-in infeasible (acceptance %s), skipped" % (name, om, rec["acceptance"]))
                continue
            rec["status"] = "pilot only (budget-limited)"
            rec["arms"] = {a.name: acc[a.name].record() for a in arms}
            rec["cpu"] = pilot_cpu
            sizes.append(rec)
            stop_reason = "pilot budget-limited at Omega=%s" % om
            log("[%s] Omega=%s pilot budget-limited; series stops" % (name, om))
            break
        c = sum(acc[a.name].cpu / acc[a.name].exits for a in arms)
        rec["pilot_cpu_per_exit"] = c
        spent_before = spent - pilot_cpu
        if fixed:
            n = n_full
        elif spent_before + n_full * c <= budget:
            n = n_full
        elif spent_before + n_red * c <= budget:
            n = n_red
        else:
            rec["status"] = "pilot only (budget-limited)"
            rec["arms"] = {a.name: acc[a.name].record() for a in arms}
            rec["cpu"] = pilot_cpu
            sizes.append(rec)
            stop_reason = "no production count fits at Omega=%s (c=%.3g s/exit)" % (om, c)
            log("[%s] Omega=%s: %s" % (name, om, stop_reason))
            break
        rec["n_target"] = n
        # ---- production
        while True:
            need = {a.name: n - acc[a.name].exits for a in arms}
            if all(v <= 0 for v in need.values()):
                break
            tasks, keys = [], []
            for a in arms:
                if need[a.name] <= 0:
                    continue
                Tr = acc[a.name].mle() if acc[a.name].exits >= 10 else 0.0
                cap = cap_mult * max(tp[a.name], Tr)
                ca = acc[a.name].cpu / max(acc[a.name].exits, 1)
                rpb = int(min(MAX_BATCH_RUNS, max(1, round(BATCH_TARGET_CPU / max(ca, 1e-9)))))
                nb = min(4 * workers, math.ceil(need[a.name] / rpb))
                rpb = math.ceil(need[a.name] / nb)
                for b in range(nb):
                    bi = acc[a.name].batches + b
                    tasks.append(a.task(om, cap, rpb, sim.seed_for(name, a.name, om, "prod", bi)))
                    keys.append((a.name, cap))
            res = sim.map_batches(tasks)
            for (an, cap), r in zip(keys, res):
                acc[an].add(r, cap)
                spent += r["cpu"]
        rec["status"] = "fitted"
        rec["arms"] = {a.name: acc[a.name].record() for a in arms}
        rec["cpu"] = sum(acc[a.name].cpu for a in arms)
        rec["wall"] = time.time() - t0
        sizes.append(rec)
        for a in arms:
            fitted[a.name].append((om, acc[a.name].mle()))
        costs.append((om, sum(acc[a.name].cpu / acc[a.name].exits for a in arms)))
        msg = ", ".join("%s T=%.4g d=%d cens=%d" % (a.name, acc[a.name].mle(), acc[a.name].exits, sum(acc[a.name].cens))
                        for a in arms)
        log("[%s] Omega=%s n=%d %s cpu=%.0fs spent=%.0f/%.0f wall=%.0fs" % (name, om, n, msg, rec["cpu"], spent, budget,
                                                                           rec["wall"]))
        if n == n_red:
            reduced += 1
            if reduced >= stop_after_reduced and not fixed:
                stop_reason = "second reduced size reached at Omega=%s" % om
                log("[%s] %s" % (name, stop_reason))
                break
    return dict(name=name, budget=budget, spent=spent, stop_reason=stop_reason, sizes=sizes)


def fitted_sizes(series, arm):
    """(Omega, times, cens) of the fitted sizes of an arm."""
    out = []
    for s in series["sizes"]:
        if s.get("status") == "fitted":
            r = s["arms"][arm]
            out.append((s["Omega"], np.asarray(r["time"]), np.asarray(r["cens"], bool)))
    return out


def summarize_series(series, arm, B=2000, seed=0):
    rows = []
    for s in series["sizes"]:
        r = s["arms"].get(arm)
        row = dict(Omega=s["Omega"], status=s["status"])
        if r is not None and len(r["time"]):
            row.update(stats.summarize(r["time"], r["cens"], B=B, rng=sim.seed_for("boot", series["name"], arm,
                                                                                     s["Omega"]) % 2**32))
            row["restarts"] = int(np.sum(r["restarts"]))
            row["attempts"] = r["attempts"]
            row["acceptance"] = (len(r["time"]) / r["attempts"]) if r["attempts"] else None
            row["cpu"] = r["cpu"]
            row["events"] = float(np.sum(r["events"]))
            row["secD_frac"] = float(np.mean(r["secD"]))
            row["cap_min"] = float(np.min(r["cap"]))
        rows.append(row)
    return rows
