# Night run steering

Glenn's lines. The night run reads this file before building its queue and obeys it.
One item per line. Leave a section empty if there's nothing to say.

## PIN — work these next (in order, ahead of anything the run would choose)
- Decision run on the five closed levels with no stable balance, depth D3: take the 5 draws from the 11 Nov closed-level sweep in which all three balances are unstable (Night report 11 Nov, item 2) and run each long enough to say how it ends. Before the run, specify the rule that classifies an ending and show on planted cases (a known steady cycle, a known damped swing that rests, a known rest) that it can return each answer at the run length used. Report one of: steady cycle; other sustained motion (describe it); unresolved. If any of the five cycles steadily, report period and size of swing and what the five draws have in common. If none does, record 'a single closed level cannot tick' as the result. Target: the emergent-period conjecture.
- [done 10 Nov — not to be re-run] Stability of the three balances, depth D3: for kr ≥ 2 on an open level of the working grammar (full four-role system), is the middle balance always unstable and the outer two stable? Start from the reduced V-equation with C, L and P pinned and test whether the sign of the Jacobian determinant at a balance tracks −g′(V*). Targets: 'One level holds at most three balances under threshold recruitment' and the gap 'Does a species' attractor drift in the working grammar?'. (Night report 9 Nov, §7 and the second §8 handoff.)
- [done 10 Nov — not to be re-run] 'Growth depletes the rung beneath', depth D2: specify the smallest two-way resource coupling between two levels consistent with 'Shared supply within aggregate capacity; each unit counted once' and the ladder principle, in which the upper rung's uptake appears as a loss or exclusive commitment in the lower rung's balance and binds when the lower rung's capacity binds. Specification only; no run. (Night report 9 Nov, item N-4.)

## SKIP — do not touch for now
- Stop rule (11 Nov): once the five-level decision run above has reported, no further single-level stability work — no new random-draw sweeps, balance classifications or stability surveys on one level, open or closed — unless Glenn pins one here. The run does not queue these on its own.

## RETIRED — judged dead; never bring back
<!-- e.g. - Free random swap -->

## NOTES — anything else for tonight
- Spec v2 (9 Nov) applies: receipts uploaded with hashes, planted failures guaranteed analytically, bound checks while the solver runs.
- After the five-level run (11 Nov): if a level ticks, the next step follows from what the five share. If none ticks, work moves to coupling between levels, using only the smallest term — the one that lets the lower rung start the upper one — not the full 11 Nov item-3 construction, which removes the upper rung's 10 Nov formation condition by how it is built.
