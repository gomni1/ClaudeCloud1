# PHYS2 order test — SANDBOX/DRAFT

Status: SANDBOX/DRAFT. Nothing here is promoted.

Question: in a one-class, reversal-symmetric capture/release grammar, does
refractory succession make the outcome depend on the order of transactions,
compared with an otherwise identical commuting control?

Python 3, stdlib only.

```
PYTHONPATH=src python3 -m unittest discover -s tests -v   # tests
PYTHONPATH=src python3 -m phys2_order.run                  # experiment -> results/
```

This README was committed **before any stage was run**. The rules below are
the rules as implemented. Results are in `RESULTS.md` and `results/`.

## Layout

| file | content |
|---|---|
| `src/phys2_order/words.py` | words, rotation / reversal / exchange, class counts, validation anchors |
| `src/phys2_order/dynamics.py` | succession, handoffs, refractory arms, cycle detection |
| `src/phys2_order/relabel.py` | the relabelling groups G1, G2, G3 and brute-force equivalence |
| `src/phys2_order/stages.py` | Stage 1, Stage 2, sequential schedules (Stage 3) |
| `src/phys2_order/run.py` | the predeclared run; writes `results/results.json`, `results/tables.md` |
| `tests/` | unit tests, hand traces, planted failures |

## Grammar as implemented

**Words.** A word `W` is a string over `{R, D, C}`, cadence `n = len(W)`, read
cyclically. Conventions:

* `rot(W, k)[i] = W[(i + k) mod n]`
* `rev(W)[i] = W[(-i) mod n]` (cyclic reversal)
* `swap_rd(W)`: every R becomes D and every D becomes R; C is unchanged.

A word is *achiral* if `rev(W)` equals some `rot(W, k)`. The word set for a
cadence is every rotation class that is achiral and contains at least one R
and one D, represented by its lexicographically least rotation (`C < D < R`
in character order). `validate_word_set` rejects a chiral word, a word without
R or without D, a foreign letter, or two words from one rotation class.

**Entities.** Every entity in a run has the same word. Entity `i` has a phase
`p_i` (mod n) and a refractory mode. It *shows* `W[p_i]`, or `C` while its
refractory mode says so.

**Instants and schedules.**

* `SYNC` (default): one instant per step. Every entity advances once between
  consecutive instants.
* Sequential order `(i0, i1, …)` (Stage 3): there is an instant before any
  advance and one after every single advance; entity `order[sub]` advances
  next, cycling. A *step boundary* is an instant with `sub = 0`.

**Transactions.** `X->Y` *fires* at an instant where X shows D and Y shows R.
It is a conservative handoff of one unit; the unit itself is not tracked
because nothing in the rules depends on holdings.

**Protocols.** An ordered list of intended transactions. At each instant only
the head of the list is checked; if it fires, the head moves on. At most one
transaction fires per instant. (In every protocol used here, consecutive
transactions share an entity in opposite roles, so a second firing at the same
instant is impossible; the simulator raises `HarnessError` if it ever could,
which makes the convention immaterial.)

**Refractory.** When a transaction fires, its donor gets the arm's donor
treatment and its receiver the arm's receiver treatment. A treatment takes
effect at that entity's *next own advance*:

| treatment | at the next own advance | until the following own advance |
|---|---|---|
| `MASK` | phase moves on by 1 as usual | shows C |
| `PAUSE` | phase does not move | shows C |
| `NONE` (CONTROL) | normal advance | normal |

At the following own advance the entity advances normally and shows its word
again. Until the next own advance after a firing, the entity keeps showing the
letter it fired with. Under `SYNC` this is exactly: MASK = "shows C on the
next step, phase still advances"; PAUSE = "holds its phase for one extra
step, showing C during that step". A second firing on an entity before its
next own advance raises `HarnessError` (it cannot happen with these protocols).

**Arms (donor, receiver).** `(MASK,PAUSE)`, `(PAUSE,PAUSE)`, `(MASK,MASK)`,
`(PAUSE,MASK)`, and `CONTROL = (NONE,NONE)`.

**Termination.** The state before each check, `(phases, modes, head index,
sub)`, determines everything after it. The run stops at the first repeated
state. The stretch from its first occurrence is the *terminal cycle*. "Never
fires" is read off the cycle (the head index is constant on it); there is no
step cutoff. On the terminal cycle there are no firings and every mode is
normal; the simulator checks both.

## Outcome signature

