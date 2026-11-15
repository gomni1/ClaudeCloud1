# NIGHT-REPORT-2026-11-11

PHYS2 Night Run, third night. Claude, unattended, 11 Nov 2026, from about 06:20 UTC. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

The 10 Nov stability result now holds for the closed level too, and it came out cleaner than expected. On a closed level, the product of the three eigenvalues that matter (those inside the conservation class) equals k8·(k5 + k6)·H′(x\*) exactly, for any recruitment law and any total. So of three balances the middle one is always unstable, on both kinds of level, by the same one-line argument. The outer balances are again not always stable. And the closed level has something the open level never showed: in 5 of 20 000 three-balance draws, all three balances are unstable at once, so the level has nowhere to rest and must keep moving.

The resting–ticking pair was not found in the one case tested. Near the open level's unstable high-Contact balance, the oscillation lasts about 16–20 swings and dies; every start then heads for the high-Void balance and stays there. So the 10 Nov unstable focus is a launch point, not a clock. The closed draws with no stable balance are now the better place to look for a level that holds a rest state and a tick.

The revised two-level coupling lets the lower rung seed the upper one, and states the exchange as a rate-level conversion. The checker found that it does more than that: it removes the upper rung's existence threshold by construction, and the minimal fix for seeding needs only the seeding term. On the literature side, a lattice skyrmion's collapse barrier does stay finite as the lattice is refined, which supports the shape of O_protect's 'rare' branch, but only for two-dimensional magnets.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-11.md (Drive ID 1kPeSD35TjxHdqUC7FEZntPNawDASU7_8, created 06:24:59 UTC) and not altered afterwards. It was uploaded from the local file by reference, so the Drive copy is byte-identical; SHA-256 5b09fa5b5b48f9e9af2df9bcd182d22c0e7fea871733baf31732f78efbad15f8. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-11
>
> PHYS2 Night Run, third night. Claude, unattended. Frozen 11 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
>
> ## How the queue was built
>
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1 (ID 1sgnU86…, title exact, not SUPERSEDED); STEERING.md (ID 12AzTA4p…, last modified 9 Nov 22:34 UTC: two PIN lines, no SKIP or RETIRED lines, one NOTE); PHYS2-STANDING-CONSTRAINTS.md (ID 1LjICJxBfjMmma25W_2r3egpFpoYt_UJA, title exact, description "CURRENT standing constraints (last amended 10 Nov 2026)"); the Premise Map (version 1794281872-597e, 177 nodes); NIGHT-REPORT-2026-11-10.md and its follow-ups; MAP-SNAPSHOT-2026-11-10.md; NIGHT-REPORT-2026-11-09.md; NOTE-Saturation-Mechanism-2026-11-06.md. The project instructions were in context. No REVIEW notes exist in Night-Reports.
> - **Reading taken on the PINs.** STEERING has not changed since 9 Nov, and both PIN items were worked to their stated depths on 10 Nov (PIN 1 at D3: middle balance proved unstable, outer stability refuted; PIN 2 at D2: coupling specified). Re-running them would duplicate a receipted result. The reading taken: the PINs are satisfied as written, and their open continuations, named in the 10 Nov follow-ups, are queued first in their place. If Glenn meant the PINs to be repeated, this reading is wrong and tonight's items 1–3 are still their nearest continuations.
> - **Priority 1 (PIN continuations) and 2 (10 Nov follow-ups):** the resting–ticking pair (PIN 1, item 1, with the Floquet check of the 10 Nov item 5 applied to any cycle found); the closed-level counterpart of PIN 1 (item 2); the C_seed coupling revised against the 10 Nov checker's disputes (PIN 2, item 3); O_protect 'rare' branch literature (carried over twice, item 4).
> - **Priority 3, map regions changed since the 10 Nov snapshot:** none. The map version is unchanged (1794281872-597e), with the same 177 nodes and the same counts by type and shelf.
> - **Excluded:** nothing is on STEERING SKIP or RETIRED. The standing constraints' Closed list and 'Open and not load-bearing' list were excluded, as were Archive and Outcome nodes.
> - **Carried over, not queued tonight:** the census of outer instability (D2). Reason: it needs the 10 Nov per-draw summary file inside the sandbox, which last night's run could not pass in from Drive without retyping; its value is moderate. The Floquet multipliers of clocks 19387 and 33538 (D3). Reason: their drawn rate vectors are in pull request 7 of gomni1/ClaudeCloud1, not in any source read tonight; the multiplier check is applied instead to whatever cycle item 1 finds.
> - **Ranking (effort versus impact):** item 1 (easy, high: decides whether one level can hold a resting and a ticking organisation side by side; bears on O_drift and G_species); item 2 (easy, high: the same theorem for the closed level, symbolic); item 3 (moderate effort, moderate-high: specification only); item 4 (easy, moderate).
>
> ---
>
> **N-2026-11-11-1 — The resting–ticking pair, and the cycle's multipliers**
> - **Target:** K_bal (its 10 Nov refinement, recommended to Glenn: an outer balance can lose stability to an oscillating pair); O_drift (shape: attractors hyperbolic within their class); G_species (isolation of cycles 'rests on two examples only').
> - **Task:** given structure S (the verified 10 Nov case: open level, m = 27, kr = 7, rates below), determine whether the trajectory leaving the unstable low-Void balance settles onto a periodic orbit that coexists with the stable high-Void balance; if a cycle is found, compute invariant I = its Floquet multipliers.
> - **Inputs:** the open-level equations (saturation note), ρ = k3·F(x), F(x) = I_x(kr, m − kr + 1), k11 = 0; rates (k1, k2, k3, k5, k6, k7, k8, k9, k10, k12) = (17.452344563736048, 0.41372216747103946, 44.67737830552512, 8.05086975924266, 0.06903256564057879, 0.03229295995554182, 0.083706798767576, 0.010174673348427083, 0.609928184398708, 0.15342684932155354) as in the 10 Nov handoff.
> - **Depth:** D3 Probe. One bounded attempt.
> - **Effort cap:** about 35%.
> - **Done means:** for each of six starts, its fate (high-Void balance / cycle / other), and, if a cycle is found, its period and all four multipliers with the trivial one identified. A statement: 'resting–ticking pair found' (stable high-Void balance and a cycle whose non-trivial multipliers all have modulus < 1), or 'not found' with what happened instead.
> - **Mechanism, specified now:**
>   - *Balances:* roots of G(x) = (k10 + k3F(x))(α − βx) − γx on (0, α/β), α = C\*, β = C\* + L\* + P\*, γ = D·C\*, by sign changes on a 4 000-point grid with exact end signs, refined by brentq; V\* = α/x − β. Exactly three must be found (else the item is ill-posed and stops). Eigenvalues of the analytic Jacobian at each; the 10 Nov values (low-Void V\* ≈ 41.1405, eigenvalues ≈ 0.8664 ± 15.778i, −0.000795, −0.1127) must be reproduced to 3 significant figures before anything else runs.
>   - *Starts (6):* S1–S4: y_low + ε·|y_low|·v, with v ∈ {+Re u, −Re u, +Im u, −Im u}, u the unit eigenvector of the unstable pair, ε = 10⁻⁴. S5–S6: y_mid ± ε·|y_mid|·w, w the unit eigenvector of the middle balance's positive real eigenvalue (its unstable manifold, both branches).
>   - *Integration:* scipy solve_ivp, LSODA, rtol 10⁻¹⁰, atol 10⁻¹², t from 0 to t_end = 2×10⁴ (about 16 times the slowest time constant at the low-Void balance, 1/0.000795), t_eval = [t_end] only (no dense output). Event 1, non-terminal: the Poincaré section C − C\* = 0 crossed upward. Only the event times and states are kept. Event 2, terminal guard: total T > 10⁶ (S1 says solutions are bounded; if this fires, the start is reported as 'guard fired', not interpreted).
>   - *Classification at t_end (fixed now):* 'rest at balance B' if |y(t_end) − y_B|/|y_B| < 10⁻⁶; 'cycle' if there are at least 20 section crossings in the last 10% of the run, and the last 10 section states agree pairwise in succession to relative 10⁻⁶, and the last 10 return times agree to relative 10⁻⁶; otherwise 'other', reported as it is.
>   - *Multipliers (only if a cycle is found):* from the last section state, integrate the state with its 4×4 variational matrix (Φ(0) = I), LSODA, rtol 10⁻¹¹, atol 10⁻¹³, until the next upward section crossing (event, terminal); that time is the period Θ and Φ(Θ) the monodromy. Eigenvalues by numpy. The trivial multiplier is the one closest to 1; the check passes if it is within 10⁻⁵ of 1. Cycle called stable if the other three have modulus < 1.
>   - *Positive control (must pass, else the harness is not a receipt):* Stuart–Landau, dz/dt = (μ + iω)z − |z|²z, μ = 1, ω = 2π, start z = 0.5, section Im z = 0 crossed upward, t_end = 200. Analytic: cycle |z| = 1, period exactly 1, multipliers exactly 1 and e^(−2μΘ) = e^(−2) = 0.1353353. The classifier must say 'cycle', with |Θ − 1| < 10⁻⁶ and both multipliers within 10⁻⁵.
>   - *Planted failure PF-A (classifier), guaranteed:* Stuart–Landau with μ = −1, ω = 2π, start z = 0.5. Analytically z → 0 (|z| ≤ 0.5·e^(−t)), so no orbit is periodic; the classifier must not return 'cycle' (it must return 'rest' at 0). If it returns 'cycle', the classifier is blind.
>   - *Planted failure PF-B (trivial-multiplier check), guaranteed:* the Stuart–Landau μ = 1 monodromy taken over 1.01·Θ instead of Θ, from the section point (1, 0). Analytically Φ = [[a·cosθ, −sinθ], [a·sinθ, cosθ]] with a = e^(−2.02), θ = 0.02π; its characteristic polynomial at 1 equals (1 + a)(1 − cosθ) > 0, so no multiplier is 1; the roots are ≈ 0.99743 and 0.13300, so the nearest is ≈ 2.6×10⁻³ from 1, far outside 10⁻⁵. The trivial-multiplier check must fail. If it passes, that check is blind.
>   - *Planted failure PF-G (guard), guaranteed:* dV/dt = 10³ from V = 1 crosses 10⁶ at t = 999 exactly (< t_end); the terminal guard must fire.
>   - *Kill lines:* none on the outcome; it is a measurement. The harness is a receipt only if the positive control passes and PF-A, PF-B and PF-G all trip.
>
> **N-2026-11-11-2 — Closed-level counterpart: does the restricted determinant track the slope?**
> - **Target:** K_bal ('One level holds at most three balances…'), whose 10 Nov stability result is for the open level only; O_drift.
> - **Task:** given rule R (closed level, o = 0, roles C, V, L, P, k11 = 0, x = C/T, any differentiable ρ(x) ≥ 0, all rates positive), determine (a) whether e3(J), the product of the three eigenvalues of J other than the zero eigenvalue of the conserved total (equivalently the determinant of J restricted to the tangent space of the conservation class), equals K·H′(x\*) at every balance with K of fixed sign, where H(x) = (k10 + ρ(x))(1 − c·x) − D·x, c = 1 + k1/(k5 + k6) + k7/k8; (b) whether, when three balances exist, the middle one is always unstable; (c) whether the outer two are always stable.
> - **Inputs:** saturation note (closed balance condition, constants D and c); 10 Nov item 1 and its handoff.
> - **Depth:** D3 Probe. One attempt: a symbolic identity for (a), (b) by consequence, one bounded numerical search for (c).
> - **Effort cap:** about 30%.
> - **Done means:** (a) proved with the exact K, or refuted; (b) stated as following or not; (c) a verified counterexample or 'none in N draws', which is not a proof.
> - **Mechanism, specified now:**
>   - *Symbolic (sympy):* rates as positive symbols, ρ an undefined function. Build the 4×4 Jacobian of the closed level. Compute e3 = sum of the four principal 3×3 minors, and separately det M with M = (BᵀB)⁻¹BᵀJB, B the columns e_C − e_V, e_L − e_V, e_P − e_V; check e3 − det M simplifies to 0 at a balance (J maps the class's tangent space into itself because 1ᵀJ = 0; J·y\* = 0 at a balance by homogeneity). Evaluate at a balance by the closed pins C = xT, L = k1xT/(k5 + k6), P = k7xT/k8, V = T(1 − cx), with ρ(x\*) = r0 eliminated through the balance condition (k10 + r0)(1 − cx) = Dx, and ρ′(x\*) = r1 a free symbol. H′(x\*) = r1(1 − cx) − c(k10 + r0) − D. Form q = e3/H′ and test ∂q/∂r1 simplifies to 0. If so, write q as numerator/denominator in the positive symbols with u = 1 − cx > 0 and x > 0 and test whether every coefficient of each has one sign. (a) holds only if ∂q/∂r1 = 0 and q is sign-definite by that test; if ∂q/∂r1 = 0 but the coefficient test is inconclusive, (a) is reported 'identity found, sign not proved', and the sign is sampled numerically (not a proof).
>   - *Consequence for (b):* in a 3-dimensional class, a negative-real-part spectrum has product < 0; so if e3 and H′ have the same sign (K > 0), then at the middle balance, where H′ > 0, the restriction has a positive real eigenvalue. If K < 0, (b) does not follow by this route. Stated as found.
>   - *Planted failure P1 (symbolic check), conditional and stated as such:* repeat the ∂q/∂r1 test with H′ replaced by H′_w = H′ + c(k10 + r0). If e3 = K·H′ with K free of r1, then ∂(e3/H′_w)/∂r1 = K·c(k10 + r0)(1 − cx)/H′_w², which is non-zero because K ≠ 0, c(k10 + r0) > 0 and 1 − cx > 0; the test must report non-zero. The guarantee holds only if (a)'s identity holds; if it does not, P1 is not interpreted.
>   - *Numerical harness (numpy/scipy, no ODE integration):* T = 1. Draws: k1, k2, k3, k5, k6, k7, k8, k10 log-uniform in [10⁻², 10²], m uniform in 2..30, kr uniform in 2..m, seed 20261111. Balances as roots of G(x) = (k10 + k3F(x))(1 − cx) − Dx on (0, 1/c), grid of 4 000 points with exact end signs, brentq. Keep draws with exactly three. At each balance: the numeric 4×4 J, M = (BᵀB)⁻¹BᵀJB, eigenvalues of M, e3 numerically; if (a) gave K, the relative error |e3 − K·H′|/(|e3| + |K·H′|), flagged if > 10⁻⁶. Flags: middle stable (max Re λ(M) ≤ 0); outer unstable (max Re λ(M) > 10⁻⁹·max|λ|). Per draw only summaries kept.
>   - *Planted failure P2 (stability classifier), guaranteed:* at the first 200 three-balance draws, also classify M + sI with s = 1 − max Re λ(M) at the low-share balance. Its eigenvalues are exactly λ + s, so its max Re λ is exactly 1 > 0; it must be flagged unstable in 200 of 200, else the harness is blind and the numerics are not a receipt.
>   - *Verification:* every outer-unstable flag (up to the first 20) is re-verified in mpmath at 50 digits (balance re-solved, eigenvalues of M recomputed).
>   - *Sizing:* a pilot of 2 000 draws timed first and written into the run notes; main loop until 20 000 three-balance draws or 30 minutes of wall time, whichever first.
>   - *Kill lines, fixed now:* (a) refuted by ∂q/∂r1 ≠ 0, by a verified sign change of K, or by any verified identity flag. (b) 'middle always unstable on a closed level' refuted by any verified middle-stable case. (c) 'outer always stable on a closed level' refuted by any mpmath-verified outer-unstable case.
>
> **N-2026-11-11-3 — The C_seed coupling, revised against its two disputes (specification only)**
> - **Target:** C_seed ('Growth depletes the rung beneath') and its shape line; A_share; F_ladder; P_fedbelow; the 10 Nov item 2 specification and the checker's disputes (1) 'feeds but cannot seed' and (2) 'single-unit currency; the upper level is a second compartment at the same scale'.
> - **Task:** given A_share, F_ladder, P_fedbelow, the forbidden moves (no coordinator above a level; no one-to-one handoff with single-unit bookkeeping; no fitting) and the 10 Nov coupling U = κ·P1·C2, specify the smallest revision that (i) lets the lower rung seed the upper rung as well as feed it, and (ii) states the exchange in ensemble terms, with complete lower organisations (not single lower units) as the upper rung's resource. Write the conservation identity it must satisfy, what changes relative to the 10 Nov specification, what it must not add, and a later-night test with a kill line and an analytically guaranteed planted failure.
> - **Inputs:** NIGHT-REPORT-2026-11-10 item 2; C_seed, A_share, F_ladder, P_fedbelow, K_ladder, K_sat node texts; the saturation note; the standing constraints.
> - **Depth:** D2 Shape.
> - **Effort cap:** about 15%.
> - **Done means:** a written specification with equations, each term's justification, the cross-level conservation identity with any conversion factor, a statement of which of the 10 Nov disputes it resolves and which remain, and a test for a later night. Explicitly not run.
> - **Mechanism:** none tonight. Algebra checked in sympy for consistency only (no dynamics run).
>
> **N-2026-11-11-4 — Does a published result fix the cost of the cheapest integer-changing path under refinement? (O_protect, 'rare' branch)**
> - **Target:** O_protect ('Is the integer's passage forbidden or rare?'), its rare-branch shape ('S need not grow with the number of local changes … a lattice skyrmion's collapse keeps a finite cost as the lattice is refined') and its first step ('search for the cheapest legal integer-changing path … before fitting any cost').
> - **Task:** given rule class R (lattice or step models carrying an integer topological invariant: winding numbers, skyrmion/hopfion charges, vortex number, dimer windings), locate published results that state whether the minimum-energy (or minimum-action) path changing the integer has a cost that stays finite, grows, or diverges as the lattice is refined, and how the rate of change scales (Arrhenius/Kramers prefactor, entropy). Search before any attempt.
> - **Inputs:** O_protect node text; web search.
> - **Depth:** D1 Locate.
> - **Effort cap:** about 10%.
> - **Done means:** a list of results found, each with what it states and whether it bears on the rare branch (yes / partly / no), and a one-line verdict: shape confirmed by literature, partly, or not located. Observational and external results labelled as such. No new proof.
> - **Mechanism:** none; a literature search.

## 3. State changes noticed

- **Map diff.** None. The Premise Map was read at version 1794281872-597e, the same version string as on 10 Nov, with the same 177 nodes and the same counts (Known 52, if-then 37, Candidate 28, Retired 19, Gap 19, Adopted 12, Floor 10; live 94, Archive 60, Reserve 15, Reservoir 8). Tonight's snapshot was generated in the 10 Nov snapshot's format, and its size differs from 10 Nov's by exactly the one sentence added to its header (30 255 against 30 210 bytes). A line-by-line machine diff against the 10 Nov file was not run, for the reason given in section 9. None of the 10 Nov recommendations has been enacted on the map yet.
- **Standing constraints.** Unchanged since 10 Nov. The current copy is file ID 1LjICJxBfjMmma25W_2r3egpFpoYt_UJA, titled exactly PHYS2-STANDING-CONSTRAINTS.md, with the description 'CURRENT standing constraints (last amended 10 Nov 2026)'. The ID named in the spec's Sources (1YmP6…) is titled SUPERSEDED-2026-11-10 and was not used.
- **Steering applied.** STEERING.md has not changed since 9 Nov. Its two PIN items were worked to their stated depths on 10 Nov. **Reading taken:** the PINs are satisfied as written, and tonight's items 1–3 are their open continuations, named in the 10 Nov follow-ups. If Glenn meant the PINs to be repeated, this reading is wrong. There were no SKIP or RETIRED lines. The NOTE (spec v2 applies) was followed, under v2.1.
- **Previous follow-ups:**
  - The resting–ticking pair became item 1.
  - The closed-level counterpart became item 2.
  - The revised C_seed coupling became item 3.
  - The O_protect literature check became item 4.
  - The Floquet multipliers of clocks 19387 and 33538 are carried over, because their rate vectors are not in any source read tonight. Item 1 carried the same check, ready for any cycle it found.
  - The census of outer instability is carried over, because last night's per-draw file could not be brought into the sandbox.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-11-1: the resting–ticking pair (D3)

- **Depth reached:** D3.
- **Crack found:** no, at this depth. In the one case tested, no resting–ticking pair exists.
- **What was done.**
  - The three balances of the verified 10 Nov case (open level, m = 27, kr = 7) were reproduced:
    - V\* = 41.1405: eigenvalues 0.8664 ± 15.778i, −0.000795, −0.1127. This is an unstable focus.
    - V\* = 117.623: eigenvalues +36.44, then three negative. This is a saddle.
    - V\* = 1274.53: eigenvalues −0.000108, −0.0948, −9.14, −17.38. This is stable.
  - Six starts were integrated to t = 2×10⁴: the focus perturbed along ±Re u and ±Im u, and the saddle perturbed along both branches of its unstable direction.
- **Outcome under the frozen classifier:** 'other' for all six. No start was classed as rest or as a cycle.
- **What actually happened.** This is report-only: a diagnostic written after the run, which the checker confirmed independently.
  - The four starts at the focus spiral outward for 16–20 upward crossings of C = C\*, all before t ≈ 8, and then stop oscillating. Both branches of the saddle make no crossings at all.
  - At t = 2×10⁴, all six are 9–10% from the high-Void balance. They are approaching it along its slow mode (eigenvalue −1.08×10⁻⁴; e^(−1.08×10⁻⁴·2×10⁴) = 0.116, which matches the offset).
  - The checker ran the same starts to t = 2×10⁵ and found all six within 4×10⁻¹⁰ of that balance. It also ran 6 large-amplitude starts and 60 random starts to t = 5×10⁴. Every one went to the high-Void balance, and none showed late oscillation.
- **Harness status:** a receipt.
  - The positive control passed. On the Stuart–Landau cycle the classifier returned 'cycle' with period 1 − 6×10⁻¹² and multipliers 0.99999999961 and 0.1353353 (e⁻² exactly).
  - PF-A tripped: the decaying case was classed as 'rest', not 'cycle'.
  - PF-B tripped: the wrong-period monodromy gave a nearest multiplier 2.58×10⁻³ from 1, against the 2.6×10⁻³ predicted.
  - PF-G tripped: the guard fired at t = 999.999.
- **A weakness in my own frozen classifier**, found by the checker and accepted:
  - It could not have returned 'rest' in a run to 2×10⁴. Reaching 10⁻⁶ of the high-Void balance takes about t ≈ 1.3×10⁵, so 'other' was guaranteed for any start that converges.
  - It cannot see a cycle with a period longer than about 100.
  - So the frozen verdict 'other' carries no information by itself. The finding rests on the trajectories, as described above and confirmed by the checker's longer runs. A sounder rule for later nights is in section 7.
- **What it means:**
  - At these rates the unstable high-Contact balance is a launch point, not a clock. A level started near it swings briefly and then settles into the high-Void rest state.
  - The 10 Nov 'resting organisation beside a ticking one' does not happen here.
  - No cycle was found, so no Floquet multipliers were computed.
- **Not shown:**
  - That the high-Void balance attracts every start.
  - That no cycle exists anywhere. Forward integration cannot find unstable cycles, and sampled starts cannot rule out a stable cycle somewhere unsampled.
  - Anything about the other 211 draws of 10 Nov.
- **Independent check:** CONFIRMED. The checker is Claude. Its caveats on the classifier are taken above.
- **Receipts:** N-2026-11-11-1-cycle.py, -cycle-output.json, -cycle-stdout.txt, -diag.py, -diag-output.txt; the checker's -checker-a.py, -b.py, -c.py.
- **Confidence:** high for 'no pair in this case', backed by independent long runs. The general question stays open.

### N-2026-11-11-2: the closed-level counterpart (D3)

- **Depth reached:** D3.
- **Crack found:** yes, both ways, as on the open level. One half is proved, and the other half is refuted with a new feature.
- **(a) Proved \[theorem, model\].**
  - On a closed level, at every balance and for any differentiable recruitment law ρ(x):
    - e3 = k8·(k5 + k6)·H′(x\*).
    - Here e3 is the product of the three eigenvalues of J other than the zero eigenvalue of the conserved total. It equals the determinant of J restricted to the conservation class, and the sum of the principal 3×3 minors.
    - H(x) = (k10 + ρ(x))(1 − c·x) − D·x.
  - The factor k8·(k5 + k6) is positive, and the identity does not depend on the total T.
  - In sympy:
    - J's column sums are 0.
    - e3 and the restricted determinant agree.
    - e3/H′ simplifies to k8·(k5 + k6), with no dependence on ρ′(x\*).
  - The planted check P1 (H′ replaced by H′ + c(k10 + ρ)) correctly reported a dependence on ρ′. Its guarantee was conditional on (a), which holds, so P1 is interpreted.
  - This is the closed counterpart of 10 Nov's open-level det J = k7·k9·(k5 + k6)·g′(V\*). The two are separate results with the same structure; neither is derived from the other.
- **(b) Follows: the middle balance is always unstable.**
  - With three simple balances, H′ is negative, positive, negative at the low-, middle- and high-share balances, since H(0) = k10 + ρ(0) > 0 and H(1/c) = −D/c < 0. (The checker's correction: H(0) is k10 + ρ(0), which equals k10 for the binomial law with kr ≥ 2.)
  - In the class, which has three dimensions, a fully stable spectrum has a negative product.
  - At the middle balance e3 > 0, so there is a positive real eigenvalue. The middle balance is always unstable, on closed levels as on open ones.
  - At the outer balances e3 < 0. That is necessary for stability, not sufficient.
- **(c) Refuted: the outer two are not always stable.**
  - The frozen harness ran 949 427 draws to collect 20 000 three-balance draws, in 239 s. The pilot took 2 000 draws in 0.54 s.
  - Identity: 0 flags; the largest relative error was 2.7×10⁻¹³.
  - Middle balance stable: 0 cases. The smallest middle max Re λ was +0.0069.
  - **Outer balance unstable: 553 balances in 548 distinct draws.**
    - 546 at the high-Contact-share balance.
    - 7 at the low-share balance.
    - The draw count, as against the balance count, is the checker's correction.
  - The first 20 stored flags were re-verified unstable at 50 digits, with residuals below 10⁻⁴⁹. Some lose stability through a complex pair, and others through a pair of positive real eigenvalues.
  - Both stored low-share cases were also verified (report-only):
    - m = 19, kr = 3: 0.0089 ± 0.7986i, −59.04.
    - m = 18, kr = 5: 0.402 ± 0.417i, −40.18.
  - The checker found further cases on each side with an independent seed.
- **New, from the checker's re-run of the same draws: five draws with no stable balance.**
  - In 5 of the 7 low-share cases (draws 2045, 301417, 384616, 456280 and 616482), the high-share balance is also unstable. The middle balance is always unstable, so these levels have **no stable balance at all**.
  - A bounded level with no stable balance cannot come to rest. On a closed level the class is compact, so a trajectory must keep moving, most likely on a cycle or something more complex. That is my reading; it was not integrated tonight.
  - The open level showed no such case in 12 264 draws on 10 Nov.
  - This rests on the checker's run (N-2026-11-11-2-checker-full.txt). My harness did not log the coincidence, and it stored only the first 200 flags.
- **Correspondence of sides.**
  - On the closed level, 'high-share' means high C, L and P together, and low V (V/T = 1 − c·x).
  - On the open level, the unstable outer balance was the low-Void one, where the Contact share is high.
  - So on both kinds of level, the outer instability falls mostly or only on the high-Contact-share side.
- **Harness status:** P2 tripped in 200 of 200, so the stability numerics are a receipt.
- **Independent check:** PARTLY. The checker is Claude.
  - The mathematics was confirmed: (a) was re-derived symbolically by two routes, the logic of (b) was confirmed, and (c) was reproduced draw by draw.
  - The disputes, all accepted and taken in above:
    - the count is 548 draws, not 553;
    - H(0) = k10 + ρ(0);
    - 'carries over' is an analogy, not a derivation;
    - the five no-stable-balance draws are the notable finding and should lead.
  - DeepSeek should check (a) (see section 8).
- **Receipts:** N-2026-11-11-2-sym.py and -sym-output.txt; -num.py, -num-output.json and -num-stdout.txt; -mpverify.py, -mpverify-output.json and -mpverify-output.txt; the checker's -checker-sym2.py, -checker-num.py, -checker-num2.py and -checker-full.txt.
- **Confidence:** high for (a) and (b), an exact identity confirmed independently. High for (c), with verified counterexamples on both sides. Medium for the reading of the five draws: the counts are high-confidence, but what the level does there has not been computed.

### N-2026-11-11-3: the C_seed coupling, revised (D2, specification only)

- **Depth reached:** D2. Nothing was run. The algebra was checked for consistency in sympy.
- **Crack found:** yes. Dispute 1 can be closed by one term. Dispute 2 can be closed only partly inside a one-level description.
- **The specification.** It has two levels in the working grammar: the lower with rates k, the upper with rates u, and the upper having no k12 of its own. Three changes from 10 Nov:
  1. *All lower output goes up.*
     - U = (k9 + κ·C2)·P1 leaves dP1/dt, replacing −k9·P1.
     - U/ν enters dV2/dt.
     - The first part is the passive breach flux. The second is the active uptake from 10 Nov.
  2. *Conversion factor ν ≥ 1:* lower units per upper unit. It is a rate-level conversion, not a per-event exchange.
  3. *Templated seeding:* the upper level's own seeding u10 is replaced by σ·x1, where x1 = C1/T1 is the lower level's Contact share. Upper Void becomes upper Contact at (σ·x1 + ρ2)·V2.
- **Checked in sympy:**
  - Each unit is counted once, in lower currency: d(T1 + ν·T2)/dt = k12 − ν·u9·P2 exactly.
  - At the lower balance, given C2:
    - P1\* = k12/(k9 + κC2);
    - C1\* = k12(κC2 + k8 + k9)/(k7(κC2 + k9));
    - dC1\*/dC2 = −k12·k8·κ/(k7(κC2 + k9)²), which is negative for k8, κ > 0 (the checker notes it is 0 if k8 = 0).
  - U\* = k12 at the lower balance, so the upper level's supply is k12/ν for every κ, and its pin is C2\* = k12(u8 + u9)/(ν·u7·u9).
  - On the face C2 = L2 = P2 = 0 with V2 > 0, dC2/dt = V2·(σ·x1 + ρ2) > 0 whenever C1 > 0. With V2 = 0 as well, dV2/dt = k9·P1/ν > 0. So the lower level now seeds the upper: **dispute 1 is resolved.**
- **Dispute 2, partly resolved.** ν makes the exchange a conversion at the level of rates, not unit-for-unit. But the resource is still breach-ready lower units, not counted complete lower organisations: a one-level mean-field description has no count of organisations. The shape of what is missing: a lower description that counts complete organisations (for example, N1 lower patches, each a full level), with upper Void fed per completed lower organisation.
- **Checker's disputes, accepted:**
  - (1) *Overclaim.* The upper level now exists for every κ ≥ 0, including κ = 0, so the 10 Nov threshold has not been resolved. It has been **removed by construction**, and with it the only test of whether the upper level can form. In an N-level tower, all of k12 would also pass through every level to the top. That is a strong structural commitment, not a small fix.
  - (2) *Not minimal.* Dispute 1 needs only the σ·x1 term. 'All output goes up' is a separate design choice. The minimal revision is the 10 Nov U = κ·P1·C2 plus σ·x1·V2, and whether a threshold then survives is a question worth running.
  - (3) *Coordinator.* σ·x1 is not a forbidden coordinator: it is a rate that comes from below, not a copied state. It is still a global mean-field share, like every rate here, and templating costs the lower level nothing. κ·C2, which makes every lower unit's exit rate depend on an upper aggregate, should be judged by the same standard.
- **What follows by construction, and is not evidence:** the depletion (C1\* falling as C2 grows) and the seeding both follow from the terms admitted (P2.6-03 §3).
- **Test for a later night, specified, not run.** Run the minimal revision (point 2): the 10 Nov term plus σ·x1·V2, with no routing.
  - Kill line (a code check): the lower level's time-averaged C1 rises when κ is raised with all else fixed.
  - Measurements: whether the upper level forms from C2 = 0 above and below the 10 Nov threshold; and whether either level's clock or bistability survives as κ grows.
  - Planted failure, guaranteed: the upper level gains 2U/ν while the lower loses U. The ledger is then off by exactly U > 0 whenever P1, C2 > 0. (For tonight's routed version, the residual is exactly (k9 + κC2)·P1, as sympy confirmed.)
- **Independent check:** PARTLY. The algebra was confirmed; disputes as above. The checker is Claude.
- **Receipts:** N-2026-11-11-3-algebra.py and -algebra-output.txt; the checker's -checker-a.py.
- **Confidence:** medium. The algebra is exact. The design question is open, on points (1) and (2).

### N-2026-11-11-4: does a published result fix the cost of the cheapest integer-changing path under refinement? (D1)

- **Depth reached:** D1.
- **Result:** partly located. All results below are external, and the comparisons are observational-register readings.
- **Results found:**
  - *Potkina, Lobanov, Jónsson, Uzdin*, 'Lifetime of skyrmions in discrete systems with infinitesimal lattice constant' (arXiv 2111.12014). As the lattice constant goes to zero, the skyrmion collapse barrier saturates at the Belavin–Polyakov bound, 4πJ (some authors write 8πJ, depending on how the exchange is normalised). The entropy part of the Arrhenius prefactor approaches a constant. *Bears:* yes, for the rare branch's shape. The cost stays finite while the number of spins grows without bound. This is the result O_protect already cites, and it is now confirmed at source.
  - *Heil, Rosch, Masell*, 'Universality of annihilation barriers of large magnetic skyrmions in chiral and frustrated magnets' (arXiv 1907.12174).
    - In the chiral (DMI) model with fourth-order gradient coefficient K4 < 0, the barrier of large skyrmions approaches 4πJ from below, as about 4π − 2π(6a/ξ)^(2/3) in units of J.
    - With K4 > 0 it exceeds 4πJ and is set by lattice-scale physics.
    - In frustrated magnets the decay runs through a singular vortex core, at a lattice-dependent cost.
    - *Bears:* partly. A finite, size-independent cost is a universal limit in one regime only. (The checker corrected my first account, which had merged the K4 > 0 and frustrated cases.)
  - *Fujiwara, Suzuki, Wu*, 'Topological charge of lattice abelian gauge theory' (hep-lat/0001029), after Lüscher's admissibility condition (hep-lat/9808021, the primary source).
    - Excising 'exceptional' configurations (sup |F| ≥ ε) leaves the configuration space disconnected, with the integer charge fixed within each part.
    - That the charge cannot change is an inference from this, not a stated theorem. The paper says nothing about the cost of crossing.
    - *Bears:* partly, for the forbidden branch. It is a published example of an integer protected by excluding configurations. Reading it as a gap condition on the step rule is my mapping (the checker's point (c)).
- **Reading:**
  - The rare branch's 'cost need not grow with the number of local changes' has published support for two-dimensional Heisenberg-type magnets. There the finite barrier comes from the scale invariance of the 2D exchange energy, so it is not a general lattice result.
  - These papers measure energy, not a count of local changes. Using them for O_protect is a translation into the project's terms.
  - Nothing found bears directly on the grammar or on the nucleon architecture's integer.
- **Independent check:** PARTLY. All three citations were confirmed; the corrections are taken above. The checker is Claude.
- **Receipts:** none (literature).
- **Confidence:** medium. The citations are confirmed, and the bearing is modest.

**Receipts table** (all in Night-Reports, uploaded from the local files by reference, so the Drive copies are byte-identical; SHA-256 of those bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-11.md | 1kPeSD35TjxHdqUC7FEZntPNawDASU7_8 | 5b09fa5b5b48f9e9af2df9bcd182d22c0e7fea871733baf31732f78efbad15f8 |
| N-2026-11-11-1-cycle.py | 1mJRIl7kLogapR_4xpDYJNG-zPhGs47Ql | 3d35686145c7316f7d950e8b979f3c961edc16c64e5faa8f52351d682d3b709a |
| N-2026-11-11-1-cycle-output.json | 1JFfANELGJf-9oPCsbH_mHW2UoNjBgwFx | 3576f309341e6a3e3c2f63b7b29d5b3464c90154db7560129e11080e1708d5df |
| N-2026-11-11-1-cycle-stdout.txt | 1RuX86OhA4CcDffH7GhpfFJkIOFcRMUWk | b900d6142c91860aec38574bbd5556a091ec6ee1e8d9b767b6248f04acfc2e2a |
| N-2026-11-11-1-diag.py | 1g09gtMaky1b8_pGLVxcK_cjK8d_eS_ol | 4102d418459b7a41eca41af0546c54bb6ba72828f1f3706322b05c4ebda2a76a |
| N-2026-11-11-1-diag-output.txt | 1pCCcNx6SUYhUHrzyMJ1XoyhvS0EjTFgH | 7865b2283aefec2bc3f728ce4fd2604691a191389c1693dbf2e9c22149233251 |
| N-2026-11-11-1-checker-a.py | 1LaxpUQIpsyfGN1qxQpnO89W90R-3xE-c | 36bc64fb079c09b7fef6927faa64017064e42f9e601b769eeba5631c36370534 |
| N-2026-11-11-1-checker-b.py | 1fvw-0S77rrylGVqvoPtogJlIshs0nrUi | 579d06584407a7cdf4567e9a9ba16cf6b65db29c477fb0ea39c26d7fed54945f |
| N-2026-11-11-1-checker-c.py | 1RpK2HaOjuWdoYVbo71Tki2-2sA5J3pjB | 6041e98d64518de2c6d988b4c76a39528b8c85e523f97bfa6c7115f154f8432d |
| N-2026-11-11-2-sym.py | 1nrOOl9PWO4vQKdh3sAau4LnImjsE9Y96 | 52e990e1f941d32ed16423adf9b0575147d0b4b6bdce167a68b41808cec7c5da |
| N-2026-11-11-2-sym-output.txt | 1oVdyuSQ2HeNIVufLPLSQrAgzR9d4S89d | af5f3d6ede86d4160667c69a0ae1991512b711016eae41d669f19ddbef304b15 |
| N-2026-11-11-2-num.py | 1DTO23q7rbXKdmdrYDafl5D7mPtCb8_A6 | 2cda75d5353625f0ac3d1b7fa738da256421e7a75cd871168b7cc57543571d56 |
| N-2026-11-11-2-num-output.json | 1i4HK4zEkSJPVi8OO6vLm7D34dTnixpZm | c173ce265c1c90cb369a47fe3c470c55a467831323e0fb6895fe2ce2d365e671 |
| N-2026-11-11-2-num-stdout.txt | 1ZFK3_MiHknk26YfQYjIiAC8n1Hno6d6d | b61780b8f0aafc58dfe946f3d7cce1aacb59a59174f6be16fe91c84490da10f4 |
| N-2026-11-11-2-mpverify.py | 1vud0NiZavwVUmE5gURMR1tqgBAWYVXD_ | 56b8a8b78f3c32c8044f9328f6fcd98c4e4a3f81eab58a365e04fac2cbb04418 |
| N-2026-11-11-2-mpverify-output.json | 1MxYvO3gJaMqfGhigJM-YF9D_HE0uIUNP | e08d83ad9d08bc09dd110b293c6b7ce5e45f28ac45827c43653b14fbabd0bfde |
| N-2026-11-11-2-mpverify-output.txt | 1wNIMoW7Fgd7SBtGVFCMTDFGLqmD1eYru | 66abd488a91dc55f190498dc08d84ac32e5a80cdb8805aaf4105cd5d28561120 |
| N-2026-11-11-2-checker-sym2.py | 1VlmxGv0MeARYwb8KD0lBQcsjyVM8YCOv | 625638035312dc67b5c1652c72d7e61127d79abf99ee800503a97ab1b10f2998 |
| N-2026-11-11-2-checker-num.py | 1Py9HeHQjnqbdd8QRERtNPokJf7KB7_sK | 16815e269de5d3e0a826edddbdf89ad06905e2ef39ec264e001b986100929420 |
| N-2026-11-11-2-checker-num2.py | 1znaFTvoyrVAXdkKe9dHuxy83KYUMuwoj | 97bb6ca21f33748a56a9e59844d8312904bca3762e47648a490132b993790a3d |
| N-2026-11-11-2-checker-full.txt | 12e2v_AAGXRSWQyuVmn1BwG3dY7hVA3AL | 7e2d9942751ee6eb644df080ad966ba0ca3c6c8e54f64ecf964e03714b647c8d |
| N-2026-11-11-3-algebra.py | 1ZmE93m3bleVIfkfPeaFtXSBSsrOae0Tn | f430ad35fa09ff71539409df67b2b0c029b2d90119de0c08c4e524e654ac70e5 |
| N-2026-11-11-3-algebra-output.txt | 12frDOETkWUL-YsWsDLgUdc5MIXlcjN8Y | c21b0093ee5ef336486f45916cd6b12997d08da0148800f2497276ac09f4a89b |
| N-2026-11-11-3-checker-a.py | 1dPnujIpdvvtnj2BN2h4e-jApYFe4dTDu | 9ba57a6bbdb61fdee58ff35353a663d49995b7c80c49eabd4884a7f773fb37da |
| MAP-SNAPSHOT-2026-11-11.md | 1FXpXgg9QeYMY9cOJgp-byjanigysruMY | 2d245795a1de11a9311aa2ffa523a1b96b7902c8d10618eb6169d761e7ee1489 |

## 5. New candidates (post-failure)

None. No candidate failed tonight. The outcome of item 1 is a measurement, not a failed candidate. The outer instability in item 2 refutes a conjecture; it does not fail a candidate. Item 3's disputes were raised against a specification before any run. Nothing was revised in response to a result.

One harness lesson is logged, not a candidate. Item 1's frozen classifier used an absolute rest tolerance (10⁻⁶) and a fixed run length (2×10⁴), which together could not certify rest against a slow mode of rate 10⁻⁴. The classifier was not changed after the run. A better rule is suggested for later nights in section 7.

## 6. Suggested Map changes for Glenn to decide

These are recommendations only.

1. **K_bal: add the closed-level result next to the open one** (this assumes the 10 Nov open-level recommendation is taken).
   - *Proved \[theorem, model\]:* on a closed level, the determinant within the conservation class equals k8·(k5 + k6)·H′(x\*) at every balance, so the middle of three balances is always unstable. Together with 10 Nov, that makes the middle balance unstable on every level.
   - *Refuted:* 'the outer two are always stable', on closed levels as on open ones.
   - *New:* a closed level can have all three balances unstable (5 in 20 000 three-balance draws).
   - Receipt: N-2026-11-11-2, check PARTLY. The mathematics was confirmed; the disputes were on counts and wording, and are taken in.
2. **O_drift: update its shape line.** 'Stability of the three is the open step' could become: middle unstable, proved for open and closed levels; outer stability not guaranteed, with the high-Contact side the usual one to go; some closed levels have no stable balance and must keep moving. Add that the one open case tested (m = 27, kr = 7) has no resting–ticking pair: the unstable focus is transient. Receipts: N-2026-11-11-1 (CONFIRMED) and N-2026-11-11-2.
3. **G_species / O_focus: consider noting** that a level with no stable balance is a candidate home for a clock that does not need fine-tuning. This is a pointer only; it has not been computed. Receipt: N-2026-11-11-2.
4. **C_seed: record tonight's revision as a second candidate coupling,** with the checker's verdict attached: dispute 1 is resolved by the seeding term alone; 'all output goes up' removes the existence threshold by construction and is not minimal; dispute 2 is only partly resolved. Do not regrade C_seed. Receipt: N-2026-11-11-3, check PARTLY.
5. **O_protect: add a note under its shape.** The skyrmion citation is confirmed at source (Potkina et al., arXiv 2111.12014). Heil–Rosch–Masell (arXiv 1907.12174) gives the regime in which a finite barrier that does not depend on size is universal (chiral magnets with K4 < 0), and the regimes in which it is not. Lüscher's admissibility condition (hep-lat/9808021; Fujiwara–Suzuki–Wu, hep-lat/0001029) is a published example for the forbidden branch, as an exclusion of configurations. All of this is 2D or lattice-gauge specific. Receipt: N-2026-11-11-4, check PARTLY.

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **What does a level with no stable balance do? (D3).**
  - Integrate the five closed draws with all three balances unstable (2045, 301417, 384616, 456280, 616482; their rates can be regenerated from seed 20261111 with N-2026-11-11-2-num.py, or taken from the receipts for 2045 and 301417).
  - Classify the attractor: a cycle, or something else.
  - If it is a cycle, compute its Floquet multipliers in the class. Two of them should be at 1, from phase and from the total.
  - This is the best current lead for a one-level clock in the working grammar.
- **The minimal C_seed revision, run (D3).** Run the 10 Nov term plus σ·x1·V2, with no routing, using the frozen kill line and plant from item 3. Does a formation threshold survive?
- **A sounder classifier for slow systems (harness, D1).**
  - Declare 'rest' by the residual |f(y)| relative to the scale of the rates, together with a contraction check over the last stretch, not by distance to a balance at a fixed time.
  - Or integrate to at least 10/|λ_slow|.
  - Allow periods up to the run length / 20.
- **Census of outer instability, open and closed (D2).** Both harnesses can now be re-run from their seeds. Which m, kr and rate regimes put the unstable outer balance on the high-Contact side, and which allow both outer balances to go?
- **Floquet multipliers of clocks 19387 and 33538 (D3).** Carried over. This needs their rate vectors from pull request 7.

## 8. Verification handoffs

```
Task (DeepSeek). Closed level: roles C,V,L,P >= 0, T = C+V+L+P conserved, x = C/T, rho(x) >= 0 differentiable, all rates positive:
dC/dt = -(k1+k2+k7)C + k6 L + (k10+rho(x))V
dV/dt = k2 C + k5 L + k8 P - (k10+rho(x))V
dL/dt = k1 C - (k5+k6) L
dP/dt = k7 C - k8 P
At a balance, C = xT, L = k1 x T/(k5+k6), P = k7 x T/k8, V = T(1 - c x), c = 1 + k1/(k5+k6) + k7/k8, where x solves H(x) = (k10 + rho(x))(1 - c x) - D x = 0, D = k2 + k7 + k1 k5/(k5+k6).
Prove or refute: the sum of the four principal 3x3 minors of the Jacobian J (equivalently, the product of the eigenvalues of J restricted to the invariant subspace {dC+dV+dL+dP = 0}) equals k8 (k5+k6) H'(x) at every balance, for every rho and every T > 0. Then state what follows for the stability of the middle of three simple balances.
```

```
Task (Astra / DeepSeek). Same closed level with rho = k3 * P[Bin(m, x) >= kr] (regularised incomplete beta I_x(kr, m-kr+1)), T = 1, m = 19, kr = 3,
(k1, k2, k3, k5, k6, k7, k8, k10) = (0.47205648482747253, 0.026204658014680544, 33.767749788910784, 0.04225910243329335, 0.030726928960954643, 36.36991748036593, 59.878770174623746, 0.8229214570079602).
(1) Find all balances (roots of H on (0, 1/c)) and the eigenvalues of J restricted to the class at each. Confirm or refute that all three are unstable. (2) Integrate from several starts in the class and classify the long-run behaviour (cycle, torus, chaos, other). If it is a cycle, report its period and Floquet multipliers, identifying the two trivial ones.
```

## 9. Run notes

- **Access.** Every required source was reached:
  - the spec (v2.1, ID 1sgnU86…, exact title);
  - STEERING.md;
  - the standing constraints (the current copy, ID 1LjICJx…, exact title and 'CURRENT' description);
  - the Premise Map, read in full through the Artifact tool (version 1794281872-597e) and parsed to JSON;
  - the 10 Nov and 9 Nov reports and the 10 Nov snapshot;
  - the saturation note.
  The project instructions were in context. The narrative spine (context only) was not opened, for time.
- **Map diff method.** The 10 Nov snapshot was read as text through the Drive connector, but it could not be passed into the sandbox without retyping it. The diff therefore rests on the identical version string, the identical node set and counts, and the identical snapshot size apart from tonight's added header sentence.
- **Freeze.** The queue was saved as its own file at 06:24:59 UTC, before any item's work. It was uploaded by file reference, so the Drive copy is byte-identical.
- **Changes to scripts before any result was read, logged here:**
  - Item 1:
    - The monodromy routine was changed from a terminal event, which would have fired at the start point, to 'the first upward crossing after half the estimated period, over 1.5 periods'.
    - A duplicated guard-plant call was removed.
    - Both changes were made before the first run. The monodromy routine was used only on the controls, since no cycle was found.
  - Item 2: a sympy substitution error (differentiating with respect to a compound expression) was fixed before the symbolic script produced any output.
- **Item 1 interpretation.** The frozen verdict for all six starts is 'other'. The finding stated in section 4 rests on a report-only diagnostic and on the checker's independent longer runs, and is labelled as such.
- **Item 2 storage.** The harness stored only the first 200 outer-unstable flags; 198 of them were high-share. The five no-stable-balance draws were identified by the checker's re-run of the same seeded draws. My harness's counts (546 high-share, 7 low-share) agree with it exactly.
- **Checks.** Three fresh Claude subagents, none of which had seen the working, checked: item 1, item 2, and items 3–4 together. The item 1 and item 3–4 checkers ran while later items were being worked. Their verdicts and disputes are in section 4. Their scripts are uploaded as receipts.
- **Time.** About 06:20–06:55 UTC. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports. Nothing else was edited.
