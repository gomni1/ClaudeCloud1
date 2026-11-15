# Identity with size: results

Status: SANDBOX / DRAFT. Not promoted. Nothing here is uniquely derived. Every statement holds only inside `SPEC.md`'s definitions: PR 3's open level, TH with m = 2, kr = kc = 2 and x = C/(C+V), the Kurtz reading, D = {nC = nL = 0}, and the seeding family. The ODE and the Markov chain are effective-register (coarse-grained) summaries of step processes.

**Well-mixed limit.** The ensemble is well mixed, so every cost grows with Ω by construction. This applies to every verdict below.

## Freeze

`SPEC.md` SHA-256: `520f897ec080d747b33263b886fd135458c02152344a1dfd40ec1609386a3a77`. Recorded 2026-10-30, before any code of this task was written or run. The file is unchanged at this commit.

**Code.** PR 3's code is copied into `gexit_pr3/` with attribution (gomni1/ClaudeCloud1#3). `grammar-exit-time/` is not modified.

## Verdicts

| Test | Verdict (well-mixed limit) | Evidence |
|---|---|---|
| **R1**: the race predicts the passage fraction (φ_obs/φ_pred ∈ [½, 2]) | **Killed** for every k10 | The ratio leaves the band at two eligible sizes for each k10. k10 = ½: 0.39 (Ω = 8, down) and 2.29 (Ω = 10, up). k10 = 1: 0.35 (8, down) and 2.54 (10, up). k10 = 2: 2.57 (8, up) and 3.15 (10, up). The exact-expectation estimator φ_pred* gives the same ratios to within 1% from Ω = 8 on. |
| **R2**: φ_obs decays at the dissolution cost (model-E slope = −W_D within 25%, ΔAIC ≥ 10) | **Underdetermined** | k10 = 1 fails. Up: W = −0.842 against −W_D = −0.820, 2.6% off, ΔAIC = 1004, pass. Down: W = −1.350 against −0.820, 65% off, fail. k10 = ½ and 2 cannot be evaluated: this run's gMAM stage stopped at its budget with no value (see the deviations). One failure is not the two required for a kill. |
| **G1**: is the threshold-law gap a small-size effect? | **Supports the small-size reading**, by the preregistered rule. Fragile: see below. | Over Ω ∈ {20, 24, 30}: s₂₅ = 0.763 (bootstrap SE 0.071, 95% interval [0.61, 0.89]); the support band is [0.738, 0.902]. |
| **G2** (report only) | — | Along complete reactive paths, the mean of max nV/Ω falls from 4.96 (Ω = 8) to 4.55 (Ω = 16) and 4.33 (Ω = 30). The mean distance from gMAM's optimal path falls from 0.85 to 0.60 and 0.46. |

**How fragile G1 is.** The verdict rests on Ω = 30, the least reliable size:
- 3 of its 8 replicates ended as failures, with no success in 2×10⁴ trials at the last stage (M = 4 → 0).
- The 5 that succeeded had only 1–6 successes there, not the 50 targeted.
- Dropping failed replicates biases ln T(30) low, and with it s₂₅.

Two checks bracket this:
- **Ω = 30 removed.** The two remaining sizes give the secant slope 20→24 = 1.052, which falls on the kill side.
- **Failures filled at one success**, an optimistic P and so a lower bound on their ln T. This gives s₂₅ = 0.847, still in the band. A smaller true P would push s₂₅ higher, and an upper bound is not available.

**The harness passed** before Part 2 counted, with all six FFS T_D values within 2 combined SE of PR 3's brute force:

| Model | Ω | T_FFS | T_PR3 | z |
|---|---|---|---|---|
| TH | 8 | 823 ± 74 | 855 ± 27 | −0.41 |
| TH | 10 | 5455 ± 758 | 5048 ± 161 | +0.53 |
| TH | 12 | 33 937 ± 4010 | 32 704 ± 1038 | +0.30 |
| MA | 6 | 538 ± 50 | 591 ± 19 | −1.00 |
| MA | 8 | 6097 ± 827 | 7756 ± 247 | −1.92 |
| MA | 10 | 111 279 ± 9720 | 107 563 ± 3415 | +0.36 |

PF1 via FFS matches the exact 1/λ₀ within 0.65% (Ω = 20) and 1.7% (Ω = 30), against the 10% allowed.

