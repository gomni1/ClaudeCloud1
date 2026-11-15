"""PF1-PF4 (SPEC §9) and the gMAM validations G1, G2."""
import numpy as np
import pytest

from gexit import gmam, planted, stats


@pytest.fixture(scope="module")
def pf1():
    return planted.evaluate_pf1(planted.run_pf1(log=lambda m: None), B=500)


def test_pf1_exact_two_ways():
    for om in planted.PF1_GRID:
        e = planted.pf1_exact(om)
        assert e["T_qsd"] == pytest.approx(e["T_sum"], rel=1e-8)


def test_pf1_coverage(pf1):
    assert pf1["pass_coverage"]


@pytest.mark.xfail(strict=True, reason="PF1 W recovery fails on the preregistered grid (W = 0.924); "
                                       "on the record in RESULTS.md")
def test_pf1_w_recovery(pf1):
    assert pf1["pass_W"]


def test_pf1_fit_to_exact_values_is_biased_low():
    om = np.array(planted.PF1_GRID, float)
    T = np.array([planted.pf1_exact(o)["T_qsd"] for o in om])
    f = stats.fit_EP(om, T, np.full(len(om), 0.03))
    assert 0.94 < f["W"] < 0.96  # the model-E form itself is about 5% low on this grid


def test_pf2_not_passed_as_exponential():
    e = planted.evaluate_pf2(planted.run_pf2(log=lambda m: None), B=500)
    assert e["pass_"]
    for r in e["rows"]:
        assert r["T_hat"] == pytest.approx(r["T_exact"], rel=0.1)


def test_pf3_censored_mle_and_naive_mean():
    r = planted.run_pf3()
    assert 0.25 < r["cens_frac"] < 0.35
    assert r["pass_mle"]
    assert r["pass_naive_low"]


def test_pf4_ageing_rejected():
    assert planted.run_pf4()["pass"]


def test_lilliefors_accepts_exponential():
    rng = np.random.default_rng(5)
    assert stats.lilliefors_exp(rng.exponential(2.0, 1000), B=2000, rng=1)["p"] > 0.01


def test_gmam_g1_immigration_death():
    r = gmam.gmam(gmam.immigration_death(1), [1.0], [0.0], [False], log=lambda m: None)
    assert r["converged"] and r["W"] == pytest.approx(1.0, rel=0.01)


def test_gmam_g2_two_copies():
    r = gmam.gmam(gmam.immigration_death(2), [1.0, 1.0], [0.0, 0.0], [False, False], log=lambda m: None)
    assert r["converged"] and r["W"] == pytest.approx(2.0, rel=0.01)


def test_gmam_free_end_point():
    r = gmam.gmam(gmam.immigration_death(2), [1.0, 1.0], [0.0, 0.5], [False, True], log=lambda m: None)
    assert r["converged"] and r["W"] == pytest.approx(1.0, rel=0.01)
    assert r["path"][-1][1] == pytest.approx(1.0, abs=0.01)


def test_gmam_numba_kernel_matches_numpy():
    from gexit import gmam_nb
    rng = np.random.default_rng(2)
    for law in ("MA", "TH"):
        net = gmam.grammar(law)
        x = rng.uniform(0.05, 3, (100, 4))
        y = rng.normal(0, 0.02, (100, 4))
        l1, _, _ = gmam.local_action(net, x, y)
        l2, _, _, _, st = gmam_nb.local_action(net.nb_id, gmam_nb.KV, net.nu, x, y, np.zeros_like(y),
                                               np.zeros(100), 1e-12)
        assert not st.any()
        assert np.allclose(l1, l2, rtol=1e-6, atol=1e-12)
