# Copied from grammar-exit-time/gexit/ (PR 3, gomni1/ClaudeCloud1#3) for task grammar-idsize; changes are marked "idsize:".
"""Estimators, memorylessness test and preregistered fits (SPEC §4, §7)."""
import numpy as np
from scipy import stats as sst

Z975 = 1.959964


def mle(times, cens):
    times = np.asarray(times, float)
    cens = np.asarray(cens, bool)
    S = times.sum()
    d = int((~cens).sum())
    return (S / d if d > 0 else np.inf), S, d


def chi2_interval(S, d, level=0.95):
    a = 1.0 - level
    lo = 2 * S / sst.chi2.ppf(1 - a / 2, 2 * d + 2)
    hi = 2 * S / sst.chi2.ppf(a / 2, 2 * d) if d > 0 else np.inf
    return lo, hi


def boot_T(times, cens, B=2000, rng=None):
    rng = np.random.default_rng(rng)
    times = np.asarray(times, float)
    ex = ~np.asarray(cens, bool)
    n = len(times)
    idx = rng.integers(0, n, size=(B, n))
    S = times[idx].sum(axis=1)
    d = ex[idx].sum(axis=1)
    return S / np.maximum(d, 1)


def boot_interval(times, cens, B=2000, rng=None):
    Tb = boot_T(times, cens, B, rng)
    return tuple(np.percentile(Tb, [2.5, 97.5]))


def summarize(times, cens, B=2000, rng=None):
    T, S, d = mle(times, cens)
    lo, hi = chi2_interval(S, d)
    blo, bhi = boot_interval(times, cens, B, rng)
    x = np.asarray(times, float)[~np.asarray(cens, bool)]
    cv = float(x.std(ddof=1) / x.mean()) if len(x) > 1 else np.nan
    return dict(T=T, S=S, d=d, n=len(times), censored=int(np.sum(cens)), chi2_lo=lo, chi2_hi=hi,
                boot_lo=blo, boot_hi=bhi, cv=cv, sigma_ln=(np.log(hi) - np.log(lo)) / (2 * Z975))


def ks_exp(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    F = 1.0 - np.exp(-x / x.mean())
    i = np.arange(1, n + 1)
    return max(np.max(i / n - F), np.max(F - (i - 1) / n))


def lilliefors_exp(x, B=10000, rng=None, chunk=500):
    """KS against an exponential with estimated mean; p-value by parametric bootstrap."""
    rng = np.random.default_rng(rng)
    x = np.asarray(x, float)
    n = len(x)
    D = ks_exp(x)
    i = np.arange(1, n + 1)
    Ds = []
    left = B
    while left > 0:
        m = min(chunk, left)
        y = np.sort(rng.exponential(1.0, size=(m, n)), axis=1)
        F = 1.0 - np.exp(-y / y.mean(axis=1, keepdims=True))
        Ds.append(np.maximum(np.max(i / n - F, axis=1), np.max(F - (i - 1) / n, axis=1)))
        left -= m
    Ds = np.concatenate(Ds)
    p = (1 + np.sum(Ds >= D)) / (B + 1)
    cv = float(x.std(ddof=1) / x.mean())
    return dict(n=n, D=float(D), p=float(p), cv=cv, B=B)


def wls(X, y, w):
    sw = np.sqrt(w)
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    r = y - X @ beta
    return beta, float(np.sum(w * r * r)), r


def design(Om, model):
    Om = np.asarray(Om, float)
    if model == "E":
        return np.column_stack([np.ones_like(Om), Om, np.log(Om)])
    return np.column_stack([np.ones_like(Om), np.log(Om)])


def fit_EP(Om, T, sigma):
    """F1: model E (a + W*Om + beta*ln Om) and P (a + beta*ln Om), WLS with w = 1/sigma^2."""
    Om = np.asarray(Om, float)
    y = np.log(np.asarray(T, float))
    w = 1.0 / np.asarray(sigma, float) ** 2
    bE, chiE, rE = wls(design(Om, "E"), y, w)
    bP, chiP, rP = wls(design(Om, "P"), y, w)
    aicE = chiE + 2 * 3
    aicP = chiP + 2 * 2
    return dict(a=bE[0], W=bE[1], beta=bE[2], chi2_E=chiE, aP=bP[0], betaP=bP[1], chi2_P=chiP,
                AIC_E=aicE, AIC_P=aicP, dAIC=aicP - aicE, resid_E=rE.tolist(), resid_P=rP.tolist())


def local_slopes(Om, T, beta=None):
    Om = np.asarray(Om, float)
    y = np.log(np.asarray(T, float))
    s = np.diff(y) / np.diff(Om)
    if beta is not None:
        s = s - beta * np.diff(np.log(Om)) / np.diff(Om)
    return s


def boot_W(sizes, B=2000, rng=None):
    """sizes: list of (Omega, times, cens).  Resample runs within each size, refit E."""
    rng = np.random.default_rng(rng)
    Om = np.array([s[0] for s in sizes], float)
    Ts, sig = [], []
    for (_, t, c) in sizes:
        t = np.asarray(t, float)
        ex = ~np.asarray(c, bool)
        n = len(t)
        idx = rng.integers(0, n, size=(B, n))
        S = t[idx].sum(axis=1)
        d = ex[idx].sum(axis=1)
        Ts.append(S / np.maximum(d, 1))
        lo = 2 * S / sst.chi2.ppf(0.975, 2 * d + 2)
        hi = 2 * S / sst.chi2.ppf(0.025, 2 * np.maximum(d, 1))
        sig.append((np.log(hi) - np.log(lo)) / (2 * Z975))
    Ts = np.array(Ts).T
    sig = np.array(sig).T
    X = design(Om, "E")
    Ws = np.empty(B)
    for b in range(B):
        beta, _, _ = wls(X, np.log(Ts[b]), 1.0 / sig[b] ** 2)
        Ws[b] = beta[1]
    return Ws


def f1(sizes, B=2000, rng=None):
    """Full F1 on a list of (Omega, times, cens)."""
    summ = [summarize(t, c, B=B, rng=None if rng is None else rng + i) for i, (_, t, c) in enumerate(sizes)]
    Om = [s[0] for s in sizes]
    T = [s["T"] for s in summ]
    sig = [s["sigma_ln"] for s in summ]
    out = fit_EP(Om, T, sig)
    Ws = boot_W(sizes, B=B, rng=rng)
    out["W_lo"], out["W_hi"] = (float(v) for v in np.percentile(Ws, [2.5, 97.5]))
    out["Omega"] = list(map(float, Om))
    out["T"] = T
    out["sigma_ln"] = sig
    out["local_slopes"] = local_slopes(Om, T).tolist()
    out["local_slopes_beta_corrected"] = local_slopes(Om, T, out["beta"]).tolist()
    out["n_sizes"] = len(Om)
    out["span"] = float(max(Om) / min(Om)) if Om else 0.0
    out["k1_triggers"] = dict(W_negative=bool(out["W"] < 0), W_ci_includes_0=bool(out["W_lo"] <= 0 <= out["W_hi"]),
                              dAIC_below_10=bool(out["dAIC"] < 10))
    out["k1_any"] = any(out["k1_triggers"].values())
    return out
