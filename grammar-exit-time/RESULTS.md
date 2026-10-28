# Grammar exit times: results

Status: SANDBOX / DRAFT. Not promoted. Nothing here is uniquely derived. Every statement holds only inside the definitions of `SPEC.md`: the open level, the fixed constants, the Kurtz finite-size reading and the targets as defined. The ODE and the Markov chain are effective-register summaries of step processes.

## Freeze

- **Original `SPEC.md`.** SHA-256 `572a96260725e796f119fd5baaf96c5614821a54e83d959738c89162ca78d550`. Frozen 2026-10-28 in commit `e52d832`, before any code was written or run.
- **Revision 1 `SPEC.md`.** SHA-256 `1cfe3572da4515612b3c62d1b350304e5b6f628042161e2f955a932c76a0fd29`. Committed in `d7b4573`. This is the file in the tree; `run_all.py` recomputes this hash and logs it in `evidence/run_log.txt`.
  - It follows the source prompt's same-day revision and changes framing only: the map gap's name, the "what this run can and cannot show" limit, and the observational-register scope.
  - Before it, only M0, a timing test and a solver test had run (SPEC §12). No production run had started.

No rate, threshold, target, start, grid, budget, estimator or criterion was changed after the freeze. Every failure below stays on the record.

## Scope limit (stated beside every verdict)

The ensemble is well mixed, so every cost in it grows with Ω by construction. The run tests "Lifetimes: memoryless, ensemble-scaled…" for this grammar at these rates. It cannot see a localised path whose cost does not grow with the ensemble, such as nucleation or collapse at lattice scale. Literature on discrete media shows such paths exist: a lattice skyrmion's collapse, for example, keeps a finite cost as the lattice is refined. In the verdict table this limit is written **[well-mixed limit]**.

## Answer to the question

At fixed rates, both times grow with Ω, but at costs per unit of ensemble that differ by more than three orders of magnitude.

1. **Dissolution (D: nC = nL = 0).**
   - On the simulator data and on gMAM, the mean time from the settled state grows exponentially, and the exit is memoryless.
   - K1's formal verdict is nevertheless underdetermined (harness), because the PF1 W recovery failed.
   - **MA.** gMAM gives W_D = 1.510. The simulator gives W = 1.528 [1.491, 1.567] over Ω = 2–10, where T̂ rises from 9.2 to 1.08×10⁵.
   - **TH.** gMAM gives W_D = 0.820 from either stable balance. The simulator gives W = 1.01–1.04 over Ω = 3–14, where T̂ rises from 12 to 2.1×10⁵. That is 23–26% above gMAM (F2, below).
2. **Expression switch (TH only).**
   - gMAM gives W_S↑ = 3.38×10⁻⁴ (from v = 2 to the saddle) and W_S↓ = 1.81×10⁻⁴ (from v = 4).
   - Up to Ω = 4096, the switching times grow only like a power of Ω (β ≈ 0.6): from 2.8 to 119 for S↑ and from 1.8 to 68 for S↓. They are not memoryless (CV 0.7–0.9).
   - With ΩW_S ≤ 1.4 on the whole grid, the switching exponential regime is not reached by simulation. gMAM is the measure of its cost.
3. **Costs per unit of ensemble.** W_D/W_S ≈ 2.4×10³ (v = 2) and 4.5×10³ (v = 4). The ratio stays above 10³ under every reading in the table below.

## Kill conditions

| | Status | Evidence | Limit |
|---|---|---|---|
| **K1** (ensemble scaling, dissolution D) | **underdetermined (harness)** | **Per-series criteria:** survived on all three sufficient series. MA: W = 1.528 [1.491, 1.567], ΔAIC = 6140, 7 sizes, span 5.0. TH2: W = 1.012 [0.984, 1.042], ΔAIC = 4574, 8 sizes, span 4.7. TH4: W = 1.035 [1.007, 1.064], ΔAIC = 4786, 8 sizes, span 4.7. No series has W < 0, an interval that includes 0, or ΔAIC < 10. **Why underdetermined:** the frozen SPEC §8 makes K1 "underdetermined (harness)" if the PF1 W recovery fails, and it did (W = 0.924 [0.896, 0.952] against the required \|W − 1\| ≤ 0.05; see PF1). The harness did correctly refuse to call PF2's linear growth exponential. | [well-mixed limit] |
| **K2** (memoryless exit from the settled state) | **survived** | At the largest size with ≥ 1000 uncensored exits: MA Ω = 10, p = 0.34, CV 1.04, D_n = 0.025. TH2 Ω = 14, p = 0.33, CV 1.01, D_n = 0.025. TH4 Ω = 14, p = 0.081, CV 0.95, D_n = 0.032. Lilliefors-type test, parametric bootstrap B = 10 000. PF4 (Erlang k = 4) is rejected at p = 1×10⁻⁴, so the test has power. No D size of any series is rejected at p < 0.01. | [well-mixed limit] |
| **K3** (two-cost analogue, TH) | **survived** | gMAM: max(W_S↑, W_S↓) = 3.38×10⁻⁴ < min(W_D(v = 2), W_D(v = 4)) = 0.820, a margin of 2.4×10³. No fallback was needed, because every gMAM item converged. | [well-mixed limit] |