For one run the simulator returns:

* `fired`: one boolean per protocol position;
* `terminal`: the set of phase tuples at step boundaries on the terminal cycle;
* `offsets`: `(p_i − p_0) mod n` on the terminal cycle (it is constant there;
  checked).

The terminal cycle is always free-running, so it is the same information as
the final offsets "once both are out of refractory" when everything fired, and
it *is* the terminal cycle when something never fires. One representation
covers both cases in the specification.

The **record** compared between two runs is `(word, fired, terminal)`, where
`word` is the concrete string. Two readings of `fired` are predeclared:

* **labeled (primary):** the set of `((donor, receiver), fired?)` over the
  intended transactions. The order in which they were intended is dropped;
  which transactions happened is kept with their labels. Reason: relabellings
  are specified as acting on transactions (G3 swaps donor and receiver; entity
  permutations rename them), and the Stage 2 signature is "which transactions
  fired". The order is the factor under test, so it is not part of the outcome.
* **positional (sensitivity, reported alongside):** the tuple
  `(first fired?, second fired?, …)` read by protocol position; entity
  permutations and exchange do not touch it.

## Lawful relabellings and their exact action

A relabelling is `g = (perm, k, rev, xch)`, applied as
`P_perm ∘ Rot_k ∘ Rev^rev ∘ X^xch` (X first). Every element of each group has
exactly one such normal form, so looping over all four components enumerates
the group. Action on each part of a record or configuration:

| relabelling | word | phases / offsets | protocol (ordered list) | outcome (labeled `fired`) | outcome (positional `fired`) | terminal set |
|---|---|---|---|---|---|---|
| entity permutation `P_perm` | unchanged | entity `i`'s phase moves to entity `perm[i]`; offsets are recomputed from the moved phases (for two entities, `pB − pA → −(pB − pA)` under the swap) | `X->Y` becomes `perm[X]->perm[Y]`, list order kept | keys renamed the same way | unchanged | each tuple permuted the same way |
| rotation `Rot_k` | `rot(W, k)` | every `p → p − k` (offsets unchanged) | unchanged | unchanged | unchanged | every phase `p → p − k` |
| reversal `Rev` | `rev(W)` | every `p → −p` (so every offset `δ → −δ`) | unchanged | unchanged | unchanged | every phase `p → −p` |
| exchange `X` | `swap_rd(W)` | unchanged | `X->Y` becomes `Y->X`, list order kept | each key `(X, Y) → (Y, X)` | unchanged | unchanged |

Rotation and reversal keep the letter each entity shows: `rot(W,k)[p−k] = W[p]`
and `rev(W)[−p] = W[p]` (tested). Exchange turns every shown R into D and back.

Groups (entity permutations of identical entities are always included):

* **G1** = {permutations} × {rotations}
* **G2** = G1 + reversal
* **G3** = G2 + exchange

Group sizes: `k! · n`, `2 · k! · n`, `4 · k! · n` for `k` entities.

**Equivalence.** Records `r1` (from the first protocol) and `r2` (from the
second protocol, same starting configuration) are equivalent under G iff some
`g ∈ G` gives `g(r1) == r2` exactly: same concrete word, same `fired` data,
same terminal set. This is checked by enumerating every element of G. Because
the word must come back to the same concrete string, rotations contribute only
through the word's own period, reversal only together with the rotation that
undoes it (every word here is achiral), and exchange only when `swap_rd(W)` is
a rotation or rotated reversal of `W`. The relabelling acts on the starting
configuration and protocol in the same way (`apply_to_configuration`,
`apply_to_protocol`); the dynamics are never run backward.

## Stages

* **Stage 1.** Entities A, B (indices 0, 1); phases `(0, d)`, `d = 0..n−1`;
  `O1 = (A->B, B->A)`, `O2 = (B->A, A->B)`. A pair `(W, d)` is
  *order-inequivalent* under G if the O1 record and the O2 record are not
  equivalent under G. Cadences 3..8.
* **Stage 2.** Entities A, B, C; phases `(0, d1, d2)` for all `d1, d2`;
  `L = (A->B, B->C, C->A)`, `LR = (A->C, C->B, B->A)`. A configuration is
  *handed* under G if the L record and the LR record are not equivalent under
  G. Cadences 3..6. Minimal cadence with a handed configuration is reported
  per arm and group.