## M0 (`evidence/m0.json`)

**The identity.** S(y) − A = k10·(y−2)(y−3)(y−4)/(1+y)² holds exactly: the sympy residual is 0. The balances V = 2, 3, 4 (with C = L = 1 and P = ½) have residuals ≤ 1.3×10⁻¹⁵.

**Largest real parts of the Jacobian eigenvalues**, matching the disclosed table:

| k10 | V = 2 | V = 3 | V = 4 | λ_slow (V = 2) | t_b = 10/\|λ_slow\| |
|---|---|---|---|---|---|
| ½ | −0.160 | +0.172 | −0.084 | −0.1598 | 62.58 |
| 1 | −0.151 | +0.295 | −0.130 | −0.1514 | 66.05 |
| 2 | −0.128 | +0.531 | −0.092 | −0.1285 | 77.85 |

## Part 1: the race test, per k10 (`evidence/switch_summary.json`, `evidence/td0.json`, `evidence/analysis.json`)

**Columns.**
- φ_obs: the fraction of switching runs that pass through D, with a Clopper–Pearson 95% interval.
- T_D⁰: the mean first-passage time to D from the same start.
- φ_pred: the brief's estimator, 1 − E[exp(−τ_S/T_D⁰)], with a bootstrap SE.
- φ_pred*: 1 − 1/E[exp(+τ_S/T_D⁰)], reported only.

R1-eligible means φ_obs ≥ 10⁻³ and both relative SEs ≤ 20%. **Bold** ratios are eligible ratios outside [½, 2]. At Ω = 16, T_D⁰ was not measured (see the deviations).

**k10 = ½**

| Ω | dir | runs | passages | φ_obs [95% CI] | T_D⁰ ± SE | φ_pred ± SE | φ_pred* | φ_obs/φ_pred | R1-eligible |
|---|---|---|---|---|---|---|---|---|---|
| 2 | up | 2000 | 696 | 0.348 [0.327, 0.369] | 3.431 ± 0.12 | 0.29 ± 9.07e-03 | 0.385 | 1.2 | yes |
| 2 | down | 2000 | 578 | 0.289 [0.269, 0.309] | 5.469 ± 0.17 | 0.165 ± 5.81e-03 | 0.209 | 1.75 | yes |
| 3 | up | 2000 | 396 | 0.198 [0.181, 0.216] | 7.998 ± 0.31 | 0.203 ± 7.42e-03 | 0.246 | 0.974 | yes |
| 3 | down | 2000 | 331 | 0.166 [0.149, 0.183] | 13.99 ± 0.44 | 0.128 ± 4.74e-03 | 0.16 | 1.29 | yes |
| 4 | up | 2000 | 262 | 0.131 [0.117, 0.147] | 20.23 ± 0.86 | 0.117 ± 4.92e-03 | 0.129 | 1.12 | yes |
| 4 | down | 2000 | 177 | 0.0885 [0.0764, 0.102] | 30.71 ± 0.97 | 0.0844 ± 3.15e-03 | 0.0954 | 1.05 | yes |
| 5 | up | 2000 | 146 | 0.073 [0.062, 0.0853] | 51.6 ± 2.1 | 0.0597 ± 2.60e-03 | 0.0625 | 1.22 | yes |
| 5 | down | 2000 | 82 | 0.041 [0.0327, 0.0506] | 70.64 ± 2.3 | 0.049 ± 1.88e-03 | 0.0524 | 0.836 | yes |
| 6 | up | 2000 | 76 | 0.038 [0.0301, 0.0473] | 139.2 ± 5.1 | 0.0291 ± 1.18e-03 | 0.0298 | 1.31 | yes |
| 6 | down | 6000 | 93 | 0.0155 [0.0125, 0.019] | 168.7 ± 5.2 | 0.0245 ± 8.40e-04 | 0.0253 | 0.633 | yes |
| 8 | up | 6000 | 64 | 0.0107 [8.22e-03, 0.0136] | 858.2 ± 28 | 5.90e-03 ± 2.10e-04 | 5.92e-03 | 1.81 | yes |
| 8 | down | 30000 | 64 | 2.13e-03 [1.64e-03, 2.72e-03] | 930.6 ± 30 | 5.47e-03 ± 1.78e-04 | 5.50e-03 | **0.39** | yes |
| 10 | up | 30000 | 80 | 2.67e-03 [2.12e-03, 3.32e-03] | 5.10e+03 ± 1.6e+02 | 1.16e-03 ± 3.88e-05 | 1.16e-03 | **2.29** | yes |
| 10 | down | 254000 | 59 | 2.32e-04 [1.77e-04, 3.00e-04] | 5.24e+03 ± 1.7e+02 | 1.11e-03 ± 3.56e-05 | 1.11e-03 | 0.21 | no |
| 12 | up | 126000 | 71 | 5.63e-04 [4.40e-04, 7.11e-04] | 3.11e+04 ± 9.4e+02 | 2.12e-04 ± 6.43e-06 | 2.12e-04 | 2.66 | no |
| 12 | down | 1000000 | 18 | 1.80e-05 [1.07e-05, 2.84e-05] | 3.10e+04 ± 1.02e+03 | 2.09e-04 ± 6.73e-06 | 2.09e-04 | 0.086 | no |
| 16 | up | 1000000 | 22 | 2.20e-05 [1.38e-05, 3.33e-05] | — | — | — | — | no |
| 16 | down | 1000000 | 0 | 0 [0, 3.69e-06] | — | — | — | — | no |

