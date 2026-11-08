# Step balance, orientation and the decay weight

**Stamp:** SANDBOX / DRAFT. Promotes nothing. 6 Nov 2026. Effective register, c = ħ = 1.
**Classes:** A proved · B refuted as stated · C blocked · D not mathematical · E external fact.

**Evidentiary limits.**
- Class-A results rest on linearity of expectation, short symmetry arguments, or sympy identities with residual 0. Monte Carlo and quadrature runs support them; they are not proofs.
- Every number comes from a script in this folder. The outputs are pasted in the appendix and stored next to the scripts as `*.out.txt`.
- Observational comparisons are labelled as such.
- Standard Model (SM) numbers are labelled controls. They are never used as explanation.
- Three parent-side inputs are taken as given: the π relation, the μ pair and relation, and the neutron's α. The only fitted *number* is α (Q5b).
- The π relation and the μ pair are discrete inputs that were also chosen by comparison with data (one of two cases, one of six). The matches in Q3(a) and Q4 show that the candidate family contains a case that fits. They are not independent predictions.
- Particle names (π, μ, e, ν) label patterns in the effective register. Helicity, chirality and V−A appear only inside labelled SM controls, or in the flags the task asked for.
- External values were checked on 6 Nov 2026 against the sources at the end. Items marked "from memory" were not re-checked.

**Anchor check.** The stated anchors come out only with full kinematics (proton recoil, and a massive electron in muon decay): N_μ/N_n = 4.22108×10⁸, miss 1.05574, and 1.02106 with the nonrelativistic (NR) Fermi function. Heavy-recoil counts give 1.05320 and 1.01861 instead. Q5(d) uses the full-kinematics anchors.

---

## Q1. One pattern

**In plain words.** Whatever the shape of a pattern's step distribution, its speed alone fixes the share of steps pointing against its travel, weighted by (1 − s·n)/2: that share is (1 − |v|)/2. In 1D it is simply the fraction of backward steps. R2 and R3 each give a number for "turnover not spent on travel", but it is a bare number with no direction, so a transition has nothing to align or oppose.

**Derivation.** (1 − s·n)/2 is affine in s, so

E[(1 − s·n)/2] = (1 − E[s]·n)/2 = (1 − v·n)/2 = (1 − |v|)/2.

- Only E[s] = v is used.
- |s| = 1 keeps the weight in [0, 1] and gives |v| = E[s·n] ≤ 1, with |v| = 1 only if s = n almost surely. Q3 and Q4 use this for massless daughters.
- In 1D, s ∈ {+n, −n}, so (1 − s·n)/2 is the indicator of a backward step. From P_f − P_b = |v| and P_f + P_b = 1 we get P_b = (1 − |v|)/2.
- At v = 0, n is undefined and the share is ½ along every axis.

The two budgets give:

- **R2:** uncommitted share √(1 − v²).
- **R3:** uncommitted share 1 − v.

Both are scalar functions of |v| and do not change when v is rotated. Neither supplies a vector that could be dotted with another daughter's. Inside 1D R1 they reappear as functions of the step shares: 1 − v = 2P_b (the steps cancelled by opposite steps), and √(1 − v²) = 2√(P_f P_b). That is bookkeeping and does not give either of them a direction.

Three step shapes with the same mean (two-point, cone, von Mises–Fisher) all give (1 − |v|)/2 within Monte Carlo error. See the Q1 output.

**Class: A.** R2 and R3 have no directional reading: A.

## Q2. Two patterns

**In plain words.** For two daughters stepping independently, the expected aligned or opposed weight depends only on their velocities: (1 ± v_i·v_j)/2. The shapes of the step distributions drop out, and only because the weight is linear in each step. A nonlinear weight does depend on shape. R2 and R3 give no pairwise form that sees the angle between daughters. They therefore predict no angular correlation, and the neutron's a = −0.104 excludes that.

**Derivation.** E[s_i·s_j] = Σ_k E[s_ik s_jk] = Σ_k E[s_ik] E[s_jk] = v_i·v_j by (iv). Hence E[(1 ∓ s_i·s_j)/2] = (1 ∓ v_i·v_j)/2.

- The condition actually needed is weaker than independence: tr Cov(s_i, s_j) = 0.
- The shared ledger acts through v_i and v_j, which are fixed once the arrangement is fixed. The statement is conditional on the arrangement.

**Dependence beyond the means.** There is none for the linear weights: all nine pairs of shapes agree to within 3×10⁻⁴. With the means held fixed, the nonlinear [(1 + s_i·s_j)/2]² ranges from 0.236 to 0.323 across shapes.

**R2/R3.** Any pairwise weight built from them has the form g(|v_i|, |v_j|) and is blind to the angle. In the heavy-recoil neutron, where the count is isotropic, such a weight gives a = 0. aSPECT measures a = −0.10430(84), which excludes this at 124σ (observational).

**Class: A** for the pairwise form and its mean-only dependence. **B (observational)** for R2/R3 as a source of correlations.

## Q3. Pion (observational)

**In plain words.** With the input choice ALIGNED, the transition requires the charged lepton's step to align with the neutrino's. That selects the lepton's *backward* steps, because the neutrino flies the other way. That share is (1 − β_ℓ)/2: tiny for the fast electron, sizable for the slow muon. Times the uniform count, it reproduces the textbook tree-level suppression formula *exactly*, R = 1.28335×10⁻⁴. That is 4.0% above PIENU, which is the size of the SM radiative correction. The opposed case gives R ≈ 5.5, off by a factor of 44,000.

**Derivation.** The decay is back to back with |v_ν| = 1, so v_ℓ·v_ν = −β_ℓ, where β_ℓ = (m_π² − m_ℓ²)/(m_π² + m_ℓ²).

- ALIGNED: W = (1 − β_ℓ)/2 = m_ℓ²/(m_π² + m_ℓ²).
- OPPOSED: W = (1 + β_ℓ)/2 = m_π²/(m_π² + m_ℓ²).
- Uniform count: N_ℓ = 4π p² E_ℓ/m_π, with p = (m_π² − m_ℓ²)/(2m_π) and E_ℓ = (m_π² + m_ℓ²)/(2m_π). So N_ℓ ∝ (m_π² − m_ℓ²)²(m_π² + m_ℓ²).

The product N·W_aligned ∝ m_ℓ²(m_π² − m_ℓ²)². The factor (m_π² + m_ℓ²) cancels exactly, so

R_a = (m_e/m_μ)²[(m_π² − m_e²)/(m_π² − m_μ²)]².

The sympy residual is 0, and the 30-digit numerical residual is 5×10⁻³¹. The identity holds exactly (class A).

**Predictions, reported before any comparison:**
- (a) ALIGNED: R = **1.283346×10⁻⁴**
- (b) OPPOSED: R = **5.486704**

**Comparison (observational).** PIENU measures (1.2344 ± 0.0030)×10⁻⁴, with statistical and systematic errors combined in quadrature.
- (a)/PIENU = 1.03965, a pull of **+16.4σ**.
- (b)/PIENU = 4.4×10⁴.

**Control (SM).** R_SM = 1.2352(1)×10⁻⁴ (Cirigliano & Rosell 2007).
- Case (a) is the SM tree-level value, identically.
- The SM radiative correction is −3.75% (R_SM/R_a = 0.96248). SM against PIENU is +0.27σ.
- So, in the SM's accounting (control), the whole miss of (a) is the radiative correction. The PHYS2 counterpart would presumably be arrangements with an extra photon, plus structure-dependent pieces. A two-body count contains neither.

**Class.**
- Identity: **A**.
- (b): **B** (observational).
- (a) as a final number: **B** as stated (16σ). Fixing it is **C**: blocked on a PHYS2 count of radiative arrangements (π → eνγ). Nothing in R1 supplies the −3.75%.

**Flag.** Two parts of the result are earned:
- The neutrino's orientation equals its direction of travel: |v| = 1 forces s = n (Q1, Q6d).
- The lepton enters only through its mean step (Q2), so the 3D continuum of step directions versus two helicity states cannot show up here.

The match still rests on the *input* choice ALIGNED, which nothing derives. Numerically, (1 − β)/2 is also the SM's wrong-helicity probability for a chiral state. The step reading reproduces that number but has not earned a spin interpretation (see Flags).

## Q4. Muon spectrum

**In plain words.** Six weightings of the uniform count were computed. Three are exactly of Michel form: the two that oppose the electron to a neutrino (ρ = 3/4), and the one that opposes the two neutrinos (ρ = 0). The three aligned cases are not of Michel form. TWIST's ρ matches 3/4 within 0.9σ. The electron spectrum cannot tell OPP(e, ν̄_e) from OPP(e, ν_μ); the ν_e spectrum (KARMEN) can, and on my reading it keeps only OPP(e, ν_μ). As a control, that case equals the SM V−A distribution over the whole Dalitz plot.

**Derivation.**
- Massless daughters have s_i = n_i exactly.
- Take M = 2, so x = E. The uniform count is 8π² E₁E₂E₃ dE₁dE₂.
- p_i·p_j = 2(1 − E_k), so OPP(i, j) = (1 − cos θ_ij)/2 = (1 − E_k)/(E_iE_j), and ALI = 1 − OPP.
- Weighted densities: OPP(i, j) gives E_k(1 − E_k); ALI(i, j) gives E₁E₂E₃ − E_k(1 − E_k).
- The electron spectrum comes from integrating E₂ over [1 − x, 1].

**All six cases (computed before any comparison):**

