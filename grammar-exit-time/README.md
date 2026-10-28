# Grammar exit times

A bounded, preregistered numerical investigation for PHYS2. Status: SANDBOX / DRAFT, not promoted.

It asks two things about the open-level Contact/Void grammar (roles C, V, L, P) at fixed rates, as the ensemble size Ω grows:

- whether the mean dissolution time grows exponentially with Ω and the exit is memoryless;
- whether an expression change (switching between the two TH balances) costs less per unit of ensemble than dissolution.

The ensemble is well mixed, so every cost in it grows with Ω by construction. The run cannot see a localised path whose cost does not grow with the ensemble.

## Files

- `SPEC.md` holds the preregistered definitions, claims, kill conditions, planted failures and expected outcomes. It was frozen before any code; revision 1 changed framing only. Both SHA-256 hashes are in `RESULTS.md`.
- `RESULTS.md` has the K1–K3 verdicts, the W table, the harness checks and every wall that bit.
- `evidence/` holds the JSON outputs: raw runs per series, summaries and `analysis.json`.

## Layout

| Path | Contents |
|---|---|
| `csrc/ssa.c` | Exact SSA (Gillespie direct method) in Kurtz form: MA, TH, the R1 combinatorial form, and the planted models. Burn-in with restarts, censoring caps, CPU deadline, histograms |
| `gexit/model.py` | Deterministic grammar: rates and gradients, ODE, balances, Jacobians, λ_slow and burn-in times |
| `gexit/sim.py` | ctypes wrapper, seeding, process pool |
| `gexit/series.py` | Series runner: pilot, burn-in feasibility, budget and grid-extension rule (SPEC §3, §6) |
| `gexit/stats.py` | Censored exponential MLE, chi-square and bootstrap intervals, Lilliefors-type test, F1 fits |
| `gexit/master.py` | Exact MFPT to D on a truncated lattice (sparse LU, or Ruge–Stüben AMG with GMRES and refinement) |
| `gexit/gmam.py`, `gexit/gmam_nb.py` | gMAM: geometric action, inner Hamiltonian solve (numpy reference and numba kernel), L-BFGS-B outer loop, reparametrisation, N-doubling |
| `gexit/m4.py` | All gMAM items and initial paths |
| `gexit/planted.py` | PF1–PF4: exact comparators and harness runs |
| `run_all.py` | Runs every stage and writes `evidence/*.json` (resumable) |
| `analysis.py` | F1, F2, M2, R1, K1–K3, W table and ratios, written to `evidence/analysis.json` |
| `tests/` | pytest for M0, M6, PF1–PF4 and the gMAM validations |

## Run

```bash
python -m pip install -r requirements.txt
```

```bash
python run_all.py
```

```bash
python -c "from gexit import m4; m4.run_all('evidence/gmam_raw.json')"
```

```bash
python analysis.py
```

```bash
python -m pytest -q
```

The C simulator is compiled on first use with `gcc -O3 -march=native` into `build/`. The run used Python 3.13 with numpy 2.5, scipy 1.18, numba 0.68 and pyamg 5. Simulation stages are capped by the CPU budgets of SPEC §6.
