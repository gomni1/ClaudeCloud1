# NIGHT-QUEUE-2026-11-09 — frozen before Phase 3

## 2. Frozen queue

Frozen 9 Nov 2026, 06:25 UTC, before any item's work began. Saved to Night-Reports as NIGHT-QUEUE-2026-11-09.md, so the freeze has its own timestamp and the report never has to be edited. Not altered after that.

Sources: STEERING has no PIN, SKIP or RETIRED lines. This is the first night, so there are no previous follow-ups and no snapshot. Every map region counts as new (source 3), so items were chosen from sources 4–8 and ranked easy and high-impact first. Retired items and closed matters were excluded: the standing constraints' Closed list, the Archive shelf and Outcome nodes.

Reading taken: the night works from the map's latest changes (6–7 Nov: 'Growth pays for itself in Void…' placed as Known; the saturation gap archived). That node has had no outside check. Several older live nodes rest on readings the 1–7 Nov work has since replaced: the three return paths (retired 1 Nov), mass action, and the crowding release (dropped 1 Nov). Those seams are cheap to locate and bear directly on what is held.

---

**N-2026-11-09-1 — independent check of the saturation proof**
- Target: Known node K_sat, 'Growth pays for itself in Void: with seeding, a level is bounded under any recruitment law; on a closed level, cycling needs a lag'. Source: NOTE-Saturation-Mechanism-2026-11-06.md, claims S1, S1b, S2, S4(a) and S5.
- Task: given the grammar's rate equations as stated in the note (roles C, V, L, P; k11 = 0; all-neighbours count; any recruitment ρ ≥ 0), prove whether S1, S1b, S2, S4(a) and S5 follow as stated, and whether the map wording claims more than the note proves.
- Inputs: the note's equations and proofs; the K_sat map text.
- Depth: D3 Probe, one bounded attempt to break it.
- Effort cap: about 30% of the night.
- Done means: each claim marked holds, holds with a narrower scope, or fails, with the reason.
- Mechanism, specified now: (a) symbolic: in sympy, rebuild A0 (ρ = 0, open level), solve wᵀ(−A0) = 1ᵀ, and check w > 0 symbolically or by sampling, w_V − w_C = 1/k10, and d(w·y)/dt = −ΣY − ρV/k10 + w_V·k12 exactly. Check the S2 sums and pins, the S4(a) derivative identities, and the closed-level reduction V = T − cC. (b) adversarial numerics, Python with scipy: open level, rates log-uniform in [10⁻², 10²], 300 draws. Recruitment laws chosen to attack S1: ρ = k3·C³, ρ = k3·e^{C}, capped at 10⁶; a time-switching ρ (k3·C² when dV/dt > 0, else 0); and ρ = 10⁴ held constant. Pass condition: w·y(t) ≤ max(w·y(0), w_max·w_V·k12)·(1 + 10⁻⁶) at every accepted solver step (dense output, 5 000 points per run, plus the step points). Planted failure: the same check on a model with a Contact-creating term k3·C² that uses no Void must flag at least 90% of draws in which that term's integral exceeds the bound, or the harness is declared blind. (c) S1b and S5 are checked by hand only.
- Kill (for the claim, not for the harness): any run that violates the bound within S1's hypotheses.

**N-2026-11-09-2 — what holds up 'A species is an isolated, non-drifting invariant' now**
- Target: conseq node G_species (live), and C_deficiency, which feeds it.
- Task: given negative result N, identify the minimal failed assumption. N is the fact that G_species's proof support, 'One level of the closed grammar holds one balance, and every start goes to it' (K_closedcount, now in the Archive), was proved under the three-return-path encoding (retired 1 Nov) and mass action, while the working grammar is two return paths, threshold recruitment and the all-neighbours count. Under the working grammar there are three balances for kr ≥ 2 (K_sat S4b) and stable clocks (K_clock). Determine which of G_species's two halves (isolated; non-drifting) still have support in the working grammar, and what a replacement root would have to show.
- Inputs: G_species, K_closedcount, K_sat, K_clock, K_tot, C_deficiency, O_focus, and the Glenn 24 Sep reframing recorded on G_species.
- Depth: D2 Shape.
- Effort cap: about 15%.
- Done means: a statement of which clause is unsupported and which survives, the smallest assumption involved, what depends on it (live nodes resting on G_species), and the shape of the missing root.
- Mechanism: none; this is an audit of the dependency chain against the node texts as read tonight.