As SPEC §11 disclosed, survival of K1's criteria and of K2 is weak evidence: it places this grammar in the class large-deviation theory already covers. The informative outputs are the W values and their ratio.

## W table

| Quantity | gMAM (M4) | Simulator fit (F1, 95% bootstrap) | Other |
|---|---|---|---|
| W_D, MA | **1.5098** (N = 100) | 1.528 [1.491, 1.567] | R1 fit: 1.503 [1.453, 1.551] |
| W_D0, MA | **0.6701** (N = 100) | 0.693 [0.663, 0.722] | |
| W_D, TH from v = 2 | **0.8200** (N = 400) | TH2: 1.012 [0.984, 1.042] | |
| W_D, TH from v = 4 | **0.8202** (N = 400) | TH4: 1.035 [1.007, 1.064] | |
| W_D0, TH from v = 2 | **0.3750** (N = 400) | TH2: 0.463 [0.439, 0.487] | |
| W_D0, TH from v = 4 | **0.3755** (N = 800) | TH4: 0.470 [0.445, 0.496] | |
| W_S↑ | **3.383×10⁻⁴** (N = 100) | M3 diagnostic: −1.0×10⁻⁴ [−1.2, −0.8]×10⁻⁴; no exponential regime | M5: ΔW↑(∞) = 6.28×10⁻⁴ ± 0.31×10⁻⁴ |
| W_S↓ | **1.809×10⁻⁴** (N = 100) | M3 diagnostic: −2.1×10⁻⁴ [−2.3, −1.9]×10⁻⁴; no exponential regime | M5: ΔW↓(∞) = 3.74×10⁻⁴ ± 0.35×10⁻⁴ |
| W_D,eff (TH) | 0.8200 | | U(v = 4) = W_S↑ − W_S↓ = 1.57×10⁻⁴, so v = 2 is the deeper balance |

**gMAM details** (`evidence/gmam_raw.json`, `evidence/gmam_log.txt`):

- Every item converged by the 1% doubling rule.
- **TH dissolution, two initial paths.** The straight path and the path through the saddle and the other balance converge to within 0.3% of each other: W_D 0.8223 against 0.8200 from v = 2, and 0.8225 against 0.8202 from v = 4. The smaller value is reported, as SPEC M4 requires.
- **Optimal end points:**

  | Item | End point (c, v, l, p) |
  |---|---|
  | TH, D | (0, 3.43, 0, 0.198) |
  | TH, D0 | (0, 3.06, 0.578, 0.289) |
  | MA, D | (0, 1.035, 0, 0.337) |
  | MA, D0 | (0, 0.861, 0.916, 0.458) |
- **Discretisation trend.** Values rise slowly with N; the error is O(ln N / N) near the c → 0 singularity. For example, TH W_D0 from v = 2 is 0.3750 at N = 400 (straight path) and 0.3776 at N = 1600 (path through the other balance).
- **Within-level stopping.** Many levels hit the 400-cycle cap of SPEC M4 without meeting the 1e−9 per-cycle test. For W_S, 1e−9 of an action of order 10⁻⁴ is below the inner-solver noise. SPEC M4 accepts the level after 400 cycles; convergence is judged between levels.

**Ratio W_D/W_S:**

| Reading | Ratio |
|---|---|
| W_D(v = 2) / W_S↑ (gMAM) | 2424 |
| W_D(v = 4) / W_S↓ (gMAM) | 4535 |
| min W_D / max W_S (gMAM) | 2424 |
| gMAM W_D / M5 ΔW↑(∞) | 1306 |
| fitted TH2 W / M5 ΔW↑(∞) | 1611 |

## Dissolution series (M1, R1)

- **Exits and censoring.** 1000 recorded exits per size (300 where the budget bound). The censoring cap was ≥ 10× the running mean; no run in any series was censored.
- **Burn-in.** t_b = 10/|λ_slow| = 53.1 (MA), 66.1 (TH, v = 2) and 76.7 (TH, v = 4). Restarts are counted over all attempts.
- **Infeasible sizes.** Sizes the §3 rule found burn-in infeasible are listed below each table. They are excluded from fits and from the six-size count, as preregistered.
- **Projection stops.** Every series was stopped by the §6 projection rule before its next size.

