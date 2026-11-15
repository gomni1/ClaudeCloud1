# PHYS2 order test — results (SANDBOX/DRAFT)

Status: SANDBOX/DRAFT. Nothing is promoted.

In the two-entity exchange (Stage 1), transaction order changed the outcome only when donor and receiver were delayed differently. Those arms were (MASK,PAUSE) and (PAUSE,MASK), each with 574 of 1550 configurations (37.0%) over cadences 3–8, while (PAUSE,PAUSE), (MASK,MASK) and CONTROL were exactly zero everywhere.
That order dependence survived every relabelling group with identical counts, G3 included, so it does not rest on declaring donor/receiver exchange unlawful.
Sequential update changed none of the Stage 1 verdicts but cut the count from 574 to 142, so whether the effect occurs does not depend on the schedule, but how large it is does.
The three-entity loop test (Stage 2), as specified, cannot separate order from blocking: CONTROL is already handed in most configurations, because a blocked first transaction stops the whole itinerary, which I worked out by hand and recorded before running.
Compared configuration by configuration with CONTROL (the separate S2-DIFF reading), every arm that pauses an end, (PAUSE,PAUSE) included, adds handed configurations from cadence 3 under G2 and G3, (MASK,MASK) adds none, and under G1 the excess appears only with sequential update.

---

Reproduce: `PYTHONPATH=src python3 -m phys2_order.run` (about 2 minutes). Full tables,
including every sequential order and the positional reading, are in
`results/tables.md`. Machine-readable output is in `results/results.json`. Rules, relabelling
actions and the two signature readings are in `README.md`, committed before
any stage ran (commit `c4ed7ac`).

"Labeled" is the primary signature reading and "positional" the predeclared
sensitivity reading (README, *Outcome signature*). Cells are
`inequivalent / total (fraction)`.

## Validation anchors

All matched before any stage ran:

| cadence | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| rotation classes | 11 | 24 | 51 | 130 | 315 | 834 |
| rotation + reversal classes | 10 | 21 | 39 | 92 | 198 | 498 |
| rotation classes ≠ own reversal | 2 | 6 | 24 | 76 | 234 | 672 |

Achiral words containing R and D at cadences 3–5: 21 words and 94 pairs.

## Stage 1 — two entities, O1 = (A->B, B->A) vs O2 = (B->A, A->B)

### SYNC (default schedule), labeled

| arm | group | n=3 | n=4 | n=5 | n=6 | n=7 | n=8 | all |
|---|---|---|---|---|---|---|---|---|
| (MASK,PAUSE) | G1 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| (MASK,PAUSE) | G2 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| (MASK,PAUSE) | G3 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| (PAUSE,PAUSE) | G1–G3 | 0/6 | 0/28 | 0/60 | 0/186 | 0/350 | 0/920 | 0/1550 |
| (MASK,MASK) | G1–G3 | 0/6 | 0/28 | 0/60 | 0/186 | 0/350 | 0/920 | 0/1550 |
| (PAUSE,MASK) | G1 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| (PAUSE,MASK) | G2 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| (PAUSE,MASK) | G3 | 4/6 (66.7%) | 12/28 (42.9%) | 24/60 (40.0%) | 76/186 (40.9%) | 124/350 (35.4%) | 334/920 (36.3%) | 574/1550 (37.0%) |
| CONTROL | G1–G3 | 0/6 | 0/28 | 0/60 | 0/186 | 0/350 | 0/920 | 0/1550 |

The positional reading gives the same table, cell for cell.

What kind of difference it is (SYNC, G1, (MASK,PAUSE)): the two orders fire a
different number of transactions in 426 of the 574 configurations. In the other
148, both orders fire the same number but end on terminal states that no
relabelling matches.

Mechanism, from hand traces (`tests/test_dynamics.py`): under (MASK,PAUSE) each
handoff makes the receiver fall one phase behind the donor. O1 therefore tries
its second handoff at offset `d−1` and O2 at offset `d+1`. These need not both be
possible. Example: `DRR`, `d = 1`. O1 fires A->B and then never fires B->A,
because A and B are left on the same phase. O2 fires both.

### Sequential update (Stage 3), labeled. Both orders gave identical counts.

| arm | group | n=3 | n=4 | n=5 | n=6 | n=7 | n=8 | all |
|---|---|---|---|---|---|---|---|---|
| (MASK,PAUSE) | G1–G3 | 0/6 | 2/28 (7.1%) | 8/60 (13.3%) | 16/186 (8.6%) | 40/350 (11.4%) | 76/920 (8.3%) | 142/1550 (9.2%) |
| (PAUSE,MASK) | G1–G3 | 0/6 | 2/28 (7.1%) | 8/60 (13.3%) | 16/186 (8.6%) | 40/350 (11.4%) | 76/920 (8.3%) | 142/1550 (9.2%) |
| (PAUSE,PAUSE), (MASK,MASK), CONTROL | G1–G3 | 0 | 0 | 0 | 0 | 0 | 0 | 0/1550 |

