"""M0: balances, stability, lambda_slow, drift check (SPEC §5)."""
import numpy as np
import pytest

from gexit import model, sim


def test_ma_balance_formula():
    b = model.balance_ma()
    assert np.allclose(b, [1.0, 0.5, 1.0, 0.5], atol=1e-15)
    assert model.A_CONST == 11.0
    assert np.abs(model.drift(b, "MA")).max() < 1e-12


def test_th_three_balances_and_identity():
    bs = model.balances_th()
    assert len(bs) == 3
    assert np.allclose([b[1] for b in bs], [2.0, 3.0, 4.0], atol=1e-12)
    for b in bs:
        assert np.allclose(b[[0, 2, 3]], [1.0, 1.0, 0.5])
        assert np.abs(model.drift(b, "TH")).max() < 1e-12
    for y in np.linspace(0.1, 10, 50):
        assert model.S_minus_A(y) == pytest.approx((y - 2) * (y - 3) * (y - 4) / (1 + y) ** 2, abs=1e-12)


def test_stability_and_saddle():
    ev = np.linalg.eigvals(model.jacobian(model.balance_ma(), "MA"))
    assert np.all(ev.real < 0)
    b2, b3, b4 = model.balances_th()
    assert np.all(np.linalg.eigvals(model.jacobian(b2, "TH")).real < 0)
    assert np.all(np.linalg.eigvals(model.jacobian(b4, "TH")).real < 0)
    e3 = np.linalg.eigvals(model.jacobian(b3, "TH")).real
    assert np.sum(e3 > 0) == 1
    assert e3.max() == pytest.approx(0.30, abs=0.01)


def test_lambda_slow_matches_hand_values():
    hand = {"MA": -0.188, "TH2": -0.153, "TH4": -0.128}
    for s, h in hand.items():
        lam = model.lambda_slow(model.BAL[s], model.LAW_OF[s])
        assert abs(lam.imag) < 1e-12
        assert lam.real == pytest.approx(h, abs=0.005)
        assert model.burn_in_time(s) == pytest.approx(10 / abs(lam.real))


def test_jacobian_matches_finite_differences():
    x = np.array([0.7, 1.3, 0.9, 0.4])
    for law in model.LAWS:
        h = 1e-6
        Jf = np.array([(model.drift(x + h * e, law) - model.drift(x - h * e, law)) / (2 * h) for e in np.eye(4)]).T
        assert np.allclose(model.jacobian(x, law), Jf, atol=1e-7)


@pytest.mark.parametrize("om", [10, 1000])
def test_drift_identity_through_c_propensities(om):
    rng = np.random.default_rng(om)
    for _ in range(300):
        n = rng.integers(0, 4 * om, size=4)
        for law in model.LAWS:
            f = sim.propensities(law, om, n) @ model.NU / om
            assert np.allclose(f, model.drift(n / om, law), rtol=1e-12, atol=1e-12)
        # R1: difference is exactly k11 * (nC / Omega) / Omega along nu_11
        f = sim.propensities("MAC", om, n) @ model.NU / om
        exp = model.drift(n / om, "MA") - model.KVEC[9] * (n[0] / om) / om * model.NU[9]
        assert np.allclose(f, exp, rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("law", model.LAWS)
def test_large_omega_trajectory_follows_ode(law):
    """The preregistered check (b), with the seed used for evidence/m0.json."""
    om = 1e5
    x0 = np.array([0.5, 1.0, 1.5, 1.0])
    times = np.array([0.5, 1.0, 2.0, 5.0])
    traj, _ = sim.run_traj(law, om, model.round_half_up(om * x0), times, sim.seed_for("M0", law))
    sol = model.integrate(x0, law, 5.0, t_eval=times)
    assert np.abs(traj / om - sol.y.T).max() <= 0.02


@pytest.mark.parametrize("law", model.LAWS)
def test_large_omega_ensemble_mean_follows_ode(law):
    """Diagnostic beyond the preregistered single trajectory: under TH a single trajectory
    diffuses along the weakly damped v direction (sd of v ~ 0.04 at t = 5 for Omega = 1e5),
    so the single-trajectory 0.02 check is seed-dependent; the mean over seeds follows the ODE."""
    om = 1e5
    x0 = np.array([0.5, 1.0, 1.5, 1.0])
    times = np.array([0.5, 1.0, 2.0, 5.0])
    sol = model.integrate(x0, law, 5.0, t_eval=times)
    tr = np.array([sim.run_traj(law, om, model.round_half_up(om * x0), times, s)[0] / om for s in range(32)])
    se = tr.std(axis=0, ddof=1) / np.sqrt(len(tr))
    assert np.all(np.abs(tr.mean(axis=0) - sol.y.T) <= 4 * se + 1e-3)


@pytest.mark.parametrize("law", model.LAWS)
def test_random_starts_reach_a_stable_balance(law):
    rng = np.random.default_rng(3)
    stab = [model.balance_ma()] if law == "MA" else [model.BAL["TH2"], model.BAL["TH4"]]
    for _ in range(20):
        e = model.integrate(rng.uniform(0, 3, 4), law, 3000.0).y[:, -1]
        assert min(np.linalg.norm(e - b) for b in stab) < 1e-6
