# Grammar exit times: preregistered specification

Status: SANDBOX / DRAFT. Not promoted. This file was written and frozen before any code was written or run. Its SHA-256 is recorded in `RESULTS.md`. After the freeze, no rate, threshold, target, start, grid, budget or criterion changes. A revision is a new claim and is logged as one. Any failure stays on the record.

Date: 2026-10-28. Source: CC-PROMPT-Grammar-Exit-Time-2026-10-28. Map items: "Lifetimes: memoryless, ensemble-scaled, phase-structured when cycling" (a working consequence) and "What makes the integer's passage rare?" (an open gap). Nothing in this run adds a rule.

## 0. Register and walls

- **Coarse-grained register.** The ODE and the Markov chain below are effective-register summaries of step processes. They are not a claim about the step processes themselves.
- **No new rule.** The grammar, constants and rate laws are those on the map. The finite-size reading (§2, the Kurtz density-dependent chain) is the one modelling choice. R1 is its robustness check. If an item needs another rule, the run stops at that item and reports what it would need.
- **Neutral labels.** Mechanical text uses C, V, L, P, "dissolution" and "expression switch". Particle names appear only in the single section of `RESULTS.md` headed "Observational register".
- **Out of scope.** The closed level, other rate constants, coupling between levels, a spatial lattice, and any attempt to connect to the winding. The phase-structure part of the lifetimes item is out of scope, because no level cycles under MA. The link from this grammar to the architecture's integer invariant is a named gap and is not attempted.

## 1. Grammar (deterministic)

Densities x = (c, v, l, p) ≥ 0. Stoichiometric vectors ν are in the order (c, v, l, p).

| # | Transition | Rate r(x) | ν |
|---|---|---|---|
| 1 | C → L | k1·c | (−1, 0, +1, 0) |
| 2 | C → V | k2·c | (−1, +1, 0, 0) |
| 3 | V + C → 2C | r3 | (+1, −1, 0, 0) |
| 5 | L → V | k5·l | (0, +1, −1, 0) |
| 6 | L → C | k6·l | (+1, 0, −1, 0) |
| 7 | C → P | k7·c | (−1, 0, 0, +1) |
| 8 | P → V | k8·p | (0, +1, 0, −1) |
| 9 | P → ∅ | k9·p | (0, 0, 0, −1) |
| 10 | V → C | k10·v | (+1, −1, 0, 0) |
| 11 | 2C → V + C | r11 | (−1, +1, 0, 0) |
| 12 | ∅ → V | k12 | (0, +1, 0, 0) |

**Rate laws** (both use the same constants):

- **MA:** r3 = k3·v·c and r11 = k11·c².
- **TH:** x = c/(c + v), with x = 0 when c + v = 0; r3 = k3·v·x² and r11 = k11·c·x². This is m = 2, kr = kc = 2, F₂(x) = Pr[Bin(2, x) ≥ 2] = x².

**Constants:** (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12) = (2, 9, 47, 1, 1, 1, 1, 1, 1, 13, ½).

**ODE:** dx/dt = f(x) = Σ_r r_r(x)·ν_r.

**Statements re-derived in M0:**

- **MA.** There is one balance, (c, v, l, p) = (1, ½, 1, ½), given by c* = k12(k8 + k9)/(k7·k9), l* = k1c*/(k5 + k6), p* = k12/k9 and v* = (A·c* + k11·c*²)/(k10 + k3·c*), with A = k2 + k7 + k1k5/(k5 + k6) = 11. It is stable.
- **TH.** There are three balances, at c = 1, l = 1, p = ½, with v = 2 (stable), v = 3 (unstable, one positive eigenvalue ≈ 0.30) and v = 4 (stable). With y = v/c*, the balance condition is S(y) − A = (y − 2)(y − 3)(y − 4)/(1 + y)².

**Hand values, disclosed.** These were computed by hand from the Jacobian while writing this spec, before any code. In coordinates (c, N, l, p), with N = c + v + l + p, one eigenvalue is always −(k8 + k9) = −2, and the other three solve a cubic. The hand values are:

