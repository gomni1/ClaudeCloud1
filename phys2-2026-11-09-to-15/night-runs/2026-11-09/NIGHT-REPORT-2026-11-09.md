# NIGHT-REPORT-2026-11-09

PHYS2 Night Run, first night. Claude, unattended, 06:21–07:10 UTC, 9 Nov 2026. Promotes nothing, closes nothing, renames nothing. Recommendations only.

## 1. Top line

The newest Known result, 'Growth pays for itself in Void…' (the saturation proof of 6 Nov), passed an independent check. Its bound, its throughput pin and its one-balance case all hold symbolically. Its 'cycling needs a lag' clause proves less than its wording: the theorem says a closed level needs a route through Loosened or locked to cycle, not that the route works as a delay.

A new result, proved and checked tonight: one level of the working grammar can hold at most three balances, for every neighbour count, every threshold and every rate choice. Under the 24 Sep reading that each attractor is a species, the number of species one level can carry is capped by its structure. This is a concrete foothold for 'Why is the set of persistent closures discrete?'.

Two live nodes still rest on readings the 1–7 Nov work replaced. 'A species is an isolated, non-drifting invariant' is propped up by an archived proof made under the retired three-return-path grammar and mass action. The promoted 'A particle as a bounded trajectory' still describes its cycle by a density-triggered retirement that the working grammar no longer has. Neither breaks what is held, but both are cracks in the receipts.

'Growth depletes the rung beneath' is half supported. Supply from below does bound growth [model, given bounded supply]. Depletion of the rung beneath appears in no model on the map, because every ladder run so far moves resources one way only.

## 2. Frozen queue

Copied unchanged from NIGHT-QUEUE-2026-11-09.md (Drive id 1ynCos_9K5JYJpfVpIJp1ao16a3tMTkk0, created 06:25:02 UTC, SHA-256 c9df7526fd55011af4be7b7463b261fe4b66190795230864e7363e3d033e8fae of the local copy before upload).

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

## 3. State changes noticed

- **Map diff:** this is the first night, so there is no previous snapshot and everything is new. The Premise Map was read at version 1794023894-eb69. It has 173 nodes: 91 live, 14 Reserve, 8 Reservoir and 60 Archive. By type: 10 Floor, 12 Adopted, 50 Known, 37 if-then, 28 Candidate, 19 Retired, 17 Gap. Tonight's dump is MAP-SNAPSHOT-2026-11-09.md, for tomorrow's diff. The latest map events are 6–7 Nov: K_sat was placed, and the saturation gap was archived on Glenn's ruling.
- **Steering:** STEERING.md has no PIN, SKIP, RETIRED or NOTES lines, so nothing was applied.
- **Previous follow-ups and REVIEW notes:** none exist, since this is the first night.

## 4. Results, per item

### N-2026-11-09-1: independent check of the saturation proof (D3)

- **Depth reached:** D3.
- **Crack found:** yes, a small one, in wording, not in mathematics.
- **What holds** (sympy, script n1_sym.py, all exact):
  - **S1:** w = (−A0)^{−T}·1 has every component a ratio of polynomials with positive coefficients (denominator k10·k7·k9·(k5+k6)), so w > 0 under exactly the stated hypotheses. w_V − w_C = 1/k10. d(w·y)/dt = −(C+V+L+P) − ρV/k10 + w_V·k12 holds identically for free ρ.
  - **S1b:** holds by hand.
  - **S2:** d(total)/dt = k12 − k9·P, with P*, C* and L* as stated. The closed and open reductions to −D·C + (k10+ρ)V are exact.
  - **S4(a), open level:** the derivative identity checks. The checker notes the quoted form drops the k10 and k3 factors (cosmetic). The closed-level half is covered by item 5's concavity argument.
  - **S5:** correct as a theorem.
