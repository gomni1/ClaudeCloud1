# TIMING–EXTENT TRADE: does sharper timing cost extent?

**SANDBOX / DRAFT · not promoted · 10 November 2026 · Claude, for Glenn**
Task prompt: TIMING-EXTENT-TRADE v3 (10 Nov 2026), rung note confirmed by Glenn. Standing constraints read first (7 October copy); the question is not recorded there as closed or forbidden. This is a targeted descent below the composite rung, finite, and ends here.

## Plain-words verdict

On this grid and for these candidates, in every ensemble stratum that could be classified, timing width and spatial extent shrink together as the drive strengthens (CO-SHRINK), for E2 and E3 and under both inheritance rules. No ensemble stratum shows a trade. The window-gated event could hardly be classified for ensembles: undecided for E2, and for E3 the 36 classifiable strata (all at ρ = 0.9) show timing and extent both growing with the window (WINDOW-ARTEFACT). As N grows, timing width and across-realisation spread vanish as N^(−1/2) at ρ = 0, while at ρ > 0 they settle at the single shared organisation variable's own noise; the within-pattern extent stays finite in both cases. No trade runs through energy: the only trades found are in single-unit controls, they come from the rest-state start or from the inheritance rule's finite-window velocity estimate, and higher drive energy narrows the extent, which is the opposite sense to the pointer as the task prompt describes it.

| Event | Axis | Inheritance | E2 (ρ = 0) | E3 (0 < ρ < 1) |
|---|---|---|---|---|
| Ev-A | DRIVE | H-nominal | CO-SHRINK (208 of 208 classified) | CO-SHRINK (318 of 318) |
| Ev-A | DRIVE | H-realised | CO-SHRINK (208 of 208) | CO-SHRINK (318 of 318) |
| Ev-B | DRIVE | both | UNDECIDED (0 classified of 160) | UNDECIDED (0 of 796) |
| Ev-B | WINDOW | both | UNDECIDED (0 classified of 136) | WINDOW-ARTEFACT (36 of 36; all ρ = 0.9) |

## Evidentiary limits (read before using any number)

- The rules, events, measures, grid and thresholds are conventions fixed in v3. No verdict here depends on PHYS2 having chosen them.
- **One literal gate in v3 was re-read before the run.** v3 required every P5/P6 test to sit within 5% or 3 standard errors. With more than a thousand tests a few chance exceedances are expected. PRE-RUN-CLARIFICATIONS.md (C1), written before any task simulation, sets a multiplicity allowance. Under C1, P5 and P6 pass. Under v3's literal wording they fail (8 and 10 exceedances at 3–4.4 standard errors). Diagnostics are in P5 below. This was my reading when the run was made. **Glenn accepted C1 on 10 November 2026, after seeing the result and the diagnostics.** The literal-wording failure stays on the record.
- Ensemble cells use L = 16 only and N ≤ 256. Ensemble simulation uses substeps (C6); single-unit simulation is exact event-driven.
- 220 of 480 single-unit cells and 432 of 648 ensemble cells have a drive rate above 1 (OVER-CAP). They are included in classification, as v3 states. Labels restricted to within-cap cells were not computed.
- The observational pointer (Maier et al.) was not read in this task. Prior-art citations in Q7 are from memory and were not re-checked.
- Single-unit strata are controls for the analysis. They are not PHYS2 verdicts.

## Infrastructure checks

Code: `tet_sim.py` (simulator), `tet_exact.py` (exact forms), `tet_analyze.py` (classifier and checks). Output: `results.txt`.

**P1 NULL — pass.** Drive (a_d, b_d) = (m, m) on the single-unit m = 0.2 grid, 240 cells.
- DRIVE axis: 456 strata, 176 classified. TRADE 1, CO-SHRINK 0, so 0.57% (limit 2%). The rest: NONE 104, MIXED 71, UNSTABLE 252, UNCLASSIFIED 28.
- WINDOW axis, Ev-B: 480 strata, 384 classified, 384 WINDOW-ARTEFACT (100%; limit ≥ 90%).

**P2 PLANTED FLOOR — pass.** 200 of 200 synthetic strata classify TRADE; planted infimum 3 gives FLOOR. The numerical cross-check falsely signals a trend in 35 of 200. That cross-check rule is weak at 8 cells and was not needed in the task (no analytic FLOOR arose).

**P3 PLANTED TENDENCY — pass.** 197 TRADE, 3 UNSTABLE; planted infimum 0 gives TENDENCY.

