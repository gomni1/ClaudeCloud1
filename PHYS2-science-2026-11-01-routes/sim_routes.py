"""
PHYS2 routes test, 1 November 2026 -- simulator.

ATTRIBUTION. This file is a verbatim copy of `PHYS2-science-2026-11-01/B/sim_b.py`
from the Part B test of the previous night, reused under the instruction to reuse
that simulator. Source SHA-256:
  7d975c5fc0dc65231c4dc7f174805b11484a08d402d5d198aba1a5123f9c6e17
The source file is unmodified below this header; only this header was added.
No run, delta, count or seed from that Part B enters the present test -- the
fresh seed base is declared in SPEC.md.
"""
"""
PHYS2 Part B -- exact stochastic simulation of switching between the two stable
balances, and of how closely those switching paths approach dissolution.

Gillespie direct method in the Kurtz form: every propensity is Omega*r(n/Omega).
Open level (rules 9 and 12 present). Contact-Void count: x = C/(C+V), with
m = 2 and kr = kc = 2, so F_kr(x) = F_kc(x) = Pr[Bin(2,x) >= 2] = x^2.

Propensities in integer counts:
  1   C->L      k1*nC          2   C->V      k2*nC
  3   V->C      k3*nV*x^2      5   L->V      k5*nL
  6   L->C      k6*nL          7   C->P      k7*nC
  8   P->V      k8*nP          9   P->()     k9*nP
  10  V->C      k10*nV         11  C->V      k11*nC*x^2
  12  ()->V     Omega*k12

D (dissolution) is the set nC = nL = 0.
delta is the closest approach to dissolution, min over the path of (nC+nL)/Omega.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)
    return np.random.random()


@njit(cache=True)
def run_batch(n_runs, nC0, nV0, nL0, nP0, Omega, kk, targetV, tol,
              max_events, out_visitD, out_delta, out_events, out_ok, out_time):
    """Simulate n_runs independent switching runs from one balance to the other.

    Fills, per run: out_visitD (1 if D visited before the target was reached),
    out_delta (min (nC+nL)/Omega over the path, start state included),
    out_events, out_ok (1 if the target was reached within max_events),
    out_time (elapsed model time).
    Returns the number of runs completed.
    """
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = kk
    a = np.zeros(11)
    a12 = Omega * k12

    for r in range(n_runs):
        nC = nC0; nV = nV0; nL = nL0; nP = nP0
        t = 0.0
        visitD = 0
        mn = nC + nL
        if mn == 0:
            visitD = 1
        ev = 0
        ok = 0
        while ev < max_events:
            cv = nC + nV
            if cv > 0:
                x = nC / cv
            else:
                x = 0.0
            x2 = x * x

            a[0] = k1 * nC
            a[1] = k2 * nC
            a[2] = k3 * nV * x2
            a[3] = k5 * nL
            a[4] = k6 * nL
            a[5] = k7 * nC
            a[6] = k8 * nP
            a[7] = k9 * nP
            a[8] = k10 * nV
            a[9] = k11 * nC * x2
            a[10] = a12

            a0 = 0.0
            for i in range(11):
                a0 += a[i]
            if a0 <= 0.0:
                break

            u1 = np.random.random()
            if u1 <= 0.0:
                u1 = 1.0e-300
            t += -np.log(u1) / a0

            u2 = np.random.random() * a0
            acc = 0.0
            sel = 10
            for i in range(11):
                acc += a[i]
                if u2 < acc:
                    sel = i
                    break

            if sel == 0:
                nC -= 1; nL += 1
            elif sel == 1:
                nC -= 1; nV += 1
            elif sel == 2:
                nC += 1; nV -= 1
            elif sel == 3:
                nV += 1; nL -= 1
            elif sel == 4:
                nC += 1; nL -= 1
            elif sel == 5:
                nC -= 1; nP += 1
            elif sel == 6:
                nV += 1; nP -= 1
            elif sel == 7:
                nP -= 1
            elif sel == 8:
                nC += 1; nV -= 1
            elif sel == 9:
                nC -= 1; nV += 1
            else:
                nV += 1

            ev += 1

            s = nC + nL
            if s < mn:
                mn = s
            if s == 0:
                visitD = 1

            # target balance reached?
            if (abs(nC / Omega - 1.0) < tol and abs(nV / Omega - targetV) < tol
                    and abs(nL / Omega - 1.0) < tol and abs(nP / Omega - 0.5) < tol):
                ok = 1
                break

        out_visitD[r] = visitD
        out_delta[r] = mn / Omega
        out_events[r] = ev
        out_ok[r] = ok
        out_time[r] = t
    return n_runs


@njit(cache=True)
def scan_states(nC_arr, nL_arr, Omega):
    """Reference scanner: the delta and passage rules of SPEC §5 applied to a
    complete recorded path. Returns (delta, visitD)."""
    mn = nC_arr[0] + nL_arr[0]
    visitD = 1 if mn == 0 else 0
    for i in range(1, nC_arr.shape[0]):
        s = nC_arr[i] + nL_arr[i]
        if s < mn:
            mn = s
        if s == 0:
            visitD = 1
    return mn / Omega, visitD


@njit(cache=True)
def run_one_record(nC0, nV0, nL0, nP0, Omega, kk, targetV, tol, max_events,
                   recC, recL):
    """One switching run that also records the full (nC,nL) path, for the
    end-to-end consistency check of SPEC §7. Returns
    (streaming_delta, streaming_visitD, n_states_recorded, ok)."""
    k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = kk
    a = np.zeros(11)
    a12 = Omega * k12
    nC = nC0; nV = nV0; nL = nL0; nP = nP0
    visitD = 0
    mn = nC + nL
    if mn == 0:
        visitD = 1
    recC[0] = nC; recL[0] = nL
    ns = 1
    ev = 0
    ok = 0
    cap = recC.shape[0]
    while ev < max_events and ns < cap:
        cv = nC + nV
        x = nC / cv if cv > 0 else 0.0
        x2 = x * x
        a[0] = k1 * nC; a[1] = k2 * nC; a[2] = k3 * nV * x2
        a[3] = k5 * nL; a[4] = k6 * nL; a[5] = k7 * nC
        a[6] = k8 * nP; a[7] = k9 * nP; a[8] = k10 * nV
        a[9] = k11 * nC * x2; a[10] = a12
        a0 = 0.0
        for i in range(11):
            a0 += a[i]
        if a0 <= 0.0:
            break
        u1 = np.random.random()
        if u1 <= 0.0:
            u1 = 1.0e-300
        _ = -np.log(u1) / a0
        u2 = np.random.random() * a0
        acc = 0.0
        sel = 10
        for i in range(11):
            acc += a[i]
            if u2 < acc:
                sel = i
                break
        if sel == 0:
            nC -= 1; nL += 1
        elif sel == 1:
            nC -= 1; nV += 1
        elif sel == 2:
            nC += 1; nV -= 1
        elif sel == 3:
            nV += 1; nL -= 1
        elif sel == 4:
            nC += 1; nL -= 1
        elif sel == 5:
            nC -= 1; nP += 1
        elif sel == 6:
            nV += 1; nP -= 1
        elif sel == 7:
            nP -= 1
        elif sel == 8:
            nC += 1; nV -= 1
        elif sel == 9:
            nC -= 1; nV += 1
        else:
            nV += 1
        ev += 1
        s = nC + nL
        if s < mn:
            mn = s
        if s == 0:
            visitD = 1
        recC[ns] = nC; recL[ns] = nL
        ns += 1
        if (abs(nC / Omega - 1.0) < tol and abs(nV / Omega - targetV) < tol
                and abs(nL / Omega - 1.0) < tol and abs(nP / Omega - 0.5) < tol):
            ok = 1
            break
    return mn / Omega, visitD, ns, ok
