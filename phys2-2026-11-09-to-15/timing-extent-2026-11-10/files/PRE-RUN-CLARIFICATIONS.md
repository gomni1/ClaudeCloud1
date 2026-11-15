# Pre-run clarifications — TIMING-EXTENT-TRADE v3

Written 10 Nov 2026, before any task simulation was run. (A preflight spot-check of two v2 gates was run earlier the same day; its numbers informed v3 and are not task results.)

None of these changes a candidate rule, an event, a measure, the grid or a label threshold. Each fixes a reading the v3 prompt left open. They are recorded here so they cannot be chosen after seeing results.

C1. Multiplicity in P5 and P6. v3 says "within 5% or 3 standard errors, whichever is larger" for every cell. With K independent tests, about 0.0027·K are expected to exceed 3 standard errors by chance (K is in the hundreds to thousands). Reading fixed here: the check passes if (a) no test exceeds 5 standard errors and 5%, and (b) the number exceeding 3 standard errors and 5% is at most the 99.9th percentile of Binomial(K, 0.0027). Every exceedance is listed. This is a change to the literal wording of v3 and is flagged as such in the note.

C2. Window status is decided on the full cell (both seed halves together). The two halves then use the same in-window cell set. The "at least 50 completers" rule applies to the full cell.

C3. Standard errors. For a variance estimate from n values, SE = sqrt((m4 − s⁴)/n) with m4 the sample fourth central moment.

C4. Ev-A extents are taken over all realisations of the cell. Ev-B extents are taken over completers and, separately, over all.

C5. Single unit. Simulated as one primitive with no separate organisation variable. This is E1 for across-realisation statistics.

C6. Simulation scheme.
 - Single unit: exact event-driven (exponential dwell times, exact crossing times).
 - Ensemble: substeps with (max total rate per primitive × dt) ≤ 0.1, where the total rate includes the copy rate c. Within a substep each primitive's state is advanced with the exact two-state transition probability given the organisation state at the start of the substep; displacement uses the trapezoid of start and end states; the crossing time is interpolated linearly within the substep. The ensemble code is checked against the exact single-unit code at N = 1 before use.

C7. Completion is the first time the pattern displacement is ≥ D.

C8. P6 "allowing for truncation": each simulated in-pulse variance is divided by the exact truncated variance for that τ (from Q1) before comparing across τ.

C9. P1 runs the null on the single-unit m = 0.2 grid with the full 4000 realisations per cell and both L.

C10. Verdict pooling. The verdict per (event, axis, inheritance, ensemble candidate) pools all of its strata, including all extent types, as v3 states. The split by extent family (across, within) is also reported. E3 pools ρ = 0.5 and ρ = 0.9, with the split by ρ also reported.

C11. Relaxation. The mean step is pooled over all τ cells of the same (m, η, class, N, ρ) that satisfy τ ≥ 5/(a_d + b_d), to reduce noise.

C12. Q5 ticks. One tick is one unit of time. Each tick the unit steps by its state (±1), then flips with probability 1 − exp(−rate). Pre-roll is 5/m ticks at rest. Completion is the first tick at which displacement ≥ D. Grid: m = 0.2, boost, the η values with every rate ≤ 1 (η ≤ 1.5), all ten τ, both L, both inheritances, 4000 realisations. Under H-realised the inherited rates are capped by the same rule: a realisation whose inherited rate exceeds 1 has that rate set to 1 and the count of such realisations is reported.

C13. A stratum whose Δx or Δt is constant across its in-window cells (Spearman undefined) is UNCLASSIFIED.

C14. Seeds. Cell seed = 20261110·1000003 + 2·(cell index) + (half: A = 0, B = 1), through numpy SeedSequence. The cell index is the row number in the cell table saved beside the note.
