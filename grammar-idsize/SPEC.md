# Identity with size: preregistered specification

Status: SANDBOX / DRAFT. Not promoted. This file is frozen before any code of this task is written or run, and its SHA-256 is recorded in `RESULTS.md`. After the freeze, no target, size, grid, threshold, interface rule or criterion changes. A revision is a new claim, logged as one, and every failure stays on the record.

Date: 2026-10-30. Source: PHYS2 cloud campaign, task B. This task follows the exit-time run, `grammar-exit-time/` (pull request 3, gomni1/ClaudeCloud1#3). It copies that run's simulator, fits, gMAM and master-equation code into `grammar-idsize/`, with attribution in every copied file, and does not modify `grammar-exit-time/`.

## 0. Register and walls

- **Coarse-grained register.** The ODE and the Markov chain are effective-register summaries of step processes. They are not a claim about the step processes themselves.
- **No new rule.** The model is PR 3's: the open level; TH with m = 2, kr = kc = 2 and x = C/(C+V); the Kurtz reading, in which each propensity is Ω·r(n/Ω); and the dissolution set D = {nC = nL = 0}. The only change is the seeding family below, which keeps the balances fixed.
- **Neutral labels.** Particle names appear only in the single paragraph of `RESULTS.md` headed "Observational register".
- **Well-mixed limit.** The ensemble is well mixed, so every cost grows with Ω by construction. `RESULTS.md` states this beside every verdict.
- **Out of scope.** Other rate laws, the closed level, spatial versions, and any link to the nucleon architecture's integer.

## 1. The seeding family

Keep k1 = 2, k5 = k6 = k7 = k8 = k9 = 1 and k12 = ½, and set

- k3 = 47·k10, k11 = 13·k10, k2 = 11·k10 − 2;
- k10 ∈ {½, 1, 2}. k10 = 1 is Astra's example.

Then A = 11·k10, and S(y) − A = k10·(y−2)(y−3)(y−4)/(1+y)². So the balances stay at V = 2, 3, 4, with C = 1, L = 1, P = ½, for every k10.

Rescaling k12 alone is not a real variation, because under the Kurtz form it is equivalent to rescaling Ω.

**Disclosed values (from the brief), to be recomputed in M0:** the largest real parts of the Jacobian eigenvalues at V = 2, 3, 4.

| k10 | V = 2 | V = 3 | V = 4 |
|---|---|---|---|
| ½ | −0.160 | +0.172 | −0.084 |
| 1 | −0.151 | +0.295 | −0.130 |
| 2 | −0.129 | +0.531 | −0.092 |

**M0 (deterministic).** Check the balance identity in exact arithmetic (sympy) and the balances numerically, recompute the eigenvalues above, and compute λ_slow and the burn-in t_b = 10/|λ_slow| at V = 2 for each k10.

## 2. Part 1: the race test, for each k10

**gMAM.** PR 3's code and convergence rule (N doubled from 50 until a change below 1%), with the k10 rates. Compute:

- W_D from each stable balance to {c = l = 0};
- W_S↑ from (1, 2, 1, ½) to the saddle (1, 3, 1, ½);
- W_S↓ from (1, 4, 1, ½) to the saddle.

Initial paths are as in PR 3 (straight, and through the other balance for W_D), and the smaller converged value is used.

**Switching runs.**

- Sizes: Ω ∈ {2, 3, 4, 5, 6, 8, 10, 12, 16}.
- **Upward:** start from the rounded V = 2 balance (Ω, 2Ω, Ω, ⌊Ω/2 + ½⌋), with no burn-in, and run until nV ≥ 4Ω.
- **Downward:** start from the rounded V = 4 balance (Ω, 4Ω, Ω, ⌊Ω/2 + ½⌋) and run until nV ≤ 2Ω.
- A run "passes through D" if it visits D before reaching the switching target. D is not absorbing, and the run continues to the target.
- Each size and direction runs until 50 passages are recorded, or 10⁶ runs.
- The runs use PR 3's C simulator. Its `secD` flag records the passage, and a cap of 10⁴ × the running mean switching time is applied; capped runs are reported.

**φ_obs.** The fraction of runs that pass through D. Its 95% interval is Clopper–Pearson, and its SE is √(φ(1−φ)/n).

**T_D⁰.** The mean first-passage time to D from the same rounded start, with no burn-in, measured in separate runs with PR 3's simulator.

- Runs continue until the relative SE (s/√n over T̄) is ≤ 5% with at least 400 runs, or until 900 CPU-s per size and direction. The SE reached is reported.
- At Ω ∈ {2, 3, 4} the exact value is also computed with PR 3's master-equation solver and its per-species truncation refinement (`m6_supp`, up to 4×10⁶ states), and compared with the simulated T_D⁰ (z score).

**φ_pred.** Exactly as the brief defines it: φ_pred = 1 − E[exp(−τ_S/T_D⁰)], where τ_S is the switching time of the runs that did *not* pass through D, and the mean is over those runs. Its SE comes from a bootstrap: resample the τ_S sample and draw T_D⁰ from a normal distribution with its SE, B = 2000.

*Disclosed property, before the run.* If the dissolution and switching clocks were independent exponentials with means b and a, the exact passage fraction would be φ = a/(a+b). The estimator above averages over runs conditioned on no passage, so its expectation is φ/(1+φ), a relative bias of −φ/(1+φ). That is below 10% wherever φ ≤ 0.11, far inside R1's band.

A second estimator is reported alongside but not used in R1: φ_pred* = 1 − 1/E_cond[exp(+τ_S/T_D⁰)]. It inverse-weights the same runs and equals φ exactly for independent clocks.

**R1 (race).**

- At every size where φ_obs ≥ 10⁻³ and both φ_obs and φ_pred have relative SE ≤ 20%, the ratio φ_obs/φ_pred lies in [½, 2].
- Evaluated per k10 and per direction.
- **Kill:** the ratio falls outside [½, 2] at two or more sizes (counted over both directions) for any k10.

**R2 (the crossover follows the dissolution cost).**

- For each k10 and each direction, fit ln φ_obs against Ω with PR 3's F1. That is weighted least squares with σ = (ln U − ln L)/(2 × 1.959964) from the Clopper–Pearson interval, comparing model E (a + W·Ω + β·ln Ω) with model P (a + β·ln Ω).
- The fit uses the sizes with at least 10 passages, and a direction is evaluated only if it has at least 4 such sizes.
- A direction passes if both hold:
  - the model-E slope W equals −W_D within 25%, using the gMAM W_D from that direction's start balance;
  - ΔAIC = AIC_P − AIC_E ≥ 10.
- A k10 passes R2 if every evaluated direction passes.
- **Kill:** two or more k10 values fail.

**Disclosed expectation.** The race picture predicts both R1 and R2. The informative outputs are how φ, W_D and W_S move together across the family, and whether the crossover size (the Ω where φ_obs falls below 0.01) scales as 1/W_D.

## 3. Part 2: is the threshold-law gap a small-size effect?

**Method.** Forward flux sampling (FFS) of dissolution to D under TH with k10 = 1, from the V = 2 balance.

- **Order parameter.** M = nC + nL, which changes by at most 1 per reaction, and λ = −M/Ω.
- **Basin A** = {M ≥ 2Ω}. The balance has M = 2Ω.
- **Interfaces:**
  - M₀ = 2Ω − ⌈2√Ω⌉ (two typical fluctuations below the balance);
  - then M_i = M₀ − i·Δ, with Δ = max(1, ⌈M₀/12⌉), until an interface would be ≤ 0;
  - the final interface is M = 0, which is D itself.
- **Flux stage.**
  - Start from the rounded V = 2 balance and run PR 3's burn-in t_b = 66.05 (restarting from the balance if D is hit).
  - Then run one trajectory, recording each first crossing of M₀ downward after a visit to A, together with its configuration.
  - Stop at 1000 crossings. Φ₀ = crossings / time.
  - If D is reached during the flux stage, the trajectory restarts with a fresh burn-in, and the time after its last visit to A is excluded.
- **Interface stages.**
  - From each interface, launch trials from configurations drawn uniformly from those stored there, until M ≤ M_(i+1) (success, which stores the configuration) or M ≥ 2Ω (failure).
  - 1000 trials per stage, extended by blocks of 1000 up to 2×10⁴ until at least 50 successes.
  - A stage with no success after 2×10⁴ trials ends the replicate as a failure, and this is reported.
- **Rate.** k = Φ₀·Π P_i, and T_FFS = 1/k.
- **Replicates.** 8 independent replicates per size. The estimate is the mean of the 8 values of ln T, and the SE is the standard deviation of the 8 divided by √8.
- **Reactive paths.** These are kept as summaries: each successful segment records its parent, the maximum nV/Ω along it, and the sum and count of the distances, every 10 events, from (nC, nV, nL, nP)/Ω to PR 3's gMAM optimal path (`TH_W_D_v2`, end point (0, 3.43, 0, 0.198)). Complete reactive paths are rebuilt from the parent links.
- **Sizes.** Ω ∈ {8, 10, 12, 14, 16, 20, 24, 30}, in order, as far as the Part 2 budget allows.

**Harness.** It must pass before any Part 2 result counts:

- **H-a.** FFS T_D matches PR 3's brute-force post-burn-in T̂ within 2 combined SE.
  - TH (v = 2): Ω = 8, 10, 12, against 855.4, 5048 and 3.27×10⁴.
  - MA: Ω = 6, 8, 10, against 591.2, 7756 and 1.076×10⁵, with the MA burn-in t_b = 53.1 and the MA basin M ≥ 2Ω.
  - The combined SE is √(SE_FFS² + SE_PR3²), with SE_PR3 = T̂·σ_ln from PR 3's chi-square interval.
- **H-b.** FFS on PF1 (immigration–death, exact W = 1) matches the exact mean first-passage time 1/λ₀ within 10% at Ω = 20 and Ω = 30.
  - Order parameter: nX. Basin: nX ≥ Ω. M₀ = Ω − ⌈2√Ω⌉. Same interface rule and replicates.
  - PF1's flux stage uses PR 3's PF1 burn-in t_b = 10.

If any harness check fails, Part 2 is reported as underdetermined, and FFS is not tuned until it agrees.

**G1.** Over Ω ∈ [20, 30], fit model E to the FFS ln T_D at the sizes reached in that range. Report the local slope s₂₅ = W + β/25, which is d ln T_D/dΩ of the fit at the midpoint Ω = 25. W and β are nearly collinear over so narrow a range, but their combination s₂₅ is well determined. With only two sizes in the range, the secant slope is used instead. The SE comes from a bootstrap over replicates (B = 2000).

- **Supports the small-size reading:** s₂₅ within 10% of 0.820, that is, in [0.738, 0.902].
- **Kill (of the small-size reading):** s₂₅ ≥ 0.95.
- **Underdetermined:** a value strictly between 0.902 and 0.95, or Ω = 20 not reached.

**G2 (report only).** At three sizes (the smallest, middle and largest reached among {8, 16, 30}, or the nearest reached), report:

- the mean over complete reactive paths of the maximum nV/Ω;
- the mean distance from gMAM's optimal path.

**Disclosed reading (Claude's, unchecked).** At small Ω, a route through a large Void reserve may dominate, with a higher cost but a larger prefactor. The slope would then fall toward 0.820 as Ω grows.

## 4. Planted failures (the harness must catch them)

- **PF1, via FFS.** As in H-b.
- **PF5. Two independent exponential clocks.**
  - Clocks of means a (switching) and b (dissolution), with (a, b) ∈ {(1, 10), (1, 100), (1, 1000)}, and 10⁵ samples per pair (seeded).
  - **Pass** requires both, for every pair:
    - φ_pred (the brief's estimator) matches its exact expectation φ/(1+φ) within 2 SE;
    - φ_pred* matches the exact passage fraction φ = a/(a+b) within 2 SE.
  - The bias of φ_pred against φ is reported.
- **PF6. Two routes with different cost and prefactor.**
  - An exit process with two independent Poisson routes, r₁(Ω) = A₁·e^(−W₁Ω) and r₂(Ω) = A₂·e^(−W₂Ω), with W₁ = 1.0, W₂ = 0.82 and A₁/A₂ = e^3.6, A₂ = 1. Exit times are exponential with mean 1/(r₁ + r₂).
  - The crossover size is Ω* = ln(A₁/A₂)/(W₁ − W₂) = 20. There the exact local slope equals (W₁ + W₂)/2 = 0.91.
  - Draw 1000 exit times at each Ω ∈ {8, 10, 12, 14, 16, 20, 24, 30}, with T̂ = mean. Compute local slopes by model-E fits on sliding windows of three consecutive sizes, each evaluated at its middle size.
  - **Pass** requires all three:
    - the windowed slope falls through 0.91 between the windows centred at 16 and 24, which bracket Ω* = 20;
    - the slope for the window centred at 12 is ≥ 0.95;
    - the slope for the window centred at 24 is ≤ 0.90.

**Consequences of a planted failure.**

- A PF5 failure makes R1 underdetermined.
- A PF6 failure makes G1 underdetermined.
- A PF1 (H-b) failure makes Part 2 underdetermined.

## 5. Budget

**Caps (CPU-hours):**

| Item | Cap |
|---|---|
| Task total | 8 |
| Switching runs | 1.5 |
| T_D⁰ runs | 1.5 |
| gMAM | 0.5 |
| Exact master-equation solves | 0.5 |
| FFS harness | 1.0 |
| FFS sizes | 2.5 |
| Planted failures | 0.5 |

A budget stop is recorded with the sizes reached.

## 6. Statuses

- **R1, R2, G1:** survived, killed or underdetermined, with the evidence.
- **G2:** reported only.
- **Every verdict:** the well-mixed limit is stated beside it.
