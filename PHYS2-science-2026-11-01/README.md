# PHYS2 local task, 1 November 2026 — two preregistered tests on the well-mixed grammar

Two independent preregistered tests. Each part has its own frozen `SPEC.md`,
its own `RESULTS.md` carrying the freeze hash and the full change log, its own
planted checks, and compressed evidence.

| part | question | verdict |
|---|---|---|
| **A** | Does a clock's escape hazard depend on its phase? | **S4' supported — not killed**, at every size, for both models (p < 1e-18 throughout) |
| **B** | Do switching paths that come closer to dissolution pass through it more often? | **KILL** — the candidate 'Identity and size, through coupled routes' is killed on this line (2 of 3 sizes) |

## Preregistration

Each `SPEC.md` was written and frozen before the production code for its part
ran, and its SHA-256 recorded in the matching `RESULTS.md`:

- `A/SPEC.md` — `dc0d610e639215764e28245fe9d8c981a5cd3377ff233f587bdc846709350866`
- `B/SPEC.md` — `806824d20f02b0c59c59da052bae4ec30ac1389fcb43ba5cb7dd1d20142ef864`

What preceded each freeze, and is disclosed in the corresponding `RESULTS.md`:
Part A's deterministic cycle extraction and the 3.7-CPU-minute R-selection pilot
(cap 5), and Part B's algebraic balance characterisation. No pilot datum enters
any test.

## Method

Exact stochastic simulation throughout — **Gillespie's direct method in the
Kurtz form**, every propensity `Omega * r(n/Omega)`, inner loops compiled with
`numba`. No tau-leaping and no time discretisation. In both parts the Markov
chain is an effective-register summary of step processes, as each SPEC states.

## Layout

```
A/  SPEC.md RESULTS.md                 frozen preregistration, results, change log
    models_a.py                        grammar, deterministic ODE, limit cycle
    cycle_A1.npz cycle_A2.npz          frozen cycles, referenced by hash in SPEC §5
    sim_a.py driver_a.py run_a.py      simulator, cell driver, production grid
    planted_a.py                       planted checks P1, P2, P3
    fig_hazard.png                     binned escape hazard with 95% intervals
    evidence_A.json.gz                 pilot, grid, per-bin counts, planted records
B/  SPEC.md RESULTS.md                 frozen preregistration, results, change log
    fixed_points.py                    the three deterministic balances
    sim_b.py driver_b.py run_b.py      simulator, cell driver, production runs
    planted_b.py                       planted checks P1, P2 and end-to-end rescan
    fig_delta.png                      closest-approach distributions by direction
    evidence_B.json.gz                 per-cell statistics and planted records
REPORT.md                              the one-page report
```

## Reproducing

Python 3.11 with `numba`, `numpy`, `scipy`, `matplotlib`. From each part's
folder: `python run_a.py` / `python run_b.py` for production, `python
planted_a.py` / `python planted_b.py` for the planted checks. Both runners
parallelise cells across processes; each cell's CPU budget is measured inside
its own process. Note that on this host a process pool could not be created
from a nested subprocess (Windows named-pipe permission), so the runners were
invoked in-process; `main()` is importable for that purpose.

## Two things that need Glenn's call

1. **Part A planted check P3 failed as frozen**, and the failure stands on the
   record. It is not a simulator bug: the frozen metric is dominated by phase
   diffusion, and the 1 % bar at `Omega = 1e5` is below A1's own fluctuation
   floor at that size. Two revisions are logged as new claims in
   `A/RESULTS.md` §3.2–3.3; the second confirms convergence to the
   deterministic cycle, which is what P3 exists to test. The frozen gate "all
   must pass before results count" is **not** satisfied as written.
2. **Part B's kill is carried by exact median ties** at `Omega = 8` and `12`,
   which the frozen SPEC §6 anticipated and ruled count towards the kill. The
   mean delta orders in the predicted direction at all three sizes. The verdict
   stands; the detail is in `B/RESULTS.md` §5.

This folder was produced locally. There is no GitHub credential configured in
this workspace, so nothing was pushed to `gomni1/ClaudeCloud1` and no pull
request was opened; the repository was not touched.
