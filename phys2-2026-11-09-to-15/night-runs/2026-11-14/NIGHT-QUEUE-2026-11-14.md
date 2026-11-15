# NIGHT-QUEUE-2026-11-14

PHYS2 Night Run, sixth night. Claude, unattended. Frozen 14 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.

## How the queue was built

- **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (see next line); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794620197-4c40, 180 nodes); NIGHT-REPORT-2026-11-13.md in full, with its follow-ups; MAP-SNAPSHOT-2026-11-13.md. The project instructions were in context. No REVIEW notes exist in Night-Reports. The narrative spine (context only) was not opened.
- **STEERING id was stale. Reading taken.** The id given in the task prompt (1YQpKFp-…) now opens SUPERSEDED-2026-11-14-STEERING.md. As instructed, I listed the folder and took the one file titled exactly STEERING.md: ID 1xvCEBQ9vpbyw7aVOIpNI81ESGMzMJsrW, modified 14 Nov 01:36 UTC. Its PIN is the slit test. The superseded file's PIN (the five closed levels) is listed in the new file's NOTES as done.
- **PIN:** 'Slit test of the angular-sum handoff', D2. It is item 1 and is run exactly as written. The PIN leaves four things for the run to fix before running (distances, slit spacing, ω; how fringes are counted and their spacing measured; the noise grid; how 'averaged over noise draws' is read). They are fixed below.
- **Stop rule applied.** No single-level stability work. That still excludes 'How sharp is the step-counted clock against size?' from the 13 Nov follow-ups.
- **Coupling not run.** Still Glenn's call; STEERING shows no call.
- **Priority 2 (13 Nov follow-ups):** 'Neighbour-reading rules (D1)' is item 3. 'The total-probability statement on the telegraph model' is dropped: the map (O_signed, 14 Nov) archives that line as superseded by the slit test. 'Byrne's trap field' was taken up in session on 13 Nov (map note on E_ntau: the 2014 review read, the 1996 paper still unread); it is not queued, because the remaining step is reading one paywalled paper and I rate its yield tonight as low. 'How a turn is read from inside (D2)' is carried over, not queued: three items fill the night.
- **Priority 3 (map regions changed since the 13 Nov snapshot):** O_signed reworded with a new kill line (the PIN's target); O_own and O_drift archived into O_ratelaw. The merges are Glenn's rulings of 14 Nov and need no work.
- **Priority 4 and 6 (unproved if-then; untagged necessity):** O_signed's statement says 'read as the squared resultant give I₂ ≠ 0 and I₃ = 0 together, since only pairs cross; any other readout generally gives I₃ ≠ 0'. 'Generally' is not a theorem, and the PIN's own scope line says a pass 'does not derive the squared readout'. Item 2 asks exactly how much of the squared readout the no-third-order condition forces.
- **Ranking:** item 1 (pinned); item 2 (easy, high: an if-then that would turn the slit conditions from a consistency check into a constraint on the readout); item 3 (easy, moderate).
- **Method lines applied:** 'say which necessary' (tags below); observational comparisons labelled; no coordinator above a level (bears on item 1's noise reading and item 3).

---

**N-2026-11-14-1 — Slit test of the angular-sum handoff (the PIN)**

- **Target:** O_signed, 'What in the handoff can cancel?', and its kill line.
- **Picture, in one sentence:** every straight route from source to screen carries an orientation that turns by a fixed angle per step; at each screen grain the arriving orientations add as axes, and we ask whether what adds up behaves as observed with two and three slits open.
- **Task:** given the rule in STEERING's PIN, compute the stated measures for the stated readouts and controls; apply the harness checks and then the kill line; then the noise part.
- **Inputs:** STEERING.md PIN text (1)–(9), which governs. Nothing in it is changed here.
- **Depth:** D2 Shape.
- **Effort cap:** about 45% of the night.
- **Done means:** the table of κ2 and κ3 for R2, R4, RS, C+ and C-arrow; harness verdict; kill-line verdict for R2; fringe counts, spacings and their ratio; the noise table under both readings below; the scope sentence the PIN requires.
- **Mechanism, fixed now.**
  - *Geometry (the PIN leaves this to the run).* Lengths in grain units; one step is one grain unit of route length. Source at lateral position 0, a distance D1 = 10 000 in front of the barrier. Slit centres at lateral positions y = −100 (A), 0 (B), +100 (C); each slit is the 5 grains at centre −2 … +2. Screen a distance D2 = 2 000 behind the barrier; 1001 grains at x = −500 … +500. ω = π/5 radians per step. A history is (slit grain y, screen grain x); L = √(D1² + y²) + √(D2² + (x − y)²), kept as a float, never rounded. w = 1. 15 histories reach each screen grain with all slits open.
  - *Why these numbers, by arithmetic and not by trial.* For the axis (R2) the resultant's phase is 2ωL, so the effective wavelength is π/ω = 5; for the arrow it is 2π/ω = 10. Two slits a distance d apart give fringes about (wavelength)·D2/d apart near the screen centre: for adjacent slits (d = 100), 100 grains for R2 and 200 for the arrow; for the outer pair (d = 200), 50 and 100. The screen is 1000 wide, so R2 should show ten or more fringes with three slits open. The single-slit envelope's first zero for R2 is at about 5·2000/5 = 2000, outside the screen, so fringes are not washed out by slit width. Off axis the spacing grows by the factor (1 + x²/D2²)^1.5, at most 1.10 at the screen edge.
  - *Fringe count (PIN (1)).* The number of strict interior local maxima of P_ABC(x) under R2 whose height is at least 10% of the screen maximum. Requirement: at least 5. If fewer, the geometry was badly chosen; the item is then reported as ill-posed and nothing is re-chosen.
  - *Readouts and controls.* Exactly as PIN (3). For RS, s = the median over the 1001 screen grains of |R(x)|² with all three slits open, computed once from the noise-free axis sum and then held fixed for all configurations.
  - *Measures.* Exactly as PIN (4). P0 = 0; no background is declared.
  - *Harness checks (PIN (5)).* C+: max over x of |I2| and |I3| ≤ 10⁻⁹ × max P_ABC. R4 and RS: κ3 > 10⁻³.
  - *Why C+ must give zero.* P is a count of open histories; counts add over disjoint slit sets, so every I2 and I3 is an exact integer zero.
  - *Why the two plants must trip (closed form).* Write s_i = |R_i|² for slit i's own resultant and p_ij = 2 R_i·R_j. For R4, P = (Σs + Σp)², and the terms that survive in I3 are exactly those that touch all three slits: I3 = 2(s₁p₂₃ + s₂p₁₃ + s₃p₁₂ + p₁₂p₁₃ + p₁₂p₂₃ + p₁₃p₂₃). Each slit's five histories are nearly aligned on this screen (phase spread across a slit at most (2π/5)·4·sin 14° ≈ 1.2 rad), so s_i ≈ s₀ between about 21 and 25 and p_ij ≈ 2s₀ cos φ_ij, giving I3 ≈ 4s₀²[(c₁₂ + c₁₃ + c₂₃) + 2(c₁₂c₁₃ + c₁₂c₂₃ + c₁₃c₂₃)] with c = cos φ. Where the three are in phase this is 36 r⁴ against I2 = 14 r⁴ per pair (r⁴ = s₀²): ratio 36/42. The bracket is not identically zero and the screen sweeps the phases through ten or more fringes, so Σ|I3| is of the order of Σ|I2|: κ3 of order 0.1 to 1, at least two orders above the 10⁻³ line. For RS, P = 1 − exp(−S/s) is strictly concave in S = |R|². Where three equal resultants are in phase with u = s₀/s, I3 = 1 − e^(−9u) + 3e^(−4u) − 3e^(−u) and I2 = 2e^(−u) − e^(−4u) − 1; at u = 0.3 these are −0.385 and +0.181, so again κ3 is of order 1. (The map note of 14 Nov records about 0.5 and 0.4 in one trial geometry; that trial was not mine and its geometry is not used.) If either plant gives κ3 ≤ 10⁻³ the harness is blind: report a harness failure and stop the item.
  - *Kill line (PIN (6)).* For R2: κ2 < 0.05 or κ3 > 10⁻⁶. Expectation stated now: κ3 at float level (10⁻¹² or below), because |R|² has only pair terms; κ2 of order 1.
  - *Fringe spacing (PIN (7)).* For the adjacent pair AB open: the mean distance between consecutive strict interior local maxima of P_AB(x) that reach at least 10% of that curve's maximum, over the whole screen; for R2 and for C-arrow; and the ratio arrow/R2. Predicted now: about 100–105 and 200–210; ratio 2.0 within 5%. The same measure for ABC is reported beside it. No kill is attached; the PIN asks for a report.
  - *Noise part (PIN (8)); run only if the harness checks pass.* Each history h gets orientation θ_h = ωL_h + σ·√L_h·ξ_h with ξ_h standard normal, independent between histories; this is the sum of L_h independent per-step jitters of standard deviation σ. Within one noise draw a history keeps its jitter in all 8 configurations (PIN (1): a history is the same history whichever slits are open). Readout R2 only, plus C+ as a null. Seed 20261114. Draws: 2000; the first 200 are also reported on their own, since the PIN's floor is 200.
  - *σ grid, fixed now.* 0, 0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.0, π/2. It runs from 0 to π/2 as the PIN says. It is dense at the small end because L ≈ 12 000 steps: the doubled-angle jitter 2σ√L reaches 1 radian at σ ≈ 0.0046, so on an even grid every point but the first would be fully scrambled.
  - *Two readings of 'averaged over noise draws'. Both are reported; neither is chosen after the fact.* Reading A: average P(x) over draws for each configuration, then form I2, I3, κ2, κ3 from the averaged P (what a screen that accumulates many arrivals would show). Reading B: form κ2 and κ3 within each draw, then average them (the literal wording).
  - *Predictions, stated now.* κ3 stays at float level under both readings, for every σ (algebra, draw by draw; A is linear in P). Under A, the pair term is multiplied by about exp(−4σ²L) (two independent histories, each contributing exp(−2σ²L)), so κ2 falls to its sampling floor, which shrinks as 1/√(draws), by σ ≈ 0.01. Under B, κ2 does not fall to 0: with 5 histories per slit, a single draw's pair term is a sum of 25 random cosines and stays of order 1; I expect a plateau of order 1 from σ ≈ 0.01 upward. If B goes to 0 or A does not, I have misread the rule and will say so.
  - *Numerics.* Everything is direct sums; no solver. Per-draw summaries only are kept for the noise part (κ2, κ3 per draw; running sums of P). Pilot: 20 draws at one σ, timed, before the main loop.
  - *By construction, said now (PIN (9), P2.6-03 §3):* R2's I3 = 0 is algebra. A pass shows that the candidate shape is consistent with both slit anchors and that the harness tells readouts apart. It does not derive the squared readout.

**N-2026-11-14-2 — How much of the squared readout does 'no third-order term' force?**

- **Target:** O_signed, the sentence 'any other readout generally gives I₃ ≠ 0'; the PIN's scope line (9).
- **Picture, in one sentence:** if what arrives at a grain is one summed arrow, and the chance of a click depends only on that sum, which ways of reading the sum leave nothing over once all the pairs are accounted for?
- **Task:** given (A1) the contributions reaching a screen grain add as vectors in the plane, R = Σ over open slits of R_i; (A2) P is a function of R alone, the same function whichever slits are open, continuous, non-negative, with P(0) = 0; prove whether I3 = 0 for all R₁, R₂, R₃ holds if and only if P is a quadratic form in R; and whether adding (A3) no preferred direction (P unchanged when all contributions are turned together) leaves exactly P = β|R|². State what each assumption does and which are earned in the grain picture. Search for a published result first.
- **Inputs:** the definitions of I2 and I3 in the PIN; standard results on Fréchet's functional equation.
- **Depth:** D3 Probe (one if-then proof, one small check).
- **Effort cap:** about 25%.
- **Done means:** the if-then proved or a counterexample; the list of assumptions with tags; one sentence for the map.
- **Mechanism, fixed now.**
  - *Proof route.* I3 = 0 for all triples, with P(0) = 0, is Fréchet's equation Δ_aΔ_bΔ_c P = 0. For continuous P its solutions are polynomials of degree at most 2: P = ℓ(R) + Q(R), ℓ linear, Q a quadratic form. Non-negativity near R = 0 forces ℓ = 0 (since ℓ(−R) = −ℓ(R) and Q is second order). Rotation invariance of a quadratic form forces Q = β|R|². Converse by expansion.
  - *Check, numerics.* 10 000 random triples of plane vectors (components uniform in [−3, 3], seed 20261114). Readouts: |R|^p for p = 1, 1.5, 2, 2.5, 3, 4; an anisotropic quadratic form R_x² + 3R_y² + R_xR_y; |R|² + (unit vector)·R; 1 − exp(−|R|²). Report max |I3| relative to max P for each. Expected: float level for the two quadratic forms and nothing else; the form with a linear term has I3 = 0 but goes negative.
  - *Planted failure, guaranteed.* The harness is first given P = |R|⁴ at R₁ = R₂ = R₃ = (1, 0): I3 = 81 − 3·16 + 3·1 = 36 exactly. And P = |R|² at the same point: 9 − 12 + 3 = 0. If it does not return 36 and 0 the check is void.
  - *Kill line:* a continuous non-negative P with P(0) = 0 that is not a quadratic form and has I3 = 0 on all triples refutes the claim.
  - *By construction, said now:* the result can only be conditional on A1 and A2. It cannot say why contributions add, or why the readout is a function of the sum alone.

**N-2026-11-14-3 — Does 'ratios only' survive when units read neighbours, and what replaces the single order of steps?**

- **Target:** P_period (13 Nov shape: inputs 'one order of all steps' and 'the well-mixed read of Contact's share'); F_time; the standing line 'no coordinator above a level'.
- **Task:** given a rule in which each unit's next step has a weight that reads only that unit's state and the states of a bounded set of neighbours, determine whether (a) the law of what happens is unchanged when every weight is multiplied by one factor; (b) there is a description of 'what happens' that does not use one order of all steps; say exactly where, if anywhere, a level-wide object is still used.
- **Inputs:** the 13 Nov item 1 result and its checker's objections; standard facts about jump chains and about commuting independent actions.
- **Depth:** D1 Locate. By argument only; nothing is run. This is not single-level stability work: no rates are drawn and no balance or cycle is examined.
- **Effort cap:** about 15%.
- **Done means:** yes or no for (a) and (b), each with its smallest assumption, and the exact place where a level-wide object remains, if one does.
- **Mechanism:** argument only; no harness, so no planted failure.

---

Checks: after each item, a fresh Claude subagent that has not seen the working. Receipts uploaded with SHA-256 before the report is written.
