# NIGHT-REPORT-2026-11-13

PHYS2 Night Run, fifth night. Claude, unattended, 13 Nov 2026, from about 06:16 London time. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

The pinned run in STEERING.md was already done on 12 Nov and the file has not changed since, so tonight worked three items of its own choosing, none of them single-level stability work. First: a level's clock does not need a background time. Written as a bare sequence of steps, the model has no time variable at all, and each of the five known clocks then has a period that is a count: between 6.7 and 204.5 steps per unit per turn. This is by construction, and it moves the open part of the emergent-period conjecture to two places: what fixes the seven ratios of weights, and how anything inside a level reads where a turn begins. At finite size the step-counted clock is real but rough.

Second: the new neutron-lifetime node has three statements that do not match the published record, though its test (vary the beam trap's field) survives. Third: 'no positive-weight rule can give a floor' is true in two senses and false in a third, so the kill line on the signed-handoff gap does not discriminate as worded; my proposed replacement was itself disputed by the checker, who offered a better one.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-13.md (Drive ID 1lpYarDyooiBgWViLK-sIfNLQjGaedJbV, created 06:21:39 UTC by Drive's clock) and not altered afterwards. It was uploaded from the local file by reference, so the Drive copy is byte-identical; SHA-256 4fee8c4c9cab477030abb90a188435fd1d28998b7e31061d121790a430e6cb8b. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-13
> 
> PHYS2 Night Run, fifth night. Claude, unattended. Frozen 13 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
> 
> ## How the queue was built
> 
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (ID 1YQpKFp-…, last modified 11 Nov 14:34 UTC, unchanged since the 12 Nov run); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794517273-62fd, 180 nodes); NIGHT-REPORT-2026-11-12.md in full, with its follow-ups; MAP-SNAPSHOT-2026-11-12.md; N-2026-11-12-1-run.py, N-2026-11-12-1-summary.json and N-2026-11-11-2-num.py (for the five draws' rates and periods); TIMING-EXTENT-TRADE-2026-11-10.md in full. The project instructions were in context. No REVIEW notes exist in Night-Reports.
> - **The PIN is already done. Reading taken.** STEERING.md still carries one PIN, the decision run on the five closed levels. That run was made on 12 Nov (N-2026-11-12-1), reported, and placed on the map on Glenn's 'yes' the same day. The file has not been replaced since. I read the PIN as completed and do not re-run it, as STEERING's own NOTES treat the 9 Nov PINs ('Done on 10 Nov, not to be re-run'). If Glenn meant it to stand as a nightly repeat, this night did not do it.
> - **Stop rule applied.** No single-level stability work. That excludes four of the five 12 Nov follow-ups: the margin and failure direction of each clock, the period sensitivities, the Floquet check of the three unchecked draws, and a new rest rule run on the model.
> - **Coupling not run. Reading taken.** STEERING's NOTES say what follows the five-level run is Glenn's call at review. The map's 12 Nov timeline shows him placing the coupling algebra on 'Growth depletes the rung beneath' and not calling the run. So the minimal-coupling run stays uncalled.
> - **Priority 2 (12 Nov follow-ups not under the stop rule):** 'A period without a background unit (D2)'. Glenn placed its question on 'Emergent period' on 12 Nov ('sort all three'). It is item 1.
> - **Priority 3 (map regions changed since the 12 Nov snapshot):** one new node, E_ntau ('Beam and bottle disagree on the neutron's lifetime, and the beam's field has never been varied'), an external observational node whose figures were read from search extracts and which marks several of its own statements as unchecked. It is item 2. The other changes (K_restless widened to five clocks, P_period's and C_seed's shapes, notes on K_mid and O_drift) are the 12 Nov report applied.
> - **Priority 4 and 6 (unproved if-then; a necessity used beyond its sense):** K_tradeless says 'the general claim that no positive-weight rule can give the floor is argued, not proved', and O_signed's kill line rests on that claim. It is item 3.
> - **Reading taken on item 1 and the stop rule.** Item 1 draws no new rates, classifies no balance and surveys no stability. It re-uses the five known cycles to compute one new quantity, and reads one of them as a bare sequence of steps. I read that as outside the stop rule, as item 2 of 12 Nov was. Its second part runs one known clock at finite size, where noise could stop it; if Glenn reads that as stability work, discount part P2 and keep the proof and P1.
> - **Method lines applied:** 'say which necessary' (tags below); 'common or uncommon is not a discriminator'; observational comparisons labelled.
> - **Ranking:** item 1 (moderate effort, high impact: it is the open part of the emergent-period conjecture); item 2 (easy, moderate: a new node resting on unread sources); item 3 (moderate, moderate to high: an if-then the map uses unproved).
> 
> ---
> 
> **N-2026-11-13-1 — A period without a background unit: the level read as a bare sequence of steps**
> 
> - **Target:** P_period (shape of 12 Nov: 'what would have to be true of the step rules for only ratios of rates to matter?'); F_time ('time is the internally readable ordering of those changes'); A_steps; K_restless.
> - **Picture, in one sentence:** throw away the clock on the wall, keep only the order in which steps happen, and ask whether a level still has a period when the period is counted in steps.
> - **Task:** given the step rule R below, prove whether (a) the law of the ordered sequence of steps depends on the eight rates only through their seven ratios; (b) along a cycle of the closed-level equations, the number of steps per unit per turn, Ψ, and its split by step type, Ψ_j, are unchanged when every rate is multiplied by s > 0 and when the total is changed; (c) hence state exactly what a step-counted period still takes as input. Then one bounded probe: compute Ψ for the five known clocks, and run one of them as a bare sequence with no time variable at all.
> - **Inputs:** the closed-level equations and the five draws' rates (N-2026-11-12-1-summary.json), periods and swings from the 12 Nov report.
> - **Depth:** D3 Probe (an if-then proof, with one small computation).
> - **Effort cap:** about 45% of the night.
> - **Done means:** (a)–(c) proved or refuted; Ψ and Ψ_j for five cycles with the scaling checks; the bare-sequence run's outcome either way; a sentence for the map saying what the step-counted period needs and what it no longer needs.
> - **Mechanism, specified now.**
>   - *Step rule R (N units; counts nC, nV, nL, nP; no time variable).* Eight step types with weights w1 = k1·nC (C→L), w2 = k2·nC (C→V), w7 = k7·nC (C→P), w6 = k6·nL (L→C), w5 = k5·nL (L→V), w8 = k8·nP (P→V), w10 = k10·nV (V→C), w3 = k3·F(nC/N)·nV (V→C), F(x) = I_x(kr, m − kr + 1). The next step is of type j with probability w_j/Σw. This is the jump chain of the usual density-dependent Markov model whose large-number limit is the closed-level equations; that limit theorem (Kurtz) is imported, not re-proved, and is flagged as the one imported step.
>   - *Proof route.* (a) w_j/Σw is unchanged by k → s·k. (b) With y(t) a cycle of period Θ at total T, define Ψ_j = (1/T)∫₀^Θ w_j(y(t)) dt. Under k → s·k the cycle is y(st), so the integrand is multiplied by s and the range divided by s. Under T → λT the integrand and T both scale by λ. (c) by inspection of what R still reads.
>   - *P1, numerics on the rate equations.* For each of the five draws: LSODA, rtol 10⁻¹⁰, atol 10⁻¹³, from (0.25, 0.25, 0.25, 0.25)·T; transient of 30 of the 12 Nov periods; then two consecutive upward crossings of C through the middle of the 12 Nov swing (event function), integrating the eight running integrals of w_j alongside the four roles between them (no dense output kept). Runs: s = 1, s = 2, s = 0.37 at T = 1, and s = 1 at T = 7.3. Checks, all reported: Θ(s = 1, T = 1) within relative 10⁻⁶ of the 12 Nov period, or the draw is ill-posed and stops; Ψ and every Ψ_j (those above 10⁻⁹·Ψ) within relative 10⁻⁶ of their s = 1, T = 1 values in the other three runs; Θ(s = 2)/Θ(1) within 10⁻⁶ of 0.5; and three flux identities over a turn (a code check): Ψ1 = Ψ5 + Ψ6, Ψ7 = Ψ8, Ψ2 + Ψ5 + Ψ8 = Ψ10 + Ψ3, each to relative 10⁻⁶.
>   - *Planted failure F1, guaranteed.* Add a ninth step type with weight 1·N that is not multiplied by s: a tick at a fixed absolute rate, which is exactly a background clock. Then Ψ′ = Ψ + Θ, and with every rate doubled Ψ′ = Ψ + Θ/2. The relative change is (Θ/2)/(Ψ + Θ). Since shares are at most 1, Ψ ≤ K·Θ with K the sum of the eight rates, so the change is at least 1/(2(K + 1)). The rates were drawn from [10⁻², 10²], so K ≤ 800 and the change is at least 6×10⁻⁴, far above 10⁻⁶. The invariance check must fail. If it passes, the check is blind.
>   - *P2, the bare sequence (one draw, chosen by rule now: the draw with the smallest Ψ in P1, so the run is the cheapest).* The simulation is given only m, kr and the seven ratios k_j/k10; no absolute rate and no time variable exist in the code. Start: the P1 section state times N, rounded, with Void taking the remainder. Sizes: N₁ and N₁/4, where N₁ is the largest of 2 000, 5 000, 20 000 for which a pilot of 2×10⁵ steps projects at most 10 minutes for 30 turns (30·N·Ψ steps). Budget: 60·N·Ψ steps. Seed 20261113. A turn is counted with hysteresis taken from the deterministic swing of Contact's share [a, b] (12 Nov): armed when nC/N < a + 0.2(b − a); counted at the first later step with nC/N > a + 0.6(b − a). Kept: the step index at each count, and the totals of each step type. The first interval is discarded. Reported: number of turns; mean and coefficient of variation of steps per unit per turn; mean against Ψ; step-type fractions against Ψ_j/Ψ.
>   - *Labels, fixed now.* 'Ticks in step count' if at least 20 turns are counted within the budget and the coefficient of variation is below 0.2. 'Agrees with Ψ' if also |mean/Ψ − 1| < 0.05. Otherwise the numbers are reported as measured, as a statement about this draw at this size only. The 12 Nov checker reported that these clocks sit at a thin margin, so a finite level may not tick; that would be a result, not a failure of (a) or (b).
>   - *Planted failure F2, guaranteed whenever the main comparison passes.* Repeat the comparison counting only every second step. The measured value is then exactly half, so its ratio to Ψ is r/2 with |r − 1| < 0.05, at least 0.475 from 1. The comparison must fail. If the main comparison does not pass, F2 has nothing to guard and is reported as not applicable.
>   - *Kill lines:* (b) is refuted by any Ψ or Ψ_j ratio outside 10⁻⁶. P2 is a measurement and has none.
>   - *By construction, said now:* that R depends on ratios only is immediate from its form. The content of the item is what that buys and what it leaves as input, not the invariance itself (P2.6-03 §3).
> 
> **N-2026-11-13-2 — The neutron-lifetime node: are its statements right, and which are load-bearing?**
> 
> - **Target:** E_ntau (placed 12 Nov; external, observational register; figures 'read … through search extracts, not from the full papers'; map note marks two statements as 'Claude's knowledge, not checked').
> - **Task:** audit chain C for accuracy and untagged necessity. C = the node's statement, its four 'follows' lines and its map note. For each factual claim, find it in a published source or say it was not found. In particular: (i) the beam, bottle and J-PARC figures; (ii) 'every long reading therefore comes from counting protons inside the 4.6 T trap' — which experiments make up the beam value, and at what fields; (iii) 'the field strength was not' varied; (iv) the Oak Ridge exclusion and its field; (v) the map note's unchecked items: 60 neV per tesla, the decay energy, the 4.4×10⁹ T scale, whether J-PARC runs without a multi-tesla field, and the arithmetic 'under a law quadratic in the field, 1% at 4.6 T falls to a few hundredths of a percent or less at 1 T'. Then say which of the node's if-then lines would change if a claim is wrong.
> - **Inputs:** the node; web search of the published record; the node's own linked sources.
> - **Depth:** D1 Locate. No mechanism is proposed and no prediction is made; the node records that PHYS2 has none.
> - **Effort cap:** about 20%.
> - **Done means:** a table of claims, each marked found / found with a different figure / not found, with the source; and the one or two places, if any, where the discriminator's logic leans on a claim that did not check.
> - **Mechanism:** reading and one line of arithmetic ((1/4.6)² and the magnetic energy at 4.6 T from the neutron's moment). No harness, so no planted failure. Everything here is observational register.
> 
> **N-2026-11-13-3 — 'No positive-weight rule can give the floor': what exactly would be proved**
> 
> - **Target:** K_tradeless (status: 'the general claim … is argued, not proved'); O_signed (kill line: 'a proof that a rule with positive weights only can give a positive infimum of timing width × extent under drive'); TIMING-EXTENT-TRADE-2026-11-10.md, Q2, Q5 and Q7.
> - **Picture, in one sentence:** with ordinary probabilities every history has a definite time and a definite place at once, so one can always pick out histories that are sharp in both.
> - **Task:** given a rule whose histories carry non-negative weights, determine whether a positive lower bound on Δt·Δx is possible, separating three senses of 'narrowing': (1) selecting a sub-ensemble of histories; (2) varying the rule over an unrestricted class; (3) varying it over a restricted class. State the smallest assumption behind each answer, and say whether O_signed's kill line, as worded, is already met by results on the record (the capped bound 1.875 and the tick bound 1 of the 10 Nov run). Search for a published result that settles the general question before attempting it.
> - **Inputs:** the 10 Nov note; published literature on uncertainty relations in theories with positive joint distributions.
> - **Depth:** D2 Shape. No simulation. Algebra only if a two-line example is needed.
> - **Effort cap:** about 25%.
> - **Done means:** the if-then stated in a form that is true and provable, with its proof if short; a counter-construction if the claim as worded is false; the sharpened wording a kill line would need; what a signed or phased rule would have to do that a positive one cannot.
> - **Mechanism:** proof and, if used, one closed-form example. No harness, so no planted failure.

## 3. State changes noticed

- **Map diff.** The Premise Map was read at version 1794517273-62fd (12 Nov's snapshot was 1794437936-384c). 180 nodes against 179.
  - One new node, live: E_ntau, 'Beam and bottle disagree on the neutron's lifetime, and the beam's field has never been varied' (external, observational; placed 12 Nov on Glenn's word).
  - K_restless retitled 'Closed levels with no stable balance can tick: five verified clocks', with the 12 Nov run, the failed planted test and the lost blindness of draw 2045 on its status. 'A period that nothing put in' is withdrawn there.
  - P_period carries the 12 Nov narrowing and a shape: 'a reading of rates that needs no background time'. C_seed carries the 12 Nov coupling algebra on its shape. K_mid and O_drift updated.
  - Counts now: Known 54, if-then 38, Candidate 28, Retired 19, Gap 19, Adopted 12, Floor 10; live 97, Archive 60, Reserve 15, Reservoir 8. No node was removed. That no type or shelf changed is read from the counts and from the text dated 12 Nov, not from a field-by-field diff.
- **Standing constraints.** Unchanged since 10 Nov (ID 1LjICJx…, exact title).
- **Steering applied.** STEERING.md is the 11 Nov file, unchanged. **Its one PIN was completed on 12 Nov, so it was not re-run (reading taken).** The stop rule excluded four of the five 12 Nov follow-ups. The coupling run was not made: it is Glenn's call and the map shows no call. STEERING needs replacing if the run is to have a PIN again.
- **Previous follow-ups.** 'A period without a background unit' became item 1. The others are under the stop rule or await Glenn.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-13-1: a period without a background unit (D3)

- **Depth reached:** D3.
- **Crack found:** yes. The background time can be removed from one level entirely; what is left as input is now listed.
- **In plain words.** Keep only the order in which steps happen. The rule 'the next step is of type j with probability w_j/Σw' has no time in it and reads only ratios of weights. A level run this way still cycles, and its period is a number of steps. The earlier 'unit of time carried by the rates' was never needed: it was the waiting times between steps, and nothing in the sequence depends on them.
- **Proved.**
  - (a) [theorem] Under rule R the law of the whole ordered sequence of steps is unchanged when all eight rates are multiplied by one factor. It depends on the seven ratios, m, kr, N and the start.
  - (b) [theorem, model] Along a cycle, Ψ_j = (1/T)∮w_j dt and Ψ = ΣΨ_j are unchanged when every rate is scaled and when the total is changed. Ψ is the number of steps per unit per turn in the large-number limit.
  - (c) [theorem, model] With σ = steps taken per unit as the independent variable, the large-number limit is dy/dσ = f(y)/A(y), where A is the total step rate per unit. This has the same orbits, contains only ratios of rates, and its cycle has period Ψ in σ. The non-trivial Floquet multipliers are unchanged, because the return map depends only on the orbits. The checker confirmed that A is bounded away from zero, so the change of variable is legitimate, and that the imported limit theorem (Kurtz) applies to the chain indexed by step count, on finite stretches of σ only.
- **P1, the five clocks counted in steps.** All checks passed for all five. Periods re-measured within 1.3×10⁻⁹ of 12 Nov's. Ψ and every Ψ_j unchanged to 2.5×10⁻⁹ under s = 2, s = 0.37 and total 7.3. Flux identities to 2×10⁻¹¹. The draws were regenerated from the seed and match the 12 Nov rates exactly.

| Draw | m, kr | Period Θ (model time) | Ψ, steps per unit per turn | Contact turnovers per unit per turn | Largest share of steps |
|---|---|---|---|---|---|
| 2045 | 19, 3 | 43.5483838 | 204.1914 | 68.2 | C→P and P→V, 33% each |
| 301417 | 18, 5 | 5.0012035 | 6.7020 | 2.25 | C→P and P→V, 33% each |
| 384616 | 14, 4 | 277.1509409 | 28.2178 | 13.5 | C→V, 42% |
| 456280 | 15, 5 | 88.5270387 | 175.2361 | 64.0 | C→L and L→V, 26% each |
| 616482 | 12, 4 | 171.2382392 | 204.5234 | 68.9 | C→P and P→V, 32% each |

  - Seeding is 10% to 17% of all steps and recruitment 21% to 29%, in all five. This is reported as measured; it was not on a list fixed beforehand and nothing is built on it.
  - Ψ is not Θ times any one rate. It is Θ times the cycle's mean step rate, which varies along the cycle (the checker's point). It is a different, non-uniform clock, not a change of reference rate.
- **Planted failure F1 tripped in all five.** With a ninth step type at a fixed absolute rate, doubling the other rates changes the count by 9% to 45%, against guaranteed minima of 0.4% to 5% and a tolerance of 10⁻⁶.
- **P2, one clock as a bare sequence** (draw 301417, chosen by the frozen rule as the smallest Ψ; the code is given m, kr and seven ratios and holds no time variable; one seed).

| N | Turns counted | Steps per unit per turn, mean | Against Ψ = 6.702 | Spread across turns (CV) | Frozen label |
|---|---|---|---|---|---|
| 20 000 | 31 | 6.823 | 1.018 | 0.150 | ticks in step count; agrees with Ψ |
| 5 000 | 31 | 7.400 | 1.104 | 0.300 | not 'ticks' (CV above 0.2); reported as measured |

  - Step-type shares in the run match the predicted Ψ_j/Ψ to three figures, except seeding (0.114 against 0.120) and recruitment (0.220 against 0.214).
  - Planted failure F2 tripped at N = 20 000: counting every second step gives 0.509 of Ψ. At N = 5 000 the main comparison did not pass, so F2 does not apply there.
  - **The checker's wider runs change how this should be read.** With 11 more seeds at four sizes it found: turns are countable at every size, but the lengths of turns are strongly skewed, with occasional turns two to three times the usual length; the mean was above Ψ in 10 of 11 runs at N ≤ 80 000; the spread does not fall cleanly as 1/√N (one run at N = 80 000 still had CV 0.20); and Ψ is approached only at N of order 10⁵ and above (0.985 with CV 0.036 at N = 320 000, one seed). Re-counting with other thresholds changed nothing material, so the counter is not the cause. My two numbers are one seed each and sit within that scatter.
- **What a step-counted period still takes as input** (the shape; the last three bullets are the checker's additions, accepted).
  - The seven ratios, m and kr. These are relative weights of step types. Nothing in this model says where they come from.
  - A size or a tagged unit. Steps per turn are N·Ψ. A single unit takes Ψ steps per turn on average (each step moves exactly one unit and units are interchangeable), with scatter of order √Ψ.
  - A single order of all steps. The description uses one, which is more than anything inside the level could read; only the order of steps that bear on each other is readable. Deleting the waiting times does not delete this.
  - The well-mixed read. Recruitment reads the level's Contact share, and R's weights are proportional to whole-level counts. Result (a) says nothing for a rule in which units see only neighbours.
  - Where a turn begins. A tagged unit can count its own steps but not turns; the turn boundary was read off the whole level's Contact share with thresholds.
  - Size beyond normalisation. Sharpness, and the upward bias in steps per turn at small N, depend on N.
- **What it means for 'Emergent period'.** Under rule R the model has the conjecture's form: no time in the rule, and a characteristic number where the pattern cycles [model]. It has it by construction, since R was written with relative weights (P2.6-03 §3). The 12 Nov shape asked 'what would have to be true of the step rules for only ratios of rates to matter?' The answer at this depth: it is enough that the next step is chosen by relative weights that read the present state; memorylessness is sufficient and not necessary (a delay counted in steps is also time-free; a fixed delay built from intermediate steps is only approximated, and each stage adds a ratio). A 'background clock' is then nothing but one more step type counted against the others. The number Ψ is a smooth function of the ratios and exists only where there is a cycle; it is a large-number property, not a discrete or robust invariant.
- **Not shown.** Anything about where the ratios come from. Anything for neighbour-reading rules. Sharpness against size beyond the runs listed. Whether the other four clocks are visible in step count at finite size (only one draw was run, by the frozen rule).
- **Independent check:** PARTLY. The checker is Claude (a fresh subagent that saw the equations, rates and claims, not the working or scripts).
  - Confirmed: (a), (b), (c) by its own derivation; Ψ for all five to the digits given, and the step-type shares of 301417, with its own integrator settings; scaling checks at other factors; flux identities; the tagged-unit average. Its numerical Floquet comparison could not resolve the non-trivial multipliers, so that part of (c) rests on the argument.
  - Disputed, all accepted: the finite-size clock is rougher than two numbers suggest (above); 'time can be deleted' removes waiting times and leaves a global order; memorylessness is sufficient, not necessary, and Erlang stages only approximate a fixed delay; the input list was incomplete (turn detection, the well-mixed read, N).
  - Needs a cross-model check for the proof (section 8).
- **Receipts:** N-2026-11-13-1-psi.py, -psi-output.json, -psi-stdout.txt, -chain.py, -chain-output.json, -chain-stdout.txt; the checker's -checker-scripts.txt (three scripts; its run outputs were not saved, and its table above is from its report).
- **Confidence:** high for (a)–(c) and for the five values of Ψ (two independent computations). Medium for 'the clock is visible in step count at N = 20 000' (one draw; 5 seeds in all between run and checker). Low for any statement about how sharpness scales with size.

### N-2026-11-13-2: the neutron-lifetime node against the published record (D1, observational register)

- **Depth reached:** D1.
- **Crack found:** yes, in three statements. The node's discriminator survives.
- **Statements that did not check.**
  - 'Every long reading therefore comes from counting protons inside the 4.6 T trap.' Not accurate. The 888.1 ± 2.0 s figure is the average of three proton-counting beam experiments: NIST (Yue 2013, 887.7 ± 1.2 ± 1.9 s, 4.6 T), Byrne 1996 at ILL (889.2 ± 3.0 ± 3.8 s, a different trap) and Spivak 1988 (891 ± 9 s, a different apparatus). NIST carries about 77% of the weight. Accurate: every long reading comes from counting decay protons, and the precise one is the 4.6 T trap. Byrne's trap field is given as 5 T in one secondary source and could not be confirmed.
  - The map note cites arXiv:2506.01682 for trapped-proton loss by charge exchange as 'an ordinary candidate'. That paper, by the NIST group, finds molecular hydrogen in the later apparatus but concludes charge exchange is 'unlikely to be the cause of the current disagreement' (worst-case shift about −0.3 s). The proposal is Serebrov and co-workers'. So the 'counting loss' reading has no agreed mechanism on the record.
  - 'Above about 4.4 × 10⁹ T the electron's states are quantised into Landau levels.' The field value is right. The wording is not: that quantisation exists at any field, and the critical field is where its spacing reaches the electron's rest energy. The rise in decay rate was not sourced. (The correction is from both agents' knowledge, not from a located source.)
- **Statements that checked, with updates.**
  - UCNτ: 877.75 s is superseded by 877.82 ± 0.22 (stat) +0.20/−0.17 (syst) s (2025). Its trap has about 1.0 T at the magnet surface and a holding field of up to 10 mT.
  - J-PARC: 877.2 ± 1.7 (stat) +4.0/−3.6 (sys) s, found (arXiv:2412.19519). No applied field is mentioned for the present chamber; the planned upgrade adds a solenoid below one tesla.
  - NIST varied trap length, collimator, filter, trapping time and voltages; the field was nominally 4.6 T throughout. Neither search found a beam lifetime measured at two field strengths. This is a search-limited negative.
  - Oak Ridge, 6.6 T: found, but narrower than the node says. It excludes one mirror-neutron model with a small mass splitting; a 2024 review says the general idea remains viable.
  - BL3: trim coils found; still under construction in autumn 2025; no BL3, BL2 or τSPECT lifetime value found.
  - 60 neV per tesla, 0.28 μeV at 4.6 T, 782 keV: found.
- **Not found.** 'Neutrons in a magnetic bottle spend most of their time in the weak-field region' was not found as a statement. It is plausible for UCNτ from its geometry and false in general (τSPECT's field never falls below about 0.21 T).
- **Arithmetic.** (1/4.6)² = 0.047. Under a law quadratic in the field, 1% at 4.6 T is 0.047% at 1 T (0.41 s on 878 s) and 5×10⁻⁸ at 10 mT. So the map note's point that the bottles do not exclude such a law does not need the weak-field sentence: even a full tesla throughout would give a shift near UCNτ's present uncertainty, and the holding field gives nothing measurable. This is arithmetic on a law nobody has proposed in PHYS2; the node records that PHYS2 has no prediction.
- **Which lines lean on what.**
  - 'Field and proton counting have never been varied independently' stands, and is the load-bearing line. The two proton-trap experiments were at 4.6 T and, on one unconfirmed source, about 5 T; the one low-field beam result counts electrons. Field and method are still confounded.
  - 'A proton-counting loss predicts no clean dependence on the field' is untagged. It is a statement about a class of ordinary explanations, not a theorem; a loss mechanism inside a Penning trap could well depend on the field. As a discriminator it should say 'no dependence of the stated form', or be marked as a reading.
  - One fact new to the node: bottles with no magnetic field read about 2.5 to 3 s above magnetic bottles on an unweighted mean (878.5 to 882.5 s against about 877.8 s). All are 6 to 10 s below the beam value. Recorded as observation only.
- **Independent check:** PARTLY CONFIRMED. The checker is Claude (a fresh subagent that found its own sources). No finding disputed. Could not check: Byrne's trap field; Spivak's apparatus; an explicit statement of zero field at J-PARC; the universal negative. Both agents read pages through a summarising fetch tool, so wording should be re-checked before it is quoted.
- **Receipts:** N-2026-11-13-2-audit-findings.txt (claim table with 22 sources and the checker's verdicts).
- **Confidence:** high for the three corrections with located sources (the beam average's make-up, the charge-exchange paper, the UCNτ update). Medium for the negative on field variation. Low for Byrne's 5 T.

### N-2026-11-13-3: 'no positive-weight rule can give the floor' (D2)

- **Depth reached:** D2. Nothing was simulated.
- **Crack found:** yes. The claim is true in two senses and false in a third, and the kill line on 'Signed or phased handoff contributions' does not discriminate as worded.
- **In plain words.** With ordinary probabilities every history has a definite event time and a definite place. So one can always pick out histories that are sharp in both, and one can always make a rule that is nearly deterministic. But one can also write down families of positive-weight rules whose two widths trade against each other, simply by tying their parameters together.
- **Proved or shown.**
  - T1 [theorem] Selection. If T and X are both functions of the same history, then for any point in the support of their joint law and any ε, the histories within ε of it have positive probability and form a sub-ensemble with both widths at most ε. This holds whatever the rates, capped or not. Conditions the checker asked to be stated: the event must complete with positive probability; exact zero widths need discrete-valued T and X; the selected sub-ensemble is not itself a rule of the capped class.
  - T2 [theorem] Unrestricted class. If the class contains rules whose two variances both go to zero, the infimum of the product is 0. The checker's correction: convergence to a deterministic history in law is not enough, since a rare long excursion can keep a variance large; in the telegraph model take the forward-to-backward rate to zero with the other fixed. This is the 10 Nov Q2 result.
  - T3 Restricted class: the claim as worded is false. A family with T-width θ and X-width 1/θ has product 1 for every θ while each width can be made as small as wanted. The checker gave a version that is a genuine rule: arrivals at rate λ each carrying a position reading of spread σ, with T the time of the n-th arrival and X the mean of n readings; the product is σ/λ for every n. Both are parameter-tied, so the floor is put in by the choice of class.
  - Published results of the same kind (located, not re-derived): Fürth 1933, Δx·Δv ≥ D for diffusion, where v is computed from the ensemble's density and is not a property of one history; Bartlett, Rudolph and Spekkens 2012, where restricting the allowed distributions by postulate reproduces Gaussian quantum mechanics and its uncertainty relation, without contextuality or Bell violation.
- **Against the record.** The 10 Nov capped bound (1.875) is a numerical search minimum, not a proved bound, and may come from the rest-state start and not the cap. The tick value (1) is one limiting case, not an infimum. Neither is shown to bound each width separately. So I withdraw my queue wording that the kill line 'is already met' by them; it is met by construction T3, trivially.
- **My reading, disputed and withdrawn.** I proposed that the floor which matters is one that survives selection of histories, and that by T1 only a signed or phased rule can have it. The checker's objections, accepted:
  - Quantum mechanics fails that criterion too, if one may select on recorded outcomes. If selection is limited to what can be prepared beforehand, positive-weight rules with irreducible noise pass it.
  - 'Signed weights or an epistemic restriction' is not a dichotomy. Fürth's relation is a third case: a floor on every sub-ensemble, with positive weights and no restriction, because one quantity belongs to the ensemble. Nelson's stochastic mechanics and Bohmian mechanics put positive weights on trajectories and reproduce interference, at the price of a guiding law that reads a phased ensemble-level object.
  - 'Not interference' was too strong for the Bartlett–Rudolph–Spekkens line; some interference phenomenology has been reproduced with restricted classical models (from the checker's memory, not sourced).
- **What survives.** T1 and T2 as mathematics. The kill line on O_signed needs rewording, since 'a positive infimum under positive weights' is available by construction. K_tradeless's sentence should read: no floor under selection of whole histories and none over an unrestricted class; over a restricted class a floor can be built by tying parameters. No published theorem on an event-time and position pair was found, and none saying plainly that the real-rate telegraph process lacks a position–momentum relation.
- **Independent check:** PARTLY. The checker is Claude (analytic only; literature from its memory). T1, T2, T3b's arithmetic, Fürth and the caveat on joint distributions confirmed; wording corrections as above; my two readings disputed.
- **Receipts:** N-2026-11-13-3-literature.txt (the literature search, with what was fetched and what was only located). No script: nothing was computed.
- **Confidence:** high for T1–T3. The readings are open; see section 5.

**Receipts table** (all in Night-Reports, uploaded from the local files by reference, so the Drive copies are byte-identical; SHA-256 of those bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-13.md | 1lpYarDyooiBgWViLK-sIfNLQjGaedJbV | 4fee8c4c9cab477030abb90a188435fd1d28998b7e31061d121790a430e6cb8b |
| N-2026-11-13-1-psi.py | 1AlAwfmDRBg1qwTdJ7QYSILq7CikYeJQ6 | 142e3322ec12c10c6e7d6ed948414b54acf90a7c3251e2c0c3745ad741dedeef |
| N-2026-11-13-1-psi-output.json | 1WQBdkjiniRBwq_rSXTe9nJBfx7038gos | 50603673a53769e81d82c808d615e1a3df3f9b5f9e86db51fdbc23ccf6e721ba |
| N-2026-11-13-1-psi-stdout.txt | 1ctKMOyYQVG3le67sQ2NuWCcEdSgcqvKo | 58dc77aaa78cbdee99775c23e5e68dc370a1636c6bfeca1a66e55f217d2c2d51 |
| N-2026-11-13-1-chain.py | 1W7puonJBSf7ojXe7N1DYsi9l8HtZ6za8 | 60e755cb4dd673c0f391204c21336d5536f4b65f4c9d68870fefa684edc6b72d |
| N-2026-11-13-1-chain-output.json | 1L5ckMWk4DZFi6toODcCtDP6gwnGfbdSx | d99341fe9529b3805b41cf408888efcf654e49fbdc00953152b185c628b05957 |
| N-2026-11-13-1-chain-stdout.txt | 1gK4Lz8Zpu64hStf1il13RA01bAmr3zX0 | 0b9f40abd154fbfdb62efcc62b2d99b9b10935e6360a5ce89d4606375c49f6f6 |
| N-2026-11-13-1-checker-scripts.txt | 1QP2RVYyk4zbDKmh3W5RCZ4XhD_-a9Bh9 | 06876a14108ee68d39d542faa9df62ee08fce658dfd187af9a0d60ca451640f6 |
| N-2026-11-13-2-audit-findings.txt | 1TRT07g1Cx0P-ov-RJJzfiZ3Qvy-YZwft | 7ca72eccade367f1d15db95ba83d8a59dda3e5bf9a929b8f3b3b0cf1ad87de23 |
| N-2026-11-13-3-literature.txt | 1mMZ5WE9BkdOw8Dl5p-AX9mt0u60E2ZkR | 779d1dd09d9db606728477d10c7bdd4a1cba33c88f91e18efd10c09d274d6e37 |
| MAP-SNAPSHOT-2026-11-13.md | 1ktXHqEwDGEO-p-A4H3twojcGjwmiMGLH | a46878a4ac6f34c219f76b63c950a70794ba4d7b023da3ad6138c1170153ad55 |

No receipt: the checker's finite-size table in item 1 (its scripts are uploaded, its outputs were not saved), and both checkers' reports for items 2 and 3, which are summarised here and not filed separately.

## 5. New candidates (after a disputed reading)

No test failed tonight. One reading of mine was disputed and withdrawn (item 3), and what follows arose after that. It is the checker's, it was not examined, and nothing above was revised to fit it.

- **'Selecting is not conditioning', stated as failure of total probability.** In a positive-weight history rule, if the ensemble is split by event time, the position distributions of the parts always add back to the unsplit one. A rule with signed or phased contributions need not do this. On this reading the mark of what the signed-handoff gap asks for is not a floor on a product of widths but that splitting by time changes what the parts add up to. It would need its own statement and a planted case before any run.

## 6. Suggested Map changes for Glenn to decide

Recommendations only.

1. **P_period, add to its shape.** 'Written as a bare sequence of steps chosen by relative weights, one level has no time variable, and its clock's period is a count: Ψ steps per unit per turn [theorem, model; by construction]. What the count still takes as input: the ratios of weights, a size or a tagged unit, one order of all steps, the well-mixed read of Contact's share, and a way to tell where a turn begins. The open part is now what fixes the ratios and how a turn is read from inside.' Receipt: N-2026-11-13-1, check PARTLY.
2. **K_restless, add one 'follows' line.** The five clocks' periods in steps per unit per turn: 204.2, 6.70, 28.2, 175.2, 204.5. Run as a bare sequence, draw 301417 is countable at every size tried, rough below about 10⁵ units, with occasional long turns (the checker's runs). Receipt: N-2026-11-13-1.
3. **E_ntau, correct three statements and update two.** Reword 'every long reading therefore comes from … the 4.6 T trap' to 'every long reading comes from counting decay protons; the precise one is the NIST trap at 4.6 T'. Reword the charge-exchange citation: arXiv:2506.01682 argues against it as the cause; the proposal is Serebrov's. Reword the Landau-level sentence. Update UCNτ to 877.82 s. Narrow the Oak Ridge line to the model it excludes. Mark 'a proton-counting loss predicts no clean dependence on the field' as a reading. Receipt: N-2026-11-13-2, check PARTLY CONFIRMED.
4. **O_signed, reword its kill line.** As worded, 'a positive infimum under positive weights' is available by tying parameters. Whether to adopt the section 5 candidate in its place is Glenn's call; I would not adopt it unexamined. Receipt: N-2026-11-13-3, check PARTLY.
5. **K_tradeless, replace 'the general claim … is argued, not proved'** with: 'No floor under selection of whole histories, and none over an unrestricted class [theorem]. Over a restricted class a floor can be built by tying parameters, so the general claim is false as worded.' Note beside the 1.875 figure that it is a search minimum and may come from the start condition. Receipt: N-2026-11-13-3.

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **Replace STEERING.md.** Its PIN is done. Without a new one the run chooses for itself inside the stop rule.
- **How a turn is read from inside (D2).** Item 1 leaves this: a tagged unit counts steps but not turns. What is the least a unit, or a small group, must read to tell a turn? Not single-level stability work.
- **Neighbour-reading rules (D1).** Result (a) is for the well-mixed rule. Does 'ratios only' survive when each unit reads m sampled neighbours, and what replaces the single order of steps? A locate, by argument.
- **How sharp is the step-counted clock against size? (D3, needs a pin.)** The checker's runs suggest a skewed, slowly sharpening clock on one draw. This is close to noise-robustness of one level, so I read it as under the stop rule.
- **The total-probability statement on the telegraph model (D2).** Write the section 5 candidate exactly for the reversal clock, with the signed version beside it, and say what a planted case would be. No run.
- **Byrne's trap field (D1).** Read Byrne 1996 itself for the field of the ILL lifetime trap. If it differs clearly from 4.6 T, two proton-trap lifetimes at two fields already exist, at low precision.
- **The minimal coupling run (D3)** still waits on Glenn's call, as on 12 Nov.

## 8. Verification handoffs

```
Task (DeepSeek). Closed level, N units in roles C, V, L, P with counts nC, nV, nL, nP (sum N). Eight step types with weights
w1 = k1*nC (C->L), w2 = k2*nC (C->V), w7 = k7*nC (C->P), w6 = k6*nL (L->C), w5 = k5*nL (L->V), w8 = k8*nP (P->V),
w10 = k10*nV (V->C), w3 = k3*F(nC/N)*nV (V->C), F any differentiable function of the share with values in [0,1], all k > 0.
Rule R: the next step is of type j with probability w_j / sum(w). No time variable.
Prove or refute:
(1) The law of the whole sequence of steps is invariant under k -> s*k for s > 0.
(2) As N -> infinity with sigma = (number of steps)/N, the shares converge on bounded sigma-intervals to the solution of
    dy/dsigma = f(y)/A(y), where f is the usual rate-equation right-hand side and A(y) = sum_j w_j(y)/T; state the theorem used and check its hypotheses (in particular that A is bounded away from zero on the simplex).
(3) If the rate equations dy/dt = f(y) have a periodic orbit of period Theta, then dy/dsigma = f/A has the same orbit with period
    Psi = integral over one period of A(y(t)) dt, the same non-trivial Floquet multipliers, and Psi is invariant under k -> s*k and under scaling of the total.
(4) Give the leading-order size dependence of the variance of the number of steps per turn for the finite-N chain near a stable cycle (phase diffusion), and say under what condition it scales as 1/N.
```

```
Task (DeepSeek). A stochastic rule assigns non-negative probabilities to histories w. T(w) is an event time (defined where the event completes) and X(w) a position at a stated moment. Prove or refute:
(1) For any point (t0, x0) in the support of the joint law of (T, X) restricted to {T finite}, and any eps > 0, the sub-ensemble
    {|T - t0| < eps, |X - x0| < eps} has positive probability and standard deviations of T and X both below eps.
(2) Total probability: for any partition of histories by T, the position laws of the parts, weighted by their probabilities, sum to the unconditioned position law.
(3) Give the simplest rule with signed or complex weights per history (for example a fixed phase per reversal in a one-dimensional
    walk at unit speed) for which the analogue of (2) fails, and compute the failure explicitly for a two-way split by T.
(4) Is there a class of positive-weight rules, closed under mixtures and containing its own conditioned sub-ensembles, on which
    inf (std T)*(std X) > 0? Prove there is none, or exhibit one.
```

## 9. Run notes

- **Access.** Every required source was reached: the spec (v2.1), STEERING.md, the standing constraints (current copy, exact title), the Premise Map (version 1794517273-62fd, parsed to 180 nodes), the 12 Nov report, queue and snapshot, three 12 Nov and 11 Nov receipts, and TIMING-EXTENT-TRADE-2026-11-10.md. The project instructions were in context. The narrative spine (context only) was not opened.
- **The PIN was stale.** Readings taken are in the queue and section 3. If re-running the five-draw decision run nightly was intended, it was not done.
- **Freeze.** The queue was saved as its own file before any item's work. Before freezing I read the 12 Nov scripts, summary and the 10 Nov note to specify the items; no item computation was run before the freeze.
- **Departures from the frozen queue.** None in rules or tolerances. Two notes: in P2 the pilot allowed the largest size on the list (20 000) with a great deal of time to spare, and I did not go beyond the list. In item 3 I withdrew one phrase of the queue's task ('already met by results on the record'), as section 4 says.
- **Item 2 was worked by a subagent and checked by a second one.** Both used web search. The worker could not save its own file, so the receipt was written by me from its report. Pages were read through a summarising fetch tool.
- **Item 3's literature search was done by a subagent;** the argument is mine. Several classic papers were located and not read in full; the receipt marks which.
- **Checks.** Three fresh Claude subagents, none of which saw the working. The item 1 checker went further than asked on finite-size runs (11 seeds, four sizes). That is near the stop rule's territory; I did not extend it and its numbers are reported as the checker's.
- **Map diff method.** By node ids, counts and text dated 12 Nov, against the 12 Nov snapshot as read through Drive; not field by field.
- **Time.** About 06:16–06:45 London time. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports. Nothing else was edited, and no message was sent.