| Balance | λ_slow | t_b = 10/\|λ_slow\| |
|---|---|---|
| MA | ≈ −0.188 | ≈ 53 |
| TH, v = 2 | ≈ −0.153 | ≈ 65 |
| TH, v = 4 | ≈ −0.128 | ≈ 78 |

The TH saddle has an unstable eigenvalue ≈ +0.298. M0 recomputes all of these, and only the code values are used.

## 2. Stochastic model (the one modelling choice)

**State.** Counts n = (nC, nV, nL, nP) ∈ ℕ⁴, with ensemble size Ω > 0. Each propensity is a_r(n) = Ω·r_r(n/Ω): the density-dependent Markov chain whose large-Ω limit is the ODE of §1 (Kurtz). Explicitly:

- reactions 1, 2, 5–10: the constant times the count (for example k1·nC);
- reaction 12: k12·Ω;
- reaction 3: MA k3·nV·nC/Ω; TH k3·nV·x²;
- reaction 11: MA k11·nC²/Ω; TH k11·nC·x²;
- x = nC/(nC + nV), and x = 0 when nC + nV = 0.

**Boundary detail, kept.** Under MA, reaction 11 can remove a lone C (at nC = 1 it has propensity k11/Ω). The TH form does the same.

**R1 variant (robustness check only).** Reaction 11 under MA is replaced by the combinatorial form k11·nC(nC − 1)/Ω. Nothing else changes.

**Simulator.**
- An exact stochastic simulation algorithm (Gillespie direct method) written in C and called from Python.
- RNG: xoshiro256**, seeded through splitmix64 from (master seed 20261028, series, size, batch).
- Times are held in double precision. The target is checked after every event.

## 3. Sets and starts

**Targets.**

| Name | Set | Used for |
|---|---|---|
| D (primary dissolution) | nC = 0 and nL = 0 | both laws |
| D0 (secondary dissolution) | nC = 0 | both laws |
| S↑ | first time nV ≥ 4Ω, started from the v = 2 balance | TH only |
| S↓ | first time nV ≤ 2Ω, started from the v = 4 balance | TH only |

D is reachable but not absorbing, because seeding (V → C) and supply continue. A run stops at its first hit.

**Starts.** Each run starts from the start balance x_b, rounded to counts by n_s = ⌊Ω·x_b,s + ½⌋ (round half up).

| Series | Start x_b |
|---|---|
| MA | (1, ½, 1, ½) |
| TH2 | (1, 2, 1, ½) |
| TH4 | (1, 4, 1, ½) |

**Burn-in (dissolution runs: M1, R1, PF1).**
- Each attempt starts at the rounded balance and runs for t_b = 10/|Re λ_slow|. Here λ_slow is the eigenvalue of the ODE Jacobian at the start balance with the smallest |Re λ|, computed in M0; it is not chosen. For R1, the MA value is used.
- An attempt that hits the target during burn-in is discarded and restarted from the balance, and the restart is counted.
- The exit time of an accepted attempt is measured from t_b. This samples the quasi-stationary state.

**Burn-in feasibility (disclosed reason).** The hand values of §1 give t_b ≈ 53–78. A restart scheme needs about exp(t_b/T) attempts per accepted run, so it is expected to be infeasible where the exit time T is short: TH at Ω = 2, and D0 at small Ω. The rule is fixed now:

1. At every size, a pilot runs first. It stops at 16 recorded exits, at 2×10⁶ burn-in attempts, or at 360 CPU-s, whichever comes first.
2. If the pilot ends with fewer than 16 exits and more than half its CPU time went into burn-in attempts that hit the target, the size is **burn-in infeasible**. It is reported with its acceptance rate, contributes no point to any fit, and does not count toward the six-size requirement. The series then continues to the next size.
3. If the pilot ends with fewer than 16 exits for any other reason, the size is budget-limited, and the series stops.

**Switching runs (M3)** and **exact-check runs (M6, PF2)** have no burn-in. They start at the rounded start state.

## 4. Estimators

