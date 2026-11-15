# Night run steering

Glenn's lines. The night run reads this file before building its queue and obeys it.
One item per line. Leave a section empty if there's nothing to say.

## PIN — work these next (in order, ahead of anything the run would choose)
- Decision run on the five closed levels with no stable balance, depth D3: integrate draws 2045, 301417, 384616, 456280 and 616482 of the 11 Nov closed-level sweep (seed 20261111; rates regenerated with N-2026-11-11-2-num.py, as in Night report 11 Nov §7, first follow-up) and say how each one ends. Before the run, specify the rule that classifies an ending, built as that report's §7 'sounder classifier' describes (rest judged by the residual and a contraction check, not by distance to a balance at a fixed time), and show on planted cases (a known steady cycle, a known damped swing that rests, a known rest) that it can return each answer at the run length used. Report for each draw one of: steady cycle; other sustained motion (describe it); settles at an edge state that is not one of the three balances (say which); unresolved. For a steady cycle, give period, size of swing and Floquet multipliers. Then say what the five draws have in common. A negative result is about these five draws only; do not state it as 'a closed level cannot tick'. Target: the emergent-period conjecture.

## SKIP — do not touch for now
- Stop rule (11 Nov, in force from tonight): apart from the PIN above, no single-level stability work — no new random-draw sweeps, balance classifications, censuses of outer instability or stability surveys on one level, open or closed — unless Glenn pins one here. This covers follow-ups carried over from earlier reports as well as anything the run would choose itself.

## RETIRED — judged dead; never bring back
<!-- e.g. - Free random swap -->

## NOTES — anything else for tonight
- Spec v2 (9 Nov) applies: receipts uploaded with hashes, planted failures guaranteed analytically, bound checks while the solver runs.
- Done on 10 Nov, not to be re-run: the two 9 Nov PINs ('Stability of the three balances', D3, and 'Growth depletes the rung beneath', D2). Their full wording is in SUPERSEDED-2026-11-11-STEERING.md.
- Coupling between levels: if it is worked, use only the smallest term — the one that lets the lower rung start the upper one (Night report 11 Nov §7, 'minimal C_seed revision') — not the full 11 Nov item-3 construction, which removes the upper rung's 10 Nov formation condition by how it is built.
- What follows the five-level run is Glenn's call at review. His current lean: if a level ticks, look at what the five share; if none does, move to coupling between levels.
