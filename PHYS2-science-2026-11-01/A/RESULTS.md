# PART A — RESULTS

## Freeze record

`A/SPEC.md` was written, the pilot of SPEC §9 was run and its selected radii
were written into §9, and the document was then frozen. **No production
simulation code was run before this freeze.**

- `A/SPEC.md` SHA-256: `dc0d610e639215764e28245fe9d8c981a5cd3377ff233f587bdc846709350866`
- frozen at: 2026-11-01T00:13:44
- frozen cycle files: `A/cycle_A1.npz`
  `45abcbb20e5e5a50ddb683a058d5998c000697ae2269c207095b1859d7b67920`,
  `A/cycle_A2.npz`
  `6cc92294b9da32e8bc43e99a54f9fda022789e5373396b85d69045eaa62c5196`

Change log after the freeze (revisions, failures, bug fixes) is kept in §5 of
this document. Nothing is removed from it.

## Pilot (SPEC §9, run before the freeze, disclosed)

`Omega = 400`, 30 CPU-seconds per cell, 222.9 CPU-seconds total
(3.72 CPU-minutes, cap 5). Pilot seeds are disjoint from production
seeds and **no pilot datum enters the test**.

| model | R | exits | periods | exits/period | >= 0.1/period |
|---|---|---|---|---|---|
| A1 | 0.75 | 1883 | 827.7 | 2.2750 | yes |
| A1 | 1.00 | 1309 | 821.7 | 1.5931 | yes |
| A1 | 1.50 | 672 | 818.1 | 0.8214 | yes |
| A1 | 2.00 | 428 | 828.1 | 0.5168 | yes |
| A2 | 0.75 | 2000 | 1754.2 | 1.1401 | yes |
| A2 | 1.00 | 2000 | 2608.1 | 0.7668 | yes |
| A2 | 1.50 | 750 | 3144.9 | 0.2385 | yes |
| A2 | 2.00 | 125 | 3141.2 | 0.0398 | no |

Selection rule "smallest R giving at least 1 exit per 10 periods" gives
**R = 0.75 for A1 and R = 0.75 for A2**. The exit rate is monotonically
decreasing in R, so the rule is satisfied at the floor of the candidate set for
both models; it was applied as written.

## 3. Planted checks (SPEC §10)

| check | verdict | detail |
|---|---|---|
| P1 modulated hazard | **PASS** | chi-square 313.0 on 9 d.o.f., p = 4.55e-62 < 0.05; recovered modulation b = 0.5529 against a true 0.5, relative error 10.6 % (bar: 20 %) |
| P2 constant hazard | **PASS** | 46/50 replicates with p >= 0.05 (92 %, bar: 90 %) |
| P3 drift at Omega = 1e5 | **FAIL** | median drift 0.2795 (A1) and 0.0449 (A2) against a bar of 0.01 |

**P3 failed as written, and the failure stays on the record.** The gate of
SPEC §10 — "all must pass before results count" — is therefore **not satisfied
as frozen**. The S4' results in §5 are reported, and are flagged as resting on
a planted-check gate that one check did not clear. Whether that is disqualifying
is Glenn's call, not this document's.

### 3.1 Diagnosis of the P3 failure (measurement, not a revision)

The frozen P3 metric compares the stochastic state with the deterministic state
**at the same time**. That quantity is dominated by *phase diffusion*, which is
an intrinsic property of a stochastic clock, not an error of the simulation.
Decomposing the same 11 seeds:

| model | frozen P3 metric (time-matched) | distance to the cycle as a set | phase slip over one period |
|---|---|---|---|
| A1 | 0.2795 | 0.0200 | 0.0286 of a period |
| A2 | 0.0449 | 0.0074 | 0.0039 of a period |

The cycle's median speed is 0.85 (A1) and 1.07 (A2) RMS radii per unit time, so
a 2.9 % phase slip alone displaces A1 by roughly 0.2 RMS radii — the whole of
the measured time-matched drift.

### 3.2 Revision R1 — new claim, logged

*Claim:* at `Omega = 1e5` the median distance from the state to the
deterministic cycle **as a set**, in unscaled concentrations divided by the RMS
cycle radius, is under 1 %. This is the `d` of SPEC §6 and matches the task
statement's wording "drift ... from the deterministic cycle".
*Result:* A2 **passes** (0.0074); A1 **fails** (0.0200). R1 does not rescue P3.

### 3.3 Revision R2 — new claim, logged

*Claim:* the drift of R1 falls towards zero with ensemble size, confirming that
the chain reproduces the deterministic cycle in the large-ensemble limit — the
property P3 exists to test. *Result:* **passes.**

