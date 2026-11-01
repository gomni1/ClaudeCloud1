# grammar-graph (PHYS2, 1 Nov 2026)

The closed-level grammar (draw 19387, PR 7) run as an exact site-level Markov chain on fixed graphs, and tested
for persistent phase defects. `SPEC.md` is the frozen preregistration (its SHA-256 is in `RESULTS.md`).
`RESULTS.md` has the verdicts (H1-H3, P1-P3, D1-D4), the graph, G2 and G3 tables, the revisions and the bug log.

| Path | Content |
|---|---|
| `SPEC.md` | Preregistration (frozen) |
| `RESULTS.md` | Verdicts, tables, revisions and bug log, CPU |
| `csrc/gg.c` | Exact simulator (per-site Gillespie with a sum tree, lumped chain on K), filtered ball fields, winding detector. The RNG and rate conventions are copied with attribution from `grammar-clock/csrc/ssa.c` (PR 7, from PR 3) |
| `gg/core.py` | Rates, homotopy, mean-field references, combinatorial graph classes (K, R, C0, C5, S, planted sphere), graph statistics, ctypes wrappers, tracker (mutual-unique same-sign), D3 pairing, MSD, replacement |
| `g1.py` | Harness: H1, H2, H3, P1, P2, P3 |
| `g23.py` | G2 (class S) and G3 (classes K, R, C0, C5) |
| `make_results.py` | Builds the generated tables in `RESULTS.md` from `evidence/` |
| `tests/test_harness.py` | pytest: H1 (N = 10^6, shortened), H2, H3, P1, P2, P3 |
| `evidence/` | `g1.json`, per-run JSON summaries, compressed per-frame series (`.npz`: role counts, coherence, defect counts, quantised phase snapshots for replicate 0), graph statistics, logs, CPU |

Run: `pip install numpy scipy numba pytest`; `python g1.py`; `python g23.py g2`; `python g23.py g3`;
`python make_results.py`; `python -m pytest -q`. The C library is built with gcc on first use.