**P4 PLANTED CO-SHRINK — pass.** 200 of 200.

**P5 ANALYTIC — pass under C1; fail under v3's literal wording.**
- Event-time variance against the exact truncated form (Q1): 1161 tests, 8 beyond max(5%, 3 SE), none beyond 5 SE; C1 allows 10. Median |z| 0.72.
- Pulse-end across variance against the exact closed form (Q2): 323 tests, 0 exceedances.
- Diagnostics (`tet_extra.py`, `results_extra.txt`): the mean of simulated/exact variance over the 1161 tests is 0.9996 ± 0.0014. The five flagged cells, rerun with 200 000 realisations and fresh seeds, agree with the exact forms (z between −0.58 and +2.12). All eight exceedances were low-side, as expected when a heavy-tailed sample misses its tail and under-reports its own standard error. I read them as chance.
- Asymptotic forms, reported and not gated: exact/(k²m²D/p_d³) has median 9.7 when the mean number of reversals during the passage a_d·D is below 0.1, 2.1 for 0.1–1, 1.16 for 1–5 and 1.04 above 5. Exact Var(x_τ)/(k²m²τ/E_d³) has median 2.3, 1.13 and 1.00 for fewer than 1, 1–5 and more than 5 mean reversals in the pulse.

**P6 τ-INDEPENDENCE — pass under C1; fail under the literal wording.** 1150 comparisons in 202 groups; 10 beyond 3 SE (C1 allows 10, so this sits on the limit), none beyond 5 SE. The exceedances are in the same cells as P5's.

**Ensemble code check (C6).** At N = 1 with 40 000 realisations the substep code agrees with the exact forms in three drives: variances within 1.5 SE, mean completion times high by 0.003 to 0.05 time units.

**Window census** (cell × D). Single unit: Ev-A in window 1161, CENSORED 615, KINEMATIC 624; Ev-B in window 768. Ensemble: Ev-A in window 2014, CENSORED 470, KINEMATIC 756; Ev-B in window 355, THIN 17. No grid cell is NOT RUN. In Q5, 30 tick cells are NOT ADMISSIBLE.

## Q1 — timing (single unit)

**Plain words.** In this single-unit model, from a rest-state start, the spread of completion times has three parts: a diffusive part that grows with D, and two parts that do not depend on D and come from half the starts stepping backward at onset. The proposed form Δt ≈ k·m·√D/p_d^(3/2) is the first part alone and is far too small when reversals are rare. Under window gating, Δt is a fixed fraction of the time available, τ − D, until the window is wide enough to hold nearly all completions.

**Derivation.** Forward-state passage over distance D is a process with independent increments in D, so its Laplace transform is exp(−Dψ(s)). In forward motion over dx, time dx passes and with probability a·dx an excursion starts: backward for ζ ~ Exp(b), then recovery of ζ. That gives ψ = s + a(s + ψ)/(b + s + ψ), so

 ψ(s) = [−(b − a) + √((b − a)² + 4s(s + a + b))]/2.

A backward start adds an independent delay R = ζ + T₊(ζ) with E[R] = 1/p and E[R²] = a/p³ + 2/p². With a rest start (probability ½ each):

 **Var(T) = a·b·D/p³ + a/(2p³) + 3/(4p²)**, with a = a_d, b = b_d, p = p_d, ab = k²m². (No window.)

In the few-reversal limit the last term is 3/b_d². The in-pulse (truncated) mean, variance and completion fraction come from numerical inversion of the same transform (`trunc_stats` in `tet_exact.py`), checked against 400 000-realisation Monte Carlo in five drives (variance within 0.5%).

**Ev-B.** T lies in [D, τ], so Δt ≤ (τ − D)/2. From the exact forms, in three drives (`results_extra.txt`): Δt/(τ − D) is 0.19–0.31 while the completion fraction is between about 0.5 and 0.95, falls towards 0.11 at fraction 0.45 just above τ = D when the T = D atom dominates, and Δt saturates at the no-window value once the fraction passes about 0.99. Example, m = 0.2, η = 1, boost, D = 8: τ = 12, 16, 24, 32 give fractions 0.62, 0.80, 0.94, 0.98 and Δt 1.22, 2.33, 4.00, 5.08 (simulated 1.20, 2.31, 3.97, 5.05); the no-window value is 6.41.