#### MA, D

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 2 | 1000 | 9.212 | [8.658, 9.811] | [8.696, 9.776] | 0.95 | 766817 | 0.30 |
| 3 | 1000 | 22.92 | [21.54, 24.41] | [21.5, 24.39] | 1.03 | 10058 | 0.11 |
| 4 | 1000 | 59.74 | [56.15, 63.63] | [56.03, 63.67] | 1.02 | 1430 | 0.06 |
| 5 | 1000 | 167 | [157, 177.9] | [157, 176.8] | 0.96 | 345 | 0.16 |
| 6 | 1000 | 591.2 | [555.6, 629.6] | [554.6, 629.8] | 1.02 | 98 | 0.81 |
| 8 | 1000 | 7756 | [7290, 8260] | [7288, 8271] | 1.05 | 5 | 0.18 |
| 10 | 1008 | 1.076e+05 | [1.011e+05, 1.145e+05] | [1.008e+05, 1.144e+05] | 1.04 | 0 | 0.34 |

- No size was burn-in infeasible.
- F1: W = 1.528 [1.491, 1.567], β = −1.80, ΔAIC = 6140.
- Local slopes d ln T̂/dΩ: 0.91, 0.96, 1.03, 1.26, 1.29, 1.32.
- Spent 1763 CPU-s. The run stopped before Ω = 12, whose projection was 300 exits × 27.2 s.

#### MA, D0

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 6 | 1008 | 5.735 | [5.392, 6.106] | [5.39, 6.087] | 0.99 | 14116663 | 0.57 |
| 8 | 1000 | 14.41 | [13.55, 15.35] | [13.54, 15.36] | 1.04 | 52053 | 0.14 |
| 10 | 1000 | 37.54 | [35.28, 39.98] | [35.28, 39.99] | 1.02 | 3438 | 0.09 |
| 12 | 1000 | 105.2 | [98.86, 112] | [98.91, 112.1] | 1.03 | 622 | 0.33 |
| 14 | 1000 | 310.1 | [291.5, 330.3] | [293, 328.5] | 0.94 | 190 | 0.43 |
| 16 | 1000 | 957.7 | [900.1, 1020] | [899.8, 1019] | 1.00 | 43 | 0.98 |
| 20 | 1006 | 1.078e+04 | [1.013e+04, 1.148e+04] | [1.011e+04, 1.144e+04] | 1.00 | 3 | 0.85 |

- Burn-in infeasible at Ω = 2, 3, 4, 5.
- F1: W = 0.693 [0.663, 0.722], β = −1.84, ΔAIC = 2187.
- Spent 1046 CPU-s, then stopped by projection.

#### TH from v = 2 (TH2), D

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 3 | 1000 | 12.2 | [11.46, 12.99] | [11.47, 12.98] | 1.01 | 671315 | 0.64 |
| 4 | 1000 | 26.6 | [25, 28.33] | [25.09, 28.2] | 0.97 | 23738 | 0.72 |
| 5 | 1000 | 59.39 | [55.82, 63.25] | [55.79, 63.04] | 1.01 | 3869 | 0.86 |
| 6 | 1000 | 126.2 | [118.6, 134.4] | [118.6, 134.1] | 0.98 | 983 | 0.17 |
| 8 | 1000 | 855.4 | [803.9, 911] | [802.4, 912.2] | 1.01 | 139 | 0.08 |
| 10 | 1000 | 5048 | [4744, 5376] | [4743, 5360] | 0.98 | 28 | 0.62 |
| 12 | 1008 | 3.27e+04 | [3.075e+04, 3.482e+04] | [3.078e+04, 3.463e+04] | 0.98 | 4 | 0.18 |
| 14 | 1008 | 2.101e+05 | [1.975e+05, 2.237e+05] | [1.973e+05, 2.233e+05] | 1.01 | 0 | 0.33 |

- Burn-in infeasible at Ω = 2 (acceptance 1×10⁻⁶).
- F1: W = 1.012 [0.984, 1.042], β = −0.88, ΔAIC = 4574.
- Local slopes: 0.78, 0.80, 0.75, 0.96, 0.89, 0.93, 0.93.
- Spent 3153 CPU-s, then stopped by projection.

