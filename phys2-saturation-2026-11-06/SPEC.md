# SPEC — The saturation mechanism in the working turnover grammar

SANDBOX/DRAFT · Claude · 6 Nov 2026 · declared before any computation; SHA-256 recorded in RUN.md before checks.py is written.

## Target

Map gap 'The saturation mechanism itself' (O_sat). It asks for a recruitment law, a counter-process and a lag, stated at least in words, and a balance set by the process itself. Glenn ruled on 1 Nov that saturation is the counter-process of 'Self-limiting growth' and that the crowding release is not needed. Nothing has derived that in the grammar now in use. This SPEC does that, in the [model] register only.

## The grammar (one level; as in grammar-instability/ginst/model.py, PR 4, with k11 = 0)

Roles C (Contact), V (Void), L, P. o = 1 for an open level, 0 for a closed one. x = C/(C+V+L+P), the all-neighbours count (Glenn, 31 Oct). F(x) = Pr[Bin(m, x) ≥ kr].

- C → L at k1·C; C → V at k2·C; C → P at k7·C
- L → V at k5·L; L → C at k6·L
- P → V at k8·P; P → out at o·k9·P (breach)
- in → V at o·k12 (supply from below)
- V → C at (k10 + ρ)·V, with seeding k10 and recruitment ρ ≥ 0. In the working grammar ρ = k3·F(x).
- No crowding release (k11 = 0; Glenn, 1 Nov).

## Claims (proof obligations; tags as in Walls → Method)

- **S1 Bound [theorem, model].** Suppose k10, k7, k9 > 0 and k5 + k6 > 0. Then on the open level every non-negative solution is bounded, for any recruitment ρ(t) ≥ 0 whatever it depends on, mass action and faster-than-linear autocatalysis included. Explicitly, w·y(t) ≤ max(w·y(0), w_max·w_V·k12), where w is the expected exit-time vector of the chain with ρ = 0. On the closed level C + V + L + P is constant. The bound comes from role conservation, supply and breach, not from the threshold cap or any release.
- **S1b Seeding bounds the reserve [theorem, model].** With k10 = 0 the open level has unbounded solutions under the threshold law and under mass action. One is C = L = P = 0, V = V0 + k12·t.
- **S2 Throughput pin.** Already known ('A level is set by three things…'). It is restated here for any ρ: every balance has P* = k12/k9, C* = (k8 + k9)·k12/(k7·k9) and L* = k1·C*/(k5 + k6), and every solution's long-run mean Contact equals C*. It is cited, not tested; checking it numerically would only check the integrator.
- **S3 Density-triggered [theorem, model].** The recruitment per unit of Contact is r = k3·V·F(x)/C = k3·(V/T)·F(x)/x. For kr = 1 it falls strictly as Contact's share rises (at fixed L, P, T). For kr ≥ 2 it rises from 0 and then falls, a threshold.
- **S4 Balance count [theorem, model].** For kr = 1 and k10 > 0 there is exactly one balance, open or closed. For kr ≥ 2 there may be several; on the open level they share C*, L* and P* and differ only in the Void reserve.
- **S5 Lag [theorem, model].** On a closed level with k1 = k7 = 0 there is no overshoot and no cycle: on L = P = 0, C(t) is monotone. Cycling needs a delayed return route through L or P.

## Numerical checks (receipts for the proofs, not searches)

Integration: scipy solve_ivp, LSODA, rtol 1e-9, atol 1e-12, own numpy right-hand side.

- **N0 Harness.** With k11 as drawn, the reimplemented RHS reproduces PR 7's clocks. Draw 19387 (K1b box: seed 31102026, log10 k ~ U(−1, 1)) has period 6.352 ± 0.01. Draw 33538 has period 4.844 ± 0.01. Kill: either fails, and nothing below is reported until it is fixed.
- **N1 Bound (S1).** 600 open-level draws, rates log-uniform in [10⁻², 10²], k11 = 0. The laws rotate: threshold (m ∈ 2..12, kr ∈ 1..m); mass action ρ = k3·C; super-autocatalytic ρ = k3·C². Each draw starts 4 times at scale 10^U(−2, 2) and runs to t = 200 / (smallest rate in use), capped at 2×10⁵. At every output time, w·y(t) ≤ max(w·y(0), w_max·w_V·k12)·(1 + 10⁻⁶) + 10⁻⁹. Kill: any violation in a run the integrator completes. Runs the integrator fails are reported, not dropped. **Planted failure:** recruitment that creates Contact without using Void (dC += k3·C², dV unchanged) must be flagged (violation or blow-up) in ≥ 95% of 200 planted draws.
- **N2 (S1b).** k10 = 0 from (0, V0, 0, 0): V(100) = V0 + 100·k12 to relative 10⁻⁸ in 20 draws per law.
- **N3 Balance count (S4).** 5000 draws per level (open and closed), threshold law, k11 = 0. Roots are found by sign changes on a 4000-point log grid, refined by brentq. Open level: g(V) − D·C* over V ∈ [10⁻¹²·s, 10¹²·s] with s = C* + L* + P*. Closed level: D·x − (k10 + k3·F(x))(1 − c·x) over x ∈ (0, 1/c). Here D = k2 + k7 + k1·k5/(k5 + k6) and c = 1 + k1/(k5 + k6) + k7/k8. Kill: any kr = 1 draw with a root count other than 1. Reported: the share of kr ≥ 2 draws with 3 roots, and one worked example. **Planted:** the counter must find exactly 3 roots of (x − 0.2)(x − 0.5)(x − 0.8) on (0, 1).
- **N4 Lag (S5).** 300 closed draws with k1 = k7 = 0 and L(0) = P(0) = 0, threshold law. Kill: dC/dt changes sign by more than 10⁻⁸ relative after its first zero. **Exploratory, no kill:** draws 19387 and 33538 with k11 = 0, scaling k1 or k7 by s ∈ {1, 0.3, 0.1, 0.03, 0.01}; report whether a cycle survives, and so which delayed route each clock uses.

## Scope and limits, declared

- Everything is [model]: rate equations as an effective-register summary of step processes, at large numbers. Nothing here is about finite ensembles.
- Physical entitlement of the rate laws stays with 'What rate law do threshold triggers give over the ensemble?'. This SPEC does not touch it.
- The grammar is a level, not a composite. 'Self-limiting growth' is stated for composites. Carrying the result to the composite rung is not claimed.
- S1 reads off how the grammar is built: role changes move a unit between roles and create none. Its content is the identification of what bounds a level, not a dynamical discovery (P2.6-03 §3: a calculation must not merely certify its own construction). The checks are receipts for the proofs.
