# NIGHT-REPORT-2026-11-15

PHYS2 Night Run, seventh night. Claude, unattended, 15 Nov 2026, from about 06:16 London time. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

STEERING's pinned slit test was done on 14 Nov and the file has not changed, so it was not re-run; the Premise Map has not changed either. The night worked four follow-ups from the 14 Nov report, and three of them correct or tighten what that report said. First, the 14 Nov theorem (three slits leave nothing over only if the readout is the squared length) still holds when the three contributions have the same size and differ only in direction, which is what slits actually deliver: proved for readouts that depend on length alone, exact for polynomial readouts up to degree 12, and supported numerically otherwise. Second, a sentence in the 14 Nov report was wrong: if jitter belongs to the grains a route passes through, routes through different slits share almost none of it, so fringes die just as fast as with independent jitter. What matters is how far apart the routes run compared with how far the jitter reaches sideways, and that gives a prediction independent jitter does not make: fringe loss grows with slit spacing.

Third, the slit run's fringe law (spacing proportional to screen distance over slit spacing) comes from the smooth, curved form of the length that was fed in, not from the handoff rule: counted in whole steps on any regular grid of grains, the same set-up gives no such fringes at all. Fourth, a unit inside a ticking level that sees only its own role changes cannot tell a turn has passed, even statistically; marking a turn needs a count to mark it against, so the two needs I tried to separate are one. For direction: the handoff candidate's open inputs are now sharper (why contributions add, why the grain reads only the sum, what supplies a curved step-distance, how jitter is shared sideways), and none of them is in the handoff rule itself.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-15.md (Drive ID 1dMpkFBCVomHCtN6ztzLkwIJfkeCxtXEp, created 06:22:07 UTC by Drive's clock) and not altered afterwards. It was uploaded from the local file by reference, so the Drive copy is byte-identical; SHA-256 01278e68140998cb1b39fc1441fc0727c5e7bf5d48f29240c6fc2e5a0a0c8640. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-15
> 
> PHYS2 Night Run, seventh night. Claude, unattended. Frozen 15 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
> 
> ## How the queue was built
> 
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (ID 1xvCEBQ9…, found by listing the folder and taking the exact title; modified 14 Nov 01:36 UTC); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794620197-4c40, 180 nodes); NIGHT-REPORT-2026-11-14.md in full with its follow-ups; MAP-SNAPSHOT-2026-11-14.md; NIGHT-REPORT-2026-11-13.md in full (for item 4's rule R). The project instructions were in context. No REVIEW notes exist in Night-Reports. The narrative spine (context only) was not opened.
> - **The PIN is already done. Reading taken.** STEERING.md is the 14 Nov file, unchanged. Its one PIN, the slit test of the angular-sum handoff, was run on 14 Nov (N-2026-11-14-1) and reported. As the task prompt instructs, it is not re-run.
> - **The map has not changed.** Same version string as the 14 Nov snapshot. So nothing from 14 Nov's section 6 has been placed, and tonight's items work from the 14 Nov report, not from new map text.
> - **Stop rule applied.** No single-level stability work: no draws, sweeps, balance classifications or stability surveys. Item 4 uses the five known clocks only as named examples and runs nothing.
> - **Coupling not run.** Still Glenn's call; STEERING shows no call.
> - **Priority 2 (14 Nov follow-ups):** 'Does fixed size with varying direction still force the squared readout?' is item 1. 'Shared-step jitter (write the rule and its prediction; no run until Glenn pins it)' is item 2, and nothing is simulated. 'Whole-step route lengths (D1)' is item 3. 'How a turn is read from inside (D2)', carried over twice, is item 4. Not queued: the scheduled task's STEERING id (already fixed in the prompt); 'the same rates across a level: law or coordinator' (Glenn's ruling, not a run); the minimal coupling run (Glenn's call).
> - **Priority 3:** nothing changed on the map.
> - **Priorities 4, 6, 7** are served by items 1 (an if-then the 14 Nov theorem leaves unproved in the case the slit set-up actually uses) and 3 (a continuum length doing load-bearing work in a rule stated in steps).
> - **Ranking:** item 1 (easy, high: it decides whether the 14 Nov theorem applies to equal-size contributions, which is what slits deliver); item 2 (easy, moderate to high: it tests a sentence in the 14 Nov report before anyone builds on it); item 3 (easy, moderate); item 4 (moderate, moderate).
> - **Depth reading taken.** The 14 Nov report suggested D2 for item 1. I set D3: the question is a yes/no if-then, and one bounded computation plus one short proof attempt is meaningful. Nothing beyond that single attempt is made.
> - **Method lines applied:** 'say which necessary' (tags); observational comparisons labelled; no coordinator above a level (bears on items 2 and 4); P2.6-03 §3 (say what is by construction).
> 
> ---
> 
> **N-2026-11-15-1 — Does 'no third-order term' still force the squared readout when the contributions all have the same size?**
> 
> - **Target:** O_signed ('What in the handoff can cancel?'); the 14 Nov result T1–T3 (N-2026-11-14-2), whose proof uses contributions of every size; 14 Nov handoff task part (4).
> - **Picture, in one sentence:** three slits deliver arrows of nearly equal length that differ only in direction, so does 'nothing left over with three slits' still pin the readout to the squared length when only directions are varied?
> - **Task:** given P: R² → R continuous with P(0) = 0, and I3(a,b,c) = P(a+b+c) − P(a+b) − P(a+c) − P(b+c) + P(a) + P(b) + P(c) − P(0) = 0 for all unit vectors a, b, c (and only those), determine whether P must equal ℓ(x) + xᵀMx on the reachable disc |x| ≤ 3. Prove it, or exhibit a continuous P that is not of that form.
> - **Inputs:** the definitions above; 14 Nov T1–T3; standard analysis. Search for a published result first (restricted-domain Fréchet or Jordan–von Neumann equations).
> - **Depth:** D3 Probe.
> - **Effort cap:** about 35% of the night.
> - **Done means:** yes or no, with either a proof (and the regularity it needs) or a counterexample checked on fresh triples; the null-space table below; one sentence for the map.
> - **Mechanism, fixed now.**
>   - *Reduction (exact).* Turning a, b, c together turns the argument of every term, so the condition is rotation-covariant and the angular modes P = f(r)·e^{imφ} decouple: each mode must satisfy I3 = 0 on its own. Real P corresponds to pairing m with −m.
>   - *Harness.* For each m = 0 … 8: write f(r) = Σ_{k=0}^{K} c_k T_k(2r/3 − 1) (Chebyshev, r in [0, 3]). Take a at angle 0 (allowed by covariance) and J = 4000 random pairs of angles (A, B) for b and c, uniform on [0, 2π), seed 20261115. Each triple gives one complex linear equation in the c_k. Stack them, take singular values, divide by the largest. A direction counts as 'null' if its normalised singular value is below 10⁻⁹, 'unresolved' between 10⁻⁹ and 10⁻⁴, 'not null' above. K = 30 is the main run; K = 20 and K = 40 are repeated to see whether any small value is stable or merely an artefact of the basis. Double precision; numpy.
>   - *Expected, stated now.* m = 0: two null directions (the constant, which the −P(0) term makes harmless, and r²). m = ±1: one (r, the linear function). m = ±2: one (r², the off-diagonal quadratic forms). m ≥ 3: none. If that is what appears, with a clean gap, the answer is 'yes on this basis' and continuity plus P(0) = 0 leave ℓ + quadratic form. Any extra null or unresolved direction is reported, reconstructed, and tested directly on 10 000 fresh unit triples (seed 20261116); if I3 stays at float level relative to max|P| it is a counterexample, and that is the result.
>   - *Planted failure, guaranteed analytically.* Restrict the triples to c = −b (still unit vectors). Then I3 = 2P(a) + P(b) + P(−b) − 2P(0) − P(a+b) − P(a−b). For a radial P = f(|x|), with 2t the angle between a and b, this is 4f(1) − 2f(0) − f(2cos t) − f(2sin t). Take f(r) = o(r² − 2) with o(u) = u⁵ − 5u³, an odd function with o(2) = 2·o(1) (−8 and −4). Then f(2cos t) + f(2sin t) = o(2cos 2t) + o(−2cos 2t) = 0, and 4f(1) − 2f(0) = 4·o(−1) − 2·o(−2) = 16 − 16 = 0. So I3 = 0 for every pair: a radial polynomial of degree 10 in r, not quadratic, that satisfies the restricted condition exactly. (Its value at 0 is 8, not 0; the −P(0) term is in I3, so this does not matter to the plant.) The harness, run on 4000 restricted triples at m = 0 with K = 30, must (i) report more than two null directions and (ii) return a residual below 10⁻⁹ (relative to the coefficient norm) for this f, which the basis represents exactly. On the full family the same f must give a residual of order 1. If (i) or (ii) fails the harness cannot see a non-quadratic solution when one exists, and the numerics are not a receipt.
>   - *Second plant, exact arithmetic.* Direct evaluator on a = b = c = (1, 0): P = |x|⁴ must give 81 − 3·16 + 3 = 36; P = |x|² must give 0.
>   - *Proof attempt (one), radial case.* Write f(r) = g(r²), h(t) = g(2 + 2t). With angles A, B between the vectors, the condition says F(A,B) = h(cos A) + h(cos B) + h(cos(A+B)) is a function of S = cos A + cos B + cos(A+B) alone. For differentiable h the Jacobian of (F, S) vanishes; expanding to first order in B at B = 0 gives a first-order linear equation for k(A) = h′(cos A)·sin A. I expect its only solution bounded at A = π to be k = λ sin A, i.e. h affine, i.e. f = α + βr². If so: [theorem, radial, differentiable P]. Whether continuity alone suffices is reported as open if not shown.
>   - *Kill line:* a continuous P, not of the form ℓ + quadratic on |x| ≤ 3, with |I3| ≤ 10⁻¹⁰·max|P| on 10 000 fresh unit triples, refutes 'yes'.
>   - *By construction, said now:* a null-space count on a polynomial basis cannot prove the absence of rough solutions; it can only fail to find smooth ones. The result is conditional in the same way as 14 Nov's: on 'contributions add' and 'the readout reads the sum alone'.
> 
> **N-2026-11-15-2 — Jitter that belongs to grains, not to routes: the rule and its prediction (no run)**
> 
> - **Target:** O_signed, candidate shape; the 14 Nov report, item 1 point 4 and section 5 ('if jitter belongs to steps, only the 2 000-step legs that differ would dephase'); 14 Nov follow-up 'Shared-step jitter (D2)'.
> - **Picture, in one sentence:** if the random extra turn belongs to the grain a route passes through at a given step, two routes are jostled alike only while they run through the same grains, so how much of their difference survives depends on how far apart they run.
> - **Task:** given the rule J below, compute in closed form how the pair term between two routes is reduced, as a function of their separation at the barrier and of the jitter's lateral reach; evaluate it on the 14 Nov geometry; say whether the 14 Nov sentence quoted above is right; state the prediction a later run would test, and its planted case.
> - **Inputs:** the 14 Nov geometry (D1 = 10 000, D2 = 2 000, slit centres −100, 0, +100, five grains each, ω = π/5) and its two recorded limits: independent jitter (κ2 falls with scale σ ≈ 1/(2√L) ≈ 0.0046) and jitter common to all routes (κ2 = 1.2402, unchanged).
> - **Depth:** D2 Shape. Closed forms and arithmetic only. **Nothing is simulated**; the follow-up says no run until Glenn pins one.
> - **Effort cap:** about 25%.
> - **Done means:** the formula; a small table for the 14 Nov geometry; a yes/no on the quoted sentence; the prediction and the plant for a future run; what the rule still leaves open.
> - **Mechanism, fixed now.**
>   - *Rule J(ℓ).* At step index n every grain has a jitter value; values at different step indices are independent; values at the same step index in grains a lateral distance s apart have correlation c(s) = max(0, 1 − s/ℓ). A route picks up, at its n-th step, σ times the value of the grain it is then in. ℓ is the jitter's lateral reach in grains. ℓ → 0 is independent jitter; ℓ → ∞ is jitter common to all routes. The triangular form of c is a modelling choice, stated as such; what depends on it is noted in the result.
>   - *Closed form.* Two routes h, h′ from the common source through barrier grains a distance Δ apart to the same screen grain are a lateral distance Δ·n/D1 apart on the first leg and Δ·(1 − n′/D2) on the second (route-length differences of up to 89 steps in 12 000 are neglected; said now). The variance of their orientation difference is 2σ²·Σ_n(1 − c(s_n)) = 2σ²·N_un, and the pair term for doubled angles is multiplied by exp(−4σ²·N_un). With q = Δ/ℓ: N_un = (D1 + D2)·(1 − μ(q)), μ(q) = 1 − q/2 for q ≤ 1 and 1/(2q) for q > 1.
>   - *Table to produce.* N_un and σ* = 1/(2√N_un) (where the pair term has fallen by 1/e) for Δ = 1, 4, 100, 200 and ℓ = 0, 1, 5, 100, 1000, ∞.
>   - *Planted checks, guaranteed.* ℓ = 0 must give N_un = 12 000 for every pair (σ* = 0.00456, the 14 Nov independent-jitter scale). ℓ = ∞ must give N_un = 0 (the 14 Nov common-jitter case, no loss). A formula that misses either limit is wrong and the item says so.
>   - *Prediction to state, not test.* The dependence of fringe loss on slit spacing d at fixed σ, in the two regimes d < ℓ and d > ℓ.
>   - *Kill line for the quoted 14 Nov sentence:* it stands only if, at ℓ of one grain, pairs of routes through different slits have N_un near 2 000 (the second leg only). If N_un is near 12 000 the sentence is wrong as written.
>   - *Flag, said now:* a jitter field whose reach ℓ is many grains is a correlation across a level. Whether that can come from neighbour interactions or amounts to a shared variable ('no coordinator above a level') is not decided here.
> 
> **N-2026-11-15-3 — Route length in a rule stated in steps: where the continuum length is doing the work**
> 
> - **Target:** O_signed, candidate shape; STEERING PIN clause (1) ('route length in step units, not rounded'); A_steps ('Steps at every scale; smoothness is coarse-graining'); 14 Nov item 1 point 6 ('imports a continuum metric into a rule stated in steps').
> - **Task:** audit one link for smuggling. Given that the slit result (fringe spacing proportional to distance over slit spacing) used straight-line Euclidean length as the step count, locate exactly what a grain rule would have to supply for that length to be the right count, and say what the fringes become if it does not.
> - **Inputs:** the 14 Nov set-up; elementary lattice geometry; published results on shortest-route counts in regular and random networks, located if possible and otherwise labelled as from memory.
> - **Depth:** D1 Locate. By argument; one exact worked example (shortest routes on a square grid of grains, steps to the four nearest neighbours) done by hand. Nothing is run.
> - **Effort cap:** about 15%.
> - **Done means:** the place where the continuum enters; the worked example's fringe law; the short list of things that could supply an isotropic length, each tagged earned / not earned.
> - **Mechanism:** argument only; no harness, so no planted failure.
> 
> **N-2026-11-15-4 — How a turn is read from inside**
> 
> - **Target:** P_period (13 Nov shape: inputs 'one order of all steps', 'a way to tell where a turn begins'); the 14 Nov section 5 idea 'heap height as a tick readable from inside'.
> - **Picture, in one sentence:** a unit inside a ticking level can count its own steps, so what more must it, or a few units together, read and hold in order to say 'one turn has gone by'?
> - **Task:** given rule R of 13 Nov (roles C, V, L, P; eight step types; recruitment reads Contact's share through kr of m neighbours) and its neighbour-reading form, determine the least a unit or small group must read and hold to (i) count along a turn and (ii) mark where a turn begins. State the smallest assumption behind each. Write the heap-height candidate exactly and say which of (i) and (ii) it supplies.
> - **Inputs:** 13 Nov item 1 (rule R, Ψ for the five clocks, its list of inputs); 14 Nov item 3 (partial order of steps; comparability of rates). The five clocks' swings are used only if already written in those two reports; no receipt is re-opened and nothing is computed from the equations.
> - **Depth:** D2 Shape. By argument only. Not single-level stability work: no rates are drawn, no balance or cycle is examined, nothing is run.
> - **Effort cap:** about 20%. If the session runs long this is the item that is dropped and carried over.
> - **Done means:** the split between counting and marking, with what each needs; the heap height written as a definition with its one proved property or a statement that none was proved; the least reader stated; what is not shown.
> - **Mechanism:** argument only; no harness, so no planted failure.
> 
> ---
> 
> Checks: after each item, a fresh Claude subagent that has not seen the working. Receipts uploaded with SHA-256 before the report is written.

## 3. State changes noticed

- **Map diff.** None. The Premise Map was read at version 1794620197-4c40, the same version as the 14 Nov snapshot: 180 nodes; Known 54, if-then 38, Candidate 28, Retired 19, Gap 19, Adopted 12, Floor 10; live 95, Archive 62, Reserve 15, Reservoir 8. So none of the 14 Nov report's five suggested changes has been placed. Tonight's snapshot records a hash of the full node data, so a later run can detect a field-level change that leaves the counts alone.
- **Standing constraints.** Unchanged since 10 Nov (ID 1LjICJx…, exact title).
- **Steering applied.** STEERING.md is ID 1xvCEBQ9vpbyw7aVOIpNI81ESGMzMJsrW (14 Nov 01:36 UTC), found by listing the folder and taking the exact title; it matches the id in the task prompt. **Its one PIN, the slit test, was completed on 14 Nov (N-2026-11-14-1) and the file has not been replaced, so it was not re-run.** The stop rule was obeyed: nothing was drawn, swept, classified or surveyed on a single level. The coupling run was not made.
- **Previous follow-ups.** Four of the seven from 14 Nov became tonight's items. The STEERING-id follow-up is already fixed in the task prompt. The 'law or coordinator' question and the coupling run wait on Glenn.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-15-1: equal-size contributions and the squared readout (D3)

- **Depth reached:** D3.
- **Crack found:** no. The wall holds at this depth, and the 14 Nov theorem is extended to the case the slit set-up uses.
- **In plain words.** The 14 Nov proof let the three contributions take any size. Slits give three arrows of about the same length that differ only in direction. Asking for 'nothing left over with three slits' for every choice of three directions turns out to be enough: no smooth readout other than the squared length (plus the harmless linear and lopsided-quadratic forms that the other 14 Nov conditions remove) was found, and for readouts that depend on length alone this is proved.
- **Results.**
  - R1 [theorem]. The condition is unchanged when all three arrows are turned together, so a readout splits into angular parts that must each satisfy it alone.
  - R2 [theorem, radial readouts]. If the readout depends only on the length of the sum, is continuous, and is twice differentiable for lengths up to 2 (in units of one contribution), then 'I3 = 0 for all unit triples' forces it to be β times the squared length on the whole reachable disc (radius 3). The proof uses an identity for unit vectors, |a+b|·|b+c|·|c+a| = | |a+b+c|² − 1 |, and reduces to a first-order differential equation with one extra solution, a logarithm, which fails the original condition. The checker re-derived every step and confirmed it; it also showed the logarithm is excluded by the condition itself, so my continuity-at-zero hypothesis is stronger than needed.
  - R3 [computed, exact]. For polynomial readouts in the plane up to degree 12, the solutions are exactly constants, linear functions and quadratic forms: six dimensions, five once P(0) = 0 (the checker's exact-arithmetic count; rigorous for polynomials).
  - R4 [computed]. On a Chebyshev basis in the length, degree 20, 30 and 40, with 4000 random unit triples: the only null directions are the expected ones (angular part 0: constant and r²; parts ±1: r; parts ±2: r²; parts 3 to 8: none). Null values sit at 10⁻¹⁷; the next values are about 10⁻²; nothing lies between. The checker found the same with splines, including piecewise-linear ones that allow kinks.
  - Direct evaluation on 10 000 fresh unit triples: max|I3|/max|P| is at 10⁻¹⁶ for the squared length, the lopsided quadratic and the squared length plus a linear term; and 0.66, 0.23, 0.11, 0.22, 0.44, 1.5 for |R|, |R|^1.5, |R|^2.5, |R|³, |R|⁴ and the saturating form.
- **Planted failures: both tripped.** Restricted to triples with c = −b, the non-quadratic function (r² − 2)⁵ − 5(r² − 2)³ satisfies the condition exactly; the harness found it (residual 9×10⁻¹³, twelve null directions on the restricted family) and rejected it on the full family (residual 24). The exact-arithmetic plant returned 36 and 0.
- **What is not shown** (the checker's points, accepted).
  - For readouts that depend on direction as well as length, and are not polynomials, the result is numerical evidence, not proof. The smallest non-null values fall slowly as the basis grows (0.019, 0.012, 0.008), so rough or rapidly oscillating solutions cannot be excluded by this method.
  - A readout that is merely continuous is not covered. The checker suggested a route (averaging the condition gains regularity) but did not carry it out.
  - The statement is for arrows in the plane, on the disc of radius three contribution-sizes; outside it the readout is unconstrained.
- **Published work.** The checker opened two papers on quadratic functional equations restricted to vectors of equal norm (Fochi and Viola 2013; Szabó 1995). Neither covers a single fixed length in the plane with triples. Nothing was found that states R2.
- **What it means for the gap.** Unchanged in kind from 14 Nov, firmer in scope: within 'contributions add and the grain reads the sum alone', the three-slit condition fixes the readout even when only directions vary. The open part of 'What in the handoff can cancel?' is still those two assumptions.
- **By construction:** conditional on the same two assumptions as 14 Nov; said in the queue.
- **Independent check:** PARTLY. The checker is Claude (a fresh subagent with its own two discretisations and its own derivation of R2). Everything it could check held; its one dispute is that 'smooth readout' in my reading overreached beyond the radial and polynomial cases. Accepted; the wording above is the corrected one. Worth a DeepSeek check and an attempt at the general proof (section 8).
- **Receipts:** N-2026-11-15-1-nullspace.py, -nullspace-output.json, -nullspace-stdout.txt, -proof.txt, -checker.txt.
- **Confidence:** high for R1–R3 (two independent derivations or computations each). Medium for the general smooth case (numerics only).

### N-2026-11-15-2: jitter that belongs to grains (D2, nothing simulated)

- **Depth reached:** D2. Closed forms and arithmetic only.
- **Crack found:** yes, in the 14 Nov report. Its sentence 'if jitter belongs to steps, only the 2 000-step legs that differ would dephase' is wrong for the straight routes the slit test used.
- **In plain words.** Two routes from the source to the same screen grain fan apart, then close up again. If the random extra turn belongs to the grain a route is in, the two routes are jostled alike only where they are within the jitter's sideways reach of each other. Routes through different slits are 100 or 200 grains apart at the barrier, so with a reach of one grain they share only the first and last hundred steps or so out of twelve thousand.
- **The rule, as frozen: J(ℓ).** Jitter values at different step indices are independent; at the same step index, grains a sideways distance s apart have correlation max(0, 1 − s/ℓ).
- **Closed form [theorem, model; confirmed by the checker's derivation and a one-pair Monte Carlo].** For two routes through barrier grains Δ apart, the pair term is multiplied by exp(−4σ²·N_un), with N_un = (D1 + D2)·(1 − μ(Δ/ℓ)), μ(q) = 1 − q/2 for q ≤ 1 and 1/(2q) for q > 1. Both planted limits hold: ℓ = 0 gives 12 000 for every pair (14 Nov's independent jitter, σ* = 0.00456), and ℓ = ∞ gives 0 (14 Nov's common jitter, no loss).

| Reach ℓ (grains) | Same slit, Δ = 1 | Same slit, Δ = 4 | Adjacent slits, Δ = 100 | Outer slits, Δ = 200 |
|---|---|---|---|---|
| 0 (independent) | 12 000 | 12 000 | 12 000 | 12 000 |
| 1 | 6 000 | 10 500 | 11 940 | 11 970 |
| 5 | 1 200 | 4 800 | 11 700 | 11 850 |
| 100 | 60 | 240 | 6 000 | 9 000 |
| 1 000 | 6 | 24 | 600 | 1 200 |
| ∞ (common) | 0 | 0 | 0 | 0 |

  (Entries are N_un, the number of steps' worth of unshared jitter. The pair term falls to 1/e at σ* = 1/(2√N_un).)
- **Kill line on the 14 Nov sentence: met; the sentence fails.** At a reach of one grain, routes through different slits have N_un = 11 940, not about 2 000. The checker sharpened this: under J(ℓ) both legs always lose the same fraction, so no reach makes 'only the second leg dephases' true. The sentence would be right only under a different rule, in which routes through one slit literally occupy the same grains up to the slit and then fan out, or in which jitter before the barrier depends on step index alone.
- **Shape.**
  - What removes fringes is the ratio of route separation to the jitter's sideways reach. Grain-scale jitter changes only the coherence within a slit.
  - Prediction, stated and not tested: for slit spacing d below the reach, the pair term is exp(−2σ²(D1 + D2)·d/ℓ), so fringe loss grows with slit spacing; above the reach it levels off at the independent value. Independent jitter predicts no dependence on d. With a correlation that is smooth at zero separation the exponent goes as d² (the checker computed (D1 + D2)·d²/(3ℓ²) for a Gaussian one). A test must compare visibility, since changing d also changes the fringe spacing (checker).
  - Observational register: in the decoherence literature the rate grows as the square of the separation at small separation and levels off at large (the checker opened Hornberger's review, quant-ph/0612118, for both statements; Joos and Zeh 1985 is from memory). J(ℓ) with a smooth correlation has that shape. A resemblance, noted as a pointer; nothing was fitted.
- **What the rule takes for granted** (mine and the checker's): a step index shared by all routes, which is a common clock with simultaneity across separated grains; a sideways distance and straight routes in an embedding geometry; jointly Gaussian jitter; a triangular correlation that is valid in one sideways dimension only; jitter that is renewed each step, not frozen into grains; and averaging over many emissions (a single emission gives a definite shifted pattern, as 14 Nov found).
- **Flag.** A reach of many grains is a correlation across a level. Whether it can arise from neighbour interactions or amounts to a shared variable under 'no coordinator above a level' is not decided here. It is Glenn's call.
- **Independent check:** CONFIRMED. The checker is Claude (own derivation, all 16 table entries reproduced by formula and by direct step sum, a grain-lattice version within 0.3%, and a Monte Carlo of one pair of routes in four cases within 1.5 standard errors). It did not simulate the slit experiment and neither did I.
- **Receipts:** N-2026-11-15-2-jitter-table.py, -jitter-table-output.json, -jitter-table-stdout.txt, -checker.txt.
- **Confidence:** high for the formula and table. The literature remark rests on one opened review.

### N-2026-11-15-3: route length in a rule stated in steps (D1)

- **Depth reached:** D1. By argument, with one exact worked example.
- **Crack found:** yes, and the checker moved where I had put it.
- **In plain words.** The slit test counted a route's steps as its straight-line length. Count the fewest whole steps on a square grid of grains instead and the familiar fringes vanish: outside the strip between two slits there are none, inside it they are 2.5 grains apart whatever the screen distance or slit spacing, and with steps to all eight neighbours every route has the same length and nothing interferes. So the fringe law in the 14 Nov run came from the form of the length, not from the handoff rule, and rounding was never the issue.
- **Located.**
  - [theorem, elementary] The worked example, confirmed exactly by the checker for all three slit pairs and every screen grain. (Its nit: sampled on whole grains the pattern repeats every 5.)
  - [theorem; the checker's, accepted] No regular grid escapes this. On any periodic grid the fewest-step distance is piecewise linear in the endpoints; within one linear sector the slit position cancels and there are no fringes; fringes appear only where the axis sits on a kink, and do not depend on screen distance. It checked a hexagonal grid directly.
  - Rounding is not the cause: the checker found the rounded straight-line length keeps the pattern (correlation 0.94 with the unrounded one), while the square-grid count has none of it (0.01).
  - **Correction to my wording.** I located the crack at isotropy. The checker showed the requirement is weaker and more exact: the step-distance between far grains must be curved (strictly convex) around the direction of travel. A smooth lopsided length still gives spacing proportional to distance over slit spacing; a smooth length that is flat along the axis does not. Isotropy is one way to get curvature, and is needed only for the same law in every direction. Accepted.
- **What could supply a curved step-distance** (tags as corrected).
  - A disordered network with no preferred direction. Published: Howard and Newman 1997 prove a ball-shaped limit for one such model (the checker opened the abstract). Two cautions from the checker: their quantity is a passage time, not a step count, and the isotropy is put in through a random scatter of points in a plane that is already Euclidean. Not earned for any grain rule. My tag 'arguably entailed by labels are not physical' is withdrawn: the square grid is label-free and has preferred directions.
  - **My estimate of the cost was wrong.** I wrote that route-to-route fluctuations of the step count (about 23 steps over 12 000) would be mostly shared between slits. The checker found a result (arXiv 2011.14686, abstract, conditional) that the difference between routes to points r apart fluctuates as about √r: roughly 10 steps, two wavelengths, for slits 100 apart. So on such a network one should expect fringes that wander like speckle unless the wavelength is much longer than √(slit spacing). Withdrawn and replaced by the checker's statement. The exponents are conjectural outside solvable models.
  - Summing over all step routes: the checker computed that with a phase per step the wave is damped at every weight it tried, with no travelling wave; at a wavelength of 5 grains the grid's directional error is 3.5%. Not earned; a different rule.
  - A finer rung beneath, or a long wavelength: these deal with whole-number counts, and a long wavelength also eases the two costs above. Neither supplies curvature by itself.
- **Located, final wording:** what a grain rule must supply is a step-distance between far grains that is curved around the direction of travel, with differences between neighbouring routes' counts that fluctuate by much less than a wavelength. Neither is shown. This is where item 2's question comes back from the substrate itself, as jitter frozen into the network.
- **Independent check:** PARTLY. The checker is Claude (exact scripts, a breadth-first check on a hexagonal grid, two abstracts opened; exponents from memory). Claims 1 and 2 confirmed and strengthened; my 'isotropy', my entailment tag and my shared-fluctuation estimate disputed, all accepted.
- **Receipts:** N-2026-11-15-3-argument.txt (as sent), -checker.txt (its report, script and output).
- **Confidence:** high for the worked example and the no-regular-grid statement. Medium for the fluctuation figures (conditional results, read from abstracts).

### N-2026-11-15-4: how a turn is read from inside (D2)

- **Depth reached:** D2. By argument only; nothing run.
- **Crack found:** yes. One clean result, and my proposed split failed.
- **In plain words.** In the step rule a unit's next role depends only on its present role, with fixed odds, wherever the level is in its turn. So a unit watching only its own role changes sees the same thing at every point of the turn. The turn shows up only in how many of everyone else's steps go by while a unit waits to be recruited, and a unit cannot count those without reading something outside itself.
- **Results.**
  - A [theorem, model; confirmed by the checker, exactly and at finite size]. A unit's own sequence of role changes is a chain with fixed odds (from Contact: k1 : k2 : k7; from L: k6 : k5; from P and from Void: certain), independent of the level's whole history. A unit reading only its own role changes cannot tell a turn, even statistically. The level's phase reaches a unit by two channels only: whether a Void-to-Contact step was a seeding or a recruitment, if those can be told apart from inside; and how many steps of other units pass while it waits.
  - A corollary from the checker: the fraction of a unit's own steps that are Void-to-Contact is fixed by the branch odds alone, (1 − p1·q6)/(2 + p7 + p1·q5), at most one half. The 13 Nov table gives 0.33 to 0.48 for the five clocks, inside the bound; the formula itself was not checked against the receipts.
  - B, heap height, written as a definition: the longest chain of steps, each bearing on the next, between two events. It needs only the partial order of steps and depends on weights through their ratios [theorem, given 13–14 Nov and given that the record of events includes what each step read, which the rule as written does not supply (checker)]. In the well-mixed rule it lies between N·Ψ₃ and N·Ψ per turn and adds nothing.
  - C, the least memory for marking a turn is one bit, armed or fired [confirmed]. The sampling-noise bound g > z²·x(1 − x)/(0.2(b − a))² is right if g counts single neighbour readings; my illustration should read 525 to 1 180 readings for z from 2 to 3, not 'several hundred'.
- **What failed** (the checker's objections, accepted; nothing above was reworded to hide them).
  - **The split between counting and marking does not hold.** I claimed they are separate needs. By result A the turn exists for a unit only as timing against a count it lacks, so marking needs a count to mark against. They are one need.
  - **'Each unit already is a one-bit reader' contradicts result A** and is withdrawn. Seen in its own steps a unit's arming and firing is the same at every phase. And the rule's read returns only pass or fail of the threshold, with only passes appearing as steps, so I overstated what a unit reads.
  - **'Nothing in heap height varies around the turn' is unproved and probably false.** Its growth per own step follows the share of steps that are recruitments, which varies around the turn.
  - 'A reader whose re-arming takes about a turn' presupposes a timer of one turn: circular. Only the group threshold survives.
  - My B3 was misworded; it should say 'any two steps of one unit'. 'Nearly total' fails in phases with little recruitment. The proportional growth of heap height with neighbour reading is plausible by a standard subadditivity theorem but unproved, and would give only an average over the cycle.
  - Carrying heap height locally means an unbounded number per unit, handed on at every read: much more than one bit.
- **What survives.** Result A and its corollary. Heap height as a well-defined, order-free count. One bit as the least memory. The pointer that a unit of the rung above, fed by many units of this level, is the natural reader, with the checker's condition: it is an observer, not a coordinator, only if it never writes back, and then its mark is not available to the level itself.
- **Smallest assumption.** A unit that stays the same unit across its own steps over a turn. Declared for counting; the checker notes the heap-height definition relies on it too. It is licensed only because a unit here is a complete organisation of the rung beneath.
- **Independent check:** PARTLY. The checker is Claude (derivation; one small script for the corollary and the arithmetic; literature from memory).
- **Receipts:** N-2026-11-15-4-argument.txt (as sent), -checker.txt.
- **Confidence:** high for result A (two derivations, elementary). Low for anything about heap height beyond its definition.

**Receipts table** (all in Night-Reports, uploaded from the local files by reference, so the Drive copies are byte-identical; SHA-256 of those bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-15.md | 1dMpkFBCVomHCtN6ztzLkwIJfkeCxtXEp | 01278e68140998cb1b39fc1441fc0727c5e7bf5d48f29240c6fc2e5a0a0c8640 |
| N-2026-11-15-1-nullspace.py | 16S_pqsj2jApUk92mXINtx8riUzeg6H-6 | 2ca16d5458d31237539a874e1d1b2feca79a58551eb983388ace3e0ef685000e |
| N-2026-11-15-1-nullspace-output.json | 1iWTmzHOp6YJtXE9fVRipZzEZ-vjEghWP | 8a490a8c989fb5e810f0bd6c737335df71e55a50780c62f8009c7ab98b8636ce |
| N-2026-11-15-1-nullspace-stdout.txt | 1A4ZZy0S5FOyG4gMjgsmuWmsUdUUz6OFR | cc7cda1021c02959f0f74ebfeee905838bb3e613ae656055e14c8632102dcffc |
| N-2026-11-15-1-proof.txt | 1Bq5Q2eTMsh4dkHh1BjxU-NbicjEDYrMc | 4d1f9d515ffeb6b4950561b05da0d6d67d1f15deac09f217d201d47ad29f3984 |
| N-2026-11-15-1-checker.txt | 1dsmwKA-E8uGyjPT9ZI5vRbWt6pLMDTAQ | 390513fd9805abee462c7adf73184680c8316bb4b47b759faddb007348874690 |
| N-2026-11-15-2-jitter-table.py | 1N28UqO5EQK808b70w2_Ln4AbbS8tkfZL | c576d2883aff42e437b36950b7978406ae54913d45ef9433fa4d079c1b0172b4 |
| N-2026-11-15-2-jitter-table-output.json | 1DEPmsUDkA_Q7R_F83kKdnGBvQZDM7k6w | d40a801c5759a663a9f48c769b40fbeb22272c9839aacb3f85b876bab5a083ec |
| N-2026-11-15-2-jitter-table-stdout.txt | 1fBYDPBa1Wkgm70S7ZlgkKlOCEMgSHQhU | 44fcf43cbb0ab245f9b8da565b353b2a1c89939b03e9eeb92b5c3c917c4cb83f |
| N-2026-11-15-2-checker.txt | 1akEaHAyk3JshnmVy7I8sITwC3k7FalZ1 | 2e414ad6a30f41907ffc971d88d72ffdc2ded3eb445f47f6cb70116983f4766d |
| N-2026-11-15-3-argument.txt | 1tioSVR6WRfaC6krKPvgqdOqtAFI4pq7- | badb4e5ff65ba9a9cb88313a926141283b5b49613f0564a216ed4e6fbe064e94 |
| N-2026-11-15-3-checker.txt | 1LuBggXB6KNRb6CP7RRmbW5mpqPjBxBIH | 50f0c1ce0c5f5bccd4780be8c30703ad9ce4e28e9b57e0126655b85ff6992cad |
| N-2026-11-15-4-argument.txt | 1e3Gs0wTq2-cubg1aYqu1zqt0Gzccid_9 | 21c380b407dac4403950b6d455487b7d2631d31b9f475b7904879f6bb831b9c1 |
| N-2026-11-15-4-checker.txt | 1Kpt9wxD_xm65IkiSvPwA_VAHEqEUtr7Q | ac67f748b8cf3571fa872dd38e778d1608fbb916a67c26b22d1102e83a2ff84e |
| MAP-SNAPSHOT-2026-11-15.md | 1MnHq6t6okJUI2G7lGV_fdbrw1R7RsHeZ | 398f296275d21ba6602e9fd51d9fea114fc574dbabc0cb189a7116bfc9a165dc |

Each checker file holds the checker's report as returned, then the scripts it saved and their output; I confirmed that the exact-arithmetic and spline counts (item 1), the one-pair Monte Carlo (item 2), the grid and damped-wave figures (item 3) and the arithmetic (item 4) appear in those outputs. No receipt: the checkers' literature findings, which are their accounts of pages opened through a search or fetch tool; and the item 3 checker's 0.94 and 0.01 correlations if not printed (not confirmed line by line).

## 5. New candidates (post-failure)

No planted test failed tonight and no candidate on the map was revised. Three statements of mine were refuted or withdrawn (the 14 Nov jitter sentence; item 3's isotropy wording and shared-fluctuation estimate; item 4's split and 'one-bit reader'). What follows arose after those results. It is labelled as such, was not examined, and nothing above was changed to fit it.

- **Routes that share a trunk.** The 14 Nov sentence would be right if routes through one slit occupy the same grains up to the slit and fan out only after it (the item 2 checker's reading). That is a different history rule from the PIN's straight routes, with its own prediction: loss of interference set by the after-slit leg only. It would need to be written and pinned before any run.
- **Heap height against own-step count as a turn marker** (the item 4 checker's). If heap height grows faster per own step when recruitment is frequent, the ratio of the two counts varies around the turn and could mark it. This replaces my withdrawn claim that heap height cannot mark. Not examined; it carries the cost of an unbounded number per unit.
- **Curvature as the requirement on step-distance** (the item 3 checker's), in place of isotropy. Stated in item 3 as the corrected location; whether any grain rule delivers it is untouched.

## 6. Suggested Map changes for Glenn to decide

Recommendations only. The 14 Nov report's five suggestions are still unplaced and still stand, except where amended here.

1. **O_signed, if the 14 Nov if-and-only-if is placed (14 Nov suggestion 2), add its scope:** 'It holds when the three contributions have equal size and only their directions vary: proved for readouts that depend on length alone, exact for polynomials to degree 12, numerical otherwise [theorem, radial; computed otherwise]; on the disc of radius three contribution-sizes.' Receipt: N-2026-11-15-1, check PARTLY.
2. **O_signed, amend 14 Nov suggestion 4.** In place of 'how jitter is shared between routes that share steps': 'what matters is route separation against the jitter's sideways reach; grain-scale jitter removes between-slit fringes as fast as independent jitter does; a reach beyond the slit spacing predicts fringe loss that grows with slit spacing.' And correct the 14 Nov report's point 4 on the record: the sentence about the 2 000-step legs is wrong for straight routes. Receipt: N-2026-11-15-2, check CONFIRMED.
3. **O_signed, add to the candidate shape one more thing a rule must settle:** 'The slit run's fringe law comes from the curved form of the route length it was given. Counted in whole steps on any regular grid the same set-up gives no fringes that depend on screen distance [theorem, elementary]. A grain rule must supply a step-distance curved around the direction of travel, with route-to-route differences well below a wavelength.' Receipt: N-2026-11-15-3, check PARTLY.
4. **P_period, add to its shape:** 'A unit that reads only its own role changes cannot tell a turn, even statistically: its role sequence has fixed odds at every phase [theorem, model]. The turn reaches a unit only as timing against other units' steps, so marking a turn and counting along it are one need. Least memory for a mark: one bit.' Receipt: N-2026-11-15-4, check PARTLY.
5. **No change suggested** to the stop rule, the coupling note or any status. Whether a jitter reach of many grains is a coordinator (item 2's flag) joins the 14 Nov question on equal rates across a level as a ruling for Glenn.

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **A new PIN, if Glenn wants one.** STEERING's PIN is done. Without one the run chooses for itself inside the stop rule.
- **The general proof for item 1 (D3).** A per-angular-part version of the radial argument, or the checker's regularity route. Better sent to DeepSeek first (section 8).
- **The fixed-odds corollary against the 13 Nov receipts (D3, small).** Compute (1 − p1·q6)/(2 + p7 + p1·q5) from the five draws' rates and compare with (Ψ₁₀ + Ψ₃)/Ψ in N-2026-11-13-1-psi-output.json. Arithmetic on existing receipts; no draw, no stability work. A mismatch would mean result A or the 13 Nov numbers are wrong.
- **Routes that share a trunk (D2), only if Glenn pins it.** Write the rule and its prediction beside J(ℓ)'s.
- **What does a turn look like in heap height against own count? (D2, by argument.)** Write the section 5 candidate exactly and say what it costs. Needs a statement of what each step reads.
- **Difference fluctuations on a disordered network (D1).** Read the two located papers properly and state what wavelength a given slit spacing would need. Observational and literature work only.
- **Rulings waiting on Glenn, not runs:** equal rates across a level (14 Nov); a jitter reach of many grains (tonight); the minimal coupling run.

## 8. Verification handoffs

```
Task (DeepSeek). Let P: R^2 -> R be continuous with P(0) = 0. Define
I3(a,b,c) = P(a+b+c) - P(a+b) - P(a+c) - P(b+c) + P(a) + P(b) + P(c) - P(0).
Hypothesis H1: I3(a,b,c) = 0 for all a,b,c with |a| = |b| = |c| = 1 (nothing is assumed for other lengths).
Known: constants, linear functions and quadratic forms satisfy H1 (ignoring P(0)=0 for the constant).
For unit complex numbers, |a+b||b+c||c+a| = | |a+b+c|^2 - 1 | and |a+b|^2+|b+c|^2+|c+a|^2 = |a+b+c|^2 + 3.
Prove or refute:
(1) Radial case: if P(x) = f(|x|) with f in C^2(0,2], then f(r) = beta*r^2 on [0,3]. (Claimed route: H1 says
    h(cos A)+h(cos B)+h(cos(A+B)), h(t) = f(sqrt(2+2t)), is a function of cos A+cos B+cos(A+B) alone; the Jacobian
    condition differentiated in B at B=0 gives k'(A) sin A - (2+cos A) k(A) = -2 k'(0) sin A for
    k(A) = f'(2cos(A/2)) sin(A/2), with general solution k = lambda sin A + gamma sin A tan^2(A/2); show the
    gamma-solution, f = 4 ln r - r^2/2, fails H1.)
(2) General case: if P is C^2 (or C^infinity) on |x| < 3, then P = l(x) + x^T M x on |x| <= 3. H1 is rotation-covariant,
    so angular modes f_m(r) e^{i m phi} decouple; treat each m. Numerics find solutions only for |m| <= 2.
(3) Regularity: does continuity of P alone imply smoothness of solutions of H1 inside the disc (for example by
    averaging H1 over the fibre {a+b+c = s})? If not, give a continuous non-quadratic solution.
(4) Is the result special to the plane? State and prove or refute the analogue for unit vectors in R^3.
```

```
Task (DeepSeek or Astra). N units, each in one of four roles C, V, L, P; counts nC, nV, nL, nP. Step types and weights:
C->L k1*nC, C->V k2*nC, C->P k7*nC, L->C k6*nL, L->V k5*nL, P->V k8*nP, V->C k10*nV, V->C k3*F(nC/N)*nV,
F any function with values in [0,1], all k > 0. The next step is of type j with probability w_j / sum(w), and the unit
that moves is uniform among units in the source role. Prove or refute:
(1) For a tagged unit, the sequence of its own role changes is a Markov chain with transition probabilities
    C->L,V,P = k1,k2,k7/(k1+k2+k7); L->C,V = k6,k5/(k6+k5); P->V = 1; V->C = 1, independent of the history of the
    rest of the level, at every finite N.
(2) Hence the long-run fraction of a unit's own steps that are V->C equals (1 - p1*q6)/(2 + p7 + p1*q5), with
    p_i = k_i/(k1+k2+k7), q_i = k_i/(k5+k6); give its maximum.
(3) Characterise exactly what information about the level's state is carried by (a) the label seeding/recruitment
    on each V->C step of the tagged unit, (b) the number of steps of other units between two steps of the tagged unit.
(4) Define dependence of two steps (one changes a unit the other changes or reads) for a variant in which a V unit
    reads m named neighbours. For the longest chain of dependent steps between two steps of one unit, state the
    theorem (Kingman) under which it grows linearly in that unit's step count, and its hypotheses here.
```

## 9. Run notes

- **Access.** Every required source was reached: the spec (v2.1, exact title), STEERING.md (found by title; same id as the prompt gives), the standing constraints (current copy, exact title), the Premise Map (version 1794620197-4c40, parsed to 180 nodes), the 14 Nov report and snapshot, and the 13 Nov report. The project instructions were in context. The narrative spine (context only) was not opened.
- **Readings taken.** The PIN was treated as done and not re-run, as the prompt instructs. Item 1 was set at D3 where 14 Nov had suggested D2 (reason in the queue). Item 2's 'no run' was read as: closed forms and arithmetic by me, and I allowed the checker a Monte Carlo of one pair of routes to test the formula; the slit experiment was not simulated by anyone. Item 4 was read as outside the stop rule because nothing is drawn or run.
- **Freeze.** The queue was saved as its own file at 06:22 UTC before any item's work. Before freezing I worked out on paper what item 1's planted function should be and what item 2's formula would look like, in order to specify them; no script ran before the freeze.
- **Departures from the frozen queue.** None in rules, tolerances or depths. Item 1's hypothesis in the queue's proof sketch ('differentiable') is stated more exactly in the result (twice differentiable up to length 2). Item 4's inputs allowed the five clocks' swings only if written in the 13–14 Nov reports; they are not, so the noise bound is a formula with one illustration.
- **Depths.** Item 1 stopped at one computation and one proof; the general proof was not attempted beyond that. Items 2 to 4 ran nothing. Two checkers went a little further than asked (item 3: a hexagonal grid, lopsided and flat lengths, a damped-wave computation; item 2: the one-pair Monte Carlo). Their extras are reported as theirs and I did not extend them.
- **Checks.** Four fresh Claude subagents, none of which saw the working; items 3 and 4, being arguments, were sent as written. Three of the four used web search or fetch for literature. No cross-model check was made.
- **Wording I got wrong and corrected:** listed in section 5's opening line and in each item.
- **Time.** About 06:16–06:45 London time. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports: the queue, thirteen receipts, the snapshot and this report. Nothing else was edited; no email or message was sent beyond the run's own notification.
