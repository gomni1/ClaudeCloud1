# PHYS2 routes test, 1 November 2026

Test of the candidate *'Identity and size, through coupled routes — tested on
the whole distribution'* on **fresh runs**.

**Verdict: KILL**, on the reversal clause. `p < 0.05` in the claimed direction
at 3 of 4 sizes (Omega = 10, 12, 16), but at Omega = 8 the opposite one-sided
test gives `p = 3.51e-03`, and SPEC §7 kills on a reversal at any size.

## Preregistration

`SPEC.md` was frozen before any production run; its SHA-256 is recorded in
`RESULTS.md`:

- `SPEC.md` — `f86996fd1078978260c5460c2cf0723ca8ab748cf6f2db474b1e4448dff927af`

**Fresh runs only.** Seed base `5000000`, disjoint from every seed used in
`PHYS2-science-2026-11-01`. No run, delta, count or seed from the previous
night's Part B entered any statistic here. The reason is on the record in
SPEC §2: the candidate was formulated after its predecessor's medians tied and
after its means had been seen to favour it.

**Simulator reused with attribution.** `sim_routes.py` is a verbatim copy of
`PHYS2-science-2026-11-01/B/sim_b.py` (source SHA-256
`7d975c5fc0dc65231c4dc7f174805b11484a08d402d5d198aba1a5123f9c6e17`) with an
attribution header prepended and the body unmodified.

## Method

Exact Gillespie direct method in the Kurtz form, every propensity
`Omega*r(n/Omega)`, numba-compiled; no tau-leaping, no time discretisation. The
Markov chain is an effective-register summary of step processes, as SPEC §1
states. Statistic: one-sided Mann-Whitney U on the runs that did not visit D,
mid-ranks with tie correction, asymptotic p.

## Result

| Omega | p (up < down) | p (up > down) | rank-biserial r | bootstrap 95 % CI | outcome |
|---|---|---|---|---|---|
| 8 | 9.965e-01 | 3.507e-03 | -0.0382 | [-0.0652, -0.0101] | **reversed** |
| 10 | 1.989e-30 | 1.000e+00 | +0.1653 | [+0.1349, +0.1926] | claim direction |
| 12 | 1.417e-26 | 1.000e+00 | +0.1535 | [+0.1244, +0.1814] | claim direction |
| 16 | 5.172e-71 | 1.000e+00 | +0.2629 | [+0.2346, +0.2901] | claim direction |

Planted checks: P1 50/50 detections, P2 45/50 non-significant,
P3 200 runs rescanned with 0 mismatches — all pass.
Production cost 21.2 CPU-seconds; no cell reached its 5-CPU-minute budget.

## Layout

```
SPEC.md              frozen preregistration
RESULTS.md           freeze record, verdict table, change log
sim_routes.py        simulator, attributed copy of the previous Part B
driver_routes.py     one (direction, Omega) cell under the stopping rule
run_routes.py        production grid
planted_routes.py    planted checks P1, P2, P3
analyse_routes.py    Mann-Whitney, rank-biserial, bootstrap, verdict rules
fig_ecdf.png         delta distributions by direction and size
evidence_routes.npz  raw delta arrays (integer lattice levels) + passage flags
evidence_routes.json.gz  per-cell summaries, test results, planted records
REPORT.md            the one-page report
```

## Reproducing

Python 3.11 with `numba`, `numpy`, `scipy`, `matplotlib`.
`python planted_routes.py` then `python run_routes.py`. Both expose an
importable `main()`; on this host a process pool cannot be created from a nested
subprocess, so the runner was invoked in-process.