**k10 = 1**

| Ω | dir | runs | passages | φ_obs [95% CI] | T_D⁰ ± SE | φ_pred ± SE | φ_pred* | φ_obs/φ_pred | R1-eligible |
|---|---|---|---|---|---|---|---|---|---|
| 2 | up | 2000 | 755 | 0.378 [0.356, 0.399] | 2.519 ± 0.087 | 0.304 ± 9.21e-03 | 0.4 | 1.24 | yes |
| 2 | down | 2000 | 469 | 0.234 [0.216, 0.254] | 4.418 ± 0.15 | 0.124 ± 4.73e-03 | 0.148 | 1.89 | yes |
| 3 | up | 2000 | 408 | 0.204 [0.187, 0.222] | 6.443 ± 0.26 | 0.19 ± 7.27e-03 | 0.225 | 1.07 | yes |
| 3 | down | 2000 | 275 | 0.138 [0.123, 0.153] | 11.55 ± 0.37 | 0.0866 ± 3.37e-03 | 0.0975 | 1.59 | yes |
| 4 | up | 2000 | 316 | 0.158 [0.142, 0.175] | 15.66 ± 0.72 | 0.124 ± 5.64e-03 | 0.138 | 1.27 | yes |
| 4 | down | 2000 | 140 | 0.07 [0.0592, 0.0821] | 26.04 ± 0.91 | 0.0598 ± 2.51e-03 | 0.0651 | 1.17 | yes |
| 5 | up | 2000 | 162 | 0.081 [0.0694, 0.0938] | 41.55 ± 1.7 | 0.06 ± 2.73e-03 | 0.0633 | 1.35 | yes |
| 5 | down | 2000 | 60 | 0.03 [0.023, 0.0384] | 61.8 ± 2 | 0.032 ± 1.25e-03 | 0.0333 | 0.937 | yes |
| 6 | up | 2000 | 79 | 0.0395 [0.0314, 0.049] | 110.2 ± 4.1 | 0.0288 ± 1.19e-03 | 0.0296 | 1.37 | yes |
| 6 | down | 6000 | 76 | 0.0127 [9.99e-03, 0.0158] | 136.8 ± 4.3 | 0.0162 ± 5.54e-04 | 0.0165 | 0.784 | yes |
| 8 | up | 6000 | 64 | 0.0107 [8.22e-03, 0.0136] | 750.5 ± 25 | 5.70e-03 ± 2.05e-04 | 5.72e-03 | 1.87 | yes |
| 8 | down | 62000 | 78 | 1.26e-03 [9.95e-04, 1.57e-03] | 775 ± 24 | 3.60e-03 ± 1.12e-04 | 3.62e-03 | **0.35** | yes |
| 10 | up | 30000 | 74 | 2.47e-03 [1.94e-03, 3.10e-03] | 5.06e+03 ± 1.7e+02 | 9.70e-04 ± 3.35e-05 | 9.71e-04 | **2.54** | yes |
| 10 | down | 454000 | 69 | 1.52e-04 [1.18e-04, 1.92e-04] | 4.93e+03 ± 1.7e+02 | 6.62e-04 ± 2.30e-05 | 6.63e-04 | 0.23 | no |
| 12 | up | 126000 | 71 | 5.63e-04 [4.40e-04, 7.11e-04] | 3.44e+04 ± 1.04e+03 | 1.61e-04 ± 4.87e-06 | 1.61e-04 | 3.49 | no |
| 12 | down | 1000000 | 7 | 7.00e-06 [2.81e-06, 1.44e-05] | 3.37e+04 ± 1.06e+03 | 1.10e-04 ± 3.53e-06 | 1.10e-04 | 0.0638 | no |
| 16 | up | 1000000 | 18 | 1.80e-05 [1.07e-05, 2.84e-05] | — | — | — | — | no |
| 16 | down | 1000000 | 0 | 0 [0, 3.69e-06] | — | — | — | — | no |

