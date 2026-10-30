# Grammar instability search: results

Status: SANDBOX / DRAFT. Not promoted. Nothing here is uniquely derived. Every statement holds only inside the definitions of `SPEC.md`: its rate laws, denominators, levels, rate distributions and mobility model. The ODEs and the ring are effective-register (coarse-grained) summaries of step processes, as `SPEC.md` §0 states.

## Freeze

`SPEC.md` SHA-256: `3cf366e942757eec9f20e6e27b6e34e86b002637381ef933538c2bf8cecc723f`. Recorded 2026-10-30, before any code of this task was written or run. The file is unchanged; the hash is the same at this commit.

## Verdicts

| Claim | Status | Kill | Where |
|---|---|---|---|
| **H-cyc**: no sustained cycle on one level under threshold rates | **Killed** | A stable cycle, verified by M4 | M2 draw 12051: closed level, tot, m = 10, kr = 8, kc = 1 |
| **H-mob-stat**: no stationary mobility instability at any stable balance | **Killed** | A stationary (Turing) instability, verified on the M4 ring, at a balance where −J is not a P-matrix | M3 balance of draw 2962: open level, tot, m = 10, kr = 2, kc = 7 |
| **H-mob-osc**: no oscillatory mobility instability | **Killed** | An oscillatory (wave) instability, verified on the M4 ring | M3 balance of draw 25922: open level, tot, m = 8, kr = 5, kc = 2 |

All three kills occur with the tot denominator. With cv, on both levels and under both laws, nothing was found:
- M0 proves stability of the cv balances for h > 0.
- M1 proves −J a P-matrix at every MA balance and at every TH cv balance with h > 0.
- In M3, −J was a P-matrix at all 7217 cv balances tested, with no oscillatory hit.

M0 locates the break exactly: with tot, γ = ∂g/∂L = ∂g/∂P = (k3·V·F′_kr − k11·C·F′_kc)·(−C/N²) has no fixed sign, and it enters the Hurwitz conditions with negative coefficients.

Stop rule (SPEC §7): each verified hit is reported below with its exact rates and is not analysed further. The cycle search, M2 and its adaptive stage, stopped at the H-cyc kill. M4 verification of each mobility claim stopped at its first verified hit.

### The verified hits (exact rates, 17 significant digits)

Rates are in the SPEC order (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12). On the closed level k9 and k12 are unused.

**H-cyc: draw 12051** (closed level, tot, TH, m = 10, kr = 8, kc = 1, T = 5.5615087789401905)

    k = (2.9003547032083254, 0.010775545859999208, 465.39899398749316, 0.019715084503096395,
         44.348507127906679, 0.015075556773752925, 0.0045307253399468556, 0.87222471602927243,
         0.022615937501073605, 0.0086023878667564075, 0.0052916453078389524)

- **The balance.** There is one balance, (C, V, L, P) = (1.1201, 0.64124, 0.073220, 3.7270). It is unstable: the reduced Jacobian has eigenvalues −47.26, +0.0407 and +0.0145, all real.
- **M2.** All 8 random starts on the simplex end on the same closed orbit, with a period of 247.528859880 (the 8 values agree to 4×10⁻¹³).
- **M4.**
  - LSODA period 247.528858734, Radau period 247.528859880 (relative difference 4.6×10⁻⁹, against the 10⁻⁶ required).
  - Floquet moduli: 1.0000000000000049 and 0.9999999999978 (the flow direction and the conserved total), then 2.4×10⁻¹⁶ and 5.1×10⁻¹⁶. Both nontrivial moduli are far below 1 − 10⁻⁶, so the cycle is **verified** and stable.
  - The orbit stays positive: C ∈ [0.767, 1.913], V ∈ [0.0286, 1.168], L ∈ [0.0502, 0.1250] and P ∈ [3.418, 3.933]. N = T is conserved along it to 10⁻¹⁴, and the orbit closes to 6×10⁻¹³.
- **Evidence:** `evidence/m4_cycle.json`. The analytic Jacobian matches central differences at 41 points around this orbit (pytest `test_jacobian_on_the_cycle_of_draw_12051`), so the variational equations behind the multipliers use a correct J.

