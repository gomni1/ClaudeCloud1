"""Harness tests for K3 (SPEC K3: H1, H2, P1-P3) and a K2/K1 smoke check."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import k3  # noqa: E402


def test_p1_renewal():
    assert k3.p1()["passed"]


def test_p3_scripted_stalls():
    r = k3.p3()
    assert r["n_found"] == r["n_expected"] and r["phases_found"] == r["phases_expected"]


def test_h1_drift():
    assert k3.h1()["passed"]


def test_h2_exact_omega5():
    assert k3.h2(5)["passed"]


def test_h2_exact_omega10():
    assert k3.h2(10)["passed"]


def test_p2_quasicycles_fail_s1():
    assert k3.p2()["s1_fails"]
