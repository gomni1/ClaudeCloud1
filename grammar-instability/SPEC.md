# Grammar instability search: preregistered specification

Status: SANDBOX / DRAFT. Not promoted. This file is frozen before any code of this task is written or run, and its SHA-256 is recorded in `RESULTS.md`. After the freeze, no target, size, grid, threshold, interface rule or criterion changes. A revision is a new claim, logged as one, and every failure stays on the record.

Date: 2026-10-30. Source: PHYS2 cloud campaign, task A.

## Question

Can one level of the grammar, for some positive rates:

- **(a)** sustain a cycle under threshold rates; or
- **(b)** become unstable when its roles move at different rates, giving stationary patterns (spots or stripes) or oscillatory ones (waves)?

## 0. Register and walls

- **Coarse-grained register.** The ODEs, the compartments and the hopping below are effective-register summaries of step processes. They are not a claim about the step processes themselves.
- **No new rule.** The grammar, the constants and the rate laws are those of the campaign brief. Mobility is the only added structure. It is declared (§5) and swept, never chosen.
- **Neutral labels.** Mechanical text uses only C, V, L and P. Particle names appear only in the single paragraph of `RESULTS.md` headed "Observational register".
- **Out of scope.** Other rate laws, coupling between levels, any lattice beyond the M4 ring, and any link to the nucleon architecture's integer.

## 1. Model

Densities x = (C, V, L, P) ≥ 0. The indicator [o] is 1 on the open level and 0 on the closed level.

    dC/dt = −(k1+k2+k7)·C + k6·L + g
    dV/dt =  k2·C + k5·L + k8·P − g + [o]·k12
    dL/dt =  k1·C − (k5+k6)·L
    dP/dt =  k7·C − (k8 + [o]·k9)·P

Here g = k10·V + r3 − r11.

**Rate laws.**

- **MA:** r3 = k3·V·C and r11 = k11·C².
- **TH:** r3 = k3·V·F_kr(x) and r11 = k11·C·F_kc(x), where F_j(x) = Pr[Bin(m, x) ≥ j] = Σ_{i≥j} C(m, i)·x^i·(1−x)^(m−i).

**Denominators.**

- "cv": x = C/(C+V).
- "tot": x = C/(C+V+L+P).
- In both, x = 0 when the denominator is 0.

**Levels.**

- **Open level:** reactions 9 and 12 are present.
- **Closed level:** reactions 9 and 12 are absent, and N = C+V+L+P = T is conserved.

**Constants.** Astra's constants, in the order (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12), are (2, 9, 47, 1, 1, 1, 1, 1, 1, 13, ½).

**Balances.** Write a = k1+k2+k7, A = k2 + k7 + k1·k5/(k5+k6), δ = a − A = k1·k6/(k5+k6), and y = V/C.

- **Open level.** P* = k12/k9, C* = k12·(k8+k9)/(k7·k9) and L* = k1·C*/(k5+k6). V solves the C equation.
  - cv: S(y) = A, where S(y) = k10·y + k3·y·F_kr(1/(1+y)) − k11·F_kc(1/(1+y)).
  - tot: Ŝ(y) = A, with the argument 1/(1+y+q), where q = (L*+P*)/C*.
  - Multiplying by (1+y)^m (or (1+y+q)^m) gives a polynomial of degree m+1 in y. All its roots are computed (companion matrix, then Newton polishing), and the real roots with y > 0 are kept.
- **Closed level.**
  - L = k1·C/(k5+k6), P = k7·C/k8, and the C equation is the same as above.
  - cv: y* solves S(y) = A, and C = T/(1 + q_c + y*), where q_c = k1/(k5+k6) + k7/k8.
  - tot: x = C/T, and the C equation is a polynomial of degree m+1 in c = C/T, with roots taken in (0, 1/(1+q_c)).
  - **MA, closed level:** the C equation (k10 + k3·C)·V = A·C + k11·C², with V = T − C·(1 + q_c), is a quadratic in C, solved exactly.

**Jacobians.** Analytic, never by finite differences.

- **Stability.**
  - Open level: a balance is stable if every eigenvalue of the 4×4 Jacobian J has Re λ < 0.
  - Closed level: the same test is applied to the 3×3 Jacobian of the reduced system in (C, V, L), with P = T − C − V − L.

## 2. M0: Astra's balance result, re-derived symbolically (sympy)

**Setting: open level, cv.** Write g(C, V) = C·S(V/C). Then g_C = S − y·S′ and g_V = S′. At a balance, g_C = A − y·h, where h = S′(y*).

**Steps:**

