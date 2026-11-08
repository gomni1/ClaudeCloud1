# ROUTES TEST — SPEC (preregistration)

**Candidate under test.** *'Identity and size, through coupled routes — tested
on the whole distribution'.*

**Claim.** Switching paths that come closer to the dissolution route pass
through it more often. In this example, **up switches come closer to
dissolution than down switches**.

**Status.** This document is frozen. Its SHA-256 is recorded in `RESULTS.md`
before any production run. After the freeze no target, grid, threshold or
criterion in this document changes. A revision is a new claim, logged in
`RESULTS.md`; every failure stays on the record; bug fixes are logged as bug
fixes.

---

## 1. Standing of the model

The Markov chain used here is an **effective-register summary of step
processes**: its states are register counts and its transitions are summary
rates, not the step processes themselves.

## 2. Why the runs are fresh

The candidate was formulated **after** its predecessor's medians tied and
**after** its means had been seen to favour it. Any statistic computed on those
same runs would therefore be tested on the data that suggested it. This test
uses **fresh runs only**: a seed base disjoint from all of
`PHYS2-science-2026-11-01` (§4), and no run, delta, count or seed from that work
enters here. The simulator is reused — `sim_routes.py` is a verbatim copy of
`PHYS2-science-2026-11-01/B/sim_b.py`, SHA-256
`7d975c5fc0dc65231c4dc7f174805b11484a08d402d5d198aba1a5123f9c6e17`, with an
attribution header prepended and the body unmodified — but none of its data is.

## 3. Model

Open level of the Contact/Void grammar. Roles `C`, `V`, `L`, `P`.

- Contact–Void count `x = C/(C+V)`; on a zero denominator `x = 0`.
- Threshold rates with `m = 2`, `kr = kc = 2`, so
  `F_kr(x) = F_kc(x) = Pr[Bin(2,x) >= 2] = x^2`.
- Constants `(k1,k2,k3,k5,k6,k7,k8,k9,k10,k11,k12) = (2,9,47,1,1,1,1,1,1,13,0.5)`.
- Stable balances `(C,V,L,P) = (1,2,1,0.5)` and `(1,4,1,0.5)`.
- `D`, dissolution, is the set `nC = nL = 0`.
- **Simulation:** exact Gillespie direct method in the Kurtz form, every
  propensity `Omega * r(n/Omega)`. No tau-leaping, no time discretisation.
- A switching run starts at one stable balance and ends on reaching the other:
  `|nV/Omega - targetV| < 0.25` with `nC/Omega`, `nL/Omega`, `nP/Omega` within
  `0.25` of `1`, `1`, `0.5`; `targetV = 4` for up, `2` for down.
- Per run: **direction** (up = 2 -> 4, down = 4 -> 2); whether **D was visited**
  before the target was reached; and
  **`delta` = min over the path of `(nC + nL)/Omega`**, start state included.
- Safety cap `10^7` reactions per run; a run reaching it is discarded from all
  statistics and counted separately.

`delta` lies on the lattice `k/Omega`. Raw `delta` arrays are stored losslessly
as the integer levels `k` together with `Omega`, compressed
(`evidence_routes.npz`).

## 4. Grid, budget and seeds

- `Omega` in `{8, 10, 12, 16}`; direction in `{up, down}`; 8 cells.
- Per cell: generation stops as soon as **either** at least **3000 switching
  runs that did not visit D** have completed, **or** **5 CPU-minutes** are
  spent — whichever comes first. Runs are generated in blocks of 100 and every
  completed run of every block is kept, so the non-passing count may slightly
  exceed 3000; this is unbiased because runs are i.i.d. Whether the CPU budget
  bound is recorded per cell.
- **Seed base `5000000`**, cell seed `5000000 + 1000*d + s` with `d` the index
  of the direction in `[up, down]` and `s` the index of the size in
  `[8, 10, 12, 16]`. This base is disjoint from every seed used in
  `PHYS2-science-2026-11-01` (which used 1, 101, 202, 303, 777+, 4242, 9000+,
  20000+ and 31000+).
- CPU time is measured by `time.process_time()` inside each cell's own process.

## 5. Analysis set

The test set at each size is the runs that **did not visit D**, for each
direction. This follows the sampling rule of §4 and matches the predecessor:
a run that visited D has `delta = 0` identically, so including those runs would
compare passage rates rather than closeness of approach. Passage fractions (§7)
are computed from **all** completed runs.

## 6. Statistic (preregistered)

At each size, a **one-sided Mann–Whitney U test**, alternative *"up deltas are
smaller than down deltas"*, ties handled by **mid-ranks with the tie
correction**, **asymptotic** p-value:
`scipy.stats.mannwhitneyu(up, down, alternative='less', method='asymptotic')`.

The **reversal test** is the same call with `alternative='greater'`.

**Effect size.** The rank-biserial correlation
`r = 1 - 2*U1/(n_up*n_down)`, with `U1` the Mann–Whitney statistic of the up
sample as returned by the call above; `r > 0` means up deltas are stochastically
smaller. Its **bootstrap 95 % interval** is the percentile interval over **2000**
replicates, each resampling both directions independently with replacement at
their observed sizes. Because `delta` is lattice-valued, resampling is performed
as a multinomial draw on each direction's level histogram, which is exactly
i.i.d. resampling of the raw values.

## 7. Verdict rules

- **Kill** if **either**: `p >= 0.05` at **2 or more** of the 4 sizes; **or**
  the opposite one-sided test (up larger than down) gives `p < 0.05` at **any**
  size.
- **Holds** if `p < 0.05` at **3 or more** sizes **and** there is no reversal.
- **Otherwise: underdetermined.**

Also reported, per size: `n` per direction; the rank-biserial effect size with
its bootstrap 95 % interval; mean and median `delta` per direction; and passage
fractions per direction.

## 8. Planted checks (all must pass before results count)

- **P1.** Two synthetic lattice-valued samples on step `1/8`, with a known small
  shift: `up ~ Binomial(8, 0.35)/8`, `down ~ Binomial(8, 0.38)/8`, `n = 3000`
  each. The test of §6 must give `p < 0.05` in at least 90 % (>= 45) of 50
  replicates.
- **P2.** Two identical lattice-valued distributions on step `1/8` with heavy
  ties: both `~ Binomial(8, 0.35)/8`, `n = 3000` each. The test must give
  `p >= 0.05` in at least 90 % (>= 45) of 50 replicates.
- **P3.** On **200 real runs** drawn with the fresh seed base, `delta` and the
  passage flag are recomputed from the stored path and compared with the values
  produced inside the simulation loop: **zero mismatches** required.

## 9. Observational register

Read as analogies only, and only here: the two balances are the sort of thing
one would call *states of a two-level system*, a switch between them the sort of
thing one would call a *transition*, and `D` the sort of thing one would call a
*vacuum* the transition may or may not pass through. The candidate's claim is
that the two routes are *coupled* — that approach and passage are the same
tendency seen twice. No claim about any named particle is made or implied
anywhere in this document.

## 10. Deliverables

`SPEC.md` (this file, frozen), `sim_routes.py`, `driver_routes.py`,
`run_routes.py`, `planted_routes.py`, `analyse_routes.py`, `RESULTS.md` with the
verdict table, compressed evidence (`evidence_routes.npz`,
`evidence_routes.json.gz`), `README.md` and `REPORT.md`.