#### TH2, D0

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 10 | 1000 | 9.473 | [8.903, 10.09] | [8.906, 10.03] | 0.99 | 11568508 | 0.96 |
| 12 | 1000 | 17.76 | [16.69, 18.91] | [16.72, 18.77] | 0.95 | 125179 | 0.29 |
| 14 | 1000 | 38.97 | [36.62, 41.5] | [36.68, 41.36] | 0.97 | 10114 | 0.92 |
| 16 | 1000 | 81.92 | [77, 87.25] | [77.26, 86.85] | 0.98 | 2253 | 0.28 |
| 20 | 1000 | 411.9 | [387.1, 438.7] | [385.6, 437.5] | 1.02 | 255 | 0.10 |
| 24 | 1000 | 2107 | [1980, 2244] | [1977, 2225] | 0.98 | 60 | 0.92 |
| 32 | 304 | 5.685e+04 | [5.081e+04, 6.383e+04] | [5.085e+04, 6.343e+04] | 0.99 | 1 | — |

- Burn-in infeasible at Ω = 2, 3, 4, 5, 6, 8.
- F1: W = 0.463 [0.439, 0.487], β = −1.22, ΔAIC = 1299.
- Spent 990 CPU-s, then stopped by projection.

#### TH from v = 4 (TH4), D

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 3 | 1000 | 13.6 | [12.78, 14.48] | [12.81, 14.39] | 0.97 | 530753 | 0.23 |
| 4 | 1000 | 27.3 | [25.66, 29.08] | [25.59, 29.01] | 1.00 | 16793 | 0.98 |
| 5 | 1000 | 60.14 | [56.52, 64.04] | [56.26, 64.13] | 1.03 | 2585 | 0.72 |
| 6 | 1000 | 135.3 | [127.2, 144.1] | [127.5, 143.6] | 0.99 | 704 | 0.50 |
| 8 | 1000 | 831.9 | [781.9, 886] | [780.3, 884.9] | 1.02 | 82 | 0.84 |
| 10 | 1000 | 4992 | [4692, 5317] | [4695, 5293] | 1.01 | 16 | 0.93 |
| 12 | 1000 | 3.2e+04 | [3.007e+04, 3.407e+04] | [3.023e+04, 3.387e+04] | 0.92 | 3 | 0.13 |
| 14 | 1008 | 2.143e+05 | [2.015e+05, 2.282e+05] | [2.024e+05, 2.268e+05] | 0.95 | 0 | 0.08 |

- Burn-in infeasible at Ω = 2 (acceptance 5×10⁻⁷).
- F1: W = 1.035 [1.007, 1.064], β = −1.11, ΔAIC = 4786.
- Local slopes: 0.70, 0.79, 0.81, 0.91, 0.90, 0.93, 0.95.
- Spent 3224 CPU-s, then stopped by projection.

#### TH4, D0

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 10 | 1008 | 9.379 | [8.817, 9.986] | [8.735, 10.08] | 1.08 | 3773417 | 0.26 |
| 12 | 1000 | 19 | [17.86, 20.23] | [17.87, 20.13] | 1.00 | 52601 | 0.82 |
| 14 | 1000 | 37.72 | [35.46, 40.18] | [35.47, 40.17] | 0.99 | 5819 | 0.15 |
| 16 | 1000 | 79.73 | [74.93, 84.91] | [74.85, 84.6] | 0.98 | 1386 | 0.43 |
| 20 | 1000 | 422 | [396.6, 449.4] | [396.3, 449.7] | 1.01 | 156 | 0.61 |
| 24 | 1000 | 2027 | [1905, 2158] | [1902, 2159] | 0.98 | 29 | 0.29 |
| 32 | 304 | 5.874e+04 | [5.249e+04, 6.594e+04] | [5.244e+04, 6.553e+04] | 0.99 | 1 | — |

- Burn-in infeasible at Ω = 2, 3, 4, 5, 6, 8.
- F1: W = 0.470 [0.445, 0.496], β = −1.37, ΔAIC = 1343.
- Spent 1085 CPU-s, then stopped by projection.

#### R1: MA with reaction 11 as k11·nC(nC − 1)/Ω, target D

| Ω | exits | T̂ | 95% χ² interval | bootstrap | CV | restarts | M2 p |
|---|---|---|---|---|---|---|---|
| 2 | 1000 | 11.2 | [10.52, 11.92] | [10.51, 11.92] | 1.02 | 240579 | 0.79 |
| 3 | 1000 | 26.17 | [24.59, 27.87] | [24.58, 27.73] | 1.01 | 6488 | 0.03 |
| 4 | 1000 | 72.39 | [68.03, 77.09] | [68.18, 77.24] | 0.99 | 1115 | 0.89 |
| 5 | 1000 | 218.8 | [205.7, 233] | [205, 232.9] | 1.02 | 273 | 0.59 |
| 6 | 1000 | 693 | [651.4, 738.1] | [652.1, 736] | 0.99 | 72 | 0.84 |
| 8 | 1001 | 8473 | [7964, 9024] | [7957, 9008] | 1.02 | 3 | 0.53 |
| 10 | 304 | 1.341e+05 | [1.198e+05, 1.506e+05] | [1.19e+05, 1.499e+05] | 1.03 | 0 | — |

