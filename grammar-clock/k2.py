"""K2: continuation of the cycle by shooting + pseudo-arclength (SPEC K2).

Usage: python k2.py lam12051 | Tup | Tdown | lamK1 <draw-json-path> <index>
Closed level: reduced coordinates y = (C, V, L), P = T - C - V - L.  Open level: full state.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp

from clock import core
from ginst import m2, model

EV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
RTOL, ATOL = 1e-10, 1e-13


class Problem:
    def __init__(self, d, mode):
        self.d, self.mode = dict(d), mode  # mode: 'lam' or 'T'
        self.closed = d["level"] == "closed"
        self.use = np.array([j for j in range(11) if not (self.closed and j in (7, 10))])
        self.lnk = np.log(np.array(d["k"], float))
        self.mean = self.lnk[self.use].mean()
        self.span0 = float((self.lnk[self.use].max() - self.lnk[self.use].min()) / np.log(10))

    def par(self, p):
        d = dict(self.d)
        if self.mode == "lam":
            lk = self.lnk.copy()
            lk[self.use] = (1 - p) * self.lnk[self.use] + p * self.mean
            d["k"] = np.exp(lk).tolist()
        else:
            d["T"] = float(p)
        return m2.par_of(d), d

    def full(self, y, p, d):
        return np.append(y, d["T"] - y.sum()) if self.closed else y

    def f(self, y, par, d, p):
        return model.f_np(self.full(y, p, d), par)[:len(y)]

    def J(self, y, par, d, p):
        Jf = model.J_np(self.full(y, p, d), par)
        n = len(y)
        if self.closed:
            return Jf[:3, :3] - Jf[:3, 3:4]
        return Jf[:n, :n]

    def flow(self, y, tau, p, var=False, dense=False):
        par, d = self.par(p)
        n = len(y)
        if not var:
            s = solve_ivp(lambda t, z: self.f(z, par, d, p), (0, tau), y, method="Radau", rtol=RTOL, atol=ATOL,
                          jac=lambda t, z: self.J(z, par, d, p))
            return s.y[:, -1]

        def rhs(t, z):
            x = z[:n]
            Phi = z[n:].reshape(n, n)
            return np.concatenate([self.f(x, par, d, p), (self.J(x, par, d, p) @ Phi).ravel()])
        z0 = np.concatenate([y, np.eye(n).ravel()])
        s = solve_ivp(rhs, (0, tau), z0, method="Radau", rtol=RTOL, atol=ATOL, dense_output=dense)
        out = dict(end=s.y[:n, -1], M=s.y[n:, -1].reshape(n, n))
        if dense:
            zz = s.sol(np.linspace(0, tau, 2000))[:n]
            out["orbit"] = zz
        return out

    def G(self, u, ref, var=True):
        n = len(u) - 2
        y, tau, p = u[:n], u[n], u[n + 1]
        r = self.flow(y, tau, p, var=var)
        e = r["end"] if var else r
        g = np.append(e - y, np.dot(y - ref[0], ref[1]))
        if not var:
            return g
        par, d = self.par(p)
        h = 1e-6 * max(1.0, abs(p))
        dp = (self.flow(y, tau, p + h) - self.flow(y, tau, p - h)) / (2 * h)
        Jg = np.zeros((n + 1, n + 2))
        Jg[:n, :n] = r["M"] - np.eye(n)
        Jg[:n, n] = self.f(e, par, d, p)
        Jg[:n, n + 1] = dp
        Jg[n, :n] = ref[1]
        return g, Jg, r["M"]


def tangent(Jg, prev=None):
    _, _, Vt = np.linalg.svd(Jg)
    t = Vt[-1]
    if prev is not None and np.dot(t, prev) < 0:
        t = -t
    return t


def describe(pb, u, M):
    n = len(u) - 2
    y, tau, p = u[:n], u[n], u[n + 1]
    par, d = pb.par(p)
    r = pb.flow(y, tau, p, var=True, dense=True)
    orb = r["orbit"]
    full = np.array([pb.full(orb[:, j], p, d) for j in range(orb.shape[1])]).T
    mu = np.linalg.eigvals(M)
    order = np.argsort(np.abs(mu - 1))
    bals = model.classify_balances(par)
    bl = []
    for b in bals:
        dist = float(np.min(np.linalg.norm(full - b["b"][:, None], axis=0)) / max(np.linalg.norm(b["b"]), 1e-300))
        bl.append(dict(b=b["b"].tolist(), stable=bool(b["stable"]), eig=[[float(z.real), float(z.imag)] for z in b["eig"]],
                       orbit_dist_rel=dist))
    return dict(p=float(p), period=float(tau), amp_C=float(full[0].max() - full[0].min()),
                C_range=[float(full[0].min()), float(full[0].max())],
                floquet_nontrivial=[float(abs(z)) for z in mu[order[1:]]], trivial=float(abs(mu[order[0]])),
                span=float((1 - p) * pb.span0) if pb.mode == "lam" else pb.span0, balances=bl, y=y.tolist())


def continue_branch(pb, u0, direction, cpu_cap, name, ds0=0.02, ds_max=0.2, p_stop=None):
    c0 = time.process_time()
    n = len(u0) - 2
    w = np.ones(n + 2)
    w[n] = 1.0 / u0[n]  # period scaled by its initial value
    sc = lambda u: u * w  # noqa: E731
    par, d = pb.par(u0[n + 1])
    ref = (u0[:n].copy(), pb.f(u0[:n], par, d, u0[n + 1]) / np.linalg.norm(pb.f(u0[:n], par, d, u0[n + 1])))
    # converge the start point at fixed parameter
    u = u0.copy()
    for _ in range(8):
        g, Jg, M = pb.G(u, ref)
        du = np.linalg.lstsq(Jg[:, :n + 1], -g, rcond=None)[0]
        u[:n + 1] += du
        if np.linalg.norm(du * w[:n + 1]) < 1e-10:
            break
    g, Jg, M = pb.G(u, ref)
    pts = [describe(pb, u, M)]
    t = tangent(Jg / w[None, :] if False else Jg @ np.diag(1 / w))
    if t[n + 1] * direction < 0:
        t = -t
    ds, reason = ds0, None
    path = os.path.join(EV, "k2_%s.json" % name)
    while True:
        if time.process_time() - c0 > cpu_cap:
            reason = "cpu cap"
            break
        par, d = pb.par(u[n + 1])
        fy = pb.f(u[:n], par, d, u[n + 1])
        ref = (u[:n].copy(), fy / np.linalg.norm(fy))
        us_pred = sc(u) + ds * t
        v = us_pred / w
        ok = False
        for it in range(7):
            try:
                g, Jg, M = pb.G(v, ref)
            except Exception:  # noqa: BLE001
                break
            if not np.all(np.isfinite(g)) or v[n] <= 0:
                break
            A = np.vstack([Jg @ np.diag(1 / w), t])
            rhs = -np.append(g, np.dot(t, sc(v) - us_pred))
            dz = np.linalg.solve(A, rhs)
            v = (sc(v) + dz) / w
            if np.linalg.norm(dz) < 1e-9 and np.linalg.norm(g) < 1e-8:
                ok = True
                break
        if ok:
            g, Jg, M = pb.G(v, ref)
            t_new = tangent(Jg @ np.diag(1 / w), t)
            turned = t_new[n + 1] * t[n + 1] < 0
            u, t = v, t_new
            pt = describe(pb, u, M)
            pt["ds"] = ds
            pts.append(pt)
            json.dump(dict(name=name, points=pts), open(path, "w"), default=float)
            if turned:
                reason = "parameter turns (fold)"
                break
            if p_stop is not None and (u[n + 1] - p_stop) * direction >= 0:
                reason = "reached parameter %g" % p_stop
                break
            if u[n] > 1e5:
                reason = "period > 1e5"
                break
            if pt["amp_C"] < 1e-4:
                reason = "amplitude < 1e-4"
                break
            ds = min(ds * (1.5 if it <= 3 else 1.0), ds_max)
        else:
            ds /= 2
            if ds < 1e-7:
                reason = "step below 1e-7 without convergence"
                break
    res = dict(name=name, mode=pb.mode, end_reason=reason, points=pts, cpu_s=time.process_time() - c0,
               span0=pb.span0)
    res["classification"] = classify(res)
    json.dump(res, open(path, "w"), default=float)
    return res


def classify(res):
    P = res["points"]
    if len(P) < 8:
        return dict(type="unclassified", note="fewer than 8 points")
    last = P[-8:]
    p = np.array([q["p"] for q in last])
    per = np.array([q["period"] for q in last])
    amp = np.array([q["amp_C"] for q in last])
    fl = [max(q["floquet_nontrivial"]) if q["floquet_nontrivial"] else 0 for q in last]
    out = dict(last_p=p.tolist(), last_period=per.tolist(), last_amp=amp.tolist(), last_max_floquet=fl,
               end_reason=res["end_reason"])
    if res["end_reason"] and "turn" in res["end_reason"]:
        out["type"] = "fold of cycles" if fl[-1] > 0.9 else "turn, unclassified (no Floquet modulus near 1)"
        return out
    # extrapolated end: p_end = last p plus a small step in the direction of travel
    dirn = np.sign(p[-1] - p[0]) or 1.0
    p_end = p[-1] + dirn * 0.5 * abs(p[-1] - p[-2])
    dist = np.abs(p_end - p)
    ok = dist > 0
    fits = {}
    if ok.sum() >= 4:
        fits["amp_loglog_slope"] = float(np.polyfit(np.log(dist[ok]), np.log(amp[ok]), 1)[0])
        fits["period_loglog_slope"] = float(np.polyfit(np.log(dist[ok]), np.log(per[ok]), 1)[0])
        X = np.log(1 / dist[ok])
        c = np.polyfit(X, per[ok], 1)
        r2 = 1 - np.sum((np.polyval(c, X) - per[ok]) ** 2) / max(np.sum((per[ok] - per[ok].mean()) ** 2), 1e-300)
        fits["period_vs_ln_r2"] = float(r2)
    out["fits"] = fits
    saddle_near = min([b["orbit_dist_rel"] for b in P[-1]["balances"] if not b["stable"]] or [np.inf])
    out["min_orbit_dist_to_unstable_balance"] = float(saddle_near)
    cpx = [b for b in P[-1]["balances"] if any(abs(e[1]) > 1e-9 for e in b["eig"])]
    if res["end_reason"] and "amplitude" in res["end_reason"] and 0.4 <= fits.get("amp_loglog_slope", 0) <= 0.6 and cpx:
        out["type"] = "Hopf"
    elif res["end_reason"] and "period" in res["end_reason"] and -0.6 <= fits.get("period_loglog_slope", 0) <= -0.4:
        out["type"] = "SNIC (candidate; check balance saddle-node)"
    elif res["end_reason"] and "period" in res["end_reason"] and fits.get("period_vs_ln_r2", 0) >= 0.99 \
            and saddle_near < 1e-2:
        out["type"] = "homoclinic"
    elif res["end_reason"] and res["end_reason"].startswith("reached"):
        out["type"] = "none (branch reached the end of the parameter range)"
    else:
        out["type"] = "unclassified"
    return out


def start_12051():
    tg, X, cdet = core.det_cycle()
    return core.D12051, X[:3, 0], core.T_DET


if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    job = sys.argv[1]
    cap = float(sys.argv[2]) if len(sys.argv) > 2 else 900
    if job in ("lam12051", "Tup", "Tdown"):
        d, y0, tau = start_12051()
        if job == "lam12051":
            pb = Problem(d, "lam")
            u0 = np.concatenate([y0, [tau, 0.0]])
            r = continue_branch(pb, u0, +1, cap, "lam12051", p_stop=1.0)
        else:
            pb = Problem(d, "T")
            u0 = np.concatenate([y0, [tau, d["T"]]])
            r = continue_branch(pb, u0, +1 if job == "Tup" else -1, cap, job, ds0=0.01, ds_max=0.1)
    else:  # lamK1 <json with draw, point, period> <name>
        spec = json.load(open(sys.argv[3]))
        d = spec["draw"]
        pb = Problem(d, "lam")
        y0 = np.array(spec["point"])[:3] if d["level"] == "closed" else np.array(spec["point"])
        u0 = np.concatenate([y0, [spec["period"], 0.0]])
        r = continue_branch(pb, u0, +1, cap, sys.argv[4], p_stop=1.0)
    print(json.dumps(dict(name=r["name"], end=r["end_reason"], n=len(r["points"]), p_last=r["points"][-1]["p"],
                          period_last=r["points"][-1]["period"], cls=r["classification"].get("type"),
                          cpu=r["cpu_s"])), flush=True)
