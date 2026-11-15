# PART B — SPEC (preregistration)

**Question.** Do switching paths that come closer to dissolution pass through it
more often?

**Status.** This document is frozen. Its SHA-256 is recorded in `RESULTS.md`
before any simulation code for this part runs. After the freeze no target, grid,
threshold or criterion in this document changes. Any revision is a new claim,
logged separately in `RESULTS.md`; every failure stays on the record; bug fixes
are logged as bug fixes.

---

## 1. Standing of the model

The Markov chain used here is an **effective-register summary of step
processes**: its states are register counts and its transitions are summary
rates, not the step processes themselves.

## 2. Grammar and model

Roles `C`, `V`, `L`, `P`; transitions and rate laws as in the shared grammar,
with `F_j(x) = Pr[Bin(m, x) >= j]` and rate order
`(k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12)`.

- **Open level** (rules 9 and 12 present).
- Contact-Void count: `x = C/(C+V)`; on a zero denominator `x = 0`.
- `m = 2`, `kr = kc = 2`, so `F_kr(x) = F_kc(x) = x^2`.
- Constants `(2, 9, 47, 1, 1, 1, 1, 1, 1, 13, 0.5)`.

Deterministic balances, verified numerically from these constants
(`B/fixed_points.py`): `(C,V,L,P) = (1,2,1,0.5)` stable, maximum real part of
the Jacobian spectrum `-0.1514`; `(1,3,1,0.5)` unstable, `+0.2953`;
`(1,4,1,0.5)` stable, `-0.1303`. Residuals at all three are below `1e-15`.

`D`, **dissolution**, is the set `nC = nL = 0`.

## 3. Simulation method

Exact stochastic simulation by **Gillespie's direct method in the Kurtz form**:
each propensity is `Omega * r(n/Omega)`. In integer counts the propensities are
`k1*nC, k2*nC, k3*nV*x^2, k5*nL, k6*nL, k7*nC, k8*nP, k9*nP, k10*nV,
k11*nC*x^2, Omega*k12`. No tau-leaping, no time discretisation. The inner loop
is compiled with `numba` (`B/sim_b.py`).

## 4. Runs

- `Omega` in `{8, 10, 12}`.
- Start states are the two stable balances scaled by `Omega` and rounded; for
  these balances and these sizes the scaling is exactly integral
  (e.g. `Omega = 8`: `(8, 16, 8, 4)` and `(8, 32, 8, 4)`).
- A run ends when the **other** balance is reached:
  `|nV/Omega - targetV| < 0.25` together with `|nC/Omega - 1| < 0.25`,
  `|nL/Omega - 1| < 0.25` and `|nP/Omega - 0.5| < 0.25`, with
  `targetV = 4` for an up switch and `2` for a down switch.
- **Direction**: up = 2 -> 4, down = 4 -> 2.
- Per direction and size: **at least 2000 switching runs, or 3 CPU-minutes**,
  whichever is reached later for the run count and earlier for the clock — i.e.
  runs are generated until 2000 runs have completed *and* at least that; the
  budget stops generation at 3 CPU-minutes only if 2000 runs are already done.
  If 2000 runs are not complete at 3 CPU-minutes, generation continues until
  2000 runs are complete, and the overrun is reported.
- **Safety cap**: `10^7` reactions per run. A run reaching the cap without
  reaching the target is discarded from all statistics and counted separately;
  the count is reported.

## 5. Per-run record

For each run: its direction; whether it **visited D** (`nC = nL = 0`) at any
point before the target was reached; and its **closest approach to
dissolution**, `delta = min over the path of (nC + nL)/Omega`. The start state
is included in the path. A run that visited D necessarily has `delta = 0`.

## 6. Claim (the kill line of the candidate 'Identity and size, through coupled routes')

PR 6 found that, relative to a race between independent routes, up switches pass
through dissolution more often than predicted and down switches less often. The
candidate reads this as route coupling: **up-switch paths come closer to
dissolution**.

- **Prediction:** among switching runs that did **not** visit `D`, the median
  `delta` of up switches is **below** that of down switches, **at each size**.
- **Kill:** at **2 or more of the 3 sizes**, the median `delta` of non-passing
  **down** switches is **less than or equal to** that of up switches.
- Medians are ordinary sample medians (`numpy.median`, linear interpolation)
  over the non-passing runs of that direction and size. `delta` is a multiple of
  `1/Omega`, so exact ties are possible; by the wording above an exact tie
  counts towards the kill.
- **Also reported:** passage fractions by direction and size, checked against
  PR 6; and the `delta` distributions.

## 7. Planted checks (all must pass before results count)

- **P1.** From a scripted path set with known `delta` values, the medians are
  recovered **exactly**.
- **P2.** The passage detector, on scripted paths, reports **exact** counts.
- Both are run against the same compiled scanning rule that the simulator uses,
  and in addition an **end-to-end consistency check** is run: for a sample of
  real simulated runs the full `(nC, nL)` path is recorded and the streaming
  `delta` and passage flags produced inside the simulation loop are required to
  equal those obtained by rescanning the recorded path.

## 8. Observational register

Read as analogies only, and only here: the two balances are the sort of thing
one would call *states of a two-level system*, a switch between them the sort of
thing one would call a *transition*, and `D` the sort of thing one would call a
*vacuum* that the transition may or may not pass through. Whether the two routes
are *coupled* is the question of §6. No claim about any named particle is made
or implied anywhere in this part.

## 9. Deliverables

`SPEC.md` (this file, frozen), `fixed_points.py`, `sim_b.py`, `driver_b.py`,
`planted_b.py`, `run_b.py`, `analyse_b.py`, `RESULTS.md` with a verdict table,
and compressed evidence (`evidence_B.json.gz`).
