"""
PHYS2 Part A -- exact stochastic simulation of the well-mixed grammar.

Gillespie direct method in the Kurtz form: every propensity is Omega * r(n/Omega),
with r the deterministic rate law in concentrations. For this grammar every
propensity reduces to a function of the integer counts alone (see below), so the
simulation is exact -- no tau-leaping, no time discretisation.

Roles are C, V, L, P with counts nC, nV, nL, nP and Omega the ensemble size.
x = C/(C+V+L+P)   (all-neighbours count, Part A)
F_j(x) = Pr[Bin(m, x) >= j]

Transitions, stoichiometry and propensity (Kurtz form):
  1   C->L            (-1, 0,+1, 0)   k1*nC
  2   C->V            (-1,+1, 0, 0)   k2*nC
  3   V+C->2C         (+1,-1, 0, 0)   k3*nV*F_kr(x)
  5   L->V            ( 0,+1,-1, 0)   k5*nL
  6   L->C            (+1, 0,-1, 0)   k6*nL
  7   C->P            (-1, 0, 0,+1)   k7*nC
  8   P->V            ( 0,+1, 0,-1)   k8*nP
  9   P->()           ( 0, 0, 0,-1)   k9*nP            (open level only)
  10  V->C            (+1,-1, 0, 0)   k10*nV
  11  2C->V+C         (-1,+1, 0, 0)   k11*nC*F_kc(x)
  12  ()->V           ( 0,+1, 0, 0)   Omega*k12        (open level only)

The closed level omits 9 and 12, so N = nC+nV+nL+nP is conserved exactly.
"""
import numpy as np
from numba import njit

# transition order used throughout: indices 0..10 map to rules 1,2,3,5,6,7,8,9,10,11,12
STOICH = np.array([
    [-1,  0,  1,  0],   # 1  C->L
    [-1,  1,  0,  0],   # 2  C->V
    [ 1, -1,  0,  0],   # 3  V+C->2C
    [ 0,  1, -1,  0],   # 5  L->V
    [ 1,  0, -1,  0],   # 6  L->C
    [-1,  0,  0,  1],   # 7  C->P
    [ 0,  1,  0, -1],   # 8  P->V
    [ 0,  0,  0, -1],   # 9  P->()
    [ 1, -1,  0,  0],   # 10 V->C
    [-1,  1,  0,  0],   # 11 2C->V+C
    [ 0,  1,  0,  0],   # 12 ()->V
], dtype=np.int64)


