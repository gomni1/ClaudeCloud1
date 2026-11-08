# ROUTES TEST — RESULTS

## Freeze record

`SPEC.md` was written and frozen before any production run of this test.

- `SPEC.md` SHA-256: `f86996fd1078978260c5460c2cf0723ca8ab748cf6f2db474b1e4448dff927af`
- frozen at: 2026-11-01T01:15:42
- seed base: `5000000`, disjoint from every seed used in
  `PHYS2-science-2026-11-01`
- simulator: `sim_routes.py`, a verbatim copy of
  `PHYS2-science-2026-11-01/B/sim_b.py` (source SHA-256
  `7d975c5fc0dc65231c4dc7f174805b11484a08d402d5d198aba1a5123f9c6e17`) with an
  attribution header prepended and the body unmodified

**No run, delta, count or seed from the previous night's Part B enters this
test.** Nothing was run against the model under this SPEC before the freeze.

Change log after the freeze (revisions, failures, bug fixes) is kept in §5.
Nothing is removed from it.

## 2. Planted checks (SPEC §8)

| check | verdict | detail |
|---|---|---|
| P1 known small shift, 1/8 lattice | **PASS** | detected in 50/50 replicates (bar 45); median p = 3.73e-12 |
| P2 identical distributions, heavy ties | **PASS** | p >= 0.05 in 45/50 replicates (bar 45); median p = 0.440 |
| P3 recompute from stored paths | **PASS** | 200 real runs rescanned; 0 delta and 0 passage-flag mismatches |

All planted checks pass, so the gate of SPEC §8 is satisfied and the results
below count. P2 landed exactly on its bar (45/50); the median p of 0.44 is
consistent with a correctly calibrated tie-corrected test, and the shortfall
from the nominal 47.5 is within binomial noise.

## 3. Runs (SPEC §4)

No cell reached its 5-CPU-minute budget and no run reached the 10^7-reaction
safety cap, so nothing was discarded. Total production cost **21.2 CPU-seconds**.

| Omega | up runs | up non-passing | down runs | down non-passing | CPU s | seeds (up, down) |
|---|---|---|---|---|---|---|
| 8 | 3300 | 3056 | 3300 | 3064 | 4.8 | 5000000, 5001000 |
| 10 | 3100 | 3054 | 3100 | 3083 | 3.9 | 5000001, 5001001 |
| 12 | 3100 | 3092 | 3100 | 3092 | 5.7 | 5000002, 5001002 |
| 16 | 3000 | 3000 | 3000 | 3000 | 6.8 | 5000003, 5001003 |

## 4. Verdict: **KILL**

Statistic as frozen: one-sided Mann-Whitney U, alternative "up deltas are
smaller than down deltas", mid-ranks with tie correction, asymptotic p, on the
runs that did not visit D.

| Omega | n up | n down | p (up < down) | p (up > down) | rank-biserial r | bootstrap 95 % CI | outcome |
|---|---|---|---|---|---|---|---|
| 8 | 3056 | 3064 | 9.965e-01 | 3.507e-03 | -0.0382 | [-0.0652, -0.0101] | **reversed** |
| 10 | 3054 | 3083 | 1.989e-30 | 1.000e+00 | +0.1653 | [+0.1349, +0.1926] | claim direction |
| 12 | 3092 | 3092 | 1.417e-26 | 1.000e+00 | +0.1535 | [+0.1244, +0.1814] | claim direction |
| 16 | 3000 | 3000 | 5.172e-71 | 1.000e+00 | +0.2629 | [+0.2346, +0.2901] | claim direction |

- `p < 0.05` in the claimed direction at **3 of 4** sizes (10, 12, 16).
- The opposite one-sided test gives **p = 3.51e-03 < 0.05 at Omega = 8** — a
  **reversal**.

SPEC §7 makes "holds" require `p < 0.05` at 3 or more sizes **and no reversal**.
The first condition is met and the second is not. The kill clause *"the opposite
one-sided test gives p < 0.05 at any size"* **is** met. The other kill clause
(`p >= 0.05` at 2 or more sizes) is **not** met — only Omega = 8 is
non-significant in the claimed direction.

**The candidate 'Identity and size, through coupled routes — tested on the whole
distribution' is killed, on the reversal clause alone.**

At Omega = 8 the rank-biserial is `-0.0382` with a bootstrap interval
`[-0.0652, -0.0101]` lying entirely below zero: up switches there are
stochastically **further** from dissolution than down switches, which is the
contradictory of the claim rather than merely a failure to support it.

## 5. Also reported (SPEC §7)

| Omega | mean delta up | mean delta down | median up | median down | passage up | passage down |
|---|---|---|---|---|---|---|
| 8 | 0.2903 | 0.2881 | 0.2500 | 0.2500 | 0.0739 | 0.0715 |
| 10 | 0.3563 | 0.4224 | 0.3000 | 0.4000 | 0.0148 | 0.0055 |
| 12 | 0.3902 | 0.4498 | 0.4167 | 0.4167 | 0.0026 | 0.0026 |
| 16 | 0.4756 | 0.5660 | 0.4375 | 0.5000 | 0.0000 | 0.0000 |

At Omega = 16 no run in either direction visited D, so both passage fractions
are exactly zero.

## 6. Reading the result

Three observations, none of which alters the verdict.

1. **The effect is real and large at Omega >= 10, and it grows**: r = +0.165,
   +0.154, +0.263 at Omega = 10, 12, 16, with p down to 5e-71. Whatever is
   killed here, it is not the idea that up switches approach dissolution more
   closely at larger sizes.
2. **The reversal at Omega = 8 is small but solidly outside its interval.** A
   candidate phrased as a universal ordering across sizes cannot absorb a
   significant reversal at one of them, and the frozen rule says so.
3. **A selection effect runs the right way to produce it.** The analysis set
   excludes runs that visited D, and at Omega = 8 that exclusion is large and
   direction-dependent: 7.39 % of up runs versus 7.15 % of down runs are
   removed, and the removed runs are exactly those with the closest approach.
   Conditioning therefore trims more of the up sample's low tail than the down
   sample's, which pushes the conditional up distribution upward. At Omega = 16
   nothing is removed at all and the effect is largest. This is a property of
   the preregistered analysis set, not a defect in it, and the SPEC fixed that
   set before the runs. A candidate stated on the unconditioned distribution,
   or one that treats passage and approach jointly, would be **a new claim** —
   not this one, and not to be read off these runs.

**On the fresh-runs rule.** The rule earned its keep. The previous night's Part
B gave mean delta at Omega = 8 as up 0.2908 against down 0.2935 — the claimed
direction. These independent runs give up 0.2903 against down 0.2881 — the
opposite, and significantly so under the whole-distribution test. The Omega = 8
signal that helped motivate this candidate does not survive resampling. Those
earlier numbers are quoted here for contrast only; no datum from them entered
any statistic in this document.

## 7. Change log

1. No planted check failed. No bug fix was required after the freeze.
2. No target, grid, threshold or criterion was altered after the freeze.
3. The histogram form of U1 used for the bootstrap was checked against
   `scipy.stats.mannwhitneyu` at every size and agreed exactly (to 1e-6), so the
   multinomial resampling is i.i.d. resampling of the raw values.

## 8. Evidence

- `evidence_routes.npz` — the raw delta arrays for all 8 cells, stored
  losslessly as integer lattice levels `k` (delta = k/Omega) with the passage
  flags, compressed.
- `evidence_routes.json.gz` — per-cell summaries, the per-size test results and
  the planted-check records.
- `fig_ecdf.png` — empirical distribution of delta by direction at each size.
