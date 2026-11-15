# Jev claim-ledger report — TIMING-EXTENT-TRADE-2026-11-10

Run 10 Nov 2026 from `~/GENERAL/phys2-claim-ledger`, `--model jev-1.13.0`, on the note as first drafted. 89 claims judged. Full machine output: `jev-ledger-summary.json` (beside this file) and `ledger-out-timing-extent/` in the ledger folder.

The ledger classifies statements about the model. It does not judge the physics, the derivations or the numbers.

## Censuses

- Register: effective 53, not a physical claim 24, observational 11, native 1.
- Result class: generative 32, structural 23, discriminating 14, not a result 13, hygiene 7. Known weak spot: hygiene is undercounted by this battery.
- Rung: mechanism 56, instrument 22, programme 8, none 3.

## Flags

- Register violations: 0. Particle-register language in mechanical text: 0.
- RA1-dependent: 0. A3-dependent: 0. Duplicate-finding candidates: 0.
- Promotion language: 4, all weak (0.62 to 0.82).
  - #0001, the opening verdict sentence (0.64). Changed: now scoped to "this grid and these candidates".
  - #0040, the Ev-B infimum row with "A proved" (0.82). Kept: "A proved" is the classification letter the task requires, and the proof is the explicit limit given in the row.
  - #0085, the Q5 summary row (0.62). Changed: scoped to the single-unit model.
  - #0086, the Q6 summary row (0.70). Kept: it says the result is true by construction and is not credited to the model.
- Anti-fitting: 1 (#0086 again, 0.64). Kept for the same reason; the sentence is the anti-fitting disclaimer itself.
- Wording exceeds evidence, score 2.0 or above: 29. Acted on 15 of them by adding scope ("in this model", "on this grid", "found", "argued, not proved"):
  - the plain-words openers of Q1, Q2, Q3, Q4 and Q5;
  - the Q4 comparison with the pointer, which now says it is the pointer as the task prompt describes it and that the paper was not read;
  - the Q7 shaped-gap paragraph ("must" to "would have to"; the closing sentence no longer claims a general impossibility);
  - four of the five load-bearing flags;
  - the Q3, Q4, Q5 and Q7 summary rows.
  The other 14 are limits statements, definitions, formula lead-ins, number lines and citations (#0008, #0010, #0022, #0027, #0034, #0041, #0048, #0053, #0054, #0068, #0069, #0070, #0081, #0040). I left them as written.
- High insertion risk: 30. Not acted on: this score is known to fire on definitions and formula lines.
- Negative results counted: 26.

## Limits of this report

The battery was run once, on the first draft. The note was edited afterwards as listed above and was not re-run, to avoid a second charge. So the counts describe the draft, not the saved text.
