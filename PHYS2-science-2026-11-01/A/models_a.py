"""Part A: model definitions and the deterministic limit cycle.

The deterministic (Kurtz) limit of the chain is

  dC/dt = -(k1+k2+k7) C + k3 V F_kr(x) + k6 L + k10 V - k11 C F_kc(x)
  dV/dt =  k2 C - k3 V F_kr(x) + k5 L + k8 P - k10 V + k11 C F_kc(x) + [open] k12
  dL/dt =  k1 C - (k5+k6) L
  dP/dt =  k7 C - k8 P - [open] k9 P

with x = C/(C+V+L+P) and F_j(x) = Pr[Bin(m,x) >= j].
On the closed level rules 9 and 12 are absent and C+V+L+P is conserved.
"""
import os
import numpy as np
from math import comb
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))

A1 = dict(
    name="A1", level="closed", m=8, kr=2, kc=4, draw=19387,
    total=12.872923044730259,
    k=(1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
       0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678,
       0.17271135353305755, 0.10361090436515946, 6.769536427560776),
    period_claim=6.3524,
)

A2 = dict(
    name="A2", level="open", m=6, kr=2, kc=3, draw=33538,
    total=None,
    k=(0.16060731572267742, 3.7768995051238523, 8.455266356236777, 0.15036717833913482,
       0.12593008757363863, 1.8070659981769923, 0.15004519519714457, 0.3071328391558332,
       0.21585689687505635, 0.4453036700615455, 0.6705277209656662),
    period_claim=4.8439,
)

MODELS = {"A1": A1, "A2": A2}


def ftail(j, m, x):
    x = min(max(x, 0.0), 1.0)
    return sum(comb(m, i) * x ** i * (1 - x) ** (m - i) for i in range(j, m + 1))


def rhs_factory(M):
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = M["k"]
    m, kr, kc = M["m"], M["kr"], M["kc"]
    op = 1.0 if M["level"] == "open" else 0.0

    def rhs(t, y):
        C, V, L, P = y
        tot = C + V + L + P
        x = C / tot if tot > 0 else 0.0
        r3 = k3 * V * ftail(kr, m, x)
        r11 = k11 * C * ftail(kc, m, x)
        return [-(k1 + k2 + k7) * C + r3 + k6 * L + k10 * V - r11,
                k2 * C - r3 + k5 * L + k8 * P - k10 * V + r11 + op * k12,
                k1 * C - (k5 + k6) * L,
                k7 * C - k8 * P - op * k9 * P]
    return rhs


def limit_cycle(M, t_trans=4000.0, nsamp=4096):
    """Return (T, cycle[nsamp,4], period_jitter). Cycle starts at a C-upcrossing
    of the mid-level and is sampled uniformly in time over one period."""
    rhs = rhs_factory(M)
    y0 = (np.array([0.25, 0.45, 0.2, 0.1]) * M["total"] if M["level"] == "closed"
          else np.array([1.0, 1.0, 1.0, 1.0]))
    s = solve_ivp(rhs, (0, t_trans), y0, method="DOP853", rtol=1e-12, atol=1e-14)
    s2 = solve_ivp(rhs, (0, 200.0), s.y[:, -1], method="DOP853", rtol=1e-12,
                   atol=1e-14, dense_output=True, max_step=0.01)
    ts = np.linspace(0, 200, 400001)
    Cs = s2.sol(ts)[0]
    Cbar = 0.5 * (Cs.max() + Cs.min())
    g = lambda t: s2.sol(t)[0] - Cbar
    cross = []
    for i in range(len(ts) - 1):
        if Cs[i] < Cbar <= Cs[i + 1]:
            cross.append(brentq(g, ts[i], ts[i + 1], xtol=1e-13, rtol=1e-14))
            if len(cross) >= 12:
                break
    per = np.diff(cross)
    T = float(np.mean(per[2:]))
    tt = cross[2] + np.linspace(0, T, nsamp, endpoint=False)
    return T, s2.sol(tt).T.copy(), float(np.std(per[2:]))


def cycle_path(name):
    return os.path.join(HERE, f"cycle_{name}.npz")


def get_cycle(name):
    """Load the frozen cycle file, computing it once if absent."""
    p = cycle_path(name)
    if not os.path.exists(p):
        M = MODELS[name]
        T, cyc, jit = limit_cycle(M)
        sig = cyc.std(axis=0, ddof=0)
        np.savez(p, T=np.array([T]), cycle=cyc, sigma=sig, jitter=np.array([jit]))
    z = np.load(p)
    return float(z["T"][0]), z["cycle"], z["sigma"]


def initial_counts(M, Omega, cyc):
    """Integer start state on the cycle. On the closed level the total is pinned
    to N = round(Omega*total) by absorbing the rounding residue into P."""
    c0 = cyc[0]
    n = np.rint(c0 * Omega).astype(np.int64)
    if M["level"] == "closed":
        N = int(round(Omega * M["total"]))
        n[3] = N - n[0] - n[1] - n[2]
    return n