**k10 = 2**

| Ω | dir | runs | passages | φ_obs [95% CI] | T_D⁰ ± SE | φ_pred ± SE | φ_pred* | φ_obs/φ_pred | R1-eligible |
|---|---|---|---|---|---|---|---|---|---|
| 2 | up | 2000 | 763 | 0.382 [0.36, 0.403] | 2.088 ± 0.069 | 0.297 ± 8.90e-03 | 0.379 | 1.29 | yes |
| 2 | down | 2000 | 288 | 0.144 [0.129, 0.16] | 3.462 ± 0.12 | 0.0928 ± 3.67e-03 | 0.105 | 1.55 | yes |
| 3 | up | 2000 | 428 | 0.214 [0.196, 0.233] | 5.028 ± 0.2 | 0.206 ± 7.59e-03 | 0.258 | 1.04 | yes |
| 3 | down | 2000 | 189 | 0.0945 [0.082, 0.108] | 9.755 ± 0.33 | 0.0603 ± 2.40e-03 | 0.0651 | 1.57 | yes |
| 4 | up | 2000 | 309 | 0.154 [0.139, 0.171] | 13.3 ± 0.59 | 0.121 ± 5.22e-03 | 0.135 | 1.28 | yes |
| 4 | down | 2000 | 82 | 0.041 [0.0327, 0.0506] | 21.86 ± 0.73 | 0.036 ± 1.43e-03 | 0.0376 | 1.14 | yes |
| 5 | up | 2000 | 169 | 0.0845 [0.0727, 0.0976] | 34.92 ± 1.5 | 0.0594 ± 2.68e-03 | 0.0629 | 1.42 | yes |
| 5 | down | 6000 | 84 | 0.014 [0.0112, 0.0173] | 54.68 ± 1.7 | 0.0184 ± 6.09e-04 | 0.0189 | 0.761 | yes |
| 6 | up | 2000 | 105 | 0.0525 [0.0431, 0.0632] | 97.63 ± 3.9 | 0.0273 ± 1.19e-03 | 0.0279 | 1.92 | yes |
| 6 | down | 14000 | 83 | 5.93e-03 [4.72e-03, 7.34e-03] | 132.7 ± 4.1 | 8.87e-03 ± 2.82e-04 | 8.97e-03 | 0.668 | yes |
| 8 | up | 6000 | 83 | 0.0138 [0.011, 0.0171] | 671.6 ± 23 | 5.38e-03 ± 1.91e-04 | 5.40e-03 | **2.57** | yes |
| 8 | down | 126000 | 87 | 6.90e-04 [5.53e-04, 8.52e-04] | 750.4 ± 24 | 2.01e-03 ± 6.26e-05 | 2.01e-03 | 0.344 | no |
| 10 | up | 30000 | 83 | 2.77e-03 [2.20e-03, 3.43e-03] | 4.96e+03 ± 1.6e+02 | 8.80e-04 ± 2.88e-05 | 8.80e-04 | **3.15** | yes |
| 10 | down | 854000 | 69 | 8.08e-05 [6.29e-05, 1.02e-04] | 5.45e+03 ± 1.8e+02 | 3.30e-04 ± 1.10e-05 | 3.30e-04 | 0.245 | no |
| 12 | up | 126000 | 77 | 6.11e-04 [4.82e-04, 7.64e-04] | 3.59e+04 ± 1.43e+03 | 1.39e-04 ± 5.47e-06 | 1.39e-04 | 4.39 | no |
| 12 | down | 1000000 | 3 | 3.00e-06 [6.19e-07, 8.77e-06] | 3.65e+04 ± 1.53e+03 | 5.73e-05 ± 2.35e-06 | 5.73e-05 | 0.0524 | no |
| 16 | up | 1000000 | 16 | 1.60e-05 [9.15e-06, 2.60e-05] | — | — | — | — | no |
| 16 | down | 1000000 | 0 | 0 [0, 3.69e-06] | — | — | — | — | no |

