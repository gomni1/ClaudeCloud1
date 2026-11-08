"""Routes test statistics (SPEC §6)."""
import numpy as np
from scipy.stats import mannwhitneyu


def mwu(up, down):
    """One-sided Mann-Whitney U, mid-ranks with tie correction, asymptotic p.

    Returns (U1, p_less, p_greater) with U1 the statistic of the `up` sample and
    p_less the p-value for 'up deltas are smaller than down deltas'.
    """
    a = mannwhitneyu(up, down, alternative='less', method='asymptotic')
    b = mannwhitneyu(up, down, alternative='greater', method='asymptotic')
    return float(a.statistic), float(a.pvalue), float(b.pvalue)


def rank_biserial(U1, n1, n2):
    """r = 1 - 2*U1/(n1*n2); r > 0 means the up sample is stochastically smaller."""
    return float(1.0 - 2.0 * U1 / (n1 * n2))


def _hist(levels, K):
    return np.bincount(np.asarray(levels, np.int64), minlength=K)[:K].astype(np.float64)


def _U1_from_hist(cu, cd):
    """U1 = #(up > down) + 0.5*#ties, computed from level histograms."""
    cum_below = np.concatenate(([0.0], np.cumsum(cd)[:-1]))   # sum_{j<k} cd[j]
    return float((cu * cum_below).sum() + 0.5 * float((cu * cd).sum()))


def bootstrap_rb(levels_up, levels_down, B=2000, seed=0):
    """Percentile 95% interval for the rank-biserial correlation.

    delta is lattice-valued, so i.i.d. resampling of the raw values is exactly a
    multinomial draw on each direction's level histogram.
    """
    K = int(max(np.max(levels_up), np.max(levels_down))) + 1
    cu = _hist(levels_up, K); cd = _hist(levels_down, K)
    n1 = int(cu.sum()); n2 = int(cd.sum())
    pu = cu / n1; pd = cd / n2
    rng = np.random.default_rng(seed)
    out = np.empty(B)
    for b in range(B):
        bu = rng.multinomial(n1, pu).astype(np.float64)
        bd = rng.multinomial(n2, pd).astype(np.float64)
        out[b] = 1.0 - 2.0 * _U1_from_hist(bu, bd) / (n1 * n2)
    lo, hi = np.percentile(out, [2.5, 97.5])
    return float(lo), float(hi)


def verdict(p_less, p_greater, alpha=0.05):
    """SPEC §7 verdict rules. p_less/p_greater are per-size arrays."""
    p_less = np.asarray(p_less, float); p_greater = np.asarray(p_greater, float)
    n_sig = int((p_less < alpha).sum())
    n_ns = int((p_less >= alpha).sum())
    reversal = bool((p_greater < alpha).any())
    if n_ns >= 2 or reversal:
        v = "KILL"
    elif n_sig >= 3 and not reversal:
        v = "HOLDS"
    else:
        v = "UNDERDETERMINED"
    return dict(verdict=v, n_sig=n_sig, n_nonsig=n_ns, reversal=reversal)
