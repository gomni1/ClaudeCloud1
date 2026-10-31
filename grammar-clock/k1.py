"""K1: where clocks live (SPEC K1).  PR 4's M2 code unchanged + a per-draw 120 CPU-s cap.

Each batch of draws runs in a forked child; before each draw (and each phase of a second-pass draw)
the child sets RLIMIT_CPU to its CPU so far + 120 s.  A draw killed at the cap is recorded as
'unresolved: cpu cap'.  Usage: taskset -c 2,3 python k1.py
"""
import gzip
import json
import os
import resource
import signal
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "grammar-instability"))
from ginst import integ, m2, m4, model  # noqa: E402

EV = os.path.join(HERE, "evidence")
CAP_DRAW = 120
CAP_VERIFY = 600
CAP_TOTAL = float(os.environ.get("K1_CAP", 2 * 3600))
WORKERS = 2
CHUNK = 50
SEED_B = 31102026
LOG = os.path.join(EV, "k1_log.txt")


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def conv(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, complex):
        return [o.real, o.imag]
    raise TypeError(type(o))


def draw_b(i):
    """K1b moderate-rate box: as PR 4's draw_params but seed 31102026, log10 k ~ U(-1, 1), tot only."""
    rng = np.random.default_rng([SEED_B, i])
    level = "open" if i % 2 == 0 else "closed"
    k = 10.0 ** rng.uniform(-1, 1, 11)
    m = int(rng.integers(2, 13))
    kr, kc = (int(v) for v in rng.integers(1, m + 1, 2))
    T = float(10.0 ** rng.uniform(-1, 2))
    return dict(i=i, level=level, den="tot", k=k.tolist(), m=m, kr=kr, kc=kc, T=T, law="TH")


def span(d):
    k = m2.rates_in_use(d)
    return float(np.log10(k.max() / k.min()))


def setcap(sec):
    used = resource.getrusage(resource.RUSAGE_SELF)
    used = used.ru_utime + used.ru_stime
    lim = int(used + sec) + 1
    resource.setrlimit(resource.RLIMIT_CPU, (lim, resource.RLIM_INFINITY))


def verify(d, run):
    """PR 4's M4 verification of a periodic end state."""
    setcap(CAP_VERIFY)
    par = m2.par_of(d)
    c = run["class"]
    v = m4.verify_cycle(par, np.array(c["point"]), c["period"])
    triv = 2 if d["level"] == "closed" else 1
    mods = np.array(v["moduli"])
    order = np.argsort(np.abs(mods - 1.0))
    nontriv = np.sort(mods[order[triv:]])[::-1]
    v["nontrivial"] = nontriv.tolist()
    v["verified"] = bool(v["agree"] and np.all(nontriv < 1 - 1e-6))
    # C range over one period
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t, z: model.f_np(z, par), (0, v["periods"]["Radau"]["period"]), np.array(c["point"]),
                    method="Radau", rtol=1e-10, atol=1e-14, jac=lambda t, z: model.J_np(z, par), dense_output=True)
    zz = sol.sol(np.linspace(0, v["periods"]["Radau"]["period"], 4000))
    v["C_range"] = [float(zz[0].min()), float(zz[0].max())]
    return v


def slim(rec):
    out = {k: rec[k] for k in ("i", "level", "den", "m", "kr", "kc", "T", "k", "n_bal", "n_stable", "kinds",
                                "n_balance", "n_periodic", "n_unresolved", "t_end", "cpu") if k in rec}
    if "runs" in rec:
        out["runs"] = [dict(cls=r["class"], end=r.get("end")) for r in rec["runs"]]
    return out


def do_task(task):
    sub, d = task["sub"], task["d"]
    t0 = time.process_time()
    if sub in ("K1a", "K1b"):
        m2.SEED = SEED_B if sub == "K1b" else 30102026
        setcap(CAP_DRAW)
        rec = slim(m2.process(d))
        rec["sub"], rec["span"] = sub, span(d)
        rec["verify"] = [verify(d, {"class": r["cls"]}) for r in rec.get("runs", []) if r["cls"]["kind"] == "periodic"]
        rec["cpu_task"] = time.process_time() - t0
        return rec
    # K1c: second pass from unresolved end states for 10 t_end
    m2.SEED = SEED_B if task["src"] == "K1b" else 30102026
    runs = task.get("runs")
    if runs is None:  # PR 4 draw: regenerate end states (deterministic)
        setcap(CAP_DRAW)
        runs = [dict(cls=r["class"], end=r.get("end")) for r in m2.process(d).get("runs", [])]
    par = m2.par_of(d)
    bals = model.classify_balances(par)
    allb = [r["b"] for r in bals]
    stable = [r["b"] for r in bals if r["stable"]]
    t_end = 1e3 / float(np.min(m2.rates_in_use(d)))
    res = []
    for r in runs:
        if r["cls"]["kind"] != "unresolved" or r["end"] is None:
            continue
        setcap(CAP_DRAW)
        out = integ.run_starts(par, np.array([r["end"]]), allb, stable, 10.0 * t_end)[0]
        item = dict(first=r["cls"], second=out["class"], end2=out["end"])
        if out["class"]["kind"] == "periodic":
            item["verify"] = verify(d, out)
        res.append(item)
    return dict(sub="K1c", src=task["src"], i=d["i"], level=d["level"], den=d["den"], m=d["m"], kr=d["kr"],
                kc=d["kc"], T=d["T"], k=d["k"], span=span(d), second=res, cpu_task=time.process_time() - t0)


