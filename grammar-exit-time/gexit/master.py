"""Exact mean first-passage time to D on a truncated lattice (SPEC §5, M6).

Propensities are re-implemented here in numpy, independently of csrc/ssa.c."""
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import pyamg

from . import model

MAX_STATES = 4_000_000


def propensities_np(law, om, n):
    """n: (..., 4) integer counts; Kurtz-form propensities (SPEC §2)."""
    k = model.KVEC
    C, V, L, P = (n[..., i].astype(float) for i in range(4))
    a = np.empty(n.shape[:-1] + (11,))
    a[..., 0] = k[0] * C
    a[..., 1] = k[1] * C
    a[..., 3] = k[3] * L
    a[..., 4] = k[4] * L
    a[..., 5] = k[5] * C
    a[..., 6] = k[6] * P
    a[..., 7] = k[7] * P
    a[..., 8] = k[8] * V
    a[..., 10] = k[10] * om
    if law == "MA":
        a[..., 2] = k[2] * V * C / om
        a[..., 9] = k[9] * C * C / om
    elif law == "MAC":
        a[..., 2] = k[2] * V * C / om
        a[..., 9] = k[9] * C * (C - 1) / om
    else:
        s = C + V
        x = np.where(s > 0, C / np.where(s > 0, s, 1), 0.0)
        a[..., 2] = k[2] * V * x * x
        a[..., 9] = k[9] * C * x * x
    return a


def mfpt_D(law, om, n0, caps, tol=1e-10, method="auto"):
    """Mean first-passage time from n0 to D = {nC = nL = 0}, caps = (KC, KV, KL, KP)."""
    caps = np.asarray(caps, int)
    dims = caps + 1
    N = int(np.prod(dims))
    if N > MAX_STATES:
        raise ValueError("lattice too large: %d" % N)
    grids = np.meshgrid(*[np.arange(d) for d in dims], indexing="ij")
    states = np.stack([g.ravel() for g in grids], axis=1)
    inD = (states[:, 0] == 0) & (states[:, 2] == 0)
    T_idx = np.flatnonzero(~inD)
    pos = -np.ones(N, np.int64)
    pos[T_idx] = np.arange(len(T_idx))
    sT = states[T_idx]
    a = propensities_np(law, om, sT)
    strides = np.array([dims[1] * dims[2] * dims[3], dims[2] * dims[3], dims[3], 1])
    rows, cols, vals = [], [], []
    diag = np.zeros(len(T_idx))
    for r in range(11):
        nu = model.NU[r].astype(int)
        tgt = sT + nu
        ok = np.all((tgt >= 0) & (tgt <= caps), axis=1) & (a[:, r] > 0)
        diag[ok] += a[ok, r]
        lin = (tgt[ok] * strides).sum(axis=1)
        j = pos[lin]
        inT = j >= 0
        rows.append(np.flatnonzero(ok)[inT])
        cols.append(j[inT])
        vals.append(-a[ok, r][inT])
    rows = np.concatenate(rows + [np.arange(len(T_idx))])
    cols = np.concatenate(cols + [np.arange(len(T_idx))])
    vals = np.concatenate(vals + [diag])
    A = sp.csr_matrix((vals, (rows, cols)), shape=(len(T_idx), len(T_idx)))
    b = np.ones(len(T_idx))
    t0 = time.time()
    if method == "direct" or (method == "auto" and len(T_idx) <= 50_000):
        tau = spla.spsolve(A.tocsc(), b)
        method = "direct"
    else:
        # classical (Ruge-Stuben) algebraic multigrid, GMRES-accelerated, with iterative refinement;
        # AIR converged faster but its setup ran out of memory (14 GB) at 3.2M states
        ml = pyamg.ruge_stuben_solver(A, max_coarse=500)
        tau = np.zeros_like(b)
        its, rounds = 0, 0
        while rounds < 20:
            r = b - A @ tau
            if np.linalg.norm(r) / np.linalg.norm(b) <= tol * 0.1:
                break
            resid = []
            tau = tau + ml.solve(r, tol=1e-6, accel="gmres", maxiter=200, residuals=resid)
            its += len(resid)
            rounds += 1
        method = "RS-AMG + GMRES, %d refinement rounds, %d it" % (rounds, its)
    res = np.linalg.norm(A @ tau - b) / np.linalg.norm(b)
    i0 = pos[int((np.asarray(n0) * strides).sum())]
    return dict(T=float(tau[i0]), residual=float(res), states=N, method=method, solve_s=time.time() - t0,
                caps=caps.tolist())


def initial_caps(n0):
    return np.maximum(6, 2 * np.ceil(np.asarray(n0, float)).astype(int) + 6)


def converged_mfpt(law, om, n0, rel=1e-3, log=print):
    caps = initial_caps(n0)
    levels = []
    while True:
        try:
            r = mfpt_D(law, om, n0, caps)
        except (ValueError, MemoryError) as e:
            return dict(converged=False, levels=levels, error=str(e))
        levels.append(r)
        log("  M6 %s Omega=%s caps=%s T=%.10g res=%.1e states=%d (%s, %.1fs)" % (
            law, om, r["caps"], r["T"], r["residual"], r["states"], r["method"], r["solve_s"]))
        if len(levels) >= 2 and abs(levels[-1]["T"] - levels[-2]["T"]) / levels[-1]["T"] < rel:
            return dict(converged=True, T=levels[-1]["T"], levels=levels)
        caps = caps * 2