| pair | relation | electron f(x) | exact Michel? | ⟨x⟩ | ρ from ⟨x⟩ | ⟨W⟩ | ν̄_e spectrum | ν_μ spectrum |
|---|---|---|---|---|---|---|---|---|
| (e, ν̄_e) | ALIGNED | 5x²(1−x)(3−x) | no | 7/12 = 0.5833 | −1/8 | 2/7 | 5x²(1−x)(3−x) | 5x⁴ |
| (e, ν̄_e) | OPPOSED | 2x²(3−2x) | yes, ρ = 3/4 | 7/10 | 3/4 | 5/7 | 2x²(3−2x) | 12x²(1−x) |
| (e, ν_μ) | ALIGNED | 5x²(1−x)(3−x) | no | 7/12 | −1/8 | 2/7 | 5x⁴ | 5x²(1−x)(3−x) |
| (e, ν_μ) | OPPOSED | 2x²(3−2x) | yes, ρ = 3/4 | 7/10 | 3/4 | 5/7 | 12x²(1−x) | 2x²(3−2x) |
| (ν̄_e, ν_μ) | ALIGNED | 5x⁴ | no | 5/6 | 7/4 | 2/7 | 5x²(1−x)(3−x) | 5x²(1−x)(3−x) |
| (ν̄_e, ν_μ) | OPPOSED | 12x²(1−x) | yes, ρ = 0 | 3/5 | 0 | 5/7 | 2x²(3−2x) | 2x²(3−2x) |

- With no weight, the anchor is reproduced: (10/7)x²(6 − 6x + x²), mean 2/3.
- ⟨W⟩ is 5/7 for every OPPOSED pair and 2/7 for every ALIGNED pair. All pairs are equivalent under the uniform count.
- An independent RAMBO Monte Carlo with explicit angles agrees on ⟨x⟩ and ⟨W⟩ to within 3×10⁻⁴.

**Comparison (observational).** TWIST measures ρ = 0.74977 ± 0.00026.
- OPP(e, ν̄_e) and OPP(e, ν_μ): **+0.89σ**.
- OPP(ν̄_e, ν_μ): ρ = 0, excluded at −2890σ.
- ALIGNED cases: not of Michel form (they have an x⁴ term). The ρ values that match their means (−1/8, −1/8, 7/4) are all excluded.

**Separating the two survivors (E, with an inference flagged).** The two survivors swap the neutrino spectra. In μ⁺ decay, which is the charge conjugate:
- OPP(e⁺, ν_e) gives the ν_e spectrum the shape 2y²(3 − 2y).
- OPP(e⁺, ν̄_μ) gives it the shape 12y²(1 − y).

KARMEN measures ω_L = 0.027 (+0.038/−0.033 stat, ±0.031 syst), with ω_L ≤ 0.113 at 90% CL. The SM value is ω_L = 0. KARMEN calls ω_L the ν_e analogue of ρ, and its Eq. 4 is normalised so that pure g^V_LR gives 3/4. Reading ω_L into the same functional form as ρ, 12y²(1 − y) corresponds to ω_L = 0 and 2y²(3 − 2y) to ω_L = 3/4. KARMEN does not print G₂(x), so **this mapping is my inference**. Under it, OPP(e, ν̄_e) is excluded and **OPP(e, ν_μ) survives**.

**Control (SM).** Uniform count × OPP(e, ν_μ) equals |M|²_V−A × LIPS up to a constant over the whole Dalitz plot (sympy gives a constant ratio of 4). Put differently, the SM weight per arrangement in muon decay is the constant 8G_F²(2π)⁻⁵ times OPP(e, ν_μ). That constant was derived by hand. The code checks only the shape here; the constant enters Q5's control, where it reproduces the SM's own τ_n to 2×10⁻⁴.

**Class.**
- The six computations: **A**.
- The match to TWIST: **E** (observational), with two degenerate survivors.
- Selecting OPP(e, ν_μ): **E** plus the flagged inference.
- Which pair the muon names is an input and is not derived. "Why that pair?" is **C**.

## Q5. Neutron, and the consequence for the rate

**In plain words.** With a share α of aligned transitions, the correlation is a = 2α − 1, so aSPECT fixes α ≈ 0.448: slightly more opposed than aligned. The average weight is exactly ½ whatever α is, so α cannot affect the rate. But the muon's Michel-matching weight averages 5/7. Putting both weights in makes the muon-to-neutron rate miss much worse: 1.056 becomes 1.508, or 1.021 becomes 1.459 with the Fermi function. Agreement would need a factor of about 1.46 from the neutron's parent side, which no pairwise orientation weight can supply. In the SM that factor is mostly (1 + 3λ²)/4, the nucleon's axial structure. The old 5.6% near-agreement looks accidental.

**(a)** W = α(1 + c)/2 + (1 − α)(1 − c)/2 = ½[1 + (2α − 1)c], with c = v_e·v_ν = β_e cos θ. The heavy-recoil uniform count is isotropic in θ, so comparing with dΓ ∝ 1 + aβ cos θ gives **a = 2α − 1**. **A.**

**(b)** α = (1 + a)/2.
- aSPECT 2020 (a = −0.10430(84), PRC 101, 055506): **α = 0.44785 ± 0.00042**.
- The 2023 reanalysis (a = −0.10402(82), arXiv:2308.16170): α = 0.44799 ± 0.00041.

α is fitted; it is the declared parent-side input. **E + fit.**

**(c)** ⟨W⟩ = ½ + (2α − 1)⟨β cos θ⟩/2.
- Heavy recoil: the angular measure dΩ_e dΩ_ν is isotropic, so ⟨cos θ⟩ = 0 at every E_e and **⟨W⟩ = ½ for every α**. **A.**
- Full recoil: ⟨β cos θ⟩ = −5.1×10⁻⁴, so ⟨W⟩ = 0.5000266 at the fitted α. The result is exact only in the stated limit; the deviation is 3×10⁻⁵.

**(d)** ⟨W_μ⟩ = 5/7 in both Michel-matching cases (0.714271 with a massive electron), and ⟨W_n⟩ = ½, so the ratio is 10/7.
- **New miss:** 1.05574 × 10/7 = **1.5082** with no Coulomb correction. 1.02106 × 10/7 = **1.4587** with the NR Fermi function (Z = 1).
- **Required parent-side factor:** F_n = 1.508 without Coulomb, 1.459 with NR Fermi. Equivalently, ⟨W_n⟩ would have to be 0.754 or 0.729. No α gives that, since every α gives ½.
- **Control, the SM factor on the same basis:** F_SM = [|V_ud|²(1 + 3λ²)/4] × [f(1 + RC)/f_PHYS2] / (1 + δ_μ) = 1.3938 × 1.0443 = **1.4555**, against 1.4587 required.
  - The ratio 0.9978 is 878.4 s / 880.5 s: the SM's own τ_n with these λ and V_ud. That is not PHYS2's to explain.
  - The pieces: (1 + 3λ²)/4 = 1.470; |V_ud|² = 0.948; 1 + RC = 1.0389; full f over the NR-Fermi count = 1.0008; muon 1/(1 + δ_μ) = 1.0044.
  - The ¼ is 2/8, the ratio of the SM prefactors per arrangement for the neutron and muon weights.
- **Control, why the old agreement was close:** in SM terms the common-W near-agreement is 8⟨W_μ⟩ = 40/7 = 5.714 against |V_ud|²(1 + 3λ²) = 5.575. Those are unrelated quantities, so the 5.6% was accidental.
- **Control, the link between α and the rate:** in the SM one parent number λ fixes both α = (1 + λ²)/(1 + 3λ²) and the rate factor ∝ 1 + 3λ². The aSPECT α gives |λ| = 1.2677, which reproduces aSPECT's own quoted value. PHYS2 has two parent-side inputs with no link between them.

**Class.**
- (a): **A**.
- (b): **E + fit**.
- (c): **A** (heavy recoil).
- (d) arithmetic: **A**.
- The rule "common prefactor plus a pairwise orientation weight": **B** as stated (miss 1.51).
- Restoring agreement: **C**. It is blocked on a derived parent-side factor, such as a count of transition channels for a composite parent, and on a rule that ties that factor to α.

**What failed, and what survives.** The smallest failed assumption is that the parent side contributes only the orientation relation (and α) on top of a common prefactor. All the shape results survive, given the data-selected inputs: R_e/μ at tree level, ρ = 3/4, and a from α.

## Q6. Clock and mass

**In plain words.** A pattern that flips between forward and backward steps at rates a and b goes forward a fraction b/(a + b) of the time and drifts at (b − a)/(a + b).
- Holding ab = m² fixed, the drift is the tanh of a rapidity.
- The flip rate slows exactly like a moving clock: m√(1 − v²).
- Half the sum and half the difference of the two rates behave like energy and momentum, with E² − p² = m².
- Zero mass means one rate is zero, so the pattern runs one way at speed 1 forever.

The linear backward share and the square-root clock are two read-outs of one process, one counting steps and one counting flips, so they do not conflict. If continuum Lorentz boosts are taken as an input (effective register; R1 does not derive them), ab staying fixed under motion follows from transforming the light-like step segments. Most of this is known prior art.

**(a)** Dwell times are exponential with means 1/a (forward) and 1/b (backward). The forward fraction is (1/a)/(1/a + 1/b) = **b/(a + b)**, and v = P_f − P_b = **(b − a)/(a + b)**. **A** (sympy; the simulation agrees to about 0.3%).

**(b)** With a = m e^(−η) and b = m e^(η): v = tanh η. The stationary reversal rate is P_f·a + P_b·b = 2ab/(a + b) = m/cosh η = **m√(1 − v²)**. **A.** Per unit proper time, the reversal rate is m.

**(c)** With E = (a + b)/2 and p = (b − a)/2: E² − p² = ab = m², and p/E = v. **A.** This holds by construction for any a and b. The content of (c) lies in reading the half-sum and half-difference as E and p, and in the boost covariance below.

