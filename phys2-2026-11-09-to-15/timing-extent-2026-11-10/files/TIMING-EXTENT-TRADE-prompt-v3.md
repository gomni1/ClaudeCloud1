PHYS2 WORK TASK — Timing–extent trade: does sharper timing cost extent? (v3, 10 Nov 2026)

READ FIRST
Read PHYS2-STANDING-CONSTRAINTS.md in the AUDIT OUTPUTS folder on Google Drive before anything else. Where it and this prompt disagree on a constraint, it wins. If it records this question as closed or forbidden, stop and report that.

RUNG NOTE (confirmed by Glenn, 10 Nov 2026)
The active rung is the composite rung, and this task works below it (primitives with a two-state alphabet and a copy rule). It is issued as a targeted, finite descent: one question, fixed candidates, no follow-on work at this level. Return to the composite rung when it is answered. If this note has been deleted, stop and ask before starting.

CONTEXT (self-contained)
PHYS2 is a candidate foundational model built from minimal relational principles and tested against observation. Working picture: a particle is a persistent pattern of turnover, with identity kept through replacement. Rest is balanced turnover. Motion is displaced reorganisation of the whole pattern. There are only discrete steps, and continuum mathematics is bookkeeping. Every process is ensemble behaviour of very many substrate primitives, and the handoff is statistical. A model's own accounting is never a requirement on the mechanism. Register: effective (time, site, speed and energy may be used as internal descriptions). Every comparison with measurement is labelled OBSERVATIONAL.

OBSERVATIONAL POINTER (guides the search; not a target; nothing is fitted to it)
Maier et al., "Tracking electrons at the space-time limit", Nature Photonics 2026, doi 10.1038/s41566-026-01932-0. Quantum mechanics has no position–time uncertainty product. Even so, confining an electron wave packet more tightly in time required more energy and widened it spatially, and the electron followed the driving field after a lag of about 500 as. The trade runs through energy.

ESTABLISHED INPUTS (do not re-derive)
R1-clock with ab = m², a = m e^(−η), b = m e^(η): v = tanh η, E = (a + b)/2 = m cosh η, p = (b − a)/2 = m sinh η, E² − p² = m². The stationary reversal rate is m√(1 − v²).

THE QUESTION
In PHYS2 step dynamics, when a pattern's reorganisation is made sharper in time, must its spatial extent grow? If it must, is there a FLOOR (a positive infimum of timing width × extent over the admissible range), or only a TENDENCY? Or do timing and extent shrink together under drive (CO-SHRINK)?

METHOD ORDER
The analysis (Q1, Q2) is the primary method. The grid is confirmation of the analysis and a search for anything it missed. It is not a sweep in search of a result.

CANDIDATE RULES (fixed before you start; do not alter them after seeing results)
R1, step balance. Every elementary displacement is a unit step at the maximal rate (speed 1). Velocity is the mean step. Rest is balanced stepping.
R1-clock (1D). A pattern alternates forward and backward stepping. It switches forward→backward at rate a and backward→forward at rate b. ab = m² is the pattern's invariant.
Time. Simulate in the continuous-time bookkeeping limit: exact event-driven, or substeps with (max rate × dt) ≤ 0.1. Declare which. Q5 is the separate discrete-tick check.
Ensemble realisation. An organisation state σ_org ∈ {+1, −1} runs R1-clock at the organisation's current rates. Each primitive i has a state σ_i ∈ {+1, −1}. It flips independently at its own current rates, and it copies σ_org at rate c = ρ·E_org/(1 − ρ), where E_org = (a + b)/2 of the organisation's current rates (the drive rates during the pulse, its inherited rates after). Three named candidates:
 E1: ρ = 1 (σ_i ≡ σ_org, the whole organisation steps together).
 E2: ρ = 0 (independent primitives).
 E3: 0 < ρ < 1.
Pre-roll. Run at rest (a = b = m) for 5/m time units before drive onset, then set all positions to 0. Drive onset is t = 0. The rest-state start (half the states stepping backward at onset) is part of the candidate, not a nuisance: do not replace it with a drive-stationary start.
Drive. A pulse of length τ with rates a_d = k·m·e^(−η), b_d = k·m·e^(η), so E_d = k·m·cosh η and p_d = k·m·sinh η. Three drive classes: boost (k = 1), excite-2 (k = 2), excite-4 (k = 4).
Inheritance after the pulse (two candidates, both run):
 H-nominal: the organisation and every primitive continue at a' = m e^(−η), b' = m e^(η). The pattern keeps the momentum it was given.
 H-realised (NEW CANDIDATE, labelled as one, fixed here before any run): every primitive, and the organisation, continues with a'b' = m² and its own bias η_i = artanh(v_i). Here v_i = (T_f − T_b)/(τ + 1/E_d), where T_f and T_b are the times it spent stepping forward and backward during the pulse.

