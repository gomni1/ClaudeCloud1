# P2.9A — Section strata: preregistered specification

Status: SANDBOX / DRAFT. Not promoted. Frozen before any code was run; the SHA-256 of this file is recorded in `RESULTS.md`. No claim or kill condition changes after the freeze. A revision is a new claim, and any failure stays on the record.

Date: 2026-10-27. Source: CC-PROMPT-P2.9A-Section-Strata-2026-10-26. Candidate under test: P2.9A-02 (20 Aug 2026), a working candidate, not an adopted premise.

## 0. Register and walls

- **Coarse-grained register.** Smooth sections and smooth loops are effective-register summaries of step processes. Where cheap, each result is re-checked on a discrete representation: n-gon sections and sampled loops.
- **No dynamics.** No energy, elasticity, stress, ribbon or rod model, and no section dynamics. One instrument below (the connection rotation, §1.9) carries an inner product. It is used only as a cross-check, and a result is claimed from it only where two different invariant inner products give the same value.
- **Neutral labels.** Class A / class B; cycles A–B–A and B⁺–A–B⁻. Particle names appear only in the "Observational register" section of `RESULTS.md`.
- **Anti-fitting.** The charge premise (B carries a half-twist with conjugate presentations B⁺ and B⁻; A carries none) is an input. It is never reported as a result.
- **No grain-level bookkeeping.** The section field is a coarse-grained whole.

## 1. Definitions

1.1 **Section space.** M ∈ {3, 4, 5}; the main case is M = 5, and M = 3 is used as a one-odd-mode truncation. V_M = ℂ^(M−1) with coordinates z_m = a_m + i b_m, m = 2..M. The section is r(φ) = 1 + Σ_m (a_m cos mφ + b_m sin mφ) = 1 + Σ_m Re(z_m e^(−imφ)). It is admissible if Σ|z_m| < 1, which gives r > 0 (star-shaped about the origin). Mode 1 is absent, so the origin is the centroid to first order, and exactly the centroid for every symmetric section. The admissible set is convex and every stratum is a cone through 0, so topological statements about V_M carry over to it by radial scaling.

1.2 **Discrete section.** The n-gon P_n(z) has vertices v_j = r(2πj/n) e^(2πij/n), j = 0..n−1, with n = 60 (divisible by 2, 3, 4, 5). Rotation acts on vertex positions. P is k-fold iff max_j |e^(2πi/k) v_j − v_(j+n/k)| ≤ τ.

1.3 **Group action.** R_β : z_m ↦ e^(imβ) z_m, which is r(φ) ↦ r(φ − β), the curve rotated by β counter-clockwise.

1.4 **Strata.** g(z) = gcd{m : z_m ≠ 0}; z = 0 is the circle (singular stratum). For z ≠ 0 the stabilizer is ℤ_g(z). Closed stratum C_k = {z : z_m = 0 whenever k ∤ m}. Open stratum C_k° = {g(z) = k}. C1° is the asymmetric stratum, written V_free. Note C4 ⊂ C2. Numerically a mode counts as nonzero iff |z_m| > τ (default τ = 1e−9), and the distance to C_k is d_k(z) = (Σ_{k∤m} |z_m|²)^½.