Further results:
- E is the arithmetic mean of the two rates, m their geometric mean, and the reversal rate their harmonic mean (E × rate = m²).
- A boost of rapidity θ Doppler-scales right-moving null segments by e^(θ) and left-moving ones by e^(−θ). Then a′ = a e^(−θ), b′ = b e^(θ), a′b′ = ab, and (E, p) transforms as a Lorentz 2-vector (sympy residuals 0).
- Scaling keeps exponential dwell times exponential, so a boosted telegraph process is again a telegraph process. An explicitly boosted rest-frame path gives a′ = 0.6046 (predicted 0.6065) and b′ = 1.6510 (predicted 1.6487), with KS p = 0.62.
- So "ab unchanged by motion" follows from continuum Lorentz boosts, which are an input here and are not derived from R1. On a literal lattice of one site per tick, where boosts are not symmetries, it is **not** earned and stays a candidate.

**(d)** If m = 0, then ab = 0. Take a = 0: the forward state is absorbing, so P_f → 1, v → 1, and the reversal rate → 0. The pattern has one fixed orientation at speed 1 and no rest frame (η → ∞ at finite E = b/2). If m > 0, then a, b > 0, so P_f and P_b lie in (0, 1) and |v| < 1, with both orientations present. **A.**

**(e)** Yes, the two hold together.
- (1 − v)/2 = a/(a + b) is an occupation share: what a transition that reads the current step sees.
- m√(1 − v²) = 2ab/(a + b) is a transition rate: how often the orientation flips.
- They are different functionals of the same (a, b), and the simulation reproduces both at once.
- R3's 1 − v = 2a/(a + b) is the fraction of cancelled steps. R2's √(1 − v²) is the reversal rate divided by m.
- Caveat on R2: its "fixed total" has to be m (the geometric mean). Its "displacement share v" matches p/E only with total E = γm, which is not fixed.

**A**, with the R2 reading noted.

**(f) Prior art** (acknowledged, not imported):
- **Feynman checkerboard.** Feynman & Hibbs, *Quantum Mechanics and Path Integrals* (1965), Problem 2-6 (problem number from memory). It builds the 1+1 Dirac propagator as a sum over light-speed zigzags with amplitude iεm per reversal. Already known: speed-1 steps, and mass as the reversal amplitude or rate.
- **Persistent random walk and the telegraph equation.** G. I. Taylor (1922); S. Goldstein, Q. J. Mech. Appl. Math. 4, 129 (1951); M. Kac, Rocky Mountain J. Math. 4, 497 (1974, from 1956 lectures). Already known: (a), and the dwell and occupation results.
- **Gaveau, Jacobson, Kac & Schulman, PRL 53, 419 (1984).** The 1+1 Dirac equation is the analytic continuation of the telegraph process. Already known: mass corresponds to the reversal rate. Their construction is limited to 1+1 dimensions.
- **Asymmetric telegraph process with a Lorentz transformation removing the drift.** Beghin, Nieddu & Orsingher, J. Appl. Math. Stoch. Anal. 14, 11 (2001), doi:10.1155/S104895330100003X. Authors and title are from memory, and I did not read the full text. Known in substance: (b) and the boost structure.
- **G. N. Ord.** Reported, in a search summary I did not follow up, to show that the checkerboard embeds in Kac's classical process. A likely reference is Ord & Gualtieri, PRL 89, 250403 (2002), from memory and not read.
- **Review and 3D.** Dunkel & Hänggi, Phys. Rep. 471, 1 (2009); Serva, Lorentz-invariant processes at speed c in 3D (arXiv:2004.11983).
- **Not found stated anywhere** (searched, not exhaustively): the explicit a = m e^(∓η) parametrisation, (E, p) = ((a + b)/2, (b − a)/2) as a 2-vector, and the harmonic-mean clock. Each follows in a few lines from the above. Treat them as re-derived, not new.
- **The decay-weight reading.** (1 − β)/2 equals the SM's chirality-flip probability, which is standard. Using it as a decay weight did not turn up in the sources checked (search not exhaustive). No novelty is claimed.

**Class:** (a)–(e) **A**; (f) **E**.

---

## Flags: where "step direction = orientation" does work it has not earned