- **The crack's shape:** S5's proof is a dimension count. With k1 = k7 = 0, a closed level reduces to one autonomous equation, which cannot oscillate. It shows that a cycle on a closed level needs k1 > 0 or k7 > 0. It shows nothing about delay, and nothing about whether such a route is enough for a cycle. The map's 'cycling needs a lag' and 'a cycle needs a delayed return through L or P' add 'lag' and 'delayed' as readings. A suggested tag is in section 6.
- **Adversarial numerics:** not a receipt, by the run's own frozen rule.
  - 300 draws were planned. The process was killed for memory after about 245 draws (dense output of a stiff run), and was not re-run.
  - Laws ρ = k3C³, min(k3e^C, 10⁶), switching k3C², and ρ = 10⁴: 0 bound violations in 241 completed draws per law. The largest ratio of w·y to the bound was 1.0000000000000004, which is the start.
  - The planted failure (Contact created without using Void) flagged 180 of 203 eligible draws, 88.7%, against the frozen 90% line. So the harness is declared blind. The fault is in the eligibility test: created Contact is drained, so 'integral of created term > bound' does not imply 'w·y > bound'. The bound itself is not at fault.
  - Harness changes before any result was read, logged here: Radau was swapped for LSODA for speed; partial solutions from failed solver runs are checked too; a terminal event fires when the total reaches 10¹⁰.
  - S1 rests on its proof, which is all it ever claimed.
- **What survives:** all five claims, as mathematics.
- **Independent check:** CONFIRMED. The checker re-derived everything in its own scripts. Its disputes are cosmetic: the S4(a) quote drops k10 and k3; y ≥ 0 should be stated for the comparison step; the closed half of S4(a) is not covered by item 1 itself. It judged the 'lag' re-tag fair.
- **Confidence:** high. Exact symbolic identities, re-derived independently.

### N-2026-11-09-2: what holds up 'A species is an isolated, non-drifting invariant' (D2)

- **Depth reached:** D2.
- **Crack found:** yes.
- **Shape:**
  - **Where it rests.** G_species's status says both halves 'now have a proof for this grammar', scoped to 'the three return paths, mass action, the 12 Oct encoding'. That proof (K_closedcount) is archived. Its grammar is not the working one: the crowding release was dropped and template-free seeding was re-read on 1 Nov, and the working rate law is threshold recruitment with the all-neighbours count. The node's deps list (C_indist, A_steps, G_lifetime) does not even name K_closedcount.
  - **Smallest failed assumption:** a single, globally attracting balance per level. In the working grammar this fails through bistability for kr ≥ 2 (K_sat S4b: two stable balances) and through clocks (K_clock), which are attractors that are not balances. A third route I proposed, the coexisting rest and tick near draw 12051, was withdrawn on the checker's objection: that clock was computed with the crowding release, in the retired grammar.
- **What survives:**
  - **Isolation.** Isolation of balances now has support: at most three per level (item 5, proved tonight). On a closed level the balance share x* does not depend on the total, so in amounts the balances form a one-parameter family. That is a continuous family only if amounts are part of the invariant. Under 'The handoff is statistical' they are not, so isolation holds for the invariant read as shares and period (K_clock: on a closed level the period does not depend on the total). That reading is needed and is not written on the node. Isolation of cycles rests on two examples only.
  - **Non-drift.** The node's own wording needs each attractor to be stable, not global convergence. But no general stability result exists for the working grammar. Astra's 3 Nov grade on this half was already B ('exponential survival can hide an internal variable that changes irreversibly with age'), independently of tonight's finding.
- **Shape of a replacement root:** for one level of the working grammar, every attractor is hyperbolic within its conservation class for generic positive rates. On a closed level the total is conserved, so plain hyperbolicity is impossible: this correction is the checker's. Attractors must also be finitely many per class, with amounts excluded from the invariant. Multistability is then a spectrum, as Glenn read it on 24 Sep.
- **What depends on it:**
  - O_focus, G_express and C_deficiency rest on G_species.
  - C_deficiency's premise class is weakly reversible, rate-proportional networks, the ext 149 class. The working grammar is outside it (O_returns2: 'lies outside 149's class'). So in the working grammar C_deficiency is vacuous: neither contradicted nor supporting.