- **Censoring cap.** Each run is censored at a cap on post-burn-in time:

  cap = 10 × max(T_proj, T̂_run).

  - T̂_run is the MLE from the runs already completed at this size. It is used only once at least 10 exits have been recorded at the size; until then cap = 10 × T_proj.
  - T_proj is 1000 time units at the first size of a series. At the second size it is 3 × T̂_prev × exp(3·ΔΩ). From the third size on, it is 3 × the log-linear extrapolation of T̂ in Ω from the previous two fitted sizes.

  Larger caps are always allowed ("at least 10×"). The only exception is PF3 (§9).
- **MLE.** T̂ = S/d, where S is the total observed post-burn-in time, Σ min(τ_i, cap_i), and d is the number of exits.
- **95% chi-square interval:** [2S/χ²₀.₉₇₅(2d + 2), 2S/χ²₀.₀₂₅(2d)]. This is the time-truncated form.
- **Bootstrap interval.** Runs (observed time, exit flag) are resampled with replacement within the size, T̂ is recomputed, and the 2.5–97.5 percentile interval of B = 2000 resamples is reported.
- **Censored count.** Reported at every size.
- **Exits per size.** A production size runs until 1000 exits are recorded. Censored runs are added on top and kept in S. The budget rule of §6 can lower the count to 300.
- **CV.** The sample standard deviation divided by the mean, over uncensored exit times.
- **Memorylessness (M2).** Applied at every size with at least 1000 uncensored exits, to the uncensored exits only.
  - D_n = sup_x |F_n(x) − (1 − e^(−x/τ̄))|, the KS statistic against an exponential with the sample mean τ̄.
  - p-value from a parametric bootstrap (Lilliefors type): B = 10 000 samples of n exponentials, each with its own estimated mean.
  - A plain KS p-value is not used.

## 5. Measurements

### M0. Deterministic checks

1. **Balances.**
   - Residual |f(x_b)| ≤ 1e−12 at each balance.
   - Uniqueness of the MA balance and the count of three TH balances, from the algebra: c* is fixed by the P equation and conservation (dN/dt = k12 − k9·p), and v solves a linear (MA) or cubic (TH) equation. The cubic's roots are checked numerically.
2. **Jacobian eigenvalues at each balance.**
   - Stability: every Re λ < 0 at a stable balance; exactly one positive eigenvalue at the TH saddle, ≈ 0.30.
   - λ_slow and t_b for each start.
3. **Drift check.**
   - (a) Through the C propensity function, Σ_r a_r(n)·ν_r/Ω = f(n/Ω) to 1e−12 relative, at 1000 random states for Ω ∈ {10, 1000}, under MA and TH. For R1, the difference equals k11·(nC/Ω)/Ω exactly, so it vanishes as 1/Ω.
   - (b) One SSA trajectory per law at Ω = 10⁵ from x0 = (0.5, 1.0, 1.5, 1.0). |n(t)/Ω − x_ODE(t)| ≤ 0.02 at t = 0.5, 1, 2 and 5.
4. **Attraction and cycle check.**
   - 200 random starts in [0, 3]⁴ per law, integrated with LSODA (rtol 1e−10) to t = 3000.
   - Each end state must lie within 1e−6 of a stable balance.
   - Any start that does not converge is examined for a sustained cycle (§10).

### M1. Dissolution mean first-passage times

- **Series.**

  | Series | Law | Start | Targets |
  |---|---|---|---|
  | MA | MA | (1, ½, 1, ½) | D, D0 |
  | TH2 | TH | (1, 2, 1, ½) | D, D0 |
  | TH4 | TH | (1, 4, 1, ½) | D, D0 |

  D and D0 are separate sets of runs, each with its own burn-in and its own restarts. D runs first.
- **Grid:** Ω ∈ {2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128}, taken in order and extended until the budget rule of §6 stops the series.
- **Reports per size:** T̂, the chi-square and bootstrap intervals, d, the censored count, restarts, the burn-in acceptance rate, CV, CPU-s and total events.

### M2. Memorylessness

At every size of every series with at least 1000 uncensored exits:

- report CV, D_n and the bootstrap p-value (§4);
- apply the same test to M3 as a diagnostic, not as a kill condition.

### M3. Expression-switch times (TH only)

