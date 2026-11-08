# The saturation mechanism in the working turnover grammar

**Stamp:** SANDBOX / DRAFT. Promotes nothing. 6 Nov 2026. Claude. [model] register: the rate equations are an effective-register summary of step processes, at large numbers.
**Classes:** A proved · B refuted as stated · C blocked · D not mathematical · E external fact.
**Target:** the premise-map gap 'The saturation mechanism itself'. It asked for a recruitment law, a counter-process and a lag, stated at least in words, and for a balance set by the process itself.
**Declared first:** SPEC.md (SHA-256 cc7ac93a1740b46be66acd2418567917823264359693a8d63c409801def9eb09) was hashed before any code was written. One revision, R1, changed the planted failure. It was declared before checks.py was written or any check run. Both are in RUN.md.
**Revised 6 Nov** after a Jev claim-ledger pass (TypeSafe, jev-1.13.0, 62 claims). The pass flagged wording that ran ahead of the proofs: hypotheses dropped in the plain-words summary, open-level results stated without that scope, and one sentence that misdescribed why R1 was made. The revision changes wording and scope only. No proof and no check result changed.

**Evidentiary limits.**
- Everything here is [model]. It concerns one level of the Contact/Void grammar as encoded in pull request 4 (roles C, V, L, P), with the crowding release removed (Glenn, 1 Nov) and the all-neighbours count (Glenn, 31 Oct). Whether these rate laws are physically entitled is the separate gap 'What rate law do threshold triggers give over the ensemble?', which this note does not touch.
- A level is not a composite. 'Self-limiting growth' is stated for composites, and nothing here is carried to the composite rung.
- The class-A results are short proofs, given in full below. The numerical checks are preregistered receipts with kill lines and planted failures. They are not proofs.
- S1 reads off how the grammar is built: a role change moves a unit between roles and creates none. Its content is the identification of what bounds a level, not a dynamical discovery (P2.6-03 §3: a calculation must not merely certify its own construction).
- S2 is already on the map, in 'A level is set by three things…'. It is restated here for any recruitment law, not claimed as new.
- The lag check on the two moderate-rate clocks is exploratory: two clocks, numerical, no kill line.

---

## In plain words

In the grammar now in use, every part the gap asked for can be stated. The recruitment law is the grammar's own and is assumed here; whether it is physically entitled stays open. The counter-process, the bound, the balance and the lag are proved for one level of this grammar [theorem, model].