- F1: W = 1.503 [1.453, 1.551], β = −1.71, ΔAIC = 3881.
- Spent 711 CPU-s; Ω = 10 ran at 300 exits, then the series stopped by projection.

**Behaviour as disclosed.** After burn-in, the TH2 and TH4 dissolution series coincide, as SPEC §11 expected:

| Ω | TH2 T̂ | TH4 T̂ |
|---|---|---|
| 14 (D) | 2.10×10⁵ | 2.14×10⁵ |
| 32 (D0) | 5.69×10⁴ | 5.87×10⁴ |

Here W_D(v = 2) = W_D(v = 4) to 0.03%, so the series cannot separate W_D,eff from either start's own W_D.

## Expression switches (M3, M5)

**M3** (no burn-in; 1000 runs per direction per size; no censoring; 1091 CPU-s; full grid reached):

| Ω | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T_S↑ mean | 2.794 | 4.289 | 6.723 | 10.34 | 15.50 | 23.33 | 33.43 | 48.12 | 63.98 | 79.48 | 119.3 |
| T_S↑ CV | 1.09 | 0.87 | 0.79 | 0.69 | 0.69 | 0.71 | 0.78 | 0.80 | 0.83 | 0.77 | 0.83 |
| T_S↓ mean | 1.767 | 2.928 | 4.448 | 7.099 | 11.72 | 18.43 | 27.16 | 34.67 | 43.78 | 53.05 | 68.20 |
| T_S↓ CV | 1.14 | 1.12 | 1.09 | 0.98 | 0.90 | 0.89 | 0.80 | 0.81 | 0.82 | 0.74 | 0.69 |

- **Standard errors.** About 2–4% of the mean.
- **Passage through D.** The fraction of switching runs that passed through D first is 0.158 (S↑) and 0.068 (S↓) at Ω = 4, 0.015 and 0.003 at Ω = 8, and 0 from Ω = 16 on.
- **Memorylessness (M2 diagnostic).** S↑ is rejected at every size (p ≤ 1×10⁻⁴). S↓ is rejected at p ≤ 0.015 at every size, and at p ≤ 4×10⁻⁴ from Ω = 32 on.
- **F1 diagnostic.** S↑: W = −1.0×10⁻⁴, β = 0.58. S↓: W = −2.1×10⁻⁴, β = 0.62. The pure power law is the better description, so no exponential regime is reached, and the K3 fallback was not needed.

The probe values are reproduced (S↑ 2.7, 4.4, … against 2.79, 4.29, …).

**M5.** Time-weighted pmf of nV, one run per size of length 400 × max(T̂_S↑, T̂_S↓), unscaled. Errors are from 20 blocks.

| Ω | switches | π(2Ω) | π(3Ω) | π(4Ω) | ΔW↑ | ΔW↓ |
|---|---|---|---|---|---|---|
| 1024 | 485 | 4.19×10⁻⁴ | 2.86×10⁻⁴ | 4.13×10⁻⁴ | 3.73×10⁻⁴ ± 0.52×10⁻⁴ | 3.59×10⁻⁴ ± 0.76×10⁻⁴ |
| 2048 | 440 | 3.48×10⁻⁴ | 9.45×10⁻⁵ | 2.44×10⁻⁴ | 6.37×10⁻⁴ ± 0.32×10⁻⁴ | 4.63×10⁻⁴ ± 0.39×10⁻⁴ |
| 4096 | 468 | 2.99×10⁻⁴ | 2.98×10⁻⁵ | 1.41×10⁻⁴ | 5.63×10⁻⁴ ± 0.19×10⁻⁴ | 3.79×10⁻⁴ ± 0.19×10⁻⁴ |

- **Extrapolation.** A weighted linear fit in 1/Ω gives ΔW↑(∞) = 6.28×10⁻⁴ ± 0.31×10⁻⁴ and ΔW↓(∞) = 3.74×10⁻⁴ ± 0.35×10⁻⁴.
- **Against gMAM:** +86% (↑) and +107% (↓). Both are **outside the 25% consistency band**. This is reported, and neither value is adjusted.
- **Where M5 and M4 agree.** They agree on the order of magnitude (10⁻⁴) and on the ordering W_S↑ > W_S↓ (v = 2 is the deeper balance; π(4Ω) < π(2Ω)).
- **Why M5 is not a clean measure here.** At these sizes ΩW_S ≤ 1.4 on gMAM's values (≤ 2.3 on M5's own), so (1/Ω)·ln of the prefactor ratio is of the same size as W itself. The three points are not monotone in 1/Ω, so the extrapolation is fragile.
- **The disclosed caveat does not explain the gap.** The hyperplane-minimum caveat (SPEC M5) would push ΔW *below* W_S, not above it.

