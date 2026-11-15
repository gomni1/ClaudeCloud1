"""Post-freeze tests prompted by the proof audit of 27 Oct (see RESULTS.md,
"Proof audit"). They change no frozen claim's status."""
import numpy as np

from strata.audit import (RHO_A, RHO_B_C3, free_passage_loop, on_b_arc, passage,
                          retraced_loop)
from strata.loops import TWO_PI, connection_rotation, stratum_audit
from strata.orientation import winding

M3_UNIT = np.ones(2)
M3_SQUARE = np.array([4.0, 9.0])

# Expected values from Claude's standalone check of 27 Oct (audit file, 4.3)
WITNESS = {0.0: ("flip", [2, 1], 3), 0.3: ("no flip", [1], 2), -0.3: ("no flip", [2], 4),
           np.pi / 2: ("no flip", [1], 2), np.pi: ("no flip", [1], 2)}


def _z3_phase(z):
    return None if abs(z[1]) < 1e-6 else float(np.angle(z[1]))


def test_p6c_exactly_retraced_aba_loop_exists():
    gamma, gap = retraced_loop()
    assert gap < 1e-12                                       # R_pi rho_B = rho_B
    assert np.linalg.norm(gamma(0.0) - gamma(TWO_PI - 1e-12)) < 1e-9   # closes
    assert np.linalg.norm(gamma(0.0) - RHO_A) < 1e-15
    for w in (M3_UNIT, M3_SQUARE):
        assert abs(connection_rotation(gamma, w, 2000) / TWO_PI - 0.5) < 1e-6
    assert stratum_audit(gamma, 2000)["circle"] > 0.3        # avoids the circle
    # control: with rho_B in C3 the joint tears
    _, gap_c3 = retraced_loop(rho_B=RHO_B_C3)
    assert gap_c3 > 0.5


def test_p7_free_passage_witness():
    ts = TWO_PI * (np.arange(4000) + 0.5) / 4000
    for psi, (kind, degs, n3) in WITNESS.items():
        raw = free_passage_loop(psi)
        for t in ts:
            z = raw(t)
            if on_b_arc(t):
                assert z[1] == 0 and abs(z[0]) > 0.3          # B held in C2
            else:
                assert abs(z[0]) > 0 and abs(z[1]) > 0        # V_free off the arc
        delta, flip, detours = passage(psi)
        assert ("flip" if flip else "no flip") == kind, psi
        got = []
        for d in detours:
            res = free_passage_loop(psi, detour=d)
            assert stratum_audit(res, 2000)["C2"] > 1e-3      # resolution avoids C2
            W, err = winding(_z3_phase, res)
            assert err < 1e-9
            got.append(round(W))
        assert got == degs, (psi, got)
        assert 2 * np.mean(got) == n3, psi
