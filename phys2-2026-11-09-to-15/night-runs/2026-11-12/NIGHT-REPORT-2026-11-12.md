# NIGHT-REPORT-2026-11-12

PHYS2 Night Run, fourth night. Claude, unattended, 12 Nov 2026, from about 06:16 UTC. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

All five closed levels with no stable balance tick. Each one, from every start tried (8 by the run, 24 by an independent checker using a different integrator), settles onto a single steady cycle, with periods of 43.5, 5.0, 277.2, 88.5 and 171.2 model time units. No start came to rest, and no other kind of motion appeared. This is about these five draws only.

What the five share, as measured: each cycle is strongly attracting, each has one slow side pool (L in two draws, P in three) with the other fast or nearly empty, and one turn takes between 3 and 6 of that pool's return times. My reading that the slow pool sets the period did not survive the check. The checker found that the period responds more strongly to the seeding rate than to the slow pool's rate in four of the five, and that all five sit close to the edge where the low balance has only just lost its stability; draw 2045 stops ticking if seeding drops by 0.05%. So the sounder statement of what they share is that they are clocks found at a thin margin, not that they share a mechanism.

Two smaller results. A clock's period on a closed level is the same at every size and scales inversely with the rates, so what the model produces is a pure number (turns counted in rate-times), while the unit of time and the size-independence are both built in by how the model is written. And for coupling between levels, the smallest seeding term cannot start an upper rung that holds nothing, and the 10 Nov formation threshold survives it unchanged; any constant passive feed that does start an empty rung turns that threshold into a smooth crossover.

