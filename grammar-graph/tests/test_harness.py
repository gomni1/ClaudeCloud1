"""pytest: H1 (as revised in R1: N = 10^6, shortened run), H2, H3, P1, P2, P3 (SPEC section 5; reduced sizes)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from g1 import h1, h2, h3, p1, p2_on, p3  # noqa: E402
from gg.core import graph_S, planted_sphere, seed_of  # noqa: E402


def test_h1_mean_field_large_N():
    r = h1(N=10 ** 6, periods=40, discard=10, seed=seed_of("test", "H1"))
    assert r["PASS"], r


def test_h2_independent_chains():
    r = h2(graph_S(2000, seed_of("test", "S")), N=2000)
    assert r["PASS"], r


def test_h3_octahedron_exact():
    r = h3(t_max=5e4)
    assert r["PASS"], r


def test_p1_planted_defects():
    r = p1(n_random=10, seed=seed_of("test", "P1"))
    assert r["PASS"], r


def test_p2_planted_noise():
    r = p2_on(planted_sphere(60), "test", nframes=1000)
    assert r["PASS"] and r["d1_criterion"] == "FAILS", r


def test_p3_planted_motion():
    r = p3()
    assert r["PASS"], r
