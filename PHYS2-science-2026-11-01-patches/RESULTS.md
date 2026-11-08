# COUPLED CLOCKS ON A GRAPH — RESULTS

## Freeze record

`SPEC.md` was written and frozen before any production run.

- `SPEC.md` SHA-256: `3004288a8f61bc3e89cb0c440ddf1757aa530e0ed48221ff835e2de0124c0e34`
- frozen at: 2026-11-01T01:42:11
- `deterministic.npz` SHA-256: `016e6361f9084d01c771543b028b90a783a4ef27a8705518e20f3201fcfcedc5`
- `graphs.npz` SHA-256: `b9a95085dbf06ddcd52641e11fe9bd44fe06d35af8b8e4c6d226c9a8b15ecadd`
- seed base: `7000000`
- declared leap step: `dt = 0.01`; declared size: `N = 2000` for all classes

Run before the freeze and disclosed in SPEC §2.1, §3 and §8.1: the recomputation
of the deterministic facts, the combinatorial graph construction and its
metrics, the CPU projection, and the leap-step calibration against exact
Gillespie. H1–H3 and P1–P2 are run after the freeze with declared seeds and
their post-freeze values are the ones that count.

Change log after the freeze is kept in §6. Nothing is removed from it.

## 2. Graphs, measured (SPEC §3)

| class | N | mean degree | degree range | clustering | diameter | growth exponent d_g |
|---|---|---|---|---|---|---|
| S | 2000 | 5.994 | 3–27 | 0.5993 | 29 | 2.227 |
| R | 2000 | 8.000 | 8–8 | 0.0039 | 6 | 3.407 |
| C5 | 2000 | 8.000 | 6–11 | 0.5454 | 13 | 2.479 |

`S` has mean degree 5.994, exactly `2(3N-6)/N` for a triangulation, and its
**measured** growth exponent is 2.23 — two-dimensional, as measured and not as
set. `R` is expander-like (clustering 0.004, diameter 6, `d_g` 3.41 fitted over
only 3 radii before the ball saturates). `C5` sits between them.

## 3. Harness (SPEC §6) — all pass

| check | verdict | detail |
|---|---|---|
| H1 sites tick at the right rate | **PASS** | median per-site period 5.1814 at `w=0`, `Omega=800`, against the exact-SSA reference 5.2010; error 0.38 % (bar 5 %) |
| H2 leap against exact Gillespie | **PASS** | `Omega=200`: period 4.4819 vs 4.5320 (1.11 %), CV 0.18 %. `Omega=800`: period 0.13 %, CV 3.04 % |
| H3 total winding on S | **PASS** | 0 in every one of 5400 frames; and 0 in every frame of all 12 production runs on `S` |
| P1 planted windings | **PASS** | tetrahedron vortex gives exactly `(+1,0,0,-1)`; constant and small-gap fields on `S` give 0 everywhere |
| P2 independent uniform phases | **PASS** | defect density 0.2498 against the 1/4 target; longest track 1 frame (bar 636) |

**The exact-SSA period of an isolated site is far from the deterministic
period.** At `Omega = 800` it is 5.2010 against a deterministic 6.3524, with a
coefficient of variation of 0.4556; at `Omega = 200` it is 4.5320 with CV 0.5291.
These ensembles are small enough that the clock is strongly noise-shortened.
H1 compares like with like, as the SPEC requires.

## 4. Main part, class S (SPEC §7)

| Omega | w | rep | R | defect density | longest track (periods) | tracks >= 5 periods | tracks >= 20 periods | median site amplitude | D3 births / deaths |
|---|---|---|---|---|---|---|---|---|---|
| 200 | 0.05 | 0 | 0.224 | 0.1960 | 0.13 | 0 | 0 | 2.4328 | 1.00 / 1.00 |
| 200 | 0.05 | 1 | 0.225 | 0.1955 | 0.19 | 0 | 0 | 2.4319 | 1.00 / 1.00 |
| 200 | 0.20 | 0 | 0.174 | 0.1311 | 0.19 | 0 | 0 | 1.8988 | 1.00 / 1.00 |
| 200 | 0.20 | 1 | 0.176 | 0.1310 | 0.19 | 0 | 0 | 1.8988 | 1.00 / 1.00 |
| 200 | 0.50 | 0 | 0.171 | 0.0715 | 0.25 | 0 | 0 | 1.5365 | 1.00 / 1.00 |
| 200 | 0.50 | 1 | 0.168 | 0.0716 | 0.28 | 0 | 0 | 1.5360 | 1.00 / 1.00 |
| 800 | 0.05 | 0 | 0.202 | 0.1792 | 0.25 | 0 | 0 | 1.8445 | 1.00 / 1.00 |
| 800 | 0.05 | 1 | 0.203 | 0.1792 | 0.22 | 0 | 0 | 1.8447 | 1.00 / 1.00 |
| 800 | 0.20 | 0 | 0.147 | 0.0943 | 0.25 | 0 | 0 | 1.3053 | 1.00 / 1.00 |
| 800 | 0.20 | 1 | 0.145 | 0.0951 | 0.31 | 0 | 0 | 1.3052 | 1.00 / 1.00 |
| 800 | 0.50 | 0 | 0.196 | 0.0431 | 0.28 | 0 | 0 | 1.0721 | 1.00 / 1.00 |
| 800 | 0.50 | 1 | 0.184 | 0.0433 | 0.38 | 0 | 0 | 1.0697 | 1.00 / 1.00 |

