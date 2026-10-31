"""K3: SSA wrapper, deterministic reference cycle, tick/stall estimators, exact master equation (SPEC K3)."""
import ctypes
import os
import subprocess
import sys

import numpy as np
from scipy import sparse
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import spsolve
from scipy.stats import binom as _binom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "grammar-instability"))
from ginst import m2, model  # noqa: E402

SRC = os.path.join(ROOT, "csrc", "ssa.c")
LIB = os.path.join(ROOT, "csrc", "libssa.so")
D12051 = m2.draw_params(12051)
K = np.array(D12051["k"])
M, KR, KC, T_TOT = D12051["m"], D12051["kr"], D12051["kc"], D12051["T"]
T_DET = 247.528859880
CMID, DELTA = 1.340, 1.146
CDROP = CMID - 0.25 * DELTA
STALL = 5 * 247.53
M_G, M_BR = 0, 1

_d = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
_f = np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS")
_i64 = np.ctypeslib.ndpointer(dtype=np.int64, flags="C_CONTIGUOUS")
_L = None


def lib():
    global _L
    if _L is None:
        if not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
            subprocess.check_call(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, SRC, "-lm"])
        L = ctypes.CDLL(LIB)
        c = ctypes
        L.run_clock.restype = c.c_int
        L.run_clock.argtypes = [c.c_int, c.c_double, _d, _d, _d, _i64, c.c_double, c.c_int64, c.c_int64, c.c_double,
                                c.c_double, c.c_double, c.c_int, c.c_int64, _f, _d, c.c_uint64, c.c_double, _d]
        L.run_hist2.restype = c.c_double
        L.run_hist2.argtypes = [c.c_int, c.c_double, _d, _d, _d, _i64, c.c_int64, c.c_int64, c.c_uint64, c.c_int64, _d]
        _L = L
    return _L


def ftables(N, m=M, kr=KR, kc=KC):
    x = np.arange(N + 1) / N
    return _binom.sf(kr - 1, m, x).astype(np.float64), _binom.sf(kc - 1, m, x).astype(np.float64)


def seed_of(*a):
    return int(np.random.default_rng([31102026, *a]).integers(0, 2 ** 63))


def run_clock(om, n0, seed, t_max, max_ticks=1000, max_events=0, nsp=1, dt_s=0.05, model_id=M_G, k=K,
              cmid=CMID, cdrop=CDROP, max_cpu=0.0, N=None):
    n0 = np.array(list(n0) + [0] * (4 - len(n0)), dtype=np.int64)
    if model_id == M_G:
        FR, FC = ftables(int(N if N is not None else n0.sum()))
    else:
        FR = FC = np.zeros(1)
    max_samp = int(t_max / dt_s) + 2
    samp = np.zeros(max_samp * nsp, dtype=np.float32)
    ticks = np.zeros(max_ticks + 1)
    stats = np.zeros(6)
    lib().run_clock(model_id, float(om), np.ascontiguousarray(k, float), FR, FC, n0, float(t_max), int(max_ticks),
                    int(max_events), float(cmid), float(cdrop), float(dt_s), int(nsp), max_samp, samp, ticks,
                    seed, float(max_cpu), stats)
    js = int(stats[5])
    return dict(ticks=ticks[:int(stats[2])].copy(), samp=samp[:js * nsp].reshape(js, nsp), events=int(stats[0]),
                dvisits=int(stats[1]), t_end=float(stats[3]), aborted=bool(stats[4]), n_end=n0.copy(), dt_s=dt_s)


# ---------- deterministic reference cycle ----------
def par12051(T=T_TOT):
    return m2.par_of(dict(D12051, T=T))


def det_cycle(npts=20000):
    """Deterministic cycle aligned on its own tick: returns (t grid over one period, states (4, npts), x_tick)."""
    par = par12051()
    path = os.path.join(ROOT, "..", "grammar-instability", "evidence", "m4_cycle.json")
    import json
    h = json.load(open(path))["hits"][0]
    x0 = None
    cache = os.path.join(ROOT, "evidence", "k3_cycle_point.json")
    if os.path.exists(cache):
        x0 = np.array(json.load(open(cache))["point"])
    if x0 is None:
        # regenerate from PR 4's M2 run of draw 12051 (start 0 end state is on the cycle)
        rec = m2.process(D12051)
        x0 = np.array(rec["runs"][0]["class"]["point"])
        json.dump(dict(point=x0.tolist(), source="m2.process(draw 12051) start 0 periodic point"), open(cache, "w"))
    f = lambda t, z: model.f_np(z, par)  # noqa: E731
    jac = lambda t, z: model.J_np(z, par)  # noqa: E731
    s = solve_ivp(f, (0, 3 * T_DET), x0, method="Radau", rtol=1e-11, atol=1e-14, jac=jac, dense_output=True)
    tt = np.linspace(0, 3 * T_DET, 300000)
    C = s.sol(tt)[0]
    armed, t_tick = False, None
    for j in range(1, len(tt)):
        if C[j] < CDROP:
            armed = True
        elif armed and C[j] >= CMID and C[j - 1] < CMID:
            a = (CMID - C[j - 1]) / (C[j] - C[j - 1])
            t_tick = tt[j - 1] + a * (tt[j] - tt[j - 1])
            break
    tg = np.linspace(0, T_DET, npts, endpoint=False)
    X = s.sol(t_tick + tg)
    return tg, X, X[0].copy()