- **Recruitment law** (the grammar's own, assumed here). Void becomes Contact at k3·V·F(x), where F(x) is the chance that at least kr of a site's m neighbours are Contact, plus seeding at k10·V. With one-neighbour recruitment (kr = 1), sparse Contact grows in proportion to the Contact present. With kr ≥ 2 it grows as a power of it, so scarce Contact relies on seeding.
- **Counter-process.** The Void that growth uses up. Each recruitment turns a unit of Void into a unit of Contact and creates nothing. With one-neighbour recruitment, recruitment per unit of Contact falls as Contact's share rises; with kr ≥ 2 it first rises, then falls (S3). No release triggered by crowding is needed, and the working grammar has none.
- **What bounds a level.** Take an open level with seeding, a route to breach, and breach itself: k10, k7, k9 > 0, and L drains. On it, every solution is bounded under any recruitment law whatever, including autocatalysis that strengthens without limit [theorem, model; S1]. The bound is set by supply from below, by breach, and by seeding, which keeps Void from piling up. It is not set by the threshold cap. Without seeding, under the threshold law or mass action, an open level with no Contact accumulates Void without bound (S1b).
- **The balance.** On an open level, the amount of Contact at a balance is pinned by throughput, and recruitment and seeding set only the Void reserve around it (S2). With kr = 1 there is exactly one balance, open or closed (S4). With kr ≥ 2 there can be three. On an open level these share the same Contact and differ in Void reserve. In the one example checked, two are stable and one is unstable.
- **The lag.** On a closed level with only Contact and Void, overshoot and cycling are impossible. So on a closed level, a cycle needs a delayed route back through L or P [theorem, model; S5]. An exploratory scan of the two moderate-rate clocks gave this: the closed one stopped cycling when either route was weakened, and the open one only when the route through P was.

Claude's reading, not a derivation: this is the shape monism asks for ('No bound on a pattern can be supplied from outside'). What keeps recruitment from breaking the bound is the single substrate's own role conservation: Contact and Void are roles, not substances (floor 'Contact and Void are scale-relative roles'). The bound itself is set by supply, breach and seeding, which the grammar already has. Nothing is added to supply it.

---

## The grammar

One level, roles C, V, L, P ≥ 0, T = C + V + L + P, x = C/T (all-neighbours count), F(x) = Pr[Bin(m, x) ≥ kr] with 1 ≤ kr ≤ m. o = 1 for an open level and 0 for a closed one. Rate order as in `grammar-instability/ginst/model.py`, with k11 = 0.

```
dC/dt = −(k1 + k2 + k7)·C + k6·L + (k10 + ρ)·V
dV/dt =  k2·C + k5·L + k8·P − (k10 + ρ)·V + o·k12
dL/dt =  k1·C − (k5 + k6)·L
dP/dt =  k7·C − (k8 + o·k9)·P
```

ρ ≥ 0 is the recruitment per unit of Void. In the working grammar ρ = k3·F(x). S1 allows any ρ.

Two constants recur: D = k2 + k7 + k1·k5/(k5 + k6), the net loss rate of Contact once L has settled, and c = 1 + k1/(k5 + k6) + k7/k8.

---

## S1. A level is bounded by role conservation, under any recruitment law (class A)

**Statement.** Let k10, k7, k9 > 0 and k5 + k6 > 0. On the open level, let ρ(t) ≥ 0 be any recruitment per unit of Void along the solution, depending on the state in any way. Let A0 be the level's transfer matrix with ρ = 0, and w the vector of expected times to exit under A0, so that wᵀ(−A0) = 1ᵀ. Then

w·y(t) ≤ max( w·y(0), w_max·w_V·k12 ) for all t ≥ 0,

so every non-negative solution is bounded. On the closed level, C + V + L + P is constant.

**Proof.** Write dy/dt = A0·y + ρ·V·(e_C − e_V) + k12·e_V. A0 is compartmental: off-diagonal entries ≥ 0, column sums 0 except P's, which is −k9. Under A0 every role reaches the exit: V → C at k10, C → P at k7, P → out at k9, and L → V or C at k5 + k6. So −A0 is a nonsingular M-matrix and w = (−A0)⁻ᵀ·1 > 0. The V-column of wᵀA0 = −1ᵀ reads k10·(w_C − w_V) = −1, so w_V − w_C = 1/k10 > 0. Then

d(w·y)/dt = −(C + V + L + P) − ρ·V/k10 + w_V·k12 ≤ w_V·k12 − (w·y)/w_max,

and the bound follows by comparison. On the closed level the four right-hand sides sum to zero. ∎

**What it says.** Recruitment moves substrate from Void to Contact, one step nearer the only exit. It never adds substrate, so in the weighted count it can only lower the load. That is why, under S1's hypotheses, no recruitment law, however strongly it favours growth, can make an open level run away: mass action (ρ = k3·C) and ρ = k3·C² are bounded too. The threshold cap F ≤ 1 is not used. The crowding release is not used.

## S1b. Seeding is what bounds the Void reserve (class A)

**Statement.** With k10 = 0, under the threshold law (kr ≥ 1) or mass action, the open level has unbounded solutions.
**Proof.** On the face C = L = P = 0 the recruitment flux is 0 (F(0) = 0 for kr ≥ 1, and k3·V·C = 0), so the face is invariant and dV/dt = k12 on it. Then V(t) = V(0) + k12·t. ∎
'One level of the grammar persists under threshold rates…' already showed seeding necessary for persistence [theorem, model]. S1b adds that, on an open level, it is also necessary for boundedness [theorem, model].

## S2. Contact is pinned by throughput (restated; already on the map)

At any balance of the open level, and for any ρ: dP/dt = 0 and d(C + V + L + P)/dt = k12 − k9·P = 0 give P* = k12/k9, C* = (k8 + k9)·k12/(k7·k9) and L* = k1·C*/(k5 + k6). Along any solution, bounded by S1, the long-run means of P and C converge to the same values, because (total(t) − total(0))/t → 0 and (P(t) − P(0))/t → 0. So recruitment and seeding set only the Void reserve. 'A level is set by three things…' already carries this. The only addition here is that it holds for every recruitment law.

## S3. The counter-process is density-triggered (class A)

**Statement.** The recruitment per unit of Contact is r = k3·V·F(x)/C = k3·(V/T)·(F(x)/x). At fixed L, P and T:
- For kr = 1, r falls strictly as Contact's share x rises: F(x)/x = (1 − (1 − x)^m)/x = Σ_{j=0}^{m−1} (1 − x)^j, which strictly decreases from m at x → 0 for m ≥ 2, and V/T = 1 − x − (L + P)/T also falls.
- For kr ≥ 2, F(x)/x ~ C(m, kr)·x^(kr−1) → 0 as x → 0, so r rises from zero and then falls to zero as V/T → 0. This is a threshold: scarce Contact cannot recruit, and seeding carries it.

**Proof.** Both are direct from the formulas above. ∎

## S4. How many balances (class A)

**Statement.** Take k10 > 0 and all listed rates positive. (a) For kr = 1 there is exactly one balance, on the open level and, for each total, on the closed level. (b) For kr ≥ 2 there can be several. On the open level they share C*, L* and P*, by S2, and differ only in V*.

**Proof, open level.** With C*, L*, P* pinned, the remaining balance condition (dC/dt = 0) is g(V) = D·C*, where g(V) = (k10 + k3·F(a/(b + V)))·V, a = C* and b = C* + L* + P*. Write h(V) = V·F(a/(b + V)) and x = a/(b + V). Then h′(V) = F(x) − x·F′(x)·V/(b + V). For kr = 1, F(x) = 1 − (1 − x)^m is concave with F(0) = 0, so F(x) ≥ x·F′(x). Since V/(b + V) < 1 and F′ > 0, this gives h′ > 0. So g strictly increases from g(0) = 0 to ∞ (k10 > 0), and g = D·C* > 0 has exactly one root. ∎
**Proof, closed level.** Settled L and P give L = k1·C/(k5 + k6) and P = k7·C/k8, so V = T − c·C. The balance condition is D·x = R(x) := (k10 + k3·F(x))(1 − c·x) on (0, 1/c). For kr = 1, R″ = k3·F″·(1 − c·x) − 2·c·k3·F′ ≤ 0, so R is concave. R(x) − D·x is then concave, equals k10 > 0 at 0 and −D/c < 0 at 1/c, and so has exactly one root. The share x* does not depend on T. ∎
**(b) by example**, from N3 below: an open level (m = 10, kr = 6) has three balances with C = 9.9835, L = 0.3184, P = 3.3399 and V = 2.589, 14.394 and 79.747. The outer two are stable and the middle one is unstable (eigenvalues in the appendix). This is the 13 Oct result, one species expressed two ways, now in the working grammar.

## S5. Cycling needs a lag (class A, with an exploratory check)

**Statement.** On a closed level with k1 = k7 = 0 and L(0) = P(0) = 0, C(t) is monotone and converges to a balance: no overshoot and no cycle.
**Proof.** L and P stay 0, and V = T − C, so dC/dt = −k2·C + (k10 + k3·F(C/T))·(T − C) is a scalar autonomous equation, whose solutions are monotone. ∎ If L(0) or P(0) is positive, both decay exponentially and the limit set lies in the same scalar system. So on a closed level, cycling needs a delayed route back through L or P. This proves [theorem, model], for a closed level of this grammar, the counterpart of the line 'Cycling around balance requires a lagged counter-process' on 'Self-limiting growth'. That premise is stated for composites. This does not settle it there, and its tag is Glenn's to change.

**Exploratory, no kill.** With the crowding release off, each delayed route of the two moderate-rate clocks was scaled down by s:

| clock | route scaled | s = 1 | 0.3 | 0.1 | 0.03 | 0.01 |
|---|---|---|---|---|---|---|
| 19387, closed | k1 (through L) | cycle, 6.352 | rest | rest | rest | rest |
| 19387, closed | k7 (through P) | cycle, 6.352 | rest | rest | rest | rest |
| 33538, open | k1 (through L) | cycle, 4.844 | cycle, 4.643 | cycle, 4.597 | cycle, 4.582 | cycle, 4.577 |
| 33538, open | k7 (through P) | cycle, 4.844 | rest | rest | rest | rest* |

\* Relative swing 8.5×10⁻⁴ at s = 0.01, at the edge of the declared 10⁻³ rule. At that s, C* is a hundred times larger, so this is a different regime.

In this scan the closed clock stopped when either delayed route was weakened. The open clock stopped only when the route through P, which is also its breach, was weakened. Two clocks and five scale factors make this an observation, not a rule.

---

## Numerical receipts (preregistered; SPEC.md with R1)

Integration: scipy `solve_ivp`, LSODA, rtol 10⁻⁹, atol 10⁻¹². The right-hand side was written independently in numpy.

| check | what | result | verdict |
|---|---|---|---|
| N0 harness | reproduce PR 7's clocks with k11 as drawn | 19387: period 6.35241, C in [0.7018, 1.5322]; 33538: period 4.84392, C in [0.2175, 1.2928] | pass (targets 6.352, 4.844; matches the map's recorded ranges) |
| N1 bound (S1) | open level, rates in [10⁻², 10²], 600 draws × 4 starts, recruitment by the threshold law, mass action (k3·C) or k3·C², rotating | 2400 of 2400 runs completed; 0 bound violations; largest w·y(t)/bound = 1.0000000000000004 (the start) | kill not met |
| N1 planted, R1 | replication faster than every Contact loss | flagged in 200 of 200 draws | pass (≥ 95%) |
| N1 planted, as declared | creation k3·C² without using Void | flagged in 173 of 200 draws (86.5%) | reported, no criterion. R1 was declared before any check ran, because this model is not guaranteed to blow up in the rate box. The 86.5% seen afterwards confirms that it would have missed the 95% line |
| N2 (S1b) | k10 = 0 from (0, V0, 0, 0): V(100) = V0 + 100·k12 | max relative error 6.4×10⁻¹⁶ in 20 draws per law | pass |
| N3 (S4) | balance count, 5000 draws per level, kr ∈ 1..m | kr = 1: exactly one balance in 910 of 910 open and 971 of 971 closed draws. kr ≥ 2: three balances in 73 of 4090 open (1.8%) and 59 of 4029 closed (1.5%) draws. No draw gave two, but that is not a finding: the counter counts sign changes, and the end signs differ, so it can only return an odd number | kill not met; planted cubic: 3 roots found |
| N4 (S5) | closed, k1 = k7 = 0, 300 draws: sign changes of dC/dt | 0 of 300 | kill not met |