- S↑ from (Ω, 2Ω, Ω, Ω/2) to nV ≥ 4Ω; S↓ from (Ω, 4Ω, Ω, Ω/2) to nV ≤ 2Ω.
- Grid: Ω = 4·2^j, j = 0, 1, …, 10 (4 to 4096), up to the M3 budget of §6.
- 1000 runs per direction per size, or 300 when the budget binds.
- No burn-in. Cap = 100 × max(T_proj, T̂_run).
- Report the mean, its standard error, CV and the censored count.
- As a diagnostic, F1 is fitted to each direction.
- Also record the fraction of runs that pass through D before the switch.

### M4. WKB actions (gMAM)

- **Hamiltonian:** H(x, θ) = Σ_r r_r(x)(e^⟨θ, ν_r⟩ − 1), with x the densities, the deterministic rates of each law, and ν_r from §1.
- **Local geometric action** (Heymann and Vanden-Eijnden, 2008): ℓ(x, y) = sup{⟨θ, y⟩ : H(x, θ) ≤ 0}.
  - It is computed by damped Newton iteration on the system ∇_θH(x, θ) = λ·y, H(x, θ) = 0, with λ > 0, warm-started.
  - ℓ = 0 when y is a non-negative multiple of the drift.
- **Discretisation.**
  - A path φ_0 … φ_N gives the action S_N = Σ_i ℓ((φ_i + φ_(i+1))/2, φ_(i+1) − φ_i).
  - Gradients use ∂ℓ/∂y = θ̂ and ∂ℓ/∂x = −λ̂·∂_xH(x, θ̂).
- **Minimisation.** L-BFGS-B over the free coordinates, alternated with reparametrisation to equal Euclidean arclength. A level stops when a cycle changes S_N by less than 1e−9 relative, or after 400 cycles.
  - This outer optimiser is an implementation choice in place of HVE's preconditioned descent. The functional and the inner problem are theirs.
  - Densities are bounded below by 1e−12, except the fixed coordinates of the end point.
- **Resolution.** N = 50, 100, 200, …, 3200. The item is converged at the first N for which |S_N − S_(N/2)|/S_N < 1%, and S_N is reported. Non-convergence by N = 3200, or an inner-solver failure that cannot be resolved, is reported as **gMAM failed** for that item. The run then stops on that item; the model is not changed.
- **Items.**

  | Item | From | To | Free end coordinates |
  |---|---|---|---|
  | W_D | each stable balance | {c = l = 0} | v, p |
  | W_D0 | each stable balance | {c = 0} | v, l, p |
  | W_S↑ | (1, 2, 1, ½) | saddle (1, 3, 1, ½) | none |
  | W_S↓ | (1, 4, 1, ½) | saddle (1, 3, 1, ½) | none |
- **Initial paths.**
  - The straight line from the start to (target-projected start) or to the saddle.
  - For TH dissolution items, also a path through the saddle and the other stable balance.
  - The reported W is the smaller converged value, and both are recorded.
- **Effective dissolution action (diagnostic).** W_D,eff = min_b [U(b) + W_D(b)], where U(b) is the quasi-potential of balance b relative to the deeper balance: U = max(0, W_S↑ − W_S↓) for v = 4, and correspondingly for v = 2.

### M5. Independent switching cost

- **Sizes.** The three largest M3 sizes with at least 300 runs in both directions.
- **Runs.** One long run per size from the v = 2 balance, with burn-in t_b(v = 2), then total time 400 × max(T̂_S↑, T̂_S↓) at that size. If the projected cost of the three runs, from the M3 cost per unit time, exceeds the M5 budget, every run length is scaled down by the same factor to fit, and the reduction is reported.
- **Histogram.** Time-weighted pmf π of nV.
- **Estimates.**
  - ΔW↑(Ω) = −(1/Ω)·ln[π(nV = 3Ω)/π(nV = 2Ω)]
  - ΔW↓(Ω) = −(1/Ω)·ln[π(nV = 3Ω)/π(nV = 4Ω)]