DECLARED CONVENTIONS (measurement choices, not PHYS2 results)
The thresholds below (0.6, 0.3, 95%, 5%, 75%, 50 completers), the 1/E_d regulariser in v_i and the form of the copy rate c are conventions fixed here so the task is executable. None is a PHYS2 result, and no verdict may be reported as depending on PHYS2 having chosen them. Where a label would change under a nearby value (0.5 or 0.7 for 0.6), say so beside the label. The verdict uses the declared values.

ADMISSIBLE RANGE (for every infimum)
A_free: m > 0, η > 0, k ≥ 1, τ > 0, D ≥ 1, L ≥ 0, N ≥ 1, ρ ∈ [0, 1], rates unbounded.
A_cap: A_free with every rate ≤ 1 (R1's maximal rate applied to switching). This cap is a declared convention; flag it wherever it carries a result.
Every infimum is reported over both, and separately in the limit N → ∞ at fixed other parameters. Grid cells with a rate above 1 are run and marked OVER-CAP in the tables.

EVENTS (both measured; the dynamics do not depend on D, so one run records every D)
Pattern displacement = the mean of constituent-lineage displacements. Do not use centroid-of-shape measurement. D ∈ {2, 4, 8, 16, 32}.
Completion = the first time the pattern displacement reaches D. Only completions during the pulse are used, for both events. A realisation that has not completed by pulse end is a non-completer and contributes no event time.
Ev-A, drive-timed: a cell is in window if ≥ 95% of realisations complete within the pulse. Otherwise it is CENSORED (KINEMATIC if τ ≤ D, since speed is 1).
Ev-B, window-gated: a cell is in window if the completion fraction lies in [0.05, 0.95] and there are at least 50 completers. Otherwise it is OUT OF WINDOW (THIN if it fails only the completer count).
Report the completion fraction for every cell.

MEASURES
Δt: the std of the event time over completers.
Extents, measured at lag L after the pulse ends (also report each at pulse end):
 Δx_across: the std over realisations of the pattern displacement. Defined for every N.
 Δx_within: the within-realisation std of constituent positions, averaged over realisations. Defined only for N ≥ 2 and ρ < 1.
 For Ev-B, compute each extent over completers and, separately, over all realisations. These are separate extent types.
Energy. Nominal: E_d and the post-pulse m cosh η. Realised: E_i = m/√(1 − v_i²) per constituent, with v_i as defined under H-realised (computed under both inheritances); ΔE is its std over constituents and realisations. Secondary: the realised reversal count per unit time during the pulse. The integral of a rate parameter is not a realised quantity.
Relaxation: the time from onset for the mean step (over realisations) to reach 1 − 1/e of the drive's stationary mean step tanh η. Measured only in cells with τ ≥ 5/(a_d + b_d).

GRID (declared. Any cell not run is reported NOT RUN with the reason. No cell is silently dropped.)
Single-unit controls (N = 1; E1 has the same across-realisation statistics): m ∈ {0.05, 0.2}; η ∈ {0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3}; all three drive classes; τ ∈ {4, 8, 12, 16, 24, 32, 48, 64, 96, 128}; L ∈ {16, 64}; both inheritances; 4000 realisations per cell.
Ensemble (E2, E3): m = 0.2; η ∈ {0.25, 0.5, 1, 1.5, 2, 3}; boost and excite-4; τ ∈ {8, 16, 24, 32, 64, 128}; L = 16; both inheritances; ρ ∈ {0, 0.5, 0.9}; N ∈ {16, 64, 256}; 1000 realisations at N = 16 and 64, 200 at N = 256.
Every cell is run as two independent halves (seed sets A and B, half the realisations each). Seeds fixed and recorded.

PRE-REGISTERED CLASSIFICATION
Two sweep axes. A stratum fixes everything except its axis variable.
 DRIVE axis: cells vary over η. Stratum = (event, m, D, N, ρ, inheritance, drive class, τ, L, extent type).
 WINDOW axis: cells vary over τ. Stratum = (event, m, D, N, ρ, inheritance, drive class, η, L, extent type).
Ev-A is classified on the DRIVE axis only: its Δt cannot depend on τ (see P6). Ev-B is classified on both axes.
Within each stratum, compute Spearman(Δx, Δt) across in-window cells. Never pool across strata. A stratum with fewer than 5 in-window cells is UNCLASSIFIED.
 TRADE: Spearman ≤ −0.6.
 CO-SHRINK (DRIVE axis only): Spearman ≥ +0.6, and both Δt and Δx have Spearman ≤ −0.6 against E_d.
 WINDOW-ARTEFACT (WINDOW axis only): Spearman ≥ +0.6. Both grow with the window; no trade.
 NONE: |Spearman| < 0.3.
 MIXED: anything else.
Stability. Each stratum is classified separately on halves A and B. If the two labels differ, the stratum is UNSTABLE and counts as unclassified.
FLOOR vs TENDENCY applies to TRADE strata only, and is decided by the analytic infimum of Δt·Δx (Q2, Q4), never by a grid minimum.
 FLOOR: infimum > 0 over A_free.
 STEP-SCALE FLOOR: infimum > 0 over A_cap only. Report it as a bound from the rate cap, distinct from a Regensburg-shaped trade.
 TENDENCY: infimum 0 over both.
 FLOOR-UNDECIDED: no analytic result.
 A constant that vanishes as L → 0 or as N → ∞ gives infimum 0; say which limit kills it.
 Numerical cross-check: in each TRADE stratum, report Spearman of the product against the axis variable. |Spearman| ≥ 0.6 alongside an analytic FLOOR is reported as CONFLICT, and the analysis is rechecked before anything is concluded.
Overall verdict per (event, axis, inheritance, ensemble candidate): the label held by ≥ 75% of its classified strata, with at least 4 classified strata; otherwise MIXED, or UNDECIDED if fewer than 4.
Single-unit strata (N = 1, E1) are reported as controls for the analysis. They are not PHYS2 verdicts and do not appear in the opening verdict.

INFRASTRUCTURE CHECKS (run first; any failure stops the task and is reported)
P1 NULL. Run the single-unit m = 0.2 grid with a drive that does not couple: (a_d, b_d) = (m, m) in every cell, cells still carrying their η and class labels, H-nominal with a' = b' = m.
 DRIVE axis: η is a dummy label. Across all classified strata, at most 2% may be labelled TRADE or CO-SHRINK.
 WINDOW axis, Ev-B: at least 90% of classified strata must be labelled WINDOW-ARTEFACT. This is the positive control for that label.
P2 PLANTED FLOOR: synthetic noisy cells with Δt·Δx = constant must classify TRADE, and FLOOR given the planted infimum.
P3 PLANTED TENDENCY: synthetic Δx ∝ Δt^(−1/2) must classify TRADE, and TENDENCY given the planted infimum 0.
P4 PLANTED CO-SHRINK: synthetic Δt, Δx ∝ E^(−3/2) on the DRIVE axis must classify CO-SHRINK.
P5 ANALYTIC. For every single-unit H-nominal cell that is in window for Ev-A, the simulated event-time variance, and Δx_across² at pulse end, must agree with the exact rest-start forms derived in Q1 and Q2, within 5% or 3 standard errors, whichever is larger. The asymptotic forms k²m²D/p_d³ and k²m²τ/E_d³ are reported as ratios beside the exact ones and are not gated: they hold only when many reversals occur during the passage. (Preflight, 10 Nov, unverified hint: with few reversals the rest start adds about 3/b_d² to the event-time variance, independent of D.)
P6 τ-INDEPENDENCE. For Ev-A, Δt at fixed (m, η, class, D) must agree across all in-window τ within 3 standard errors, after allowing for the ≤ 5% truncation. A failure means the event or censoring code is wrong.

QUESTIONS
For each: say what the result means in plain words first, then give the derivation or computation. Classify it as A proved, B refuted as stated, C blocked (say exactly what is missing), D not mathematical, or E external fact. Include code and its output for every numerical result.

Q1, timing (single unit). Derive the in-pulse completion-time distribution from the rest-state start, exactly or as a controlled asymptotic, and from it Δt for Ev-A. State where Δt ≈ k·m·√D/p_d^(3/2) holds and where the rest-start term dominates. For Ev-B, derive how Δt scales with τ and with the completion fraction.

Q2, GATE (single unit; E1 has the same across-realisation statistics). Derive Δx_across at pulse end and at lag L under both inheritances, from the rest-state start. Under H-realised, derive Var(v_i) as a function of (η, k, τ) and the post-pulse spread it produces. For each (event, axis, inheritance), prove or refute inf Δt·Δx_across > 0 over A_free and over A_cap. Expected, to be checked and not assumed: H-nominal with Ev-A is CO-SHRINK with infimum 0; H-realised with Ev-B on the WINDOW axis shows a trade by construction, because Var(v_i) falls roughly as 1/τ while Δt rises with τ, with a product proportional to L. Where Q2 settles a case, the matching grid runs are confirmation only. Say so, and say where the weight of the task falls instead.

Q3, the ensemble fork. Run E2 and E3. Classify Δx_within and Δx_across per stratum. Give the N-scaling of Δt, Δx_across and Δx_within at each ρ, and test N^(−1/2) at ρ = 0. State which quantities survive N → ∞ and what the question reduces to there. Report any TRADE that appears at intermediate ρ but is absent at both ends.

Q4, routing. For any TRADE, determine whether it runs through energy (timing set by the drive, extent set by realised ΔE), directly through the window, or is the sampling noise of a velocity estimated over a finite window. Report Spearman(Δx, ΔE) within strata, and the sign of the dependence of Δx on drive energy. Give the dependence of any floor constant on m, D, N, ρ and L.

Q5, step-scale check. Repeat the single-unit, m = 0.2, boost strata in discrete ticks: flip probability 1 − exp(−rate) per tick, and cells with any rate above 1 reported NOT ADMISSIBLE. Say whether discreteness alone produces a positive bound. Label any such bound a step-scale bound.

Q6, relaxation. The mean step obeys a linear equation, so the lag is expected to be 1/(2E_d) for every candidate here, by construction of the rate parametrisation. Confirm or refute that, including under E3 copying. OBSERVATIONAL, shape only: the lag shortens as drive energy rises. Because this is built into the parametrisation, it is not credited to the model as a recovered behaviour. Do not convert to attoseconds and do not compare numbers.

Q7, prior art and limits. Identify the prior art: Feynman's checkerboard; Gaveau, Jacobson, Kac and Schulman (1984); persistent random walks and the telegraph equation; counting-statistics bounds on event timing; any prior art for velocity-memory inheritance like H-realised. State plainly whether a real-probability telegraph process can produce a FLOOR of the Regensburg shape at all (the quantum floor comes from Fourier conjugacy of amplitudes). If it cannot, say what the minimal missing ingredient must do, as far as the structure fixes its shape (for example, signed or interfering handoff contributions). Log it as a shaped gap. Do not add it, and do not run it.

DISCIPLINE
- Rules, events, measures, grid, conventions and classification are fixed above. Do not tune anything. Do not drop cells. Do not add rescue terms after seeing results.
- H-realised is a new candidate, fixed before the run. If it fails, it is retired on the record, not amended.
- Schrödinger evolution, wavefunctions and ħ may appear only as labelled OBSERVATIONAL controls, never as explanation.
- Honest negatives are reportable results. If a candidate fails, say what failed, name the smallest assumption responsible, and say what survives. A revised rule may be offered as a new candidate, labelled as one, with the failure left on the record. It is not run in this task.
- A result that only restates how a quantity was constructed is reported as "by construction" and is not counted as a finding.
- No particle-register language in mechanical text.
- Flag any place where R1's step direction, the rest-state start, the ensemble realisation, the rate cap or the inheritance rule is doing load-bearing work it has not earned.

OUTPUT
Save as TIMING-EXTENT-TRADE-2026-11-10.md in AUDIT OUTPUTS, marked SANDBOX/DRAFT and "not promoted". Put the scripts, seeds and raw tables beside it.
Open with a plain-words verdict of no more than five sentences: the label for each (event, axis, inheritance, ensemble candidate) among E2 and E3, what survives N → ∞, and whether any trade runs through energy.
Then give P1–P6, then one section per question in order. End with a summary table with these columns: question, classification, key number(s), and what it means for PHYS2 in one line.
Before saving, run the note's claims through the Jev claim-ledger battery. Attach its report, and remove or flag any promotion language it finds.