**Classification.** Exact variance: A proved. "Δt ≈ k·m·√D/p_d^(3/2)": B refuted as stated; it holds only when a_d·D is well above 1. Ev-B scaling: the bound is A; the 0.2–0.3 proportionality is numerical, from exact forms.

## Q2 — GATE (single unit)

**Plain words.** For a single unit under these rules, timing width and across-realisation spread both go to zero as the drive bias grows without limit, so there is no floor anywhere in the uncapped range. If every rate is capped at 1 there is a positive lower bound for the drive-timed event, of about one time unit by two steps; it comes from the cap together with the rest-state start, and it is not a trade. Under H-realised the spread a unit carries forward is the sampling noise of a velocity measured over a finite window. That makes extent fall as the window lengthens whenever the lag is longer than the window: a trade by construction, with no positive infimum.

**Across spread at pulse end (exact, rest start).** With λ = a + b, v = tanh η, u = λτ:

 ⟨x⟩ = v[τ − (1 − e^(−u))/λ]
 E[x²] = 2v²[τ²/2 − τ/λ + (1 − e^(−u))/λ²] + (2/λ){(1 − v²)[τ − (1 − e^(−u))/λ] + v²[(1 − e^(−u))/λ − τe^(−u)]}
 Var(x_τ) = E[x²] − ⟨x⟩² → k²m²τ/E_d³ + (5v² − 2)/(4E_d²) for λτ ≫ 1.

**At lag L, H-nominal.** Exact by propagating the six moments (P±, E[x; ±], E[x²; ±]) through the pulse and post-pulse rate matrices (`disp_moments`). For boost at large λτ this is m²(τ + L)/E³ + (5v² − 2)/(4E²). Simulation against exact over 960 cell-lags: median deviation −0.07 rough standard errors.

**H-realised.** For a single unit v_i = x_τ/(τ + 1/E_d), so Var(v_i) = Var(x_τ)/(τ + 1/E_d)² exactly, about k²m²/(E_d³τ) at large E_dτ (simulated/exact mean 1.0008 over 480 cells). Leading order for the spread at lag L:

 Δx² ≈ Var(x_τ)·[1 + L/(τ + 1/E_d)]² + L·(1 − v̄²)^(3/2)/m.

The first (ballistic) term is the carried-forward velocity noise and falls with τ once τ < L. Simulated/formula has median 0.97–1.01 when E_dτ ≥ 20 and m·L ≥ 3.2, and 0.63–0.85 outside that range (formula too large when few post-pulse reversals occur). H-realised widens the extent: the realised/nominal variance ratio has medians 1.5–3.8 by regime and reaches about 200.

**Infimum of Δt·Δx_across.**

| Case | Over A_free | Over A_cap | Status |
|---|---|---|---|
| Ev-A, DRIVE, either inheritance | 0 (η → ∞: every term in Var(T) and Var(x) carries 1/p or 1/E) | positive on the numerical search: smallest product 1.875 (Δt 1.099, Δx 1.707) at a → 0, b = 1, D = 1, L = 0, fraction 0.95 | A proved for A_free (H-realised via the leading-order form). A_cap: C blocked — a rigorous lower bound on the truncated Δt is missing; Δx ≥ 0.43 is proved |
| Ev-B, either axis, either inheritance | 0 (τ → D⁺: Δt ≤ (τ − D)/2 while Δx stays finite and the T = D atom keeps the cell in window) | 0, same argument | A proved. Grid cells with Δt = 0 exactly were observed |

Uncapped direction, m = 0.2, boost, D = 2, τ = 8: η = 2, 4, 6, 8 give products 1.54, 0.026, 0.00046, 0.000009.

**Grid confirmation (controls).** Ev-A/DRIVE: CO-SHRINK in 280 of 280 classified strata under each inheritance, as expected. Ev-B/WINDOW: WINDOW-ARTEFACT under H-nominal (259 of 259); under H-realised 221 WINDOW-ARTEFACT, 23 TRADE (20 of them at L = 64), 5 NONE, 1 MIXED. Ev-B/DRIVE: MIXED (CO-SHRINK 56, TRADE 32, NONE 20, MIXED 16 under each inheritance); see Q4. Since Q2 settles every single-unit case, these runs are confirmation only. The weight of the task falls on Q3 (does an ensemble change the label) and Q7 (what is missing).

## Q3 — the ensemble fork

**Plain words.** On this grid, neither ensemble candidate shows a trade. Independent primitives average: the pattern's timing and its run-to-run position both sharpen as N^(−1/2), and what is left is the within-pattern spread, which equals the single-unit spread and shrinks with drive. With copying switched on, the run-to-run quantities stop improving with N, because every primitive follows one shared two-state organisation variable.

