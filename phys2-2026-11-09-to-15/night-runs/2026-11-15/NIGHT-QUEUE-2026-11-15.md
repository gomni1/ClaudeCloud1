# NIGHT-QUEUE-2026-11-15

PHYS2 Night Run, seventh night. Claude, unattended. Frozen 15 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.

## How the queue was built

- **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact); STEERING.md (ID 1xvCEBQ9…, found by listing the folder and taking the exact title; modified 14 Nov 01:36 UTC); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJx…, title exact, amended 10 Nov); the Premise Map (version 1794620197-4c40, 180 nodes); NIGHT-REPORT-2026-11-14.md in full with its follow-ups; MAP-SNAPSHOT-2026-11-14.md; NIGHT-REPORT-2026-11-13.md in full (for item 4's rule R). The project instructions were in context. No REVIEW notes exist in Night-Reports. The narrative spine (context only) was not opened.
- **The PIN is already done. Reading taken.** STEERING.md is the 14 Nov file, unchanged. Its one PIN, the slit test of the angular-sum handoff, was run on 14 Nov (N-2026-11-14-1) and reported. As the task prompt instructs, it is not re-run.
- **The map has not changed.** Same version string as the 14 Nov snapshot. So nothing from 14 Nov's section 6 has been placed, and tonight's items work from the 14 Nov report, not from new map text.
- **Stop rule applied.** No single-level stability work: no draws, sweeps, balance classifications or stability surveys. Item 4 uses the five known clocks only as named examples and runs nothing.
- **Coupling not run.** Still Glenn's call; STEERING shows no call.
- **Priority 2 (14 Nov follow-ups):** 'Does fixed size with varying direction still force the squared readout?' is item 1. 'Shared-step jitter (write the rule and its prediction; no run until Glenn pins it)' is item 2, and nothing is simulated. 'Whole-step route lengths (D1)' is item 3. 'How a turn is read from inside (D2)', carried over twice, is item 4. Not queued: the scheduled task's STEERING id (already fixed in the prompt); 'the same rates across a level: law or coordinator' (Glenn's ruling, not a run); the minimal coupling run (Glenn's call).
- **Priority 3:** nothing changed on the map.
- **Priorities 4, 6, 7** are served by items 1 (an if-then the 14 Nov theorem leaves unproved in the case the slit set-up actually uses) and 3 (a continuum length doing load-bearing work in a rule stated in steps).
- **Ranking:** item 1 (easy, high: it decides whether the 14 Nov theorem applies to equal-size contributions, which is what slits deliver); item 2 (easy, moderate to high: it tests a sentence in the 14 Nov report before anyone builds on it); item 3 (easy, moderate); item 4 (moderate, moderate).
- **Depth reading taken.** The 14 Nov report suggested D2 for item 1. I set D3: the question is a yes/no if-then, and one bounded computation plus one short proof attempt is meaningful. Nothing beyond that single attempt is made.
- **Method lines applied:** 'say which necessary' (tags); observational comparisons labelled; no coordinator above a level (bears on items 2 and 4); P2.6-03 §3 (say what is by construction).

---

**N-2026-11-15-1 — Does 'no third-order term' still force the squared readout when the contributions all have the same size?**

- **Target:** O_signed ('What in the handoff can cancel?'); the 14 Nov result T1–T3 (N-2026-11-14-2), whose proof uses contributions of every size; 14 Nov handoff task part (4).
- **Picture, in one sentence:** three slits deliver arrows of nearly equal length that differ only in direction, so does 'nothing left over with three slits' still pin the readout to the squared length when only directions are varied?
- **Task:** given P: R² → R continuous with P(0) = 0, and I3(a,b,c) = P(a+b+c) − P(a+b) − P(a+c) − P(b+c) + P(a) + P(b) + P(c) − P(0) = 0 for all unit vectors a, b, c (and only those), determine whether P must equal ℓ(x) + xᵀMx on the reachable disc |x| ≤ 3. Prove it, or exhibit a continuous P that is not of that form.
- **Inputs:** the definitions above; 14 Nov T1–T3; standard analysis. Search for a published result first (restricted-domain Fréchet or Jordan–von Neumann equations).
- **Depth:** D3 Probe.
- **Effort cap:** about 35% of the night.
- **Done means:** yes or no, with either a proof (and the regularity it needs) or a counterexample checked on fresh triples; the null-space table below; one sentence for the map.
- **Mechanism, fixed now.**
  - *Reduction (exact).* Turning a, b, c together turns the argument of every term, so the condition is rotation-covariant and the angular modes P = f(r)·e^{imφ} decouple: each mode must satisfy I3 = 0 on its own. Real P corresponds to pairing m with −m.
  - *Harness.* For each m = 0 … 8: write f(r) = Σ_{k=0}^{K} c_k T_k(2r/3 − 1) (Chebyshev, r in [0, 3]). Take a at angle 0 (allowed by covariance) and J = 4000 random pairs of angles (A, B) for b and c, uniform on [0, 2π), seed 20261115. Each triple gives one complex linear equation in the c_k. Stack them, take singular values, divide by the largest. A direction counts as 'null' if its normalised singular value is below 10⁻⁹, 'unresolved' between 10⁻⁹ and 10⁻⁴, 'not null' above. K = 30 is the main run; K = 20 and K = 40 are repeated to see whether any small value is stable or merely an artefact of the basis. Double precision; numpy.
  - *Expected, stated now.* m = 0: two null directions (the constant, which the −P(0) term makes harmless, and r²). m = ±1: one (r, the linear function). m = ±2: one (r², the off-diagonal quadratic forms). m ≥ 3: none. If that is what appears, with a clean gap, the answer is 'yes on this basis' and continuity plus P(0) = 0 leave ℓ + quadratic form. Any extra null or unresolved direction is reported, reconstructed, and tested directly on 10 000 fresh unit triples (seed 20261116); if I3 stays at float level relative to max|P| it is a counterexample, and that is the result.
  - *Planted failure, guaranteed analytically.* Restrict the triples to c = −b (still unit vectors). Then I3 = 2P(a) + P(b) + P(−b) − 2P(0) − P(a+b) − P(a−b). For a radial P = f(|x|), with 2t the angle between a and b, this is 4f(1) − 2f(0) − f(2cos t) − f(2sin t). Take f(r) = o(r² − 2) with o(u) = u⁵ − 5u³, an odd function with o(2) = 2·o(1) (−8 and −4). Then f(2cos t) + f(2sin t) = o(2cos 2t) + o(−2cos 2t) = 0, and 4f(1) − 2f(0) = 4·o(−1) − 2·o(−2) = 16 − 16 = 0. So I3 = 0 for every pair: a radial polynomial of degree 10 in r, not quadratic, that satisfies the restricted condition exactly. (Its value at 0 is 8, not 0; the −P(0) term is in I3, so this does not matter to the plant.) The harness, run on 4000 restricted triples at m = 0 with K = 30, must (i) report more than two null directions and (ii) return a residual below 10⁻⁹ (relative to the coefficient norm) for this f, which the basis represents exactly. On the full family the same f must give a residual of order 1. If (i) or (ii) fails the harness cannot see a non-quadratic solution when one exists, and the numerics are not a receipt.
  - *Second plant, exact arithmetic.* Direct evaluator on a = b = c = (1, 0): P = |x|⁴ must give 81 − 3·16 + 3 = 36; P = |x|² must give 0.
  - *Proof attempt (one), radial case.* Write f(r) = g(r²), h(t) = g(2 + 2t). With angles A, B between the vectors, the condition says F(A,B) = h(cos A) + h(cos B) + h(cos(A+B)) is a function of S = cos A + cos B + cos(A+B) alone. For differentiable h the Jacobian of (F, S) vanishes; expanding to first order in B at B = 0 gives a first-order linear equation for k(A) = h′(cos A)·sin A. I expect its only solution bounded at A = π to be k = λ sin A, i.e. h affine, i.e. f = α + βr². If so: [theorem, radial, differentiable P]. Whether continuity alone suffices is reported as open if not shown.
  - *Kill line:* a continuous P, not of the form ℓ + quadratic on |x| ≤ 3, with |I3| ≤ 10⁻¹⁰·max|P| on 10 000 fresh unit triples, refutes 'yes'.
  - *By construction, said now:* a null-space count on a polynomial basis cannot prove the absence of rough solutions; it can only fail to find smooth ones. The result is conditional in the same way as 14 Nov's: on 'contributions add' and 'the readout reads the sum alone'.

**N-2026-11-15-2 — Jitter that belongs to grains, not to routes: the rule and its prediction (no run)**

- **Target:** O_signed, candidate shape; the 14 Nov report, item 1 point 4 and section 5 ('if jitter belongs to steps, only the 2 000-step legs that differ would dephase'); 14 Nov follow-up 'Shared-step jitter (D2)'.
- **Picture, in one sentence:** if the random extra turn belongs to the grain a route passes through at a given step, two routes are jostled alike only while they run through the same grains, so how much of their difference survives depends on how far apart they run.
- **Task:** given the rule J below, compute in closed form how the pair term between two routes is reduced, as a function of their separation at the barrier and of the jitter's lateral reach; evaluate it on the 14 Nov geometry; say whether the 14 Nov sentence quoted above is right; state the prediction a later run would test, and its planted case.
- **Inputs:** the 14 Nov geometry (D1 = 10 000, D2 = 2 000, slit centres −100, 0, +100, five grains each, ω = π/5) and its two recorded limits: independent jitter (κ2 falls with scale σ ≈ 1/(2√L) ≈ 0.0046) and jitter common to all routes (κ2 = 1.2402, unchanged).
- **Depth:** D2 Shape. Closed forms and arithmetic only. **Nothing is simulated**; the follow-up says no run until Glenn pins one.
- **Effort cap:** about 25%.
- **Done means:** the formula; a small table for the 14 Nov geometry; a yes/no on the quoted sentence; the prediction and the plant for a future run; what the rule still leaves open.
- **Mechanism, fixed now.**
  - *Rule J(ℓ).* At step index n every grain has a jitter value; values at different step indices are independent; values at the same step index in grains a lateral distance s apart have correlation c(s) = max(0, 1 − s/ℓ). A route picks up, at its n-th step, σ times the value of the grain it is then in. ℓ is the jitter's lateral reach in grains. ℓ → 0 is independent jitter; ℓ → ∞ is jitter common to all routes. The triangular form of c is a modelling choice, stated as such; what depends on it is noted in the result.
  - *Closed form.* Two routes h, h′ from the common source through barrier grains a distance Δ apart to the same screen grain are a lateral distance Δ·n/D1 apart on the first leg and Δ·(1 − n′/D2) on the second (route-length differences of up to 89 steps in 12 000 are neglected; said now). The variance of their orientation difference is 2σ²·Σ_n(1 − c(s_n)) = 2σ²·N_un, and the pair term for doubled angles is multiplied by exp(−4σ²·N_un). With q = Δ/ℓ: N_un = (D1 + D2)·(1 − μ(q)), μ(q) = 1 − q/2 for q ≤ 1 and 1/(2q) for q > 1.
  - *Table to produce.* N_un and σ* = 1/(2√N_un) (where the pair term has fallen by 1/e) for Δ = 1, 4, 100, 200 and ℓ = 0, 1, 5, 100, 1000, ∞.
  - *Planted checks, guaranteed.* ℓ = 0 must give N_un = 12 000 for every pair (σ* = 0.00456, the 14 Nov independent-jitter scale). ℓ = ∞ must give N_un = 0 (the 14 Nov common-jitter case, no loss). A formula that misses either limit is wrong and the item says so.
  - *Prediction to state, not test.* The dependence of fringe loss on slit spacing d at fixed σ, in the two regimes d < ℓ and d > ℓ.
  - *Kill line for the quoted 14 Nov sentence:* it stands only if, at ℓ of one grain, pairs of routes through different slits have N_un near 2 000 (the second leg only). If N_un is near 12 000 the sentence is wrong as written.
  - *Flag, said now:* a jitter field whose reach ℓ is many grains is a correlation across a level. Whether that can come from neighbour interactions or amounts to a shared variable ('no coordinator above a level') is not decided here.

**N-2026-11-15-3 — Route length in a rule stated in steps: where the continuum length is doing the work**

- **Target:** O_signed, candidate shape; STEERING PIN clause (1) ('route length in step units, not rounded'); A_steps ('Steps at every scale; smoothness is coarse-graining'); 14 Nov item 1 point 6 ('imports a continuum metric into a rule stated in steps').
- **Task:** audit one link for smuggling. Given that the slit result (fringe spacing proportional to distance over slit spacing) used straight-line Euclidean length as the step count, locate exactly what a grain rule would have to supply for that length to be the right count, and say what the fringes become if it does not.
- **Inputs:** the 14 Nov set-up; elementary lattice geometry; published results on shortest-route counts in regular and random networks, located if possible and otherwise labelled as from memory.
- **Depth:** D1 Locate. By argument; one exact worked example (shortest routes on a square grid of grains, steps to the four nearest neighbours) done by hand. Nothing is run.
- **Effort cap:** about 15%.
- **Done means:** the place where the continuum enters; the worked example's fringe law; the short list of things that could supply an isotropic length, each tagged earned / not earned.
- **Mechanism:** argument only; no harness, so no planted failure.

**N-2026-11-15-4 — How a turn is read from inside**

- **Target:** P_period (13 Nov shape: inputs 'one order of all steps', 'a way to tell where a turn begins'); the 14 Nov section 5 idea 'heap height as a tick readable from inside'.
- **Picture, in one sentence:** a unit inside a ticking level can count its own steps, so what more must it, or a few units together, read and hold in order to say 'one turn has gone by'?
- **Task:** given rule R of 13 Nov (roles C, V, L, P; eight step types; recruitment reads Contact's share through kr of m neighbours) and its neighbour-reading form, determine the least a unit or small group must read and hold to (i) count along a turn and (ii) mark where a turn begins. State the smallest assumption behind each. Write the heap-height candidate exactly and say which of (i) and (ii) it supplies.
- **Inputs:** 13 Nov item 1 (rule R, Ψ for the five clocks, its list of inputs); 14 Nov item 3 (partial order of steps; comparability of rates). The five clocks' swings are used only if already written in those two reports; no receipt is re-opened and nothing is computed from the equations.
- **Depth:** D2 Shape. By argument only. Not single-level stability work: no rates are drawn, no balance or cycle is examined, nothing is run.
- **Effort cap:** about 20%. If the session runs long this is the item that is dropped and carried over.
- **Done means:** the split between counting and marking, with what each needs; the heap height written as a definition with its one proved property or a statement that none was proved; the least reader stated; what is not shown.
- **Mechanism:** argument only; no harness, so no planted failure.

---

Checks: after each item, a fresh Claude subagent that has not seen the working. Receipts uploaded with SHA-256 before the report is written.
