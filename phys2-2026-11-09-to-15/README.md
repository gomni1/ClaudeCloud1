# PHYS2, 9–15 November 2026

SANDBOX/DRAFT. Copies of the working files from Glenn's Google Drive (Audit Outputs and its Night-Reports folder), made 15 Nov 2026 so the repository catches up after the last push on 8 Nov. Nothing here is promoted; the Premise Map and Glenn's rulings decide status.

## What is here

| Folder | Contents |
|---|---|
| `night-runs/2026-11-09` … `2026-11-15` | One folder per PHYS2 Night Run: the report (`NIGHT-REPORT-*.md`), the queue frozen before any work (`NIGHT-QUEUE-*.md`), the Premise Map snapshot the run read (`MAP-SNAPSHOT-*.md`), and the receipts (scripts, outputs, checker reports) named `N-<date>-<item>-*`. |
| `night-runs/` | `NIGHT-RUN-SPEC.md` (v2.1, 10 Nov) and the current `STEERING.md` (15 Nov; PIN: where a curved step-distance can come from). |
| `night-runs/superseded/` | Earlier steering files and spec versions, kept for the record. |
| `timing-extent-2026-11-10/` | The timing–extent trade run of 10 Nov: the note, its first filed copy (before Glenn's acceptance of clarification C1), and `files/` with the v3 prompt, pre-run clarifications, Jev ledger report and summary, results and the two CSV tables. |
| `audit-outputs/` | Astra's closed-level clock (11 Nov), DeepSeek's balance identities (11 Nov), and PHYS2-STANDING-CONSTRAINTS.md as amended 10 Nov. |

## Integrity

Files were downloaded from Drive byte-for-byte. Every receipt listed in a night report's SHA-256 table (103 files across the seven nights) was checked against its hash after download: all match.

## Not included

Five Python scripts from the timing–extent run could not be copied in this pass: `tet_exact.py`, `tet_sim.py`, `tet_analyze.py`, `tet_extra.py` and `tet_ticks.py`. They remain in Drive, in Audit Outputs › TIMING-EXTENT-TRADE-2026-11-10-files. Their outputs (`results.txt`, `results_extra.txt`, `results_ticks.txt`, `cells.csv`, `strata.csv`) are included.

## Where the results went

The Premise Map (claude.ai artifact) carries what Glenn placed from these runs, with sources pointing at the files above. Main changes in this period: the ownership and drift gaps merged into "What rate law holds a pattern in its basin?"; the cancellation gap reworded as "What in the handoff can cancel?" with the slit conditions as its kill line; the readout theorem (no third-order term forces the squared readout, given that contributions add and the grain reads only their sum); the finding that the slit run's fringe law came from the smooth length supplied, not the handoff rule; and Glenn's ruling of 15 Nov that a uniform rule across a level is a law, not a coordinator.
