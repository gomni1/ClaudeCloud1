# P2.9A — Section strata

A bounded investigation for PHYS2. It asks what continuity and closure alone force about which symmetry stratum a closed field of planar cross-sections must pass through to carry a half-twist. SANDBOX / DRAFT, not promoted.

- `SPEC.md` holds the preregistered definitions, claims, kill conditions and planted failures. It is frozen; its SHA-256 is in `RESULTS.md`.
- `RESULTS.md` has one row per claim, the exact proofs, the stop points, and the observational register.
- `evidence/results.json` is the full output of `run_all.py`.

## Layout

| Path | Contents |
|---|---|
| `strata/sections.py` | Mode vectors, rotation action, strata and tolerances, area moments, 60-gon analogue |
| `strata/orientation.py` | Orientation maps θ_P, θ_R, θ_M, θ_P′, ψ_2; guarded lifts; lift validator; windings |
| `strata/loops.py` | Connection rotation, passage detector, stratum audit, H1b homotopy, rigid-sector and passage loops |
| `strata/proofs.py` | Exact sympy checks |
| `strata/experiments.py` | H0–H2 constructions |
| `strata/experiments_h34.py` | H3–H4 constructions |
| `tests/test_planted.py` | The three planted failures |
| `tests/test_core.py` | Regression tests for the main constructions |

## Run

```
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q
```

Python 3.14 with numpy 2.5 and sympy 1.14 was used. The full run takes about 13 s.
