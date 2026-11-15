# grammar-idsize

Status: SANDBOX / DRAFT. Not promoted. PHYS2 cloud campaign, task B (30 Oct 2026).

Identity with size, in two parts:

1. **The race test.** For a family of rate constants that keeps the balances fixed (k10 ∈ {½, 1, 2}), is the fraction of switches that pass through dissolution predicted by a race between the switching and dissolution clocks (R1)? Does its decay with Ω follow the dissolution cost W_D (R2)?
2. **The small-size test.** Is the gap between PR 3's brute-force dissolution slope and gMAM's W_D = 0.820 a small-size effect? Forward flux sampling (FFS) to Ω = 30 answers this (G1, with G2 reported only).

`SPEC.md` is the preregistration. It was frozen before any code ran; its SHA-256 is in `RESULTS.md`, and `RESULTS.md` holds the outcomes. The ensemble is well mixed, so every cost grows with Ω by construction.

## Layout

| Path | Content |
|---|---|
| `SPEC.md` | frozen preregistration |
| `RESULTS.md` | outcomes, verdicts, deviations, CPU |
| `gexit_pr3/` | PR 3's simulator, master-equation solver, gMAM and fits, copied with attribution from `grammar-exit-time/` (which is not modified). `model.set_k` is the one addition. |
| `csrc/ffs.c` | FFS kernels: flux stage and interface trials (propensities and RNG copied from PR 3's `ssa.c`) |
| `idsize/family.py` | the seeding family and M0 |
| `idsize/race.py` | switching runs, T_D⁰ runs, φ estimators, Clopper–Pearson |
| `idsize/ffs.py` | the FFS driver (interfaces, stages, replicates, reactive-path summaries) |
| `idsize/planted.py` | PF5, PF6, and PF1 via FFS |
| `run_b.py` | stages `m0`, `planted`, `gmam`, `switch`, `td0`, `exact`, `harness`, `ffs` |
| `analysis_b.py` | race table, R1, R2, G1, G2, crossover → `evidence/analysis.json` |
| `tests/test_b.py` | pytest |
| `evidence/` | outputs and run logs. The raw switching times (267 MB) are not committed: `switch_summary.json` keeps counts and moments, and the runs are reproducible from their seeds. |

## Reproduce

Python 3.13 with numpy, scipy, numba, sympy and mpmath, plus gcc (`requirements.txt`). On 2 cores:

```bash
python3 run_b.py m0 planted harness ffs switch td0 exact
```

```bash
python3 analysis_b.py
```

```bash
python3 -m pytest -q
```