Configuration-level change against SYNC (either order, either unequal arm): 509
configurations became equivalent and 77 became inequivalent.

## Stage 2 — three entities, L = (A->B, B->C, C->A) vs LR = (A->C, C->B, B->A)

### As specified, SYNC, labeled: handed configurations

| arm | group | n=3 | n=4 | n=5 | n=6 | all |
|---|---|---|---|---|---|---|
| (MASK,PAUSE) | G1 | 12/18 | 74/112 | 224/300 | 846/1116 | 1156/1546 (74.8%) |
| (MASK,PAUSE) | G2 | 12/18 | 72/112 | 200/300 | 782/1116 | 1066/1546 (69.0%) |
| (MASK,PAUSE) | G3 | 12/18 | 72/112 | 200/300 | 774/1116 | 1058/1546 (68.4%) |
| (PAUSE,PAUSE) | G1 | 12/18 | 74/112 | 224/300 | 846/1116 | 1156/1546 (74.8%) |
| (PAUSE,PAUSE) | G2 | 12/18 | 60/112 | 168/300 | 764/1116 | 1004/1546 (64.9%) |
| (PAUSE,PAUSE) | G3 | 12/18 | 60/112 | 168/300 | 744/1116 | 984/1546 (63.6%) |
| (MASK,MASK) | G1 | 12/18 | 74/112 | 224/300 | 846/1116 | 1156/1546 (74.8%) |
| (MASK,MASK) | G2 | 8/18 | 48/112 | 112/300 | 650/1116 | 818/1546 (52.9%) |
| (MASK,MASK) | G3 | 8/18 | 48/112 | 112/300 | 634/1116 | 802/1546 (51.9%) |
| (PAUSE,MASK) | G1 | 12/18 | 74/112 | 224/300 | 846/1116 | 1156/1546 (74.8%) |
| (PAUSE,MASK) | G2 | 12/18 | 66/112 | 168/300 | 764/1116 | 1010/1546 (65.3%) |
| (PAUSE,MASK) | G3 | 12/18 | 66/112 | 168/300 | 752/1116 | 998/1546 (64.6%) |
| **CONTROL** | G1 | 12/18 | 74/112 | 224/300 | 846/1116 | **1156/1546 (74.8%)** |
| **CONTROL** | G2 | 8/18 | 48/112 | 112/300 | 650/1116 | **818/1546 (52.9%)** |
| **CONTROL** | G3 | 8/18 | 48/112 | 112/300 | 634/1116 | **802/1546 (51.9%)** |

Minimal cadence with a handed configuration under SYNC: 3, for every arm,
CONTROL included, in every group and under both readings. Under every
sequential order it is 3 under G1 (labeled) and 4 otherwise, again for CONTROL
as well.

Under the six sequential orders the totals are smaller but the pattern is the
same. Example: SEQABC, G2, labeled gives (MASK,PAUSE) 600, (PAUSE,PAUSE) 585,
(MASK,MASK) 518, (PAUSE,MASK) 550 and CONTROL 518. The positional reading
gives smaller counts and no difference between G1, G2 and G3 (SYNC: CONTROL
622, (MASK,MASK) 622, (MASK,PAUSE) 944, (PAUSE,PAUSE) 852, (PAUSE,MASK) 828).

### S2-DIFF (separate reading, predeclared in README): arm verdict vs CONTROL verdict at the same configuration

SYNC, labeled. Cells are `arm-only / control-only / both`.

| arm | group | n=3 | n=4 | n=5 | n=6 | arm-only total |
|---|---|---|---|---|---|---|
| (MASK,PAUSE) | G1 | 0 / 0 / 12 | 0 / 0 / 74 | 0 / 0 / 224 | 0 / 0 / 846 | 0 |
| (MASK,PAUSE) | G2 | 4 / 0 / 8 | 24 / 0 / 48 | 88 / 0 / 112 | 144 / 12 / 638 | 260 |
| (MASK,PAUSE) | G3 | 4 / 0 / 8 | 24 / 0 / 48 | 88 / 0 / 112 | 152 / 12 / 622 | 268 |
| (PAUSE,PAUSE) | G1 | 0 / 0 / 12 | 0 / 0 / 74 | 0 / 0 / 224 | 0 / 0 / 846 | 0 |
| (PAUSE,PAUSE) | G2 | 4 / 0 / 8 | 12 / 0 / 48 | 56 / 0 / 112 | 114 / 0 / 650 | 186 |
| (PAUSE,PAUSE) | G3 | 4 / 0 / 8 | 12 / 0 / 48 | 56 / 0 / 112 | 118 / 8 / 626 | 190 |
| (MASK,MASK) | G1–G3 | 0 / 0 / … | 0 / 0 / … | 0 / 0 / … | 0 / 0 / … | 0 |
| (PAUSE,MASK) | G1 | 0 / 0 / 12 | 0 / 0 / 74 | 0 / 0 / 224 | 0 / 0 / 846 | 0 |
| (PAUSE,MASK) | G2 | 4 / 0 / 8 | 18 / 0 / 48 | 56 / 0 / 112 | 126 / 12 / 638 | 204 |
| (PAUSE,MASK) | G3 | 4 / 0 / 8 | 18 / 0 / 48 | 56 / 0 / 112 | 130 / 12 / 622 | 208 |