| model | Omega = 1e4 | 1e5 | 1e6 | log-log slope |
|---|---|---|---|---|
| A1 | 0.1973 | 0.0155 | 0.0043 | -0.831 |
| A2 | 0.0320 | 0.0109 | 0.0020 | -0.605 |

(11, 11 and 7 seeds.) Drift decreases monotonically and the slope brackets the
-0.5 of Poisson scaling. The reading: **the 1 % bar at `Omega = 1e5` sits at or
below these clocks' own fluctuation floor at that size** — for A1 the intrinsic
transverse fluctuation there is about 2 % of the RMS cycle radius, so no correct
simulator could have passed P3 at that size. A1 needs roughly `Omega = 4e5`.

## 4. Production grid (SPEC §7)

`R = 0.75` for both models; burn-in 20 periods, excluded from the budget. Every
cell reached the 2000-exit cap inside its 2-CPU-minute budget, so **no cell was
clock-limited**.

| model | Omega | exits | periods | occupancy | CPU s | chi2 (9 d.f.) | p | min hazard | max hazard | max/min |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 50 | 2000 | 336.6 | 364.0 | 1.6 | 108.5 | 2.92e-19 | 3.663 | 8.297 | 2.27 |
| A1 | 100 | 2000 | 457.4 | 687.2 | 4.2 | 145.1 | 8.95e-27 | 1.366 | 4.952 | 3.62 |
| A1 | 200 | 2000 | 594.9 | 1390.9 | 10.8 | 108.0 | 3.67e-19 | 0.756 | 2.131 | 2.82 |
| A1 | 400 | 2000 | 884.2 | 2862.5 | 31.5 | 251.8 | 4.20e-49 | 0.284 | 1.201 | 4.23 |
| A1 | 800 | 2000 | 1362.7 | 5663.3 | 96.4 | 480.1 | 1.03e-97 | 0.095 | 0.567 | 5.94 |
| A2 | 50 | 2000 | 1741.6 | 1415.8 | 2.2 | 397.7 | 4.24e-80 | 0.920 | 3.147 | 3.42 |
| A2 | 100 | 2000 | 1474.2 | 2106.2 | 3.7 | 343.7 | 1.36e-68 | 0.646 | 1.853 | 2.87 |
| A2 | 200 | 2000 | 1420.0 | 3362.8 | 6.9 | 358.7 | 8.82e-72 | 0.314 | 1.187 | 3.78 |
| A2 | 400 | 2000 | 1773.2 | 5931.5 | 16.9 | 505.0 | 4.77e-103 | 0.152 | 0.669 | 4.41 |
| A2 | 800 | 2000 | 2898.5 | 12312.6 | 53.8 | 737.7 | 5.51e-153 | 0.044 | 0.379 | 8.60 |

## 5. Claim S4' — verdict

SPEC §8 selects "the size with the most exits (at least 200)". **All five sizes
tie at exactly 2000 exits**, because every cell hit the cap; the frozen SPEC
gives no tie-break. Rather than pick one, the test is reported at **every** size.
The ambiguity is immaterial: the verdict is identical at all five.

| model | sizes with >= 200 exits | p < 0.05 at | verdict |
|---|---|---|---|
| A1 | 5 of 5 | 5 of 5 (largest p = 3.7e-19) | **S4' supported — not killed** |
| A2 | 5 of 5 | 5 of 5 (largest p = 1.4e-68) | **S4' supported — not killed** |

The kill line — "p >= 0.05 with at least 200 exits" — is **not** met anywhere.
The escape hazard of both clocks depends on phase, and not marginally: the
smallest chi-square anywhere on the grid is 108 on 9 degrees of freedom.

The binned hazard with 95 % Garwood exact Poisson intervals is in
`A/fig_hazard.png`. The phase contrast **sharpens with ensemble size** — the
max/min hazard ratio rises from 2.3 to 5.9 (A1)
and from 3.4 to 8.6 (A2) between Omega = 50 and
Omega = 800 — the opposite of what a phase-independent escape would do.

## 6. Change log

1. **P3 FAIL** as frozen (§3). On the record; not removed.
2. **R1** logged as a new claim (§3.2): set-distance metric. A2 passes, A1 fails.
3. **R2** logged as a new claim (§3.3): convergence scaling. Passes.
4. **Tie in SPEC §8's selector** (§5): all five sizes tie at the 2000-exit cap.
   Resolved by reporting all five, not by inventing a tie-break. No target,
   grid, threshold or criterion was altered.
5. No bug fixes were required after the freeze. The only post-freeze code
   addition was `run_until_time` in `A/sim_a.py`, used solely by P3; it shares
   its propensities and direct-method step with the production loop and touches
   no production result.

## 7. Evidence

`A/evidence_A.json.gz` — pilot, production grid with per-bin exits, occupancy,
hazards and intervals, and the planted-check records.