## Harness checks

**M0 (deterministic).**

| Balance | Point | Residual | Eigenvalues |
|---|---|---|---|
| MA | (1, ½, 1, ½) | 0 | −60.07, −4.24, −2, −0.188 |
| TH | (1, 2, 1, ½) | ≤ 3×10⁻¹⁵ | −3.03, −2, −0.484, −0.151 |
| TH (saddle) | (1, 3, 1, ½) | ≤ 3×10⁻¹⁵ | −2.97, −2, −0.071, **+0.295** |
| TH | (1, 4, 1, ½) | ≤ 3×10⁻¹⁵ | −3.07, −2, −0.200, −0.130 |

- **Balance algebra.** The TH balance cubic has roots 2, 3 and 4, and the identity S(y) − A = (y − 2)(y − 3)(y − 4)/(1 + y)² holds to 7×10⁻¹⁵.
- **λ_slow.** −0.1883, −0.1514 and −0.1303, against the hand values −0.188, −0.153 and −0.128 disclosed in SPEC.
- **Drift check (a).** The C propensities reproduce f(n/Ω) to 1.3×10⁻¹⁴ under MA and TH, at Ω = 10 and 1000. For R1 the difference equals k11·(nC/Ω)/Ω exactly (error 1×10⁻¹⁴), shrinking from 5.07 at Ω = 10 to 0.052 at Ω = 1000.
- **Drift check (b), single trajectory at Ω = 10⁵.** Maximum deviation 0.0059 (MA) and 0.0162 (TH), so it passes ≤ 0.02 with the recorded seeds. *Seed dependence, found after the run:* over 32 seeds, TH single trajectories reach a median deviation of 0.030 at t = 5 (maximum 0.10). This is diffusion along the weakly damped v direction (the spread in v is 0.040 at t = 5), not a drift error. The mean over 64 seeds stays within about 2 standard errors of the ODE for both laws (`tests/test_m0.py`).
- **Attraction and cycles.** All 200 + 200 random starts converge to a stable balance (distance ≤ 1×10⁻¹¹). No sustained cycle was seen.

**M6 (exact master equation against the simulator).**

| Start | Ω | Frozen rule | Lattice levels: T (states) | Exact | Simulator (n = 2000) ± SE | z |
|---|---|---|---|---|---|---|
| MA | 2 | converged | 5.29103 (9.8k), 5.22102 (127k), 5.22102 (1.83M) | 5.22102 | 4.930 ± 0.149 | −1.96 |
| MA | 3 | unconverged | 21.6659 (20k), 21.4893 (276k); next level 4.04M > 4×10⁶ | 21.4893 | 21.82 ± 0.51 | +0.66 |
| MA | 4 | unconverged | 60.8443 (27k), 59.0797 (371k); next level 5.5M | 59.0797 | 59.10 ± 1.35 | +0.01 |
| TH v = 2 | 2 | converged | 2.71063 (16k), 2.60139 (217k), 2.60138 (3.16M) | 2.60138 | 2.559 ± 0.064 | −0.67 |
| TH v = 2 | 3 | unconverged | 7.66838 (35k), 6.40032 (486k); next level 7.2M | 6.40032 | 6.391 ± 0.191 | −0.05 |
| TH v = 2 | 4 | unconverged | 21.3195 (57k), 15.9622 (795k); next level 11.9M | 15.9622 | 16.77 ± 0.51 | +1.60 |
| TH v = 4 | 2 | converged | 4.19147 (25k), 4.18853 (337k) | 4.18853 | 4.294 ± 0.102 | +1.04 |
| TH v = 4 | 3 | unconverged | 11.2405 (58k), 11.1241 (801k); next level 11.6M | 11.1241 | 11.46 ± 0.26 | +1.27 |
| TH v = 4 | 4 | unconverged | 27.1590 (97k), 26.2767 (1.36M); next level 21M | 26.2767 | 26.99 ± 0.60 | +1.18 |

- **Under the frozen rule.** The three converged cases agree within 3 SE. The other six are **unconverged**: the next doubling exceeds the preregistered 4×10⁶-state limit.
- **Size of the truncation effect.** It is large for TH at small Ω, and larger V caps *shorten* T. Dissolution at small Ω runs through large V reserves, which dilute x and starve recruitment.
- **Solver residuals.** All linear solves reach a relative residual ≤ 5×10⁻¹¹.

*Post-freeze supplementary check (a new claim, logged here, not preregistered;* `gexit/m6_supp.py`, `evidence/m6_supp*.json`*).* For each unconverged case:

