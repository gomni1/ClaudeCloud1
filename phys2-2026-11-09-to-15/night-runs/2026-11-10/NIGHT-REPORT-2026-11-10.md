# NIGHT-REPORT-2026-11-10

PHYS2 Night Run, second night. Claude, unattended, 10 Nov 2026, from about 06:20 UTC. It promotes nothing, closes nothing and renames nothing. Everything below is a recommendation.

## 1. Top line

Glenn's first pin has a clean answer in two parts. The middle of three balances is always unstable: on an open level, the Jacobian's determinant equals k7·k9·(k5 + k6)·g′(V*) exactly, so it takes the sign of the slope of the balance curve, and at the middle balance that slope is negative. The outer two are not always stable. A verified case (m = 27, kr = 7) has its low-Void balance losing stability to an oscillating pair while its high-Void balance stays stable. In the main search, 212 of 12 264 three-balance draws had an unstable outer balance, every one on the low-Void side, and all 212 were confirmed at 50 digits. So one level can hold a resting organisation and an oscillating one side by side, and 'at most two stable resting organisations' is an upper count, not a description.

The second pin is specified, not run. One bilinear uptake term, the upper rung's Contact meeting the lower rung's breach-ready units, makes the coupling two-way and conserves every unit. With it, the lower rung's Contact falls as the upper rung grows, and the upper rung's supply saturates at the lower rung's throughput. Both follow by construction, so they are a specification, not evidence. The checker found two real problems: the term feeds the upper rung but cannot seed it, and it moves single units in one currency, which sits close to the forbidden one-to-one handoff.

The newest Known node, 'With positive-weight turnover, sharper timing does not cost extent', still counts the copy-the-state ensemble (E3) as support, although the 10 Nov wall 'No coordinator above a level' names E3 as a violation. Without E3, the node holds for single units and for non-interacting copies only. A literature pass found the known positive-weight bounds (thermodynamic and kinetic uncertainty relations): all of them sharpen timing and position together as the drive or the activity rises, and none gives a floor. That is consistent with the node, but it does not prove its general claim.

## 2. Frozen queue

The queue was frozen before any item's work began, saved to Night-Reports as NIGHT-QUEUE-2026-11-10.md (Drive ID 1h81kRXLAF_iW_iPvdakjQqW41r8XT4Lx, created 06:23:03 UTC) and not altered afterwards. SHA-256 of the uploaded file: ea13e9bad6b731307265980ece11a6941fecddf6970124c3a3d7396953acf10b. Its full text follows unchanged.

