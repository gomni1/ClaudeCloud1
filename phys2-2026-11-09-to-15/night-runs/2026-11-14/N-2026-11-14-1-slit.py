#!/usr/bin/env python3
"""N-2026-11-14-1: slit test of the angular-sum handoff (STEERING PIN, 14 Nov).
Everything here follows NIGHT-QUEUE-2026-11-14.md, frozen before this file was written.
Usage: python3 N-2026-11-14-1-slit.py [out.json]
"""
import sys, json, time, itertools
import numpy as np

D1, D2 = 10000.0, 2000.0
CENTRES = {'A': -100, 'B': 0, 'C': 100}
OMEGA = np.pi / 5
X = np.arange(-500, 501, dtype=float)           # 1001 screen grains
SEED = 20261114
SIGMAS = [0, 0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03,
          0.05, 0.1, 0.2, 0.5, 1.0, float(np.pi / 2)]
NDRAW = 2000
CONFIGS = ['', 'A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC']
PAIRS = ['AB', 'AC', 'BC']

# histories: (slit, grain y) x screen grain; L[slit] has shape (5, 1001)
L = {}
for s, c in CENTRES.items():
    y = np.arange(c - 2, c + 3, dtype=float)[:, None]
    L[s] = np.sqrt(D1 ** 2 + y ** 2) + np.sqrt(D2 ** 2 + (X[None, :] - y) ** 2)   # float, not rounded


def slit_sums(theta, mult):
    """Complex resultant of each slit; theta[s] shape (5,1001); mult=2 axis, 1 arrow."""
    return {s: np.exp(1j * mult * theta[s]).sum(axis=0) for s in theta}


def resultants(Rs):
    out = {}
    for cfg in CONFIGS:
        r = np.zeros(X.size, dtype=complex)
        for s in cfg:
            r = r + Rs[s]
        out[cfg] = r
    return out


def measures(P):
    """P: dict config -> array over x. Returns I2 per pair, I3, kappa2, kappa3."""
    P0 = P['']
    I2 = {jk: P[jk] - P[jk[0]] - P[jk[1]] + P0 for jk in PAIRS}
    I3 = P['ABC'] - P['AB'] - P['AC'] - P['BC'] + P['A'] + P['B'] + P['C'] - P0
    s2 = sum(np.abs(I2[jk]).sum() for jk in PAIRS)
    k2 = s2 / P['ABC'].sum()
    k3 = np.abs(I3).sum() / s2 if s2 > 0 else float('nan')
    return I2, I3, float(k2), float(k3)


def maxima(curve, frac=0.10):
    m = curve.max()
    idx = [i for i in range(1, curve.size - 1)
           if curve[i] > curve[i - 1] and curve[i] > curve[i + 1] and curve[i] >= frac * m]
    return idx


def spacing(curve):
    idx = maxima(curve)
    if len(idx) < 2:
        return len(idx), float('nan')
    return len(idx), float(np.mean(np.diff(X[idx])))


out = {'geometry': dict(D1=D1, D2=D2, centres=CENTRES, slit_width=5, omega=OMEGA,
                        screen=[float(X[0]), float(X[-1]), int(X.size)]),
       'L_range': [float(min(v.min() for v in L.values())), float(max(v.max() for v in L.values()))]}

# ---------- part one (no noise) ----------
theta = {s: OMEGA * L[s] for s in L}
R_axis = resultants(slit_sums(theta, 2))
R_arrow = resultants(slit_sums(theta, 1))
absq = {c: np.abs(R_axis[c]) ** 2 for c in CONFIGS}
s_sat = float(np.median(absq['ABC']))
readouts = {
    'R2': absq,
    'R4': {c: absq[c] ** 2 for c in CONFIGS},
    'RS': {c: 1 - np.exp(-absq[c] / s_sat) for c in CONFIGS},
    'C+': {c: np.full(X.size, 5.0 * len(c)) for c in CONFIGS},        # count of open histories, w = 1
    'C-arrow': {c: np.abs(R_arrow[c]) ** 2 for c in CONFIGS},
}
part1 = {'s_sat': s_sat}
for name, P in readouts.items():
    I2, I3, k2, k3 = measures(P)
    part1[name] = dict(kappa2=k2, kappa3=k3,
                       max_abs_I2=float(max(np.abs(I2[jk]).max() for jk in PAIRS)),
                       max_abs_I3=float(np.abs(I3).max()),
                       max_P_ABC=float(P['ABC'].max()),
                       sum_P={c: float(P[c].sum()) for c in CONFIGS})
out['part1'] = part1

tolC = 1e-9 * part1['C+']['max_P_ABC']
harness = {
    'C+_I2_zero': part1['C+']['max_abs_I2'] <= tolC,
    'C+_I3_zero': part1['C+']['max_abs_I3'] <= tolC,
    'R4_kappa3_gt_1e-3': part1['R4']['kappa3'] > 1e-3,
    'RS_kappa3_gt_1e-3': part1['RS']['kappa3'] > 1e-3,
}
harness['pass'] = all(harness.values())
out['harness'] = harness
out['kill_R2'] = {'kappa2_lt_0p05': part1['R2']['kappa2'] < 0.05,
                  'kappa3_gt_1e-6': part1['R2']['kappa3'] > 1e-6}