(MASK,MASK) has the same verdict as CONTROL in every configuration, group,
reading and schedule.

Minimal cadence for arm-only handedness, labeled:

| arm | SYNC G1 | SYNC G2 | SYNC G3 | sequential G1 (all 6 orders) | sequential G2/G3 |
|---|---|---|---|---|---|
| (MASK,PAUSE) | none (n ≤ 6) | 3 | 3 | 4 | 4 |
| (PAUSE,PAUSE) | none | 3 | 3 | 4 | 4 |
| (PAUSE,MASK) | none | 3 | 3 | 5 | 4 |
| (MASK,MASK) | none | none | none | none | none |

Sequential arm-only totals, labeled, G1 / G2 / G3 (range over the six orders):
(MASK,PAUSE) 40–44 / 77–84 / 83–89; (PAUSE,PAUSE) 36–40 / 61–71 / 65–74;
(PAUSE,MASK) 4–12 / 32–44 / 36–47; (MASK,MASK) 0 / 0 / 0.

Mechanism, from a hand-checked example (`tests/test_dynamics.py`):
`DRR` with phases (0, 1, 2) under (PAUSE,PAUSE). L closes the loop. In LR,
the first handoff A->C pauses both A and C, which puts C on B's phase, so C->B
can never fire. Under CONTROL both itineraries close. A pause can lock two
entities onto the same phase, and which pair gets locked depends on the
direction of the loop.

## Stage 3 — verdicts by schedule

A verdict is "nonzero" if the count summed over cadences is above zero. An arm
is flagged schedule-dependent when any sequential order gives a different
verdict from SYNC. Full table: `results/tables.md`.

| reading | flips |
|---|---|
| Stage 1, all arms, all groups, both readings | none |
| Stage 2 as specified, all arms, all groups, both readings | none (every arm, CONTROL included, is nonzero under every schedule) |
| S2-DIFF, labeled, G1: (MASK,PAUSE), (PAUSE,PAUSE), (PAUSE,MASK) | **zero under SYNC, nonzero under all six sequential orders. Flagged schedule-dependent.** |
| S2-DIFF, G2/G3 (either reading), and G1 positional | none |
| S2-DIFF, (MASK,MASK) and CONTROL | none (zero everywhere) |

## The six readings

1. **CONTROL must be exactly zero.** Stage 1: yes, CONTROL is 0 in every
   cadence, group, reading and schedule (0/1550 each). Stage 2: no.
   CONTROL is handed in 1156/1546 (G1), 818 (G2) and 802 (G3) configurations
   under SYNC. I did not treat this as a harness fault, and changed nothing in
   the harness or the rules. I derived it by hand before running and recorded
   it in README with the example `DRR, (0, 0, 1)`: L blocks on its first
   transaction, while LR fires two. A test now pins that example. The cause is
   the rule that only the head of the protocol may fire, combined with
   comparing L and LR at the same configuration: they start with different
   transactions, so CONTROL itself already differs between them. **So Stage 2,
   as specified, fails its own precondition and cannot be read per the plan.**
   I log the proposed change as the separate S2-DIFF reading, which compares
   each arm with CONTROL configuration by configuration. It was predeclared,
   not substituted.
2. **Negative result?** No. In the unseen region (everything except Stage 1 /
   SYNC / G1 / n=3–5), (MASK,PAUSE) and (PAUSE,MASK) are nonzero in Stage 1 at
   every cadence 4–8, in every group and under both schedules.
3. **Only the unequal arms?** In Stage 1, yes. Only (MASK,PAUSE) and
   (PAUSE,MASK) are nonzero, so in the two-entity exchange order asymmetry
   depends on giving and receiving being delayed differently. This is a
   dependency, not a verdict. Stage 2 under S2-DIFF does not follow that
   pattern: (PAUSE,PAUSE) also adds handed configurations, and only
   (MASK,MASK) adds none. In the closed loop the dependency is on a PAUSE
   being present, not on unequal treatment.