One part of my harness failed its own planted test: the rest rule did not recognise a known damped swing as rest. No draw's result depends on that rule, but it is on the record in sections 4 and 5.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-12.md (Drive ID 1YFFTrve5pOLZdl8oS9gIhpjqcSD-ZkVA, created 06:21:20 UTC) and not altered afterwards. It was uploaded from the local file by reference, so the Drive copy is byte-identical; SHA-256 90db63b1b75d55db4fe56defe247d859eedf61e835f8b0f66b0729fb1396fba5. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-12
>
> PHYS2 Night Run, fourth night. Claude, unattended. Frozen 12 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
>
> ## How the queue was built
>
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (ID 1YQpKFp-…, created 11 Nov 14:34 UTC: one PIN, one SKIP line, four NOTES); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794437936-384c, 179 nodes); NIGHT-REPORT-2026-11-11.md with its follow-ups; MAP-SNAPSHOT-2026-11-11.md; the 10 Nov report's coupling item; N-2026-11-11-2-num.py, its stdout, and the checker's N-2026-11-11-2-checker-num2.py and -checker-full.txt (the source of the five draw numbers); ASTRA-2026-11-11-closed-level-clock-m19-kr3.md. The project instructions were in context. No REVIEW notes exist in Night-Reports.
> - **Not blind on one draw.** The map's node K_restless says the night run 'does not know' Astra's result on the m = 19, kr = 3 draw, so that its answer would be a blind reproduction. That did not hold: the run is required to read the map, the map carries the result (period 43.548384, a relaxation cycle, Floquet logarithms −728.66 and −2509.65), and I also opened Astra's file before freezing this queue. Draw 2045 is therefore a reproduction with knowledge of the answer. The other four are blind. The classifier below was written with that one case in mind (it told me the system is stiff and that ordinary monodromy eigenvalues will underflow); no threshold in it was set from Astra's numbers.
> - **Draw numbering, reading taken.** The five numbers come from the checker's script, whose loop index `it` starts at 0. So draw n means the (n+1)-th call of `draw()` in N-2026-11-11-2-num.py with seed 20261111. This is checked before any integration: draw 2045 must come out as m = 19, kr = 3 with the rates printed in the 11 Nov report's second handoff, and each of the five must have exactly three balances, all unstable in the class. If either check fails the item is ill-posed and stops.
> - **Priority 1 (PIN):** item 1.
> - **Priority 2 (11 Nov follow-ups):** 'What does a level with no stable balance do?' is the PIN. 'A sounder classifier' is built into the PIN. 'The minimal C_seed revision, run (D3)': **not run tonight.** Reading taken of STEERING's NOTES: 'What follows the five-level run is Glenn's call at review', so a coupling run would pre-empt that call. It is queued as item 3 at D2, specification and algebra only, in the minimal form the NOTE requires, so that it is ready if Glenn calls it. 'Census of outer instability' and 'Floquet multipliers of clocks 19387 and 33538': excluded by the SKIP stop rule (single-level stability work, carried follow-ups included).
> - **Priority 3 (map regions changed since the 11 Nov snapshot):** two new Known nodes, K_mid and K_restless, with notes on K_bal, O_drift and K_clock and a new Walls method line ('common or uncommon is not a discriminator'). K_restless's first 'follows' line ('a period that nothing put in … set by the rates alone') is an if-then that tests P_period and has no proof on the map: item 2.
> - **Excluded:** everything under the SKIP stop rule; the standing constraints' Closed and 'Open and not load-bearing' lists; Archive and Outcome nodes. Nothing is on RETIRED.
> - **Reading taken on item 2 and the stop rule.** Item 2 is a scaling argument about what fixes a clock's period, with one numerical confirmation on cycles item 1 has already computed. It draws no new rates, classifies no balances and surveys no stability, so I read it as outside the stop rule. If Glenn reads the rule as 'nothing on one level but the PIN', item 2 should be discounted; its proof is two lines and stands or falls on its own.
> - **Method line applied (Walls, 11 Nov):** how often something turned up in the sweep is not reported as evidence for or against anything. The PIN's own caution is applied: a negative result is about these five draws only.
> - **Ranking:** item 1 (PIN; hard, high); item 2 (easy, high: says exactly what in a level's period is and is not put in by hand); item 3 (easy, moderate: preparation).
>
> ---
>
> **N-2026-11-12-1 — Decision run on the five closed levels with no stable balance (PIN)**
>
> - **Target:** P_period (the emergent-period conjecture); K_restless; K_mid; O_drift.
> - **Task:** given structure S (closed level, T = 1, roles C, V, L, P, ρ(x) = k3·I_x(kr, m − kr + 1), x = C/T; draws 2045, 301417, 384616, 456280, 616482 of the 11 Nov sweep), integrate each and say how it ends: steady cycle / other sustained motion (described) / settles at an edge state that is not one of the three balances (which) / unresolved. For a steady cycle compute invariant I = period, swing of each role, Floquet multipliers. Then say what the five have in common.
> - **Inputs:** `draw()` of N-2026-11-11-2-num.py, seed 20261111; the closed-level equations as in the 11 Nov report's first handoff.
> - **Depth:** D3 Probe. One bounded attempt per draw.
> - **Effort cap:** about 70% of the night.
> - **Done means:** per draw, one of the four answers for each start and for the draw; for cycles the numbers above; a table of the pre-listed common-feature quantities; a statement of what is and is not shown.
> - **Mechanism, specified now.**
>   - *Equations (4 variables, T conserved):* dC = −(k1+k2+k7)C + k6·L + (k10+ρ)V; dV = k2·C + k5·L + k8·P − (k10+ρ)V; dL = k1·C − (k5+k6)L; dP = k7·C − k8·P. Analytic Jacobian J as in the 11 Nov scripts. 'In the class' means restricted to the tangent space {δC+δV+δL+δP = 0}, M = (BᵀB)⁻¹BᵀJB.
>   - *Balances:* roots of H(x) = (k10+ρ(x))(1 − c·x) − D·x on (0, 1/c), 4 000-point grid with exact end signs, brentq to 10⁻¹⁵. Exactly three, each with max Re λ(M) > 0, or the draw is ill-posed.
>   - *Time scale:* τ = 1/min |Re λ| over the nine class eigenvalues at the three balances. One block is B = 10·τ.
>   - *Starts (8 per draw):* (0.25, 0.25, 0.25, 0.25); (0.02, 0.18, 0.70, 0.10); and each balance y* ± 10⁻⁶·(1, −0.3, −0.4, −0.3).
>   - *Integration:* scipy solve_ivp, LSODA, rtol 10⁻¹⁰, atol 10⁻¹³, analytic Jacobian, in blocks, no dense output. From each block only summaries are kept, taken at the solver's own steps: min and max of each role, and the largest relative residual r(y) = max_i |f_i(y)| / g_i(y), where g_i is the sum of the absolute values of the terms of equation i (r = 0 at a balance, r of order 1 in fast motion). A guard stops a start if any role leaves [−10⁻⁹, 1 + 10⁻⁹] (reported as 'guard fired', not interpreted).
>   - *Rounds:* a round is Stage A, 6 blocks (60 τ) of transient, then Stage B, measurement. At most 4 rounds per start.
>   - *Rest rule (the sounder classifier of 11 Nov §7; no distance to a balance at a fixed time):* after Stage A, the start is 'at rest' only if all three hold. (i) Residual: r < 10⁻⁸ at every solver step of the last block. (ii) Contraction: the largest ‖f‖∞ in the last block is no larger than in the block before it. (iii) Newton's method on f = 0 within the class, started from the end state, converges (‖f‖∞ < 10⁻¹³) to a point within relative 10⁻⁶ of the end state at which every class eigenvalue has negative real part. The answer names the point: one of the three balances, or 'an edge state' with its coordinates if it is none of them. If (i) holds and Newton lands on a point with an eigenvalue of non-negative real part, the start is not at rest (it is passing a saddle) and the round continues.
>   - *Cycle rule:* if not at rest, Stage B fixes the section C = (C_min + C_max)/2 from the last Stage A block and records upward crossings (event, direction +1; only crossing times and states kept) until 40 crossings or 100 τ, whichever first. 'Steady cycle' if, for the smallest p in {1, 2, 3, 4}, the last 12 + p crossings satisfy: states p apart agree to 10⁻⁷ (largest absolute difference over the four roles, T = 1), and the p-step return times agree to relative 10⁻⁷. The period Θ is the mean p-step return time. So a cycle is detectable only if its period is below about 100 τ/(13 + p); a longer one comes out 'unresolved', and that limit is reported per draw.
>   - *After 4 rounds without rest or cycle:* 'other sustained motion' if at least 14 crossings were recorded in the last Stage B and the largest residual r in the last Stage A block is above 10⁻⁶ and within a factor 2 of its value in the round before (described by the spread of return times and section states); otherwise 'unresolved'.
>   - *Draw verdict:* the common answer if all 8 starts agree (cycles count as the same if their periods agree to 10⁻⁶ and their section-independent swings agree to 10⁻⁶); otherwise the starts are listed separately. A start placed 10⁻⁶ from a balance that is still within 10⁻³ of it after 4 rounds is reported as 'did not leave', not as rest.
>   - *Cycle measurements:* one more period from the last section state with 20 001 output times (discarded after use): min and max of each role, and the fraction of the period C spends above the section.
>   - *Floquet multipliers:* the 4-variable flow has one multiplier exactly 1 from the conserved total (the equations are homogeneous of degree 1, so scaling the total maps the cycle to a cycle); this one is stated, not computed. The three in the class: propagate an orthonormal basis of the class tangent space under the variational equation along the cycle, in n segments per period with n = ⌈Θ·Λ/5⌉, Λ the largest absolute row sum of J seen on the cycle, re-orthonormalising by QR at each segment and summing the logarithms of the diagonal of R. Three periods are propagated; the three sums over the third period are the Floquet logarithms (multipliers e^log). Checks, all reported: the largest log is within 10⁻⁵ of 0 (the phase direction); the third period's sums agree with the second's to 10⁻⁵ (absolute, or relative for sums larger than 1); the sum of the three equals ∫tr J dt over the period to relative 10⁻⁶. The cycle is called stable if the other two logs are negative.
>   - *Common features, listed now so they are not picked afterwards:* m, kr, kr/m; the eight rates; c and D; the class eigenvalue pattern at each balance (real or complex, how many unstable); the ratios k8/(k5+k6), k1/(k5+k6), k7/k8, k3/k10; τ; Θ; Θ·(k5+k6), Θ·k8, Θ·k10; swing of each role; the fraction of the period spent with C above the section; the two non-trivial Floquet logs divided by Θ. Anything said to be 'in common' beyond this table is marked as a reading. Per the PIN and the 11 Nov method line: no statement about how common such levels are, and a negative result is about these five draws only.
> - **Planted cases, run with the same code and the same rules (the generic classifier takes f, J, the equilibria and the section coordinate), before the five draws.**
>   - *Known steady cycle (must return 'steady cycle'):* Stuart–Landau, ż = (μ + iω)z − |z|²z, μ = 1, ω = 2π, start z = 0.5, equilibrium z = 0 (τ = 1). Analytic: period exactly 1; Floquet logs 0 and −2μ = −2. Pass if p = 1, |Θ − 1| < 10⁻⁶, logs within 10⁻⁵ of 0 and −2.
>   - *Stiff cycle (control for the multiplier routine in the regime the model is expected to be in):* the same with μ = 400. Analytic: |z| = 20, period 1, logs 0 and −800, a multiplier (e^−800) far below double precision. Pass if the second log is within relative 10⁻⁵ of −800.
>   - *Known damped swing that rests (must return 'at rest', must not return 'steady cycle'):* Stuart–Landau with μ = −0.05, ω = 2π, start z = 0.5. Analytically |z(t)| ≤ 0.5·e^(−0.05t), so no orbit is periodic and z → 0; τ = 20, so Stage A is 1 200 time units and |z| ≤ 0.5·e^(−60) at its end, far below every tolerance. It swings about 1 200 times on the way.
>   - *Known rest in the model's own code (must return 'at rest'):* draw 2045's rates with k3 = 0. Then ρ ≡ 0 and the level is a closed linear exchange among four roles with every role reachable from every other (k1, k2, k5, k6, k7, k8, k10 > 0), i.e. the generator of an irreducible four-state Markov chain: one balance, and every start with T = 1 converges to it (Perron–Frobenius). Start (0.25, 0.25, 0.25, 0.25).
>   - *Known sustained motion that is not a cycle (must return 'other sustained motion', must not return 'steady cycle'):* two uncoupled Stuart–Landau units, μ = 1, with ω₁ = 2π and ω₂ = 2π√2, starts 0.5 and 0.5i, section on Re z₁. Analytically the attractor is a 2-torus with irrational frequency ratio: Re z₁ returns with period exactly 1, but z₂ advances by the angle 2π√2 per return, so states p apart differ by |e^(2πi·p√2) − 1| ≥ 1.03 for p = 1..4 (the smallest is p = 2: 2√2 = 2.828…, 0.172 of a turn from an integer, chord 2·sin(π·0.172) = 1.03; p = 1: 0.414 of a turn; p = 3: 0.243; p = 4: 0.343). No p ≤ 4 can meet 10⁻⁷, so 'steady cycle' is impossible.
>   - *Planted failure F1 (cycle rule), guaranteed:* the damped swing above. It crosses any section through its swing many times with slowly changing return states; successive section states shrink by the factor e^(−0.05) per turn, a relative change of 4.9% ≫ 10⁻⁷, and in any case the rest rule fires first. If the classifier says 'steady cycle', it is blind.
>   - *Planted failure F2 (rest rule), guaranteed:* the μ = 1 cycle. On it |ż| = |ω|·|z| = 2π and the gross terms are bounded, so r stays of order 1 ≫ 10⁻⁸ at every step; the rest rule must refuse. If it says 'at rest', it is blind.
>   - *Planted failure F3 (trace check of the multiplier routine), guaranteed:* on the μ = 1 cycle, repeat the trace check with tr J replaced by tr J + 1. The integral then differs from the true one by exactly Θ = 1, so the check (relative 10⁻⁶ of |−2|) must fail.
>   - *Harness status:* the item's numerics are a receipt only if all five planted cases return their required answers and F1–F3 trip. If the stiff control fails but the others pass, the classification stands as a receipt and the Floquet numbers do not.
> - **Sizing:** pilot = the planted cases plus one start of draw 2045, timed and written into the run notes before the main loop. If the projected time for 5 draws × 8 starts exceeds 60 minutes, the number of starts is cut from 8 to 4 (the two interior starts, and the + perturbation of the low- and high-share balances) for all draws alike, and that is said in the report. A run killed for time is reported with the count completed and is not re-run with changed rules.
> - **Kill lines:** none on the outcome; it is a measurement. For K_restless's kill line: draw 2045 settling to rest, or onto anything other than a cycle of period 43.548, would trip it, and is reported as such.
>
> **N-2026-11-12-2 — What sets a closed level's period, and what in it is put in by hand**
>
> - **Target:** the edges K_restless → P_period and K_clock → P_period ('the period is set by the rates alone, not by the start and not by how much the level holds … a period that nothing put in'); P_period's statement ('no time at the substrate').
> - **Task:** given the closed-level equations with any recruitment law ρ(x) of Contact's share, prove whether (a) a cycle's period and its class Floquet multipliers are the same at every total T; (b) multiplying every rate (k1, k2, k3, k5, k6, k7, k8, k10) by s > 0 divides the period by s and leaves the multipliers unchanged; (c) hence Θ = Φ/k_ref, where k_ref is any one rate and Φ depends only on m, kr and the seven rate ratios. Then tag the map's sentence by sense: which part is a theorem of the model, and which part of the period is an input.
> - **Inputs:** the equations; cycles found in item 1 (for the numerical confirmation only).
> - **Depth:** D3 Probe (an if-then proof; easy).
> - **Effort cap:** about 10%.
> - **Done means:** (a)–(c) proved or refuted; one numerical confirmation; a sentence for the map stating what is emergent (the pure number Φ) and what is not (the unit of time, carried by the rates).
> - **Mechanism, specified now:**
>   - *Proof route:* (a) f(λy) = λf(y) for λ > 0 because x = C/T is unchanged; so y(t) a solution ⇒ λy(t) a solution with the same time course; J(λy) = J(y) (degree 0), so the variational equation along λy(t) is identical. (b) f_s = s·f; y(st) solves the scaled system; J_s = s·J and the period is Θ/s, so the monodromy is unchanged. (c) from (b) with s = 1/k_ref.
>   - *Numerical confirmation (uses item 1's code and rules unchanged; only if item 1 found a cycle):* for each cycle, re-measure the period (i) at total T = 7.3 from the start 7.3·(0.25, 0.25, 0.25, 0.25), and (ii) with every rate doubled. Check (i): Θ_T/Θ within 10⁻⁶ of 1. Check (ii): Θ_s/Θ within 10⁻⁶ of 0.5. (The guard and tolerances that assume T = 1 are scaled by T.)
>   - *Planted failure, guaranteed:* apply check (i)'s test, 'ratio within 10⁻⁶ of 1', to the doubled-rate run. By (b) the ratio is exactly 0.5, so the test must fail. If it passes, the comparison is blind.
>   - *Kill line:* (a) refuted by any cycle whose period differs between totals beyond 10⁻⁶ relative; (b) likewise for the ratio 0.5.
>
> **N-2026-11-12-3 — The minimal C_seed coupling: what the smallest seeding term can and cannot start (specification and algebra only)**
>
> - **Target:** C_seed ('Growth depletes the rung beneath'); P_fedbelow; 11 Nov item 3 and its checker's point (2); STEERING NOTE ('use only the smallest term — the one that lets the lower rung start the upper one').
> - **Task:** given the 10 Nov coupling (U = κ·P1·C2 leaves dP1/dt and enters dV2/dt; the upper level has no outside supply) plus the one term σ·x1·V2 in place of the upper level's own seeding u10·V2 (x1 = C1/T1), determine by algebra: (a) which upper states are invariant, in particular whether the empty upper level (T2 = 0) can be started by the lower one; (b) the joint balances, and whether the 10 Nov existence threshold κ·c·k12 > k9 (c = (u8+u9)/(u7·u9)) survives; (c) the sign condition on the linearisation at the empty upper level with the lower level at its balance. Then write the run Glenn may call, with kill line and planted failure.
> - **Inputs:** 10 Nov item 2 and 11 Nov item 3 as written in those reports; the open-level equations.
> - **Depth:** D2 Shape. No dynamics are integrated.
> - **Effort cap:** about 15%.
> - **Done means:** the equations; answers to (a)–(c) from sympy; the smallest further term needed if (a) says the empty level cannot be started; a frozen test for a later night. Explicitly not run.
> - **Mechanism:** sympy algebra only. Conservation identity to be checked: d(T1 + T2)/dt = k12 − k9·P1 − u9·P2. Nothing is tuned and nothing is integrated.

## 3. State changes noticed

- **Map diff.** The Premise Map was read at version 1794437936-384c (11 Nov's snapshot was 1794281872-597e). 179 nodes against 177. Two new Known nodes, both live:
  - K_mid, 'The middle of three balances is always unstable, on open and closed levels' (night runs of 10–11 Nov, DeepSeek's proof check).
  - K_restless, 'A closed level with no stable balance can tick: one verified clock (m = 19, kr = 3)' (Astra, reproduced by Claude).
  - Notes dated 11 Nov were added to K_bal, O_drift and K_clock, and a method line to the Walls: common or uncommon is not a discriminator.
  - Counts now: Known 54, if-then 37, Candidate 28, Retired 19, Gap 19, Adopted 12, Floor 10; live 96, Archive 60, Reserve 15, Reservoir 8. No node was removed and no type or shelf changed. The diff was made by node ids and counts against the 11 Nov snapshot read through Drive; a field-by-field machine diff was not run.
- **Standing constraints.** Unchanged since 10 Nov (ID 1LjICJx…, exact title).
- **Steering applied.** STEERING.md was replaced on 11 Nov. Its one PIN is item 1. Its stop rule excluded the census of outer instability and the Floquet multipliers of clocks 19387 and 33538. **Reading taken on the NOTES:** 'What follows the five-level run is Glenn's call at review', so the coupling run suggested on 11 Nov was not run; item 3 prepares it at D2, in the minimal form the NOTE requires. **Reading taken on item 2:** a scaling proof with one confirmation on cycles already computed is not 'single-level stability work'. If Glenn reads the stop rule more widely, discount item 2.
- **Not blind on draw 2045.** The map says this run would not know Astra's result. It did: the run must read the map, and the map carries it. Draws 301417, 384616, 456280 and 616482 were blind.
- **Previous follow-ups:** the five-draw run became the PIN; the sounder classifier was built into it; the coupling run became item 3 at D2; the rest are under the stop rule.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-12-1: decision run on the five closed levels (PIN, D3)

- **Depth reached:** D3.
- **Crack found:** yes. Every one of the five draws ends on a steady cycle.
- **Inputs checked first.** Draw n is the (n+1)-th call of `draw()` with seed 20261111. Draw 2045 came out as m = 19, kr = 3 with the 11 Nov handoff's rates exactly. Each of the five has exactly three balances, all unstable in the class.
- **How each draw ends.** All 8 starts per draw (two interior starts, and both sides of each balance at 10⁻⁶) were classed 'steady cycle' in the first round, with one crossing of the section per turn. Within a draw the 8 periods agree to 2×10⁻⁹ and the swings to 10⁻⁹.

| Draw | m, kr | Verdict (8 of 8 starts) | Period Θ | Contact's swing | Void's swing | Floquet logs in the class (phase log ≈ 0) |
|---|---|---|---|---|---|---|
| 2045 | 19, 3 | steady cycle | 43.5483838 | 0.0117 – 0.3025 | 0.2728 – 0.7686 | −728.6581, −2509.6482 |
| 301417 | 18, 5 | steady cycle | 5.0012035 | 0.0252 – 0.5886 | 0.0070 – 0.7244 | −26.4637, −201.3061 |
| 384616 | 14, 4 | steady cycle | 277.1509408 | 0.0185 – 0.5828 | 0.0886 – 0.7036 | −120.5322, −1506.5514 |
| 456280 | 15, 5 | steady cycle | 88.5270387 | 0.0430 – 0.5777 | 0.1212 – 0.6716 | −453.2033, −4593.0757 |
| 616482 | 12, 4 | steady cycle | 171.2382391 | 0.0639 – 0.4907 | 0.3092 – 0.7414 | −188.4835, −9790.0927 |

  - A multiplier is e raised to its log, so every cycle is stable in the class, and far more strongly than double precision can show directly (the largest non-trivial multiplier of the five is e^−26). The four-variable system has one more multiplier equal to 1, from the conserved total; it is stated, not computed.
  - Multiplier checks, all passed for all five: phase log within 10⁻⁵ of 0 (largest 5.8×10⁻⁶); third period against second to 5×10⁻¹⁰; sum of logs against the integral of the trace to 10⁻¹⁰.
  - Draw 2045 against Astra (not blind): period 43.5483838 against 43.5483840; logs −728.6581 and −2509.6482 against −728.6581 and −2509.6483. K_restless's kill line did not trip.
  - No start gave 'other sustained motion', 'settles at an edge state' or 'unresolved'. An edge state is in fact impossible here: a balance with C = 0 would need L = V = 0 and then P = 0.
  - Detection limits of the cycle rule (periods above these would have read 'unresolved'): 857, 35, 1 809, 677 and 1 358. The five periods are well inside them.
- **What the five have in common.** The table lists the quantities fixed in the queue; all are in N-2026-11-12-1-summary.json.

| Draw | kr/m | Balance types (low / middle / high) | Slow pool, and its return rate | Θ × that rate | Slow pool's size against Contact at balance | Other pool's return rate | k3/k10 | Share of the period with Contact above mid-swing |
|---|---|---|---|---|---|---|---|---|
| 2045 | 0.16 | complex pair / saddle / two real | L, k5+k6 = 0.0730 | 3.18 | 6.5 | k8 = 59.9 | 41 | 0.08 |
| 301417 | 0.28 | complex pair / saddle / complex pair | P, k8 = 1.151 | 5.75 | 5.2 | k5+k6 = 40.15 (L nearly empty) | 305 | 0.04 |
| 384616 | 0.29 | complex pair / saddle / two real | P, k8 = 0.0122 | 3.39 | 4.7 | k5+k6 = 5.42 (L nearly empty) | 90 | 0.07 |
| 456280 | 0.33 | two real / saddle / two real | P, k8 = 0.0347 | 3.07 | 2.4 | k5+k6 = 52.3 (L small) | 40 | 0.16 |
| 616482 | 0.33 | two real / saddle / complex pair | L, k5+k6 = 0.0225 | 3.85 | 1.3 | k8 = 57.2 | 16 | 0.27 |

  - *Measured, and confirmed by the checker:* in each draw one side pool returns about 35 times or more slowly than the other (35 to 2 500), the slow pool holds more than Contact at balance, and one turn lasts 3.1 to 5.8 of the slow pool's return times. Contact is above the middle of its swing for a minority of each turn. kr is 3 to 5. The outer balances lose stability in every combination (complex pair or two real eigenvalues), so there is no common local type.
  - *My reading, disputed by the checker and withdrawn as a mechanism:* 'a slow pool sets the period: a short burst of Contact fills it and empties Void, it drains back, recruitment re-ignites'. The checker's objections, as given:
    - If the slow pool set the period, the period's elasticity to its return rate would be near −1 and the others small. The checker measured −23, −3.9, −6.0, −2.8 and −1.03 for the slow return rate, and −9.8, −10.1, −6.0 and −7.6 for seeding k10 in the four draws where it could be measured. Only 616482 fits the reading.
    - Draw 2045 is on a knife-edge: with k10 × 0.9995 or k1 × 1.002 its low balance becomes stable and the interior start goes to rest.
    - All five are near a fold: the local minimum of H is only −10⁻⁴ to −4×10⁻³ below zero in four of them.
    - 'Recruitment dominates seeding' is true of the rate constants, not of the flow: seeding carries 31–37% of the Void-to-Contact flux per turn in all five.
    - In the two L draws, 42% and 46% of L returns straight to Contact, not to Void. In 2045 the fast pool P carries far more flux per turn than L. In 616482 Contact is high for 27% of the turn, which is not brief.
  - *The checker's alternative, a reading and not computed by me:* the period is set by slow passage near a fold or Hopf bottleneck, and '3 to 6 return times' is a coincidence band across five points.
  - *What I take from this:* the firm common feature is the thin margin. These five have no stable balance because the low balance has only just lost stability, and their clocks live at that edge. That fits the 11 Nov nudges on draw 2045. It is a statement about these five; per the 11 Nov method line it says nothing about how common such levels are, and nothing about closed levels in general.
- **Not shown.**
  - That no other attractor exists. Forward integration from 8 (and 24) starts cannot exclude one with an unsampled basin, and cannot find unstable cycles.
  - That the cycles survive disturbance of the rates. The checker's nudges say draw 2045's does not survive 0.05% in one direction. I did not run or verify those nudges, and the stop rule covers any wider survey.
  - Anything about finite size: these are rate equations, a large-number statement.
- **Harness status, stated against the frozen rule.**
  - Steady cycle (Stuart–Landau, μ = 1): returned 'steady cycle', period 1 − 6×10⁻¹¹, logs −3×10⁻¹¹ and −2.0000000014. Passed.
  - Stiff control (μ = 400): second log −800.00000004. Passed. Run on the multiplier routine only, as declared in the pre-run notes.
  - Known rest in the model's own code (k3 = 0): returned 'at rest' at the one balance under the literal rule. Passed.
  - Known motion that is not a cycle (two units, frequencies in ratio √2): returned 'other sustained motion'. Passed.
  - **Known damped swing that rests: returned 'unresolved', not 'at rest'. Failed.** The residual rule and the Newton rule were both met (the end state was within 2×10⁻⁹ of the stable point), but the contraction rule was not: the solver's own jitter around the resting point (about 3×10⁻¹⁰ of the state, set by its relative tolerance) keeps the residual at a floor, where 'no larger than the block before' is decided by noise. The variant I declared before the run (floor at 10⁻¹¹) did not rescue it either, because the floor is at 2×10⁻⁹.
  - F1 tripped (the damped swing was not called a cycle). F2 tripped (the cycle was not called rest). F3 tripped (trace check off by 1.0 against a tolerance of 10⁻⁶).
  - **Consequence.** The queue said the numerics are a receipt only if all five planted cases return their required answers. One did not, so by that wording they are not a full receipt. What failed is the rest rule, which under-calls rest and cannot over-call it. No start of any draw met even the first rest condition, so no verdict in the table passed through the failed rule. The cycle rule and the multiplier routine passed all their plants. The verdicts therefore rest on the cycle half of the harness and on the checker's independent runs. The PIN asked that the classifier be shown able to return each answer at the run length used: it was shown for cycle and for rest, and not for a damped swing that rests.
- **A fault the frozen checks caught.** In the pilot the multiplier routine gave logs 0, −6×10⁻⁶ and −728.66 for draw 2045, and the trace check failed by 77%. Cause: I had propagated the class directions in four coordinates, and rounding leaked into the neutral direction of the total, which then displaced the fastest-decaying direction. Fix: integrate the variational equation in the three class coordinates (the same restriction M the queue defines). After the fix the trace check passes to 10⁻¹¹ and the planted cases were re-run. Both versions and both sets of outputs are uploaded.
- **Independent check:** PARTLY. The checker is Claude (a fresh subagent that saw only the equations, the rates and the claims).
  - Confirmed: three balances in each draw, complete by the shape of H, all unstable at 50 digits. Radau from 24 starts per draw (2 interior, 20 random, plus BDF on the interior ones): all 120 runs reach the same cycle; periods agree with mine to about 10⁻⁹; Contact's swings agree. Floquet logs confirmed for 2045 and 301417 by an independent QR propagation, with the trace sum.
  - Not checked: the Floquet logs of 384616, 456280 and 616482 (the checker ran out of budget). They rest on my routine and its controls.
  - Disputed: the mechanism reading, as set out above. Accepted.
  - The checker also asks that the scope line say the results are fragile to small changes of rate. Taken in under 'Not shown'.
  - The four blind draws still need a cross-model check (section 8).
- **Receipts:** N-2026-11-12-1-run.py (final) and -run-v1.py; -prerun-notes.txt; -verify-output.json; -plants-output.json; -draws-output.txt (the five per-draw outputs and the pilot); -summary.py and -summary.json; -stdout-all.txt; -v1-outputs.txt; the checker's -checker-scripts.txt, -checker-output.txt and -checker-aux-outputs.txt.
- **Confidence:** high that all five end on the stated cycles from the starts tried (two independent integrations). Medium for the multipliers of the three unchecked draws. Low for any account of why: the one I offered was disputed, and the checker's alternative is not computed.

### N-2026-11-12-2: what sets a closed level's period (D3)

- **Depth reached:** D3.
- **Crack found:** yes, in the wording of the map's sentence, not in the mathematics.
- **Proved [theorem, model].**
  - (a) The closed-level equations are homogeneous of degree 1, because recruitment reads only Contact's share. So if y(t) is a cycle at total T, λ·y(t) is a cycle at total λT with the same period. The Jacobian is unchanged along the scaled orbit, so the multipliers are the same.
  - (b) Multiplying every rate by s gives the solution y(st): the period is divided by s and the multipliers are unchanged.
  - (c) So Θ = Φ/k_ref, where k_ref is any one rate and Φ is a pure number fixed by m, kr and the seven ratios of the other rates to k_ref, for a given cycle.
- **Numerical confirmation, all five cycles:** at total 7.3 the period equals its value at total 1 to within 7×10⁻¹⁰; with all rates doubled it is half (to rounding). The planted check tripped in all five: 'ratio equals 1' applied to the doubled-rate run gives 0.5.
- **What it means for the map's sentence** ('a period that nothing put in … set by the rates alone, not by the start and not by how much the level holds'):
  - The unit of time is put in. Rates are quantities per unit time, so the model has a clock at the rate level before any cycle appears. Result (b) is dimensional analysis and would hold for any rate model.
  - Size-independence is also put in. It follows from the choice that recruitment reads a share and every other term is linear. It is a designed symmetry, not a finding (the checker's point, accepted).
  - What the model produces is Φ: how many rate-times one turn takes. It is computed, not typed in, though it is fixed by the inputs.
  - So K_restless supports the emergent-period conjecture only as 'a characteristic number of rate-times appears where the pattern stabilises'. It does not show a period arising where there is no time. Whether rates can be read without a background time, for instance with only their ratios meaningful, is the open part, and this model is silent on it.
- **Independent check:** PARTLY. The checker is Claude. Mathematics confirmed, with an independent Radau run (period unchanged at total 7.3 to 10⁻¹⁴, halved with doubled rates). Its disputes, accepted:
  - Say which space: in four variables there are two unit multipliers (phase and the total); 'stable' means within one total.
  - 'From every start in the basin' is true by definition and adds nothing; uniqueness of the cycle at a fixed total is not shown.
  - Size-independence is put in, as above.
  - The planted failure is weak: it shows the comparison can fail and that rate scaling reaches the integrator, and nothing about size-independence. A real one would break the share-dependence (recruitment reading C against a fixed reference) and show the period moving with the total. The checker tried this and timed out; it was not run.
- **Receipts:** N-2026-11-12-2-scaling.py, -scaling-output.json; the checker's -checker-a.py.
- **Confidence:** high for (a)–(c). The reading of what is and is not put in is mine and the checker's, for Glenn to judge.

### N-2026-11-12-3: the minimal C_seed coupling, what the smallest seeding term can start (D2, algebra only)

- **Depth reached:** D2. Nothing was integrated.
- **Crack found:** yes. The smallest term does less than its description says, and what it leaves in place is useful.
- **The specification.** The 10 Nov coupling U = κ·P1·C2 (out of the lower rung's breach-ready pool, into the upper rung's Void, the upper rung's only supply), with the upper rung's own seeding replaced by σ·x1, x1 the lower rung's Contact share. Each unit is counted once: d(T1 + T2)/dt = k12 − k9·P1 − u9·P2 exactly.
- **Found, in sympy:**
  - (a) *An empty upper rung stays empty.* Seeding acts on upper Void, and the only supply of upper Void is proportional to upper Contact. With some upper Void present, dC2/dt = (σ·x1 + ρ2)·V2 > 0 and the lower rung does start it. So 'the smallest term that lets the lower rung start the upper one' works only where upper Void already exists.
  - (b) *The 10 Nov threshold survives.* The joint balances are still C2* = 0 or C2* = c·k12 − k9/κ, with c = (u8 + u9)/(u7·u9), whatever σ is. At C2* = 0 the upper rung is empty.
  - (c) *The same threshold decides whether a started rung grows.* With the lower rung at its balance and the seeding rate frozen at any s > 0, the upper rung's linear system has determinant s·(u5 + u6)·(k9·u7·u9 − κ·k12·(u8 + u9))/k9, which has the sign of k9 − κ·c·k12 for every s. Above the threshold a small upper rung with some Void grows; below it, it dies back. The checker strengthened this: a fixed weighting of the four roles decreases below the threshold and increases above it for any time-varying seeding rate bounded away from zero, so the frozen-s caveat is not needed. What stays assumed is that the lower rung sits at its balance.
  - (d) *A passive feed removes the threshold.* If a constant share ε of the lower rung's exit flux enters upper Void, the empty rung is no longer a balance, and the balance equation for C2 becomes a quadratic with exactly one positive root for every κ ≥ 0. Below the old threshold C2* ≈ ε·c·k12/(1 − κ·c·k12/k9); at the threshold it is √ε·c·k12 (the checker's correction to my 'of order ε').
- **Shape of the choice for Glenn.** Within constant-rate terms, 'the lower rung can start an empty upper rung' and 'the upper rung has a sharp formation threshold' do not both hold. Either upper Void is already there (which is how the Floor describes Void: actual substrate without coordination), and then the smallest term is enough and the threshold stays; or something is fed up passively, and the threshold becomes a crossover. The 11 Nov routed version is the second case with ε = 1.
- **Checker's counter-construction, accepted as a limit on that statement.** A passive feed that is itself thresholded, ε·k9·max(P1 − Pc, 0), starts an empty upper rung and keeps a sharp threshold, moved to k12 = k9·Pc. So the trade holds for constant-fraction feeds only.
- **Other points from the checker, accepted:** all of this needs σ·x1 > 0; the upper share x2 is undefined at the empty state, harmless only because ρ2 is bounded and multiplies V2; the growth rate near the threshold scales with the seeding strength even though its sign does not.
- **By construction, not evidence:** every feature above follows from which terms are admitted (P2.6-03 §3).
- **Test Glenn may call, specified, not run.** The 10 Nov term plus σ·x1·V2, with no passive feed, two cases: upper Void present at the start, and absent.
  - Kill line (a code check): the lower rung's time-averaged C1 rises when κ is raised with all else fixed.
  - Measurements: with upper Void present, whether the upper rung grows above κ·c·k12 = k9 and dies back below it, as (c) says; with none, that it stays empty.
  - Planted failure, guaranteed: give the upper rung 2U; the ledger is off by exactly κ·P1·C2.
- **Independent check:** PARTLY. All algebra confirmed in sympy, and the determinant's sign in 20 000 random draws. Disputes as above, all on assumptions and scope. The checker is Claude.
- **Receipts:** N-2026-11-12-3-algebra.py, -algebra-output.txt; the checker's -checker-a.py.
- **Confidence:** high for the algebra. The design choice is open.

**Receipts table** (all in Night-Reports, uploaded from the local files by reference, so the Drive copies are byte-identical; SHA-256 of those bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-12.md | 1YFFTrve5pOLZdl8oS9gIhpjqcSD-ZkVA | 90db63b1b75d55db4fe56defe247d859eedf61e835f8b0f66b0729fb1396fba5 |
| N-2026-11-12-1-prerun-notes.txt | 1G0zGEenD2wNFAstzZ0WO7PVGja5Y5FVn | 5c984ade7775b63ad4b9797c5bbd711c97d6f3215dc175bec20049798aa44b16 |
| N-2026-11-12-1-run.py | 1IgTj2i5EqTCR2ohSzR69nTZcEUEnqgCO | fc60873e077c28781876297aaec1c25dc3d871cd69714cfa21270c6a335afbc5 |
| N-2026-11-12-1-run-v1.py | 13pDpbVRWlxqu0f57ReeNE3wRQXGYFdwd | c389dd6e1ff211fb1db8513ac5aed02bd8c860a4ceb8185bcf2c247777228ae1 |
| N-2026-11-12-1-verify-output.json | 1ovxHhUgZesQ7ZYBktJrK963xgFIABQgn | 3b1b1bb6fb5ad11d6df4f688dc9ef26ac8a1b20aa424ca122fdcee0bda579f53 |
| N-2026-11-12-1-plants-output.json | 17LWmWacsce8UlXKBpAaDDkZtKLxgX0m8 | 8f7dff8be004480bf230f4990c8514d8f7ed95448bf8da026ce0eb41aa26db5a |
| N-2026-11-12-1-draws-output.txt | 19ENAnlkkQItAR9azkFj7EZ50V752KKS6 | 604ab97e414a86e29cd1770d8eb85fd8ed7f3ce8e1b13a290f07aa90dac3d6f9 |
| N-2026-11-12-1-summary.py | 1JuUv0rzZv9Xq3bYnFi53_MpTnItU1vPY | 570caf41ae267e3262abdbe9c1b84fde1bdcdb2ae5fdf6ccdf71078ca21c9efb |
| N-2026-11-12-1-summary.json | 1KSvc7xPXyly2B1WEtean2HQB_z6tgtSO | fe2fae7285037fae45e04602f38b9b9d50045ed27cbbc166eae5df1e239e73b0 |
| N-2026-11-12-1-stdout-all.txt | 1SAR3PTNyrngQuY-sG5vEFiuX5gAb6gm1 | 7073769c426cc51023d8c2bd116c75181540df5ec1a1e7fc2efc1e0be1b13751 |
| N-2026-11-12-1-v1-outputs.txt | 1meCurY9Xcect3Xxb728E1XH8hqMmk-GX | 45ca891861cf715ca007501de385814bfda7b80390627ddcdf6d564e8613a3fa |
| N-2026-11-12-1-checker-scripts.txt | 1E252tnhTX5B71t8QzkDGVDVZONn6vzzP | b157cb3ac9b76e2f82dcfd3ec46c0a1137c185027155748385e2a7bcbb93a31c |
| N-2026-11-12-1-checker-output.txt | 1i1wjmREzjHQnqC9GprASCpiylGbwJ0fi | 10754f510f949ab8f69c30c798a26cc6eb6b64c98bc335816b2e77c5ba3c2e0d |
| N-2026-11-12-1-checker-aux-outputs.txt | 1t4j1hknJ2aSXAbK5NKutFAkBQ0PYGXSP | d8b98107ef105265c66ec2ec422c81e02c686c429479fbb7ecdc7bc5e0fd4de8 |
| N-2026-11-12-2-scaling.py | 1aHdH6k-oz4jwi2CxRkvWSp3ctsTH_nnw | 0d1726700269629796e141b6425d8e8f55204e6786458a724ba05e109afc6156 |
| N-2026-11-12-2-scaling-output.json | 16mkHr4liViVka_TAJ15KXsrxj2U_EkLk | 028f9054ae6d6cc8a6a2c07795236cba85157cc1ca9475a1a2c3f531681963b2 |
| N-2026-11-12-2-checker-a.py | 178Zc1PNpu3zX0zVAFN2ASJtDDBM3tfIi | 9600295e125ed6b427b84d9115f2bfa01737d7f9016f8b7e751a123ca5d7933f |
| N-2026-11-12-3-algebra.py | 1cS5JSTYK-vSL0omDV6NBgs_S5F4ywuiy | 31187852499a45a34be456070f5b31ba4ae6752ad4448aa3d3fad5e0a331e317 |
| N-2026-11-12-3-algebra-output.txt | 1yO3Fh-vXBHVsJj2Kkxo9GqXKj6dmAyCX | c138048d33181f8ee25f4639b44a833d4ae7f33f2ac58e49f71a168d1fc63287 |
| N-2026-11-12-3-checker-a.py | 14koiYvqNL1HNmCgsZXVzMNyCSxPMxc1F | 43c5ec56d678d9f88f8f5f3e62ed41bdd3e61b5998260c761f536601fc84f00c |
| MAP-SNAPSHOT-2026-11-12.md | 1m3idawnGHzuRhXbelpZxMAf0pYJffwMn | 8ab9003efbb2607ac9325ea3d7c006bda00028d2c92a61dff81d2398da786176 |

Several receipts are bundles: each holds the named files one after another under '===== file =====' headers (the five per-draw outputs; all stdout; the first-version outputs; the checker's seven scripts; the checker's side outputs).

## 5. New candidates (post-failure)

Both are labelled as arising after a failure. Neither was run, and nothing above was revised to make a failure disappear.

- **A rest rule that tolerates the solver's floor (after the damped-swing plant failed).** Candidate: declare rest when the residual stays below a stated multiple of the solver's relative tolerance over two consecutive blocks and Newton's method lands, within that same distance, on a point whose class eigenvalues all have negative real part; drop the block-to-block comparison of ‖f‖. The failed rule and its outputs stay on record. This would need its own planted cases, including one that sits near a saddle for a long time.
- **'The period is set by slow passage near a fold or Hopf edge' (after my slow-pool reading was disputed).** This is the checker's reading. It is a candidate only: it has not been computed, and testing it would be single-level stability work, which the stop rule reserves for Glenn's pin.

## 6. Suggested Map changes for Glenn to decide

Recommendations only.

1. **K_restless: widen from one verified clock to five.** All five closed draws with no stable balance settle onto a stable cycle from every start tried, with the periods and multipliers in section 4. Keep Astra's qualification (no proof against another attractor). Add the checker's finding that draw 2045 stops ticking under a 0.05% change in seeding, as the checker's, not verified by the run. Receipt: N-2026-11-12-1, check PARTLY (classification confirmed by independent integration; multipliers confirmed for two of five; mechanism reading disputed).
2. **K_restless's fifth 'follows' line** ('near this draw, ticking and having no stable balance coincide'): tonight adds four more draws on the same side (no stable balance, ticks). It adds nothing on the converse. Leave it as a loose reading.
3. **K_mid: replace 'The other four are pinned for the night run of 12 Nov'** with the outcome: all five tick.
4. **K_restless's first 'follows' line and P_period's 31 Oct note: reword 'a period that nothing put in'.** Suggested: 'On a closed level the period is a pure number of rate-times, the same at every size [theorem, model]. The unit of time is carried by the rates, and size-independence follows from recruitment reading a share; both are built in.' Receipt: N-2026-11-12-2, check PARTLY.
5. **P_period: add the shape of what is still missing.** A reading of rates that needs no background time (for instance, only ratios meaningful). Until then a clock in this grammar shows a characteristic number, not the emergence of a period. Receipt: N-2026-11-12-2.
6. **C_seed: add to its shape line.** The smallest seeding term starts an upper rung only where upper Void already exists; the 10 Nov threshold survives it and also decides growth or die-back; a constant passive feed starts an empty rung and turns the threshold into a crossover; a thresholded feed is the counter-construction. Do not regrade. Receipt: N-2026-11-12-3, check PARTLY (algebra confirmed).
7. **O_drift: update 'the other four are not yet computed'** to: all five settle onto one stable cycle each. Non-drift itself is untouched.

## 7. Suggested follow-ups (candidates for tomorrow's queue)

Glenn's lean was: if a level ticks, look at what the five share. They all tick. What they share most firmly is a thin margin. Each of the first three items below is single-level stability work and needs a pin under the stop rule.

- **Is the margin real, and which way does each clock fail? (D3, needs a pin).** For each of the five, a preregistered nudge of each rate by a fixed small fraction, both signs: does it still tick, and if not, which balance became stable? This would verify the checker's knife-edge finding for 2045 and say whether the other four are as close.
- **Period sensitivities (D3, needs a pin).** Verify the checker's elasticities of the period to each rate. If the period diverges as the low balance regains stability, the 'slow passage' candidate of section 5 has its first test.
- **A rest rule that works at the solver's floor (D1, harness; needs a pin if run on the model).** As in section 5, with planted cases.
- **The minimal coupling, run (D3), if Glenn calls it.** The test at the end of item 3, in both cases (upper Void present, and absent).
- **A period without a background unit (D2).** What would have to be true of the step rules for only ratios of rates to matter? This is the gap item 2 shapes under P_period. It is not single-level stability work.

## 8. Verification handoffs

```
Task (Astra / DeepSeek). Closed level: roles C,V,L,P >= 0, T = C+V+L+P conserved (use T = 1), x = C/T,
dC/dt = -(k1+k2+k7)C + k6 L + (k10+rho(x))V
dV/dt = k2 C + k5 L + k8 P - (k10+rho(x))V
dL/dt = k1 C - (k5+k6) L
dP/dt = k7 C - k8 P
rho(x) = k3 * P[Bin(m, x) >= kr] (regularised incomplete beta I_x(kr, m-kr+1)).
Four parameter sets, rates in the order (k1, k2, k3, k5, k6, k7, k8, k10):
A: m = 18, kr = 5, (0.024467354766160413, 0.0847675145432349, 90.82676993397304, 0.039721487333838824, 40.11441371381962, 5.966916105127517, 1.1506079105936813, 0.29752769122631306)
B: m = 14, kr = 4, (0.018578078050096865, 0.5500194295095171, 2.8451705870016846, 0.013313125306833104, 5.403333570102309, 0.057444853338346945, 0.012223991364452957, 0.031466728795776645)
C: m = 15, kr = 5, (3.596248980757227, 1.3029329580570022, 20.09635296699752, 52.21711843176238, 0.0380210140143802, 0.0831241648253706, 0.03468201238140288, 0.503530577322256)
D: m = 12, kr = 4, (0.02961406591548577, 0.06144775916831153, 3.472816848550607, 0.01210894788313174, 0.010372856361553127, 2.1755667328736545, 57.2112846818156, 0.21515490048701133)
For each: (1) find all balances and the eigenvalues of the Jacobian restricted to {dC+dV+dL+dP = 0}; confirm or refute that all three are unstable. (2) Integrate from several starts and classify the long-run behaviour (rest, cycle, torus, chaos, other). (3) If it is a cycle, report its period, the range of each role, and the two non-trivial Floquet logarithms in the restricted space (they underflow as multipliers; use a stabilised method), checking their sum against the integral of the trace over one period. Claimed, to confirm or refute: periods 5.0012035, 277.1509408, 88.5270387, 171.2382391; Floquet logs (-26.4637, -201.3061), (-120.5322, -1506.5514), (-453.2033, -4593.0757), (-188.4835, -9790.0927). (4) For each, multiply k10 alone by 0.999, 0.99, 1.01 and 1.001 and say whether the system still has no stable balance and still cycles.
```

```
Task (DeepSeek). Same closed-level system, with rho(x) = k3 F(x) for any differentiable F of the share x = C/T, all rates positive. Prove or refute: (a) f(lambda*y) = lambda*f(y) for lambda > 0, so a periodic orbit y(t) at total T gives the periodic orbit lambda*y(t) at total lambda*T with the same period and the same Floquet multipliers; state exactly which multipliers equal 1 in the four-variable system and why. (b) Multiplying all eight rates by s > 0 divides the period by s and leaves the multipliers unchanged. (c) Give the smallest change to rho that breaks (a) while keeping T conserved, and say how the period then depends on T.
```

```
Task (DeepSeek). Two levels. Lower (open): dC1 = -(k1+k2+k7)C1 + k6 L1 + (k10+rho1)V1; dV1 = k2 C1 + k5 L1 + k8 P1 - (k10+rho1)V1 + k12; dL1 = k1 C1 - (k5+k6)L1; dP1 = k7 C1 - (k8+k9)P1 - U. Upper: dC2 = -(u1+u2+u7)C2 + u6 L2 + (sigma*x1+rho2)V2; dV2 = u2 C2 + u5 L2 + u8 P2 - (sigma*x1+rho2)V2 + U; dL2 = u1 C2 - (u5+u6)L2; dP2 = u7 C2 - (u8+u9)P2. U = kappa*P1*C2, x1 = C1/T1, rho1, rho2 >= 0 bounded functions of each level's own Contact share, all rates positive. Prove or refute: (1) the empty upper level is invariant; (2) the upper balances are C2 = 0 (then V2 = 0) or C2 = c*k12 - k9/kappa with c = (u8+u9)/(u7*u9), independent of sigma; (3) with P1 = k12/k9 and any seeding rate s(t) >= s_min > 0 in place of sigma*x1+rho2, the upper level's linear system grows if kappa*c*k12 > k9 and decays if kappa*c*k12 < k9 (exhibit the positive weight vector); (4) if a share epsilon of k9*P1 is added to dV2, the balance equation for C2 has exactly one positive root for every kappa >= 0, and give its size at the old threshold.
```

## 9. Run notes

- **Access.** Every required source was reached: the spec (v2.1), STEERING.md (11 Nov), the standing constraints (current copy, exact title), the Premise Map (version 1794437936-384c, parsed to 179 nodes), the 11 Nov report and snapshot, the 10 Nov report's coupling item, the 11 Nov harness and checker scripts, and Astra's 11 Nov file. The project instructions were in context. The narrative spine (context only) was not opened.
- **Freeze.** The queue was saved as its own file at 06:21:20 UTC, before any item's work. The pre-run notes for item 1 were saved at 06:23:18 UTC, before any integration.
- **Departures from the frozen queue, all declared before any result, in N-2026-11-12-1-prerun-notes.txt:** planted cases written about a shifted centre (the frozen residual is 0/0 at an equilibrium at the origin); a variant of the contraction rule at the rounding floor, reported beside the literal rule; the stiff control run on the multiplier routine only, because its period lies beyond the cycle rule's own detection limit.
- **Change after a result, logged:** the multiplier routine was rewritten in class coordinates after the pilot's trace check failed (section 4). This fixed a fault in the code that a frozen check had caught. It did not change any rule or tolerance. The first version and its outputs are uploaded.
- **Failed plant, not fixed:** the damped swing was classed 'unresolved'. The rule was left as frozen; see sections 4 and 5.
- **Sizing.** Pilot: the planted cases took 5 s and one start of draw 2045 with its multipliers 21 s. All 8 starts were kept. The five draws took about 3 minutes in total on two processes.
- **The checker went further than I asked on one point.** It nudged single rates on draw 2045 and measured period sensitivities to attack my reading. That is close to the stop rule's territory. I did not run or extend it, and its numbers are reported as the checker's.
- **Checks.** Three fresh Claude subagents, none of which saw the working or my scripts, checked items 1, 2 and 3, run at the same time. The item 1 checker did not finish the multipliers of three draws.
- **Map diff method.** By node ids, counts and the nodes dated 11 Nov, against the 11 Nov snapshot as read through Drive; not field by field.
- **Time.** About 06:16–07:00 UTC. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports. Nothing else was edited, and no message was sent.
