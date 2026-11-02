# PART A — SPEC (preregistration)

**Question.** Does a clock's escape hazard depend on its phase?

**Status.** This document is frozen. Its SHA-256 is recorded in `RESULTS.md`
before any production simulation code runs. After the freeze no target, grid,
threshold or criterion in this document changes. Any revision is a new claim,
logged separately in `RESULTS.md`; every failure stays on the record; bug fixes
are logged as bug fixes.

---

## 1. Standing of the model

The Markov chain used here is an **effective-register summary of step
processes**: its states are register counts and its transitions are summary
rates, not the step processes themselves.

## 2. Grammar

Roles `C`, `V`, `L`, `P`. With `x` the contact fraction and
`F_j(x) = Pr[Bin(m, x) >= j]`, the transitions and deterministic rate laws are

| # | transition | rate |
|---|---|---|
| 1 | C -> L | `k1*C` |
| 2 | C -> V | `k2*C` |
| 3 | V + C -> 2C | `k3*V*F_kr(x)` |
| 5 | L -> V | `k5*L` |
| 6 | L -> C | `k6*L` |
| 7 | C -> P | `k7*C` |
| 8 | P -> V | `k8*P` |
| 9 | P -> () | `k9*P` (open level only) |
| 10 | V -> C | `k10*V` |
| 11 | 2C -> V + C | `k11*C*F_kc(x)` |
| 12 | () -> V | `k12` (open level only) |

Rate vectors are given in the order
`(k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12)`.
In Part A, `x = C/(C+V+L+P)` (all-neighbours count).

## 3. Simulation method

Exact stochastic simulation by **Gillespie's direct method in the Kurtz form**:
each propensity is `Omega * r(n/Omega)` with `r` the deterministic rate law in
concentrations and `n` the integer counts. No tau-leaping and no time
discretisation are used. The inner loop is compiled with `numba`
(`A/sim_a.py`). On the closed level rules 9 and 12 are absent, so
`N = nC+nV+nL+nP` is conserved exactly and only `N = round(Omega*total)`
matters. Concentrations are `n/Omega`.

## 4. Models

**A1 — closed level, draw 19387.** `m = 8`, `kr = 2`, `kc = 4`,
`total = 12.872923044730259`, rates
`(1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678,
0.17271135353305755, 0.10361090436515946, 6.769536427560776)`.
Deterministic period 6.3524.

**A2 — open level, draw 33538.** `m = 6`, `kr = 2`, `kc = 3`, rates
`(0.16060731572267742, 3.7768995051238523, 8.455266356236777, 0.15036717833913482,
0.12593008757363863, 1.8070659981769923, 0.15004519519714457, 0.3071328391558332,
0.21585689687505635, 0.4453036700615455, 0.6705277209656662)`.
Deterministic period 4.8439.

Both models are analysed. Claim S4' below is evaluated **separately for A1 and
A2**; each model receives its own verdict and neither overrides the other.

## 5. The deterministic cycle (frozen reference)

The deterministic limit is integrated with `DOP853` (`rtol=1e-12`, `atol=1e-14`)
from a transient of 4000 time units; the period is taken from upcrossings of the
mid-level of `C` through a Poincare section, and the cycle is sampled at 4096
points uniformly in arc-time over one period (`A/models_a.py`).

The resulting cycle files are frozen and referenced by hash:

| file | SHA-256 |
|---|---|
| `A/cycle_A1.npz` | `45abcbb20e5e5a50ddb683a058d5998c000697ae2269c207095b1859d7b67920` |
| `A/cycle_A2.npz` | `6cc92294b9da32e8bc43e99a54f9fda022789e5373396b85d69045eaa62c5196` |

Recovered periods: A1 `6.352409101`, A2 `4.843916612`; both agree with the
stated periods to a relative error below `4e-6`, and the period jitter across
successive Poincare crossings is below `1e-13`.

Per-coordinate standard deviations on the cycle (the scaling used in §6):

| model | sigma_C | sigma_V | sigma_L | sigma_P |
|---|---|---|---|---|
| A1 | 0.275054 | 0.790408 | 0.265127 | 0.340132 |
| A2 | 0.349630 | 0.626259 | 0.039779 | 0.432083 |

## 6. Definitions (tick-free)

1. Each coordinate is scaled by its standard deviation on the deterministic
   cycle (table above).
2. `d(t)` is the minimum scaled Euclidean distance from the state, taken as
   concentrations `n/Omega`, to the deterministic cycle. Because the state is
   piecewise constant between reactions, evaluating `d` at every reaction event
   is exact. The nearest cycle point is found by a coarse scan of stride 16 over
   the 4096 samples followed by a local refinement of +/- 16 samples.
3. The **phase** of a state is the arc-time fraction in `[0, 1)` of its nearest
   cycle point.
