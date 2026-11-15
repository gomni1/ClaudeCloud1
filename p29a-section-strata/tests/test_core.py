"""Regression tests for the main constructions. They pin what the harness found;
they are not proofs."""
import numpy as np
import pytest

from strata import experiments as E
from strata import experiments_h34 as F
from strata import proofs
from strata.loops import connection_rotation, sector_loop, unit_weights
from strata.sections import area_moment, polygon, polygon_moment, rotate, section


@pytest.mark.parametrize("check", proofs.ALL, ids=lambda f: f.__name__)
def test_exact_checks(check):
    assert check()[1]


def test_area_moments_agree_between_smooth_and_fine_polygon():
    z = section(M=5, z2=0.12, z3=0.06j, z4=0.03, z5=0.02 * np.exp(0.4j))
    for a in (2, 3):
        assert abs(area_moment(z, a) - polygon_moment(polygon(z, 4000), a)) < 1e-6


def test_rotation_weight_of_area_moments():
    z = section(M=5, z2=0.12, z3=0.06j, z4=0.03, z5=0.02)
    for a in (2, 3):
        assert abs(area_moment(rotate(z, 0.7), a) - np.exp(1j * a * 0.7) * area_moment(z, a)) < 1e-12


def test_h2a_flip_turns_for_every_map():
    for key, case in E.h2a().items():
        assert all(v == case["expected_turns"] for v in case["jumps_turns"].values()), key
        assert case["middle_section"] != "circle"


def test_h1b_m5_windings_change_at_asymmetric_sections():
    out = E.h1b_m5()
    assert [r["theta_P"] for r in out["rows"]][0] == 1.0
    assert [r["theta_P"] for r in out["rows"]][-1] == 0.0
    for found in out["witnesses"].values():
        assert found
        for w in found:
            assert w["section"]["g"] == 1 and w["section"]["min_d_k"] >= 1e-3


def test_h3_survivor_tables():
    cells = F.h3()
    even = {"C2", "C4"}
    for key, cell in cells.items():
        SA, SB = key.replace("S_A=", "").replace("S_B=", "").split(",")
        assert cell["survive_S"] == (SB in even), key
        assert cell["survive_R"] == (SA in even or SB in even), key
        assert cell["A_could_carry_instead"] == (SA in even), key


def test_retraced_loop_twist_is_weighting_independent():
    shapes = {"A": F.REF["C3"][0], "B": F.REF["C2"][1]}
    g, info = sector_loop(["A", "B", "A"], shapes, [0, 0.5, 0], [0, 1, 0])
    a1 = connection_rotation(g, unit_weights(5), 2000) / (2 * np.pi)
    a2 = connection_rotation(g, np.arange(2, 6, dtype=float) ** 2, 2000) / (2 * np.pi)
    assert info["residual"] < 1e-9
    assert abs(a1 - 0.5) < 1e-6 and abs(a2 - 0.5) < 1e-6


def test_h4a_one_odd_mode_parity_is_invariant_and_map_independent():
    out = F.h4a_one_odd()
    for row in out["A-B+-A"]:
        assert row["N_3"] == 3.0 and row["arc_max_d2"] == 0.0
        assert row["sum_theta_P"] % 2 == row["sum_theta_Pprime"] % 2 == row["sum_theta_M"] % 2 == 1
    for row in out["B+-A-B-"]:
        assert row["N_3"] == 0.0


def test_h4a_two_odd_modes_resolutions_are_joined_in_v_free():
    out = F.h4a_two_odd()
    rows = out["rows"]
    assert rows[0]["theta_P"] != rows[-1]["theta_P"]
    assert min(r["min_d_C2"] for r in rows) > 1e-3
    for found in out["witnesses"].values():
        for w in found:
            assert w["section"]["g"] == 1
