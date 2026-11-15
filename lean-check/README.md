# Lean check

An independent compile and comparator check of external Lean proofs from github.com/openai/math, for PHYS2 (task C, 30 Oct 2026). Status: SANDBOX / DRAFT, not promoted.

`REPORT.md` has one row per target, the environment, the budget, and the family 149 questions. `logs/` holds the logs (large ones gzipped) and `scripts/` the scripts that produced them. The release was built outside this repository, and no build products are committed.

Outcome:
- **SecondKahnKalai (family 176): Verified.** It builds, `#print axioms` gives only the permitted axioms, and the comparator accepts it.
- **The other six targets: Underdetermined.** Families 149, 131, 186, 220, and 229 (two configs) each need all of Mathlib, built from source because the cache was unreachable. That is about 11 CPU-hours, over the 10 CPU-hour cap.
