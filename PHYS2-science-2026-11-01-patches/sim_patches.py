"""Site ensembles on a frozen neighbour relation.

Each site holds Omega units with counts (C,V,L,P) summing to Omega. Within a
site the seven transitions are those of the closed level; sites couple only
through the count each unit reads,

    x_i = (1-w)*C_i/Omega + w * mean over i's graph neighbours of C_j/Omega.

Production uses tau-leaping with a declared step dt, Poisson leaps clipped so
that no species goes negative. The clip is applied per source species: if the
draws leaving a species exceed its count, the largest draw is decremented until
they balance. `ssa_site` is the exact Gillespie direct method for one isolated
site and is the reference the leap is validated against (harness H2).
"""
import numpy as np
from numba import njit

K = np.array((1.1104700305441388, 3.392924979396869, 6.841291178912343,
              0.24399914028161648, 0.2564493936497987, 4.507911093539853,
              3.4671282746997387, 9.305812659924678, 0.17271135353305755,
              0.10361090436515946, 6.769536427560776))


@njit(cache=True, inline='always')
def _tails(x):
    """(F_2(x), F_4(x)) for Bin(8, x)."""
    if x < 0.0:
        x = 0.0
    elif x > 1.0:
        x = 1.0
    q = 1.0 - x
    p = q * q * q * q * q * q * q * q          # p0
    s0 = p
    r = x / q if q > 1e-300 else 0.0
    p = p * 8.0 * r; s1 = p                    # p1
    p = p * (7.0 / 2.0) * r; s2 = p            # p2
    p = p * (6.0 / 3.0) * r; s3 = p            # p3
    f2 = 1.0 - s0 - s1
    f4 = 1.0 - s0 - s1 - s2 - s3
    if f2 < 0.0:
        f2 = 0.0
    if f4 < 0.0:
        f4 = 0.0
    return f2, f4


@njit(cache=True, inline='always')
def _clip3(a, b, c, tot):
    """Decrement the largest of three draws until they sum to at most tot."""
    s = a + b + c
    while s > tot:
        if a >= b and a >= c:
            a -= 1
        elif b >= c:
            b -= 1
        else:
            c -= 1
        s -= 1
    return a, b, c


@njit(cache=True)
def tau_leap(C, V, L, P, indptr, indices, Omega, w, kk, dt, n_steps,
             n_rec, burn_steps, tau_filt, cstar, vstar, s_c, s_v, phase, amp):
    """Advance all sites by n_steps leaps, recording phase and amplitude every
    n_rec steps once burn_steps have passed."""
    k1 = kk[0]; k2 = kk[1]; k3 = kk[2]; k5 = kk[3]; k6 = kk[4]
    k7 = kk[5]; k8 = kk[6]; k10 = kk[8]; k11 = kk[9]
    N = C.shape[0]
    inv = 1.0 / Omega
    cf = np.empty(N); vf = np.empty(N)
    for i in range(N):
        cf[i] = C[i] * inv; vf[i] = V[i] * inv
    a_f = np.exp(-dt / tau_filt)
    cb = np.empty(N)
    frame = 0
    for step in range(n_steps):
        for i in range(N):
            s = 0.0
            lo = indptr[i]; hi = indptr[i + 1]
            for j in range(lo, hi):
                s += C[indices[j]] * inv
            cb[i] = s / (hi - lo)
        for i in range(N):
            ci = C[i] * inv
            x = (1.0 - w) * ci + w * cb[i]
            f2, f4 = _tails(x)
            nCL = np.random.poisson(k1 * C[i] * dt)
            nCV = np.random.poisson((k2 + k11 * f4) * C[i] * dt)
            nCP = np.random.poisson(k7 * C[i] * dt)
            nCL, nCV, nCP = _clip3(nCL, nCV, nCP, C[i])
            nVC = np.random.poisson((k10 + k3 * f2) * V[i] * dt)
            if nVC > V[i]:
                nVC = V[i]
            nLV = np.random.poisson(k5 * L[i] * dt)
            nLC = np.random.poisson(k6 * L[i] * dt)
            nLV, nLC, _ = _clip3(nLV, nLC, 0, L[i])
            nPV = np.random.poisson(k8 * P[i] * dt)
            if nPV > P[i]:
                nPV = P[i]
            C[i] += -nCL - nCV - nCP + nVC + nLC
            V[i] += nCV - nVC + nLV + nPV
            L[i] += nCL - nLV - nLC
            P[i] += nCP - nPV
            cf[i] = a_f * cf[i] + (1.0 - a_f) * (C[i] * inv)
            vf[i] = a_f * vf[i] + (1.0 - a_f) * (V[i] * inv)
        if step >= burn_steps and (step - burn_steps) % n_rec == 0:
            if frame < phase.shape[0]:
                for i in range(N):
                    dc = (cf[i] - cstar) / s_c
                    dv = (vf[i] - vstar) / s_v
                    phase[frame, i] = np.arctan2(dv, dc)
                    amp[frame, i] = np.sqrt(dc * dc + dv * dv)
                frame += 1
    return frame


