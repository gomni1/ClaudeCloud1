# PART B — RESULTS

## Freeze record

`B/SPEC.md` was written and frozen before any Part B simulation code ran. The
deterministic balance characterisation of SPEC §2 (`B/fixed_points.py`) was run
before the freeze and is disclosed: it is an algebraic property of the stated
constants, contains no stochastic simulation, and fixes no target or threshold
beyond what the task statement already gave.

- `B/SPEC.md` SHA-256: `806824d20f02b0c59c59da052bae4ec30ac1389fcb43ba5cb7dd1d20142ef864`
- frozen at: 2026-11-01T00:23:02

Balances recovered (residual < 1e-15), maximum real part of the Jacobian
spectrum in brackets: `(1,2,1,0.5)` stable `[-0.1514]`, `(1,3,1,0.5)` unstable
`[+0.2953]`, `(1,4,1,0.5)` stable `[-0.1303]`.

Change log after the freeze (revisions, failures, bug fixes) is kept in §5 of
this document. Nothing is removed from it.

## 3. Planted checks (SPEC §7)

| check | verdict | detail |
|---|---|---|
| P1 scripted medians | **PASS** | 6 scripted paths; every delta recovered exactly; median 0.175000 against an expected 0.175000 |
| P2 passage detector | **PASS** | every passage flag exact; passage count 2 against an expected 2 |
| End-to-end consistency | **PASS** | 400 real simulated runs rescanned from their recorded paths; **0 mismatches** in streaming delta or passage flag |

All Part B planted checks pass, so the gate of SPEC §7 is satisfied and the
results below count.

## 4. Runs (SPEC §4)

No run reached the 10^7-reaction safety cap at any size or direction, so nothing
was discarded. Every cell greatly exceeded the 2000-run minimum within its
3-CPU-minute budget (1081 CPU-seconds over the six cells).

| Omega | direction | runs | capped | passage fraction | non-passing runs | median delta | mean delta |
|---|---|---|---|---|---|---|---|
| 8 | up | 817000 | 0 | 0.0762 | 754746 | 0.2500 | 0.2908 |
| 8 | down | 150000 | 0 | 0.0686 | 139714 | 0.2500 | 0.2935 |
| 10 | up | 887000 | 0 | 0.0134 | 875118 | 0.3000 | 0.3588 |
| 10 | down | 183000 | 0 | 0.0052 | 182055 | 0.4000 | 0.4208 |
| 12 | up | 589000 | 0 | 0.0026 | 587442 | 0.4167 | 0.3917 |
| 12 | down | 121000 | 0 | 0.0009 | 120890 | 0.4167 | 0.4453 |

## 5. Claim — verdict: **KILL**

*Prediction:* among runs that did not visit `D`, the median delta of **up**
switches is **below** that of **down** switches, at each size.
*Kill:* at 2 or more of the 3 sizes, median delta of non-passing **down**
switches is **less than or equal to** that of up switches.

| Omega | median delta up | median delta down | prediction holds (up < down)? | kill condition met (down <= up)? |
|---|---|---|---|---|
| 8 | 0.2500 | 0.2500 | **no** | **yes** |
| 10 | 0.3000 | 0.4000 | yes | no |
| 12 | 0.4167 | 0.4167 | **no** | **yes** |

**2 of 3 sizes meet the kill condition, so the kill line is met and the
candidate 'Identity and size, through coupled routes' is killed on this line.**

The kill is carried by **exact ties** at Omega = 8 and Omega = 12, not by a
reversal. This was anticipated and preregistered: SPEC §6 records that delta
lives on a lattice of step `1/Omega`, that exact ties are therefore possible,
and that by the stated wording a tie counts towards the kill. At these sizes the
lattice is coarse — 0.125, 0.1 and 0.0833 — and the sample median lands on a
lattice point.

**Context, not the preregistered statistic.** The *mean* delta of non-passing
runs is lower for up switches at all three sizes
(0.2908 vs 0.2935;
0.3588 vs 0.4208;
0.3917 vs 0.4453),
and the Omega = 10 median does show up < down. So there is a weak ordering in the
predicted direction that the preregistered median statistic does not resolve at
these lattice spacings. **This does not change the verdict**, which is fixed by
the frozen criterion; it is recorded so the kill is not read as a reversal. A
test able to resolve it would need either larger `Omega` or a statistic that is
not pinned to the lattice — that would be a new claim, not this one.

## 6. Passage fractions, against PR 6

| Omega | up passes D | down passes D | ratio up/down |
|---|---|---|---|
| 8 | 0.0762 | 0.0686 | 1.11 |
| 10 | 0.0134 | 0.0052 | 2.59 |
| 12 | 0.0026 | 0.0009 | 2.91 |

Up switches pass through dissolution more often than down switches at **every**
size, and the asymmetry grows sharply as the ensemble grows (1.1x at Omega = 8,
2.9x at Omega = 12). The *direction* of this asymmetry agrees with what the task
statement reports from PR 6 — up more often, down less often, relative to a race
between independent routes. **The quantitative comparison against PR 6 has not
been made here: PR 6's numbers are not in this workspace.** Supplying them would
complete the check; nothing in this part depends on it.

Note that the absolute passage fractions fall steeply with size (0.076 to 0.003
for up switches), as expected for an excursion to a boundary state.

The delta distributions are in `B/fig_delta.png`.

## 7. Change log

1. No planted check failed; no bug fix was required after the freeze.
2. A resource guard of 2x10^6 completed runs per cell is present in
   `B/driver_b.py` alongside the 3-CPU-minute budget. It never bound: the
   largest cell completed 887,000 runs. It alters no target or criterion.
3. The median ties at Omega = 8 and 12 were anticipated in the frozen SPEC §6
   and resolved by the frozen wording. No criterion was altered after the
   freeze.

## 8. Evidence

`B/evidence_B.json.gz` — per-cell run counts, passage fractions, delta medians,
means, quantiles and full delta histograms, plus the planted-check records.