- **Errors.** From batch means over 20 equal time blocks.
- **Extrapolation.** A weighted linear fit of ΔW against 1/Ω over the three sizes; the intercept is reported as ΔW(∞).
- **Comparison.** ΔW(∞) is compared with the gMAM W_S↑ and W_S↓; agreement within 25% is a consistency check, not a kill condition.
- **Caveat, disclosed.** ΔW measures min U on the hyperplane nV = 3Ω. This equals the saddle value only if the saddle is the minimum of U on that hyperplane.

### M6. Exact check of the simulator

- **Cases.** Ω ∈ {2, 3, 4} × {MA from (1, ½, 1, ½), TH from (1, 2, 1, ½), TH from (1, 4, 1, ½)}: nine cases.
- **Exact solve.** The mean first-passage time from the rounded start state to D, by a linear solve on the generator restricted to the states outside D, on a truncated lattice.
- **Truncation.**
  - Initial caps K_s = max(6, 2·⌈n_s*⌉ + 6) per species, where n* is the rounded start.
  - Transitions that would exceed a cap are suppressed.
  - All caps are doubled together until the start-state MFPT changes by less than 0.1%, with at most 4×10⁶ states. Otherwise the case is reported unconverged.
  - The linear solve must reach a relative residual ≤ 1e−10.
- **Simulator comparison.** 2000 runs from the same start, no burn-in, no effective cap. Agreement means |T_sim − T_exact| ≤ 3 standard errors of the sample mean.
- **Disclosed false-alarm rate.** About 2.4% across the nine cases.

## 6. Budgets and grid extension

**CPU time.** The sum over worker processes of process CPU time spent inside the simulator, including pilots and failed burn-in attempts. The total cap is 8 CPU-hours, allocated as follows:

| Item | Cap (CPU-h) |
|---|---|
| M1 series MA | 2.0 |
| M1 series TH2 | 2.0 |
| M1 series TH4 | 2.0 |
| R1 (MA dissolution D, combinatorial form) | 0.75 |
| M3 (both directions together) | 0.5 |
| M5 | 0.25 |
| Everything else (M0, M2 bootstraps, M4, M6, PF1–PF4, F1 bootstraps) | 0.5 |

Within each M1 series, D may use at most 1.75 CPU-h. D0 uses the remainder of the series budget, at most 0.5 CPU-h. Unused budget is not reallocated.

**Extension rule (per series and per target, sizes in grid order).**

1. **Projection.** From the third size on, project the cost per exit by log-linear extrapolation in Ω of the measured CPU-s per exit at the previous two run sizes. The projection is never less than the last cost × Ω_next/Ω_last. If spent + 300 × projection exceeds the series or target budget, the series stops before the pilot.
2. **Pilot.** Run the pilot of §3 and apply its feasibility rule.
3. **Production count.** Let c be the pilot's CPU-s per exit, and let n be the largest of 1000 or 300 with spent + n·c ≤ budget. The size runs n exits in total, pilot included. If neither fits, the series stops; the pilot is reported but not fitted.
4. **Reduced sizes.** At most two sizes may run at 300. After the second, the series stops.
5. **K1 sufficiency.** A series is sufficient for K1 if its fitted sizes (those with ≥ 300 exits) number at least 6 and span a factor of at least 4 in Ω. Otherwise K1 is underdetermined for that series.

M3 applies the same rule, with both directions at each size counted together.

## 7. Fits (preregistered)

**F1.** For each dissolution series, fit two models of ln T̂ against Ω over the fitted sizes:

- **E:** ln T = a + W·Ω + β·ln Ω.
- **P:** ln T = a + β·ln Ω.

Use weighted least squares, with σ_i = [ln U_i − ln L_i]/(2 × 1.959964) from the chi-square interval, and w_i = 1/σ_i².

- AIC = χ²_min + 2k (k = 3 for E, 2 for P), and ΔAIC = AIC_P − AIC_E.
- W's 95% interval comes from a bootstrap over runs: runs are resampled within each size, T̂ and σ are recomputed, E is refitted, and the 2.5–97.5 percentile is taken over B = 2000.
- Also reported: β, the residuals of E, and the local slopes s_k = (ln T̂_(k+1) − ln T̂_k)/(Ω_(k+1) − Ω_k).
- F1 is applied to D (K1), D0 (reported), R1, the M3 directions (diagnostic), PF1 and PF2.