1. From the finest preregistered level, double each species' cap on its own.
2. Keep the doublings that move T by more than 0.1%, and repeat.
3. Stop when no single-cap doubling does.

Results:

| Start | Ω | Caps (C, V, L, P) | T (supplementary) | Largest single-cap change | Converged | Simulator z |
|---|---|---|---|---|---|---|
| MA | 3 | (24, 20, 24, 20) | 21.4893 | 5.8e-10 | yes | +0.66 |
| MA | 4 | (28, 20, 28, 20) | 59.0797 | 4.1e-08 | yes | +0.01 |
| TH v = 2 | 3 | (24, 36, 24, 20) | 6.40032 | 8.4e-06 | yes | -0.05 |
| TH v = 2 | 4 | (28, 44, 28, 20) | 15.9622 | 1.1e-05 | yes | +1.60 |
| TH v = 4 | 3 | (24, 60, 24, 20) | 11.1241 | 2.5e-07 | yes | +1.27 |
| TH v = 4 | 4 | (28, 76, 28, 20) | 26.2767 | 5.4e-07 | yes | +1.18 |

- Every case converges at its level-2 caps: no single-cap doubling moves T by more than 1.1×10⁻⁵.
- So the level-1-to-level-2 jumps under the frozen rule came from level-1 caps that were too small (for TH v = 2, the V cap cutting off the large-V dissolution route), not from a slowly converging tail.
- On this post-freeze evidence, all nine M6 cases agree with the simulator within 3 SE (|z| ≤ 1.96). The preregistered status stays as recorded above: three converged and six unconverged.

- **F2 (fitted W against gMAM W_D, within 25%).**

  | Series | Gap | Verdict |
  |---|---|---|
  | MA D | +1.2% | consistent |
  | MA D0 | +3.4% | consistent |
  | TH2 D | +23.4% | consistent |
  | TH2 D0 | +23.5% | consistent |
  | TH4 D | **+26.2%** | not consistent |
  | TH4 D0 | **+25.3%** | not consistent |

  - The TH4 gaps stay on the record, and neither value is adjusted.
  - The sizes may not be called pre-asymptotic. The preregistered test fails: for TH4 D, the β-corrected local slopes have Spearman ρ = 0.25 (p = 0.59), and the last corrected slope (1.036) is no closer to 0.820 than the fit is.
  - Under TH the simulator's exponent is consistently about 25% above gMAM, while under MA the two agree to 1–3%.
- **R1 (combinatorial reaction 11).** W = 1.503 [1.453, 1.551] against MA's 1.528 [1.491, 1.567]. The intervals overlap, so the leading exponent is unchanged. The prefactor changes: T̂_R1/T̂_MA = 1.22, 1.14, 1.21, 1.31, 1.17, 1.09, 1.25 at Ω = 2, 3, 4, 5, 6, 8, 10.
- **PF1 (immigration–death, exact W = 1) — FAILED (W recovery).**
  - W = 0.924 [0.896, 0.952], β = −0.65, ΔAIC = 3743, against the required \|W − 1\| ≤ 0.05.
  - Coverage passed: T_ex = 1/λ₀ (4.441, 18.15, 83.92, 437.9, 2489, 14957) lies inside the 95% χ² interval at all six sizes, and inside the Bonferroni intervals too.
  - Diagnosis: model E fitted to the *exact* PF1 times on the same grid gives W = 0.9505, already at the edge of the band. The rest of the shortfall is sampling noise (z of ln T̂/T_ex between −1.5 and +1.8).
  - A diagnostic with 20 000 runs at Ω = 4 and 8 found no simulator bias: the quasi-stationary and fixed-start means match the exact values within 1.3σ at 0.7% precision.
  - Consequence (frozen SPEC §8): K1 is underdetermined (harness).
- **PF2 (neutral drift) — passed.** W = −0.0034 [−0.0070, +0.0002] and ΔAIC = 0.4, so all three K1 criteria trigger. T̂ = 1.01, …, 8.11 against exact 1.03, …, 8.37 (linear in Ω).
- **PF3 (censoring) — passed.** At Ω = 8 the cap was 527.2 and 28.7% of runs were censored. The MLE gave 424.7, with interval [394.6, 457.7] containing T_ex = 437.9. The naive mean, 302.8, lies below both.
- **PF4 (Erlang k = 4) — passed.** Rejected at p = 1×10⁻⁴ (D_n = 0.267, CV 0.49).
- **gMAM validations.**

  | Check | Result | Exact |
  |---|---|---|
  | G1 (immigration–death) | 0.9965 | 1 |
  | G2 (two copies) | 1.9931 | 2 |
  | Free-end-point variant | 0.9965, end point 0.99994 | 1, end point 1 |

  All within 1%. The numba kernel agrees with the numpy reference to 7×10⁻⁹ relative.