**H-mob-stat: draw 2962** (open level, tot, TH, m = 10, kr = 2, kc = 7)

    k = (1.8047325554223845, 19.472814957834093, 717.86952393710192, 21.802082050661369,
         2.9442878450717398, 26.997306462616024, 0.10472386745043281, 1.6631630540346891,
         0.25326717741596944, 0.026476541916487024, 0.0012468653812572382)

- **The balance.** It is stable, at (4.9093×10⁻⁵, 2.8599×10⁻⁵, 3.5803×10⁻⁶, 7.4970×10⁻⁴).
- **The P-matrix test fails** on two principal minors of −J: {C} = −27.67 and {C, L} = −681.3.
- **M3.**
  - The random-D test finds a real eigenvalue of J − s·D with Re λ = 27.52, at D = diag(2.8276×10⁻⁴, 598.75, 3989.3, 12.041) and s* = 250.88.
  - The two-class sweep finds it too, with critical ρ = 40.95.
- **M4 ring** (200 sites, κ = 2562.9, so s* falls on mode 10).
  - The mode-10 coefficient along the leading eigenvector grew 10-fold by t = 0.0836, at a fitted rate of 27.69 against a predicted 27.52 (+0.6%). **Verified.**
  - Mode 10 is also the fastest-growing ring mode.
  - By 50 e-folding times the pattern is **stationary**: C varies from 3.3×10⁻⁷ to 2.05×10⁻⁴ around the ring, against 4.9×10⁻⁵ at the balance.

**H-mob-osc: draw 25922** (open level, tot, TH, m = 8, kr = 5, kc = 2)

    k = (2.511956395794086, 0.010236849356936459, 200.13067228788776, 0.95435863117548769,
         0.22090205518827652, 0.0068107600790384441, 116.90482801439401, 0.026564659181766367,
         6.097599308456032, 0.012926069620468996, 379.58573007166569)

- **The balance.** It is stable, at (2.4532×10⁸, 2.6687×10⁷, 5.2435×10⁸, 1.4289×10⁴). −J is not a P-matrix: {C} = −1.332 and {C, P} = −155.8.
- **M3.** At D = diag(2.5856×10⁻³, 8435.7, 1.5418×10⁻³, 229.25) and s* = 1.3821, J − s·D has the complex pair 0.07290 ± 1.4837i, with |Im|/Re = 20.
- **M4 ring.**
  - κ = 14.120. The mode-10 coefficient grew 10-fold by t = 32.2, at a fitted rate of 0.07022 against a predicted 0.07290 (−3.7%). **Verified.**
  - Mode 10 is the fastest-growing ring mode, so no real (stationary) mode outgrows the wave at this D.
  - At 50 e-folding times the pattern is **time-dependent, but not a rigid travelling wave** (standing or irregular): C varies over [1.57, 3.94]×10⁸ around the ring.

This balance also fails the P-matrix test. In this search no oscillatory hit occurred at a balance where −J is a P-matrix (see M3).

## M0 and M1 (symbolic, sympy; `evidence/m0_m1.json`)

| Setting | Result |
|---|---|
| M0, open, cv | det(−J) = h·k7·k9·(k5+k6). Every Hurwitz coefficient and determinant (c3, c2, c1, c0, D2, D3) is a polynomial with all coefficients positive for h > 0. **Holds**: stable if h > 0, a real positive eigenvalue if h < 0. |
| M0, closed, cv | det(−J_red) = h·(k1·k8 + k5·k7 + k5·k8·y + k5·k8 + k6·k7 + k6·k8·y + k6·k8); c2, c1, c0 and D2 are positive for h > 0. **Holds.** |
| M0, open, tot | **Fails.** c2 first loses sign definiteness, through the terms −γ·k1·k5, −γ·k1·k6, −γ·k5·k7 and −γ·k6·k7. c1, D2 and D3 are mixed as well. |
| M0, closed, tot | **Fails.** c1 first loses sign definiteness, through the same four −γ terms. c0 and D2 are mixed as well. |
| M1, MA, open | All 15 principal minors of −J at the closed-form balance have only positive coefficients after clearing positive denominators. −J is **a P-matrix for all positive rates.** |
| M1, TH, open, cv | All 15 minors factor into positive rate factors times h, y or neither, for example {C, V} = h·(k1+k7) and {C, V, L, P} = h·k7·k9·(k5+k6). −J is **a P-matrix for h > 0.** For any law in which g depends only on C and V, {C, V} = g_V·(k1+k7). |