- **Independent check:** PARTLY. The disputes are taken into the result above: draw 12051 is out of scope (withdrawn); 'finite number' needed a proof (item 5 now supplies one for balances); hyperbolicity has to be read within conservation classes (corrected); Astra's prior B grade was missing (added).
- **Confidence:** medium. The dependency facts are clear; the shape of the replacement is a proposal.

### N-2026-11-09-3: the mechanism written into a promoted node (D1)

- **Depth reached:** D1.
- **Crack found:** yes, but narrower than first claimed.
- **Where:** P_traj's statement, 'recruitment raises density, density raises retirement, retirement lowers density, recruitment returns'.
  - Read loosely, 'density raises retirement' still holds: retirement flux is linear in Contact.
  - Read as the mechanism that bounds and turns the cycle, it is not the working grammar's mechanism. There is no density-triggered retirement (the crowding release was dropped 1 Nov). The counter-process is Void depletion (K_sat S3). On a closed level, a cycle needs a route through L or P (S5).
  - The statement does not say where retirement goes, so it is not shown to be a two-role loop. My first claim that S5 contradicts it outright was too strong, and is withdrawn on the checker's objection.
- **What survives:** the promotion's support (K_persist, P_stat, F_persist) is untouched, and cycling inside bounds is shown by K_clock. Only the illustrative mechanism is out of step, and the node's status already calls it 'one picture'.
- **A caution on the rewording:** for kr ≥ 2, which covers both working clocks, recruitment per unit of Contact first rises with Contact's share and then falls (S3). So 'the shortage slows recruitment' is true only past the peak.
- **Independent check:** PARTLY. Its disputes, all accepted: 'contradicted' is too strong under the evident-meaning rule; the two-role inference is not forced; the open-level 'need' is exploratory, not proved.
- **Confidence:** medium.

### N-2026-11-09-4: does 'Growth depletes the rung beneath' now follow? (D2)