**Report only. This was added after the run; it was not declared and is not a check.** result_N1.json also logs, for each law, the second-half mean Contact over the pin C*, and a rough count of runs still swinging. Neither was declared, and S2 is cited, not tested. The logged mean runs from 0.02 to 1.75 times C*. To see why, diag_n1_mean.py and diag_n1_followup.py re-ran the 600 first starts. In 83 of them the mean is more than 5% off the pin over the declared window. There are two causes, and neither bears on S1 or S2:

- **Still filling: 79 runs, all below the pin.** Over the window the level's total was still growing. In these runs the window identity holds to 10⁻⁶. That identity is exact: the mean of C equals the pin, minus the growth of the total and the change in P over the window. In the six lowest runs, growth of the total accounts for the whole shortfall, and the growth went mostly into L or Void. A later window, from 10 to 20 times the run length, moves all 79 toward the pin (0.019 → 0.31, 0.08 → 0.80, 0.12 → 0.91), and leaves 10 more than 5% off. The declared run length, 200 over the smallest rate, is shorter than some levels take to fill.
- **Sampling: 4 runs, plus 11 within 5%, all under k3·C² recruitment.** In these runs the mean taken from the 2001 saved points is wrong: the sampled identity is off by up to 76%. Integrating ∫C dt along with the ODE restores the identity to 10⁻¹¹, so the error is in the sampling, not in the solution. It puts 14 of these 15 runs within 1.2% of the pin; the fifteenth, at 0.83, is still filling. In draw 245 the sampled mean is 1.75 times the pin; integrated, it is 0.996.
- **What this means for N1:** as declared, N1 checks the bound only at output times. In these 15 runs, the motion between output times was not checked. S1 rests on its proof; N1 is a receipt.