**Labels.** Table at the top. Δx_within and Δx_across carry the same label in every classified Ev-A stratum (CO-SHRINK; E2 104 + 104, E3 159 + 159 per inheritance). By ρ: 0 → 104, 0.5 → 91, 0.9 → 68 classified per extent family, all CO-SHRINK. By N: 172, 176, 178 classified, all CO-SHRINK. Unclassified Ev-A strata are those with fewer than 5 in-window η values (short τ, large D).

**Ev-B.** For ensembles the completion fraction jumps from near 0 to near 1 over a narrow range of τ or η, so few strata have 5 in-window cells: none at ρ = 0 or 0.5, and 18 per extent family at ρ = 0.9, all WINDOW-ARTEFACT. The operating window for a gated event was looked for and mostly not found on this grid.

**N-scaling** (log–log slope over N = 16, 64, 256; m = 0.2; `results.txt`).

| ρ | Δt (Ev-A) | Δx_across, L = 16 | Δx_within, L = 16 |
|---|---|---|---|
| 0 | −0.506 (IQR −0.521 to −0.492) | −0.507 nominal, −0.502 realised | +0.020 |
| 0.5 | −0.049 | −0.058, −0.048 | +0.018 |
| 0.9 | +0.001 | −0.001, −0.003 | +0.017 |

At ρ = 0 the N^(−1/2) law holds (also proved: the pattern displacement is a mean of N independent copies). Ratios to the single unit in matching cells at N = 256: Δx_across 0.062, 0.335, 0.822 and Δt 0.060, 0.359, 0.848 for ρ = 0, 0.5, 0.9; 1/√256 = 0.0625.

**N → ∞.** At ρ = 0: Δt → 0 and Δx_across → 0; Δx_within tends to the single-unit across spread (ratio 0.996 at N = 256). The question reduces to a deterministic event time and a within-pattern extent that falls with drive energy and grows with τ + L. There is nothing left to trade against. At ρ > 0: conditional on the organisation path the primitives are independent, so the pattern displacement tends to its conditional mean, whose run-to-run variance does not depend on N. The pattern then inherits a smoothed copy of the single-unit statistics.

**TRADE at intermediate ρ only.** None. No ensemble stratum at any ρ is labelled TRADE, and the matching single-unit strata (m = 0.2, L = 16) have none either.

**Classification.** "Sharper timing must cost extent": B refuted as stated for these candidates under the drive-timed event; undecided under the gated event. N^(−1/2) at ρ = 0: A proved, numerically confirmed.

## Q4 — routing

**Plain words.** No ensemble trade was found on this grid, so there is none to route. The single-unit trades found are of two kinds, and in neither does extent follow energy in the pointer's sense.

1. **Ev-B, DRIVE axis (32 strata per inheritance, m = 0.05, short τ).** At weak drive only units already stepping forward complete, at T ≈ D, so timing over completers is sharp; meanwhile half the units run backward, so the across spread is close to τ + L. Stronger drive lets backward starters complete late (Δt rises) and pulls the spread in. Example, m = 0.05, boost, τ = 4, D = 2: η from 0.25 to 3 takes the fraction 0.48 → 0.83, Δt 0.29 → 0.54, Δx 15.0 → 1.7. Route: the rest-state start plus completer selection. Median Spearman(Δx, ΔE) = −1.00.
2. **Ev-B, WINDOW axis, H-realised (23 strata, 20 at L = 64).** The carried-forward velocity noise falls as the window lengthens while gated Δt rises. Route: sampling noise of a velocity estimated over a finite window, visible when L exceeds τ. Median Spearman(Δx, ΔE) = −0.66 (L = 64) and −0.80 (L = 16): extent falls as the realised energy spread rises.

**Sign.** In every classified DRIVE-axis group the median Spearman of Δx against drive energy is −1.00. More drive energy narrows the extent in these candidates. OBSERVATIONAL, shape only: that is the opposite sense to the pointer as the task prompt describes it (tighter timing took more energy and widened the packet). The paper itself was not read here.

**FLOOR or TENDENCY.** Every TRADE stratum is TENDENCY: the analytic infimum is 0 over both ranges for Ev-B (Q2). The product also trends with the axis variable in these strata (median Spearman −0.99 to −0.33 on the DRIVE axis, +1.00 on the WINDOW axis). There is no floor constant to give a dependence for. The capped-range bound of Q2 belongs to CO-SHRINK strata; it scales as 1/N at ρ = 0, persists with N at ρ > 0, and is smallest at L = 0 and D = 1.