The pre-spec expectation (SPEC §10) that H-mob-stat would survive held for cv and for MA, but not for tot.

## M2: cycle search (`evidence/m2_draws.jsonl.gz`)

**Coverage.** M2 ran draws 0–41099: 10 275 per variant, out of a planned 10⁵. It stopped under the H-cyc stop rule, not the budget (see the deviations). The adaptive stage (Nelder–Mead) was not run: it belongs to the cycle search, which the stop rule ended.

| Variant | Draws | End states: balance | periodic | unresolved | Draws with any unresolved | Draws with all 8 unresolved | Multistable draws | No stable balance |
|---|---|---|---|---|---|---|---|---|
| open, cv | 10 275 | 59 619 | 0 | 22 581 | 2 935 | 2 708 | 473 | 0 |
| closed, cv | 10 275 | 82 113 | 0 | 87 | 36 | 0 | 461 | 0 |
| open, tot | 10 275 | 58 179 | 0 | 24 021 | 3 097 | 2 885 | 225 | 6 |
| closed, tot | 10 275 | 82 042 | **8** | 150 | 29 | 12 | 155 | 12 |

**Unresolved end states**, by note:

| Note | End states |
|---|---|
| slow drift (fewer than 4 section crossings in 9·t_end) | 28 931 |
| reached a balance only after t_end | 17 772 |
| ode23s step limit | 136 |

**On the open level,** 26–28% of draws end entirely unresolved. Those starts neither reach a balance by t_end nor oscillate. That is not evidence of a cycle, but it also leaves the open level weakly covered. H-cyc's kill does not depend on this coverage. Had there been no hit, H-cyc would have been underdetermined.

**The closed level** resolves all but 0.1–0.2% of end states. Draw 12051 is the only draw with periodic end states. It is also one of the 12 closed-tot draws without a stable balance; those draws were not analysed further.

## M3: mobility tests (`evidence/m3_summary.json`, `evidence/m3_balances.jsonl.gz`)

**The set.**
- 10 330 stable balances: from every tenth draw of each variant, over the planned 10⁵-draw subsample.
- 1998 MA balances: from 2000 MA draws, 1000 open and 1000 closed, all cv.
- All 12 328 tests ran within the 1 CPU-hour cap (2557 CPU-s).

| Set | Stable balances | −J not a P-matrix | Stationary hits | Oscillatory hits | mpmath recomputations | max Γ / max\|λ(J)\| |
|---|---|---|---|---|---|---|
| TH, open, cv | 2607 | 0 | 0 | 0 | 209 | −1.1×10⁻⁴ |
| TH, closed, cv | 2612 | 0 | 0 | 0 | 128 | −5.7×10⁻⁵ |
| TH, open, tot | 2565 | 18 | 17 | 12 | 201 | +0.19 |
| TH, closed, tot | 2546 | 12 | 12 | 6 | 105 | +0.13 |
| MA, open, cv | 998 | 0 | 0 | 0 | 156 | −2.4×10⁻⁴ |
| MA, closed, cv | 1000 | 0 | 0 | 0 | 42 | −1.3×10⁻⁵ |

**Stationary hits.** Every one occurs where −J is not a P-matrix (29 of the 30 non-P balances), as the theorem in SPEC §5 requires.

**Oscillatory hits.** All 18 occur at non-P balances that also carry a stationary hit. Only 7 of the 18 are genuine complex pairs at the tested (D, s*), with |Im|/Re between 0.12 and 20. In the other 11, the golden-section refinement maximised over eigenvalues flagged complex by |Im λ| > 10⁻⁹·max|λ|. It converged onto a point where two real, Turing-unstable eigenvalues collide, so |Im| there is at roundoff level.