### Verdicts

| claim | verdict | basis |
|---|---|---|
| **E1** sites tick | **PASS** | median site amplitude 1.8445 and 1.8447 at `Omega=800, w=0.05`, against a bar of 0.68619 — 2.7 times the bar |
| **D1** persistent localised integer | **KILL** | the longest track at **any** grid point is 0.38 periods, against a bar of 20 |
| **D2** cores at local zeros | **UNDERDETERMINED** | no track anywhere lasts 5 periods, so the statistic has no support |
| **D3** pair births and deaths are local | criterion met, **but vacuous** | 100 % of births and deaths have an opposite-sign partner within 3 hops and one frame, against an 80 % bar — see below |
| **D4** motion | **not computable** | no track reaches 20 periods, so there is no mean squared displacement to fit |

**D1 is killed, and not because the sites fail to tick.** E1 passes by a factor
of 2.7 and H1 shows the per-site period matches an isolated site's to 0.38 %.
The clocks run; what fails is the coupling's ability to hold a winding together.
Defects are produced in enormous numbers — between 0.9 and 4.2 million tracks
per run — and essentially all of them live less than half a period. The longest
track seen anywhere on `S` is 0.38 periods.

**D3 passes its stated bar but carries no information at these densities.** On
`S` a triangle's hop-3 neighbourhood holds about 329 of the 3996 triangles; at a
defect density near 0.18, searching three frames of it gives roughly 97 expected
opposite-sign defects. A partner is therefore near-certain by chance alone, and
the 100 % figure is what any arrangement would give. This is recorded as a
limitation of the test at this density, not as a revision: the criterion is
applied exactly as frozen.

## 5. Comparison, classes R and C5 (SPEC §9) — report only

| class | w | triangles | R | defect density | longest track (periods) |
|---|---|---|---|---|---|
| R | 0.05 | 73 | 0.203 | 0.1968 | 0.54 |
| R | 0.20 | 73 | 0.130 | 0.1571 | 0.44 |
| C5 | 0.05 | 10123 | 0.203 | 0.1863 | 0.19 |
| C5 | 0.20 | 10123 | 0.148 | 0.0903 | 0.16 |

No class behaves differently in kind. The expander `R` does **not** globally
synchronise, contrary to the disclosed expectation in SPEC §10; `C5` does not
either. Total winding is nonzero on `R` and `C5` (up to 294) exactly as it
should be: they are not closed surfaces, their triangles are 3-cliques with no
coherent orientation, and H3 applies only to `S`.

## 6. Reading the result, and the change log

**What the coupling does.** Raising `w` steadily removes defects — density falls
from 0.196 to 0.072 at `Omega=200` and from 0.179 to 0.043 at `Omega=800` — but
synchrony does **not** rise with it: `R` stays between 0.13 and 0.22 throughout,
against 1/sqrt(N) = 0.022 for independent phases and 1 for a synchronised
ensemble. Over the same range the median site amplitude falls from 1.84 to 1.07
at `Omega=800`. The coupling pulls sites toward the balance and shrinks the
oscillation, which removes windings by flattening the field rather than by
ordering it. On this grammar, coupling through the recruitment count **damps**
rather than synchronises; the disclosed expectation of drifting defects in a
synchronising background is not what this grammar does.

**What this run settles against its predecessor.** The earlier one-unit-per-site
run lost the clock entirely on sparse graphs. Giving every site an ensemble
large enough to tick repairs that — H1 and E1 both pass — and the conclusion
about persistent windings nevertheless stands: no track reaches 20 periods.
The kill is therefore a statement about the coupling, not an artefact of sites
that cannot tick.

**Change log.**
1. No harness or planted check failed. No bug fix was required after the freeze.
2. No target, grid, threshold or criterion was altered after the freeze.
3. D3's vacuity at the observed defect density is recorded above as a
   limitation. The criterion was applied as written and its verdict is reported
   as the SPEC defines it.
4. `N = 2000` was kept for all classes; the CPU projection did not require a
   reduction.

## 7. CPU used, against the cap

| stage | CPU |
|---|---|
| pre-freeze setup (deterministic facts, graphs, caches, projection, leap calibration) | ~32 s |
| harness H1–H3, P1–P2 | 89.4 s |
| production, 16 runs | 1791.0 s |
| **total** | **0.531 CPU-hours of a 4 CPU-hour cap** |

Nothing was stopped at: no run hit a budget, no cell was truncated, and nothing
in the SPEC was left unexecuted.

## 8. Evidence

`evidence_patches.json.gz` — per-run summaries with R and defect count over
time, track statistics, D2–D4 inputs, the harness record and the graph metrics.
`fig_patches.png` — synchrony, defect density and site amplitude.
Frozen inputs: `deterministic.npz`, `graphs.npz`, `topo_cache.npz`.
