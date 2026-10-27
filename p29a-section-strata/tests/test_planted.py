"""The three planted failures of SPEC section 4. Each test passes only if the
harness catches the planted defect."""
import numpy as np
import pytest

from strata.loops import find_passages
from strata.orientation import (LiftError, lift_samples, theta_M, theta_P,
                                theta_R, validate_lift, wrap)
from strata.sections import classify, section
from strata.proofs import check_pf3_exact

T_STAR = 1.2345
EPS = 0.05
KAPPA = 0.8


def hidden_c2_loop(t):
    """M = 5; (z3, z5) vanish together only at t = T_STAR, between grid points."""
    w = EPS * (np.exp(1j * (t - T_STAR)) - 1)
    return np.array([0.15 * np.exp(2j * t), w, 0.04 * np.exp(4j * t), w * np.exp(1j * KAPPA)])


def test_pf1_hidden_c2_passage_is_found():
    passages, grid_min = find_passages(hidden_c2_loop, k=2, n=256, tol=1e-9)
    assert grid_min > 1e-9, "the planted passage must be invisible on the grid"
    assert len(passages) == 1
    t, d = passages[0]
    assert abs(t - T_STAR) < 1e-6 and d < 1e-9


def test_pf1_no_false_passage_on_a_free_loop():
    free = lambda t: hidden_c2_loop(t) + np.array([0, 0.01, 0, 0])
    passages, _ = find_passages(free, k=2, n=256, tol=1e-9)
    assert passages == []


def test_pf2_artificial_2pi_jump_is_rejected():
    true = np.linspace(0, 4 * np.pi, 400)
    raw = wrap(true)
    good = lift_samples(raw)
    assert validate_lift(raw, good)[0]
    planted = good.copy()
    planted[150:] += 2 * np.pi
    ok, why = validate_lift(raw, planted)
    assert not ok and "jumps" in why


def test_pf2_undersampled_step_is_flagged():
    raw = wrap(np.array([0.0, 0.5, 0.5 + 2.0, 3.0]))   # one true step of 2 > pi/2
    with pytest.raises(LiftError):
        lift_samples(raw)


def test_pf3_near_c2_section_respects_tolerance():
    z = section(M=5, z2=0.15, z3=1e-7, z4=0.04, z5=1e-7)
    tight = classify(z, tol=1e-9)
    assert tight["stratum"] == "C1" and 2 in tight["near"]
    assert classify(z, tol=1e-6)["stratum"] == "C2"
    assert theta_P(z) is None and theta_R(z) is None and theta_M(z) is None
    assert check_pf3_exact()[1]