**Classification.** Energy routing: B refuted for the trades found. Numerical.

## Q5 — step-scale check

**Plain words.** On the m = 0.2 boost grid, in discrete ticks the labels are the same as in continuous time, and both widths are somewhat larger. Discreteness with a rest-state start does give a single unit a positive bound of about one tick by one step, but it is a resolution limit, not a trade, and it averages away with N at ρ = 0.

**Run** (`tet_ticks.py`, `results_ticks.txt`): m = 0.2, boost, 50 cells; 30 cells (η = 2, 2.5, 3) NOT ADMISSIBLE. Ev-A/DRIVE: CO-SHRINK (6 of 6 classified, each inheritance). Ev-B/WINDOW: WINDOW-ARTEFACT (40 of 40 nominal; 33 of 39 realised, with 2 TRADE). Ev-B/DRIVE: MIXED. Under H-realised, 1837 realisations had an inherited rate capped at 1. Over 88 matched Ev-A cells, ticks/continuous is 1.12 for Δt (0.95–1.31) and 1.05 for Δx (0.94–1.19). Grid minima: ticks Δt 2.18, Δx 3.03, product 6.6; continuous 1.81, 2.66, 4.8.

**Discreteness alone.** With no rate cap, let the backward→forward flip probability go to 1 and the forward→backward probability to 0. A backward starter steps back once and then forward, so T is D or D + 2 with probability ½ each and x_τ is τ or τ − 2. Hence Δt = 1 tick and Δx = 1 step: a **step-scale bound** with product 1. This is derived, not simulated (the limit is not admissible under the cap), and it is not shown to be the infimum over all rates.

**Classification.** A for the limiting value; numerical for the grid.

## Q6 — relaxation

**Plain words.** The response lag is 1/(2E_d) for every candidate, because the rate parametrisation makes it so.

The mean step obeys d⟨σ⟩/dt = (b_d − a_d) − (a_d + b_d)⟨σ⟩. With copying, the primitive's equation gains c(⟨σ_org⟩ − ⟨σ_i⟩), and both start from 0 and obey the same equation, so the term vanishes. Hence ⟨σ⟩ = tanh η·(1 − e^(−2E_d·t)) and the 1 − 1/e time is 1/(2E_d). Simulated lag × 2E_d: medians 0.986–1.017 across single-unit and all nine ensemble groups; the widest ranges (0.72–1.18) are at ρ = 0.9 and η ≤ 0.5, where the target is small and noise is largest.

OBSERVATIONAL, shape only: the lag shortens as drive energy rises. **By construction** — not counted as a finding and not credited to the model.

**Classification.** A proved (identity).

## Q7 — prior art and limits

**Prior art** (E external fact; from memory, not re-checked in this task).
- Feynman's checkerboard (Feynman and Hibbs 1965, problem 2-6): paths at speed 1 with an amplitude factor per reversal.
- Gaveau, Jacobson, Kac and Schulman, Phys. Rev. Lett. 53, 419 (1984): the telegraph process with a real reversal rate, continued to an imaginary rate, gives the 1+1 Dirac equation.
- Persistent random walks and the telegraph equation: Goldstein (1951); Kac (1974). R1-clock from a rest start is this process with asymmetric rates. The first-passage transform in Q1 is standard for it.
- Counting-statistics bounds on timing: thermodynamic uncertainty relations (Barato and Seifert 2015) and their first-passage forms (Garrahan 2017; Gingrich and Horowitz 2017). These trade timing precision against dissipation or activity. They do not involve spatial extent.
- Velocity-memory inheritance: H-realised sets future bias from a time-averaged past velocity. Nearest relatives known to me are reinforced and memory walks (the "elephant" walk, Schütz and Trimper 2004) and walks with quenched random drift. I know of no exact precedent.

**Can a real-probability telegraph process give a FLOOR of the Regensburg shape?** For the candidates here, no: Q2 proves infimum 0 over the uncapped range for every event, axis and inheritance. The general reason is that with non-negative probabilities the timing distribution and the position distribution can be narrowed together towards a deterministic path; nothing ties one width to the inverse of the other. The bounds that do appear are a step-scale resolution limit (Q5), a rate-cap limit (Q2) and finite-sample estimation noise (Q4), and all weaken or vanish with N at ρ = 0. The general statement beyond these candidates is argued, not proved.