out['kill_R2']['killed'] = out['kill_R2']['kappa2_lt_0p05'] or out['kill_R2']['kappa3_gt_1e-6']

fr = {}
for name in ('R2', 'C-arrow'):
    nABC, spABC = spacing(readouts[name]['ABC'])
    nAB, spAB = spacing(readouts[name]['AB'])
    fr[name] = dict(n_maxima_ABC=nABC, spacing_ABC=spABC, n_maxima_AB=nAB, spacing_AB=spAB,
                    maxima_AB_x=[float(X[i]) for i in maxima(readouts[name]['AB'])])
fr['ratio_AB_arrow_over_R2'] = fr['C-arrow']['spacing_AB'] / fr['R2']['spacing_AB']
fr['ratio_ABC_arrow_over_R2'] = fr['C-arrow']['spacing_ABC'] / fr['R2']['spacing_ABC']
fr['fringe_count_ok'] = fr['R2']['n_maxima_ABC'] >= 5
out['fringes'] = fr
# slit coherence actually present (for the plant argument)
out['slit_s_range'] = {s: [float(absq[s].min()), float(absq[s].max())] for s in 'ABC'}

print(json.dumps({k: out[k] for k in ('harness', 'kill_R2', 'fringes')}, indent=1, default=float))
for name in readouts:
    print(f"{name:8s} kappa2={part1[name]['kappa2']:.6g} kappa3={part1[name]['kappa3']:.6g} "
          f"max|I3|={part1[name]['max_abs_I3']:.3g} maxP={part1[name]['max_P_ABC']:.6g}")

# ---------- part two (turnover noise), only if the harness passes ----------
if harness['pass'] and fr['fringe_count_ok']:
    rng = np.random.default_rng(SEED)
    sqrtL = {s: np.sqrt(L[s]) for s in L}
    t0 = time.time()
    for _ in range(20):                                   # pilot
        xi = {s: rng.standard_normal(L[s].shape) for s in L}
        th = {s: OMEGA * L[s] + 0.01 * sqrtL[s] * xi[s] for s in L}
        measures({c: np.abs(r) ** 2 for c, r in resultants(slit_sums(th, 2)).items()})
    pilot = (time.time() - t0) / 20
    out['pilot_seconds_per_draw'] = pilot
    print(f"pilot: {pilot*1e3:.2f} ms/draw; projected {pilot*NDRAW*len(SIGMAS):.0f} s")
    rng = np.random.default_rng(SEED)                     # main loop restarts from the seed
    noise = []
    for sg in SIGMAS:
        sumP = {c: np.zeros(X.size) for c in CONFIGS}
        sumP200 = None
        k2s, k3s, maxI3rel = [], [], 0.0
        for d in range(NDRAW):
            xi = {s: rng.standard_normal(L[s].shape) for s in L}       # one jitter per history, all configs
            th = {s: OMEGA * L[s] + sg * sqrtL[s] * xi[s] for s in L}
            P = {c: np.abs(r) ** 2 for c, r in resultants(slit_sums(th, 2)).items()}
            _, I3, k2, k3 = measures(P)
            k2s.append(k2); k3s.append(k3)
            maxI3rel = max(maxI3rel, float(np.abs(I3).max() / P['ABC'].max()))
            for c in CONFIGS:
                sumP[c] += P[c]
            if d == 199:
                sumP200 = {c: sumP[c] / 200 for c in CONFIGS}
        meanP = {c: sumP[c] / NDRAW for c in CONFIGS}
        _, _, A2, A3 = measures(meanP)
        _, _, A2_200, A3_200 = measures(sumP200)
        k2s = np.array(k2s); k3s = np.array(k3s)
        row = dict(sigma=sg, decoh_pred=float(np.exp(-4 * sg ** 2 * 12000.0)),
                   A_kappa2=A2, A_kappa3=A3, A200_kappa2=A2_200, A200_kappa3=A3_200,
                   B_kappa2=float(k2s.mean()), B_kappa2_sd=float(k2s.std()),
                   B_kappa3=float(k3s.mean()), B_kappa3_max=float(k3s.max()),
                   B200_kappa2=float(k2s[:200].mean()), B200_kappa3=float(k3s[:200].mean()),
                   max_I3_rel=maxI3rel, mean_P_ABC=float(meanP['ABC'].mean()))
        noise.append(row)
        print(' '.join(f"{k}={v:.4g}" for k, v in row.items()))
    out['noise'] = noise
    out['noise_seconds'] = time.time() - t0
else:
    out['noise'] = 'not run: harness or fringe-count check failed'

json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'N-2026-11-14-1-slit-output.json', 'w'), indent=1, default=float)