**Pattern.** The race picture holds for Ω ≤ 6, where every ratio is within [0.63, 1.92]. From Ω = 8 on, it fails in opposite directions:
- **Upward switches** (V = 2 → 4) pass through D more often than the race predicts. The ratio is 1.8–2.6 at Ω = 8, 2.3–3.1 at Ω = 10 and 2.7–4.4 at Ω = 12.
- **Downward switches** (V = 4 → 2) pass through D less often. The ratio is 0.34–0.39, 0.21–0.25 and 0.05–0.09 at those sizes.
- **k10 makes little difference.** At each Ω, φ_obs barely moves across the family in the up direction. In the down direction, it falls with k10.

**Exact T_D⁰** (PR 3's master equation with `m6_supp`). Where computed, it matches the simulated T_D⁰ at all 9 points, with |z| ≤ 1.76. The points are Ω = 2 for every k10 and direction, and Ω = 3 for k10 = ½ and for k10 = 1 up. The stage stopped at its budget before the rest of Ω = 3 and all of Ω = 4.

**Crossover size** (the first Ω with φ_obs < 0.01):
- Up: Ω* = 10 for every k10.
- Down: Ω* = 8, 8 and 6 for k10 = ½, 1 and 2.
- With W_D known only at k10 = 1, Ω*·W_D = 8.2 (up) and 6.6 (down). Whether Ω* scales as 1/W_D across the family cannot be tested.

**R2 fit slopes** (model E, sizes with ≥ 10 passages):

| k10 | Up: W | Up: ΔAIC | Down: W | Down: ΔAIC |
|---|---|---|---|---|
| ½ | −0.801 | 899 | −1.310 | 858 |
| 1 | −0.842 | 1004 | −1.350 | 635 |
| 2 | −0.847 | 1028 | −1.349 | 512 |

The up slopes sit within 3% of −W_D(k10 = 1) for all three k10. The down slopes are about 1.65× steeper, for all three k10.

## Part 2: FFS to D, k10 = 1 (`evidence/ffs.json`)

| Ω | T_FFS (mean of ln T over replicates) | SE of ln T | Replicates ok | Local slope to the next size |
|---|---|---|---|---|
| 8 | 739 | 0.072 | 8 | 0.970 |
| 10 | 5144 | 0.131 | 8 | 1.010 |
| 12 | 3.87×10⁴ | 0.114 | 8 | 0.804 |
| 14 | 1.94×10⁵ | 0.184 | 8 | 0.981 |
| 16 | 1.38×10⁶ | 0.143 | 8 | 1.106 |
| 20 | 1.15×10⁸ | 0.194 | 8 | 1.052 |
| 24 | 7.72×10⁹ | 0.305 | 8 | 0.618 |
| 30 | 3.15×10¹¹ | 0.688 | 5 (3 failed) | — |

Local slopes include the prefactor's ln Ω term. Up to Ω = 24 they stay at 0.97–1.11, apart from one dip (0.80 at 12→14), and well above 0.820. Only the last step, 24→30, falls (0.62), and it depends on Ω = 30. G1's support for the small-size reading is therefore carried by a single, poorly sampled size. The evidence for a slope approaching 0.820 is weak, though the preregistered rule returns "supports".

**G2.** The reactive paths' Void excursion (max nV/Ω) shrinks and the paths approach gMAM's optimal path as Ω grows. That is the direction the disclosed reading (SPEC §3) predicted.

## Planted failures (`evidence/planted.json`, `evidence/harness.json`)

| Test | Result |
|---|---|
| PF5 | For (a, b) = (1, 10), (1, 100) and (1, 1000), φ_pred matches φ/(1+φ) with z = 0.39, −1.39 and −1.19, and φ_pred* matches φ with z = −0.05, −1.40 and −1.19. Bias of φ_pred against φ: −8.2%, −1.4% and −0.5%. **Pass.** |
| PF6 | Windowed slopes are 0.969, 0.958, 0.953, 0.938, 0.906 and 0.875 at centres 10, 12, 14, 16, 20 and 24. They fall through 0.91 between 16 and 24; the slope is 0.958 ≥ 0.95 at 12 and 0.875 ≤ 0.90 at 24. **Pass.** |
| PF1 via FFS | See the harness above. **Pass.** |

**pytest:** 7 passed (`evidence/pytest_output.txt`).

## Deviations and implementation notes (all on the record)

1. **gMAM stopped at its budget, with no result.**
   - The stage (3 k10 × 4 paths, PR 3's N-doubling rule) had no budget check and saved only at its end.
   - It passed its 0.5 CPU-h cap and was allowed to continue until 07:45 UTC, because FFS had used only 0.06 of its 3.5 h and the task total was not at risk. It had not finished by then and was stopped by PID after 1.52 CPU-h, three times its cap, with nothing saved.
   - **Consequence:** this run has no W_D or W_S for any k10. For k10 = 1, R2 uses PR 3's gMAM values (W_D = 0.81996 at V = 2 and 0.82021 at V = 4), which come from the identical model and code. For k10 = ½ and 2, R2 is not evaluable.
2. **Stage budgets were enforced by size level.** This was added before those stages ran. As written, the 900 CPU-s per-cell T_D⁰ rule allowed up to 13.5 CPU-h against the stage's 1.5 h cap, and the switching runs had no total cap. Both stages now run sizes in increasing order, with all six (k10, direction) cells of a size together, each capped at an equal share of what remains. Switching used 872 CPU-s and no cell reached its share.
3. **T_D⁰ stopped after Ω = 12**, at 3082 of 5400 CPU-s. At Ω = 16, φ_obs ≤ 2.2×10⁻⁵ for every k10 and direction, so no Ω = 16 cell can be R1-eligible (φ_obs ≥ 10⁻³), and R2 does not use T_D⁰. The roughly 10 runs per cell that the remaining budget allowed would also have given SEs near 30%.
4. **The exact stage** was rewritten before it ran, to save after each job and stop at its cap, ordered by Ω. It stopped after 9 of 18 solves. The in-flight job took the stage to 2181 CPU-s, 381 s over its 1800 s cap.
5. **FFS replicates ran in parallel** (2 workers). The seeds and the rule are unchanged.
6. **Raw switching times** (267 MB) are not committed. `switch_summary.json` keeps counts and moments, and every batch is reproducible from `sim.seed_for("idsize-switch", k10, Ω, direction, 0, batch)`.
7. **φ_pred's bias** for independent clocks was disclosed in the SPEC before the run. The R1 kill does not depend on it: φ_pred* gives the same out-of-band ratios.

## CPU (CPU-hours; 2–4 cores)

| Item | CPU-h | Cap |
|---|---|---|
| M0 and planted (PF5, PF6) | < 0.01 | 0.5 |
| gMAM (stopped, no result) | 1.52 | 0.5 |
| Switching runs | 0.24 | 1.5 |
| T_D⁰ runs | 0.86 | 1.5 |
| Exact master-equation solves | 0.61 | 0.5 |
| FFS harness (TH, MA, PF1) | < 0.01 | 1.0 |
| FFS sizes | 0.06 | 2.5 |
| Analysis, pytest and smoke tests | ≈ 0.1 | |
| **Task total** | **≈ 3.4** | 8 |

## Observational register

Analogies only. In this register, a level's identity is its V basin: switching between V = 2 and V = 4 is a change of identity at fixed size, and dissolution to D is loss of identity. The race test asked whether loss of identity during a switch is a simple race between two clocks. For small ensembles it is. At Ω ≥ 8 the two directions depart from it in opposite ways, and switching upward drags the ensemble through dissolution more often than a race allows. A reader may be reminded of composites, such as nucleons, whose identity is most stable at large size. But nothing here identifies a particle, or the nucleon architecture's integer, and every effect sits inside the well-mixed limit.
