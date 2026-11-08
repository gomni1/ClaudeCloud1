# PHYS2 — 'Identity and size, through coupled routes', tested on the whole distribution
**1 November 2026 · fresh runs, seed base 5000000 · SPEC frozen before production ·
`f86996fd1078978260c5460c2cf0723c…`**

## Verdict: **KILL**

One-sided Mann–Whitney U on the non-passing runs, alternative "up deltas are
smaller than down deltas", mid-ranks with tie correction, asymptotic p.

| Omega | n up / n down | p (up < down) | p (up > down) | rank-biserial r | bootstrap 95 % CI |
|---|---|---|---|---|---|
| 8 | 3056 / 3064 | 9.965e-01 | **3.507e-03** | **-0.0382** | [-0.0652, -0.0101] |
| 10 | 3054 / 3083 | 1.989e-30 | 1.000 | +0.1653 | [+0.1349, +0.1926] |
| 12 | 3092 / 3092 | 1.417e-26 | 1.000 | +0.1535 | [+0.1244, +0.1814] |
| 16 | 3000 / 3000 | 5.172e-71 | 1.000 | +0.2629 | [+0.2346, +0.2901] |

The claim's direction is significant at **3 of 4** sizes, and the effect grows
with size (r = +0.165, +0.154, +0.263). But at **Omega = 8 the ordering reverses
significantly**: p = 3.51e-03 against the claim, with a rank-biserial interval
lying entirely below zero. SPEC §7 requires "no reversal" for the candidate to
hold and kills on a reversal at **any** size, so the candidate is killed — on
that clause alone. The other kill clause (p >= 0.05 at 2 or more sizes) is not
met; only Omega = 8 fails in the claimed direction.

A selection effect runs the right way to produce the reversal and is worth
stating: the preregistered analysis set drops runs that visited D, and at
Omega = 8 that removes 7.39 % of up runs against 7.15 % of down runs — exactly
the closest-approaching ones — trimming more of the up sample's low tail. At
Omega = 16 nothing is removed and the effect is largest. That is a property of
the analysis set the SPEC fixed before the runs, not a defect in it. A candidate
stated on the unconditioned distribution, or treating approach and passage
jointly, is **a new claim** and must not be read off these runs.

**The fresh-runs rule earned its keep.** The previous night's Part B had mean
delta at Omega = 8 of up 0.2908 against down 0.2935 — the claimed direction.
These independent runs give 0.2903 against 0.2881, the opposite, significantly.
The Omega = 8 signal that helped motivate the candidate does not survive
resampling. Those earlier figures are quoted for contrast only; no datum from
them entered any statistic here.

Supporting numbers — mean / median delta and passage fraction, up vs down:
Omega = 8, 0.2903/0.2881, 0.2500/0.2500, 0.0739/0.0715; Omega = 10,
0.3563/0.4224, 0.3000/0.4000, 0.0148/0.0055; Omega = 12, 0.3902/0.4498,
0.4167/0.4167, 0.0026/0.0026; Omega = 16, 0.4756/0.5660, 0.4375/0.5000,
0.0000/0.0000. Passage favours up wherever passage occurs.

## Planted checks — all pass

| check | verdict | detail |
|---|---|---|
| P1 known small shift on the 1/8 lattice | **PASS** | detected in 50/50 replicates (bar 45), median p = 3.7e-12 |
| P2 identical distributions, heavy ties | **PASS** | p >= 0.05 in 45/50 replicates (bar 45), median p = 0.44 |
| P3 recompute from stored paths | **PASS** | 200 real runs rescanned, 0 delta and 0 passage-flag mismatches |

P2 landed exactly on its bar; its median p of 0.44 is consistent with a
correctly calibrated tie-corrected test.

## CPU used

Production **21.2 CPU-seconds** over 8 cells (no cell reached its 5-CPU-minute
budget; none of the 25,000 runs hit the 10^7-reaction safety cap). Planted
checks 3.1 CPU-seconds. Total **24 CPU-seconds**.

## Location

`C:\Users\gomni\.claude-science\orgs\507f6842-5f31-4700-810b-ef2f8851a6d3\workspaces\546fe95b-6295-4b36-92c3-038b033f2b5f\PHYS2-science-2026-11-01-routes`
