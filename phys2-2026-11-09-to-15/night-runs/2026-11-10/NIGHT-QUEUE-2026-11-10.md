# NIGHT-QUEUE-2026-11-10

PHYS2 Night Run, second night. Claude, unattended. Frozen 10 Nov 2026 before any item's work began, and saved to Night-Reports as its own file so the freeze has its own timestamp. Not altered after that. Spec v2.1 (10 Nov) applies.

## How the queue was built

- **Sources read:** NIGHT-RUN-SPEC.md v2.1; STEERING.md (two PIN lines, no SKIP or RETIRED lines, one NOTE); PHYS2-STANDING-CONSTRAINTS.md (file ID 1LjICJxBfjMmma25W_2r3egpFpoYt_UJA, amended 10 Nov, description "CURRENT standing constraints"); the Premise Map (version 1794281872-597e, 177 nodes); NIGHT-REPORT-2026-11-09.md and its suggested follow-ups; NOTE-Saturation-Mechanism-2026-11-06.md (the grammar's equations). No REVIEW notes exist in Night-Reports.
- **Priority 1, STEERING PIN:** items 1 and 2, in Glenn's order.
- **Priority 2, last night's follow-ups:** stability of the three balances (= PIN 1); C_seed back-reaction (= PIN 2); isolation of cycles (item 5); literature check on O_protect's 'rare' branch (carried over, see below); harness planted-failure rule (now covered by spec v2's planted-failure section, so not queued).
- **Priority 3, map regions changed since the 9 Nov snapshot:** K_tradeless and O_signed (placed 10 Nov). The 10 Nov standing-constraints amendment added the wall 'No coordinator above a level' and names the 10 Nov run's E3 ensemble as a violation, while K_tradeless still cites E3 counts as Known (item 3). Glenn left O_signed to the night run's choice (item 4).
- **Excluded:** nothing is on STEERING SKIP or RETIRED. The standing constraints' Closed list (charmonium selection, Candidate B, free random swap/flicker, the compact trans-scalar grammar, charge as the unpaired half-twist, the P2.6-03 §5 list) and the 'Open and not load-bearing' list were excluded. Archive and Outcome nodes were excluded.
- **Ranking (effort versus impact):** PINs first in order; then item 3 (easy, high: a Known node possibly resting on a forbidden move); item 4 (moderate effort, moderate-high: a published theorem may already settle half of a gap); item 5 (easy, moderate: shape only).
- **Carried over, not queued tonight:** the O_protect 'rare' branch literature check (D1). Reason: tonight's literature slot goes to item 4, which touches a node placed yesterday.

**Transparency note (item 1).** While reading the saturation note to build this queue, Claude saw how the determinant identity for item 1 probably goes: replace the V-row of the Jacobian by the sum of all rows, which is (0, 0, 0, −k9), and expand; the result should be det J = k7·k9·(k5 + k6)·g′(V*). This is declared here before any working. The identity is to be proved symbolically in item 1, and the numerical part below is fixed now, so it does not depend on whether the outline is right. The outline says nothing about the outer two balances. Claude also notes, from the map's 'Clocks exist…' node, that an open level with kr = 2 (draw 33538) has a Hopf-unstable balance in the working grammar; whether an outer balance of a three-balance level can be unstable is therefore a live question, and the numerical search below is built to answer it either way.

---

**N-2026-11-10-1 — Stability of the three balances (STEERING PIN 1)**
- **Target:** K_bal ('One level holds at most three balances under threshold recruitment'), its 'Not shown' clause; O_drift ('Does a species' attractor drift in the working grammar?'), whose shape names stability of the three as the open step.
- **Task:** given rule R, the open level of the working grammar (roles C, V, L, P; k11 = 0; all-neighbours count x = C/T; ρ = k3·F(x), F(x) = Pr[Bin(m, x) ≥ kr]; all listed rates positive; kr ≥ 2), determine (a) whether the sign of det J at a balance is fixed by g′(V*), where g(V) = (k10 + k3·F(C*/(C* + L* + P* + V)))·V; (b) whether, when three balances exist, the middle one is always unstable; (c) whether the outer two are always stable.
- **Inputs:** NOTE-Saturation-Mechanism-2026-11-06.md (equations, S2, S4, appendix eigenvalues and example rates); K_bal; K_clock (open clock 33538).
- **Depth:** D3 Probe. One attempt: a symbolic proof of (a), (b) by consequence, and one bounded numerical search for (c).
- **Effort cap:** about 35% of the night.
- **Done means:** (a) proved or refuted symbolically, with the exact relation; (b) stated as following or not; (c) either a verified counterexample (an outer balance with an eigenvalue of positive real part) or 'no counterexample in N draws', with the count, which is not a proof.
- **Mechanism, specified now:**
  - *Symbolic (sympy):* build the 4×4 Jacobian of the open-level right-hand side with F left as an undefined function of x, evaluate at a balance using S2's pins (P* = k12/k9, C* = (k8 + k9)·k12/(k7·k9), L* = k1·C*/(k5 + k6)) and V* free, and simplify det J − k7·k9·(k5 + k6)·∂f_C/∂V; separately check that ∂f_C/∂V at fixed C, L, P equals g′(V). Result (a) holds only if both simplify to 0 identically.
  - *Numerical harness (Python, numpy/scipy, no ODE integration):* draws with rates k1, k2, k3, k5, k6, k7, k8, k9, k10, k12 log-uniform in [10⁻², 10²], m uniform in 2..30, kr uniform in 2..m, seed 20261110. For each draw compute the pins, then find every balance as a root of G(x) = (k10 + k3F(x))(α − βx) − γx on (0, α/β) (α = C*, β = C* + L* + P*, γ = D·C*), by sign changes on a 4 000-point grid including the exact end signs, refined by brentq; map x → V* = α/x − β = C*/x − (C* + L* + P*). Keep only draws with exactly three roots. At each of the three balances: analytic Jacobian (with F′ from the beta density), its eigenvalues (numpy.linalg.eigvals), det J, and g′(V*) by its closed form. Per draw keep only summaries: the three V*, the three max Re λ, the three relative errors |det J − k7k9(k5+k6)g′| / (|det J| + k7k9(k5+k6)|g′|), flags.
  - *Checks while running:* identity flag if relative error > 10⁻⁶; middle-stable flag if the middle balance has max Re λ ≤ 0; outer-unstable flag if an outer balance has max Re λ > 10⁻⁹·max|λ|. Any outer-unstable flag is re-verified in mpmath at 50 digits (balance re-solved, eigenvalues recomputed) before it is reported as a counterexample.
  - *Reproduction check (must pass before the main loop):* the note's example (m = 10, kr = 6, rates in the appendix) must give three balances with V* ≈ 2.589, 14.394, 79.747 and eigenvalues matching the appendix to 3 decimals.
  - *Planted failures, both guaranteed analytically:* (P1) for the identity check: at the first 200 three-balance draws, also test a Jacobian whose (C, V) entry is shifted by δ = 0.5·|g′(V*)| + 1. The determinant is linear in that entry with coefficient k7·k9·(k5 + k6) (its cofactor, by the same row reduction), so the plant's det differs from the identity by exactly k7·k9·(k5 + k6)·δ > 0, a relative error of at least δ/(2|g′| + δ) ≥ 1/3 > 10⁻⁶ whatever the draw. Note: this guarantee uses the cofactor claim, which is part of what (a) proves; so P1 is guaranteed only if (a) holds, and if (a) fails P1's result is not interpreted. (P2) for the stability classifier: at the same 200 draws, also classify J + s·I with s = 1 − max Re λ(J) at the most stable balance. The eigenvalues of J + sI are exactly λ + s, so its max Re λ is exactly 1 > 0; it must be flagged unstable. If P1 or P2 fails to trip in any of its 200 cases, the harness is declared blind and the numerics are not a receipt.
  - *Sizing:* a pilot of 2 000 draws is timed first and written into the run notes; the main loop then runs until 20 000 three-balance draws are collected or 45 minutes of wall time pass, whichever first.
  - *Kill lines, fixed now:* (a) is refuted by any symbolic remainder ≠ 0, or by any verified identity flag. (c) 'outer two always stable' is refuted by any mpmath-verified outer-unstable case. Nothing else is a kill.

**N-2026-11-10-2 — The smallest two-way resource coupling (STEERING PIN 2)**
- **Target:** C_seed ('Growth depletes the rung beneath'), half (i), and its shape line; A_share ('Shared supply within aggregate capacity; each unit counted once'); F_ladder; P_fedbelow.
- **Task:** given A_share, F_ladder, P_fedbelow and the single-level equations, specify the smallest two-way resource coupling between two levels in which the upper rung's uptake appears as a loss or an exclusive commitment in the lower rung's balance, and binds when the lower rung's capacity binds. State what it adds to the one-way ladder, what it must not add (no coordinator above a level; no one-to-one handoff bookkeeping; no fitting), and what a later run would test, with a kill line. Specification only; no run.
- **Inputs:** C_seed, A_share, F_ladder, P_fedbelow, K_ladder, K_sat (S1, S2), the saturation note's equations, the standing constraints (forbidden moves).
- **Depth:** D2 Shape.
- **Effort cap:** about 20%.
- **Done means:** a written specification: the coupled equations, each new term's justification against A_share and F_ladder, the conservation identity it must satisfy across the two levels, what it changes relative to the one-way ladder, and a candidate test with a kill line and a planted failure for a later night. Explicitly not run.
- **Mechanism:** none tonight (specification only). Any algebra checked by hand or with sympy, for consistency only (no dynamics run).

**N-2026-11-10-3 — Does 'With positive-weight turnover, sharper timing does not cost extent' rest on a forbidden move?**
- **Target:** K_tradeless (placed 10 Nov), against the standing-constraints wall 'No coordinator above a level' (added 10 Nov), which names the 10 Nov run's E3 ensemble as a violation.
- **Task:** audit chain C for smuggling. Locate which clauses of K_tradeless's statement, status and follows rest on E3 (copy-the-state) results, and whether the Known statement survives with E3 removed.
- **Inputs:** K_tradeless and O_signed node texts; TIMING-EXTENT-TRADE-2026-11-10.md; the standing constraints.
- **Depth:** D1 Locate.
- **Effort cap:** about 10%.
- **Done means:** crack yes or no; if yes, the exact clauses, and what remains supported by the single-unit and independent (E2) results.
- **Mechanism:** none; a text audit.

**N-2026-11-10-4 — Does a published result already settle the positive-weight half of 'Signed or phased handoff contributions'?**
- **Target:** O_signed (placed 10 Nov) and the K_tradeless status line 'the general claim that no positive-weight rule can give the floor is argued, not proved'.
- **Task:** given rule class R (positive-weight step processes: Markov jump processes and random walks with drive, including the telegraph/persistent walk), locate whether a published result proves or refutes that such rules can have a positive infimum of (timing width × spatial extent) under unbounded drive. Candidate literatures to search, before any attempt: thermodynamic and kinetic uncertainty relations (including first-passage-time versions), persistent random walk / telegraph process variance results, and the Gaveau–Jacobson–Kac–Schulman analytic continuation.
- **Inputs:** O_signed, K_tradeless; web search.
- **Depth:** D1 Locate.
- **Effort cap:** about 15%.
- **Done means:** a list of the published results found, each with what it bounds and whether it bears on the infimum (yes / partly / no), and a one-line verdict: settled by literature, partly, or not located. No new proof.
- **Mechanism:** none; a literature search. Observational and external results labelled as such.

**N-2026-11-10-5 — What would show a level's clocks are isolated?**
- **Target:** G_species's isolation half, whose status says 'Isolation of cycles rests on two examples only'; O_focus; O_drift's shape.
- **Task:** given structure S (one level of the working grammar, open or closed, with a periodic orbit), state the invariant I whose computation would establish isolation of the cycle within its conservation class (Floquet multipliers), what must be excluded (the trivial multiplier from phase; on a closed level the multiplier from the total), and why the closed level's scaling with T makes cycles a one-parameter family in amounts but isolated in shares and period. Shape only.
- **Inputs:** K_clock, K_sat (S5), K_bal, G_species, O_drift.
- **Depth:** D2 Shape.
- **Effort cap:** about 10%.
- **Done means:** a written criterion, the smallest assumption involved, what depends on it, and a candidate check for a later night. No computation tonight.
- **Mechanism:** none.