> # NIGHT-QUEUE-2026-11-10
>
> PHYS2 Night Run, second night. Claude, unattended. Frozen 10 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.
>
> ## How the queue was built
>
> - **Sources read:** NIGHT-RUN-SPEC.md v2.1; STEERING.md (two PIN lines, no SKIP or RETIRED lines, one NOTE); PHYS2-STANDING-CONSTRAINTS.md (file ID 1LjICJxBfjMmma25W_2r3egpFpoYt_UJA, amended 10 Nov, description "CURRENT standing constraints"); the Premise Map (version 1794281872-597e, 177 nodes); NIGHT-REPORT-2026-11-09.md and its suggested follow-ups; NOTE-Saturation-Mechanism-2026-11-06.md (the grammar's equations). No REVIEW notes exist in Night-Reports.
> - **Priority 1, STEERING PIN:** items 1 and 2, in Glenn's order.
> - **Priority 2, last night's follow-ups:** stability of the three balances (= PIN 1); C_seed back-reaction (= PIN 2); isolation of cycles (item 5); literature check on O_protect's 'rare' branch (carried over, see below); harness planted-failure rule (now covered by spec v2's planted-failure section, so not queued).
> - **Priority 3, map regions changed since the 9 Nov snapshot:** K_tradeless and O_signed (placed 10 Nov). The 10 Nov standing-constraints amendment added the wall 'No coordinator above a level' and names the 10 Nov run's E3 ensemble as a violation, while K_tradeless still cites E3 counts as Known (item 3). Glenn left O_signed to the night run's choice (item 4).
> - **Excluded:** nothing is on STEERING SKIP or RETIRED. The standing constraints' Closed list (charmonium selection, Candidate B, free random swap/flicker, the compact trans-scalar grammar, charge as the unpaired half-twist, the P2.6-03 §5 list) and the 'Open and not load-bearing' list were excluded. Archive and Outcome nodes were excluded.
> - **Ranking (effort versus impact):** PINs first in order; then item 3 (easy, high: a Known node possibly resting on a forbidden move); item 4 (moderate effort, moderate-high: a published theorem may already settle half of a gap); item 5 (easy, moderate: shape only).
> - **Carried over, not queued tonight:** the O_protect 'rare' branch literature check (D1). Reason: tonight's literature slot goes to item 4, which touches a node placed yesterday.
>
> **Transparency note (item 1).** While reading the saturation note to build this queue, Claude saw how the determinant identity for item 1 probably goes: replace the V-row of the Jacobian by the sum of all rows, which is (0, 0, 0, −k9), and expand; the result should be det J = k7·k9·(k5 + k6)·g′(V*). This is declared here before any working. The identity is to be proved symbolically in item 1, and the numerical part below is fixed now, so it does not depend on whether the outline is right. The outline says nothing about the outer two balances. Claude also notes, from the map's 'Clocks exist…' node, that an open level with kr = 2 (draw 33538) has a Hopf-unstable balance in the working grammar; whether an outer balance of a three-balance level can be unstable is therefore a live question, and the numerical search below is built to answer it either way.
>
> ---
>
> **N-2026-11-10-1 — Stability of the three balances (STEERING PIN 1)**
> - **Target:** K_bal ('One level holds at most three balances under threshold recruitment'), its 'Not shown' clause; O_drift ('Does a species' attractor drift in the working grammar?'), whose shape names stability of the three as the open step.
> - **Task:** given rule R, the open level of the working grammar (roles C, V, L, P; k11 = 0; all-neighbours count x = C/T; ρ = k3·F(x), F(x) = Pr[Bin(m, x) ≥ kr]; all listed rates positive; kr ≥ 2), determine (a) whether the sign of det J at a balance is fixed by g′(V*), where g(V) = (k10 + k3·F(C*/(C* + L* + P* + V)))·V; (b) whether, when three balances exist, the middle one is always unstable; (c) whether the outer two are always stable.
> - **Inputs:** NOTE-Saturation-Mechanism-2026-11-06.md (equations, S2, S4, appendix eigenvalues and example rates); K_bal; K_clock (open clock 33538).
> - **Depth:** D3 Probe. One attempt: a symbolic proof of (a), (b) by consequence, and one bounded numerical search for (c).
> - **Effort cap:** about 35% of the night.
> - **Done means:** (a) proved or refuted symbolically, with the exact relation; (b) stated as following or not; (c) either a verified counterexample (an outer balance with an eigenvalue of positive real part) or 'no counterexample in N draws', with the count, which is not a proof.
> - **Mechanism, specified now:**
>   - *Symbolic (sympy):* build the 4×4 Jacobian of the open-level right-hand side with F left as an undefined function of x, evaluate at a balance using S2's pins (P* = k12/k9, C* = (k8 + k9)·k12/(k7·k9), L* = k1·C*/(k5 + k6)) and V* free, and simplify det J − k7·k9·(k5 + k6)·∂f_C/∂V; separately check that ∂f_C/∂V at fixed C, L, P equals g′(V). Result (a) holds only if both simplify to 0 identically.
>   - *Numerical harness (Python, numpy/scipy, no ODE integration):* draws with rates k1, k2, k3, k5, k6, k7, k8, k9, k10, k12 log-uniform in [10⁻², 10²], m uniform in 2..30, kr uniform in 2..m, seed 20261110. For each draw compute the pins, then find every balance as a root of G(x) = (k10 + k3F(x))(α − βx) − γx on (0, α/β) (α = C*, β = C* + L* + P*, γ = D·C*), by sign changes on a 4 000-point grid including the exact end signs, refined by brentq; map x → V* = α/x − β = C*/x − (C* + L* + P*). Keep only draws with exactly three roots. At each of the three balances: analytic Jacobian (with F′ from the beta density), its eigenvalues (numpy.linalg.eigvals), det J, and g′(V*) by its closed form. Per draw keep only summaries: the three V*, the three max Re λ, the three relative errors |det J − k7k9(k5+k6)g′| / (|det J| + k7k9(k5+k6)|g′|), flags.
>   - *Checks while running:* identity flag if relative error > 10⁻⁶; middle-stable flag if the middle balance has max Re λ ≤ 0; outer-unstable flag if an outer balance has max Re λ > 10⁻⁹·max|λ|. Any outer-unstable flag is re-verified in mpmath at 50 digits (balance re-solved, eigenvalues recomputed) before it is reported as a counterexample.
>   - *Reproduction check (must pass before the main loop):* the note's example (m = 10, kr = 6, rates in the appendix) must give three balances with V* ≈ 2.589, 14.394, 79.747 and eigenvalues matching the appendix to 3 decimals.
>   - *Planted failures, both guaranteed analytically:* (P1) for the identity check: at the first 200 three-balance draws, also test a Jacobian whose (C, V) entry is shifted by δ = 0.5·|g′(V*)| + 1. The determinant is linear in that entry with coefficient k7·k9·(k5 + k6) (its cofactor, by the same row reduction), so the plant's det differs from the identity by exactly k7·k9·(k5 + k6)·δ > 0, a relative error of at least δ/(2|g′| + δ) ≥ 1/3 > 10⁻⁶ whatever the draw. Note: this guarantee uses the cofactor claim, which is part of what (a) proves; so P1 is guaranteed only if (a) holds, and if (a) fails P1's result is not interpreted. (P2) for the stability classifier: at the same 200 draws, also classify J + s·I with s = 1 − max Re λ(J) at the most stable balance. The eigenvalues of J + sI are exactly λ + s, so its max Re λ is exactly 1 > 0; it must be flagged unstable. If P1 or P2 fails to trip in any of its 200 cases, the harness is declared blind and the numerics are not a receipt.
>   - *Sizing:* a pilot of 2 000 draws is timed first and written into the run notes; the main loop then runs until 20 000 three-balance draws are collected or 45 minutes of wall time pass, whichever first.
>   - *Kill lines, fixed now:* (a) is refuted by any symbolic remainder ≠ 0, or by any verified identity flag. (c) 'outer two always stable' is refuted by any mpmath-verified outer-unstable case. Nothing else is a kill.
>
> **N-2026-11-10-2 — The smallest two-way resource coupling (STEERING PIN 2)**
> - **Target:** C_seed ('Growth depletes the rung beneath'), half (i), and its shape line; A_share ('Shared supply within aggregate capacity; each unit counted once'); F_ladder; P_fedbelow.
> - **Task:** given A_share, F_ladder, P_fedbelow and the single-level equations, specify the smallest two-way resource coupling between two levels in which the upper rung's uptake appears as a loss or an exclusive commitment in the lower rung's balance, and binds when the lower rung's capacity binds. State what it adds to the one-way ladder, what it must not add (no coordinator above a level; no one-to-one handoff bookkeeping; no fitting), and what a later run would test, with a kill line. Specification only; no run.
> - **Inputs:** C_seed, A_share, F_ladder, P_fedbelow, K_ladder, K_sat (S1, S2), the saturation note's equations, the standing constraints (forbidden moves).
> - **Depth:** D2 Shape.
> - **Effort cap:** about 20%.
> - **Done means:** a written specification: the coupled equations, each new term's justification against A_share and F_ladder, the conservation identity it must satisfy across the two levels, what it changes relative to the one-way ladder, and a candidate test with a kill line and a planted failure for a later night. Explicitly not run.
> - **Mechanism:** none tonight (specification only). Any algebra checked by hand or with sympy, for consistency only (no dynamics run).
>
> **N-2026-11-10-3 — Does 'With positive-weight turnover, sharper timing does not cost extent' rest on a forbidden move?**
> - **Target:** K_tradeless (placed 10 Nov), against the standing-constraints wall 'No coordinator above a level' (added 10 Nov), which names the 10 Nov run's E3 ensemble as a violation.
> - **Task:** audit chain C for smuggling. Locate which clauses of K_tradeless's statement, status and follows rest on E3 (copy-the-state) results, and whether the Known statement survives with E3 removed.
> - **Inputs:** K_tradeless and O_signed node texts; TIMING-EXTENT-TRADE-2026-11-10.md; the standing constraints.
> - **Depth:** D1 Locate.
> - **Effort cap:** about 10%.
> - **Done means:** crack yes or no; if yes, the exact clauses, and what remains supported by the single-unit and independent (E2) results.
> - **Mechanism:** none; a text audit.
>
> **N-2026-11-10-4 — Does a published result already settle the positive-weight half of 'Signed or phased handoff contributions'?**
> - **Target:** O_signed (placed 10 Nov) and the K_tradeless status line 'the general claim that no positive-weight rule can give the floor is argued, not proved'.
> - **Task:** given rule class R (positive-weight step processes: Markov jump processes and random walks with drive, including the telegraph/persistent walk), locate whether a published result proves or refutes that such rules can have a positive infimum of (timing width × spatial extent) under unbounded drive. Candidate literatures to search, before any attempt: thermodynamic and kinetic uncertainty relations (including first-passage-time versions), persistent random walk / telegraph process variance results, and the Gaveau–Jacobson–Kac–Schulman analytic continuation.
> - **Inputs:** O_signed, K_tradeless; web search.
> - **Depth:** D1 Locate.
> - **Effort cap:** about 15%.
> - **Done means:** a list of the published results found, each with what it bounds and whether it bears on the infimum (yes / partly / no), and a one-line verdict: settled by literature, partly, or not located. No new proof.
> - **Mechanism:** none; a literature search. Observational and external results labelled as such.
>
> **N-2026-11-10-5 — What would show a level's clocks are isolated?**
> - **Target:** G_species's isolation half, whose status says 'Isolation of cycles rests on two examples only'; O_focus; O_drift's shape.
> - **Task:** given structure S (one level of the working grammar, open or closed, with a periodic orbit), state the invariant I whose computation would establish isolation of the cycle within its conservation class (Floquet multipliers), what must be excluded (the trivial multiplier from phase; on a closed level the multiplier from the total), and why the closed level's scaling with T makes cycles a one-parameter family in amounts but isolated in shares and period. Shape only.
> - **Inputs:** K_clock, K_sat (S5), K_bal, G_species, O_drift.
> - **Depth:** D2 Shape.
> - **Effort cap:** about 10%.
> - **Done means:** a written criterion, the smallest assumption involved, what depends on it, and a candidate check for a later night. No computation tonight.
> - **Mechanism:** none.
>

## 3. State changes noticed

- **Map diff.** The map was version 1794023894-eb69 on 9 Nov and version 1794281872-597e tonight. It has 177 nodes, up from 173. By type: Known 52 (was 50) and Gap 19 (was 17); the other types are unchanged. By shelf: 94 live (was 91), 15 Reserve (was 14), 8 Reservoir and 60 Archive.
  - **Added:** K_bal ('One level holds at most three balances under threshold recruitment', Known, 9 Nov). O_drift ('Does a species' attractor drift in the working grammar?', Gap, 9 Nov). K_tradeless ('With positive-weight turnover, sharper timing does not cost extent…', Known, 10 Nov). O_signed ('Signed or phased handoff contributions', Gap, 10 Nov).
  - **Changed (9 Nov, Glenn's 'do the lot'):**
    - K_sat retitled: 'cycling needs a lag' became 'needs a route through L or P'. The check is recorded on the node.
    - G_species retitled to its isolation half, with K_bal added to its deps.
    - C_deficiency moved from live to Reserve.
    - P_traj's illustrative mechanism reworded. Its promotion is unchanged.
    - C_seed was given the shape of its back-reaction gap.
  - **Removed:** none.
  - **How the diff was made:** the node set and the counts were compared by machine. Field-level changes were taken from the map's timeline (9–10 Nov events) and confirmed on each node named there. A line-by-line machine diff of deps and tests against the 9 Nov snapshot was not run (see section 9).
- **Standing constraints.** They were amended on 10 Nov, and the new copy is file ID 1LjICJxBfjMmma25W_2r3egpFpoYt_UJA, titled exactly PHYS2-STANDING-CONSTRAINTS.md, with the description 'CURRENT standing constraints'. Two changes were made. The forbidden move 'No coordinator above a level' was added, naming the 10 Nov E3 ensemble. 'Charge as the unpaired half-twist' was added to the Closed list. The id named in the spec (1YmP6…) is now titled SUPERSEDED, and was not used.
- **Steering applied.** The two PIN items became items 1 and 2, in Glenn's order. There were no SKIP or RETIRED lines. The NOTE (spec v2 applies) was followed, under v2.1.
- **Previous follow-ups:**
  - Stability of the three balances became PIN 1.
  - The C_seed back-reaction became PIN 2.
  - Isolation of cycles became item 5.
  - The O_protect literature check is carried over.
  - The harness planted-failure rule is now covered by spec v2.
- **REVIEW notes:** none in Night-Reports.

## 4. Results, per item

### N-2026-11-10-1: stability of the three balances (D3, STEERING PIN 1)

- **Depth reached:** D3.
- **Crack found:** yes, both ways. One half of the conjecture is now proved, and the other half is refuted.
- **(a) Proved [theorem, model].**
  - At every state of an open level, and for any recruitment function ρ(x), det J = k7·k9·(k5 + k6)·∂f_C/∂V. At a balance, ∂f_C/∂V (taken at fixed C, L, P) equals g′(V*).
  - So det J = k7·k9·(k5 + k6)·g′(V*). The sign of the determinant is the sign of the balance curve's slope. Note that this is +g′, not −g′: for a 4×4 matrix, a stable balance has det J > 0.
  - Proof: the four right-hand sides sum to k12 − k9·P, so replacing the V-row of J by the sum of all rows gives (0, 0, 0, −k9). Expanding along that row, and then along the V-column, leaves the factor ∂f_C/∂V. sympy confirms the remainder is identically 0 at any state, and also at the throughput pins.
- **(b) Follows.** With three simple balances, g(0) − D·C* < 0 and g − D·C* → +∞, so g′ is positive, negative, positive at the low-Void, middle and high-Void balances. At the middle balance det J < 0. A real 4×4 matrix with a negative determinant has a positive real eigenvalue, so **the middle balance is always unstable**.
- **(c) Refuted: the outer two are not always stable.**
  - A three-balance level can have its **low-Void (high Contact share) balance** unstable through a complex pair with positive real part. There g′ > 0 and det J > 0, but two eigenvalues have crossed: an oscillatory, Hopf-type instability.
  - Verified example (pilot draw 318; m = 27, kr = 7; rates in the receipt): low-Void balance V* = 41.1404511944, eigenvalues 0.8664 ± 15.778i, −0.000795, −0.1127. The middle balance is a saddle, with eigenvalue +36.44 (checker). The high-Void balance is stable.
- **Search (frozen harness):**
  - 425 454 draws in the 45-minute cap; the 20 000 target was not reached. 12 264 draws had three balances (2.9%); every other draw had one.
  - Identity: 0 flags; the largest relative error was 8.9×10⁻¹⁰.
  - Middle balance stable: 0 cases. The smallest middle max Re λ was +0.0154.
  - **Outer balance unstable: 212 draws (1.7% of three-balance draws), all at the low-Void balance, none at the high-Void balance**, and no draw with both.
  - All 212 were re-verified at 50 digits. 200 came from the stored cases; the output kept only 200 cases, so the remaining 12 were re-verified by replaying the seeded draw sequence. Every one was unstable, with residuals below 10⁻³⁰.
  - The cases spread over kr = 2 to 23, most often at small kr. By kr: 2: 61, 3: 46, 4: 24, 5: 21, 6: 21, 7: 10, 8: 9, 9: 5, 10: 6, 11: 2, 12: 3, 13: 1, 16: 2, 23: 1.
  - That the high-Void balance was never unstable is an observation over 12 264 draws, not a proof.
- **Harness status:**
  - *Reproduction check:* V* = 2.589, 14.393, 79.746, and eigenvalues within one unit of the third decimal of the appendix. On the strictest reading of 'match to 3 decimals' this fails by one unit (−15.249 against −15.248, 3.528 against 3.527, and V* 14.393 against 14.394). The reading taken was 'agree to 3 decimals up to rounding of the published rates'. The checker found a rate vector inside the appendix's rounding box that reproduces every published figure, so the difference is rounding.
  - *Planted failure P2* (stability classifier, J + sI; guaranteed analytically): tripped in 200 of 200. **The stability numerics are a receipt.**
  - *Planted failure P1* (identity check) tripped in 200 of 200, but **its stated guarantee was false**. The queue claimed that shifting only the (C, V) entry changes det J by k7·k9·(k5 + k6)·δ. The true change is δ times the (C, V) cofactor, which is a different expression and not of fixed sign (sympy; checker). The smallest relative error seen was 0.0025, not the claimed ≥ 1/3.
  - By the spec, a plant that is not analytically guaranteed is not a sound plant. **The numerical identity agreement is therefore not a receipt.** Part (a) rests on the symbolic proof, which is exact and was re-derived by the checker. The failure is left on record; a sound plant is noted in section 5 as a post-failure idea only.
- **What it means:**
  - A level with three balances never rests at the middle one.
  - It can sit at the high-Void balance while its other candidate resting state, the high-share one, is replaced by an oscillation. So one level can carry a resting organisation and a ticking one side by side, if the oscillation settles to a cycle; that is not checked tonight.
  - 'At most two stable balances' now holds as a proved upper count: the middle one is never stable.
  - O_drift's 'stability of the three is the open step' is answered for the middle balance only. For the outer two, stability is not structural.
- **Not shown:**
  - The closed level. There the 4×4 determinant is identically 0 (checker), so the argument needs the 3×3 restriction to the conservation class.
  - Folds (g′ = 0).
  - Whether the unstable outer balance feeds a limit cycle.
  - Whether the high-Void balance can ever go unstable.
- **Independent check:** CONFIRMED for (a)–(d). It also confirmed the P1 guarantee is false, as the working had found before the checker reported. Its list of what (b) does not show is taken into 'Not shown' above. The checker is Claude; DeepSeek should check (a) and (c) (see section 8).
- **Receipts:** N-2026-11-10-1-sym.py and -sym-output.txt; -num.py, -num-output.json, -num-stdout.txt and -num-perdraw-summary.json; -pilot.json; -mpverify.py, -mpverify-output.txt, -mpverify-rest.py and -mpverify-rest-output.txt; the checker's -checker-num.py and -checker-sens.py. IDs and hashes are in the receipts table.
- **Confidence:** high for (a) and (b), an exact symbolic identity re-derived independently. High for (c), with 212 counterexamples verified at 50 digits and the example re-derived by the checker.

### N-2026-11-10-2: the smallest two-way resource coupling (D2, specification only)

- **Depth reached:** D2. Nothing was run. The algebra was checked for consistency only, in sympy.
- **Crack found:** yes. The shape of C_seed's gap can now be written as equations, and doing so exposes two seams the shape line did not mention.
- **The specification.** Two levels each use the working grammar: the lower one with rates k, the upper one with rates u. One term is added:
  - U = κ·P1·C2. This is an encounter between the lower level's breach-ready units (P1) and the upper level's Contact (C2).
  - U enters as −U in dP1/dt and as +U in dV2/dt, and it is the upper level's only supply. Supply arrives as Void, as 'Each level is fed and seeded…' says.
  - The lower level keeps its own exit k9·P1, and the upper level keeps u9·P2.
  - Nothing else changes. Seeding (k10, u10) stays as each level's own term.
- **Why each term:**
  - *Two-way.* U depends on the state of both levels. Bilinear is the lowest degree at which this happens; κ·P1 alone would be one-way.
  - *Each unit counted once.* U leaves one balance and enters the other. The sympy check gives d(T1 + T2)/dt = k12 − k9·P1 − u9·P2, with U cancelling.
  - *Binds at capacity.* At the lower level's balance, given C2, U* = κ·C2·k12/(k9 + κ·C2), which tends to k12: the upper level can never draw more than the lower level's throughput.
  - *No coordinator.* No unit copies or follows a shared variable. U is a rate term in C2, the upper level's own amount.
- **What follows, by construction:**
  - The lower level's pins become P1* = k12/(k9 + κ·C2) and C1* = (k12/k7)(1 + k8/(k9 + κ·C2)).
  - C1* falls strictly as C2 grows, from k12(k8 + k9)/(k7·k9) down to k12/k7. That is 'growth depletes the rung beneath' in definite form.
  - Joint balance: C2* = 0, or C2* = c·k12 − k9/κ with c = (u8 + u9)/(u7·u9). So the upper level exists only if κ·c·k12 > k9: its uptake must out-compete the lower level's other exit.
  - Above that threshold any small seed grows (checker, from linearising at C2 = 0). So 'seeds are not arbitrarily small' still does not follow.
- **What this does not show.** The depletion is built in by admitting U, so it is not evidence (P2.6-03 §3). The open questions are:
  - whether such a term is entitled, which is the rate-law gap;
  - what U does to the dynamics, for example whether the upper level's growth can push the lower level out of a clock regime or into bistability.
- **Test for a later night, specified now, not run.**
  - Run: both levels in the working grammar with U.
  - Kill line: a two-level run in which the lower level's time-averaged Contact rises when κ is raised with all else fixed. The algebra says it must fall, so this kill line is a check of the code.
  - The substantive measurement: whether either level's clock or bistability survives as κ grows from 0 past the threshold. There is no kill line on that, since it is a measurement.
  - Planted failure, guaranteed analytically: give the upper level 2U while the lower level loses U. The cross-level identity is then off by exactly κ·P1·C2 > 0 whenever P1 and C2 are positive.
- **Independent check:** PARTLY. The algebra was confirmed in sympy. The checker's disputes, as given:
  - (1) 'Because U ∝ C2, C2 = 0 is invariant: the lower level feeds the upper but cannot seed it.' So 'fed and seeded' is met only for feeding. Accepted, and logged.
  - (2) 'U moves one breach-ready unit into one upper Void unit, in the same currency', which is close to the forbidden one-to-one handoff. It also cuts against the ladder's 'complete organisations at R(n−1) are the resources': as written, the upper level is a second compartment at the same scale. The checker suggests a conversion factor (ν lower units per upper unit, or uptake per completed lower cycle). Accepted as unresolved.
  - (3) The pairing P1·C2 is a choice; P1·V2 or C1·C2 are equally small. So this is 'a minimal coupling', not 'the minimal coupling'. Accepted.
  - (4) Mass action is a well-mixed mean field: 'local pairwise encounter' is asserted, not built. Accepted as a flag.
  - The checker agrees it is not a coordinator in the E3 sense, and that depletion is not evidence.
- **Receipts:** N-2026-11-10-2-algebra.py and N-2026-11-10-2-algebra-output.txt (IDs and hashes in the receipts table).
- **Confidence:** medium. The algebra is exact. Whether this is the right coupling is open on the checker's points (1) and (2).

### N-2026-11-10-3: does K_tradeless rest on a forbidden move? (D1)

- **Depth reached:** D1.
- **Crack found:** yes.
- **Where:**
  - K_tradeless's statement: 'in every classified ensemble stratum the drive-timed event is CO-SHRINK (208 of 208 independent, **318 of 318 copy-the-state**)'.
  - The same statement: '**with copying, run-to-run noise stops improving with N (slope 0.00 at ρ = 0.9)**'.
  - Its status: 'Known for these candidates only: R1-clock, ensembles E2 and **E3**…'.
  - 'Ensembles do not change this', in so far as it generalises over E3.
  - All four rest on E3, in which every primitive copies one shared two-state organisation variable. The 10 Nov wall 'No coordinator above a level' names exactly this ('its ρ > 0 results rest on that variable'). The node's own follows line already flags the variable as 'load-bearing and not earned', but the Known statement still counts it.
- **What survives with E3 removed:**
  - The single-unit result: infimum 0 of Δt·Δx over the uncapped range, proved (class A, Q2).
  - E2 (independent primitives): CO-SHRINK in 208 of 208 classified strata, and N^(−1/2) averaging. The latter is the central limit theorem for identical, independent copies.
  - So the Known stands for single units and non-interacting copies. That is a much thinner ensemble claim: an interacting ensemble without a coordinator was not tested.
  - The two inheritance rules (H-nominal and H-realised) are defined on a unit's own velocity, single-unit first (TIMING-EXTENT-TRADE Q2), so they survive. O_signed is untouched, since it rests on positive weights, not on E3.
- **Independent check:** CONFIRMED, with two flags.
  - (1) 'Confirm that H-nominal and H-realised are definable without E3's shared variable.' They are: Q2 defines both for a single unit.
  - (2) 'In E2 every unit follows one common drive p. I read a fixed rate parameter as part of the rule, not a variable units follow. Say so explicitly, or the wall can be turned on E2 too.' Said so here: a fixed rate parameter is part of the rule, not a state copied by the units.
- **Receipts:** none (text audit).
- **Confidence:** high. The clauses are quoted, and the wall names the run.

### N-2026-11-10-4: does a published result settle the positive-weight half of O_signed? (D1)

- **Depth reached:** D1.
- **Result:** not settled by the literature located; it bears on the question only in part.
- **What was found (external results, labelled as such):**
  - *Gingrich & Horowitz 2017* (arXiv 1706.09027; PRL 119, 170601 as recalled, journal not confirmed on the page opened). For Markov jump processes with reversible transitions and local detailed balance, at steady state, the first-passage time T to a large current threshold obeys Var(T)/⟨T⟩² ≥ 2/(⟨T⟩σ), where σ is the entropy-production rate. *Bears:* partly. It bounds timing precision by dissipation, not by extent.
  - *Garrahan 2017* (arXiv 1701.00539; PRE 95, 032134 as recalled). First-passage bounds in terms of activity. *Bears:* partly, in the same way.
  - *Di Terlizzi & Baiesi 2019* (arXiv 1809.06410; J. Phys. A 52, 02LT03). The kinetic uncertainty relation: precision is bounded by activity, with no reversibility needed. *Bears:* partly.
  - *Macieszczak 2024* (arXiv 2407.09839). A tighter asymptotic bound for Markov processes on discrete configurations, using the harmonic mean of decay rates weighted by the stationary distribution. It can always be saturated. *Bears:* partly.
  - *Barato & Seifert 2015*, the current TUR (recalled, not re-opened). Displacement is a current, so Var(x_t)/⟨x_t⟩² ≥ 2/(σt). *Bears:* partly. It bounds run-to-run extent by dissipation.
- **Reading:**
  - Multiplying the two dissipation bounds for one steady-state process gives a lower bound on Var(T)·Var(x) of order ⟨T⟩⟨x⟩²/(σ²t), which vanishes as the drive, and so σ, grows. Every known positive-weight bound ties both widths to dissipation or activity in the same direction. That is co-shrink, which is what K_tradeless found, and none is conjugate.
  - But these are lower bounds. That they vanish does not show no positive-weight rule has a floor. 'Argued, not proved' stays as it is.
  - An exact witness, from the checker: a one-way Poisson stepper at rate r has Var(T_ℓ) = ℓ/r² and Var(x_t) = r·t, so the product ℓt/r goes to 0.
- **Independent check:** PARTLY.
  - Citations: Di Terlizzi–Baiesi and Macieszczak confirmed by web search; the others match the checker's recollection.
  - The combination step is legitimate for one steady-state process.
  - Dispute 1: 'If the project's positive-weight steps can be unidirectional, σ = ∞ and both TURs are vacuous. Only the KUR and Macieszczak activity bounds apply then.' Accepted. For irreversible rules the argument should cite the KUR, not the TUR.
  - Dispute 2: '"Spatial extent" may not be Var(x_t).' The current-TUR leg covers the run-to-run spread, not a pattern's own within-pattern width. Accepted.
- **Receipts:** none (literature).
- **Confidence:** medium. The located results are real and the reading is modest; the search was one pass.

### N-2026-11-10-5: what would show a level's clocks are isolated? (D2)

- **Depth reached:** D2.
- **Crack found:** yes, in the sense that the criterion was never written down. The G_species status says 'Isolation of cycles rests on two examples only'.
- **The criterion.** A periodic orbit γ of one level, with period Θ, is isolated within its conservation class if it is hyperbolic within the class: its Floquet multipliers lie off the unit circle, apart from the trivial multiplier 1 from phase and, on a closed level, a second multiplier 1 from the total. Hyperbolic implies isolated and structurally stable. The converse fails (checker).
- **Why the closed level needs the second exclusion.**
  - On a closed level the right-hand side is homogeneous of degree 1 in (C, V, L, P): the rates k3·F(x) depend on the share x = C/T only, and multiply linear terms.
  - So λ·γ(t) is again an orbit, with the same period, for every λ > 0. Every closed-level cycle is a one-parameter family in amounts, and a single point in shares and period.
  - That is the cycle counterpart of K_bal's 'isolated when read as shares'. It holds only while every rate depends on shares alone; a rate that depends on an amount breaks it.
- **Smallest assumption:** hyperbolicity within the class. It is generic, not guaranteed: it fails at Hopf points, and at the fold of cycles where clock 12051 dies.
- **What depends on it:** G_species's isolation half for cycles; O_focus (discreteness); O_drift, whose shape asks for hyperbolic attractors within each class.
- **Check for a later night** (named, not run, so not frozen as a test):
  - Integrate the two working-grammar clocks: draw 19387, closed; draw 33538, open; both with k11 = 0, rate law ρ = k3·F(x).
  - Compute the monodromy matrix over one period.
  - Report all multipliers. The closed clock should show two at 1, the open clock one at 1.
- **Independent check:** PARTLY.
  - Homogeneity confirmed, with the remark that the scaling multiplier should also be semisimple. Worth checking numerically.
  - Dispute 1: 'iff' is wrong. Hyperbolicity is sufficient, not necessary. Accepted; the criterion is stated one-way above.
  - Dispute 2: 'the single-level equations as written cannot cycle' because they are linear. Not accepted as stated. The checker was given the equations without the recruitment law. In the working grammar ρ = k3·F(x) makes them nonlinear, and both clocks exist. Its point that the run must name its equations before it runs is accepted, and they are named above.
- **Receipts:** none.
- **Confidence:** medium-high for the criterion; the computation is not done.

**Receipts table** (all are in Night-Reports, uploaded as plain files, SHA-256 of the uploaded bytes)

| File | Drive ID | SHA-256 |
|---|---|---|
| NIGHT-QUEUE-2026-11-10.md | 1h81kRXLAF_iW_iPvdakjQqW41r8XT4Lx | ea13e9bad6b731307265980ece11a6941fecddf6970124c3a3d7396953acf10b |
| N-2026-11-10-1-sym.py | 1A-bkq3-hdLPSCSoR5NHxasxc6E9sd9Eo | acdc5eed8c8ba522a5476b2d35a21f457367e6a4b3159d91785770ab7b33037a |
| N-2026-11-10-1-sym-output.txt | 1wHWmhltyOiL8U4PtOwDEbKIdKIgWT3JM | 7fab420ab64ac69654552f61a4ac3b7f327d66a725fb701c58505e710303e187 |
| N-2026-11-10-1-num.py | 1HYb_-Zuv3lQ5qoja_sFdl3r0lzxEqynZ | ae54cce375fa2f8d3b113aa523a605c87a0f4e68481838601a446636e12edaf2 |
| N-2026-11-10-1-num-output.json | 1DJ2iD6IWbD6CLtPwem9-F74L-s1ylCGj | 4597a7c940abf914820918f0ed1fd7cd32fe45e6b0309a3960084c091f062e28 |
| N-2026-11-10-1-num-stdout.txt | 1tGrAZ6dGVXTfGh0K84IR8pbmqm47MYCK | daabf58291b6654f9b1fe33c4ad6572ac1574abe0d9a620878daa0ac63ef1904 |
| N-2026-11-10-1-num-perdraw-summary.json | 1R5s0FeYovttEexXFvWVQweJ5uly4Fgon | 02d8c42918936e8b26e64553699b217fe4dd174b11f1f2c9f791cbc738035907 |
| N-2026-11-10-1-pilot.json | 13CFmodz64TbLuiM9P3VS5jLR-1kox243 | 917fddd01d93edf86a38ee0b581cc3ae1705a31bea3810192761bd479ab56838 |
| N-2026-11-10-1-mpverify.py | 1-GwWEQNb7qY4DoZivpIBv0Pce9XYLySC | da60c9f0253ef6c8272490253afb14e7d92f896eb1345603ad914786febe2adc |
| N-2026-11-10-1-mpverify-output.txt | 1PNPad69aLtbjflg0i6RMKr0O7GS3i4W- | f64b5d68343086e2c6a7f9d074d2d48ea4c160c5740cad2bb1b29525d3b4f7b2 |
| N-2026-11-10-1-mpverify-rest.py | 1LbsRAcoNrOiw0SYZQe8sGwP8JtGsdbCL | 0f06a47f5912c7dbd8dc29695c4e29319aec802f64b8a15a61bf50ae3252286d |
| N-2026-11-10-1-mpverify-rest-output.txt | 1Zb9fPfjRHSlHwo59wJtP27FTiu2ry7hF | 625f680379c8b1701ad230645c5db95461367f602fa528028d455d8acf29e56f |
| N-2026-11-10-1-checker-num.py | 1dEwy7rd7J3Z1pXcxrJxNSwanw88svRYl | 1d6353b4b154151ca30724533fcdb5f8b31248351d5879e95226a4efd1f7f176 |
| N-2026-11-10-1-checker-sens.py | 1OGWFTWyJeHHgL1PkQugooLi6qhu1Htqb | 657cbc5fccc872eaa0624754717382a28a654353d50adac5b66843f8ffa41c3c |
| N-2026-11-10-checker-chk.py | 1cuPTKOcD_r5h36_NU3DxJYmaA8850sv5 | 962f7d9e7a51cf6938df65e855288a786a7d51857f66bf46ec19fb278253d66f |
| N-2026-11-10-2-algebra.py | 1-egnzw7N4PjMnp7v_s-NPXWREYICsTMj | b6aefb1b32c7c5cff1546e7cd0e707efcd9249bc995522e774005050476e8077 |
| N-2026-11-10-2-algebra-output.txt | 1I7M8jbaD5L_6MPjlk3FMCclcHH-ASRGL | b5546efe6d8605b137ee4065e50ce2b2be3a68707ce693d99fba430b1fe53b40 |
| N-2026-11-10-2-checker-d2.py | 1iZn-19VaKlBcQ_DykQNj_T2N-_Rec9e8 | ebd10b07be210cced630a23b82ae89224be0e7adee4c60020828b86615530222 |
| N-2026-11-10-1-num-output-perdraw.json | not uploaded (3.95 MB, over the connector's per-call limit); summarised in the per-draw summary file | 67b09295ccce3b357d518bea2eca2aa8cab810b78ad87ea9915e77c7eb9ccb1a |


## 5. New candidates (post-failure)

The queue's planted failure P1 for item 1 failed in its specification, not in its run (see item 1). The following is a post-failure idea, labelled as such, and is not used tonight. A sound plant for the determinant check would shift the (C, V) entry by +δ and the (V, V) entry by −δ together. That keeps the column sums, and it changes det J by exactly k7·k9·(k5 + k6)·δ, as the checker showed. P1's failure stays on the record.

The queue had no candidate in the physical sense. Item 1's finding that an outer balance can be unstable is a refutation of a conjecture, not a failed candidate. Nothing was revised in response to it.

## 6. Suggested Map changes for Glenn to decide

These are recommendations only.

1. **K_bal: replace the 'Not shown' clause with two results.**
   - *Proved [theorem, model]:* on an open level, det J = k7·k9·(k5 + k6)·g′(V*) at every balance, so of three simple balances the middle one is always unstable, a saddle.
   - *Refuted:* 'the outer two are always stable'. An outer balance can lose stability to an oscillating pair while g′ > 0, as in the verified case (m = 27, kr = 7), which has one unstable focus, one saddle and one stable balance.
   - Receipt: N-2026-11-10-1, check CONFIRMED.
   - The phrase 'at most two stable ones if the stability conjecture holds' would then become 'at most two stable balances (proved: the middle is never stable); fewer if an outer one goes unstable'.
2. **O_drift: update its shape line.** 'Stability of the three is the open step' could become: the middle is unstable, proved; outer stability is not generic-guaranteed, and an outer balance can carry an oscillation. Whether a level can hold a resting organisation beside a ticking one in the same total is now a concrete question (receipt: N-2026-11-10-1).
3. **K_tradeless: narrow it.** Strike or bracket the E3 clauses: the '318 of 318 copy-the-state' count, the 'with copying, run-to-run noise stops improving with N' sentence, and E3 in the status's candidate list. These clauses rest on the shared organisation variable that the 10 Nov wall forbids. 'Ensembles do not change this' would then read 'non-interacting ensembles (E2) do not change this'. Receipt: N-2026-11-10-3, check CONFIRMED.
4. **K_tradeless / O_signed: add a note under Tests or follows.** It would name the positive-weight bounds located tonight: the first-passage TUR, the current TUR, the kinetic uncertainty relation, and the harmonic-mean bound. All of them tighten timing and position together as dissipation or activity grows, and none is a timing–extent floor. They are consistent with 'no floor', but they do not prove the general claim. Receipt: N-2026-11-10-4, check PARTLY. The prior art in the 10 Nov note was cited from memory. Tonight Gingrich–Horowitz (arXiv 1706.09027) and Di Terlizzi–Baiesi (arXiv 1809.06410) were opened. Garrahan (arXiv 1701.00539) appeared in the search results but was not opened.
5. **C_seed: record tonight's specification as a candidate coupling,** with the checker's two disputes attached: it feeds but does not seed, and it uses single-unit currency. Do not regrade C_seed. The depletion follows by construction (receipt: N-2026-11-10-2, check PARTLY).
6. **G_species: no change to the statement.** Consider adding a note to its status, 'isolation of cycles: criterion written (night run 10 Nov, item 5); not computed' (receipt: N-2026-11-10-5, check PARTLY).

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **The resting–ticking pair (D3).** In the verified case of item 1, integrate from near the unstable low-Void balance. Does it settle onto a cycle that coexists with the stable high-Void balance? That is two attractors of different kinds on one level, which bears directly on O_drift and G_species.
- **Closed-level counterpart of item 1 (D3).** Restrict J to the conservation class, which is 3×3, and test whether its determinant tracks the slope of R(x) − D·x. The checker notes that the full 4×4 determinant is identically 0 there.
- **Census of outer instability (D2).** Using tonight's per-draw summaries, ask which (m, kr) and which rate regimes carry an unstable outer balance. No new run is needed.
- **The C_seed coupling, revised (D2).** Resolve the two disputes before any run: a conversion factor between rungs (complete lower organisations becoming upper Void), and a seeding route from below. Then specify a run with a kill line.
- **Floquet multipliers of the two clocks (D3).** Compute the monodromy of clocks 19387 (closed) and 33538 (open) in the working grammar (k11 = 0), and report the non-trivial multipliers. This is item 5's check.
- **O_protect 'rare' branch literature (D1).** Carried over.

## 8. Verification handoffs

```
Task (DeepSeek). Given the open-level system with all rates positive, roles C,V,L,P >= 0, T=C+V+L+P, x=C/T, any differentiable rho(x) >= 0:
dC/dt = -(k1+k2+k7)C + k6 L + (k10+rho(x))V
dV/dt = k2 C + k5 L + k8 P - (k10+rho(x))V + k12
dL/dt = k1 C - (k5+k6) L
dP/dt = k7 C - (k8+k9) P
Prove or refute: (1) det J = k7*k9*(k5+k6)*dfC/dV at every state; (2) at a balance, dfC/dV equals g'(V*), where g(V) = (k10 + rho(C*/(C*+L*+P*+V)))*V with C*=(k8+k9)k12/(k7 k9), L*=k1 C*/(k5+k6), P*=k12/k9; (3) hence, when g(V)=D*C* (D=k2+k7+k1k5/(k5+k6)) has three simple roots, the middle balance has a positive real eigenvalue. Then, for rho = k3*I_x(kr, m-kr+1) (binomial tail), m=27, kr=7, (k1,k2,k3,k5,k6,k7,k8,k9,k10,k12) = (17.452344563736048, 0.41372216747103946, 44.67737830552512, 8.05086975924266, 0.06903256564057879, 0.03229295995554182, 0.083706798767576, 0.010174673348427083, 0.609928184398708, 0.15342684932155354): compute all balances and the Jacobian eigenvalues at each, and confirm or refute that the lowest-V balance is unstable with g'>0.
```

```
Task (Astra / DeepSeek). Same system, closed level: drop k12 and the k9 exit (o=0), so T is conserved and the equations are homogeneous of degree 1. Restrict the Jacobian at a balance to the conservation class (3x3). Determine whether its determinant has a fixed sign relation to the slope of H(x) = R(x) - D*x, R(x) = (k10 + k3*F(x))(1 - c*x), c = 1 + k1/(k5+k6) + k7/k8, at the balance share x*, and hence whether the middle of three closed-level balances is always unstable. Report a proof or a counterexample.
```

## 9. Run notes

- **Access.** Every required source was reached:
  - the spec (v2.1, file ID 1sgnU86…);
  - STEERING.md;
  - the standing constraints, the current copy (ID 1LjICJx…, exact title, 'CURRENT' description);
  - the Premise Map, read in full through the Artifact tool (version 1794281872-597e) and parsed to JSON for the snapshot;
  - the 9 Nov report and snapshot;
  - the saturation note;
  - TIMING-EXTENT-TRADE-2026-11-10.md.
  The project instructions were in context. The narrative spine (context only) was not opened, for time.
- **Map diff method.** The 9 Nov snapshot came back from Drive as base64 that could not be passed into the sandbox without retyping it. The diff was therefore made from node counts and IDs, with field changes checked against the map's own 9–10 Nov timeline and on each named node. A line-by-line machine diff of deps and tests was not done. Tomorrow's run can diff MAP-SNAPSHOT-2026-11-10.md directly if it can read it as text.
- **Freeze.** The queue was saved as its own file at 06:23:03 UTC, before any item's work. The outline of item 1's determinant identity occurred to me while I was building the queue, and is declared there.
- **Item 1, the specification error.** The queue's guarantee for planted failure P1 was false. I found this from the symbolic cofactor, before the main loop's results were read, and the checker confirmed it independently. The queue was not altered. P1 was run as frozen, and its numerics are not counted as a receipt.
- **Item 1, deviations from the queue:**
  - brentq's rtol was raised from 4×10⁻¹⁶ to 10⁻¹⁵ (scipy's floor) before the reproduction check ran.
  - The output stored only the first 200 outer-unstable cases. The other 12 were verified by replaying the seeded sequence (N-2026-11-10-1-mpverify-rest.py), not dropped.
  - Pilot: 2 000 draws in 12.4 s, 56 with three balances, about 80 MB resident memory. The main loop hit the 45-minute wall at 425 454 draws (12 264 with three balances), short of the 20 000 target, as the pilot had predicted. It was not extended.
- **Receipts.** The 3.95 MB per-draw file was over the Drive connector's per-call limit. The spec allows a summary when raw output is large, so a summary file (all 212 flagged rows and aggregate statistics) was uploaded instead, and the raw file's hash is listed. The raw file stays in the session sandbox only, and will be lost when the session ends.
- **Checks.** Independent checks were made by two fresh Claude subagents that had not seen the working: one for item 1, which re-derived everything with its own scripts, and one for items 2–5. They ran after the items' working, in parallel, rather than strictly after each item. Their verdicts are summarised above. The checker for items 2–5 was given the single-level equations without the recruitment law ρ = k3·F(x); its item-5 'linear system' dispute comes from that omission and is answered there.
- **Time.** The run went from about 06:20 to 07:20 UTC. Nothing was skipped.
- **Writes.** New files only, all in Night-Reports. Nothing else was edited.
