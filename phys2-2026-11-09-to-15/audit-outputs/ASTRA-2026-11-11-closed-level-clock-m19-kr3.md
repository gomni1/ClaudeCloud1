# Astra — a closed level with no stable balance: balances, long integrations, limit cycle

Received 11 Nov 2026 (relayed by Glenn). Answers the second verification handoff of NIGHT-REPORT-2026-11-11 (§8): the closed level with rho = k3 · P[Bin(m, x) ≥ kr], T = 1, m = 19, kr = 3,
(k1, k2, k3, k5, k6, k7, k8, k10) = (0.47205648482747253, 0.026204658014680544, 33.767749788910784, 0.04225910243329335, 0.030726928960954643, 36.36991748036593, 59.878770174623746, 0.8229214570079602).

Section 1 is Claude's note. Section 2 is Astra's summary as received (its tables re-laid as Markdown; its LaTeX kept). Astra's own files, Astra_Closed_Turnover_Audit.md and Astra_Turnover_Reproducibility.zip, are on Glenn's side and were not read by Claude.

## 1. Claude's note (11 Nov 2026)

**Reproduced.** Independent integration (scipy, LSODA, rtol 1e-10, atol 1e-12): the same three balances (Contact share 0.028813617, 0.051069697, 0.060222280); the same restricted eigenvalues (largest real parts +0.0089, +23.52, +24.60); and from two starts, (0.25, 0.25, 0.25, 0.25) and (0.02, 0.18, 0.70, 0.10), one cycle of period 43.548384 with Contact between 0.011698 and 0.3025 and Void between 0.272784 and 0.768553.

**Astra's correction, accepted.** The night report's "bounded with no stable balance, so the level must keep moving" is too strong: exact balances are stationary, and exceptional starts on their stable manifolds converge to them. Claude repeated that wording on the Premise Map on 11 Nov; corrected the same night.

**Exploratory nudges (Claude, not preregistered; numpy seed 11).** Every rate multiplied by 1 + pct·u, u uniform in [−1, 1], 12 samples at each of pct = 0.5%, 2%, 5%; one start, (0.25, 0.25, 0.25, 0.25), integrated to t = 3000.
- Still ticking: 8, 7 and 4 of 12. Periods 37.9–41.5 (±0.5%), 34.1–41.3 (±2%), 27.0–38.7 (±5%).
- In all 36 samples the level ticks exactly when it has no stable balance: 19 tick (17 with three unstable balances, 2 with a single unstable balance), 17 rest (11 with one stable balance, 6 with three balances of which the low-share one is stable).
- The nine resting samples at ±0.5% and ±2% were re-run from six starts each: every start rests. No resting state beside a ticking one was found.
- Reading: the clock occupies an open region of rates, and this draw sits near its edge. Its low-share balance is unstable by only 0.0089, and a 0.5% change of rates stops the clock in a third of samples.

**Claude's error, logged.** Before running these nudges Claude told Glenn that the clock "passes" a robustness test because it is strongly attracting. Strong attraction guarantees survival only under small enough changes, and here "small enough" is below 0.5% in some directions.

## 2. Astra's summary, as received

Worked for 11m 7s

Confirmed: exactly three balances, all unstable. All 12 tested non-equilibrium starts converge to the same stable relaxation limit cycle, with period approximately 43.548384 model time units.

Controls passed before the turnover integrations.

- Stuart–Landau, \(\mu=1\): recovered period \(0.999999999998\) and nontrivial multiplier \(0.135335283236\), agreeing with \(e^{-2}\). Maximum multiplier error: \(2.7\times10^{-12}\).
- Planted failure, \(\mu=-1\): correctly classified as decay to equilibrium, not a cycle. Radau independently confirmed this.
- The stabilized Floquet procedure was also checked against the analytic \(\log\lambda=-2\).

### Balances and restricted stability

Coordinates are ordered \(C,V,L,P\).