1. **Orientation at rest (polarization).** R1(ii) gives E[s] = 0 at rest, so a pattern at rest carries no net orientation for a transition to read. Yet muons from π decay keep their polarization after stopping, and their decay electrons come out asymmetric about it (ξ ≈ 1; E, from memory, not re-verified here). R1 as stated cannot represent this. The smallest missing piece is a *persistent, axial* quantity carried by the step sequence (for example a sense of circulation), distinct from the polar mean step.
2. **Parity.** (1 ± s_i·s_j)/2 is parity-even, and so is every observable used here (R_e/μ, ρ, a). The measured parity-odd correlations (neutron A and B, the muon's ξ, neutrino helicity) refer to a parent or daughter spin. R1's only orientation is the polar mean step, which is zero at rest. This note does *not* show that no step-based construction can reach P-odd data; it shows only that the weights used here cannot. **Kill trigger:** if no axial orientation can be built from step balance, R1 cannot address P-odd decay data.
3. **ν versus ν̄.** Every massless pattern has orientation equal to its direction of travel (Q6d), so R1's orientation does not distinguish ν from ν̄. The distinction enters only through which pair and relation the parent names. The same gap makes the Q4 survivors' labels (ν̄_e or ν_μ) inputs: R1 supplies no identity criterion that separates the two neutrinos. KARMEN separates them through flavour-specific detection.
4. **Two states versus a continuum.** The 1D clock has exactly two orientations, which matches two helicity states numerically. In 3D the orientations form a continuum, and linear weights hide that (Q2). Any nonlinear read-out, or any observable sensitive to the second moments of s, would expose it. No 3D clock with an invariant m is established here.
5. **Three parent inputs with no link.** ALIGNED (π), OPP(e, ν_μ) (μ) and α = 0.448 (n) are each supplied and none is derived. A quick test of "pairs from the same current are aligned" would pick ALI(e, ν̄_e) for the muon, which Q4 refutes. No unifying rule is offered.

## Summary

| Question | Class | Key number(s) | What it means for PHYS2 |
|---|---|---|---|
| Q1 | A | backward share (1 − \|v\|)/2 for any shape; in 1D = P(backward); R2 √(1 − v²), R3 1 − v are scalars | R1 gives an orientation share a transition can read; R2/R3 give none. |
| Q2 | A (R2/R3: B obs.) | (1 ∓ v_i·v_j)/2, independent of shape; a nonlinear weight varies 0.236–0.323 | Pairwise weights see only velocities, and only because they are linear. |
| Q3 identity | A | R_a ≡ (m_e/m_μ)²[(m_π² − m_e²)/(m_π² − m_μ²)]² | The ratio of the two leptons' backward-step shares carries the suppression; the count supplies the rest. |
| Q3(a) ALIGNED | B as stated; C remedy | 1.28335×10⁻⁴; ÷ PIENU = 1.0397 (+16σ); [control] SM radiative correction −3.75% | Equals SM tree level; [control] the miss equals the SM radiative correction; PHYS2 has no radiative count. |
| Q3(b) OPPOSED | B | 5.487 (×4.4×10⁴) | OPPOSED on (ℓ, ν) is dead for the pion. |
| Q4 | A (computations); E (match) | OPP(e, ν): ρ = 3/4 (+0.89σ); OPP(ν̄, ν): ρ = 0; ALIGNED not Michel; ⟨W⟩ = 5/7 or 2/7 | One of six cases gives ρ = 3/4; the data select it, so this is a fitted discrete input, not a prediction; KARMEN separates the two survivors (inference flagged). |
| Q5(a) | A | a = 2α − 1 | α is the aligned share. |
| Q5(b) | E + fit | α = 0.44785(42) | The neutron is slightly opposed-dominant. |
| Q5(c) | A (heavy recoil) | ⟨W⟩ = ½ for all α; 0.500027 with full recoil | α carries no rate information. |
| Q5(d) | A arithmetic; B common-prefactor rule; C remedy | miss 1.5082 / 1.4587; F_n ≈ 1.46–1.51 needed; [control] SM 1.4555, mostly (1 + 3λ²)/4 = 1.470 | Weighting breaks the rate; [control] in SM terms the old 5.6% is a coincidence of unrelated factors; a parent-side factor is missing. |
| Q6(a–d) | A | v = tanh η; reversal rate m√(1 − v²); E² − p² = m²; m = 0 gives speed 1 | In 1D, R1-clock's rates reproduce known relations (v = tanh η, the time-dilated clock, and E² − p² = m², which holds by construction). |
| Q6(e) | A | (1 − v)/2 is an occupation share, m√(1 − v²) a rate | The linear share and the quadrature clock coexist; R2's fixed total is m. |
| Q6(f) | E | Feynman–Hibbs 1965; Kac 1974; GJKS 1984; Beghin et al. 2001 | The clock structure is known prior art; the decay-weight use did not turn up in the sources checked. |

**Kill triggers.**
1. If PHYS2 cannot count radiative arrangements that supply about −3.75% for π → eν, the pion stays 16σ off.
2. If no parent-side rule produces F_n ≈ 1.46 from the neutron's structure and ties it to α, the rate comparison fails by 46–51%.
3. If no axial orientation can be built from step balance, P-odd data is out of scope.

**Hand-offs.**
- Verify the ω_L ↔ shape mapping against Greub et al.'s G₂(x).
- Find a 3D step process with an invariant m (Serva 2020 is a lead).

## Sources (checked 6 Nov 2026 unless marked)

- aSPECT 2020, a = −0.10430(84): [arXiv:1908.04785](https://arxiv.org/abs/1908.04785), PRC 101, 055506. Reanalysis a = −0.10402(82): [arXiv:2308.16170](https://arxiv.org/abs/2308.16170).
- PIENU: arXiv:1506.05845 (value as given in the task; not re-fetched).
- SM R_e/μ: Cirigliano & Rosell, [arXiv:0707.3439](https://arxiv.org/abs/0707.3439) and [arXiv:0707.4464](https://arxiv.org/abs/0707.4464) (PRL 99, 231801). A later lattice value, 1.23501(10)×10⁻⁴ ([arXiv:2607.22358](https://arxiv.org/abs/2607.22358)), was not checked.
- TWIST ρ = 0.74977(12)(23): Bayes et al., PRL 106, 041804 (2011); review [arXiv:1902.06291](https://arxiv.org/abs/1902.06291).
- KARMEN ω_L: Armbruster et al., PRL 81, 520 (1998), [hep-ex/9806024](https://arxiv.org/abs/hep-ex/9806024).
- Gaveau, Jacobson, Kac & Schulman, PRL 53, 419 (1984). Dunkel & Hänggi, [arXiv:0812.1996](https://arxiv.org/abs/0812.1996). Serva, [arXiv:2004.11983](https://arxiv.org/abs/2004.11983). Beghin, Nieddu & Orsingher, doi:10.1155/S104895330100003X.
- SM controls from memory: |V_ud| = 0.97373 and λ = −1.2754 (PDG 2024); f = 1.6887 and 1 + RC = 1.03886 (Czarnecki, Marciano & Sirlin 2018). These are mutually consistent: they reproduce the 4908.6 s constant (Q5 output).

## Lint record (claim-ledger battery, 6 Nov 2026)

- **Run.** `phys2-claim-ledger` with `jev-1.13.0` pinned, the model id the calibration gate passed with on 2026-09-22. 122 of the 130 extracted claims were judged; the source list and the appendix line were left out. Raw answers are in `phys2-claim-ledger/ledger-out-step-balance/judged.jsonl`. This is a triage index over wording, not a verdict on the physics.
- **Censuses.**
  - Register: effective 56, observational 43, not a physical claim 15, native 6, mixed 2.
  - Result class: generative 47, structural 39, discriminating 13, hygiene 8, not a result 15. Hygiene is known to be undercounted.
- **Acted on** (wording changed in this note):
  - All 3 promotion flags.
  - 15 of the 19 overclaims.
  - 4 of the 6 anti-fitting flags, the ones about data-selected discrete inputs.
  - The 15 register flags, answered with one register line.
  - The 3 unstated-identity flags, answered by noting in Flag 3 that R1 has no criterion separating the two neutrinos.
- **Not acted on:**
  - 4 overclaims on statements that are computed or given: the Q1 summary, the neutrino's speed 1, the boosted-path numbers, and a conditional kill trigger.
  - 2 anti-fitting flags: one on a labelled control, one on a flag that cites data as a failure rather than a target.
  - 71 high insertion-risk scores. These are dominated by definitions and formula lines, the tool's known weak spot (it flags rule definitions, and it missed a planted insertion at 1.73). The two that matter were handled: Q6(c) holds by construction, and the boost invariance rests on an imported input.
  - 195 low-confidence routings, mostly on formula and table rows.
- **Uninformative here.** RA1/A3 dependence 0 and duplicates 0: the note uses neither axiom, and the duplicate detector skips same-document pairs.
- **Not re-linted.** The edited wording has not been run through the battery again.

---

## Appendix: code and output

Run with Python 3.14, sympy 1.14, numpy 2.5, scipy 1.18. Monte Carlo seeds are fixed.

### q1_q2_patterns.py

```python
"""Q1 and Q2: orientation shares of one pattern and of two independent patterns under R1.

The proofs are linearity of expectation. This script checks them on step
distributions of different shapes that share the same mean, and shows that a
weight that is not linear in each step does depend on shape.
"""
import numpy as np
from scipy.optimize import brentq

rng = np.random.default_rng(20261106)
NS = 2_000_000


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def basis(n):
    n = unit(n)
    t = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = unit(np.cross(n, t))
    e2 = np.cross(n, e1)
    return n, e1, e2


def two_point(vvec, size):
    """1D-embedded: s = +n or -n, P(+n) = (1+|v|)/2."""
    n = unit(vvec); v = np.linalg.norm(vvec)
    fwd = rng.random(size) < (1 + v) / 2
    return np.where(fwd[:, None], n, -n)


def cone(vvec, size):
    """s uniform on a cone of half-angle acos(|v|) about n."""
    n, e1, e2 = basis(vvec); c = np.linalg.norm(vvec); s_ = np.sqrt(1 - c * c)
    phi = rng.random(size) * 2 * np.pi
    return c * n + s_ * (np.cos(phi)[:, None] * e1 + np.sin(phi)[:, None] * e2)


def vmf(vvec, size):
    """von Mises-Fisher on the sphere with mean resultant length |v|."""
    n, e1, e2 = basis(vvec); R = np.linalg.norm(vvec)
    kappa = brentq(lambda k: 1 / np.tanh(k) - 1 / k - R, 1e-6, 1e4)
    u = rng.random(size)
    w = 1 + np.log(u + (1 - u) * np.exp(-2 * kappa)) / kappa   # exact inverse-CDF for cos
    phi = rng.random(size) * 2 * np.pi
    sw = np.sqrt(np.clip(1 - w * w, 0, None))
    return w[:, None] * n + sw[:, None] * (np.cos(phi)[:, None] * e1 + np.sin(phi)[:, None] * e2)


shapes = {"two-point": two_point, "cone": cone, "vMF": vmf}

print("Q1  E[(1 - s.n)/2] versus (1 - |v|)/2   (N = %d samples each)" % NS)
for vvec in ([0.3, 0, 0], [0.2, 0.5, -0.4], [0, 0, 0.9]):
    vvec = np.array(vvec); v = np.linalg.norm(vvec); n = unit(vvec)
    row = []
    for name, f in shapes.items():
        s = f(vvec, NS)
        mean_s = s.mean(0)
        share = ((1 - s @ n) / 2).mean()
        row.append(f"{name}: {share:.5f} (|E[s]-v|={np.linalg.norm(mean_s - vvec):.1e})")
    print(f"  |v|={v:.4f}  predicted {(1 - v) / 2:.5f} | " + " | ".join(row))

print("\nQ1  1D: P(backward) = (1-v)/2 exactly; R2/R3 'uncommitted shares' (scalars, no direction)")
print("   v     P_b=(1-v)/2   R3: 1-v   2*P_b   R2: sqrt(1-v^2)   2*sqrt(P_f*P_b)")
for v in (0.0, 0.3, 0.6, 0.9, 0.99):
    pb, pf = (1 - v) / 2, (1 + v) / 2
    print(f"  {v:4.2f}   {pb:.6f}      {1 - v:.6f}  {2 * pb:.6f}  {np.sqrt(1 - v * v):.6f}         {2 * np.sqrt(pf * pb):.6f}")

print("\nQ2  E[(1 -/+ s_i.s_j)/2] for independent patterns, versus (1 -/+ v_i.v_j)/2")
vi = np.array([0.5, 0.2, 0.0]); vj = np.array([-0.3, 0.6, 0.4])
pred_al = (1 + vi @ vj) / 2; pred_op = (1 - vi @ vj) / 2
print(f"  v_i.v_j = {vi @ vj:.5f}; predicted ALIGNED {pred_al:.5f}, OPPOSED {pred_op:.5f}")
for ni, fi in shapes.items():
    for nj, fj in shapes.items():
        si = fi(vi, NS); sj = fj(vj, NS)
        d = np.einsum("ij,ij->i", si, sj)
        al = ((1 + d) / 2).mean(); op = ((1 - d) / 2).mean()
        sq = (((1 + d) / 2) ** 2).mean()   # a weight that is NOT linear in each step
        print(f"  {ni:>9} x {nj:<9}  ALIGNED {al:.5f}  OPPOSED {op:.5f}   nonlinear [(1+s.s)/2]^2 {sq:.5f}")
se = 0.5 / np.sqrt(NS)
print(f"  Monte Carlo standard error on each linear entry <= {se:.1e}")
```

**Output**

```text
Q1  E[(1 - s.n)/2] versus (1 - |v|)/2   (N = 2000000 samples each)
  |v|=0.3000  predicted 0.35000 | two-point: 0.34986 (|E[s]-v|=2.9e-04) | cone: 0.35000 (|E[s]-v|=3.0e-04) | vMF: 0.34988 (|E[s]-v|=9.7e-04)
  |v|=0.6708  predicted 0.16459 | two-point: 0.16484 (|E[s]-v|=5.1e-04) | cone: 0.16459 (|E[s]-v|=5.7e-04) | vMF: 0.16464 (|E[s]-v|=5.8e-04)
  |v|=0.9000  predicted 0.05000 | two-point: 0.05009 (|E[s]-v|=1.8e-04) | cone: 0.05000 (|E[s]-v|=2.5e-04) | vMF: 0.04995 (|E[s]-v|=4.5e-04)

Q1  1D: P(backward) = (1-v)/2 exactly; R2/R3 'uncommitted shares' (scalars, no direction)
   v     P_b=(1-v)/2   R3: 1-v   2*P_b   R2: sqrt(1-v^2)   2*sqrt(P_f*P_b)
  0.00   0.500000      1.000000  1.000000  1.000000         1.000000
  0.30   0.350000      0.700000  0.700000  0.953939         0.953939
  0.60   0.200000      0.400000  0.400000  0.800000         0.800000
  0.90   0.050000      0.100000  0.100000  0.435890         0.435890
  0.99   0.005000      0.010000  0.010000  0.141067         0.141067

Q2  E[(1 -/+ s_i.s_j)/2] for independent patterns, versus (1 -/+ v_i.v_j)/2
  v_i.v_j = -0.03000; predicted ALIGNED 0.48500, OPPOSED 0.51500
  two-point x two-point  ALIGNED 0.48498  OPPOSED 0.51502   nonlinear [(1+s.s)/2]^2 0.23626
  two-point x cone       ALIGNED 0.48501  OPPOSED 0.51499   nonlinear [(1+s.s)/2]^2 0.28426
  two-point x vMF        ALIGNED 0.48507  OPPOSED 0.51493   nonlinear [(1+s.s)/2]^2 0.27844
       cone x two-point  ALIGNED 0.48473  OPPOSED 0.51527   nonlinear [(1+s.s)/2]^2 0.32341
       cone x cone       ALIGNED 0.48510  OPPOSED 0.51490   nonlinear [(1+s.s)/2]^2 0.32060
       cone x vMF        ALIGNED 0.48511  OPPOSED 0.51489   nonlinear [(1+s.s)/2]^2 0.32111
        vMF x two-point  ALIGNED 0.48491  OPPOSED 0.51509   nonlinear [(1+s.s)/2]^2 0.30225
        vMF x cone       ALIGNED 0.48452  OPPOSED 0.51548   nonlinear [(1+s.s)/2]^2 0.31130
        vMF x vMF        ALIGNED 0.48484  OPPOSED 0.51516   nonlinear [(1+s.s)/2]^2 0.31036
  Monte Carlo standard error on each linear entry <= 3.5e-04
```

### q3_pion.py

```python
"""Q3: pi -> l nu with the uniform count and one pairwise orientation weight on (l, nu)."""
import sympy as sp
from mpmath import mp, mpf, sqrt

mp.dps = 30
m_pi, m_mu, m_e = mpf("139.57039"), mpf("105.6583755"), mpf("0.51099895")


def kin(ml):
    p = (m_pi**2 - ml**2) / (2 * m_pi)
    E = (m_pi**2 + ml**2) / (2 * m_pi)
    return p, E, p / E


pe, Ee, be = kin(m_e)
pm, Em, bm = kin(m_mu)
# uniform count N = 4 pi p^2 / |d(E_l+E_nu)/dp| = 4 pi p^2 E_l / m_pi
Ne_over_Nmu = (pe**2 * Ee) / (pm**2 * Em)
print(f"beta_e = {float(be):.9f}   beta_mu = {float(bm):.9f}")
print(f"N_e/N_mu (uniform count) = {float(Ne_over_Nmu):.6f}")

# back to back, neutrino speed 1:  v_l . v_nu = -beta_l
W = {"ALIGNED": lambda b: (1 - b) / 2, "OPPOSED": lambda b: (1 + b) / 2}
R = {}
for k, w in W.items():
    R[k] = Ne_over_Nmu * w(be) / w(bm)
    print(f"{k:8s}: W_e = {float(w(be)):.6e}  W_mu = {float(w(bm)):.6e}  W_e/W_mu = {float(w(be)/w(bm)):.6e}  R = {float(R[k]):.6e}")

closed = (m_e / m_mu)**2 * ((m_pi**2 - m_e**2) / (m_pi**2 - m_mu**2))**2
print(f"closed form (m_e/m_mu)^2[(m_pi^2-m_e^2)/(m_pi^2-m_mu^2)]^2 = {float(closed):.10e}")
print(f"ALIGNED minus closed form (30-digit arithmetic) = {float(R['ALIGNED'] - closed):.3e}")

# symbolic identity
M, ml1, ml2 = sp.symbols("M m1 m2", positive=True)
def sym(ml):
    p = (M**2 - ml**2) / (2 * M); E = (M**2 + ml**2) / (2 * M)
    return p, E, (1 - p / E) / 2
p1, E1, w1 = sym(ml1); p2, E2, w2 = sym(ml2)
ratio = (p1**2 * E1 * w1) / (p2**2 * E2 * w2)
target = (ml1 / ml2)**2 * ((M**2 - ml1**2) / (M**2 - ml2**2))**2
print("sympy: ALIGNED ratio - closed form simplifies to", sp.simplify(ratio - target))
print("sympy: ALIGNED weight W_l =", sp.simplify(w1), "  OPPOSED weight =", sp.simplify(1 - w1))

# observation (PIENU 2015) and SM control (Cirigliano & Rosell 2007)
R_exp, s_stat, s_sys = 1.2344e-4, 0.0023e-4, 0.0019e-4
s_exp = (s_stat**2 + s_sys**2) ** 0.5
R_SM = 1.2352e-4
Ra = float(R["ALIGNED"]); Rb = float(R["OPPOSED"])
print(f"\nPIENU R = {R_exp:.4e} +/- {s_exp:.4e} (stat+syst in quadrature)")
print(f"ALIGNED/PIENU = {Ra / R_exp:.5f}   pull = {(Ra - R_exp) / s_exp:+.1f} sigma")
print(f"OPPOSED/PIENU = {Rb / R_exp:.4e}")
print(f"[control] SM R = {R_SM:.4e};  SM/tree = {R_SM / Ra:.5f}  -> radiative correction {100 * (R_SM / Ra - 1):+.3f} %")
print(f"[control] SM vs PIENU pull = {(R_SM - R_exp) / s_exp:+.2f} sigma")
```

**Output**

```text
beta_e = 0.999973191   beta_mu = 0.271384734
N_e/N_mu (uniform count) = 3.487903
ALIGNED : W_e = 1.340441e-05  W_mu = 3.643076e-01  W_e/W_mu = 3.679420e-05  R = 1.283346e-04
OPPOSED : W_e = 9.999866e-01  W_mu = 6.356924e-01  W_e/W_mu = 1.573067e+00  R = 5.486704e+00
closed form (m_e/m_mu)^2[(m_pi^2-m_e^2)/(m_pi^2-m_mu^2)]^2 = 1.2833457598e-04
ALIGNED minus closed form (30-digit arithmetic) = -4.854e-31
sympy: ALIGNED ratio - closed form simplifies to 0
sympy: ALIGNED weight W_l = m1**2/(M**2 + m1**2)   OPPOSED weight = M**2/(M**2 + m1**2)

PIENU R = 1.2344e-04 +/- 2.9833e-07 (stat+syst in quadrature)
ALIGNED/PIENU = 1.03965   pull = +16.4 sigma
OPPOSED/PIENU = 4.4448e+04
[control] SM R = 1.2352e-04;  SM/tree = 0.96248  -> radiative correction -3.752 %
[control] SM vs PIENU pull = +0.27 sigma
```

### q4_muon.py

```python
"""Q4: muon decay, massless daughters, uniform count x one pairwise orientation weight.

Units: parent mass M = 2, so x = 2E/M = E.  Daughters: 1 = e, 2 = anti-nu_e, 3 = nu_mu.
Uniform count:  d^3p1 d^3p2 d^3p3 delta^4  =  8 pi^2 E1 E2 E3 dE1 dE2   (massless).
Massless: s_i = n_i exactly, and p_i.p_j = 2(1 - E_k), so
  OPPOSED(i,j) = (1 - cos th_ij)/2 = (1 - E_k)/(E_i E_j),   ALIGNED = 1 - OPPOSED.
"""
import itertools
import numpy as np
import sympy as sp

x, y, E1, E2, E3, rho = sp.symbols("x y E1 E2 E3 rho", real=True)
names = {1: "e", 2: "nubar_e", 3: "nu_mu"}
E = {1: E1, 2: E2, 3: E3}
uniform = E1 * E2 * E3


def opp(i, j):
    k = ({1, 2, 3} - {i, j}).pop()
    return (1 - E[k]) / (E[i] * E[j])


def spectrum(density, which):
    """Normalised energy spectrum of daughter `which` (x = its E), integrating the other energy."""
    others = [q for q in (1, 2, 3) if q != which]
    a, b = others  # integrate over E_a; E_b = 2 - x - E_a ; E_a in [1-x, 1]
    d = density.subs({E[which]: x, E[b]: 2 - x - E[a]})
    f = sp.integrate(sp.expand(sp.cancel(d)), (E[a], 1 - x, 1))
    f = sp.expand(sp.simplify(f))
    Z = sp.integrate(f, (x, 0, 1))
    return sp.factor(sp.expand(f / Z)), Z


michel = 4 * x**2 * (3 * (1 - x) + sp.Rational(2, 3) * rho * (4 * x - 3))


def michel_rho(f):
    sol = sp.solve(sp.Poly(sp.expand(f - michel), x).coeffs(), rho, dict=True)
    return sol[0][rho] if sol else None


# --- uniform count alone (anchor check) ---
fu, Zu = spectrum(uniform, 1)
print("uniform count alone: f(x) =", fu, "  mean =", sp.integrate(x * fu, (x, 0, 1)), "  total =", Zu)

rows = []
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    for rel in ("ALIGNED", "OPPOSED"):
        W = opp(i, j) if rel == "OPPOSED" else 1 - opp(i, j)
        dens = sp.cancel(uniform * W)
        fe, Z = spectrum(dens, 1)
        rho_exact = michel_rho(fe)
        mean = sp.integrate(x * fe, (x, 0, 1))
        rho_mean = sp.Rational(15, 2) * (mean - sp.Rational(3, 5))
        Wavg = Z / Zu
        fnb, _ = spectrum(dens, 2)
        fnm, _ = spectrum(dens, 3)
        rows.append(((names[i], names[j]), rel, sp.simplify(dens), fe, rho_exact, mean, rho_mean, Wavg, fnb, fnm))

print("\nALL SIX CASES (reported before any comparison)")
for (pair, rel, dens, fe, rx, mean, rm, Wavg, fnb, fnm) in rows:
    print(f"\n{rel} {pair}:  weighted density in (E1,E2) ~ {dens}")
    print(f"   electron f(x) = {fe}")
    print(f"   exact Michel? {'yes, rho = ' + str(rx) if rx is not None else 'no'}")
    print(f"   <x> = {mean} = {float(mean):.6f};  rho matching mean = {rm} = {float(rm):.6f}")
    print(f"   <W> over uniform count = {Wavg} = {float(Wavg):.6f}")
    print(f"   nubar_e spectrum = {fnb};   nu_mu spectrum = {fnm}")

# --- comparison with TWIST, only after the table ---
rho_T, sT = 0.74977, (0.00012**2 + 0.00023**2) ** 0.5
print(f"\nTWIST rho = {rho_T} +/- {sT:.5f} (stat+syst in quadrature)")
for (pair, rel, *_r) in rows:
    rx = _r[2]
    if rx is not None:
        print(f"   {rel} {pair}: rho = {float(rx):.5f}  pull = {(float(rx) - rho_T) / sT:+.2f} sigma")

# --- [control] Standard Model |M|^2 ~ (p_mu.p_nubar_e)(p_e.p_nu_mu); LIPS is flat in dE1 dE2 ---
M = 2
sm_density = (M * E2) * (2 * (1 - E2))          # (p_mu.p2)(p1.p3) with p1.p3 = 2(1-E2)
ours = sp.cancel(uniform * opp(1, 3))
print("\n[control] SM Dalitz density / (uniform x OPPOSED(e,nu_mu)) =", sp.simplify(sm_density / ours))
ours2 = sp.cancel(uniform * opp(1, 2))
print("[control] SM Dalitz density / (uniform x OPPOSED(e,nubar_e)) =", sp.simplify(sm_density / ours2))

# --- independent Monte Carlo check with explicit 3-vectors (RAMBO, massless) ---
rng = np.random.default_rng(7)
N = 1_000_000


def rambo3(n):
    c = 2 * rng.random((n, 3)) - 1
    phi = 2 * np.pi * rng.random((n, 3))
    q0 = -np.log(rng.random((n, 3)) * rng.random((n, 3)))
    s = np.sqrt(1 - c**2)
    q = np.stack([q0, q0 * s * np.cos(phi), q0 * s * np.sin(phi), q0 * c], -1)
    Q = q.sum(1)
    Mq = np.sqrt(Q[:, 0]**2 - (Q[:, 1:]**2).sum(-1))
    b = -Q[:, 1:] / Mq[:, None]
    g = Q[:, 0] / Mq
    a = 1 / (1 + g)
    xs = 2.0 / Mq                          # total mass 2
    bq = (b[:, None, :] * q[:, :, 1:]).sum(-1)
    p0 = xs[:, None] * (g[:, None] * q[:, :, 0] + bq)
    pv = xs[:, None, None] * (q[:, :, 1:] + b[:, None, :] * (q[:, :, 0][..., None] + (a[:, None] * bq)[..., None]))
    return p0, pv


p0, pv = rambo3(N)
w_u = p0[:, 0] * p0[:, 1] * p0[:, 2]       # uniform count = LIPS x prod(2E)
nhat = pv / p0[..., None]
print("\nMonte Carlo (RAMBO, explicit angles), N =", N, " max|sum p| =", f"{np.abs(pv.sum(1)).max():.1e}")
for (i, j) in [(0, 1), (0, 2), (1, 2)]:
    cij = (nhat[:, i] * nhat[:, j]).sum(-1)
    for rel, W in (("ALIGNED", (1 + cij) / 2), ("OPPOSED", (1 - cij) / 2)):
        ww = w_u * W
        print(f"   {rel} ({names[i+1]},{names[j+1]}): <x_e> = {np.sum(ww * p0[:, 0]) / ww.sum():.4f}   <W> = {ww.sum() / w_u.sum():.4f}")
```

**Output**

```text
uniform count alone: f(x) = 10*x**2*(x**2 - 6*x + 6)/7   mean = 2/3   total = 7/60

ALL SIX CASES (reported before any comparison)

ALIGNED ('e', 'nubar_e'):  weighted density in (E1,E2) ~ E3*(E1*E2 + E3 - 1)
   electron f(x) = 5*x**2*(x - 3)*(x - 1)
   exact Michel? no
   <x> = 7/12 = 0.583333;  rho matching mean = -1/8 = -0.125000
   <W> over uniform count = 2/7 = 0.285714
   nubar_e spectrum = 5*x**2*(x - 3)*(x - 1);   nu_mu spectrum = 5*x**4

OPPOSED ('e', 'nubar_e'):  weighted density in (E1,E2) ~ E3*(1 - E3)
   electron f(x) = -2*x**2*(2*x - 3)
   exact Michel? yes, rho = 3/4
   <x> = 7/10 = 0.700000;  rho matching mean = 3/4 = 0.750000
   <W> over uniform count = 5/7 = 0.714286
   nubar_e spectrum = -2*x**2*(2*x - 3);   nu_mu spectrum = -12*x**2*(x - 1)

ALIGNED ('e', 'nu_mu'):  weighted density in (E1,E2) ~ E2*(E1*E3 + E2 - 1)
   electron f(x) = 5*x**2*(x - 3)*(x - 1)
   exact Michel? no
   <x> = 7/12 = 0.583333;  rho matching mean = -1/8 = -0.125000
   <W> over uniform count = 2/7 = 0.285714
   nubar_e spectrum = 5*x**4;   nu_mu spectrum = 5*x**2*(x - 3)*(x - 1)

OPPOSED ('e', 'nu_mu'):  weighted density in (E1,E2) ~ E2*(1 - E2)
   electron f(x) = -2*x**2*(2*x - 3)
   exact Michel? yes, rho = 3/4
   <x> = 7/10 = 0.700000;  rho matching mean = 3/4 = 0.750000
   <W> over uniform count = 5/7 = 0.714286
   nubar_e spectrum = -12*x**2*(x - 1);   nu_mu spectrum = -2*x**2*(2*x - 3)

ALIGNED ('nubar_e', 'nu_mu'):  weighted density in (E1,E2) ~ E1*(E1 + E2*E3 - 1)
   electron f(x) = 5*x**4
   exact Michel? no
   <x> = 5/6 = 0.833333;  rho matching mean = 7/4 = 1.750000
   <W> over uniform count = 2/7 = 0.285714
   nubar_e spectrum = 5*x**2*(x - 3)*(x - 1);   nu_mu spectrum = 5*x**2*(x - 3)*(x - 1)

OPPOSED ('nubar_e', 'nu_mu'):  weighted density in (E1,E2) ~ E1*(1 - E1)
   electron f(x) = -12*x**2*(x - 1)
   exact Michel? yes, rho = 0
   <x> = 3/5 = 0.600000;  rho matching mean = 0 = 0.000000
   <W> over uniform count = 5/7 = 0.714286
   nubar_e spectrum = -2*x**2*(2*x - 3);   nu_mu spectrum = -2*x**2*(2*x - 3)

TWIST rho = 0.74977 +/- 0.00026 (stat+syst in quadrature)
   OPPOSED ('e', 'nubar_e'): rho = 0.75000  pull = +0.89 sigma
   OPPOSED ('e', 'nu_mu'): rho = 0.75000  pull = +0.89 sigma
   OPPOSED ('nubar_e', 'nu_mu'): rho = 0.00000  pull = -2890.15 sigma

[control] SM Dalitz density / (uniform x OPPOSED(e,nu_mu)) = 4
[control] SM Dalitz density / (uniform x OPPOSED(e,nubar_e)) = 4*E2*(E2 - 1)/(E3*(E3 - 1))

Monte Carlo (RAMBO, explicit angles), N = 1000000  max|sum p| = 6.9e-13
   ALIGNED (e,nubar_e): <x_e> = 0.5827   <W> = 0.2859
   OPPOSED (e,nubar_e): <x_e> = 0.6998   <W> = 0.7141
   ALIGNED (e,nu_mu): <x_e> = 0.5831   <W> = 0.2860
   OPPOSED (e,nu_mu): <x_e> = 0.6996   <W> = 0.7140
   ALIGNED (nubar_e,nu_mu): <x_e> = 0.8334   <W> = 0.2854
   OPPOSED (nubar_e,nu_mu): <x_e> = 0.5996   <W> = 0.7146
```

### q5_neutron.py

```python
"""Q5: neutron decay, (e, nubar) weight mixing ALIGNED (share alpha) and OPPOSED (share 1-alpha)."""
import numpy as np
import sympy as sp
from scipy import integrate

# ---------- (a) a = 2 alpha - 1 (symbolic) ----------
al, c = sp.symbols("alpha c", real=True)          # c = v_e . v_nu = beta_e cos(theta)
W = al * (1 + c) / 2 + (1 - al) * (1 - c) / 2
print("(a) W =", sp.collect(sp.expand(W), c), " = (1/2)(1 + a c) with a =", sp.simplify(2 * sp.expand(W).coeff(c, 1)))

# ---------- (b) alpha from aSPECT ----------
for label, a, da in (("aSPECT 2020 (PRC 101, 055506)", -0.10430, 0.00084),
                     ("aSPECT reanalysis (arXiv:2308.16170)", -0.10402, 0.00082)):
    print(f"(b) {label}: a = {a} +/- {da}  ->  alpha = (1+a)/2 = {(1 + a) / 2:.5f} +/- {da / 2:.5f}")
alpha = (1 - 0.10430) / 2

# ---------- (c) <W> over the uniform count ----------
th = sp.symbols("theta")
print("(c) heavy recoil: angular measure dOmega_e dOmega_nu is isotropic; integral of cos(theta) over the relative angle =",
      sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi)), "-> <W> = 1/2 for every alpha")

m_n, m_p, m_e = 939.56542052, 938.27208816, 0.51099895
m_mu = 105.6583755
Delta = m_n - m_p
aem = 1 / 137.035999084


def N_exact(weight=lambda pe, Ee, Enu, cth: 1.0):
    """Uniform count with full proton recoil: int d3pe d3pnu delta(M - Ee - Enu - Ep)."""
    Eemax = (m_n**2 + m_e**2 - m_p**2) / (2 * m_n)
    pmax = np.sqrt(Eemax**2 - m_e**2)

    def inner(cth, pe):
        Ee = np.sqrt(pe**2 + m_e**2); A = m_n - Ee
        Enu = (A**2 - m_p**2 - pe**2) / (2 * (A + pe * cth))
        if Enu <= 0:
            return 0.0
        Ep = A - Enu
        jac = 1 + (Enu + pe * cth) / Ep
        return 8 * np.pi**2 * pe**2 * Enu**2 / jac * weight(pe, Ee, Enu, cth)

    val, err = integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)
    return val


N0 = N_exact()
Nbc = N_exact(lambda pe, Ee, Enu, cth: (pe / Ee) * cth)
mean_bc = Nbc / N0
print(f"(c) full recoil: <beta_e cos theta> over uniform count = {mean_bc:.3e}")
print(f"    -> <W> = 1/2 + (2 alpha - 1)<beta cos>/2 = {0.5 + (2 * alpha - 1) * mean_bc / 2:.8f}  (alpha = {alpha:.5f})")

# ---------- anchors: reproduce the stated 4.2211e8, 1.0557 and 1.0211 ----------
def N3(M, m1, m3, fermi=False):
    """Uniform count int d3p1 d3p2 d3p3 delta^4 with daughter 2 massless (full recoil)."""
    E1max = (M**2 + m1**2 - m3**2) / (2 * M); pmax = np.sqrt(E1max**2 - m1**2)

    def inner(cth, p):
        E1 = np.sqrt(p * p + m1 * m1); A = M - E1
        E2 = (A * A - m3 * m3 - p * p) / (2 * (A + p * cth))
        if E2 <= 0:
            return 0.0
        E3 = A - E2
        F = 1.0
        if fermi and p > 0:
            eta = aem * E1 / p
            F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
        return 8 * np.pi**2 * p * p * E2 * E2 / (1 + (E2 + p * cth) / E3) * F
    return integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)[0]


def N_heavy(E0, fermi=False):
    def f(Ee):
        pe = np.sqrt(Ee**2 - m_e**2)
        F = 1.0
        if fermi:
            eta = aem * Ee / pe
            F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
        return 16 * np.pi**2 * pe * Ee * (E0 - Ee)**2 * F
    return integrate.quad(f, m_e, E0, epsabs=0, epsrel=1e-12)[0]


obs = 878.4 / 2.1969811e-6
N_mu = N3(m_mu, m_e, 0.0)                    # massive e, massless neutrinos
N_n, N_nF = N3(m_n, m_e, m_p), N3(m_n, m_e, m_p, fermi=True)
print(f"\nobserved Gamma_mu/Gamma_n = tau_n/tau_mu = {obs:.6e}")
print(f"   full kinematics: N_mu/N_n = {N_mu / N_n:.5e}  miss = {N_mu / N_n / obs:.5f};  with NR Fermi: miss = {N_mu / N_nF / obs:.5f}")
print(f"   (heavy-recoil variant for reference: miss = {7*np.pi**2*m_mu**5/240 / N_heavy(Delta) / obs:.5f}; "
      f"NR Fermi {7*np.pi**2*m_mu**5/240 / N_heavy(Delta, True) / obs:.5f})")
miss0 = N_mu / N_n / obs
missF = N_mu / N_nF / obs

# ---------- (d) muon weight = Michel-matching case (<W_mu> = 5/7), neutron <W_n> = 1/2 ----------
Wmu, Wn = 5 / 7, 1 / 2
print(f"\n(d) <W_mu>/<W_n> = {Wmu / Wn:.6f}")
print(f"    new miss (no Coulomb)     = {miss0:.5f} x {Wmu / Wn:.5f} = {miss0 * Wmu / Wn:.5f}")
print(f"    new miss (NR Fermi, Z=1)  = {missF:.5f} x {Wmu / Wn:.5f} = {missF * Wmu / Wn:.5f}")
print(f"    required neutron parent-side factor F_n = {miss0 * Wmu / Wn:.4f} (no Coulomb) / {missF * Wmu / Wn:.4f} (NR Fermi)")
print(f"    equivalently <W_n> would have to be {Wn * miss0 * Wmu / Wn:.4f} / {Wn * missF * Wmu / Wn:.4f} instead of 0.5")

# ---------- [control] Standard Model factor on the same basis ----------
hbar = 6.582119569e-22        # MeV s
GF = 1.1663788e-11            # MeV^-2 (PDG)
Vud, lam = 0.97373, 1.2754    # PDG 2024 (Vud from superallowed; lambda average)
f_full, one_RC = 1.6887, 1.03886   # Czarnecki-Marciano-Sirlin 2018 (f incl. Coulomb, size, recoil)
f0 = N_n / (16 * np.pi**2 * m_e**5)           # PHYS2 neutron count in f units (anchor basis)
fNR = N_nF / (16 * np.pi**2 * m_e**5)
Gmu0 = GF**2 * m_mu**5 / (192 * np.pi**3)
one_dmu = (hbar / 2.1969811e-6) / Gmu0       # muon corrections absorbed when GF is defined
core = Vud**2 * (1 + 3 * lam**2) / 4
F_SM0 = core * f_full * one_RC / f0 / one_dmu
F_SMF = core * f_full * one_RC / fNR / one_dmu
print(f"\n[control] PHYS2 count in f units: no Coulomb = {f0:.5f}, f with NR Fermi = {fNR:.5f}, full SM f = {f_full}")
print(f"[control] muon side 1+delta_mu = {one_dmu:.5f}")
print(f"[control] V_ud^2 = {Vud**2:.5f}, 1+3 lambda^2 = {1 + 3 * lam**2:.5f}, (2/8) V^2(1+3l^2) = {core:.5f}, (1+3l^2)/4 = {(1 + 3 * lam**2) / 4:.5f}")
print(f"[control] SM factor, no-Coulomb basis = {F_SM0:.4f}  (required {miss0 * Wmu / Wn:.4f}; ratio {F_SM0 / (miss0 * Wmu / Wn):.5f})")
print(f"[control] SM factor, NR-Fermi basis   = {F_SMF:.4f}  (required {missF * Wmu / Wn:.4f}; ratio {F_SMF / (missF * Wmu / Wn):.5f})")
print(f"[control] SM tau_n = 4908.6 s / (V^2(1+3l^2)) = {4908.6 / (Vud**2 * (1 + 3 * lam**2)):.2f} s  vs 878.4 s")
# SM link between alpha and lambda: alpha = (1+l^2)/(1+3l^2)
lam_from_alpha = np.sqrt((1 - alpha) / (3 * alpha - 1))
print(f"[control] SM link alpha = (1+l^2)/(1+3l^2): alpha(l=1.2754) = {(1 + lam**2) / (1 + 3 * lam**2):.5f}; "
      f"|l| from aSPECT alpha = {lam_from_alpha:.4f}")

# ---------- electron-mass check on <W_mu> (Q4 used massless daughters) ----------
def N3w(M, m1, m3, w):
    E1max = (M**2 + m1**2 - m3**2) / (2 * M); pmax = np.sqrt(E1max**2 - m1**2)

    def inner(cth, p):
        E1 = np.sqrt(p * p + m1 * m1); A = M - E1
        E2 = (A * A - m3 * m3 - p * p) / (2 * (A + p * cth))
        if E2 <= 0:
            return 0.0
        E3 = A - E2
        return 8 * np.pi**2 * p * p * E2 * E2 / (1 + (E2 + p * cth) / E3) * w(p / E1, cth)
    return integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)[0]


Wmu_me = N3w(m_mu, m_e, 0.0, lambda be, cth: (1 - be * cth) / 2) / N_mu
print(f"\n<W_mu> for OPPOSED(e, nu) with massive electron (Q2: W = (1 - v_e.n_nu)/2) = {Wmu_me:.6f}  (massless 5/7 = {5/7:.6f})")
print(f"   -> new miss with this <W_mu> and <W_n> = 0.5: {miss0 * Wmu_me / 0.5:.5f} (no Coulomb), {missF * Wmu_me / 0.5:.5f} (NR Fermi)")
print(f"[control] consistency of SM constants: 2 pi^3 hbar / (G_F^2 m_e^5 f (1+RC)) = "
      f"{2 * np.pi**3 * hbar / (GF**2 * m_e**5 * f_full * one_RC):.1f} s (CMS 2018 quote: 4908.6 s)")
print(f"[control] SM pieces: f/fNR = {f_full / fNR:.5f}, 1/(1+delta_mu) = {1 / one_dmu:.5f}, "
      f"f(1+RC)/fNR/(1+delta_mu) = {f_full * one_RC / fNR / one_dmu:.5f}")
print(f"[control] old common-W near-agreement in SM terms: 8<W_mu> = {8 * 5 / 7:.4f} vs V^2(1+3l^2) = {Vud**2 * (1 + 3 * lam**2):.4f}")
```

**Output**

```text
(a) W = c*(alpha - 1/2) + 1/2  = (1/2)(1 + a c) with a = 2*alpha - 1
(b) aSPECT 2020 (PRC 101, 055506): a = -0.1043 +/- 0.00084  ->  alpha = (1+a)/2 = 0.44785 +/- 0.00042
(b) aSPECT reanalysis (arXiv:2308.16170): a = -0.10402 +/- 0.00082  ->  alpha = (1+a)/2 = 0.44799 +/- 0.00041
(c) heavy recoil: angular measure dOmega_e dOmega_nu is isotropic; integral of cos(theta) over the relative angle = 0 -> <W> = 1/2 for every alpha
(c) full recoil: <beta_e cos theta> over uniform count = -5.105e-04
    -> <W> = 1/2 + (2 alpha - 1)<beta cos>/2 = 0.50002662  (alpha = 0.44785)

observed Gamma_mu/Gamma_n = tau_n/tau_mu = 3.998214e+08
   full kinematics: N_mu/N_n = 4.22108e+08  miss = 1.05574;  with NR Fermi: miss = 1.02106
   (heavy-recoil variant for reference: miss = 1.05320; NR Fermi 1.01861)

(d) <W_mu>/<W_n> = 1.428571
    new miss (no Coulomb)     = 1.05574 x 1.42857 = 1.50820
    new miss (NR Fermi, Z=1)  = 1.02106 x 1.42857 = 1.45865
    required neutron parent-side factor F_n = 1.5082 (no Coulomb) / 1.4587 (NR Fermi)
    equivalently <W_n> would have to be 0.7541 / 0.7293 instead of 0.5

[control] PHYS2 count in f units: no Coulomb = 1.63189, f with NR Fermi = 1.68732, full SM f = 1.6887
[control] muon side 1+delta_mu = 0.99561
[control] V_ud^2 = 0.94815, 1+3 lambda^2 = 5.87994, (2/8) V^2(1+3l^2) = 1.39377, (1+3l^2)/4 = 1.46998
[control] SM factor, no-Coulomb basis = 1.5049  (required 1.5082; ratio 0.99783)
[control] SM factor, NR-Fermi basis   = 1.4555  (required 1.4587; ratio 0.99783)
[control] SM tau_n = 4908.6 s / (V^2(1+3l^2)) = 880.46 s  vs 878.4 s
[control] SM link alpha = (1+l^2)/(1+3l^2): alpha(l=1.2754) = 0.44671; |l| from aSPECT alpha = 1.2677

<W_mu> for OPPOSED(e, nu) with massive electron (Q2: W = (1 - v_e.n_nu)/2) = 0.714271  (massless 5/7 = 0.714286)
   -> new miss with this <W_mu> and <W_n> = 0.5: 1.50817 (no Coulomb), 1.45862 (NR Fermi)
[control] consistency of SM constants: 2 pi^3 hbar / (G_F^2 m_e^5 f (1+RC)) = 4908.6 s (CMS 2018 quote: 4908.6 s)
[control] SM pieces: f/fNR = 1.00082, 1/(1+delta_mu) = 1.00440, f(1+RC)/fNR/(1+delta_mu) = 1.04429
[control] old common-W near-agreement in SM terms: 8<W_mu> = 5.7143 vs V^2(1+3l^2) = 5.5751
```

### q6_clock.py

```python
"""Q6: R1-clock, a 1D telegraph process: forward->backward at rate a, backward->forward at rate b."""
import numpy as np
import sympy as sp

a, b, m, eta, th = sp.symbols("a b m eta theta", positive=True)

# (a) stationary two-state chain: mean dwell 1/a forward, 1/b backward
pf = (1 / a) / (1 / a + 1 / b)
v = sp.simplify(pf * 1 + (1 - pf) * (-1))
print("(a) forward fraction =", sp.simplify(pf), "   net speed v =", v)

# (b) ab = m^2: a = m e^-eta, b = m e^eta
sub = {a: m * sp.exp(-eta), b: m * sp.exp(eta)}
v_eta = sp.simplify(v.subs(sub).rewrite(sp.tanh))
rev = pf * a + (1 - pf) * b                      # stationary reversals per unit time
rev_eta = sp.simplify(rev.subs(sub))
print("(b) v =", v_eta, "   reversal rate =", sp.simplify(rev), "=", rev_eta,
      "   minus m*sqrt(1-v^2):", sp.simplify((rev_eta - m * sp.sqrt(1 - sp.tanh(eta)**2)).rewrite(sp.exp)))

# (c) E = (a+b)/2, p = (b-a)/2
Ec, pc = (a + b) / 2, (b - a) / 2
print("(c) E^2 - p^2 =", sp.expand(Ec**2 - pc**2), "   p/E - v =", sp.simplify(pc / Ec - v))
# boost by rapidity theta: forward (right-moving null) dwell times scale by e^theta, backward by e^-theta
a2, b2 = a * sp.exp(-th), b * sp.exp(th)
E2, p2 = (a2 + b2) / 2, (b2 - a2) / 2
print("    under a boost: a'b' - ab =", sp.simplify(a2 * b2 - a * b),
      "  E' - (E cosh + p sinh) =", sp.simplify((E2 - (Ec * sp.cosh(th) + pc * sp.sinh(th))).rewrite(sp.exp)),
      "  p' - (p cosh + E sinh) =", sp.simplify((p2 - (pc * sp.cosh(th) + Ec * sp.sinh(th))).rewrite(sp.exp)))
print("    arithmetic mean E, geometric mean m, harmonic mean (reversal rate): E * rev =",
      sp.simplify(Ec * rev), " (= m^2)")

# (d) limits
print("(d) a -> 0 (m = 0): forward fraction ->", sp.limit(pf, a, 0), ", v ->", sp.limit(v, a, 0),
      ", reversal rate ->", sp.limit(rev, a, 0))

# ---------- simulation ----------
rng = np.random.default_rng(42)


def simulate(a_, b_, T=2.0e5):
    t, state, xpos, tf, nrev = 0.0, +1, 0.0, 0.0, 0
    durs = {+1: [], -1: []}
    while t < T:
        rate = a_ if state > 0 else b_
        d = rng.exponential(1 / rate)
        durs[state].append(d)
        t += d; xpos += state * d
        if state > 0:
            tf += d
        state = -state; nrev += 1
    return tf / t, xpos / t, nrev / t, durs


mass = 1.0
print("\nSimulation (m = 1, T = 2e5 per run)")
print("  eta    v_pred    v_sim     fwd_pred  fwd_sim   back_pred(1-v)/2  back_sim   rev_pred m*sqrt(1-v^2)  rev_sim")
for e in (0.0, 0.5, 1.0, 2.0):
    A_, B_ = mass * np.exp(-e), mass * np.exp(e)
    fwd, vs, rv, _ = simulate(A_, B_)
    vp = np.tanh(e)
    print(f"  {e:3.1f}   {vp:.5f}  {vs:.5f}   {(1 + vp) / 2:.5f}   {fwd:.5f}   {(1 - vp) / 2:.5f}           {1 - fwd:.5f}    "
          f"{mass * np.sqrt(1 - vp**2):.5f}                 {rv:.5f}")

# boost the rest-frame path explicitly with a Lorentz transformation of its vertices
from scipy import stats
_, _, _, d0 = simulate(1.0, 1.0)
seq = []
for f_, b_ in zip(d0[+1], d0[-1]):
    seq += [(+1, f_), (-1, b_)]
tt = np.concatenate([[0.0], np.cumsum([d for _, d in seq])])
xx = np.concatenate([[0.0], np.cumsum([s * d for s, d in seq])])
for e in (0.5, 1.0):
    g, beta = np.cosh(e), np.tanh(e)
    tp = g * (tt + beta * xx)               # active boost to velocity +tanh(eta)
    xp = g * (xx + beta * tt)
    dtp = np.diff(tp)
    fdur, bdur = dtp[0::2], dtp[1::2]
    ap, bp = 1 / fdur.mean(), 1 / bdur.mean()
    ks_f = stats.kstest(fdur, "expon", args=(0, fdur.mean())).pvalue
    print(f"  boosted eta={e}: a' = {ap:.4f} (pred {np.exp(-e):.4f}), b' = {bp:.4f} (pred {np.exp(e):.4f}), a'b' = {ap * bp:.4f}, "
          f"v' = {(xp[-1] - xp[0]) / (tp[-1] - tp[0]):.4f} (pred {beta:.4f}), KS p(forward dwell exponential) = {ks_f:.2f}")

# discrete ticks (one site per tick): two-state chain with flip probabilities per tick
pa, pb = 0.02, 0.05
print(f"\nDiscrete-tick chain, flip probs pa={pa}, pb={pb}: forward fraction pb/(pa+pb) = {pb / (pa + pb):.5f}, "
      f"v = {(pb - pa) / (pa + pb):.5f}, reversals/tick = 2 pa pb/(pa+pb) = {2 * pa * pb / (pa + pb):.5f}, "
      f"sqrt(pa pb) sqrt(1-v^2) = {np.sqrt(pa * pb) * np.sqrt(1 - ((pb - pa) / (pa + pb))**2):.5f}")
```

**Output**

```text
(a) forward fraction = b/(a + b)    net speed v = (-a + b)/(a + b)
(b) v = tanh(eta)    reversal rate = 2*a*b/(a + b) = m/cosh(eta)    minus m*sqrt(1-v^2): 0
(c) E^2 - p^2 = a*b    p/E - v = 0
    under a boost: a'b' - ab = 0   E' - (E cosh + p sinh) = 0   p' - (p cosh + E sinh) = 0
    arithmetic mean E, geometric mean m, harmonic mean (reversal rate): E * rev = a*b  (= m^2)
(d) a -> 0 (m = 0): forward fraction -> 1 , v -> 1 , reversal rate -> 0

Simulation (m = 1, T = 2e5 per run)
  eta    v_pred    v_sim     fwd_pred  fwd_sim   back_pred(1-v)/2  back_sim   rev_pred m*sqrt(1-v^2)  rev_sim
  0.0   0.00000  0.00431   0.50000   0.50215   0.50000           0.49785    1.00000                 1.00091
  0.5   0.46212  0.46543   0.73106   0.73272   0.26894           0.26728    0.88682                 0.88658
  1.0   0.76159  0.76231   0.88080   0.88115   0.11920           0.11885    0.64805                 0.64904
  2.0   0.96403  0.96349   0.98201   0.98175   0.01799           0.01825    0.26580                 0.26741
  boosted eta=0.5: a' = 0.6046 (pred 0.6065), b' = 1.6510 (pred 1.6487), a'b' = 0.9982, v' = 0.4639 (pred 0.4621), KS p(forward dwell exponential) = 0.62
  boosted eta=1.0: a' = 0.3667 (pred 0.3679), b' = 2.7221 (pred 2.7183), a'b' = 0.9982, v' = 0.7626 (pred 0.7616), KS p(forward dwell exponential) = 0.62

Discrete-tick chain, flip probs pa=0.02, pb=0.05: forward fraction pb/(pa+pb) = 0.71429, v = 0.42857, reversals/tick = 2 pa pb/(pa+pb) = 0.02857, sqrt(pa pb) sqrt(1-v^2) = 0.02857
```