---

## What this does not show

- Whether the rate laws (constant supply k12, seeding k10·V, threshold recruitment F) are physically entitled. That stays open under 'What rate law do threshold triggers give over the ensemble?'.
- Anything at the composite rung, or about a persistent composite. 'Self-limiting growth' keeps its kill line, which needs a persistent composite, and none exists yet.
- Anything about finite ensembles: die-out, escape and lifetimes are large-number questions not asked here.
- The size of the bound. w_max·w_V·k12 is loose, and it is not a prediction of how much a level holds. S2 gives that for Contact.
- Whether saturation counts as the counter-process in the sense of 'Self-limiting growth'. That is a reading, which Glenn gave on 1 Nov ('yes and yes'). This note shows what that reading amounts to in the grammar. It does not make the reading compulsory.

## Kill triggers

- S1, S1b, S3, S4, S5: a counterexample within the stated hypotheses, which would be a check of the proofs.
- The reading 'saturation is role conservation': a route admitted in the grammar that creates Contact without using Void, or an open level that is bounded with every listed rate positive although its bound involves none of supply, breach or seeding.

## Placement on the premise map (done 6 Nov on Glenn's instruction to execute)

- New Known node: 'Growth pays for itself in Void: with seeding, a level is bounded under any recruitment law; on a closed level, cycling needs a lag'. Not promoted.
- The gap 'The saturation mechanism itself' is archived as filled in the [model] register, with a pointer to the new node and its record kept. Closing a gap is Glenn's ruling: the archive is reversible, and it stands only if he keeps it. 'Why is the set of persistent closures discrete?' now rests on the new node in its place.
- Notes on 'Self-limiting growth', 'One level of the grammar persists…' and 'Each level is fed and seeded…'.

---

## Appendix

**Files** (C:\Users\gomni\GENERAL\phys2-saturation-2026-11-06\): SPEC.md, RUN.md (hash and R1), checks.py, example_stability.py, diag_n1_mean.py, diag_n1_followup.py, result_N0–N4.json, result_example_stability.json, result_diag_n1_mean.json, result_diag_n1_followup.txt, run_stdout.txt. example_stability.py, the two diag_n1 scripts and their result files are report-only, written after the run.

**Eigenvalues at N3's three balances** (open, m = 10, kr = 6; residuals below 10⁻¹³):
- V = 2.589: −1.377, −5.990 ± 3.527i, −15.248 (stable)
- V = 14.394: +4.517, −0.579, −5.646, −15.474 (unstable)
- V = 79.747: −0.198, −2.496, −6.211, −15.623 (stable)

**Example rates** (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12) = (0.4885, 0.1976, 13.992, 7.024, 8.293, 2.092, 1.267, 4.986, 0.3117, 0, 16.654).
