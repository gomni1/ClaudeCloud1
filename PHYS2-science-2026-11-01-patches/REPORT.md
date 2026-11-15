# PHYS2 — coupled clocks on a graph: a ticking ensemble at every site
**1 November 2026 · SPEC frozen `3004288a8f61bc3e89cb0c440ddf1757…` · N = 2000, dt = 0.01, seed base 7000000**

## Verdicts

| claim | verdict | basis |
|---|---|---|
| **E1** sites tick | **PASS** | median site amplitude 1.8445, 1.8447 at `Omega=800, w=0.05` against a bar of 0.68619 — 2.7x |
| **D1** persistent localised integer | **KILL** | longest track at any grid point 0.38 periods, bar 20 |
| **D2** cores at local zeros | **UNDERDETERMINED** | no track anywhere lasts 5 periods |
| **D3** births and deaths local | met (100 % vs 80 %), **vacuous** | a hop-3 neighbourhood on S holds ~329 of 3996 triangles; at density 0.18 about 97 opposite-sign defects are expected there by chance |
| **D4** motion | **not computable** | no track reaches 20 periods |

**D1 is killed, and not because the sites fail to tick.** H1 matches the
per-site period to an isolated site's exact-SSA period within 0.38 %, and E1
clears its bar by 2.7x. The clocks run; the coupling cannot hold a winding
together. Between 0.9 and 4.2 million tracks form per run and essentially all
die inside half a period.

## R and defect counts by grid point and class

| class | Omega | w | R | defect density | longest track (periods) |
|---|---|---|---|---|---|
| S | 200 | 0.05 | 0.224 | 0.1960 | 0.13 |
| S | 200 | 0.20 | 0.174 | 0.1311 | 0.19 |
| S | 200 | 0.50 | 0.171 | 0.0715 | 0.25 |
| S | 800 | 0.05 | 0.202 | 0.1792 | 0.25 |
| S | 800 | 0.20 | 0.147 | 0.0943 | 0.25 |
| S | 800 | 0.50 | 0.196 | 0.0431 | 0.28 |
| R | 800 | 0.05 | 0.203 | 0.1968 | 0.54 |
| R | 800 | 0.20 | 0.130 | 0.1571 | 0.44 |
| C5 | 800 | 0.05 | 0.203 | 0.1863 | 0.19 |
| C5 | 800 | 0.20 | 0.148 | 0.0903 | 0.16 |

(Class S shows replicate 0; replicate 1 agrees to within 0.003 in R and 0.001 in
defect density at every grid point.)

**What the coupling does.** Raising `w` removes defects (0.179 -> 0.043 at
`Omega=800`) while synchrony does **not** rise — `R` stays 0.13–0.22 against
0.022 for independent phases and 1 for a synchronised ensemble — and the median
site amplitude falls from 1.84 to 1.07. The coupling pulls sites toward the
balance and flattens the field rather than ordering it. **It damps rather than
synchronises.** The expander `R` does not globally synchronise either, against
the disclosed expectation.

## Harness and planted checks — all pass

H1 median per-site period 5.1814 vs exact-SSA 5.2010 (0.38 %, bar 5 %).
H2 leap vs exact Gillespie: worst error 1.11 % on period, 3.04 % on CV.
H3 total winding on S is 0 in every frame of the harness run and of all 12
production runs. P1 planted windings detected exactly (tetrahedron vortex gives
`(+1,0,0,-1)`). P2 independent phases give defect density 0.2498 against 1/4 with a
longest track of 1 frame.

Worth recording: the exact-SSA period of an isolated site is 5.2010 at
`Omega=800` and 4.5320 at `Omega=200`, against a deterministic 6.3524, with
CV 0.456 and 0.529. These ensembles are small enough that the clock is
strongly noise-shortened; H1 compares like with like.

## CPU used against the cap

Pre-freeze setup ~32 s, harness 89.4 s, production 1791.0 s over 16 runs.
**Total 0.531 CPU-hours of a 4 CPU-hour cap.**

## Anything stopped at

Nothing. No run hit a budget, no cell was truncated, nothing in the SPEC was
left unexecuted, and `N = 2000` was kept for all classes. Nothing was pushed
anywhere.

## Location

`C:\Users\gomni\.claude-science\orgs\507f6842-5f31-4700-810b-ef2f8851a6d3\workspaces\546fe95b-6295-4b36-92c3-038b033f2b5f\PHYS2-science-2026-11-01-patches`
