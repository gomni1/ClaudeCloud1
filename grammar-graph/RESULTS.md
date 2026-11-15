# RESULTS: the grammar on a graph (PHYS2, 1 Nov 2026)

## Freeze

SPEC.md frozen before any simulation code ran. SHA-256: `f9be5551a459fba1e3a150f46c509e120abfccbb311b675bf2ad0a91fdc6d1c6` (1 Nov 2026, commit "SPEC freeze").

## Summary

The site rule of draw 19387 was simulated exactly on fixed graphs (N = 10^4). On the triangulated sphere S, local
phase defects are abundant (about 2.2% of faces in every frame). Their cores sit at low amplitude (D2 passes), and
they are born and die in local opposite-sign pairs (D3 passes). But no defect keeps an identity for longer than 2.8
time units (0.44 periods), so D1 (a persistent localised integer) is **killed** and D4 cannot be computed. No
comparison class (K, R, C0, C5) hosts a track lasting 20 periods. On every sparse graph the well-mixed clock is lost:
the global C fraction fluctuates with A of about 0.2-0.3 of the well-mixed cycle's spread, with no spectral line, at
lam = 0, 0.006 and 0.02 alike. The harness failed H1 as frozen. That was a finite-size effect of the well-mixed chain
at N = 10^4, not a code bug (see the bug log). It passed under revision R1 (H1 at N = 10^6), and **the G2/G3 verdicts
count under R1 only**.

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
| K | - | 10000 | 9999 | 1 | 1 | n/a (no radii 2..0) | C(10^4, 3) = 166616670000 |
| R | 0 | 10000 | 8.0000 | 0.0005 | 7 | 4.763 (2-3) | 50 |
| R | 1 | 10000 | 8.0000 | 0.0005 | 7 | 4.762 (2-3) | 46 |
| C0 | 0 | 10000 | 8.0000 | 0.6429 | 1250 | 0.997 (2-625) | 60000 |
| C0 | 1 | 10000 | 8.0000 | 0.6429 | 1250 | 0.997 (2-625) | 60000 |
| C5 | 0 | 10000 | 8.0000 | 0.5513 | 15 | 3.553 (2-7) | 51195 |
| C5 | 1 | 10000 | 8.0000 | 0.5549 | 16 | 3.710 (2-8) | 51550 |

## G2: class S by lam (3 replicates; mean over replicates, longest = max)

| lam | A (global amplitude / well-mixed s_c) | Rbar | mean global (c, v) | defect density | longest track (time units) | tracks >= 20 periods | replacement | identity violations |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 0.221 | 0.169 | (0.0759, 0.6568) | 0.0219 | 2.4 | 0 | n/a (no long tracks) | 0 |
| 0.006 | 0.289 | 0.187 | (0.0764, 0.6563) | 0.0217 | 2.8 | 0 | n/a (no long tracks) | 0 |
| 0.02 | 0.217 | 0.220 | (0.0776, 0.6546) | 0.0214 | 2.8 | 0 | n/a (no long tracks) | 0 |

## G3: comparison classes at lam = 0 (2 replicates each; S from G2 for reference)

| Class | Rbar (global coherence) | A | Triangles | Defect density | Longest track | Tracks >= 20 periods |
|---|---|---|---|---|---|---|
| K | 1.000 | 1.278 | 166616670000 | 0.0000 | 0.0 | 0 |
| R | 0.746 | 0.247 | 48 | 0.0296 | 2.0 | 0 |
| C0 | 0.130 | 0.207 | 60000 | 0.0065 | 1.2 | 0 |
| C5 | 0.075 | 0.214 | 51372 | 0.0196 | 1.6 | 0 |
| S (G2, lam = 0) | 0.169 | 0.221 | 19996 | 0.0219 | 2.4 | 0 |

C-report: classes hosting defect tracks lasting >= 20 periods: none (of K, R, C0, C5; S: none).

## CPU

| Part | CPU used | Cap |
|---|---|---|
| G1 | 0.024 h (85 s, incl. H1-R1) | 0.5 h |
| G2 | 0.072 h (258 s) | 3.0 h |
| G3 | 0.055 h (196 s) | 1.5 h |
<!-- END GENERATED -->

## Reading the results

- **D2 and D3 pass, but D1 is killed.** This is the profile of phase singularities in a spatially smoothed, temporally
  filtered noisy field. Zeros of such a field sit at low amplitude (D2: ratio 0.43), and they are created and destroyed
  as nearby opposite-sign pairs (D3: births and deaths paired at 99.999%). They live 1-7 frames. Track-lifetime
  histograms are in `evidence/g2/*.json`. The D3 pass therefore describes short-lived pairs, not persistent defects.
- **No collective clock on S.** The mean global (c, v) on S is (0.076, 0.657), against the well-mixed balance
  (0.0812, 0.6332). An exploratory check, not preregistered (`evidence/exploratory_spectrum_S.json`): the
  periodogram of the global C fraction has no line. Its largest bin is 12-15 times the median at every lam, which is
  the level expected for the largest of about 2000 noise bins (about 11). A = 0.22 is broadband fluctuation.
- **Rbar on R (0.75) is an offset, not synchrony.** On R the mean global (c, v) is (0.0945, 0.573), which is
  +0.6 s_c and -1.0 s_v from (c*, v*). The radius-2 balls (65 sites) average the noise down, so most local phases
  point the same way. A is 0.25 there too. C0 and C5 have Rbar 0.13 and 0.075, and mean states close to the balance.
- **R has only 48 triangles** (locally tree-like; about (d-1)^3/6 = 57 expected), so its defect density is a density
  over very few triangles. C0 has a lower density (0.65%) than S (2.2%) and C5 (2.0%). Rewiring 5% of the edges
  triples it.
- **K at N = 10^4** oscillates with A = 1.28, larger than the mean-field cycle (the H1 finding). Its fields are all
  equal by construction, so no defects are possible there.
- The total-winding identity held on every frame of all 9 runs on S (4764 frames each; 0 violations) and on
  every planted field.

## Past the Hopf point

In the mean field the cycle is gone at lam = 0.02: the balance is a stable focus, and s_c, s_v are taken from lam = 0
as preregistered. On S nothing changes qualitatively across the Hopf point. A is 0.221, 0.289 and 0.217 at lam = 0,
0.006 and 0.02. Rbar rises slightly (0.169, 0.187, 0.220), defect density stays at 2.1-2.2%, and the longest track
is 2.4-2.8 time units at every lam. On S the stochastic site dynamics is already non-oscillatory at lam = 0, so the
mean-field bifurcation leaves no visible trace in these measurements.

## Observational register

Analogies only: short-lived opposite-sign phase-winding pairs that nucleate and annihilate locally resemble
vortex-antivortex pair fluctuations in a two-dimensional medium below any binding regime, or virtual
particle-antiparticle pairs, rather than stable particles; nothing here supports reading them as persistent
particles.

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
  Result: H1-R1 **passes** (period 6.3535, range [0.0542, 0.1190]).
- **Accounting fix (not a simulator bug):** the first `evidence/g2_cpu.json` double-counted CPU (it added the
  workers' own figures to the parent's figure, which already includes the reaped workers). It was corrected to the
  parent's figure (258 s) and the code was fixed before G3. No simulator, detector or tracker bug was found or fixed.
- **Wording clarifications, criteria unchanged:** in D3, a fraction with zero events is underdetermined (stated in the
  SPEC). In the G3 table, K's triangle count is C(10^4, 3) and its defect density 0, both by construction (SPEC 4).
