"""Planted failures PFA1-PFA4 (SPEC §9)."""
import math

import numpy as np
from scipy.integrate import solve_ivp

from . import integ, m3, model

D_C_SCHNAKENBERG = (5.6 + math.sqrt(28.8)) / 1.28
J_SCHNAKENBERG = np.array([[0.8, 1.0], [-1.8, -1.0]])
J_PFA4 = np.array([[0.1, -1.0, -1.0], [1.0, 0.1, 0.0], [1.0, 0.0, -1.0]])


def brusselator_reference_period(a=1.0, b=3.0, n=20):
    """Independent reference: Radau rtol 1e-12, mean of n returns to x = a with dx > 0."""
    def f(t, z):
        x, y = z
        return [a - (b + 1) * x + x * x * y, b * x - x * x * y]

    sol = solve_ivp(f, (0, 200), [1.0, 1.0], method="Radau", rtol=1e-12, atol=1e-14)  # settle on the cycle
    z0 = sol.y[:, -1]

    def ev(t, z):
        return z[0] - a

    ev.direction = 1.0
    sol = solve_ivp(f, (0, 30 * (n + 2)), z0, method="Radau", rtol=1e-12, atol=1e-14, events=ev)
    t = sol.t_events[0]
    return float(np.mean(np.diff(t[1:n + 2])))


def pfa1(n_starts=8):
    par = model.make_par(np.zeros(11), model=1, extra=(1.0, 3.0))
    rng = np.random.default_rng(1)
    starts = rng.uniform(0.2, 4.0, (n_starts, 2))
    runs = integ.run_starts(par, starts, [np.array([1.0, 3.0])], [], 1e3)
    ref = brusselator_reference_period()
    kinds = [r["class"]["kind"] for r in runs]
    periods = [r["class"].get("period") for r in runs]
    ok = all(k == "periodic" for k in kinds) and all(abs(p - ref) / ref <= 0.01 for p in periods)
    return dict(kinds=kinds, periods=periods, reference=ref, pass_=bool(ok))


def pfa2():
    par = model.make_par(np.zeros(11), model=2, extra=(1e-4, 0.0))
    full = integ.run_starts(par, np.array([[1.0, 0.0]]), [np.zeros(2)], [], 1e3 / 1e-4)[0]["class"]
    stage = integ.classify_end(np.array([1.0, 0.0]), par, [np.zeros(2)], 1e3)
    ok = full["kind"] != "periodic" and stage["kind"] != "periodic"
    return dict(full=full, poincare_stage=stage, pass_=bool(ok))


def pfa3():
    pm = m3.pmatrix_test(J_SCHNAKENBERG)
    mt = m3.mobility_tests(J_SCHNAKENBERG, two_class_index=1)
    rc = mt.get("critical_rho", dict(found=False))
    err = abs(rc["rho_c"] - D_C_SCHNAKENBERG) / D_C_SCHNAKENBERG if rc.get("found") else None
    ok = (not pm["is_P"]) and mt["two_class"]["stat"]["stat_hit"] and err is not None and err <= 1e-3
    return dict(pmatrix=pm, stat_hit=mt["two_class"]["stat"]["stat_hit"], critical=rc, exact=D_C_SCHNAKENBERG,
                rel_err=err, pass_=bool(ok))


def pfa4():
    ev = np.linalg.eigvals(J_PFA4)
    mt = m3.mobility_tests(J_PFA4, two_class_index=1)
    return dict(J_eigs=[[float(z.real), float(z.imag)] for z in ev], hurwitz=bool(np.all(ev.real < 0)),
                Gamma=mt["random"]["osc"]["Gamma"], D=mt["random"]["osc"]["D"], s=mt["random"]["osc"].get("s_ref"),
                pass_=bool(mt["random"]["osc"]["osc_hit"]))
