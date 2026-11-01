# PHYS2 — two preregistered tests on the well-mixed grammar
**1 November 2026 · exact Gillespie (Kurtz form), numba · both SPECs frozen before production**

## A — Does a clock's escape hazard depend on its phase? **S4' supported; not killed.**

Both deterministic cycles reproduce the stated periods (A1 6.352409 vs 6.3524;
A2 4.843917 vs 4.8439). The disclosed pilot (3.7 of 5 CPU-minutes, Omega = 400)
selected **R = 0.75** for both models. Every one of the ten production cells hit
the 2000-exit cap inside its 2-CPU-minute budget, so all five sizes tie on exit
count; SPEC §8's "size with the most exits" has no tie-break, so the test is
reported at **every** size. The verdict is the same at all five.

| model | Omega | chi2 (9 d.f.) | p | max/min hazard |
|---|---|---|---|---|
| A1 | 50 | 109 | 2.9e-19 | 2.27 |
| A1 | 100 | 145 | 9.0e-27 | 3.62 |
| A1 | 200 | 108 | 3.7e-19 | 2.82 |
| A1 | 400 | 252 | 4.2e-49 | 4.23 |
| A1 | 800 | 480 | 1.0e-97 | 5.94 |
| A2 | 50 | 398 | 4.2e-80 | 3.42 |
| A2 | 100 | 344 | 1.4e-68 | 2.87 |
| A2 | 200 | 359 | 8.8e-72 | 3.78 |
| A2 | 400 | 505 | 4.8e-103 | 4.41 |
| A2 | 800 | 738 | 5.5e-153 | 8.60 |

The kill line (p >= 0.05 with >= 200 exits) is met **nowhere**. The smallest
chi-square on the grid is 108 on 9 degrees of freedom. The phase contrast
*sharpens* with ensemble size — the max/min hazard ratio runs 2.3 -> 5.9 (A1)
and 3.4 -> 8.6 (A2) from Omega = 50 to 800 — which is the opposite of what a
phase-independent escape would produce. Binned hazard with 95 % Garwood exact
Poisson intervals: `A/fig_hazard.png`.

## B — Do paths that come closer to dissolution pass through it more often? **KILL.**

Six cells, 2.75 million completed switching runs, none hitting the safety cap.

| Omega | median delta, up | median delta, down | up < down? | kill met (down <= up)? |
|---|---|---|---|---|
| 8 | 0.2500 | 0.2500 | no | **yes** |
| 10 | 0.3000 | 0.4000 | yes | no |
| 12 | 0.4167 | 0.4167 | no | **yes** |

**2 of 3 sizes meet the kill condition**, so the kill line is met and the
candidate *'Identity and size, through coupled routes'* is killed on this line.
The kill is carried by **exact ties**, not a reversal: delta lives on a lattice
of step `1/Omega` (0.125, 0.1, 0.0833), the frozen SPEC §6 anticipated ties and
ruled that a tie counts towards the kill. For context only — not the
preregistered statistic — the *mean* delta is lower for up switches at all three
sizes (0.2908/0.2935, 0.3588/0.4208, 0.3917/0.4453), so a weak ordering in the
predicted direction survives that the median cannot resolve at this lattice
spacing. Passage fractions: up exceeds down at every size (0.0762/0.0686,
0.0134/0.0052, 0.0026/0.0009), agreeing in *direction* with PR 6; PR 6's own
numbers are not in this workspace, so the quantitative check against them is
**not** made here. Distributions: `B/fig_delta.png`.

## Planted checks

| part | check | verdict |
|---|---|---|
| A | P1 modulated hazard | **PASS** — p = 4.5e-62, modulation 0.553 vs 0.5, 10.6 % error (bar 20 %) |
| A | P2 constant hazard | **PASS** — 46/50 replicates with p >= 0.05 (bar 45) |
| A | P3 drift at Omega = 1e5 | **FAIL** — 0.2795 (A1), 0.0449 (A2) against a 0.01 bar |
| B | P1 scripted medians | **PASS** — every delta exact |
| B | P2 passage detector | **PASS** — every flag and count exact |
| B | end-to-end rescan | **PASS** — 400 real runs, 0 mismatches |

**P3's failure stands on the record and the Part A gate is not satisfied as
frozen.** It is not a simulator bug. The frozen metric compares states *at equal
times*, so it is dominated by phase diffusion: A1 slips 2.9 % of a period in one
period, which alone displaces it by ~0.2 RMS cycle radii. Measuring distance to
the cycle *as a set* (revision R1, logged) gives 0.0200 (A1) and 0.0074 (A2) —
A2 passes, A1 still fails. Revision R2, logged, shows the drift falling
monotonically with size (A1: 0.197, 0.0155, 0.0043 at Omega = 1e4, 1e5, 1e6;
log-log slope -0.83), confirming convergence to the deterministic cycle, which
is the property P3 exists to test. The reading: **a 1 % bar at Omega = 1e5 is
below A1's own fluctuation floor there** (~2 % of the RMS cycle radius); A1
would need Omega ~ 4e5. Whether that disqualifies Part A's results is Glenn's
call, not this report's.

## Location

Local only, on this machine:
`C:\Users\gomni\.claude-science\orgs\507f6842-5f31-4700-810b-ef2f8851a6d3\workspaces\546fe95b-6295-4b36-92c3-038b033f2b5f\PHYS2-science-2026-11-01`
No GitHub credential is configured in this workspace, so nothing was pushed to
`gomni1/ClaudeCloud1`, no branch `grammar-science` was created and no pull
request opened. The repository was not touched.