def child(tasks, path):
    signal.signal(signal.SIGXCPU, signal.SIG_DFL)
    with open(path, "w") as f:
        for t in tasks:
            try:
                rec = do_task(t)
            except Exception as e:  # noqa: BLE001
                rec = dict(sub=t["sub"], i=t["d"]["i"], level=t["d"]["level"], error=repr(e))
            f.write(json.dumps(rec, default=conv) + "\n")
            f.flush()
    os._exit(0)


def run_tasks(tasks, out, state):
    """Run tasks in forked children (2 at a time).  Returns False if the CPU cap stopped it."""
    queue = [tasks[i:i + CHUNK] for i in range(0, len(tasks), CHUNK)]
    live = {}
    nfile = [0]

    def launch(ch):
        p = os.path.join(EV, ".k1_tmp_%d.jsonl" % nfile[0])
        nfile[0] += 1
        pid = os.fork()
        if pid == 0:
            child(ch, p)
        live[pid] = (ch, p)

    while queue or live:
        while queue and len(live) < WORKERS and state["cpu"] < CAP_TOTAL:
            launch(queue.pop(0))
        if not live:
            break
        pid, st, ru = os.wait4(-1, 0)
        ch, p = live.pop(pid)
        state["cpu"] += ru.ru_utime + ru.ru_stime
        lines = open(p).read().splitlines() if os.path.exists(p) else []
        os.remove(p) if os.path.exists(p) else None
        for ln in lines:
            out.write(ln + "\n")
            state["done"] += 1
        if len(lines) < len(ch):  # killed: the next task hit the cap
            t = ch[len(lines)]
            sig = os.WTERMSIG(st) if os.WIFSIGNALED(st) else None
            out.write(json.dumps(dict(sub=t["sub"], src=t.get("src"), i=t["d"]["i"], level=t["d"]["level"],
                                      den=t["d"]["den"], capped=True, signal=sig,
                                      kinds=["unresolved: cpu cap"]), default=conv) + "\n")
            state["capped"] += 1
            state["done"] += 1
            if ch[len(lines) + 1:]:
                queue.insert(0, ch[len(lines) + 1:])
        out.flush()
        if state["done"] % 2000 < CHUNK:
            log("done=%d cpu=%.0f capped=%d" % (state["done"], state["cpu"], state["capped"]))
    return state["cpu"] < CAP_TOTAL and not queue


def main():
    os.makedirs(EV, exist_ok=True)
    m2.process(m2.draw_params(3))  # numba warm-up in the parent (inherited by forks)
    state = dict(cpu=0.0, done=0, capped=0)
    t0 = time.time()
    summary = dict(sub={})
    path = os.path.join(EV, "k1_records.jsonl")
    with open(path, "w") as out:
        for sub, tasks in (("K1b", [dict(sub="K1b", d=draw_b(i)) for i in range(40000)]),
                           ("K1a", [dict(sub="K1a", d=m2.draw_params(i)) for i in range(41100, 100000)
                                    if i % 4 in (2, 3)])):
            c0, n0 = state["cpu"], state["done"]
            ok = run_tasks(tasks, out, state)
            summary["sub"][sub] = dict(complete=ok, tasks=len(tasks), done=state["done"] - n0, cpu=state["cpu"] - c0)
            log("%s finished complete=%s cpu=%.0f" % (sub, ok, state["cpu"]))
            if not ok:
                break
    # K1c task list
    new = [json.loads(l) for l in open(path)]
    pr4 = []
    with gzip.open(os.path.join(HERE, "..", "grammar-instability", "evidence", "m2_draws.jsonl.gz"), "rt") as f:
        for l in f:
            r = json.loads(l)
            if r["n_unresolved"]:
                pr4.append(r["i"])
    pr4_closed = [i for i in pr4 if i % 2 == 1]
    pr4_open = [i for i in pr4 if i % 2 == 0]
    newu = [r for r in new if r.get("n_unresolved") and "runs" in r]
    t_c = [dict(sub="K1c", src="PR4", d=m2.draw_params(i)) for i in pr4_closed]
    t_c += [dict(sub="K1c", src="K1a", d=m2.draw_params(r["i"]), runs=r["runs"]) for r in newu
            if r["sub"] == "K1a" and r["level"] == "closed"]
    t_b = [dict(sub="K1c", src="K1b", d=draw_b(r["i"]), runs=r["runs"]) for r in newu if r["sub"] == "K1b"]
    t_b.sort(key=lambda t: t["d"]["level"] != "closed")
    t_o = [dict(sub="K1c", src="PR4", d=m2.draw_params(i)) for i in pr4_open]
    t_o += [dict(sub="K1c", src="K1a", d=m2.draw_params(r["i"]), runs=r["runs"]) for r in newu
            if r["sub"] == "K1a" and r["level"] == "open"]
    perm = np.random.default_rng(SEED_B).permutation(len(t_o))
    t_o = [t_o[j] for j in perm]
    summary["K1c_queue"] = dict(closed=len(t_c), K1b=len(t_b), open=len(t_o))
    c0, n0 = state["cpu"], state["done"]
    with open(os.path.join(EV, "k1c_records.jsonl"), "w") as out:
        ok = run_tasks(t_c + t_b + t_o, out, state) if state["cpu"] < CAP_TOTAL else False
    summary["sub"]["K1c"] = dict(complete=ok, done=state["done"] - n0, cpu=state["cpu"] - c0)
    summary.update(cpu_total=state["cpu"], capped=state["capped"], wall=time.time() - t0)
    json.dump(summary, open(os.path.join(EV, "k1_summary.json"), "w"), indent=1)
    log("K1 finished: %s" % json.dumps(summary))


if __name__ == "__main__":
    main()