1. Derive the characteristic polynomial of J in terms of (k's, y, h).
2. Show that det(−J) = h × (a positive expression). So h < 0 gives a real positive eigenvalue: the characteristic polynomial is negative at λ = 0 and positive as λ → ∞.
3. Test the Routh–Hurwitz conditions for h > 0 by expanding each Hurwitz determinant, after clearing positive denominators, as a polynomial in (k's, y, h). It is shown positive when every coefficient is positive.

**Extensions:**

- **Closed level, cv.** Use the reduced 3×3 system. The result holds or fails by the same steps.
- **tot, both levels.** g_L and g_P are nonzero, and J gains the entries J_CL, J_CP, J_VL and J_VP.

The output states whether each extension holds. If one does not, it states the first condition that is no longer sign-definite, and the term responsible.

## 3. M1: principal minors of −J

**MA, open level.** Compute all 15 principal minors of −J at the closed-form balance as rational functions of the rates. Then:

- clear the positive denominators (k5+k6, k7, k9, k10 + k3·C*, and powers of these);
- if every coefficient of each numerator is positive, the minor is proved positive for all positive rates;
- otherwise, search for an exact rational counterexample. Use 10⁵ log-uniform rate draws over [10⁻³, 10³] to locate a sign change, then confirm it in exact rational arithmetic.

**TH, open level, cv.**

- −J depends on (k's, y, h) only, so the same coefficient test applies with h as a free symbol.
- The minors are proved positive for h > 0 if the test passes; minors that contain h are reported in factored form.
- **tot and the closed level:** reported numerically from the M2 balances (the fraction of stable balances at which −J is a P-matrix). On the closed level the test uses the 14 proper principal minors, because det(−J) = 0 there.

**Numerical P-matrix test (M3).** Minors are computed in float64. A minor whose value is below 10⁻¹⁰ × the product of the absolute row sums of its submatrix is recomputed in 50-digit arithmetic (mpmath) from the analytic Jacobian.

## 4. M2: cycle search under TH

**Draws.** Up to 10⁵ draws, or until the M2 budget (§8) is spent.

- Draws are taken round-robin over the four variants (open/closed × cv/tot), so that a budget stop leaves equal coverage.
- The 11 rates are log-uniform over [10⁻³, 10³].
- m is uniform in {2, …, 12}; kr and kc are each uniform in {1, …, m}.
- On the closed level, T is log-uniform over [10⁻¹, 10²], and k9 and k12 are unused.
- Seeds are fixed and recorded.

**Per draw:**

1. Find all balances and classify their stability (§1).
2. Integrate from 8 random positive starts.
   - **Open level:** each coordinate is log-uniform over [10⁻²·s, 10²·s], where s is the mean coordinate of the largest balance.
   - **Closed level:** a uniform point on the simplex {N = T}.
   - **End time:** t_end = 10³ / (smallest rate constant in use).
3. **Integrator.**
   - Production: an L-stable Rosenbrock 2(3) method (Shampine–Reichelt ode23s) in numba, with the analytic Jacobian, rtol 10⁻⁷ and atol 10⁻¹²·s.
   - Early stop is allowed once the state is within 10⁻¹² (relative) of a linearly stable balance. Such a trajectory remains there, so this is equivalent to integrating on to t_end.
   - Non-finite or negative states beyond −10⁻⁹·s are logged as integration failures and counted as unresolved.
4. **Classifying each end state x_e.**
   - **balance:** ‖x_e − b‖₂/‖b‖₂ < 10⁻⁸ for some balance b.
   - **periodic:** decided by a Poincaré stage. Integrate on with scipy Radau (rtol 10⁻¹⁰, atol 10⁻¹⁴·s). The section is the hyperplane through x_e normal to f(x_e), crossed in the direction of f(x_e). Record crossings p₁, p₂, … for up to 200 crossings or 10·t_end. The state is periodic if ‖p_(k+1) − p_k‖₂/‖p_k‖₂ < 10⁻⁷ for three consecutive k. The period is the mean return time over those returns.
   - **unresolved:** anything else, including a balance not reached and no closed return.

**Adaptive stage.**

1. **Scores at the stable balances of each draw:**
   - δ_rel = −max Re λ / max |λ| (smallest means slowest);
   - ω = max |Im λ| / |Re λ| over eigenvalues with Im λ ≠ 0.
2. **Selection.** The 0.5% of draws with the smallest δ_rel and the 0.5% with the largest ω, about 1% in all.
3. **Nelder–Mead.**
   - From the 10 most extreme draws on each score (20 starts), each with 1000 objective evaluations: 2×10⁴ in all.
   - Variables are the log-rates (and log T on the closed level); m, kr and kc are held at the draw's values.
   - The objective is minimised: f = max over stable balances of δ_rel, that is, minus the slowest decay rate's magnitude in units of the spectral radius. f is set to +1 if no stable balance exists.
4. **Follow-up.** Every point visited with f ≤ 10⁻⁶ and a complex pair at the least stable eigenvalue is re-run through the per-draw classification (8 starts), and through 8 starts at f's crossing point found by bisection along the last simplex edge.

## 5. M3: mobility instability

**Mobility.** D = diag(d_C, d_V, d_L, d_P) ≥ 0, and s ≥ 0 is the wavenumber squared. A mode with wavenumber squared s grows by the eigenvalues of J − s·D.

**Set.**

- The stable balances of a 10% subsample of the M2 draws (every tenth draw, all variants).
- 2000 MA draws: 1000 open and 1000 closed, with the M2 rate distribution, all balances.

**Tests at each stable balance:**

- **Stationary.**
  - The P-matrix test of −J. On the closed level: the 14 proper principal minors > 0.
  - Where it fails, search s on a log grid of 201 points over [10⁻⁵, 10⁵], against the same 200 random D and the two-class sweep, for a real eigenvalue of J − s·D with Re λ > 0.
  - Each hit is refined by golden-section search in log s.
- **Oscillatory.**
  - Γ = the largest Re λ over eigenvalues of J − s·D with |Im λ| > 10⁻⁹·max|λ|, over s on the 201-point grid and over 200 random D (each d_r log-uniform over [10⁻⁴, 10⁴], fixed seed).
  - The maximum is refined by golden-section search in log s around the best grid point.
  - A hit is Γ > 10⁻⁹·max|λ(J)|.
- **Two-class sweep.** D = diag(1, ρ, 1, 1), with ρ on 81 log points over [10⁻⁴, 10⁴]. The same s grid and both tests are applied. A stationary hit in the sweep is refined to the critical ρ by bisection to relative 10⁻⁶.

**Theorem used.** If −J is a P-matrix, then det(−J + s·D) > 0 for all s ≥ 0 and all D ≥ 0. Proof: expand det(M + Δ) over principal minors for diagonal Δ ≥ 0. This excludes a real eigenvalue crossing zero, that is, stationary (Turing) instability. It does not exclude a complex pair crossing, that is, oscillatory (wave) instability. On the closed level the same expansion with det(−J) = 0 and positive proper minors gives det(−J + s·D) > 0 for s > 0 and D > 0.

## 6. M4: verifying a hit

**A cycle:**

- Reproduce it with scipy LSODA and Radau at rtol 10⁻¹⁰.
- The two periods must agree to relative 10⁻⁶.
- Floquet multipliers come from the monodromy matrix (variational equations over one period, Radau at rtol 10⁻¹⁰).
- The cycle is verified if the periods agree and every nontrivial multiplier has modulus below 1 − 10⁻⁶. One multiplier equals 1, and on the closed level a second one also equals 1.
- A cycle with a multiplier of modulus above 1 is reported as unstable. It is not a sustained cycle.

**A mobility instability:**

- Integrate the lattice ODE on a ring of 200 compartments: dX_i/dt = F(X_i) + κ·D·(X_(i+1) − 2·X_i + X_(i−1)).
- κ is set so that the most unstable s* falls on mode j = 10, that is, κ = s* / (2·(1 − cos(2π·10/200))).
- Start from the balance plus 1% independent uniform noise per site and role, and integrate with Radau (rtol 10⁻⁸) to 50 e-folding times of the growth rate.
- **Verified** if the amplitude of the unstable mode (the projection onto the leading eigenvector at its wavenumber) grows by at least a factor of 10 at the predicted rate within 20%.
- Report what the pattern saturates to: stationary, travelling or standing wave, or unbounded.

## 7. Claims and kill conditions

| Claim | Statement | Kill |
|---|---|---|
| **H-cyc** | No sustained cycle on one level under threshold rates | A cycle verified by M4 |
| **H-mob-stat** | No stationary mobility instability at any stable balance | An M1 counterexample, or a Turing instability confirmed by M4 at a balance where −J is not a P-matrix |
| **H-mob-osc** | No oscillatory mobility instability | One confirmed by M4 |

**Statuses.**

- **Survived:** the search ran its preregistered coverage and the kill did not occur.
- **Killed:** the kill occurred.
- **Underdetermined:** coverage fell short of the planned draws, or a planted failure that tests the relevant component failed.
  - H-cyc depends on PFA1 and PFA2.
  - H-mob-stat depends on PFA3.
  - H-mob-osc depends on PFA4.

**Stop rule.** On a verified hit, the hit is reported with its exact rates (all 17 digits) and the search for that claim stops. It is not analysed further.

## 8. Budget

**Caps (CPU-hours):**

| Item | Cap |
|---|---|
| Task total | 6 |
| M2 draws | 3.5 |
| M2 adaptive | 0.5 |
| M3 | 1.0 |
| M0, M1, M4 and planted failures | 1.0 |

**Cores.** At most 2 cores (`taskset`) while task C's build runs.

**Coverage.** A budget stop is recorded with the number of draws reached per variant.

## 9. Planted failures (the harness must catch all four)

- **PFA1. Brusselator.**
  - System: dx = a − (b+1)·x + x²·y and dy = b·x − x²·y, with a = 1, b = 3.
  - Run through the M2 classifier with t_end = 10³ (unit rates), from 8 starts.
  - **Pass:** all 8 are classified periodic, with periods within 1% of a reference period computed independently (Radau, rtol 10⁻¹², mean of 20 consecutive returns to x = a with dx > 0).
- **PFA2. Linear 2D focus.**
  - System: dz = (−10⁻⁴ + i)·z.
  - **Pass:** neither of two runs is classified periodic:
    - the full classifier (t_end = 10³/10⁻⁴);
    - the Poincaré stage alone, started at |z| = 1.
- **PFA3. Schnakenberg.**
  - System: du = a − u + u²·v and dv = b − u²·v, with a = 0.1, b = 0.9.
  - The balance is (1, 0.9), and J = [[0.8, 1], [−1.8, −1]].
  - The analytic critical ratio is d_c = (5.6 + √28.8)/1.28 = 8.567627…
  - **Pass:**
    - M1's numerical P-matrix test reports −J not a P-matrix (minor −0.8 < 0);
    - M3's two-class sweep D = diag(1, ρ) finds the stationary instability;
    - the bisection recovers d_c within 0.1%.
- **PFA4. Three-species linear system with a wave instability.**
  - J = [[a, −1, −c], [1, a, 0], [c, 0, −b]], with a = 0.1, b = 1, c = 1.
  - **Derivation.** The characteristic polynomial is λ³ + (b−2a)·λ² + (a²+1−2ab+c²)·λ + b·(a²+1) − a·c² = λ³ + 0.8·λ² + 1.81·λ + 0.91. The Hurwitz test holds (0.8·1.81 = 1.448 > 0.91), so J is stable. The {1, 2} subsystem [[0.1, −1], [1, 0.1]] has eigenvalues 0.1 ± i. With species 3 mobile (d₃ = 1) and species 1 and 2 nearly immobile (d₁ = d₂ = 10⁻⁴), the Schur complement at large s tends to that subsystem. So J − s·D has a complex pair with Re λ > 0 for a band of s: a wave instability.
  - **Source.** The mechanism, an unstable subsystem destabilised by the diffusion of the remaining species, is documented by Anma, Sakamoto and Yoneda, "Unstable subsystems cause Turing instability", Kodai Math. J. 35 (2012) 215–247, and, for wave instability in three-component systems, by Hata, Nakao and Mikhailov, "Sufficient conditions for wave instability in three-component reaction–diffusion systems", Prog. Theor. Exp. Phys. 2014, 013A01 (arXiv:1302.0683).
  - **Disclosed deviation.** arXiv was not reachable from this session, so the specific matrix is constructed here and its instability is derived above. It is not copied from those papers.
  - **Pass:** M3's oscillatory test, run with its 200 random D and the 201-point s grid, reports Γ > 0.

## 10. Expected outcomes (disclosed before the run)

**Claude's pre-spec check (30 Oct).** Reproduced, not copied:

- −J is a P-matrix at every stable balance at Astra's constants.
- A two-class sweep and 2×10⁴ random D gave no instability.
- In 4000 random draws, −J was a P-matrix at every stable balance except one MA case with entries near 10⁷. That case was attributed to finite-difference conditioning, unchecked.

**Expectations:**

- **H-mob-stat** is expected to survive. A plausible route to a proof: the minors of −J on the open level with cv depend on h and y only, and the {C, V} minor equals h·(k1+k7) for any rate law where g depends on C and V only.
- **H-cyc** is open. MA and Astra's result exclude cycles born at open-level cv balances, but not the closed level, the tot denominator, or cycles not born at a balance.
- **H-mob-osc** is open.
- A negative result is useful: localised or cycling patterns would then have to come from composites or from coupling between levels.
