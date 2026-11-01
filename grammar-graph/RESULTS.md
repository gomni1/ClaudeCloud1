# RESULTS: the grammar on a graph (PHYS2, 1 Nov 2026)

## Freeze

SPEC.md frozen before any simulation code ran. SHA-256: `f9be5551a459fba1e3a150f46c509e120abfccbb311b675bf2ad0a91fdc6d1c6` (1 Nov 2026, commit "SPEC freeze").

## Revisions and bug log

- **Mean-field references reproduced (no discrepancy).** lam = 0: period 6.3524, balance (0.0812, 0.6332, 0.1801,
  0.1055), c in [0.0545, 0.1190], v in [0.5445, 0.7235], winding number -1 (once, clockwise in (c, v)); Hopf at
  lam_H = 0.012300. lam = 0.006: period 5.9896. lam = 0.02: no cycle (s_c, s_v from lam = 0, as preregistered).
- **H1 FAILED as preregistered** (K, N = 10^4): period 5.783 (-9.0%; tolerance 3%), range [0.0466, 0.1263]
  (tolerance 10%). Not a code bug: an exploratory check after the failure (60 periods, discard 20) gave period
  5.873 / 6.303 / 6.397 and range [0.0467, 0.1262] / [0.0552, 0.1156] / [0.0543, 0.1186] at N = 10^4 / 10^5 / 10^6,
  so the lumped chain converges to the mean field and the deviation is a finite-size effect of the well-mixed
  chain at N = 10^4 (shorter period, larger excursions; lam = 0 sits 0.0123 from the Hopf point). This failure
  stays on the record: under the frozen SPEC the harness did not pass, and G2/G3 do not count under it.
- **Revision R1 (new claim, written after the exploratory check above, so not blind).** H1-R1: SPEC H1 unchanged
  (130 periods, discard 30, same estimators and tolerances) at N = 10^6, seed seed_of("H1", "R1"). If H1-R1 passes,
  the harness passes under R1 and G2/G3 are reported as counting under R1 only. Nothing else changes.
