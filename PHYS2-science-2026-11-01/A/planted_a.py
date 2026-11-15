"""Part A planted checks P1, P2, P3 (SPEC §10). All must pass before results count."""
import os, sys, json
import numpy as np
from math import comb
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from models_a import MODELS, get_cycle, initial_counts
from sim_a import run_until_time
from driver_a import _seed

NBIN = 10
PHI_C = (np.arange(NBIN) + 0.5) / NBIN


def chi2_from_bins(obs, occ):
    """Chi-square of exits-per-bin against expectation from occupancy, 9 d.o.f."""
    obs = np.asarray(obs, float)
    occ = np.asarray(occ, float)
    exp = obs.sum() * occ / occ.sum()
    stat = float(((obs - exp) ** 2 / exp).sum())
    p = float(chi2dist.sf(stat, NBIN - 1))
    return stat, p, exp


def fit_modulation(haz):
    """Least-squares fit of a*(1 + b*cos(2*pi*phi - c)) via the linear form
    h = a + A*cos + B*sin. Returns b_hat."""
    X = np.column_stack([np.ones(NBIN), np.cos(2 * np.pi * PHI_C), np.sin(2 * np.pi * PHI_C)])
    coef, *_ = np.linalg.lstsq(X, np.asarray(haz, float), rcond=None)
    a, A, B = coef
    return float(np.hypot(A, B) / a)


def sample_cos_phases(n, b, rng):
    """Rejection sampling from density proportional to 1 + b*cos(2*pi*phi)."""
    out = np.empty(n)
    k = 0
    while k < n:
        u = rng.random(2 * n)
        v = rng.random(2 * n) * (1.0 + abs(b))
        acc = u[(v <= 1.0 + b * np.cos(2 * np.pi * u))]
        take = min(n - k, acc.size)
        out[k:k + take] = acc[:take]
        k += take
    return out


def p1(n_exits=2000, seed=101):
    rng = np.random.default_rng(seed)
    ph = sample_cos_phases(n_exits, 0.5, rng)
    obs = np.histogram(ph, bins=NBIN, range=(0, 1))[0]
    occ = np.full(NBIN, 0.1)                      # uniform occupancy
    stat, p, _ = chi2_from_bins(obs, occ)
    b_hat = fit_modulation(obs / occ)
    # bin-averaging attenuates a cosine by sinc(1/NBIN); the SPEC tolerance is on b itself
    ok = (p < 0.05) and (abs(b_hat - 0.5) / 0.5 <= 0.20)
    return dict(check="P1", n_exits=n_exits, chi2=stat, p=p, b_hat=b_hat,
                b_true=0.5, rel_err=abs(b_hat - 0.5) / 0.5, passed=bool(ok))


def p2(n_rep=50, n_exits=2000, seed=202):
    rng = np.random.default_rng(seed)
    occ = np.full(NBIN, 0.1)
    ps = []
    for _ in range(n_rep):
        ph = rng.random(n_exits)                   # constant hazard
        obs = np.histogram(ph, bins=NBIN, range=(0, 1))[0]
        ps.append(chi2_from_bins(obs, occ)[1])
    ps = np.array(ps)
    n_ok = int((ps >= 0.05).sum())
    return dict(check="P2", n_rep=n_rep, n_exits=n_exits, n_pass=n_ok,
                frac=n_ok / n_rep, passed=bool(n_ok >= 0.9 * n_rep),
                p_quantiles=[float(np.quantile(ps, q)) for q in (0, .25, .5, .75, 1)])


def p3(Omega=100_000, n_seed=11, seed0=303):
    res = {}
    for nm in ("A1", "A2"):
        M = MODELS[nm]
        T, cyc, sig = get_cycle(nm)
        binom = np.array([comb(M["m"], i) for i in range(M["m"] + 1)], dtype=np.float64)
        kk = np.array(M["k"], dtype=np.float64)
        is_open = 1.0 if M["level"] == "open" else 0.0
        rms = float(np.sqrt((sig ** 2).sum()))
        drifts = []
        for s in range(n_seed):
            _seed(np.int64(seed0 + 1000 * (nm == "A2") + s))
            n = initial_counts(M, Omega, cyc)
            run_until_time(n, kk, M["m"], M["kr"], M["kc"], is_open, float(Omega), binom, T)
            # after exactly one period the deterministic state is the start cycle point
            d = float(np.linalg.norm(n / Omega - cyc[0]))
            drifts.append(d / rms)
        res[nm] = dict(drifts=drifts, median=float(np.median(drifts)),
                       max=float(np.max(drifts)), rms_radius=rms)
    passed = all(res[nm]["median"] < 0.01 for nm in res)
    return dict(check="P3", Omega=Omega, n_seed=n_seed, per_model=res, passed=bool(passed))


def main():
    out = [p1(), p2(), p3()]
    json.dump(out, open(os.path.join(HERE, "planted_A.json"), "w"), indent=1)
    for r in out:
        print(r["check"], "PASS" if r["passed"] else "FAIL",
              {k: v for k, v in r.items() if k not in ("check", "passed", "per_model", "p_quantiles")})
        if r["check"] == "P3":
            for nm, d in r["per_model"].items():
                print("   ", nm, "median drift %.5f  max %.5f" % (d["median"], d["max"]))
    print("ALL PLANTED PASS:", all(r["passed"] for r in out))
    return out


if __name__ == "__main__":
    main()
