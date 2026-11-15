# NIGHT-REPORT-2026-11-14

PHYS2 Night Run, sixth night. Claude, unattended, 14 Nov 2026, from about 06:16 London time. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

The pinned slit test ran as written and the angular-sum handoff, read as the squared resultant, was not killed: it interferes with two slits open (κ2 = 1.24) and leaves nothing over with three (κ3 at rounding level, 10⁻¹⁶), while both planted readouts show a clear third-order term (0.58 and 0.38). That pass is weaker than it looks, and the night's second item says exactly how: once contributions add as arrows and the click depends only on their sum, 'nothing left over with three slits' forces the squared readout and nothing else, so the three-slit half of the kill line can never fire on this candidate. The whole physical content sits in two unearned inputs: that contributions add, and that the readout sees only the sum.

The noise part found something more useful for direction. Jitter that is independent between routes does not remove cancellation in any single run; it only scrambles where the bright and dark grains fall, and interference disappears only when many runs are averaged. And it disappears only because the jitter was made independent between routes that share five-sixths of their length; with jitter common to all routes the fringes do not move at all. So what destroys interference in this picture is difference between routes, not turnover as such. The third item located where a level-wide object survives when units read only neighbours: not in the order of steps, which becomes a partial order, but in the comparability of rates between distant units.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-14.md (Drive ID 10jVPTcxdbAdBgF81vhklKsyx_r8eBOCs, created 06:20:17 UTC by Drive's clock) and not altered afterwards. It was uploaded from the local file by reference, so the Drive copy is byte-identical; SHA-256 61f2ae8e28f7d8d647a0e62dd724efc344a2b897889322c0535a84a9e98a3581. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-14
> 
> PHYS2 Night Run, sixth night. Claude, unattended. Frozen 14 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
> 
> ## How the queue was built
> 
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (see next line); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794620197-4c40, 180 nodes); NIGHT-REPORT-2026-11-13.md in full, with its follow-ups; MAP-SNAPSHOT-2026-11-13.md. The project instructions were in context. No REVIEW notes exist in Night-Reports. The narrative spine (context only) was not opened.
> - **STEERING id was stale. Reading taken.** The id given in the task prompt (1YQpKFp-…) now opens SUPERSEDED-2026-11-14-STEERING.md. As instructed, I listed the folder and took the one file titled exactly STEERING.md: ID 1xvCEBQ9vpbyw7aVOIpNI81ESGMzMJsrW, modified 14 Nov 01:36 UTC. Its PIN is the slit test. The superseded file's PIN (the five closed levels) is listed in the new file's NOTES as done.
> - **PIN:** 'Slit test of the angular-sum handoff', D2. It is item 1 and is run exactly as written. The PIN leaves four things for the run to fix before running (distances, slit spacing, ω; how fringes are counted and their spacing measured; the noise grid; how 'averaged over noise draws' is read). They are fixed below.
> - **Stop rule applied.** No single-level stability work. That still excludes 'How sharp is the step-counted clock against size?' from the 13 Nov follow-ups.
> - **Coupling not run.** Still Glenn's call; STEERING shows no call.
> - **Priority 2 (13 Nov follow-ups):** 'Neighbour-reading rules (D1)' is item 3. 'The total-probability statement on the telegraph model' is dropped: the map (O_signed, 14 Nov) archives that line as superseded by the slit test. 'Byrne's trap field' was taken up in session on 13 Nov (map note on E_ntau: the 2014 review read, the 1996 paper still unread); it is not queued, because the remaining step is reading one paywalled paper and I rate its yield tonight as low. 'How a turn is read from inside (D2)' is carried over, not queued: three items fill the night.
> - **Priority 3 (map regions changed since the 13 Nov snapshot):** O_signed reworded with a new kill line (the PIN's target); O_own and O_drift archived into O_ratelaw. The merges are Glenn's rulings of 14 Nov and need no work.
> - **Priority 4 and 6 (unproved if-then; untagged necessity):** O_signed's statement says 'read as the squared resultant give I₂ ≠ 0 and I₃ = 0 together, since only pairs cross; any other readout generally gives I₃ ≠ 0'. 'Generally' is not a theorem, and the PIN's own scope line says a pass 'does not derive the squared readout'. Item 2 asks exactly how much of the squared readout the no-third-order condition forces.
> - **Ranking:** item 1 (pinned); item 2 (easy, high: an if-then that would turn the slit conditions from a consistency check into a constraint on the readout); item 3 (easy, moderate).
> - **Method lines applied:** 'say which necessary' (tags below); observational comparisons labelled; no coordinator above a level (bears on item 1's noise reading and item 3).
> 
> ---
> 
> **N-2026-11-14-1 — Slit test of the angular-sum handoff (the PIN)**
> 
> - **Target:** O_signed, 'What in the handoff can cancel?', and its kill line.
> - **Picture, in one sentence:** every straight route from source to screen carries an orientation that turns by a fixed angle per step; at each screen grain the arriving orientations add as axes, and we ask whether what adds up behaves as observed with two and three slits open.
> - **Task:** given the rule in STEERING's PIN, compute the stated measures for the stated readouts and controls; apply the harness checks and then the kill line; then the noise part.
> - **Inputs:** STEERING.md PIN text (1)–(9), which governs. Nothing in it is changed here.
> - **Depth:** D2 Shape.
> - **Effort cap:** about 45% of the night.
> - **Done means:** the table of κ2 and κ3 for R2, R4, RS, C+ and C-arrow; harness verdict; kill-line verdict for R2; fringe counts, spacings and their ratio; the noise table under both readings below; the scope sentence the PIN requires.
> - **Mechanism, fixed now.**
>   - *Geometry (the PIN leaves this to the run).* Lengths in grain units; one step is one grain unit of route length. Source at lateral position 0, a distance D1 = 10 000 in front of the barrier. Slit centres at lateral positions y = −100 (A), 0 (B), +100 (C); each slit is the 5 grains at centre −2 … +2. Screen a distance D2 = 2 000 behind the barrier; 1001 grains at x = −500 … +500. ω = π/5 radians per step. A history is (slit grain y, screen grain x); L = √(D1² + y²) + √(D2² + (x − y)²), kept as a float, never rounded. w = 1. 15 histories reach each screen grain with all slits open.
>   - *Why these numbers, by arithmetic and not by trial.* For the axis (R2) the resultant's phase is 2ωL, so the effective wavelength is π/ω = 5; for the arrow it is 2π/ω = 10. Two slits a distance d apart give fringes about (wavelength)·D2/d apart near the screen centre: for adjacent slits (d = 100), 100 grains for R2 and 200 for the arrow; for the outer pair (d = 200), 50 and 100. The screen is 1000 wide, so R2 should show ten or more fringes with three slits open. The single-slit envelope's first zero for R2 is at about 5·2000/5 = 2000, outside the screen, so fringes are not washed out by slit width. Off axis the spacing grows by the factor (1 + x²/D2²)^1.5, at most 1.10 at the screen edge.
>   - *Fringe count (PIN (1)).* The number of strict interior local maxima of P_ABC(x) under R2 whose height is at least 10% of the screen maximum. Requirement: at least 5. If fewer, the geometry was badly chosen; the item is then reported as ill-posed and nothing is re-chosen.
>   - *Readouts and controls.* Exactly as PIN (3). For RS, s = the median over the 1001 screen grains of |R(x)|² with all three slits open, computed once from the noise-free axis sum and then held fixed for all configurations.
>   - *Measures.* Exactly as PIN (4). P0 = 0; no background is declared.
>   - *Harness checks (PIN (5)).* C+: max over x of |I2| and |I3| ≤ 10⁻⁹ × max P_ABC. R4 and RS: κ3 > 10⁻³.
>   - *Why C+ must give zero.* P is a count of open histories; counts add over disjoint slit sets, so every I2 and I3 is an exact integer zero.
>   - *Why the two plants must trip (closed form).* Write s_i = |R_i|² for slit i's own resultant and p_ij = 2 R_i·R_j. For R4, P = (Σs + Σp)², and the terms that survive in I3 are exactly those that touch all three slits: I3 = 2(s₁p₂₃ + s₂p₁₃ + s₃p₁₂ + p₁₂p₁₃ + p₁₂p₂₃ + p₁₃p₂₃). Each slit's five histories are nearly aligned on this screen (phase spread across a slit at most (2π/5)·4·sin 14° ≈ 1.2 rad), so s_i ≈ s₀ between about 21 and 25 and p_ij ≈ 2s₀ cos φ_ij, giving I3 ≈ 4s₀²[(c₁₂ + c₁₃ + c₂₃) + 2(c₁₂c₁₃ + c₁₂c₂₃ + c₁₃c₂₃)] with c = cos φ. Where the three are in phase this is 36 r⁴ against I2 = 14 r⁴ per pair (r⁴ = s₀²): ratio 36/42. The bracket is not identically zero and the screen sweeps the phases through ten or more fringes, so Σ|I3| is of the order of Σ|I2|: κ3 of order 0.1 to 1, at least two orders above the 10⁻³ line. For RS, P = 1 − exp(−S/s) is strictly concave in S = |R|². Where three equal resultants are in phase with u = s₀/s, I3 = 1 − e^(−9u) + 3e^(−4u) − 3e^(−u) and I2 = 2e^(−u) − e^(−4u) − 1; at u = 0.3 these are −0.385 and +0.181, so again κ3 is of order 1. (The map note of 14 Nov records about 0.5 and 0.4 in one trial geometry; that trial was not mine and its geometry is not used.) If either plant gives κ3 ≤ 10⁻³ the harness is blind: report a harness failure and stop the item.
>   - *Kill line (PIN (6)).* For R2: κ2 < 0.05 or κ3 > 10⁻⁶. Expectation stated now: κ3 at float level (10⁻¹² or below), because |R|² has only pair terms; κ2 of order 1.
>   - *Fringe spacing (PIN (7)).* For the adjacent pair AB open: the mean distance between consecutive strict interior local maxima of P_AB(x) that reach at least 10% of that curve's maximum, over the whole screen; for R2 and for C-arrow; and the ratio arrow/R2. Predicted now: about 100–105 and 200–210; ratio 2.0 within 5%. The same measure for ABC is reported beside it. No kill is attached; the PIN asks for a report.
>   - *Noise part (PIN (8)); run only if the harness checks pass.* Each history h gets orientation θ_h = ωL_h + σ·√L_h·ξ_h with ξ_h standard normal, independent between histories; this is the sum of L_h independent per-step jitters of standard deviation σ. Within one noise draw a history keeps its jitter in all 8 configurations (PIN (1): a history is the same history whichever slits are open). Readout R2 only, plus C+ as a null. Seed 20261114. Draws: 2000; the first 200 are also reported on their own, since the PIN's floor is 200.
>   - *σ grid, fixed now.* 0, 0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.0, π/2. It runs from 0 to π/2 as the PIN says. It is dense at the small end because L ≈ 12 000 steps: the doubled-angle jitter 2σ√L reaches 1 radian at σ ≈ 0.0046, so on an even grid every point but the first would be fully scrambled.
>   - *Two readings of 'averaged over noise draws'. Both are reported; neither is chosen after the fact.* Reading A: average P(x) over draws for each configuration, then form I2, I3, κ2, κ3 from the averaged P (what a screen that accumulates many arrivals would show). Reading B: form κ2 and κ3 within each draw, then average them (the literal wording).
>   - *Predictions, stated now.* κ3 stays at float level under both readings, for every σ (algebra, draw by draw; A is linear in P). Under A, the pair term is multiplied by about exp(−4σ²L) (two independent histories, each contributing exp(−2σ²L)), so κ2 falls to its sampling floor, which shrinks as 1/√(draws), by σ ≈ 0.01. Under B, κ2 does not fall to 0: with 5 histories per slit, a single draw's pair term is a sum of 25 random cosines and stays of order 1; I expect a plateau of order 1 from σ ≈ 0.01 upward. If B goes to 0 or A does not, I have misread the rule and will say so.
>   - *Numerics.* Everything is direct sums; no solver. Per-draw summaries only are kept for the noise part (κ2, κ3 per draw; running sums of P). Pilot: 20 draws at one σ, timed, before the main loop.
>   - *By construction, said now (PIN (9), P2.6-03 §3):* R2's I3 = 0 is algebra. A pass shows that the candidate shape is consistent with both slit anchors and that the harness tells readouts apart. It does not derive the squared readout.
> 
> **N-2026-11-14-2 — How much of the squared readout does 'no third-order term' force?**
> 
> - **Target:** O_signed, the sentence 'any other readout generally gives I₃ ≠ 0'; the PIN's scope line (9).
> - **Picture, in one sentence:** if what arrives at a grain is one summed arrow, and the chance of a click depends only on that sum, which ways of reading the sum leave nothing over once all the pairs are accounted for?
> - **Task:** given (A1) the contributions reaching a screen grain add as vectors in the plane, R = Σ over open slits of R_i; (A2) P is a function of R alone, the same function whichever slits are open, continuous, non-negative, with P(0) = 0; prove whether I3 = 0 for all R₁, R₂, R₃ holds if and only if P is a quadratic form in R; and whether adding (A3) no preferred direction (P unchanged when all contributions are turned together) leaves exactly P = β|R|². State what each assumption does and which are earned in the grain picture. Search for a published result first.
> - **Inputs:** the definitions of I2 and I3 in the PIN; standard results on Fréchet's functional equation.
> - **Depth:** D3 Probe (one if-then proof, one small check).
> - **Effort cap:** about 25%.
> - **Done means:** the if-then proved or a counterexample; the list of assumptions with tags; one sentence for the map.
> - **Mechanism, fixed now.**
>   - *Proof route.* I3 = 0 for all triples, with P(0) = 0, is Fréchet's equation Δ_aΔ_bΔ_c P = 0. For continuous P its solutions are polynomials of degree at most 2: P = ℓ(R) + Q(R), ℓ linear, Q a quadratic form. Non-negativity near R = 0 forces ℓ = 0 (since ℓ(−R) = −ℓ(R) and Q is second order). Rotation invariance of a quadratic form forces Q = β|R|². Converse by expansion.
>   - *Check, numerics.* 10 000 random triples of plane vectors (components uniform in [−3, 3], seed 20261114). Readouts: |R|^p for p = 1, 1.5, 2, 2.5, 3, 4; an anisotropic quadratic form R_x² + 3R_y² + R_xR_y; |R|² + (unit vector)·R; 1 − exp(−|R|²). Report max |I3| relative to max P for each. Expected: float level for the two quadratic forms and nothing else; the form with a linear term has I3 = 0 but goes negative.
>   - *Planted failure, guaranteed.* The harness is first given P = |R|⁴ at R₁ = R₂ = R₃ = (1, 0): I3 = 81 − 3·16 + 3·1 = 36 exactly. And P = |R|² at the same point: 9 − 12 + 3 = 0. If it does not return 36 and 0 the check is void.
>   - *Kill line:* a continuous non-negative P with P(0) = 0 that is not a quadratic form and has I3 = 0 on all triples refutes the claim.
>   - *By construction, said now:* the result can only be conditional on A1 and A2. It cannot say why contributions add, or why the readout is a function of the sum alone.
> 
> **N-2026-11-14-3 — Does 'ratios only' survive when units read neighbours, and what replaces the single order of steps?**
> 
> - **Target:** P_period (13 Nov shape: inputs 'one order of all steps' and 'the well-mixed read of Contact's share'); F_time; the standing line 'no coordinator above a level'.
> - **Task:** given a rule in which each unit's next step has a weight that reads only that unit's state and the states of a bounded set of neighbours, determine whether (a) the law of what happens is unchanged when every weight is multiplied by one factor; (b) there is a description of 'what happens' that does not use one order of all steps; say exactly where, if anywhere, a level-wide object is still used.
> - **Inputs:** the 13 Nov item 1 result and its checker's objections; standard facts about jump chains and about commuting independent actions.
> - **Depth:** D1 Locate. By argument only; nothing is run. This is not single-level stability work: no rates are drawn and no balance or cycle is examined.
> - **Effort cap:** about 15%.
> - **Done means:** yes or no for (a) and (b), each with its smallest assumption, and the exact place where a level-wide object remains, if one does.
> - **Mechanism:** argument only; no harness, so no planted failure.
> 
> ---
> 
> Checks: after each item, a fresh Claude subagent that has not seen the working. Receipts uploaded with SHA-256 before the report is written.

## 3. State changes noticed

- **Map diff.** The Premise Map was read at version 1794620197-4c40 (13 Nov's snapshot was 1794517273-62fd). 180 nodes, as before; none added or removed.
  - O_signed retitled 'What in the handoff can cancel?' (14 Nov), with the two- and three-slit conditions as statement and kill line, the angular-sum picture as candidate shape, and the old Δt·Δx kill line retired on the record.
  - O_own ('Handoff in the basin', re-scoped 13 Nov) and O_drift archived into O_ratelaw, now 'What rate law holds a pattern in its basin?'. Live nodes 95 (were 97), Archive 62 (were 60). Gaps live: two fewer.
  - The 13 Nov report applied on Glenn's 'proceed': E_ntau corrected, K_tradeless and P_period updated. E_ntau also carries a session note on Byrne's field (1.2 T in the 2014 review for the re-configured trap; the 1996 paper unread).
  - Type counts unchanged: Known 54, if-then 38, Candidate 28, Retired 19, Gap 19, Adopted 12, Floor 10. The diff is from the counts and the map's own 13–14 Nov timeline, not field by field.
- **Standing constraints.** Unchanged since 10 Nov (ID 1LjICJx…, exact title).
- **Steering applied.** The id in the task prompt now opens SUPERSEDED-2026-11-14-STEERING.md. The current STEERING.md is ID 1xvCEBQ9vpbyw7aVOIpNI81ESGMzMJsrW (14 Nov 01:36 UTC), found by listing the folder and taking the exact title. Its PIN, the slit test, is item 1. The stop rule and the coupling note were obeyed. **The scheduled task's prompt should be given the new id, or told to find STEERING.md by title.**
- **Previous follow-ups.** 'Neighbour-reading rules' became item 3. The others: see the queue's opening section.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-14-1: slit test of the angular-sum handoff (the PIN, D2)

- **Depth reached:** D2.
- **Crack found:** not in the candidate (it passes). Three in the test and the rule, listed under 'Shape' below.
- **In plain words.** Fifteen straight routes reach each screen grain, five through each slit. Each carries an axis that has turned by a fixed angle per step. Adding the axes and squaring gives bright and dark bands with two slits open, and with three slits open the pattern is exactly what the pairs predict. Squaring twice, or letting the detector saturate, leaves something over that the pairs do not predict, and the test sees it.
- **Set-up, fixed in the queue.** D1 = 10 000, D2 = 2 000, slit centres −100, 0, +100, five grains each, screen −500 … +500, ω = π/5, route lengths 12 000 to 12 089 steps, unrounded. s for the saturating readout = 38.57.
- **Part one.**

| Readout | κ2 | κ3 | Reading |
|---|---|---|---|
| R2, squared axis sum (the candidate) | 1.2403 | 2.2×10⁻¹⁶ | interferes; no third-order term |
| R4, fourth power (plant) | 0.9213 | 0.5797 | third-order term seen |
| RS, saturating (plant) | 1.5309 | 0.3782 | third-order term seen |
| C+, positive weights (control) | 0 exactly | 0/0 (I3 = 0 exactly) | no interference of any order |
| C-arrow, squared arrow sum (control) | 1.3185 | 2.2×10⁻¹⁶ | interferes; no third-order term |

  - **Harness checks: passed.** C+ gives I2 = I3 = 0 exactly. Both plants are far above 10⁻³, as the closed forms in the queue said they must be. (κ3 for C+ is 0/0, since its denominator is zero; the PIN's check is on I2 and I3, which are exact zeros.)
  - **Kill line for R2: not met.** κ2 = 1.24 against the line at 0.05; κ3 = 2×10⁻¹⁶ against 10⁻⁶.
  - **Fringes.** R2 with three slits open: 19 maxima (requirement: at least 5). Spacing with A and B open: 102.67 grains for the axis, 204.0 for the arrow; ratio 1.987 (predicted 2.0 within 5%). With all three open: 51.3 and 102.25, ratio 1.992.
- **Part two, turnover noise** (R2; 2000 draws per σ, seed 20261114; the first 200 also reported). κ3 stayed at 10⁻¹³ or below at every σ under both readings.

| σ per step | κ2, reading A (average the screen, then measure) | κ2, reading A, 200 draws | κ2, reading B (measure each run, then average) |
|---|---|---|---|
| 0 | 1.240 | 1.240 | 1.240 |
| 0.001 | 1.227 | 1.227 | 1.240 |
| 0.002 | 1.188 | 1.188 | 1.235 |
| 0.003 | 1.114 | 1.115 | 1.220 |
| 0.005 | 0.834 | 0.836 | 1.136 |
| 0.007 | 0.415 | 0.416 | 1.055 |
| 0.01 | 0.052 | 0.089 | 1.028 |
| 0.015 to π/2 (nine values) | 0.025 | 0.078–0.081 | 1.026–1.028 |

  - Both predictions in the queue held. Under A, κ2 falls to a sampling floor (0.025 at 2000 draws, 0.08 at 200; ratio √10). Under B it settles near 1.03 and does not go to 0.
  - The PIN's expected shape ('κ2 falls toward 0 as σ grows; κ3 stays at float level') holds under reading A and not under reading B.
  - The screen's mean reading with three slits open falls from 71.5 to 15.0 as noise grows.
- **Shape: what the pass does and does not show** (the checker's points, all accepted, with mine).
  1. **The three-slit half of the kill line cannot fire on R2.** I3 = 0 is an identity for any readout quadratic in a sum of per-slit vectors, for any ω, geometry, weights or noise draw. The 32 000 noise-run values of κ3 are that identity re-evaluated, not further evidence. Only κ2 ≥ 0.05 could have failed, and it is a low bar. This is what the PIN's own scope line (9) says; item 2 turns it into a theorem.
  2. **The doubled-angle check is true by construction.** The ratio 2 follows from u = (cos 2θ, sin 2θ); it checks the code. What it does record usefully: for the same ω an axis gives fringes at half the arrow's spacing, so the turn per step inferred from a fringe pattern differs by a factor of two between the two readings.
  3. **Reading B's plateau is speckle, not fringes.** With full noise each run's screen is an unstructured grain-to-grain pattern; κ2 uses absolute values and cannot tell that from fringes. The accurate statement: within one run the readings still do not add (cancellation persists), but no banding survives; banding is lost in the average.
  4. **The loss of interference rests entirely on jitter being independent between routes.** Routes through one slit share the 10 000-step leg from the source, yet drew independent jitter over it. The checker ran one case outside the rule: jitter common to all 15 routes at σ = 0.05 leaves κ2 at 1.2402, unchanged. If jitter belongs to steps, only the 2 000-step legs that differ would dephase. The decay scale σ ≈ 0.005 is 1/√L and is set by the chosen distances, nothing else. The exact expectation (checker) is E|R|² = Σ(1 − d_h²) + |Σ d_h u_h|² with d_h = exp(−2σ²L_h); it matches the table to three figures. My queue's bare factor exp(−4σ²L) is right for one pair and not for κ2.
  5. **P is not a normalised probability.** Screen totals: single slits 23 280, 23 503, 23 280 (sum 70 063); all three 71 593. The total falls 4.8-fold under full noise. The checker showed this is not only the finite screen: on a screen 40 times wider the mean with three slits open is 4.55, below the incoherent 15. The cause is w = 1 with no fall-off with length or angle. So 'P per unit emitted' is not conserved in this rule.
  6. **Unearned inputs doing the work** (checker's list, accepted): vectors add and the readout is quadratic (the Born shape, put in by hand); straight routes with one kink only; w = 1; route length as an unrounded Euclidean float, which imports a continuum metric into a rule stated in steps; five mutually coherent grains per slit and a point source; a history keeping its jitter across all 8 configurations, which makes I3 = 0 run by run, whereas real configurations are separate runs and only reading A is observable.
- **The sentence the PIN requires.** R2 gives I3 = 0 by algebra, since only pairs cross. The pass shows the candidate shape is consistent with both slit anchors (observational register: Sorkin 1994; Sinha et al. 2010) and that the test separates readouts. It does not derive the squared readout.
- **Independent check:** numbers CONFIRMED; interpretation PARTLY. The checker is Claude (a fresh subagent that wrote its own code from the rule and did not see mine). Every figure above reproduced, the noise tables with a different seed. Its six disputes are points 1 to 6 above. A cross-model check is not needed for the numbers; point 4 deserves Astra's or Glenn's eye, because it is a modelling choice and not arithmetic.
- **Receipts:** N-2026-11-14-1-slit.py, -slit-output.json, -slit-stdout.txt; N-2026-11-14-1-checker.py, -checker-output.txt.
- **Confidence:** high for every number (two independent computations). High that the pass is by construction. Medium for point 4's reading, which rests on one out-of-rule case run by the checker.

### N-2026-11-14-2: how much of the squared readout does 'no third-order term' force? (D3)

- **Depth reached:** D3.
- **Crack found:** yes, a usable one. The map's 'any other readout generally gives I₃ ≠ 0' can be replaced by an if-and-only-if.
- **In plain words.** Suppose what reaches a grain from each slit is an arrow, the arrows add, and the chance of a click depends only on the sum. Then 'three slits show nothing beyond what pairs show' holds for every arrangement if and only if the chance is the squared length of the sum. No other way of reading the sum does it.
- **Proved.**
  - T1 [theorem]. Assume (A1) contributions add as plane vectors; (A2) P is a function of the sum alone, the same whichever slits are open, non-negative, zero at zero, and regular (continuous, or merely measurable). Then I3 = 0 for all triples if and only if P is a positive quadratic form in R. The proof is four lines: B(a,b) = P(a+b) − P(a) − P(b) satisfies I3 = B(a+b,c) − B(a,c) − B(b,c), so I3 = 0 makes B additive in each slot; P minus B(x,x)/2 is then additive; non-negativity removes the additive part. (The checker's route, shorter than the queue's; the queue's also goes through.)
  - T2 [theorem]. Add (A3) no preferred direction. Then P = β|R|². This holds equally for doubled-angle vectors.
  - T3 [theorem], local form. If I3 = 0 is known only for contributions up to size r, P is fixed on the reachable set (sums up to 3r) and nothing is said beyond. My queue did not have the radius; the checker supplied it.
- **Check.** Plant passed (36 and 0 exactly). On 10 000 random triples, max|I3|/max|P| is 3×10⁻¹⁶ for |R|², for the lopsided quadratic and for |R|² plus a linear term (which goes negative, to −0.25, so A2 excludes it); and 0.53, 0.20, 0.11, 0.22, 0.44 and 2.96 for |R|, |R|^1.5, |R|^2.5, |R|³, |R|⁴ and the saturating form.
- **What each assumption does, and whether the grain picture earns it.**
  - A1, contributions add: carries almost everything. Not earned; it is Glenn's picture of 5–6 Oct ('like angular components') taken as given. Observational register, from the checker's memory and not sourced tonight: in real three-slit set-ups A1 is only approximate, because one slit's contribution depends slightly on which others are open (looped paths), giving a small non-zero I3.
  - A2, the click reads the sum alone: not earned. If the grain may also read an additive count n of arrivals, the same theorem gives P = β|R|² + αn + γn²: a phase-blind background and a phase-blind pair term. The |R|² part cannot change.
  - Regularity: needed (without it there are pathological solutions), and harmless.
  - A3, no preferred direction: earned from 'labels are not physical' [source-entailed], since turning every contribution together is a relabelling of the reference orientation.
- **Limits, accepted from the checker.**
  - A probability bounded by 1 cannot be a quadratic form everywhere. T1 is about an unnormalised rate; for a click chance only the local form has content. This is the same crack as point 5 of item 1.
  - Observation gives κ3 below a bound, not zero. The checker computed that P = |R|^(2+ε) gives κ3 of about 0.2ε to 1.4ε, so a bound of 10⁻² fixes the exponent to about 2 ± 0.01, not exactly 2. Honest wording: 'consistent only with the squared length, to within the experimental bound, on the reachable set'.
  - A saturating detector gives κ3 proportional to intensity over saturation, so it vanishes at low intensity.
  - Nothing selects the plane: the theorem holds for arrows in any number of dimensions.
- **Published work.** Not new. It is a short corollary of classical results on quadratic functionals (Fréchet; Jordan–von Neumann). Sorkin 1994 has the set-level analogue; the generalised-probability papers (Barnum, Müller, Ududec; Ududec, Barnum, Emerson) are different and stronger. The checker located these by title and did not open them; what they contain is from its memory. No paper stating exactly T1 with T2 was found.
- **What it means for the gap.** Within 'contributions add and the grain reads the sum', the slit conditions no longer test the readout: they fix it. The open part of 'What in the handoff can cancel?' is then A1 and A2 themselves: why crossing contributions add, and why a grain's response sees only their sum.
- **Independent check:** PARTLY. The checker is Claude (own derivation, own script, brief literature search). T1, T2 and the numerics confirmed; T3's radius, the list of ways out and my scope sentence corrected, all accepted. Worth a DeepSeek check of T1–T3 (section 8).
- **Receipts:** N-2026-11-14-2-readout.py, -readout-output.json, -readout-stdout.txt, -proof.txt; N-2026-11-14-2-checker.py.
- **Confidence:** high for T1 and T2 (two derivations, classical mathematics). Medium for T3's exact statement. The literature summary is from memory.

### N-2026-11-14-3: neighbour-reading rules (D1)

- **Depth reached:** D1. By argument only.
- **Crack found:** yes, and it is located.
- **In plain words.** If each unit reads only its neighbours, the 13 Nov result survives: multiplying every weight by one factor changes nothing, so only ratios matter. The single order of all steps is not needed to say what happened: steps that do not bear on each other have no order, and what is left is a partial order. But the chances of the possible histories are still defined only by way of a total order or a time. What that hides is one thing: the rates of far-apart units must be comparable with each other.
- **Located.**
  - (a) Yes [theorem, finite level]. The checker sharpened it: the sequence's law is unchanged under any factor that depends on the whole configuration; requiring weights to stay local is what cuts that down to one constant on each part of the level joined by chains of steps that bear on each other.
  - (b) Yes for the description, not shown for the law. The partial order of steps is well defined and its law is unchanged by the common factor [theorem]. But that law is the image of the sequence law; no way of producing it without a total order or a time is known to me or the checker. The most local known construction gives each unit its own random rings in a common time and uses only the order of rings among neighbours.
  - **Where the level-wide object sits.** In the comparability of rates between distant units: a common time standard in disguise. Example: two units that are not neighbours flip at weights α and β and a third step fires when both are up; the chance that the first flips exactly once before the firing is 2αβ/(α+β)². My two residues (a shared table of ratios; no pairwise local rule) are this one thing, as the checker said.
  - **This bears on 'no coordinator above a level'.** Is 'the same rule at the same rate everywhere on a level' a law, which monism would grant, or a shared variable, which the 2 Nov line forbids? The argument cannot say. It is Glenn's call, and I flag it without a view.
  - Refinements (checker): the table of ratios may differ from site to site, it must only be fixed; rules with no races have a history that is the same under any rescaling; on an unbounded level the 'next step' rule does not exist at all and only the time-based construction does.
  - Even in the well-mixed rule the single order was partly removable: two steps on different units that read Contact's share without changing it are unordered.
  - Unison ticking under neighbour reading is unproven either way. A gap, not a result.
- **Offered by the checker, not examined:** see section 5.
- **Independent check:** PARTLY. The checker is Claude (argument only; its references to the concurrency literature are from memory).
- **Receipts:** N-2026-11-14-3-argument.txt (the argument as sent, and the verdict in summary). No script.
- **Confidence:** high for the two invariance statements. Medium for 'no order-free, time-free way to produce the law': not proved, only not known.

**Receipts table** (all in Night-Reports, uploaded from the local files by reference, so the Drive copies are byte-identical; SHA-256 of those bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-14.md | 10jVPTcxdbAdBgF81vhklKsyx_r8eBOCs | 61f2ae8e28f7d8d647a0e62dd724efc344a2b897889322c0535a84a9e98a3581 |
| N-2026-11-14-1-slit.py | 1cOH3T-oVPMk64ShCf_kQldUpILQyprQU | 08dabfbbd225f9750ba4fe9fac0f4d35300f2d15d38d50bb194ab1371752f3dd |
| N-2026-11-14-1-slit-output.json | 1kkNXgjRtGPK4g8EJuD3KOGJyb31gx1c0 | 5d02f55a7635a21135d0460c3d5e9a08a9dd0c577ce859814d6331f5531775c3 |
| N-2026-11-14-1-slit-stdout.txt | 1bbgH-U7Ibeoay5c_okF0OHJ8yHVrhdxV | 4cf25eb44dcce041387584eef2fcefc1303310651f2f09e18d502b0f1eddd9c4 |
| N-2026-11-14-1-checker.py | 1B6ddu_Yo1nTpVLa3N5xVUlb9FhJ5wlLK | 55ed5505b380aa7b59531f995ea74bb001879420170571871b3811c4442de59d |
| N-2026-11-14-1-checker-output.txt | 1-lbN6C_f54pMOz-t_ia2q0-C-lJj24VI | 817fc85ed268283f67af63d3f91593db8a7c74f663158dfa8315119569affce9 |
| N-2026-11-14-2-readout.py | 1Dz6vtfMkEs_23tO920Wss1FtWG7LVqvn | d868acacaeaa67ffd595850d0cd5572a97ee091bcbc9d6611ffc588124234d6f |
| N-2026-11-14-2-readout-output.json | 1LpUg4b1kAwlaVdm4pLCeU68nKPBGkTtl | 5d1d8a2b055cfec1c71211d651e64eb02b3e346798138f4de10e669724974d2f |
| N-2026-11-14-2-readout-stdout.txt | 1Mo3h9unA6T6eIb9uZTW4sfFMiJhB87Uu | 56ca9e5235aae6e1c79f4b2527d6933d0e21cc60a0c16e0c518b015a1816deea |
| N-2026-11-14-2-checker.py | 18lARzlmil8tsV90Djmf_nW8YEAJs0clw | 02372f179388604d0008c38324b2affed5e21610cd9fd3f91fd5836191ecb304 |
| N-2026-11-14-2-proof.txt | 1WjKIUVi53qBgyj5z31U7BBzlwwFZG3my | 10083e71827025ad76ed791c1e6529fa16fe5632d22d026588b1e275692a1e83 |
| N-2026-11-14-3-argument.txt | 19XuQQcJXuUB8G5FzLP5PJDj4mu_7kyvB | 3c97b8ec8072b9a0c064c63881ed714405a98da6befcfc87fcace0fe5891334d |
| MAP-SNAPSHOT-2026-11-14.md | 10jag0wBBDPot8_0kvRir7SrrzX8BDyiB | 402d7c28c37a4ad1949eaf5c619634fa8fe4c51b88db52697ae6cc2f030170b4 |

No receipt: the item 2 checker's printed output (its script is uploaded; its figures above are from its report), including the sensitivity figure 0.2ε to 1.4ε; the item 1 checker's wide-screen and common-jitter cases are in its script and output, which are uploaded. The three checkers' reports are summarised here and in the receipts, not filed in full.

## 5. New candidates (post-failure)

No test failed tonight and no candidate was revised. Three ideas arose after results were seen. They are labelled as such, were not examined, and nothing above was changed to fit them.

- **Jitter that belongs to steps, not to routes** (from item 1, point 4). Routes that share a stretch share its jitter; only the stretches that differ dephase. Loss of interference would then scale with how far apart the routes run and for how long, not with total route length. It would need its own rule and prediction, fixed before any run.
- **A slit test that can fire.** Since I3 = 0 is forced for R2, a discriminating version would have to test A1 or A2: for example, a rule in which a slit's contribution depends on which other slits are open, or a grain that reads more than the sum. Not specified.
- **Heap height as a tick readable from inside** (the item 3 checker's). In the partial order of steps, the length of the longest chain between two events is a count that needs no order of all steps and depends on ratios only. A candidate answer to 'how a turn is read from inside'. Not examined.

## 6. Suggested Map changes for Glenn to decide

Recommendations only.

1. **O_signed, record the run in its status.** 'Slit test run 14 Nov (Night Run N-2026-11-14-1; numbers confirmed by an independent check): the angular-sum shape read as the squared resultant is not killed (κ2 = 1.24, κ3 = 2×10⁻¹⁶; plants at 0.58 and 0.38). The pass is by construction and derives nothing.' The gap stays open.
2. **O_signed, replace 'any other readout generally gives I₃ ≠ 0'** with: 'If contributions add as vectors and the readout is a regular, non-negative function of the sum alone, I₃ = 0 for all arrangements holds if and only if the readout is a quadratic form; with no preferred direction, the squared length [theorem; classical]. The open part is why contributions add and why a grain reads only the sum.' Receipt: N-2026-11-14-2, check PARTLY.
3. **O_signed, note on its kill line.** For any candidate of the 'add, then read the sum quadratically' kind, the three-path half cannot fire; only the two-path half can. Whether to reword is Glenn's call. Receipt: N-2026-11-14-1 point 1 and N-2026-11-14-2.
4. **O_signed, add to the candidate shape two things a rule must still settle:** how jitter is shared between routes that share steps (independent jitter is what removed the fringes; common jitter removed nothing), and how arrivals are normalised (with w = 1 the screen total is not conserved). Receipt: N-2026-11-14-1 points 4 and 5.
5. **P_period, add to its shape.** 'With neighbour reading, ratios only still holds and the single order of steps reduces to a partial order [theorem, finite level]. What remains level-wide is that rates of distant units are comparable. Whether that is a law or a coordinator is undecided.' Receipt: N-2026-11-14-3, check PARTLY.

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **Update the scheduled task's STEERING id** to 1xvCEBQ9vpbyw7aVOIpNI81ESGMzMJsrW, or have it find the file by title. Tonight's PIN is now done; without a new one the run chooses for itself inside the stop rule.
- **Shared-step jitter (D2).** Write the rule for jitter that belongs to steps, with its prediction for how fringe contrast depends on slit spacing and distance, and a planted case. No run until Glenn pins it.
- **Is 'the same rates across a level' a law or a coordinator? (Glenn's ruling, not a run.)** Item 3 leaves this.
- **How a turn is read from inside (D2),** carried over from 13 Nov, now with the heap-height idea as one candidate to write down exactly.
- **Whole-step route lengths (D1).** The PIN forbids rounding L because rounding adds phase noise. But a rule stated in steps has whole-number lengths. Locate what a grain rule would need for the unrounded length to be the right count (many routes averaging, or a finer rung beneath).
- **Does fixed size with varying direction still force the squared readout? (D2.)** The local theorem needs contributions that vary in size. The checker's quick test suggests yes; not proved.
- **The minimal coupling run (D3)** still waits on Glenn's call.

## 8. Verification handoffs

```
Task (DeepSeek). Let P: R^2 -> R with P(0) = 0 and P >= 0. Define
I3(a,b,c) = P(a+b+c) - P(a+b) - P(a+c) - P(b+c) + P(a) + P(b) + P(c).
Prove or refute:
(1) If P is Lebesgue measurable and I3(a,b,c) = 0 for all a,b,c in R^2, then P(x) = x^T M x with M symmetric positive semidefinite. Give a counterexample when measurability is dropped.
(2) If in addition P(Ux) = P(x) for every rotation U, then P(x) = beta*|x|^2 with beta >= 0.
(3) Local version: if P is continuous and I3(a,b,c) = 0 only for |a|,|b|,|c| <= r, determine the largest set on which P is forced to be of the form l(x) + x^T M x, and whether non-negativity still forces l = 0.
(4) Phase-only version: suppose I3(a,b,c) = 0 is known only for |a| = |b| = |c| = 1 (all directions). Is a continuous P then forced to agree with beta*|x|^2 + const on the reachable set {|x| <= 3}? Prove, or give a continuous counterexample.
(5) Sensitivity: for P = |x|^(2+eps), give the leading-order expression in eps for I3(a,b,c), and its value for a = b = c.
```

```
Task (DeepSeek or Astra). A finite graph of bounded degree; each vertex has a state in a finite set. A local step e changes the state of one vertex, with weight w_e > 0 that is a function of the states of that vertex and its neighbours. Rule L: the next step is e with probability w_e / sum of all enabled weights. Two steps are independent if neither changes a vertex the other changes or reads. A trace is an equivalence class of step sequences under swapping adjacent independent steps.
Prove or refute:
(1) The law of the step sequence is invariant under w_e -> s(eta)*w_e for any positive function s of the whole configuration eta; if s(eta)*w_e must remain a local function for every e, then s is constant on each set of vertices connected by chains of dependent steps.
(2) The induced law on traces is invariant under a common factor and, for rules in which two enabled steps can disable or re-weight one another, is not invariant under independent factors on two dependency-connected regions. Give the smallest example.
(3) Is there a construction of the trace law that uses neither a total order of steps nor a real-valued time (for instance from local random choices alone)? Either give one, or state the known obstruction (confusion in probabilistic event structures) precisely and say whether it applies to this class.
(4) For the trace, define the height between two events as the length of the longest chain of dependent steps between them. Show its law depends on the weights only through their ratios.
```

## 9. Run notes

- **Access.** Every required source was reached: the spec (v2.1), the standing constraints (current copy, exact title), the Premise Map (version 1794620197-4c40, parsed to 180 nodes), the 13 Nov report and snapshot. The project instructions were in context. The narrative spine (context only) was not opened.
- **STEERING id.** The id in the task prompt opened the superseded file; the current one was found by title, as the prompt provides for. I read the superseded file too, before noticing its title; nothing from it was used except that its PIN is done.
- **Freeze.** The queue was saved as its own file at 06:20 UTC before any item's work. No item computation ran before the freeze; the geometry was chosen by arithmetic, stated in the queue.
- **One code slip after the freeze.** The slit script's first launch stopped on a Python syntax error (a dictionary key written as a keyword). I fixed that line and ran it. No rule, number or threshold changed, and nothing had been computed before the fix.
- **Departures from the frozen queue.** None in rules or tolerances. Two things the queue got wrong and the report corrects: its factor exp(−4σ²L) for κ2 under reading A (right for one pair, not for κ2); and its 'between about 21 and 25' for a slit's squared resultant (it runs from 18.7 to 25.0). Neither affects a check. In item 2 the report uses the checker's shorter proof.
- **Depths.** Item 1 stopped at D2: nothing was done about the cracks it found. The checker ran two cases outside the rule (common jitter; a wide screen); they are reported as the checker's and I did not extend them. Item 3 stopped at locating.
- **Checks.** Three fresh Claude subagents, none of which saw the working. The item 2 checker used web search for titles only.
- **Time.** About 06:16–06:40 London time. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports. Nothing else was edited, and no email or message was sent beyond the run's own notification.
