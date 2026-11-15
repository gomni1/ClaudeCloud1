# grammar-instability

Status: SANDBOX / DRAFT. Not promoted. PHYS2 cloud campaign, task A (30 Oct 2026).

**Outcome: all three claims killed, each with the tot denominator** (see `RESULTS.md`).

Can one level of the grammar sustain a cycle under threshold rates (H-cyc), or become unstable when its roles move at different rates (H-mob-stat, H-mob-osc)? `SPEC.md` is the preregistration, frozen before any code ran; its SHA-256 is in `RESULTS.md`, and `RESULTS.md` holds the outcomes.

## Layout

| Path | Content |
|---|---|
| `SPEC.md` | frozen preregistration |
| `RESULTS.md` | outcomes, claim statuses, deviations, CPU |
| `ginst/model.py` | the model (§1): rates, TH and MA laws, cv and tot, open and closed levels, balances, analytic Jacobians (numba) |
| `ginst/integ.py` | ode23s (Rosenbrock 2(3), numba), the continuation filter, the Radau Poincaré stage, the end-state classifier |
| `ginst/symbolic.py` | M0 and M1 in sympy |
| `ginst/m2.py` | M2 draws, per-draw processing, the adaptive-stage objective |
| `ginst/m3.py` | M3: P-matrix test (mpmath fallback), oscillatory and stationary mobility scans, two-class sweep |
| `ginst/m4.py` | M4: cycle verification (LSODA and Radau, Floquet multipliers) and the 200-site ring |
| `ginst/planted.py` | planted failures PFA1–PFA4 |
| `run_a.py` | stages `planted`, `m2`, `m4cyc`, `m3`, `m4ring` (and `adaptive`, not run: see `RESULTS.md`) |
| `analysis_a.py` | coverage, outcome tables and claim statuses → `evidence/analysis.json` |
| `tests/test_a.py` | pytest: M0 and PFA1–PFA4 |
| `evidence/` | raw outputs and run logs |

## Reproduce

Python 3.13 with numpy, scipy, numba, sympy and mpmath (`requirements.txt`). On 2 cores:

```bash
python3 -m ginst.symbolic
```

```bash
python3 run_a.py planted m2 m4cyc m3 m4ring
```

```bash
python3 analysis_a.py
```

```bash
python3 -m pytest -q
```

M2 is deterministic per draw (seed 30102026), and the cycle at draw 12051 can be reproduced on its own from the rates in `RESULTS.md` or `evidence/m4_cycle.json`.
