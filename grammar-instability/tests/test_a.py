"""Tests for M0 and PFA1-PFA4 (SPEC §2, §9)."""
import numpy as np
import pytest
import sympy as sp

from ginst import m2, model, planted, symbolic


def test_astra_balances_and_stability():
    p = model.make_par(model.ASTRA, "MA")
    (r,) = model.classify_balances(p)
    assert np.allclose(r["b"], [1, 0.5, 1, 0.5]) and r["stable"]
    p = model.make_par(model.ASTRA, "TH", "cv", "open", 2, 2, 2)
    rs = model.classify_balances(p)
    assert np.allclose([r["b"][1] for r in rs], [2, 3, 4])
    assert [r["stable"] for r in rs] == [True, False, True]
    assert np.max(rs[1]["eig"].real) == pytest.approx(0.2953, abs=1e-3)


@pytest.mark.parametrize("variant", m2.VARIANTS)
def test_balances_are_zeros_and_jacobian_matches_fd(variant):
    for i in range(12):
        d = m2.draw_params(4 * i + m2.VARIANTS.index(variant))
        par = m2.par_of(d)
        for b in model.balances(par):
            f = model.f_np(b, par)
            assert np.abs(f).max() <= 1e-8 * (1 + np.abs(b).max()) * max(d["k"])
            if variant[0] == "closed":
                assert b.sum() == pytest.approx(d["T"], rel=1e-10)
            J = model.J_np(b, par)
            hh = 1e-7 * np.maximum(np.abs(b), 1e-12)
            Jf = np.column_stack([(model.f_np(b + hh[j] * np.eye(4)[j], par) - model.f_np(b - hh[j] * np.eye(4)[j], par))
                                  / (2 * hh[j]) for j in range(4)])
            assert np.allclose(J, Jf, rtol=1e-4, atol=1e-6 * np.abs(J).max())


def test_m0_open_cv_det_is_h_times_positive():
    J = symbolic.J_general(symbolic.A - symbolic.y * symbolic.h, symbolic.h)
    det = sp.factor(sp.simplify((-J).det()))
    q = sp.simplify(det / symbolic.h)
    s, num, den, nneg = symbolic.poly_sign(q, list(symbolic.RATES[:10]) + [symbolic.y])
    assert s == "positive"


def test_m1_general_cv_minor():
    M = -symbolic.J_general(symbolic.gC, symbolic.gV)
    assert sp.simplify(M.extract([0, 1], [0, 1]).det() - symbolic.gV * (symbolic.k1 + symbolic.k7)) == 0


def test_pfa1_brusselator_periodic():
    r = planted.pfa1()
    assert r["pass_"], r


def test_pfa2_focus_not_periodic():
    assert planted.pfa2()["pass_"]


def test_pfa3_schnakenberg():
    r = planted.pfa3()
    assert r["pass_"] and r["rel_err"] < 1e-3


def test_pfa4_wave():
    r = planted.pfa4()
    assert r["hurwitz"] and r["pass_"]