@njit(cache=True)
def leap_site(C0, V0, L0, P0, Omega, kk, dt, n_steps, n_rec, burn_steps,
              tau_filt, cstar, vstar, s_c, s_v, phase):
    """Tau-leap of one isolated site (w = 0); records phase only."""
    C = C0; V = V0; L = L0; P = P0
    k1 = kk[0]; k2 = kk[1]; k3 = kk[2]; k5 = kk[3]; k6 = kk[4]
    k7 = kk[5]; k8 = kk[6]; k10 = kk[8]; k11 = kk[9]
    inv = 1.0 / Omega
    cf = C * inv; vf = V * inv
    a_f = np.exp(-dt / tau_filt)
    frame = 0
    for step in range(n_steps):
        x = C * inv
        f2, f4 = _tails(x)
        nCL = np.random.poisson(k1 * C * dt)
        nCV = np.random.poisson((k2 + k11 * f4) * C * dt)
        nCP = np.random.poisson(k7 * C * dt)
        nCL, nCV, nCP = _clip3(nCL, nCV, nCP, C)
        nVC = np.random.poisson((k10 + k3 * f2) * V * dt)
        if nVC > V:
            nVC = V
        nLV = np.random.poisson(k5 * L * dt)
        nLC = np.random.poisson(k6 * L * dt)
        nLV, nLC, _ = _clip3(nLV, nLC, 0, L)
        nPV = np.random.poisson(k8 * P * dt)
        if nPV > P:
            nPV = P
        C += -nCL - nCV - nCP + nVC + nLC
        V += nCV - nVC + nLV + nPV
        L += nCL - nLV - nLC
        P += nCP - nPV
        cf = a_f * cf + (1.0 - a_f) * (C * inv)
        vf = a_f * vf + (1.0 - a_f) * (V * inv)
        if step >= burn_steps and (step - burn_steps) % n_rec == 0:
            if frame < phase.shape[0]:
                phase[frame] = np.arctan2((vf - vstar) / s_v, (cf - cstar) / s_c)
                frame += 1
    return frame


@njit(cache=True)
def ssa_site(C0, V0, L0, P0, Omega, kk, t_stop, dt_rec, burn_t,
             tau_filt, cstar, vstar, s_c, s_v, phase):
    """Exact Gillespie direct method for one isolated site, same seven channels,
    same filter and phase definition as the leap."""
    C = C0; V = V0; L = L0; P = P0
    k1 = kk[0]; k2 = kk[1]; k3 = kk[2]; k5 = kk[3]; k6 = kk[4]
    k7 = kk[5]; k8 = kk[6]; k10 = kk[8]; k11 = kk[9]
    inv = 1.0 / Omega
    cf = C * inv; vf = V * inv
    t = 0.0
    t_next = burn_t
    frame = 0
    a = np.zeros(7)
    while t < t_stop and frame < phase.shape[0]:
        f2, f4 = _tails(C * inv)
        a[0] = k1 * C
        a[1] = (k2 + k11 * f4) * C
        a[2] = k7 * C
        a[3] = (k10 + k3 * f2) * V
        a[4] = k5 * L
        a[5] = k6 * L
        a[6] = k8 * P
        a0 = 0.0
        for i in range(7):
            a0 += a[i]
        if a0 <= 0.0:
            break
        u = np.random.random()
        if u <= 0.0:
            u = 1e-300
        tau = -np.log(u) / a0
        t_end = t + tau
        cc = C * inv
        vv = V * inv
        # the state is fixed over the dwell, so the filter advances exactly
        while t_next <= t_end and frame < phase.shape[0]:
            af = np.exp(-(t_next - t) / tau_filt)
            cf = af * cf + (1.0 - af) * cc
            vf = af * vf + (1.0 - af) * vv
            phase[frame] = np.arctan2((vf - vstar) / s_v, (cf - cstar) / s_c)
            frame += 1
            t = t_next
            t_next += dt_rec
        af = np.exp(-(t_end - t) / tau_filt)
        cf = af * cf + (1.0 - af) * cc
        vf = af * vf + (1.0 - af) * vv
        t = t_end
        u2 = np.random.random() * a0
        acc = 0.0
        sel = 6
        for i in range(7):
            acc += a[i]
            if u2 < acc:
                sel = i
                break
        if sel == 0:
            C -= 1; L += 1
        elif sel == 1:
            C -= 1; V += 1
        elif sel == 2:
            C -= 1; P += 1
        elif sel == 3:
            V -= 1; C += 1
        elif sel == 4:
            L -= 1; V += 1
        elif sel == 5:
            L -= 1; C += 1
        else:
            P -= 1; V += 1
    return frame


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)
    return np.random.random()
