# ClaudeCloud1 — PHYS2 working record

Computations, preregistrations and night-run reports for PHYS2.0, Glenn Millar's theoretical physics reconstruction from minimal relational principles. Everything here is **SANDBOX/DRAFT**: nothing is promoted by being in this repository. What Glenn has placed or ruled is recorded on the PHYS2 Premise Map (a claude.ai artifact), which cites these folders.

Most runs follow one pattern: a `SPEC.md` frozen before any code ran (its SHA-256 recorded in `RESULTS.md`), planted failures to show the harness can see what it is looking for, and a `RESULTS.md` with verdicts, revisions and the evidence beside it.

## Index, oldest first

| Date | Folder | What it asks | Outcome in brief |
|---|---|---|---|
| 5 Oct | repository root: `src/`, `tests/`, `results/`, `RESULTS.md`, `ORDER-TEST-README.md` | Order test: does refractory succession make the outcome depend on transaction order, against a commuting control? | Order mattered only when donor and receiver were delayed differently; the framing was later rejected (one-to-one bookkeeping) |
| 27 Oct | `p29a-section-strata/` | P2.9A: what continuity and closure alone force about the symmetry stratum a closed field of cross-sections must pass to carry a half-twist | Proofs and stop points per claim |
| 28 Oct | `grammar-exit-time/` | Open-level Contact/Void grammar: do dissolution times grow exponentially with ensemble size, and is switching cheaper than dissolution? | See its RESULTS |
| 30 Oct | `grammar-instability/` | Can one level sustain a cycle under threshold rates, or go unstable when roles move at different rates? | All three claims killed (with the all-neighbours count) |
| 30 Oct | `lean-check/` | Independent compile and comparator check of external Lean proofs (OpenAI maths release) | Family 176 verified; six targets underdetermined (compute budget) |
| 30 Oct | `grammar-idsize/` | Identity with size: race test between switching and dissolution; small-size test of the dissolution slope | See its RESULTS |
| 31 Oct | `grammar-clock/` | The grammar's clock: where stable cycles live in rate space, how they end, and how a finite cycle behaves as a stochastic clock | Stable cycles found (C1 yes); finite-size clock holds (S1); S3–S4 underdetermined |
| 1 Nov | `grammar-graph/` | The closed-level grammar on fixed graphs, tested for persistent phase defects | Persistent defects killed (D1); D2–D3 pass; D4 not applicable |
| 1 Nov | `PHYS2-science-2026-11-01/` | A: does a clock's escape hazard depend on its phase? B: do switching paths near dissolution pass through it more often? | A supported, not killed; B killed |
| 1 Nov | `PHYS2-science-2026-11-01-patches/` | Coupled clocks on a graph: do persistent localised integers form? | Sites tick; persistent localised integer killed |
| 1 Nov | `PHYS2-science-2026-11-01-routes/` | 'Identity and size, through coupled routes', on fresh runs | Killed on the reversal clause |
| 6 Nov | `phys2-saturation-2026-11-06/` | What bounds one level of the turnover grammar: short proofs S1–S5 and preregistered checks N0–N4 | See its note and RUN |
| 6 Nov | `phys2-step-balance-2026-11-06/` | Step balance, orientation and the decay weight (pion ratio, muon spectrum, neutron, clock) | No frozen SPEC; the note is the record |
| 9–15 Nov | `phys2-2026-11-09-to-15/` | Seven PHYS2 Night Runs, the timing–extent run, Astra and DeepSeek replies of 11 Nov, standing constraints of 10 Nov | See its README |

## Working files elsewhere

- **Google Drive, Audit Outputs:** the live standing constraints, night reports as they are written, and verification replies from DeepSeek and Astra.
- **PHYS2 Premise Map and narrative spine:** claude.ai artifacts; the map's timeline records each decision with its source.