1.5 **Orientation maps.** A weight-w orientation map is a continuous θ : U → ℝ/2πℤ on an open rotation-invariant U with θ(R_β z) = θ(z) + wβ. Weight 1 is an orientation mod 2π; weight w gives an orientation mod 2π/w. Concrete maps:
- θ_P = arg(z_3 z̄_2), on U_P = {z_2 z_3 ≠ 0}.
- θ_R = arg(z_5 z̄_4), on U_R = {z_4 z_5 ≠ 0} (M ≥ 5). It shares no mode with θ_P.
- θ_M = arg(I_3 Ī_2), with I_a = ∬ ζ^a dA the complex area moments of the enclosed region (ζ = x + iy), on U_M = {I_2 I_3 ≠ 0}. One routine family serves smooth sections (polar integral, exact quadrature) and n-gons (Green's theorem, exact per edge).
- M = 3 only: θ_P′ = θ_P + arg(z_2³ z̄_3²).
- ψ_2 = arg z_2 (weight 2). For a single odd mode, ψ_3 = arg z_3 (weight 3).

A map returns "undefined" when any factor has modulus < η = 1e−6 (domain margin).

1.6 **Section field (loop).** A continuous γ : ℝ/2πℤ → V. The centreline is planar and sections are measured in its plane, which is a frame with zero holonomy. Writhe and Călugăreanu's theorem are out of scope; `RESULTS.md` notes where they would re-enter. A loop is sampled at t_i = 2πi/N. A lift accumulates wrapped differences in (−π, π]. It is accepted only if every step satisfies |Δ| ≤ π/2 (sampling guard); a failing step is bisected (depth ≤ 20), and if it still fails the lift is rejected.

1.7 **Winding.** For a weight-1 map θ and γ ⊂ U_θ: W_θ(γ) = (total lift)/2π.

1.8 **Odd-mode degree (one odd mode).** For M = 3, V ∖ C2 = {z_3 ≠ 0}, and D_3(γ) = deg(z_3 ∘ γ) for loops avoiding C2. For a loop with arcs in C2 (z_3 ≡ 0), each such arc is resolved by pushing z_3 off zero along the minimal body-frame paths (one path if the odd part returns with the same sign in the co-rotating frame, two paths ±π if it returns with the opposite sign: a "flip passage"). N_3(γ) = 2 × (mean of D_3 over the minimal resolutions).

1.9 **Connection rotation (cross-check instrument).** For an invariant inner product ⟨x, y⟩_w = Re Σ w_m x̄_m y_m (w_m > 0) and the rotation generator (ξz)_m = i m z_m: A_w(γ) = ∮ ⟨ξγ, dγ⟩_w / ⟨ξγ, ξγ⟩_w, defined if γ avoids the circle. Two weightings: w ≡ 1 and w_m = m². A value is claimed only where A_1 = A_(m²) to 1e−6.

1.10 **Rigid-sector loop.** Three sectors centred at 0, 2π/3 and 4π/3 (= −2π/3), each of half-width 0.6, separated by transition gaps. In a sector of class X the field is γ(t) = R_β(t) ρ, with ρ a fixed representative of a reference shape s_X, g(s_X) = k_X, S_X = C_(k_X). A transition is a straight body path between the reference shapes, rotated to the current representative, at fixed β; consecutive sectors of the same class need no transition. Every transition is later retraced in reverse, so the shape path is back-and-forth. At a sector, the representative may be relabelled ρ ↦ R_(2πj/k_X) ρ (j ∈ ℤ_(k_X)). This changes no section, so it is not a rotation. Sector twist c_X = (change of β across the sector)/2π. Total twist T = Σ c_X in turns.
- Charge-premise inputs: "A carries none" means c_A = 0. "B carries a half-twist" means c_B = ±½, with B⁺ = +½ and B⁻ = −½.
- **Attribution S (closure).** A class carries the half-twist iff closing the loop needs a relabel at that class's sections with Σ j/k ≡ ½ (mod 1).
- **Attribution R (rotation).** A class carries the half-twist iff its sectors' rotation is ≡ ½ (mod 1).

## 2. Claims (hypotheses, not expected results) and kill conditions

**H0 — Genericity.**
- H0a: V_free is open, dense and of full measure, and every C_k (k ≥ 2) is a linear subspace of real codimension 2·#{m ∈ [2, M] : k ∤ m} ≥ 2. Refuted if some C_k with k ≥ 2 has codimension 0 for some M ≥ 3. Discrete: the k-fold n-gons form a subspace of real codimension 2n(1 − 1/k) > 0.
- H0b, recorded as a requirement and not tested: holding a sector of positive length in C_k (k ≥ 2) needs a symmetry or constraint on whatever holds it. Even a point passage through C_k is non-generic for a single loop when the codimension is ≥ 2.

**H1 — All-asymmetric loops.**
- H1a: a closed field with every section in V_free and inside U_θ has W_θ ∈ ℤ. Refuted if a validated lift gives a non-integer beyond 1e−9.
- H1b: W_θ is invariant under deformations through loops that stay in V_free. Refuted for a given (M, θ) by one explicit homotopy inside V_free along which W_θ changes, with the change located at a section verified asymmetric (g = 1 and d_k ≥ 1e−3 for every k ≥ 2). Tested for M = 3 (θ_P, θ_P′, θ_M) and M = 5 (θ_P, θ_R, θ_M).
- H1b*: some weight-1 orientation map is defined on all of V_free. Refuted for M if the orbit loop of a free section is null-homotopic in V_free (degree 1 versus degree 0).

**H2 — Passing through a symmetric section.**
- H2a: for s ∈ C_k° (k = 2, 3, 4) and u supported on modes with k ∤ m, the body path s + εu → s → s + ε R_(2π/k) u is a continuous field whose end section is the start section rotated by 1/k turn. For k = 2 this is teardrop → ellipse → flipped teardrop along a straight line. Refuted if any of θ_P, θ_R, θ_M reads a change other than 2π/k (mod 2π) beyond 1e−9, or if the field is not continuous (sup-norm step not O(1/N)). The same check is repeated on 60-gons.
- H2b (consequence 1): a winding changes in a deformation only where passages through symmetric strata are gained or lost. Tested per map (it shares the witness of H1b) and for the canonical invariant N_3 / D_3 in M = 3. Refuted for a quantity if it changes at an asymmetric section.
- H2c (consequence 2): the conversion rule's "high-symmetry state" includes C2 passages, not only the circle. Supported if no weight-1 map is defined at any C2 section (exact) and an explicit C2 passage that avoids the circle changes the asymmetric orientation by ½ turn. Refuted if a weight-1 map is defined at a C2 section, or if the flip requires passing through the circle.

**H3 — Three sectors.** For each (S_A, S_B) ∈ {C1, C2, C3, C4}², decide whether (i) B⁺–A–B⁻ closes with T = 0 and (ii) A–B–A closes with T ∈ ½ + ℤ, under attribution S (primary) and attribution R (secondary). Hypothesis: the survivors are exactly S_B ∈ {C2, C4}. Refuted, under a given attribution, if any explicit construction with S_B ∈ {C1, C3} closes (residual < 1e−9) with both properties while the attribution assigns the half-twist to B. Also reported: whether S_A is forced or underdetermined, and whether the attribution is unambiguous (A could not carry the half-twist instead). Each construction is checked for continuity, closure, and A_1 = A_(m²) = 2πT.

**H4 — The unpaired half-twist as an invariant.**
- H4a: in A–B–A, the half-integer twist is a deformation invariant as long as the passages through B's stratum are kept, and twice the twist is an integer invariant equal to ±1 for A–B–A and 0 for B⁺–A–B⁻. Tested at three levels:
  - L-rigid: rigid-sector loops, continuous families.
  - L-one-odd: M = 3, deformations that keep B's arc in C2° and every other section in V_free. Invariant: N_3, whose parity is checked against the parity of the resolution-summed windings of θ_P, θ_P′, θ_M.
  - L-two-odd: M = 5, the same kind of deformation.

  Refuted at a level if an explicit deformation at that level changes the claimed invariant, or if two maps disagree on its parity.
- H4b: a loop with exact three-fold symmetry, γ(t + 2π/3) = R_α γ(t) for a fixed α, admits no A–B–A or B⁺–A–B⁻ pattern when classes are assigned by any rotation-invariant criterion. Refuted by an explicit three-fold-symmetric loop with a 2 : 1 class pattern.

## 3. Method and evidence grades

- **Exact** (sympy, or a hand proof written out in `RESULTS.md`): the rotation action, stabilizers, the obstruction to weight-1 maps on symmetric sections, the codimension formula, the flip identity, the rigid closure lemma, the π₁ statements, and the three-fold orbit argument.
- **Numerical** (support, not proof): windings, homotopies, construction closures, area-moment maps. Tolerances: τ = 1e−9 (stratum), η = 1e−6 (map domain), closure 1e−9, connection agreement 1e−6. Sampling convergence is checked at N and 2N.
- Small explicit constructions only; no parameter sweeps. The 16-cell enumeration of H3 is the one the prompt asks for.

## 4. Planted failures (the harness must catch all three)

- **PF1, hidden C2 passage.** A loop in M = 5 with (z_3, z_5)(t) = ε(e^(i(t − t*)) − 1)(1, e^(iκ)), t* = 1.2345, so the C2 passage falls between grid points (N = 256). The stratum detector must report a passage within |t − t*| < 1e−6 with d_2 < τ, and the grid minimum alone must stay above τ, which shows the passage is hidden from a naive check.
- **PF2, artificial 2π jump.** A lift with +2π added from some index onwards must be rejected by the lift validator. A raw sequence whose true step exceeds π must be flagged by the sampling guard.
- **PF3, near-C2 section.** A C2 section with z_3 = z_5 = 1e−7. classify(τ = 1e−9) must return C1 with a near-C2 flag; classify(τ = 1e−6) must return C2; θ_P, θ_R and θ_M must return undefined at η = 1e−6; the exact (sympy, rational) classification must give g = 1.

## 5. Stop conditions

- Stop at any claim that needs a dynamical choice, and record the choice.
- No extension to ribbons, elasticity, grain models, masses or spin.
- **Question-removal criterion.** A failure of H1 or H2 removes the question iff (i) the flip identity fails, or (ii) the rigid closure lemma fails, or (iii) the fractional part of T for retraced rigid-sector loops differs between the two weightings or between orientation maps. If the question is removed, stop after H2 and report.

## 6. Pre-freeze disclosure

A desk analysis preceded this spec. Its expectations, recorded before any code ran:
- H0 supported.
- H1a supported. H1b refuted for M ≥ 4 (no global weight-1 map on V_free; for M ≥ 5, V_free is simply connected) and supported for M = 3.
- H2a and H2c supported. H2b refuted for M ≥ 4 for map windings, supported in M = 3.
- H3 supported under attribution S with S_A underdetermined; refuted under attribution R when S_A is even.
- H4a supported at L-rigid, supported for parity at L-one-odd, refuted at L-two-odd.
- H4b supported.

They are listed so a reader can judge whether the spec was shaped to them. The kill conditions above stand regardless.
