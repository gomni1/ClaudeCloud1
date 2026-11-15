# PHYS2 — coupled clocks on a graph, 1 November 2026

A ticking ensemble at every site of a graph; sites couple only through the count
each unit reads. Closed level of the grammar, clock draw 19387.

| claim | verdict |
|---|---|
| **E1** sites tick | **PASS** (median amplitude 1.845 vs bar 0.686) |
| **D1** persistent localised integer | **KILL** (longest track anywhere 0.38 periods, bar 20) |
| **D2** cores at local zeros | **UNDERDETERMINED** (no track lasts 5 periods) |
| **D3** pair births and deaths are local | criterion met at 100 %, but **vacuous** at the observed defect density |
| **D4** motion | **not computable** (no track reaches 20 periods) |

**Headline.** Coupling through the recruitment count **damps** the clocks
instead of synchronising them. Raising `w` removes defects (density 0.179 ->
0.043 at `Omega=800`) but does not raise synchrony (`R` stays 0.13–0.22 against
0.022 for independent phases and 1 for a synchronised ensemble); over the same
range the median site amplitude falls from 1.84 to 1.07. Neither the
surface-like class, the expander, nor the small-world ring synchronises — which
contradicts the disclosed expectation for expanders in SPEC §10.

The sites do tick: H1 matches the per-site period to an isolated site's exact
Gillespie period within 0.38 %, and E1 clears its bar by a factor of 2.7. So the
D1 kill is a statement about the coupling, **not** an artefact of sites that
cannot tick — which is what separates this run from the earlier
one-unit-per-site study where the clock vanished outright.

## Preregistration

`SPEC.md` was frozen before any production run; its SHA-256 is in `RESULTS.md`:

- `SPEC.md` — `3004288a8f61bc3e89cb0c440ddf1757aa530e0ed48221ff835e2de0124c0e34`
- seed base `7000000`, declared leap step `dt = 0.01`, declared size `N = 2000`

Disclosed as run before the freeze (SPEC §2.1, §3, §8.1): recomputation of the
deterministic facts, the combinatorial graph construction and its metrics, the
CPU projection, and the leap-step calibration against exact Gillespie.

## Method

Closed level per site, `Omega` units per site, seven within-site transitions;
sites couple only through `x_i = (1-w) c_i + w * (neighbour mean of c_j)`. No
mobility, swap move or rate was added. Tau-leaping at `dt = 0.01` with Poisson
leaps clipped to keep counts non-negative, validated against exact Gillespie
(H2). The Markov chain, its tau-leaping approximation and the graph are
effective-register summaries; the graph is a frozen neighbour relation, the one
approximation named in advance. No coordinates are used anywhere and every
dimension is measured: `d_g` = 2.23 (S), 3.41 (R), 2.48 (C5).

## Layout

```
SPEC.md RESULTS.md README.md REPORT.md
grammar.py          ODE, balance, limit cycle, s_c and s_v
graphs.py           combinatorial S, R, C5 and their measured metrics
sim_patches.py      tau-leap on the graph; exact Gillespie for one site
measure.py          phase, winding, defects, tracks, synchrony
harness.py          H1-H3, P1-P2
run_patches.py      main grid and comparison
deterministic.npz graphs.npz topo_cache.npz    frozen inputs
production_patches.json harness.json graph_metrics.json
evidence_patches.json.gz  fig_patches.png
```

## Reproducing

Python 3.11 with `numba`, `numpy`, `scipy`, `matplotlib`.
`python harness.py` then `python run_patches.py`. Both expose an importable
`main()`; on this host a process pool cannot be created from a nested
subprocess, so the runner was invoked in-process.

Nothing was pushed anywhere.