- **Tests.** `python -m pytest -q`: 29 passed, plus 1 strict expected failure (the PF1 W recovery).

## Walls that bit, deviations and implementation notes

1. **SPEC revision 1** (framing only), made after M0, a timing test and a solver test had run (§Freeze, SPEC §12).
2. **PF1's W recovery failed**, so K1 is underdetermined (harness). This is the frozen rule, applied as written.
3. **F2 failed narrowly for TH4** (D +26.2%, D0 +25.3%), and the pre-asymptotic exemption was not earned.
4. **M5 is inconsistent with M4** by a factor of about 2. Not adjusted.
5. **M6.** Six of nine cases are unconverged under the frozen 4×10⁶-state limit. The supplementary per-species check above is a post-freeze addition.
6. **M0 drift check (b)** passes with the recorded seeds but is seed-dependent under TH. Diagnosed above; the threshold is unchanged.
7. **Burn-in infeasibility (SPEC §3)** removed TH Ω = 2 from both D series and the small-Ω sizes from every D0 series, as disclosed beforehand.
8. **Budget.**
   - Simulator CPU (SPEC §6 definition) totalled about 3.7 CPU-h of the 8 allowed.

     | Series or stage | CPU-s |
     |---|---|
     | MA (D 1763 + D0 1046) | 2809 |
     | TH2 (D 3153 + D0 990) | 4143 |
     | TH4 (D 3224 + D0 1085) | 4309 |
     | R1 | 711 |
     | M3 | 1091 |
     | M5 | 277 |
     | PF and M6 | < 60 |

   - Every series was stopped by the projection rule; none exceeded its cap.
   - Not counted as simulator time: gMAM about 0.8 CPU-h, and the exact master-equation solves about 1 CPU-h.
9. **Implementation notes.** None of these changes a preregistered quantity.
   - **gMAM inner problem.** SPEC M4 describes Newton on the KKT system. That stalled near c → 0, so the implemented solver is equivalent but robust: convex Newton in θ for fixed λ, and a safeguarded Newton step in log λ on the increasing function H(θ(λ)). The functional and the inner problem are unchanged.
   - **gMAM equal-arclength constraint.** During each L-BFGS-B phase it is enforced by a spacing penalty κ Σ(|dᵢ|/mean − 1)², with κ = 1, as well as by reparametrisation. Without it, L-BFGS clustered points at the log singularity and lowered the discrete action below the true value (0.93 against 1 on G2b). The reported action never includes the penalty and is always evaluated on the reparametrised path.
   - **gMAM gradient bug.** A multiplier error in ∂ℓ/∂x (λ in place of 1/λ) was found by a finite-difference check and fixed before any M4 item ran.
   - **M6 solver.** The direct sparse LU did not scale; the AIR multigrid ran out of memory at 3.2M states. Ruge–Stüben AMG with GMRES and refinement was used.
   - **Restarts.** The gMAM and M6 jobs were restarted several times during the session: to add logging, after an out-of-memory kill, for a solver-tolerance fix, and after a process-kill mistake. Every reported value comes from the last complete run, and no partial results were selected.

## Stop points

- No sustained cycle appeared under TH, so the phase-structure part was not needed.
- gMAM converged for every item; no fallback was used.
- No item needed another rule.
- Out of scope and not attempted: the closed level, other rate constants, coupling between levels, a spatial lattice, and the winding.

## Expected outcomes against the run

- **Theory (K1 criteria and K2 survive).** Confirmed in the series. K1's verdict is still underdetermined (harness), because of PF1.
- **Probe numbers.** Reproduced within noise at the shared sizes. MA D from the balance: 4.6, 60, 560, 7700, against post-burn-in 9.2 (Ω = 2, different start state), 59.7, 591, 7756. Switching S↑ matches.
- **"W_D of order 1".** Confirmed: 1.51 (MA) and 0.82 (TH).
- **"K3 survives by a wide margin".** Confirmed (margin about 2400).
- **Spec-time estimate W_S ≈ 10⁻³–10⁻².** **Wrong:** W_S is 1.8–3.4×10⁻⁴, an order of magnitude smaller. The switching exponential regime therefore lies beyond Ω ≈ 4096 (ΩW_S↑ = 1.4 there).

## Gap to the architecture's integer

The link from this grammar's dissolution and expression switch to the architecture's integer invariant is a **named gap**. This run does not attempt it. Neither quantity measured here is that invariant.

## Observational register

This run bears on the rare branch of the map gap "Is the integer's passage forbidden or rare?" only by analogy. Neither quantity it measures is the nucleon architecture's integer invariant.
