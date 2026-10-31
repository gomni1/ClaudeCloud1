# grammar-clock (PHYS2, 31 Oct 2026)

The grammar's clock: where stable cycles live in rate space (K1), how far the draw-12051 cycle survives toward
moderate rates and how cycles end (K2), and how the cycle behaves as a finite-size stochastic clock (K3).
SPEC.md is the frozen preregistration (SHA-256 in RESULTS.md); RESULTS.md has the verdicts and tables.

| Path | Content |
|---|---|
| `SPEC.md` | Preregistration (frozen) |
| `RESULTS.md` | Verdicts C1, S1-S4, tables, revisions, CPU |
| `k1.py` | K1: PR 4's M2 (`../grammar-instability/ginst`, unchanged) + per-draw 120 CPU-s cap (fork + RLIMIT_CPU); K1b, K1a, K1c |
| `k2.py` | K2: shooting + pseudo-arclength continuation, Floquet moduli, balances, end classification |
| `k2_k1cycles.py`, `run_k2_after_k1.sh` | Selection of the K1 cycles for K2 (smallest span) |
| `k3.py` | K3: harness (H1, H2, P1-P3), size sweep, claims S1-S4 |
| `clock/core.py` | ctypes wrapper of the SSA, deterministic reference cycle, tick/stall estimators, exact master equation |
| `csrc/ssa.c` | Gillespie direct method, copied from PR 3 (`grammar-exit-time/csrc/ssa.c`) with an attribution header and adapted |
| `make_results.py` | Builds the RESULTS.md tables from `evidence/` |
| `tests/test_k3.py` | pytest: H1, H2 (Omega 5, 10), P1, P2, P3 |
| `evidence/` | Records (gzipped JSONL), JSON summaries, logs |

Run: `pip install -r ../grammar-instability/requirements.txt`; `taskset -c 2,3 python k1.py`;
`python k3.py harness sizes`; `python k2.py lam12051 1500` (also `Tup`, `Tdown`, `lamK1`); `python -m pytest -q`.
The C library is built on first use with gcc.