M4 tried three of these collision hits first, in job order (draws 2962, 5162 and 25163). It found no complex eigenvalue with Re > 0 at s* and recorded each as not verified. It then verified the genuine pair at draw 25922.

The preregistered criterion was applied as written. The collision cases are reported here, not removed.

## M4 (`evidence/m4_cycle.json`, `evidence/m4_lattice.json`)

| Run | Kind | Draw | Predicted rate | Measured rate | Verified | Pattern at 50 e-folds |
|---|---|---|---|---|---|---|
| cycle | — | 12051 (closed, tot) | — | — | yes | stable cycle, period 247.53 |
| ring | stationary | 2962 (open, tot) | 27.523 | 27.689 | yes | stationary |
| ring | oscillatory | 2962 | — | — | no: real-pair collision at s* | — |
| ring | oscillatory | 5162 (open, tot) | — | — | no: real-pair collision at s* | — |
| ring | oscillatory | 25163 (closed, tot) | — | — | no: real-pair collision at s* | — |
| ring | oscillatory | 25922 (open, tot) | 0.07290 | 0.07022 | yes | time-dependent, not a rigid travel |

## Planted failures (`evidence/planted.json`); all four caught

| Test | Result |
|---|---|
| PFA1, Brusselator | 8/8 starts periodic. Periods are 7.15691992 (spread 5×10⁻¹⁰), against an independent reference of 7.156919921, so within 10⁻¹⁰ rather than the 1% required. **Pass.** |
| PFA2, linear focus | Full classifier: unresolved (step limit). Poincaré stage alone: unresolved, with return differences of 6.3×10⁻⁴ over 207 crossings. Neither is periodic. **Pass.** |
| PFA3, Schnakenberg | The P-matrix test fails with minor −0.8. The two-class sweep finds the instability, and bisection gives ρ_c = 8.567631 against the exact 8.567627 (relative error 4×10⁻⁷). **Pass.** |
| PFA4, three-species wave | J is stable (eigenvalues −0.128 ± 1.286i and −0.545). M3 finds Γ = 0.0994 > 0 at s = 0.204. **Pass.** |

**Tests.** `pytest`: 12 tests in `tests/test_a.py`, covering M0 and PFA1–PFA4 (and the cycle Jacobian check above). The final output is in `evidence/pytest_output.txt`.

The first run failed one test, `test_balances_are_zeros_and_jacobian_matches_fd[closed-tot]` (`evidence/pytest_output_first_run.txt`). The cause was the test itself:
- Its central-difference step was relative to each coordinate, and a closed-tot balance has L = 3.6×10⁻⁸. The step, about 4×10⁻¹⁵, makes the difference quotient roundoff.
- The analytic Jacobian agrees with central differences at relative steps of 10⁻⁵ on every tested draw.

The step is now floored at 10⁻⁴ of the largest coordinate.

## Deviations and implementation notes (all failures stay on the record)

1. **M2 restarts.** Three M2 attempts were aborted while the classifier's efficiency steps were added, and their logs are kept as `evidence/run_log_{first,second,third}_m2_attempt.txt`:
   - The Radau Poincaré stage dominated the CPU, so these steps were added: an ode23s continuation to 10·t_end that counts section crossings; "slow drift" (fewer than 4 crossings) and "damped or irregular oscillation" (return differences ≥ 10⁻⁴) marked unresolved without the Radau stage; and CPU caps on that stage.
   - These steps can only lower sensitivity: a cycle approached too slowly would be unresolved, not missed silently. They do not touch the classification criteria. Attempt three (to draw 40 000) also found the periodic hit at draw 12051.
2. **The production M2 run stalled and was stopped.** It began 05:10 and was killed by PID at 06:07.
   - It stalled at draw 41199: the end state sat ~10⁻⁸ from a stable node, just outside the 10⁻⁸ balance test, and noise-level crossings sent it into the Radau stage.
   - Two fixes were drafted after it started: an ode23s step-size guard and Newton polishing of balances. Both were reverted unused, so the committed code is the code that produced `m2_draws.jsonl.gz`.
   - M2 was then not resumed, because draw 12051 was verified and the stop rule applies. The gzip, cut mid-write by the kill, was rewritten from its 41 100 complete records.
