"""Forward flux sampling of dissolution to D (SPEC §3), over csrc/ffs.c."""
import ctypes
import math
import os
import subprocess
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "csrc", "ffs.c")
LIB = os.path.join(ROOT, "build", "libffs.so")
MODELS = {"MA": 0, "TH": 1, "ID": 3}
_lib = None
_d = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
_i64 = np.ctypeslib.ndpointer(dtype=np.int64, flags="C_CONTIGUOUS")
_i32 = np.ctypeslib.ndpointer(dtype=np.int32, flags="C_CONTIGUOUS")


def lib():
    global _lib
    if _lib is None:
        os.makedirs(os.path.dirname(LIB), exist_ok=True)
        if not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
            subprocess.check_call(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, SRC, "-lm"])
        L = ctypes.CDLL(LIB)
        L.ffs_flux.restype = ctypes.c_int
        L.ffs_flux.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, ctypes.c_double, ctypes.c_int64,
                               ctypes.c_int64, ctypes.c_int, ctypes.c_uint64, ctypes.c_double, _i64, _d, _i64, _d, _i64]
        L.ffs_trials.restype = ctypes.c_int
        L.ffs_trials.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, ctypes.c_int, ctypes.c_int, ctypes.c_int64,
                                 ctypes.c_int64, ctypes.c_uint64, ctypes.c_int, _d, ctypes.c_int, _i32, _i64, _i32, _d,
                                 _d, _i32, _d]
        _lib = L
    return _lib


def interfaces(om, basin_mult=2.0, pf1=False):
    """SPEC §3: basin A = {M >= basin_mult*Om}; M0 = basin - ceil(2 sqrt Om); spacing max(1, ceil(M0/12)); last M = 0."""
    MA = int(round(basin_mult * om))
    M0 = MA - int(math.ceil(2 * math.sqrt(om)))
    d = max(1, int(math.ceil(M0 / 12)))
    Ms = [M0]
    while Ms[-1] - d > 0:
        Ms.append(Ms[-1] - d)
    Ms.append(0)
    return MA, Ms


def run_ffs(model, om, k, n0, t_burn, seed, path=None, ncross=1000, trials=1000, min_success=50, max_trials=20000,
            basin_mult=2.0, sample_every=10, max_flux_events=5e10):
    L = lib()
    k = np.ascontiguousarray(k, float)
    n0 = np.ascontiguousarray(n0, np.int64)
    MA, Ms = interfaces(om, basin_mult)
    pth = np.ascontiguousarray(path if path is not None else np.zeros((1, 4)), float)
    npth = len(pth) if path is not None else 0
    t0 = time.process_time()
    st = np.zeros((ncross, 4), np.int64)
    tt = np.zeros(1)
    rs = np.zeros(1, np.int64)
    ev = np.zeros(1)
    nd = np.zeros(1, np.int64)
    got = L.ffs_flux(MODELS[model], float(om), k, n0, float(t_burn), MA, Ms[0], ncross, seed, max_flux_events,
                     st, tt, rs, ev, nd)
    rec = dict(Omega=om, MA=MA, interfaces=Ms, flux_crossings=int(got), flux_time=float(tt[0]),
               flux_restarts=int(rs[0]), flux_events=float(ev[0]), flux_hitD=int(nd[0]))
    if got == 0:
        rec.update(ok=False, reason="no flux crossings", cpu=time.process_time() - t0)
        return rec
    rec["flux"] = got / tt[0]
    states = st[:got].copy()
    stages = []
    # reactive-path bookkeeping: per stage, arrays of (parent, maxv, dsum, dcnt) for stored successes
    tree = []
    logP = 0.0
    events = 0.0
    for i in range(len(Ms) - 1):
        oks, ends, pars, mv, ds, dc = [], [], [], [], [], []
        n_tr = 0
        while True:
            ntr = trials
            ok = np.zeros(ntr, np.int32)
            es = np.zeros((ntr, 4), np.int64)
            pa = np.zeros(ntr, np.int32)
            mx = np.zeros(ntr)
            dsm = np.zeros(ntr)
            dcn = np.zeros(ntr, np.int32)
            evs = np.zeros(1)
            L.ffs_trials(MODELS[model], float(om), k, np.ascontiguousarray(states), len(states), ntr, Ms[i + 1], MA,
                         seed * 1000003 + 7919 * i + n_tr, sample_every, pth, npth, ok, es, pa, mx, dsm, dcn, evs)
            events += float(evs[0])
            n_tr += ntr
            sel = ok.astype(bool)
            oks.append(ok)
            ends.append(es[sel])
            pars.append(pa[sel])
            mv.append(mx[sel])
            ds.append(dsm[sel])
            dc.append(dcn[sel])
            nsucc = int(sum(o.sum() for o in oks))
            if nsucc >= min_success or n_tr >= max_trials:
                break
        nsucc = int(sum(o.sum() for o in oks))
        P = nsucc / n_tr
        stages.append(dict(M_from=Ms[i], M_to=Ms[i + 1], trials=n_tr, successes=nsucc, P=P))
        if nsucc == 0:
            rec.update(ok=False, reason="stage %d had no success in %d trials" % (i, n_tr), stages=stages,
                       cpu=time.process_time() - t0)
            return rec
        logP += math.log(P)
        tree.append(dict(parent=np.concatenate(pars), maxv=np.concatenate(mv), dsum=np.concatenate(ds),
                         dcnt=np.concatenate(dc)))
        states = np.concatenate(ends)
    k_rate = rec["flux"] * math.exp(logP)
    rec.update(ok=True, stages=stages, logP=logP, rate=k_rate, T=1.0 / k_rate, lnT=-math.log(k_rate),
               trial_events=events, cpu=time.process_time() - t0)
    # complete reactive paths: walk back from each final success
    last = tree[-1]
    maxv, dmean = [], []
    for j in range(len(last["parent"])):
        mv_path, dsum, dcnt = 0.0, 0.0, 0
        idx = j
        for s in range(len(tree) - 1, -1, -1):
            mv_path = max(mv_path, tree[s]["maxv"][idx])
            dsum += tree[s]["dsum"][idx]
            dcnt += tree[s]["dcnt"][idx]
            idx = tree[s]["parent"][idx] if s > 0 else None
        maxv.append(mv_path)
        dmean.append(dsum / dcnt if dcnt else float("nan"))
    rec["paths"] = dict(n=len(maxv), mean_max_v=float(np.mean(maxv)), mean_dist=float(np.nanmean(dmean)) if npth else None)
    return rec


def run_size(model, om, k, n0, t_burn, seed0, path=None, replicates=8, **kw):
    reps = [run_ffs(model, om, k, n0, t_burn, seed0 + r, path=path, **kw) for r in range(replicates)]
    good = [r for r in reps if r.get("ok")]
    out = dict(Omega=om, model=model, replicates=reps, n_ok=len(good), cpu=sum(r["cpu"] for r in reps))
    if len(good) >= 2:
        lnT = np.array([r["lnT"] for r in good])
        out["lnT_mean"] = float(lnT.mean())
        out["lnT_se"] = float(lnT.std(ddof=1) / math.sqrt(len(lnT)))
        out["T"] = float(math.exp(lnT.mean()))
        out["T_se"] = out["T"] * out["lnT_se"]
        if path is not None:
            out["mean_max_v"] = float(np.mean([r["paths"]["mean_max_v"] for r in good]))
            out["mean_dist"] = float(np.mean([r["paths"]["mean_dist"] for r in good]))
    return out