4. **Survives under G3?** Yes. Stage 1 counts are identical under G1, G2 and G3
   (574/1550 SYNC, 142/1550 sequential), so the inequivalence needs no
   assumption that donor/receiver exchange is unlawful. S2-DIFF also survives
   G3 (G3 arm-only counts are equal to or slightly above G2).
5. **Stage 2: can a closed loop of achiral entities be handed from order
   alone?** As specified the stage cannot answer this, because CONTROL is
   handed from cadence 3 (reading 1). Under S2-DIFF, refractory-attributable
   handedness exists under G2 and G3 at minimal cadence 3 for (MASK,PAUSE),
   (PAUSE,PAUSE) and (PAUSE,MASK) under SYNC. It never appears for
   (MASK,MASK). Under G1 with the labeled reading it does not appear under
   SYNC (n ≤ 6) and appears from cadence 4 ((MASK,PAUSE), (PAUSE,PAUSE)) or 5
   ((PAUSE,MASK)) under sequential update.
6. **Schedule dependence.** No arm's verdict flips in Stage 1 or in Stage 2 as
   specified. Under S2-DIFF, G1, labeled, (MASK,PAUSE), (PAUSE,PAUSE) and
   (PAUSE,MASK) flip from zero (SYNC) to nonzero (every sequential order), so
   they are **flagged schedule-dependent for that reading**. Magnitudes depend
   strongly on schedule even where verdicts do not: in Stage 1 the count drops
   from 574 to 142, with 509 configurations flipping one way and 77 the other.

## Prior information: reproduced or not

Stage 1, cadences 3–5, G1, SYNC:

| figure | source | this run (labeled) | this run (positional) | reproduced? |
|---|---|---|---|---|
| (MASK,PAUSE) 40/94 | 5 Oct 2026 pre-check | 40/94 | 40/94 | **yes** |
| (PAUSE,PAUSE) 0/94 | 5 Oct 2026 pre-check | 0/94 | 0/94 | **yes** |
| CONTROL 0/94 | 5 Oct 2026 pre-check | 0/94 | 0/94 | **yes** |
| (MASK,PAUSE) 55/94 | source document, implementation not on record | 40/94 | 40/94 | **no** |

Nothing was adjusted toward any of these figures, and I did not search for an
implementation that gives 55. The 40 inequivalent pairs are listed in
`results/results.json` (`stage1_inequivalent_configs_SYNC_G1_labeled`). Most
have `d = 1` or `d = n − 1`. The exceptions are `CDCRR` and `CDDCR` at
`d = 2, 3`.

## Planted failures

| planted failure | caught? |
|---|---|
| chiral word `RDC` in a word set | yes: `validate_word_set` raises |
| CONTROL with an injected order-dependent fault | yes: Stage 1 count becomes nonzero under G1 and G3 |
| hand-built order-inequivalent configuration (`DRR`, d = 1, (MASK,PAUSE)) | yes: detected under every group and reading |
| reversal without remapping phases | yes: configuration-orbit counts change, and a record verdict changes. In the full run it also changes Stage 2 G2 counts (e.g. CONTROL 818 → 1156, (MASK,PAUSE) 1066 → 1156). It does not change Stage 1, where G2 adds nothing beyond G1. |

## Log of everything done after the predeclaration commit

* Two test expectations were wrong and were corrected before any stage ran
  (commit after `c4ed7ac`). I had mis-traced `DRR` at phases (1, 0); the
  offset there is 2, not 0. I had also wrongly expected the buggy reversal's
  orbits to equal G1's; it is not a group action. The harness was not changed.
* After the first full run I added the Stage 3 verdict table to the runner.
  This implements reporting item 3 as already predeclared in README. No rule,
  comparison or reading changed, and the rerun reproduced every count.
* A helper function was renamed (`representative`, for the least rotation of
  a word) to keep a forbidden word out of the code. A full rerun gave
  byte-identical results apart from runtime.
* Two hand-checked Stage 2 tests were added after the run: the pre-run CONTROL
  example and the (PAUSE,PAUSE) phase-lock example above.

## Not tested

* Out of scope by design: replacement tolerance, orientation return, burden,
  where the refractory rule comes from, and any mapping to known physics.
* Cadences above 8 (Stage 1) and above 6 (Stage 2). The G1 S2-DIFF "none"
  under SYNC holds only for n ≤ 6.
* Schedules other than SYNC and the fixed sequential orders: no random,
  asynchronous or per-step-varying orders.
* Refractory lasting more than one step, or mixed treatments within one arm.
* Protocols other than O1/O2 and L/LR. In particular, cyclic rotations of the
  itinerary's starting transaction, which bear directly on the Stage 2
  blocking issue.
* Unit holdings. The handoff is conservative by rule and nothing depends on
  holdings, so they are not tracked.
* Any alternative Stage 2 comparison other than S2-DIFF.