def n_start(om, x):
    N = int(round(om * T_TOT))
    n = np.round(om * np.asarray(x)).astype(np.int64)
    n[3] = N - n[:3].sum()
    return n, N


# ---------- estimators ----------
def tick_stats(ticks):
    iv = np.diff(np.asarray(ticks))
    if len(iv) < 2:
        return dict(n_int=len(iv), mean=np.nan, cv=np.nan, ncoh=np.nan)
    mu, sd = iv.mean(), iv.std(ddof=1)
    return dict(n_int=int(len(iv)), mean=float(mu), cv=float(sd / mu), ncoh=float((mu / sd) ** 2))


def stalls(ticks, t_end, samp_c, dt_s, Tbar, cdet, thr=STALL, band=0.25 * DELTA):
    """Stalls = gaps > thr (final censored gap included).  Start phase per stall:
    (t_exit - t_last)/Tbar, t_exit = first grid time after t_last with |c - c_det(phi)| > band,
    phi = (t - t_last)/Tbar, c_det(phi) = cdet[((phi mod 1) * len(cdet))]."""
    ticks = np.asarray(ticks)
    out = []
    ends = list(ticks[1:]) + [t_end]
    for j, (a, b) in enumerate(zip(ticks, ends)):
        if b - a <= thr:
            continue
        j0 = int(np.ceil(a / dt_s - 1e-9))
        j1 = min(int(b / dt_s), len(samp_c))
        tg = np.arange(j0, j1) * dt_s
        ph = (tg - a) / Tbar
        cd = cdet[((ph % 1.0) * len(cdet)).astype(int) % len(cdet)]
        bad = np.nonzero(np.abs(samp_c[j0:j1] - cd) > band)[0]
        phase = float((tg[bad[0]] - a) / Tbar) if len(bad) else np.nan
        out.append(dict(t_last=float(a), gap=float(b - a), censored=bool(j == len(ticks) - 1), phase=phase))
    return out


# ---------- exact closed-level master equation (independent numpy propensities) ----------
def exact_stationary(om):
    N = int(round(om * T_TOT))
    states = [(c, v, l, N - c - v - l) for c in range(N + 1) for v in range(N + 1 - c) for l in range(N + 1 - c - v)]
    idx = {s: i for i, s in enumerate(states)}
    S = np.array(states)
    k1, k2, k3, k5, k6, k7, k8, _k9, k10, k11, _k12 = K
    x = S[:, 0] / N
    Fr = _binom.sf(KR - 1, M, x)
    Fc = _binom.sf(KC - 1, M, x)
    C, V, L, P = S.T
    reac = [(k1 * C, (-1, 0, 1, 0)), (k2 * C, (-1, 1, 0, 0)), (k3 * V * Fr, (1, -1, 0, 0)), (k5 * L, (0, 1, -1, 0)),
            (k6 * L, (1, 0, -1, 0)), (k7 * C, (-1, 0, 0, 1)), (k8 * P, (0, 1, 0, -1)), (k10 * V, (1, -1, 0, 0)),
            (k11 * C * Fc, (-1, 1, 0, 0))]
    rows, cols, vals = [], [], []
    out = np.zeros(len(S))
    for a, nu in reac:
        tgt = S + np.array(nu)
        ok = (a > 0) & np.all(tgt >= 0, axis=1)
        j = np.array([idx[tuple(t)] for t in tgt[ok]])
        rows += list(np.nonzero(ok)[0])
        cols += list(j)
        vals += list(a[ok])
        out += np.where(ok, a, 0.0)
    Q = sparse.csr_matrix((vals, (rows, cols)), shape=(len(S), len(S))) - sparse.diags(out)
    A = Q.T.tolil()
    A[0, :] = np.ones(len(S))
    b = np.zeros(len(S))
    b[0] = 1.0
    pi = spsolve(A.tocsr(), b)
    pc = np.bincount(S[:, 0], weights=pi, minlength=N + 1)
    return dict(N=N, n_states=len(S), pi_C=pc, min_pi=float(pi.min()))


def hist_chain(om, seed, n_burn, n_events, n0):
    N = int(round(om * T_TOT))
    FR, FC = ftables(N)
    h = np.zeros(N + 1)
    T = lib().run_hist2(M_G, float(om), K, FR, FC, np.array(n0, np.int64), int(n_burn), int(n_events), seed, N + 1, h)
    return h / T


def tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) / np.sum(p) - np.asarray(q) / np.sum(q)).sum())
