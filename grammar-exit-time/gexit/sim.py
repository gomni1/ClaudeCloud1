"""ctypes wrapper around csrc/ssa.c and a process pool for batches (SPEC §2)."""
import ctypes
import hashlib
import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from . import model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "csrc", "ssa.c")
LIB = os.path.join(ROOT, "build", "libssa.so")

MODELS = {"MA": 0, "TH": 1, "MAC": 2, "ID": 3, "ND": 4}
TARGETS = {"D": 0, "D0": 1, "VGE": 2, "VLE": 3, "X0": 4, "XOUT": 5, "NONE": 6}
MASTER_SEED = 20261028

_lib = None
_d = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
_i64 = np.ctypeslib.ndpointer(dtype=np.int64, flags="C_CONTIGUOUS")
_i32 = np.ctypeslib.ndpointer(dtype=np.int32, flags="C_CONTIGUOUS")


def build(force=False):
    os.makedirs(os.path.dirname(LIB), exist_ok=True)
    if force or not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
        subprocess.check_call(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, SRC, "-lm"])


def lib():
    global _lib
    if _lib is None:
        build()
        L = ctypes.CDLL(LIB)
        L.run_exits.restype = ctypes.c_int
        L.run_exits.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, ctypes.c_int, ctypes.c_int64,
                                ctypes.c_int64, ctypes.c_double, ctypes.c_double, ctypes.c_int,
                                ctypes.c_uint64, ctypes.c_int64, ctypes.c_double, _d, _i32, _i64, _d, _i32,
                                _i64, _d, _d, _i32]
        L.run_hist.restype = ctypes.c_double
        L.run_hist.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, ctypes.c_double, ctypes.c_double,
                               ctypes.c_uint64, ctypes.c_int64, ctypes.c_int, _d, ctypes.c_int64,
                               ctypes.c_int64, _i64]
        L.run_traj.restype = ctypes.c_double
        L.run_traj.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, ctypes.c_int, _d, ctypes.c_uint64,
                               _i64]
        L.propensity_vec.restype = ctypes.c_int
        L.propensity_vec.argtypes = [ctypes.c_int, ctypes.c_double, _d, _i64, _d]
        _lib = L
    return _lib


def seed_for(*parts):
    h = hashlib.sha256(("%d|" % MASTER_SEED + "|".join(str(p) for p in parts)).encode()).digest()
    return int.from_bytes(h[:8], "little")


def propensities(mdl, omega, n, k=model.KVEC):
    a = np.zeros(11)
    m = lib().propensity_vec(MODELS[mdl], float(omega), np.ascontiguousarray(k, float),
                             np.ascontiguousarray(n, np.int64), a)
    return a[:m]


def run_exits(task):
    """One batch.  task: dict(model, omega, n0, target, ta, tb, t_burn, cap, nruns, seed,
    max_attempts, max_cpu).  Returns arrays plus the CPU seconds of the call."""
    L = lib()
    n = int(task["nruns"])
    out_t = np.zeros(n)
    out_c = np.zeros(n, np.int32)
    out_r = np.zeros(n, np.int64)
    out_e = np.zeros(n)
    out_s = np.zeros(n, np.int32)
    att = np.zeros(1, np.int64)
    fev = np.zeros(1)
    aev = np.zeros(1)
    ab = np.zeros(1, np.int32)
    k = np.ascontiguousarray(task.get("k", model.KVEC), float)
    c0 = time.process_time()
    w0 = time.time()
    done = L.run_exits(MODELS[task["model"]], float(task["omega"]), k,
                       np.ascontiguousarray(task["n0"], np.int64), TARGETS[task["target"]],
                       int(task.get("ta", 0)), int(task.get("tb", 0)), float(task["t_burn"]),
                       float(task["cap"]), n, int(task["seed"]), int(task.get("max_attempts", 0)),
                       float(task.get("max_cpu", 0.0)), out_t, out_c, out_r, out_e, out_s, att, fev, aev, ab)
    cpu = time.process_time() - c0
    return dict(time=out_t[:done], cens=out_c[:done], restarts=out_r[:done], events=out_e[:done],
                secD=out_s[:done], attempts=int(att[0]), failed_events=float(fev[0]),
                all_events=float(aev[0]), aborted=int(ab[0]), cpu=cpu, wall=time.time() - w0,
                seed=int(task["seed"]), nruns_req=n)


def run_hist(task):
    L = lib()
    nmax = int(task["nmax"])
    nb = int(task["nblocks"])
    hist = np.zeros(nb * (nmax + 1))
    nsw = np.zeros(1, np.int64)
    c0 = time.process_time()
    ev = L.run_hist(MODELS[task["model"]], float(task["omega"]), np.ascontiguousarray(model.KVEC),
                    np.ascontiguousarray(task["n0"], np.int64), float(task["t_burn"]), float(task["t_total"]),
                    int(task["seed"]), nmax, nb, hist, int(task["lo"]), int(task["hi"]), nsw)
    return dict(hist=hist.reshape(nb, nmax + 1), events=ev, n_switch=int(nsw[0]),
                cpu=time.process_time() - c0)


def run_traj(mdl, omega, n0, times, seed):
    times = np.ascontiguousarray(times, float)
    out = np.zeros(4 * len(times), np.int64)
    ev = lib().run_traj(MODELS[mdl], float(omega), np.ascontiguousarray(model.KVEC),
                        np.ascontiguousarray(n0, np.int64), len(times), times, int(seed), out)
    return out.reshape(len(times), 4), ev


_pool = None


def pool(workers=None):
    global _pool
    if _pool is None:
        lib()  # compile once before forking
        _pool = ProcessPoolExecutor(max_workers=workers or os.cpu_count())
    return _pool


def map_batches(tasks, fn=run_exits):
    return list(pool().map(fn, tasks))