@njit(cache=True, inline='always')
def _ftail(j, m, x, binom):
    """Pr[Bin(m,x) >= j] by direct summation of the upper tail."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    s = 0.0
    for i in range(j, m + 1):
        s += binom[i] * x ** i * (1.0 - x) ** (m - i)
    if s < 0.0:
        s = 0.0
    elif s > 1.0:
        s = 1.0
    return s


@njit(cache=True, inline='always')
def _nearest(cycS, y, coarse):
    """Nearest point of the scaled deterministic cycle: coarse scan + local refine.

    Returns (distance, phase) with phase the arc-time fraction in [0,1).
    """
    M = cycS.shape[0]
    best = 1.0e300
    bi = 0
    i = 0
    while i < M:
        s = 0.0
        for j in range(4):
            dd = cycS[i, j] - y[j]
            s += dd * dd
        if s < best:
            best = s
            bi = i
        i += coarse
    lo = bi - coarse
    hi = bi + coarse
    for i in range(lo, hi + 1):
        ii = i % M
        s = 0.0
        for j in range(4):
            dd = cycS[ii, j] - y[j]
            s += dd * dd
        if s < best:
            best = s
            bi = ii
    return np.sqrt(best), bi / M


@njit(cache=True)
def run_until_time(n, kk, m, kr, kc, is_open, Omega, binom, t_stop):
    """Advance the chain from t=0 to the last event time <= t_stop.

    Used only by the P3 planted check (SPEC §10). Same propensities and same
    direct-method step as run_chunk; no cycle geometry is computed.
    Returns the elapsed model time.
    """
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = kk
    a = np.zeros(11)
    t = 0.0
    while True:
        nC = n[0]; nV = n[1]; nL = n[2]; nP = n[3]
        tot = nC + nV + nL + nP
        x = nC / tot if tot > 0 else 0.0
        Fr = _ftail(kr, m, x, binom)
        Fc = _ftail(kc, m, x, binom)
        a[0] = k1 * nC; a[1] = k2 * nC; a[2] = k3 * nV * Fr
        a[3] = k5 * nL; a[4] = k6 * nL; a[5] = k7 * nC
        a[6] = k8 * nP; a[7] = k9 * nP * is_open; a[8] = k10 * nV
        a[9] = k11 * nC * Fc; a[10] = Omega * k12 * is_open
        a0 = 0.0
        for i in range(11):
            a0 += a[i]
        if a0 <= 0.0:
            break
        u1 = np.random.random()
        if u1 <= 0.0:
            u1 = 1.0e-300
        tau = -np.log(u1) / a0
        if t + tau > t_stop:
            break
        t += tau
        u2 = np.random.random() * a0
        acc = 0.0
        sel = 10
        for i in range(11):
            acc += a[i]
            if u2 < acc:
                sel = i
                break
        if sel == 0:
            n[0] -= 1; n[2] += 1
        elif sel == 1:
            n[0] -= 1; n[1] += 1
        elif sel == 2:
            n[0] += 1; n[1] -= 1
        elif sel == 3:
            n[1] += 1; n[2] -= 1
        elif sel == 4:
            n[0] += 1; n[2] -= 1
        elif sel == 5:
            n[0] -= 1; n[3] += 1
        elif sel == 6:
            n[1] += 1; n[3] -= 1
        elif sel == 7:
            n[3] -= 1
        elif sel == 8:
            n[0] += 1; n[1] -= 1
        elif sel == 9:
            n[0] -= 1; n[1] += 1
        else:
            n[1] += 1
    return t


@njit(cache=True)
def run_chunk(n, aux, kk, m, kr, kc, is_open, Omega, binom, cycS, invsig,
              R, t_burn, occ, occ_armed, exits, exit_phase_log, max_events, max_exits):
    """Advance the chain by at most max_events reactions.

    n    : int64[4] counts (nC,nV,nL,nP), updated in place
    aux  : float64[4] = (t, armed, half_phase, n_exits_total), updated in place
    occ  : float64[10] time in each phase bin while d < R          (post burn-in)
    occ_armed : float64[10] same but only while additionally armed (secondary)
    exits: float64[10] exit counts by the phase of the last d<R/2 moment
    Returns (events_done, exits_this_chunk).
    """
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = kk
    a = np.zeros(11)
    y = np.zeros(4)
    coarse = 16

    t = aux[0]
    armed = aux[1]
    half_ph = aux[2]
    nex = aux[3]

    # state descriptors for the current (piecewise-constant) state
    for j in range(4):
        y[j] = n[j] * invsig[j] / Omega
    d, ph = _nearest(cycS, y, coarse)

    ev = 0
    ex0 = nex
    while ev < max_events and (nex - ex0) < max_exits:
        nC = n[0]; nV = n[1]; nL = n[2]; nP = n[3]
        tot = nC + nV + nL + nP
        x = nC / tot if tot > 0 else 0.0
        Fr = _ftail(kr, m, x, binom)
        Fc = _ftail(kc, m, x, binom)

        a[0] = k1 * nC
        a[1] = k2 * nC
        a[2] = k3 * nV * Fr
        a[3] = k5 * nL
        a[4] = k6 * nL
        a[5] = k7 * nC
        a[6] = k8 * nP
        a[7] = k9 * nP * is_open
        a[8] = k10 * nV
        a[9] = k11 * nC * Fc
        a[10] = Omega * k12 * is_open

        a0 = 0.0
        for i in range(11):
            a0 += a[i]
        if a0 <= 0.0:
            break

        u1 = np.random.random()
        if u1 <= 0.0:
            u1 = 1.0e-300
        tau = -np.log(u1) / a0

        # occupancy accrues over the dwell in the current state
        if t >= t_burn and d < R:
            b = int(ph * 10.0)
            if b > 9:
                b = 9
            occ[b] += tau
            if armed > 0.5:
                occ_armed[b] += tau

        t += tau

        # choose the reaction
        u2 = np.random.random() * a0
        acc = 0.0
        sel = 10
        for i in range(11):
            acc += a[i]
            if u2 < acc:
                sel = i
                break
        if sel == 0:
            n[0] -= 1; n[2] += 1
        elif sel == 1:
            n[0] -= 1; n[1] += 1
        elif sel == 2:
            n[0] += 1; n[1] -= 1
        elif sel == 3:
            n[1] += 1; n[2] -= 1
        elif sel == 4:
            n[0] += 1; n[2] -= 1
        elif sel == 5:
            n[0] -= 1; n[3] += 1
        elif sel == 6:
            n[1] += 1; n[3] -= 1
        elif sel == 7:
            n[3] -= 1
        elif sel == 8:
            n[0] += 1; n[1] -= 1
        elif sel == 9:
            n[0] -= 1; n[1] += 1
        else:
            n[1] += 1

        for j in range(4):
            y[j] = n[j] * invsig[j] / Omega
        d, ph = _nearest(cycS, y, coarse)

        # arming / exit logic, evaluated at the new state
        if d < 0.5 * R:
            armed = 1.0
            half_ph = ph
        elif d > R and armed > 0.5:
            armed = 0.0
            if t >= t_burn:
                b = int(half_ph * 10.0)
                if b > 9:
                    b = 9
                exits[b] += 1.0
                idx = int(nex)
                if idx < exit_phase_log.shape[0]:
                    exit_phase_log[idx] = half_ph
                nex += 1.0

        ev += 1

    aux[0] = t
    aux[1] = armed
    aux[2] = half_ph
    aux[3] = nex
    return ev, int(nex - ex0)
