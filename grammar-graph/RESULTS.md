# RESULTS: the grammar on a graph (PHYS2, 1 Nov 2026)

## Freeze

SPEC.md frozen before any simulation code ran. SHA-256: `f9be5551a459fba1e3a150f46c509e120abfccbb311b675bf2ad0a91fdc6d1c6` (1 Nov 2026, commit "SPEC freeze").

<!-- BEGIN GENERATED -->
## Verdicts

| Item | Verdict | Numbers |
|---|---|---|
| H1 (frozen: K, N = 10^4) | **FAIL** | period 5.783 (target 6.3524 +-3%), range [0.0466, 0.1263] (target [0.0545, 0.119] +-10%) |
| H1-R1 (revision R1: N = 10^6) | **PASS** | period 6.3535, range [0.0542, 0.1190], 99 cycles |
| H2 (k3 = k11 = 0) | **PASS** | S: chi2 = 3.24, p = 0.357, max abs z = 1.74; K: chi2 = 0.52, p = 0.915 (40 snapshots x 10^4 sites) |
| H3 (octahedron, exact 4096-state chain) | **PASS** | z = c +0.14, v +0.74, l -0.72, p -0.42, c^2 +0.18 |
| P1 (planted defects) | **PASS** | 21 configurations (2-6 vortices) all exact; identity 0 violations (plus 200 random fields) |
| P2 (planted noise) | **PASS** | density 0.25000 (z = +0.05) planted, 0.24996 (z = -1.12) on S; exact 1/4; longest noise track 0.4; D1 criterion FAILS on noise (0 of 3 replicates, both graphs) |
| P3 (planted motion) | **PASS** | 2 tracks, lifetimes 127.6, 127.6; on planted faces in every frame; 0 swaps |
| Harness | frozen SPEC: **FAIL** (H1); under R1: **PASS** | G2/G3 below count under R1 only |
| D1 (persistent localised integer) | **KILL** | tracks >= 20 periods (127.05) in 0 of 3 replicates; longest track 2.4 time units (0.38 periods) |
| D2 (cores at local zeros) | **PASS** | ratio 0.428 (defect triangles 0.859 / all 2.007); 5212430 defect-frames |
| D3 (pairing is local) | **PASS** | births paired 1.0000 (5117710/5117740), deaths paired 1.0000 (5117815/5117842) |
| D4 (motion; report only) | not computable | no track lasts 20 periods, so the MSD set is empty |

## Graph classes

S is topologically two-dimensional by construction; it is a declared comparison class, not an assumption about the substrate. d_g is measured (fit of ln M(r) on ln r, r = 2..floor(diameter/2)).

| Class | Replicate | N | Mean degree | Clustering | Diameter | d_g (radii) | Triangles |
|---|---|---|---|---|---|---|---|
| S | 0 | 10000 | 5.9988 | 0.6034 | 31 | 2.765 (2-15) | 19996 (faces) |
| S | 1 | 10000 | 5.9988 | 0.6005 | 31 | 2.818 (2-15) | 19996 (faces) |
| S | 2 | 10000 | 5.9988 | 0.6005 | 30 | 2.786 (2-15) | 19996 (faces) |

## G2: class S by lam (3 replicates; mean over replicates, longest = max)

| lam | A (global amplitude / well-mixed s_c) | Rbar | mean global (c, v) | defect density | longest track (time units) | tracks >= 20 periods | replacement | identity violations |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 0.221 | 0.169 | (0.0759, 0.6568) | 0.0219 | 2.4 | 0 | n/a (no long tracks) | 0 |
| 0.006 | 0.289 | 0.187 | (0.0764, 0.6563) | 0.0217 | 2.8 | 0 | n/a (no long tracks) | 0 |
| 0.02 | 0.217 | 0.220 | (0.0776, 0.6546) | 0.0214 | 2.8 | 0 | n/a (no long tracks) | 0 |

## G3: comparison classes at lam = 0 (2 replicates each; S from G2 for reference)

| Class | Rbar (global coherence) | A | Triangles | Defect density | Longest track | Tracks >= 20 periods |
|---|---|---|---|---|---|---|
| S (G2, lam = 0) | 0.169 | 0.221 | 19996 | 0.0219 | 2.4 | 0 |

## CPU

| Part | CPU used | Cap |
|---|---|---|
| G1 | 0.024 h (85 s, incl. H1-R1) | 0.5 h |
| G2 | 0.072 h (258 s) | 3.0 h |
<!-- END GENERATED -->

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
