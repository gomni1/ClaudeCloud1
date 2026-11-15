"""Closed level of the grammar at one site, in ensemble fractions.

Per site the counts (C,V,L,P) sum to Omega; the fractions are (c,v,l,p).
With F_j(x) = Pr[Bin(m,x) >= j] and x the count each unit reads,

  dc/dt = -(k1 + k2 + k11 F_kc(x) + k7) c + (k10 + k3 F_kr(x)) v + k6 l
  dv/dt =  (k2 + k11 F_kc(x)) c - (k10 + k3 F_kr(x)) v + k5 l + k8 p
  dl/dt =   k1 c - (k5 + k6) l
  dp/dt =   k7 c - k8 p

k9 and k12 are unused at the closed level, so c+v+l+p is conserved.
For an isolated site x = c.
"""
import numpy as np
from math import comb
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

K = (1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
     0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678,
     0.17271135353305755, 0.10361090436515946, 6.769536427560776)
k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = K
M, KR, KC = 8, 2, 4
PERIOD_CLAIM = 6.3524
BINOM = np.array([comb(M, i) for i in range(M + 1)], dtype=np.float64)


def ftail(j, x):
    x = min(max(x, 0.0), 1.0)
    return float(sum(BINOM[i] * x ** i * (1 - x) ** (M - i) for i in range(j, M + 1)))


def rhs(t, y):
    c, v, l, p = y
    Fr, Fc = ftail(KR, c), ftail(KC, c)
    out_c = k1 + k2 + k11 * Fc + k7
    in_c = k10 + k3 * Fr
    return [-out_c * c + in_c * v + k6 * l,
            (k2 + k11 * Fc) * c - in_c * v + k5 * l + k8 * p,
            k1 * c - (k5 + k6) * l,
            k7 * c - k8 * p]


def balance():
    """The fixed point the cycle winds around. l and p follow c linearly and the
    fractions sum to 1, so only dc/dt = 0 has to be solved."""
    a_l = k1 / (k5 + k6)
    a_p = k7 / k8

    def g(c):
        l, p = a_l * c, a_p * c
        return rhs(0.0, [c, 1.0 - c - l - p, l, p])[0]
    c = brentq(g, 1e-9, 1.0 / (1 + a_l + a_p) - 1e-9, xtol=1e-15, rtol=8.9e-16)
    y = np.array([c, 1.0 - c * (1 + a_l + a_p), a_l * c, a_p * c])
    assert abs(y.sum() - 1) < 1e-12
    return y


def limit_cycle(nsamp=4096, t_trans=3000.0):
    """One period of the deterministic cycle, sampled uniformly in time."""
    y0 = np.array([0.25, 0.45, 0.18, 0.12]); y0 /= y0.sum()
    s = solve_ivp(rhs, (0, t_trans), y0, method="DOP853", rtol=1e-12, atol=1e-14)
    s2 = solve_ivp(rhs, (0, 200.0), s.y[:, -1], method="DOP853", rtol=1e-12,
                   atol=1e-14, dense_output=True, max_step=0.01)
    ts = np.linspace(0, 200, 400001)
    cs = s2.sol(ts)[0]
    mid = 0.5 * (cs.max() + cs.min())
    g = lambda t: s2.sol(t)[0] - mid
    cross = []
    for i in range(len(ts) - 1):
        if cs[i] < mid <= cs[i + 1]:
            cross.append(brentq(g, ts[i], ts[i + 1], xtol=1e-13, rtol=8.9e-16))
            if len(cross) >= 12:
                break
    per = np.diff(cross)
    T = float(np.mean(per[2:]))
    tt = cross[2] + np.linspace(0, T, nsamp, endpoint=False)
    return T, s2.sol(tt).T.copy(), float(np.std(per[2:]))


def deterministic_facts():
    """Period, balance, c and v ranges, cycle standard deviations, the winding of
    the cycle about the balance, and the cycle's mean scaled amplitude."""
    T, cyc, jit = limit_cycle()
    bal = balance()
    cstar, vstar = bal[0], bal[1]
    s_c = float(cyc[:, 0].std(ddof=0)); s_v = float(cyc[:, 1].std(ddof=0))
    ph = np.arctan2((cyc[:, 1] - vstar) / s_v, (cyc[:, 0] - cstar) / s_c)
    d = np.diff(np.concatenate([ph, ph[:1]]))
    d = (d + np.pi) % (2 * np.pi) - np.pi
    amp = np.hypot((cyc[:, 0] - cstar) / s_c, (cyc[:, 1] - vstar) / s_v)
    return dict(T=T, period_jitter=jit, balance=bal.tolist(),
                c_range=[float(cyc[:, 0].min()), float(cyc[:, 0].max())],
                v_range=[float(cyc[:, 1].min()), float(cyc[:, 1].max())],
                s_c=s_c, s_v=s_v, winding=float(d.sum() / (2 * np.pi)),
                mean_amplitude=float(amp.mean()), cycle=cyc)