- **Depth reached:** D2.
- **Crack found:** yes. It is the one the 3 Nov cross-read named, now given a sharper shape.
- **Half (ii), 'supply from below is part of what bounds growth':** follows [theorem, model, given bounded supply] for an open level. The long-run term of S1's bound is proportional to k12, and S2's pin is C* = k12(k8+k9)/(k7k9). Scope: constant supply is a rate-law choice (P_fedbelow's scope note), so this half shows that given a bounded supply, the supply sets the bound. It does not derive the bounded supply. A closed level is bounded by conservation, with no supply.
- **Half (i), 'growth draws on and depletes the rung beneath':** does not follow.
  - In the single-level equations, supply and seeding are fixed inputs.
  - The ladder runs behind K_ladder carried no resource back-reaction from upper to lower. The archived component's scope line reads 'one-way'. One run (SPEC11) had top-down coupling on phase, which failed, but none had it on resources.
  - The rung beneath does lose units by breach (−k9·P) as they leave to feed the rung above. What is missing is any dependence of that drain on the upper rung's growth.
- **Shape of the missing piece:** a back-reaction term, through which the upper rung's uptake appears as a loss or exclusive commitment in the lower rung's balance, and binds when the lower rung's aggregate capacity binds ('Shared supply within aggregate capacity; each unit counted once'). Without it, depletion is a modelling choice, not a consequence. Claude flagged the omission on 1 Nov ('the upper level draws on the lower, so the coupling runs both ways').
- **'Seeds are not arbitrarily small':** untouched. K_sat needs seeding above zero but sets no floor on its size.
- **Independent check:** PARTLY. Its disputes, all accepted: (ii) assumes bounded supply; 'one-way' holds for resources, not for phase (SPEC11); the drain by breach is already there and only its dependence on growth is missing.
- **Confidence:** medium-high.

### N-2026-11-09-5: how many balances can one level hold? (D3)

- **Depth reached:** D3.
- **Result:** proved. **At most three balances per level** (per total on a closed level), for every m, every 1 ≤ kr ≤ m and every positive rate choice. Generically one or three; exactly two only at a fold, where one balance is tangent.
- **Proof, in plain words:**
  - On both kinds of level, the balance condition reduces to one equation in Contact's share x, G(x) = (k10 + k3F(x))(α − βx) − γx = 0, on an interval inside (0, 1).
    - Open level: x = C*/(C* + L* + P* + V), α = C*, β = C* + L* + P*, γ = D·C*.
    - Closed level: α = 1, β = c, γ = D.
  - The second derivative of G has the sign of F″/F′ − 2β/(α − βx).
    - F′ ∝ x^(kr−1)(1−x)^(m−kr), the beta form.
    - So F″/F′ = (kr−1)/x − (m−kr)/(1−x), which only falls.
    - 2β/(α − βx) only rises.
    - So the second derivative changes sign at most once, and that zero is simple.
  - Hence G has at most three zeros, counted with multiplicity.
  - The end signs are G(0) = k10α > 0 and G(end) = −γα/β < 0.
  - For kr = 1, G is concave and the zero is unique, which recovers S4(a).
- **General form:** the argument needs only F′ > 0 with F″/F′ non-increasing (F′ log-concave) on the interval where the balances lie. Any recruitment law of that shape gives at most three balances.
- **Numerical check (frozen before the run):** 928 000 draws (m = 2..30, every kr, 2 000 each). Root counts: 1 in 887 008 draws, 3 in 40 992 draws, 4 or more in none. The kill line is not met. The planted quartic was counted as 4.
- **Not shown:** that at most two of the three are stable. The checker rightly notes that G locates balances; it is not an equation of motion, so even the one-dimensional index argument has no footing yet. That stays a conjecture, supported by the one example in the 6 Nov note.
- **What it means:** one level of the working grammar can carry at most two stable resting organisations at once (if the stability conjecture holds), and never a continuum. That is a structural cap on per-level species. It gives O_focus's shape ('isolated attractors') a proved instance for balances, though not for cycles.
- **Independent check:** CONFIRMED. The checker re-derived every step, proved φ′ < 0 in all cases including m = 1, and found only 1 or 3 roots in its own 6 000 draws, including a targeted search. Caveats: keep 'generically'; 1/c < 1 needs k1 or k7 > 0; the stability sentence is a conjecture.
- **Confidence:** high.

## 5. New candidates (post-failure)

None. No candidate failed tonight. Item 1's harness failing its own planted line is a test-infrastructure failure, logged as such, with no candidate revised.

## 6. Suggested Map changes for Glenn to decide

Recommendations only.

1. **K_sat:** record that tonight's independent check confirmed S1, S1b, S2, S4(a) and S5 symbolically (receipt: N-2026-11-09-1, check CONFIRMED). Consider re-tagging the clause 'on a closed level, cycling needs a lag' as 'needs a route through L or P [theorem, model]; that the route acts as a delay is a reading'.
2. **New Known node, or a line on K_sat:** 'One level holds at most three balances, under any threshold recruitment law' [theorem, model] (receipt: N-2026-11-09-5, check CONFIRMED). It bears on O_focus.
3. **G_species:** note that its proof scope (three return paths, mass action) is no longer the working grammar, and that its listed deps omit the archived proof it cites. Isolation of balances is re-supported by item 5; non-drift has no working-grammar support (receipt: N-2026-11-09-2, check PARTLY). Re-rooting is Glenn's call.
4. **C_deficiency:** note that the working grammar is outside its premise class, so it is vacuous there (receipt: N-2026-11-09-2).
5. **P_traj (promoted):** consider a note, or a rewording of the illustrative mechanism, to: recruitment uses up Void, and lost Contact returns by routes through L and P. The promotion itself is not touched (receipt: N-2026-11-09-3, check PARTLY).
6. **C_seed:** mark half (ii) as following [model, given bounded supply], and write the shape of the gap for half (i): a resource back-reaction from the upper rung, bounded by aggregate capacity (receipt: N-2026-11-09-4, check PARTLY).

## 7. Suggested follow-ups (candidates for tomorrow's queue)

- **Stability of the three balances (D3):** for kr ≥ 2, is the middle balance always unstable and the outer two stable, in the full four-role system on an open level? Start from the reduced V-equation with C, L and P pinned, and check whether the Jacobian's determinant sign tracks G′.
- **Isolation of cycles (D2):** what would show that a level's clocks are isolated within each conservation class, for example with Floquet multipliers away from 1 apart from the phase and the total?
- **C_seed back-reaction (D2):** specify the smallest two-way resource coupling consistent with 'Shared supply… each unit counted once' and the ladder principle, before any run.
- **Literature check (D1):** O_protect's 'rare' branch. Is there a published result on the cheapest integer-changing path in lattice models with refinement-stable cost? This was skipped tonight.
- **Harness (D1):** a sound planted failure for bound checks, using an eligibility test that does imply violation of the bound.

## 8. Verification handoffs

```
Task (DeepSeek / Astra). Given: for m ≥ 1, 1 ≤ kr ≤ m, F(x) = Pr[Bin(m,x) ≥ kr] = I_x(kr, m−kr+1); constants α, β, γ, k10, k3 > 0 with α/β ≤ 1. Let G(x) = (k10 + k3·F(x))(α − β·x) − γ·x on I = (0, α/β). Prove or refute: G has at most three zeros on I counted with multiplicity. Suggested route: G'' = k3[F''(α−βx) − 2βF'], F' = K x^(kr−1)(1−x)^(m−kr), show φ(x) = F''/F' − 2β/(α−βx) is strictly decreasing on I, then Rolle. Also state precisely what weaker hypothesis on F (e.g. F' > 0 and log-concave on I) suffices.
```

```
Task (DeepSeek). Given the open-level system dC/dt = −(k1+k2+k7)C + k6L + (k10 + k3F(x))V, dV/dt = k2C + k5L + k8P − (k10 + k3F(x))V + k12, dL/dt = k1C − (k5+k6)L, dP/dt = k7C − (k8+k9)P, with x = C/(C+V+L+P), F as the binomial tail with m, kr, all rates positive. At any balance, C*, L*, P* are fixed (C* = k12(k8+k9)/(k7k9)) and V* solves g(V) = (k10 + k3F(C*/(C*+L*+P*+V)))V = D·C*, D = k2+k7+k1k5/(k5+k6). Determine whether the sign of the Jacobian determinant at a balance equals the sign of −g'(V*) (or another fixed relation), and hence whether, when three balances exist, the middle one is always unstable. Report a proof or a counterexample.
```

## 9. Run notes

- **Access:** all required sources were reached: the spec, STEERING, the standing constraints, the Premise Map (read in full through the Artifact tool, version 1794023894-eb69, 1 065 lines) and the saturation note. The project instructions were already in context. The narrative spine (context only) was not opened, for time.
- **Freeze:** the queue was saved as its own file at 06:25 UTC, before any item work, so the report never needed editing. The outline of item 5's proof occurred to me while I was building the queue. This is declared in the queue.
- **Item 1 numerics:**
  - Radau was too slow and was swapped for LSODA.
  - The first planted run was miscounted as a solver failure, so partial solutions are now checked.
  - The process was then killed by memory exhaustion after about 245 of 300 draws.
  - By its own frozen 90% line the harness was blind anyway. Not re-run.
  - Choices not fixed in the queue: starts log-uniform in [10⁻², 10²], horizon 200/min(rate) capped at 2 000, seed 20261109.
- **Item 5 numerics:** the first launch counted only interior sign changes and missed roots lying before the first grid point, which showed up as even counts. It was relaunched with the exact endpoint signs included, before any count was used. Sign changes cannot see tangent double roots.
- **Checks:** independent checks were done by two fresh subagents that had not seen the working: one for items 2–4 (texts only) and one for items 1 and 5 (re-derived, with its own scripts). Their full reports are summarised in section 4.
- **Files:** the scripts are in the session sandbox (n1_sym.py, n1_num.py, n5_num.py, and the checker's s1.py and r5.py). They were not uploaded, because none is a standalone result beyond what this report states.