3. **M4 cycle verification.**
   - As committed in the harness, `verify_cycle` ran Radau twice, never LSODA. It was fixed before the verification.
   - LSODA's event location then failed when started exactly on the section (scipy brentq sign error). Both integrators now start 1% of a period downstream of the section point, and the section is unchanged.
4. **M3 subsample.** As committed, "every tenth draw" was `i % 10 == 0`. Draws are round-robin over 4 variants, so this selects the two open variants only.
   - Before M3 ran, it was changed to every tenth draw of each variant, `(i // 4) % 10 == 0`.
   - Draws 41100–99999 of that subsample had not been run by M2. They got M2 step 1 only (balances and stability, same code), so that M3 covers the planned 10⁵-draw subsample.
5. **M4 ring.** The harness's `verify_lattice` measured max |FFT₁₀| over roles, with the rate fitted over the first 20% of the run, which is past saturation.
   - Before any ring ran, it was replaced by `verify_ring`, which implements SPEC §6's measure: the mode-10 coefficient along the leading (left-)eigenvector, with the rate fitted over its 10-fold growth window. It also uses a sparse analytic Jacobian.
   - s* is the golden-section point when refinement improved on the grid, else the grid point.
   - The first ring attempt crashed at draw 2962's oscillatory hit (no complex eigenvalue at s*); `evidence/m4ring_stdout_first_attempt.txt` keeps it. It now records that case as not verified.
6. **The pytest step** (above).
7. **Storage.** The task directory's `.gitattributes` (`* text eol=lf`, added at the SPEC freeze) made git rewrite line endings inside `m2_draws.jsonl.gz` in commit `05450e5`. `.gz` and `.png` are now binary, and the blob is byte-identical from commit `8d83789` on.
8. **PFA4** uses a constructed matrix, because arXiv was unreachable. This is disclosed in the SPEC itself.

## CPU (CPU-hours; 2 cores, `taskset -c 2,3`, while task C built on cores 0–1)

| Item | CPU-h | Cap |
|---|---|---|
| M0 and M1 (sympy) | 0.13 | |
| Planted failures | 0.06 | |
| M4 (cycle 8 s, ring 67 s with the failed first attempt) | 0.02 | |
| **M0, M1, M4 and planted** | **0.21** | 1.0 |
| M2 attempt 1 (04:12–04:23, aborted) | ≤ 0.37 (upper bound: 2 cores × wall) | |
| M2 attempt 2 (04:23–04:27, aborted) | ≤ 0.13 (same bound) | |
| M2 attempt 3 (04:32–05:10, aborted; 2170 CPU-s logged by draw 40 000) | ≤ 1.25 (same bound) | |
| M2 production run (05:10–06:07; workers 73.5 CPU-min, of which 0.63 h in completed draws) | 1.23 | |
| **M2 draws, all attempts** | **≤ 2.98** | 3.5 |
| M2 adaptive | 0 (not run: stop rule) | 0.5 |
| M3 (jobs 2557 s, subsample balances 106 s) | 0.74 | 1.0 |
| Diagnostics and two pytest runs | ≈ 0.4 | |
| **Task total** | **≤ 4.3** | 6 |

## Observational register

Analogies only; nothing in this paragraph is a result. The kills show one level of the grammar with tot denominators doing three things: running as an autonomous clock, a stable relaxation cycle at fixed total; breaking into a stationary spatial pattern when its roles move at different rates; and supporting growing waves. A reader may be reminded of an internal clock inside a composite such as a nucleon, or of a localised structure. But nothing here identifies any particle, or the nucleon architecture's integer, and every effect sits on the tot side of the M0 break. With cv denominators the single level stayed stable, stationary and uniform throughout. On the reading in SPEC §10, cycling or patterned behaviour on the cv side would have to come from composites or from coupling between levels.