**Shaped gap (logged; not added, not run).** As far as the structure fixes it, the missing ingredient would have to make handoff contributions combine with signs or phases, so that contributions from different step histories can cancel. In the GJKS construction that is a fixed phase per reversal in place of a reversal probability. Then narrowing the set of histories in time removes cancellation in position, and the two widths become conjugate. On the argument above, which is not a general proof, a positive-weight rule does not do this at any rates.

## Load-bearing work not yet earned

- **The rest-state start.** In this model it supplies the D-independent terms that dominate Δt when reversals are rare, the capped-range bound, and the Ev-B/DRIVE trades.
- **The organisation variable.** One shared two-state variable is single-unit bookkeeping inside the ensemble candidate. At ρ > 0 it sets the run-to-run quantities measured here at large N (shown for N up to 256, argued beyond). This sits badly with the standing line against single-unit handoff grammar.
- **The rate cap.** The only positive bound found for Ev-A (numerical, not proved) depends on it.
- **H-realised's regulariser and the lag L.** Its trade appears at L = 64 and mostly not at L = 16; a result that depends on an arbitrary lag is not a property of the pattern.
- **R1's unit speed.** In this model it causes the kinematic censoring (τ ≤ D) and the T = D atom that drives the Ev-B results.

## Candidates on the record

- H-nominal and H-realised were both run as fixed. No kill condition for H-realised was pre-registered, so it is neither declared failed nor amended here. The record: it widens extent, its window trade is a finite-window estimation effect, and it does not route through energy.
- E2 and E3 as specified do not produce a trade. No revised rule is offered.

## Summary

| Question | Class | Key numbers | What it means for PHYS2, in one line |
|---|---|---|---|
| Q1 timing | A (exact form); B (proposed approximation) | Var(T) = abD/p³ + a/(2p³) + 3/(4p²); proposed form low by a median factor 9.7 in variance when a_d·D < 0.1 | From rest, timing width is set mostly by the backward-stepping half, not by D |
| Q2 gate | A over A_free; C over A_cap | infimum 0 uncapped; capped search minimum 1.875 | No floor in these single-unit dynamics; the capped bound is a step-scale limit |
| Q3 ensemble | B (trade refuted, Ev-A); undecided (Ev-B) | CO-SHRINK 208/208 (E2), 318/318 (E3); slopes −0.506 at ρ = 0, 0.00 at ρ = 0.9 | Neither ensemble candidate shows a trade on this grid; at ρ > 0 the shared organisation variable carries the noise |
| Q4 routing | B (energy routing refuted) | Spearman(Δx, E_d) = −1.00; 87 single-unit TRADE strata, all TENDENCY | In these candidates extent narrows with drive energy, the opposite sense to the pointer as the prompt describes it |
| Q5 ticks | A (limit); numerical (grid) | Δt = 1 tick, Δx = 1 step in the limit; ticks/continuous 1.12 and 1.05 | In the single-unit model, discreteness gives a resolution limit and no trade |
| Q6 relaxation | A (identity) | lag × 2E_d = 0.99–1.02 (medians) | True by construction of the rates; not a recovered behaviour |
| Q7 limits | E (prior art); argued (general limit) | — | These positive-weight candidates do not give the pointer's shape; the general limit is argued, not proved; the gap (signed or phased handoff) is logged only |

## Files beside this note

In the folder `TIMING-EXTENT-TRADE-2026-11-10-files`, next to this note in AUDIT OUTPUTS: `jev-ledger-summary.json` (the ledger's machine output), `TIMING-EXTENT-TRADE-prompt-v3.md` (task prompt), `PRE-RUN-CLARIFICATIONS.md`, `tet_exact.py`, `tet_sim.py`, `tet_analyze.py`, `tet_ticks.py`, `tet_extra.py`, `results.txt`, `results_ticks.txt`, `results_extra.txt`, `cells.csv` (one row per cell × D; the `idx` column gives each cell's seed under C14), `strata.csv` (every stratum with its label, half-sample correlations and threshold sensitivity), `JEV-LEDGER-REPORT.md`. Threshold sensitivity: 68 of 2564 strata change label if 0.6 is replaced by 0.5 or 0.7, mostly to or from UNSTABLE; no verdict in the table at the top changes. Per-realisation arrays were not kept; every cell is reproducible from its seed.