4. An **exit** occurs when `d > R`, after the trajectory has been inside
   `d < R/2`. Equivalently: the chain is *armed* whenever it attains `d < R/2`,
   and an exit is recorded, and disarms the chain, the first time `d > R` while
   armed.
5. The **exit phase** is the phase at the last moment before the exit at which
   `d < R/2`.
6. **Occupancy** is the time spent in each of 10 equal phase bins
   (`bin = floor(phase*10)`) while `d < R`. Occupancy is accumulated over the
   dwell time in each state, so it too is exact. The time-while-armed is also
   recorded, as a secondary diagnostic only; it enters no verdict.
7. **Burn-in.** The first 20 deterministic periods of each run are discarded:
   no occupancy and no exits are accumulated before `t = 20*T`. Burn-in is
   excluded from the CPU budget.
8. The start state is the integer rounding of the cycle point at phase 0; on
   the closed level the rounding residue is absorbed into `P` so that
   `N = round(Omega*total)` holds exactly.

## 7. Grid and budget

`Omega` in `{50, 100, 200, 400, 800}`. At each size, recording stops at **2000
exits or 2 CPU-minutes**, whichever comes first. Cells are independent and may
be run in parallel processes; the 2-CPU-minute budget is per cell and is
measured by `time.process_time()` inside that cell's process. Each cell is
seeded independently and its seed is recorded.

## 8. Claim S4' (preregistered)

> At the size with the most exits (at least 200), the exits per bin differ from
> those expected from occupancy (chi-square, 9 degrees of freedom, p < 0.05).

- Expected counts are `E_i = n_exits * occ_i / sum(occ)`; the statistic is
  `sum_i (O_i - E_i)^2 / E_i` on 9 degrees of freedom.
- **Pass (S4' supported):** `p < 0.05`.
- **Kill (escape hazard does not depend on phase, for this clock):**
  `p >= 0.05` with at least 200 exits.
- **Underdetermined:** fewer than 200 exits at every size.
- The binned hazard — exits per unit occupancy — is reported with 95 %
  intervals (Garwood exact Poisson intervals on the counts, divided by the bin
  occupancy).

## 9. Pilot (run before the freeze, disclosed)

A pilot of at most 5 CPU-minutes at `Omega = 400`, run before this document was
frozen, selects `R` from `{0.75, 1.0, 1.5, 2.0}`: **the smallest value giving at
least 1 exit per 10 periods**, i.e. an exit rate of at least `0.1` per
deterministic period. The pilot is run separately for A1 and A2 and its full
table is disclosed in `RESULTS.md`. **Pilot data are not used in the test** —
the production runs start from fresh seeds and accumulate their own statistics.

Selected radii, written in before the freeze:

| model | R |
|---|---|
| A1 | 0.75 |
| A2 | 0.75 |

Note on the rule: the exit rate falls monotonically in `R`, so "the smallest
value giving at least 1 exit per 10 periods" is satisfied by the smallest
candidate whenever that candidate qualifies, and it does here for both models.
The rule is applied exactly as written; this note records that it was not
binding above the floor of the candidate set.

## 10. Planted checks (all must pass before results count)

- **P1.** A synthetic point process with hazard proportional to
  `1 + 0.5*cos(2*pi*phi)` and uniform occupancy: the chi-square test gives
  `p < 0.05`, and the modulation amplitude recovered by a least-squares fit of
  `a*(1 + b*cos(2*pi*phi - c))` to the binned hazard satisfies
  `|b_hat - 0.5|/0.5 <= 0.20`.
- **P2.** Constant hazard: `p >= 0.05` in at least 90 % (>= 45) of 50 synthetic
  replicates, each with the same number of exits as P1.
- **P3.** At `Omega = 1e5`, the drift of one period from the deterministic cycle
  is under 1 %. Metric: starting on the cycle at phase 0, after one
  deterministic period `T` the Euclidean distance in *unscaled* concentrations
  between the stochastic state and the deterministic state at the same time,
  divided by the root-mean-square cycle radius
  `sqrt(sigma_C^2+sigma_V^2+sigma_L^2+sigma_P^2)`, is below 0.01. Reported as
  the median over 11 independent seeds, for both models.

## 11. Observational register

Read as analogies only, and only here: a limit cycle of this kind is the sort of
object one would call a *clock*, its escape events the sort of thing one would
call a *decay*, and the question of §8 is whether that decay is *phase-locked*
to the clock's internal angle rather than memoryless in it. No claim about any
named particle is made or implied anywhere in this part.

## 12. Deliverables

`SPEC.md` (this file, frozen), `models_a.py`, `sim_a.py`, `driver_a.py`,
`pilot_a.py`, `planted_a.py`, `run_a.py`, `analyse_a.py`, `RESULTS.md` with a
verdict table, and compressed evidence (`evidence_A.json.gz`).