**N-2026-11-09-3 — the mechanism written into a promoted node**
- Target: promoted conseq node P_traj, 'A particle as a bounded trajectory'.
- Task: audit chain C for smuggling or untagged necessity. P_traj's statement gives the cycle's mechanism as 'recruitment raises density, density raises retirement, retirement lowers density, recruitment returns'. Locate whether that mechanism, as worded, is contradicted or unsupported in the working grammar: no crowding release (dropped 1 Nov), K_sat S5 (a closed Contact–Void level cannot cycle), and the clocks' dependence on routes through L and P.
- Inputs: P_traj, K_sat (note S3 and S5 and the exploratory lag scan), K_clock, P_fedbelow, P_growth.
- Depth: D1 Locate.
- Effort cap: about 10%.
- Done means: crack yes or no; if yes, the exact clause, and whether the promotion's support is touched.
- Mechanism: none; a text audit.

**N-2026-11-09-4 — does 'Growth depletes the rung beneath' now follow?**
- Target: conseq node C_seed. The 3 Nov cross-read by DeepSeek and Astra graded it C, blocked: 'missing cross-rung resource accounting'.
- Task: given K_sat (S1, S2), P_fedbelow (supply arrives as Void; 'the upper level's Void is the lower level') and K_ladder, determine whether either half of C_seed follows: (i) growth at a rung draws on and depletes the rung beneath; (ii) supply from below is part of what bounds growth. If not, give the shape of the missing accounting.
- Inputs: C_seed, K_sat and its note, P_fedbelow, K_ladder, F_ladder, F_cv, the 3 Nov cross-read note on C_seed.
- Depth: D2 Shape.
- Effort cap: about 15%.
- Done means: for each half, follows [model], or does not follow, with the missing piece stated as what it would have to do.
- Mechanism: none beyond reading S1 and S2 against the single-level equations; no new run.

**N-2026-11-09-5 — how many balances can one level hold?**
- Target: K_sat S4(b), which says that for kr ≥ 2 there 'can be several' balances and found at most three in 8 119 draws; and the gap O_focus (discreteness of the set of persistent closures).
- Task: given rule R (the working grammar's balance condition with the threshold law F(x) = Pr[Bin(m, x) ≥ kr], k10 > 0, all rates positive), determine whether more than three balances are possible on one level, open or closed, for any m and kr.
- Inputs: the note's balance conditions. Open: g(V) = (k10 + k3·F(a/(b + V)))·V = D·C*. Closed: D·x = (k10 + k3·F(x))(1 − c·x).
- Depth: D3 Probe, one attempt at a proof of an upper bound, plus a numerical check.
- Effort cap: about 20%.
- Done means: a proof that the count is at most three, a counterexample, or 'not settled in one attempt'.
- Mechanism, specified now: change variable to x = a/(b + V) on the open level, so that V ∈ (0, ∞) maps to x ∈ (0, a/b), and write both conditions as G(x) = 0 with G(x) = (k10 + k3F(x))(α − βx) − γx, where α, β, γ > 0. Attempt: show that G″ changes sign at most once on the interval, using F′ ∝ x^{kr−1}(1 − x)^{m−kr} (the beta-density form) and the monotonicity of F″/F′. Then Rolle gives at most three roots. Numerical check, with the proof's verdict fixed before it runs: for m = 2..30 and every kr, 2 000 random draws of (α, β, γ, k10, k3), log-uniform in [10⁻³, 10³] and kept to x ∈ (0, min(1, α/β)), counting roots by sign changes on a 20 000-point grid refined by brentq. Kill: any draw with four or more roots. Planted check: a hand-built G with four roots must be counted as four.
- Note, for transparency: the outline of this proof occurred to Claude while the queue was being built (reading K_sat). It is written down here before any working, and the numerical check is fixed in advance.

Skipped at queue-building, for tomorrow: (a) an observational-register literature check for O_protect's 'rare' branch, which is harder; (b) the K_telegraph boost-invariance caveat, which is already logged on the node.