**F2.** Compare each fitted D-series W with the gMAM W_D from that series' start balance.

- |W_fit − W_gMAM|/W_gMAM ≤ 0.25 means the harness is consistent.
- W_D,eff is also reported as a diagnostic.
- On a disagreement, the gap is reported and neither value is adjusted.
- The sizes may be called **pre-asymptotic** only if both of these hold:
  1. the β-corrected local slopes s_k − β·ln(Ω_(k+1)/Ω_k)/(Ω_(k+1) − Ω_k) have a Spearman correlation with Ω whose sign points toward W_gMAM, with p < 0.05;
  2. the last corrected local slope is closer to W_gMAM than the fitted W is.

**R1 criterion.** The leading exponent is unchanged if the R1 fitted W and the MA fitted W have overlapping 95% bootstrap intervals. The prefactor change is reported as the ratio T̂_R1/T̂_MA at each common size.

## 8. Kill conditions (none changes after the freeze)

**K1 (the map's kill for the ensemble-scaling claim).** K1 is evaluated separately on the D series MA, TH2 and TH4. For a series sufficient under §6, K1 triggers if any of these holds:

- W < 0;
- W's 95% bootstrap interval includes 0;
- ΔAIC < 10.

Overall status:

- **Killed** if K1 triggers on any sufficient series. The ensemble-scaling half of "Lifetimes: memoryless, ensemble-scaled…" is then refuted for this grammar at these rates.
- **Underdetermined** if no sufficient series triggers but at least one series is insufficient. The verdict is then reported per law.
- **Survived** otherwise.
- **Underdetermined (harness)** if the PF1 W recovery or PF2 fails (§9), whatever the series show.

**K2 (the memoryless half).** For each D series, take the largest size with at least 1000 uncensored exits. K2 triggers if M2 rejects the exponential law there at p < 0.01.

- **Killed** if it triggers for any series. The memoryless exit is then refuted for this grammar at these rates.
- **Underdetermined** if some series has no such size and none triggers, or if PF4 fails.
- **Survived** otherwise.
- D0 is reported but is not part of K2. No multiple-testing correction is applied.

**K3 (the two-cost analogue, TH only).** Using gMAM values, K3 triggers if max(W_S↑, W_S↓) ≥ min(W_D(v = 2), W_D(v = 4)). This is the strictest reading. If it triggers, this grammar does not put an expression change at a lower cost than dissolution, and the two-cost shape gets no support from it.

If gMAM fails for an item, a fallback is used, and the report says which:

| Item | Fallback |
|---|---|
| W_D | the smaller fitted W of the TH2 and TH4 D series |
| W_S | (1) the F1 W of the M3 direction, only if that direction passes all three K1 criteria (an exponential regime is reached); otherwise (2) the M5 ΔW(∞); otherwise K3 is underdetermined |

## 9. Planted failures (the harness must catch all four)

**PF1. Immigration–death.**
- Model: ∅ → X with propensity Ω, X → ∅ with propensity nX; target nX = 0.
- Start at nX = Ω with burn-in t_b = 10 (λ = −1), using the same restart rule. This samples the quasi-stationary state.
- Exact comparator: T_ex = 1/λ₀, the principal decay rate of the generator restricted to nX ≥ 1. It is checked against Σ_n q_n T_n, where q is the quasi-stationary distribution and T_n = Σ_(k=1..n) Σ_(j≥k) π_j/(k·π_k) are the birth–death sums with π = Poisson(Ω). The exact W is 1.
- Grid: Ω ∈ {2, 4, 6, 8, 10, 12}, with 1000 exits each.
- **Pass** requires both:
  - the F1 E-model W satisfies |W − 1| ≤ 0.05 (W recovery);
  - T_ex lies inside the 95% chi-square interval at every size (coverage).
- **Disclosed false-failure rate.** Coverage at all six sizes fails by chance with probability 1 − 0.95⁶ ≈ 26%. A coverage miss is reported as a PF1 failure in any case.
- A secondary Bonferroni reading (99.17% intervals) is also reported.
- A coverage-only failure marks the interval estimates as suspect but does not make K1 underdetermined.

**PF2. Neutral drift.**
- Model: X + Y → 2X and X + Y → 2Y, each with propensity nX·nY/Ω, and nX + nY = Ω.
- Start at nX = Ω/2, no burn-in. Target: nX ≤ Ω/4 or nX ≥ 3Ω/4.
- Grid, fixed now without computing anything: Ω ∈ {8, 12, 16, 20, 24, 32, 48, 64}, with 1000 exits each.
- The exact MFPT from the birth–death sums is reported.
- **Pass** requires that at least one K1 criterion triggers on its F1 fit. If the K1 criteria call it exponential, the harness fails.

**PF3. Censoring.**
- PF1 at Ω = 8, with cap = T_ex·ln(1/0.3), which censors about 30% of runs, and 1000 runs.
- **Pass** requires both:
  - T_ex lies inside the 95% chi-square interval of the censored MLE;
  - the naive mean, which treats caps as exits, lies below both T_ex and the MLE interval's lower bound.

**PF4. Ageing.**
- Exit times drawn as Erlang (k = 4, mean 1), n = 1000, seeded.
- **Pass** requires M2 to reject at p < 0.01.

**gMAM validations (harness tests beyond the four).**
- G1: immigration–death in density form (H = (e^θ − 1) + x(e^(−θ) − 1)), from x = 1 to x = 0. Exact W = 1.
- G2: two independent copies, from (1, 1) to {x₁ = x₂ = 0}. Exact W = 2.
- Each must agree within 1%.

## 10. Stop conditions

- **Out of scope:** the closed level, other rate constants, coupling between levels, a spatial lattice, and any attempt to connect to the winding.
- **A sustained cycle under TH.** If M0 or any trajectory shows one, it is reported, the phase-structure part stops, and it is not analysed further.
- **gMAM non-convergence.** The fallback of §8 applies, and the model is not altered.
- **Another rule needed.** If an item needs another rule, the run stops on that item and reports what it would need.

## 11. Expected outcomes (disclosed before the run)

**Theory.** Large-deviation theory (Freidlin–Wentzell; WKB for master equations; quasi-stationary exits) predicts that K1 and K2 survive for any finite network with a stable balance and a target at finite distance.

- Survival is therefore weak evidence. It shows that the grammar is in the class the theory covers.
- The informative outputs are W_D, W_D0, W_S↑ and W_S↓, and the ratio W_D/W_S.

**Claude's feasibility probe of 28 Oct.** These are quoted as expectations, not results.

- **How it was run.** A C Gillespie code in Kurtz form, with 60–200 runs per point, started from the balance with no burn-in.
- **MA, D:** T ≈ 4.6, 60, 560, 7700 at Ω = 2, 4, 6, 8, with CV 0.92–1.3.
- **MA, D0:** T ≈ 0.21, 0.99, 3.9, 12.5 at the same sizes.
- **TH, D, at Ω = 2, 4, 6, 8:** from v = 2, 2.8, 18, 122, 764; from v = 4, 4.3, 28, 140, 719.
- **TH, S↑:**
  - 2.7, 4.4, 5.5, 6.8, 8.3 at Ω = 4, 8, 12, 16, 24;
  - 14.6, 19, 27, 37, 52 at Ω = 50, 100, 200, 400, 800;
  - CV 0.65–0.8. S↓ is similar and somewhat shorter.
- **What the probe suggests.**
  - **Switching.** No exponential growth of switching time is visible up to Ω = 800, and switching is not memoryless at those sizes.
  - **Dissolution.** W_D is of order 1.
  - **K3.** It is expected to survive by a wide margin.

**Added expectations from writing this spec.**
- Burn-in infeasibility is expected at TH Ω = 2 and at the smallest D0 sizes (§3).
- Because switching is expected to be much faster than dissolution, the TH2 and TH4 dissolution series are expected to converge to the same values after burn-in. Their fitted W are expected to approach W_D,eff rather than each start's own W_D.
- A rough one-dimensional estimate puts W_S at 10⁻³ to 10⁻², so the switching exponential regime may begin only near the top of the M3 grid.
