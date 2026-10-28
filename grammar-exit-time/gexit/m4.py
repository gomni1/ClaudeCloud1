"""M4 driver: all gMAM items and initial paths (SPEC §5, M4)."""
import json
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from . import gmam, model

B2 = np.array([1.0, 2.0, 1.0, 0.5])
B3 = np.array([1.0, 3.0, 1.0, 0.5])
B4 = np.array([1.0, 4.0, 1.0, 0.5])
BMA = model.balance_ma()

FREE_D = [False, True, False, True]   # end in {c = l = 0}: v, p free
FREE_D0 = [False, True, True, True]   # end in {c = 0}: v, l, p free
FIXED = [False] * 4


def project(x, target):
    e = np.array(x, float)
    e[0] = 0.0
    if target == "D":
        e[2] = 0.0
    return e


def polyline(points, n=200):
    pts = np.asarray(points, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)]) / seg.sum()
    u = np.linspace(0, 1, n + 1)
    return np.column_stack([np.interp(u, s, pts[:, j]) for j in range(4)])


def items():
    out = []
    for target, free in (("D", FREE_D), ("D0", FREE_D0)):
        out.append(dict(name="MA_W_%s" % target, law="MA", start=BMA, end=project(BMA, target), free=free,
                        init="straight", init_pts=[BMA, project(BMA, target)]))
        for b, other, lab in ((B2, B4, "v2"), (B4, B2, "v4")):
            out.append(dict(name="TH_W_%s_%s" % (target, lab), law="TH", start=b, end=project(b, target), free=free,
                            init="straight", init_pts=[b, project(b, target)]))
            out.append(dict(name="TH_W_%s_%s" % (target, lab), law="TH", start=b, end=project(other, target),
                            free=free, init="via other balance", init_pts=[b, B3, other, project(other, target)]))
    out.append(dict(name="TH_W_Sup", law="TH", start=B2, end=B3, free=FIXED, init="straight", init_pts=[B2, B3]))
    out.append(dict(name="TH_W_Sdown", law="TH", start=B4, end=B3, free=FIXED, init="straight", init_pts=[B4, B3]))
    return out


LOGFILE = None


def run_item(it):
    t0 = time.process_time()
    log = []

    def logger(msg):
        log.append(msg)
        if LOGFILE:
            with open(LOGFILE, "a") as f:
                f.write("%s %s cpu=%.0fs\n" % (time.strftime("%H:%M:%S"), msg, time.process_time() - t0))

    net = gmam.grammar(it["law"])
    phi0 = polyline(it["init_pts"], 50)
    r = gmam.gmam(net, it["start"], it["end"], it["free"], phi_init=phi0, log=logger,
                  label="%s/%s" % (it["name"], it["init"]))
    r.update(name=it["name"], law=it["law"], init=it["init"], start=list(it["start"]), log=log,
             cpu=time.process_time() - t0)
    return r


def run_all(path_out, workers=3, logfile=None):
    global LOGFILE
    LOGFILE = logfile
    its = items()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(run_item, its))
    json.dump(res, open(path_out, "w"), indent=1)
    return res


def collect(res):
    """Per item: the smaller converged value over initial paths."""
    best = {}
    for r in res:
        if not r.get("converged"):
            continue
        b = best.get(r["name"])
        if b is None or r["W"] < b["W"]:
            best[r["name"]] = r
    out = {}
    for r in res:
        n = r["name"]
        out.setdefault(n, dict(runs=[]))["runs"].append(dict(init=r["init"], converged=r.get("converged"),
                                                            W=r.get("W"), N=r.get("N"),
                                                            reason=r.get("reason"),
                                                            end=r["path"][-1] if r.get("path") else None))
    for n in out:
        out[n]["W"] = best[n]["W"] if n in best else None
        out[n]["converged"] = n in best
        out[n]["init"] = best[n]["init"] if n in best else None
    return out
