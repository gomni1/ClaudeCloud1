"""Tests for PF1 (via FFS), PF5, PF6, the FFS harness and the family identity (SPEC §1, §3, §4)."""
import json
import math
import os

import numpy as np
import pytest

from idsize import family, ffs, planted, race

EV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence")


def test_family_identity_and_balances():
    m0 = family.m0()
    assert m0["identity_residual"] == "0"
    for k10, row in m0["per_k10"].items():
        for v in ("2.0", "3.0", "4.0"):
            assert row["balances"][v]["residual"] < 1e-12
        assert row["balances"]["2.0"]["max_re"] < 0 < row["balances"]["3.0"]["max_re"]
        assert row["balances"]["4.0"]["max_re"] < 0
    # disclosed values (brief), two decimals
    assert m0["per_k10"]["1.0"]["balances"]["3.0"]["max_re"] == pytest.approx(0.295, abs=2e-3)


def test_interface_rule():
    MA, Ms = ffs.interfaces(16)
    assert MA == 32 and Ms[0] == 32 - 8 and Ms[-1] == 0
    assert all(a > b for a, b in zip(Ms, Ms[1:]))


def test_pf5_race_estimators():
    assert planted.pf5()["pass_"]


def test_pf6_crossover():
    r = planted.pf6()
    assert r["pass_"], r["windows"]


def test_ffs_pf1_small():
    """FFS on immigration-death at Omega = 12 against the exact MFPT (fast version of H-b)."""
    from gexit_pr3 import planted as p3
    ex = p3.pf1_exact(12)["T_qsd"]
    r = ffs.run_size("ID", 12, np.zeros(11), np.array([12, 0, 0, 0], np.int64), 10.0, 77, replicates=4,
                     basin_mult=1.0)
    assert abs(r["T"] - ex) / ex < 0.15


@pytest.mark.skipif(not os.path.exists(os.path.join(EV, "harness.json")), reason="run python run_b.py harness first")
def test_recorded_harness():
    h = json.load(open(os.path.join(EV, "harness.json")))
    for row in h["rows"]:
        assert row["z"] is not None
    assert len(h["pf1"]["rows"]) == 2


def test_clopper_pearson():
    lo, hi = race.clopper_pearson(5, 1000)
    assert lo < 0.005 < hi