| Balance | C | V | L | P |
|---|---|---|---|---|
| Low | 0.028813617441 | 0.767325505996 | 0.186359700678 | 0.017501175885 |
| Middle | 0.051069696692 | 0.587604164553 | 0.330306786670 | 0.031019352085 |
| High | 0.060222279987 | 0.513695614495 | 0.389503542745 | 0.036578562773 |

The eigenvalues of \(M\), excluding the conserved-total mode, are:

| Balance | Restricted eigenvalues |
|---|---|
| Low | \(-59.043829547,\quad 0.008922660009\pm0.798616608520i\) |
| Middle | \(-58.490444412,\quad23.520922907,\quad-0.008335834365\) |
| High | \(-58.030558474,\quad24.597498277,\quad0.011287195379\) |

Thus Claude's instability claim is correct. Maximum equilibrium residual was \(1.2\times10^{-15}\).

Root completeness was checked using the analytic shape of \(H''\): \(H\) has precisely two extrema in the physical interval, giving three monotone intervals, each containing one root. There are no boundary balances.

### Long integrations and classification

I tested:

- Both perturbations \(y_* \pm10^{-6}(1,-0.3,-0.4,-0.3)\) of each balance.
- All four pure-role vertices.
- \((0.25,0.25,0.25,0.25)\).
- \((0.02,0.18,0.70,0.10)\).

Each LSODA run used rtol \(=10^{-10}\), atol \(=10^{-12}\), and lasted 21,774.191889 time units—approximately 500 periods. The conservative equilibrium-timescale requirement was only \(1,199.639959\).

Using upward crossings of \(C=0.041665100934\), over the final 200 returns:

- Worst within-run return-time range: \(4.77\times10^{-7}\).
- Worst return-point coordinate spread: \(1.67\times10^{-10}\).
- Spread between the final section points of all 12 starts: \(6.46\times10^{-11}\).

An independent full four-variable Radau integration agreed with the refined section state within \(3.2\times10^{-13}\).

These converged returns, a closed shooting solution, and the Floquet calculation identify a limit cycle, with no evidence of a torus or chaos on the observed attractor.

### Cycle measurements

Refined period:

\[
\boxed{\mathcal T=43.54838398633}
\]

| Role | Minimum | Maximum |
|---|---|---|
| C | 0.011697817869 | 0.302538526798 |
| V | 0.272783600522 | 0.768552745380 |
| L | 0.186097769037 | 0.509584840875 |
| P | 0.007108892982 | 0.179324681614 |

The extrema occur at different phases.

### Floquet multipliers

The full-system multipliers are numerically:

\[
\boxed{
1,\quad1,\quad
e^{-728.658094179},\quad
e^{-2509.648255052}
}
\]

Equivalently, the two contracting multipliers are approximately

\[
3.53029\times10^{-317},
\qquad
1.18471\times10^{-1090}.
\]

The two unit multipliers represent phase and conserved-total scaling. Within \(T=1\), only the phase multiplier remains neutral: the cycle is locally stable and isolated.

Both contracting multipliers are too small to resolve by ordinary eigenvalue extraction from the full monodromy matrix. I therefore used segmented variational propagation with transverse QR stabilization. Halving the segment length and tightening tolerances changed their logarithms by less than \(3\times10^{-8}\). Their sum also matched \(\int\mathrm{tr}(M)\,dt\) within \(4\times10^{-9}\).

### Confidence and qualification

Confidence is high in the numerical classification and the common attractor for these 12 starts. This is not an interval-certified proof, and finite sampling cannot exclude another attractor with an untested basin.

The statement "bounded, therefore trajectories must keep moving" needs correction: exact balances remain stationary, and exceptional trajectories on their stable manifolds converge to them. The supported conclusion is that every tested generic start reached the same stable cycle; no second attractor was found.

Astra_Closed_Turnover_Audit.md · Astra_Turnover_Reproducibility.zip