* **Stage 3.** Stages 1 and 2 repeated under every fixed sequential order
  (2 orders for two entities, 6 for three). The schedule is not relabelled
  (both protocols of a comparison run under the same order, and the record
  holds step-boundary states only).

## Predeclared reporting, fixed before the run

1. Counts and fractions per arm × group × cadence × schedule, for both
   signature readings; labeled is primary.
2. **Prior pre-check:** Stage 1, cadences 3–5, G1, SYNC — reproduced or not for
   `(MASK,PAUSE)` 40/94, `(PAUSE,PAUSE)` 0/94, `CONTROL` 0/94, and the source
   document's 55/94. No rule or reading is adjusted toward any of these.
3. **Stage 3 verdict:** for each stage × arm × group, the verdict is "zero" or
   "nonzero" summed over all cadences. An arm is flagged *schedule-dependent*
   if any sequential order changes that verdict relative to SYNC.
   Configuration-level flips are also reported.
4. **Unseen region:** every cell except Stage 1 / SYNC / G1 / cadences 3–5.

### Issue identified before running: Stage 2 CONTROL

Reading 1 requires CONTROL to be zero everywhere. Working the rules by hand
before running anything shows that **Stage 2 CONTROL cannot be zero under the
comparison as specified**, and that this comes from the rules, not the
harness:

* Under CONTROL the phases free-run, so a transaction `X->Y` can fire iff
  `a(p_Y − p_X)` holds, where `a(δ)` = "some phase t has `W[t] = D` and
  `W[t+δ] = R`". For an achiral word `a(δ) = a(−δ)`.
* Only the head of a protocol may fire, so a blocked first transaction blocks
  the whole itinerary. L starts with A->B (needs `a(d1)`), LR starts with A->C
  (needs `a(d2)`).
* Example: `W = DRR`, phases `(0, 0, 1)`. A and B always show the same letter,
  so A->B never fires and L fires nothing. LR fires A->C and C->B and then
  blocks on B->A. The fired counts differ (0 vs 2), so no relabelling can
  match them: this configuration is handed under CONTROL in every group.

In Stage 1 this does not arise: both orders contain the same two transactions
with conditions `a(d)` and `a(−d)`, which are equal for achiral words, so
CONTROL is zero by construction there.

Following the instruction to finish the run as specified and log any proposed
change separately:

* Stage 2 is run and reported **exactly as specified** (L vs LR at the same
  configuration). A nonzero Stage 2 CONTROL is reported as a property of the
  specification. It is checked against the hand example above, not "fixed".
* **Supplementary statistic S2-DIFF (predeclared here, separate from the
  specified reading):** for each configuration, compare the arm's verdict with
  CONTROL's verdict at the same configuration, schedule, group and signature
  reading. Report *arm-only* (handed under the arm, not under CONTROL),
  *control-only*, and *both*. The minimal cadence for S2-DIFF uses arm-only
  counts. This is the reading that matches the stated goal ("compared with an
  otherwise identical commuting control"). It is a proposed separate reading,
  not a replacement.

## Validation anchors (checked before any stage runs; the runner aborts on mismatch)

| cadence | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| rotation classes | 11 | 24 | 51 | 130 | 315 | 834 |
| rotation + reversal classes | 10 | 21 | 39 | 92 | 198 | 498 |
| rotation classes ≠ own reversal | 2 | 6 | 24 | 76 | 234 | 672 |

Achiral words containing R and D, cadences 3–5: 21 words, 94 `(word, offset)`
pairs. All are computed by brute-force enumeration of the `3^n` strings.

## Planted failures (tests)

| planted failure | test |
|---|---|
| chiral word `RDC` slipped into a word set is rejected | `test_words.WordSet.test_planted_chiral_word_rejected` |
| CONTROL with an injected order-dependent fault (the first transaction of any protocol pauses its receiver) is flagged nonzero | `test_dynamics.PlantedControlBug.test_injected_bug_is_flagged` |
| hand-built order-inequivalent configuration (`DRR`, d = 1, `(MASK,PAUSE)`: O1 fires one transaction, O2 fires two; traced by hand) is detected | `test_dynamics.PlantedInequivalence.test_hand_built_configuration_detected` |
| reversal implemented without remapping the phases changes counts | `test_relabel.PlantedRelabelBug.*` (configuration-orbit counts and a record verdict change) |

## Out of scope (named gaps, not pursued)

Replacement tolerance; orientation return; burden; where the refractory rule
comes from; any mapping to known physics.
