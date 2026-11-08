# COUPLED CLOCKS ON A GRAPH — SPEC (preregistration)

A ticking ensemble at every site. Sites couple only through the count each unit
reads.

**Status.** Frozen. The SHA-256 of this file is recorded in `RESULTS.md` before
any production run. After the freeze no target, grid, threshold or criterion
here changes. A revision is a new claim, logged in `RESULTS.md`; every failure
stays on the record; bug fixes are logged as bug fixes.

---

## 1. Standing of the model

The Markov chain, its tau-leaping approximation, and the graph are **effective-
register summaries**. The graph is a **frozen neighbour relation** — the one
approximation named in advance.

No coordinates are used anywhere. Every graph is built combinatorially and every
dimension is **measured**, never set.

## 2. Model

Closed level of the grammar at each site `i` of a graph `G`. Site `i` holds
`Omega` units with counts `(C_i, V_i, L_i, P_i)` summing to `Omega`.

| transition | rate |
|---|---|
| C -> L | `k1 C_i` |
| C -> V | `(k2 + k11 F_kc(x_i)) C_i` |
| C -> P | `k7 C_i` |
| V -> C | `(k10 + k3 F_kr(x_i)) V_i` |
| L -> V | `k5 L_i` |
| L -> C | `k6 L_i` |
| P -> V | `k8 P_i` |

`F_j(x) = Pr[Bin(m, x) >= j]`. The count a unit at site `i` reads is

`x_i = (1 - w) * C_i/Omega + w * (mean over i's graph neighbours j of C_j/Omega)`

with `w` the share of a unit's neighbours lying at adjacent sites — a structural
variable of the neighbourhood, not a rate. At `w = 0` each site is an
independent copy of the well-mixed clock. No mobility, swap move or rate is
added.

Clock: draw 19387, `m = 8`, `kr = 2`, `kc = 4`, rates
`(1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678,
0.17271135353305755, 0.10361090436515946, 6.769536427560776)`;
`k9` and `k12` unused.

### 2.1 Deterministic facts, recomputed

Recomputed here with `DOP853` (`rtol=1e-12`, `atol=1e-14`) and frozen in
`deterministic.npz`, SHA-256
`016e6361f9084d01c771543b028b90a783a4ef27a8705518e20f3201fcfcedc5`:

| quantity | recomputed | stated |
|---|---|---|
| period `T` | 6.352409 | 6.3524 |
| balance `(c*,v*,l*,p*)` | 0.0812, 0.6332, 0.1801, 0.1055 | same |
| `c` range | [0.0545, 0.1190] | [0.0545, 0.119] |
| `v` range | [0.5445, 0.7235] | [0.5445, 0.7235] |
| winding of the cycle about the balance | 1 (sign -1 under the §4 phase convention) | once |
| `s_c` | 0.0213670 | — |
| `s_v` | 0.0614013 | — |
| mean scaled amplitude of the cycle | 1.37240 | — |

Period jitter across successive Poincare crossings is `1.9e-13`.

## 3. Graphs

Built combinatorially, `N = 2000` sites for all classes. The CPU projection
(§8) does not require a reduction to 1000, so **N = 2000 is declared**.

- **S**, random triangulated sphere: tetrahedron, then vertex insertion into
  uniformly chosen faces up to `N`, then `20*E` random edge flips, rejecting
  multi-edges and any flip dropping a degree below 3. Faces are kept
  consistently oriented throughout. Topologically two-dimensional by
  construction: a declared comparison class, not an assumption about the
  substrate.
- **R**, random 8-regular graph (pairing model repaired by double-edge swaps).
- **C5**, ring of `N` sites joined to the 4 nearest on each side, Watts–Strogatz
  rewiring 0.05.

**Triangle set.** For `S` it is the `2N-4 = 3996` oriented faces of the
triangulation. `R` and `C5` are not surfaces, so for them it is every 3-clique.

Measured (reported in `RESULTS.md`): `N`, mean degree, mean local clustering,
diameter, and the growth exponent `d_g` from mean ball size against hop radius,
fitted by least squares on log–log over radii whose mean ball size is at most
`N/2`.

## 4. Measurements

- Per site, from its own ensemble, **no spatial smoothing**: `c_i = C_i/Omega`,
  `v_i = V_i/Omega`, exponential time filter with time constant **0.3**,
  recorded every **0.2**.
- `phi_i = atan2((v_i - v*)/s_v, (c_i - c*)/s_c)`.
- `a_i = sqrt(((c_i - c*)/s_c)^2 + ((v_i - v*)/s_v)^2)`.
- **Winding** `w_t` on every triangle: `(1/2pi)` times the sum of the three
  wrapped phase differences around the triangle, in `{-1,0,+1}`. A **defect** is
  a triangle with `w_t != 0`.
- **Hop distance between triangles**: the least graph hop distance between a
  vertex of one and a vertex of the other.
- **Tracks**: strict same-sign matching within hop distance 2, unique in both
  directions — a pair is accepted only when each defect is the other's single
  same-sign candidate. An unmatched defect in the later frame is a **birth**; an
  unmatched defect in the earlier frame is a **death**.
- **Global synchrony** `R = |mean of exp(i phi)|`.

## 5. Simulation

Tau-leaping with declared step **`dt = 0.01`**, Poisson leaps clipped to keep
counts non-negative: when the draws leaving a species exceed its count, the
largest draw is decremented until they balance. It is validated against exact
Gillespie in H2.

Runs: **200 periods** (`1270.48` time units), **the first 30 discarded**
(`190.57`), leaving 170 periods and **5400 recorded frames**. Each site starts
at a uniformly random point of the deterministic cycle, rounded to integer
counts with the residue absorbed into `P`.

**Seed base `7000000`**; each run's seed is declared and recorded.

## 6. Harness — must pass before results count

- **H1.** At `w = 0` and `Omega = 800`, the median per-site period is within
  **5 %** of the exact-SSA period of one isolated site at `Omega = 800`,
  measured in H2.
- **H2.** One isolated site at `Omega = 200` and `800`, tau-leap against exact
  Gillespie: mean period and its coefficient of variation agree within **5 %**.
  Periods are taken from the same filter and phase definition in both, as
  successive crossings of multiples of `2pi` by the unwrapped phase.
- **H3.** Total winding over all triangles of `S` is **0 in every frame**.
- **P1.** Planted phase fields on a small combinatorial sphere with known
  windings, detected **exactly**:
  (a) a constant field, and any field whose every edge phase difference is below
  `2pi/3` in absolute value, must give winding 0 on every triangle — three
  wrapped differences each below `2pi/3` cannot sum to `+-2pi`;
  (b) the oriented tetrahedron with phases `(0, 2pi/3, 4pi/3, 0)` on vertices
  `(0,1,2,3)` must give exactly `+1` on face `(0,1,2)`, `-1` on face `(1,3,2)`
  and `0` on the other two.
- **P2.** Independent uniform phases: defect density **1/4** (tolerance `+-0.01`
  over at least 200 frames of `S`), and **no track reaches 20 periods**.

## 7. Main part, class S

Grid: `Omega` in `{200, 800}`; `w` in `{0.05, 0.2, 0.5}`; **2 replicates** each
— 12 runs.

- **E1 (sites tick).** At `Omega = 800`, `w = 0.05`: the median over sites of
  the time-averaged site amplitude is at least **0.5** of the deterministic
  cycle's mean amplitude (`1.37240`), i.e. at least `0.68620`.
- **D1 (persistent localised integer).** At some grid point, a defect track
  lasts at least **20 periods** (`127.05` time units, 636 frames) in **both**
  replicates. **Kill:** no track reaches 20 periods at any grid point.
- **D2 (cores at local zeros).** For tracks lasting at least **5 periods** (159
  frames), the mean amplitude on their triangles — the mean of `a_i` over the
  three vertices of each occupied triangle, over the track's frames — is at most
  **0.5** of the mean over all triangles and all frames. **Kill:** above 0.5.
  **Underdetermined:** no such tracks.
- **D3 (pair births and deaths are local).** At least **80 %** of births, and
  at least 80 % of deaths, have an opposite-sign partner of the same kind — a
  birth for a birth, a death for a death — within hop distance **3** in the same
  or an adjacent frame. **Kill:** under **50 %**.
- **D4 (motion; report only).** Mean squared hop displacement of tracks lasting
  at least 20 periods against lag, for lags 1 to 100 frames, with the exponent
  from a log–log least-squares fit over lags with positive mean square.

Reported per grid point: `R` over time, defect count over time, the longest
track, and the D4 exponent.

## 8. CPU projection and cap

Total cap **4 CPU-hours**. Measured cost of one full `S` run at `N = 2000`,
`Omega = 800`, `dt = 0.01`: **89 CPU-seconds** for 127,048 leaps. Twelve main
runs plus four comparison runs project to **0.40 CPU-hours** of simulation, so
`N = 2000` is kept. Measurement and harness are added to the reported total.

### 8.1 Disclosed pre-freeze calibration

The leap step was chosen before the freeze by comparing `dt` in
`{0.01, 0.005, 0.002}` against exact Gillespie at `Omega` in `{200, 800}` over
2000 periods. All three passed the 5 % bar; the largest, `dt = 0.01`, is
declared. Errors at `dt = 0.01`: period 1.79 % (`Omega = 200`) and 1.21 %
(`Omega = 800`); CV 0.59 % and 0.26 %. The reference exact-SSA periods measured
there were 4.5083 (`Omega = 200`) and 5.2324 (`Omega = 800`), with CV 0.5156 and
0.4488. H1 and H2 are re-run after the freeze with declared seeds and their
post-freeze values are the ones that count.

## 9. Comparison, classes R and C5 — report only, no kill

`Omega = 800`, `w` in `{0.05, 0.2}`, 1 replicate each. Report `R`, defect
density and the longest track.

## 10. Disclosed expectation

Coupled noisy oscillators on surface-like graphs, started with random phases,
often form point defects that drift and annihilate in pairs while the rest
synchronises. On expander-like graphs global synchrony is likely. Whether this
grammar's coupling — through the recruitment count — synchronises or
desynchronises sites is not known in advance.

## 11. Observational register

Read as analogies only, and only here: a persistent `+-1` winding that moves and
annihilates with its opposite is the sort of thing one would call a *point
defect* or a *vortex*, its conserved integer the sort of thing one would call a
*topological charge*, and the surrounding synchronised region the sort of thing
one would call an *ordered phase*. No claim about any named particle is made or
implied anywhere in this document.

## 12. Deliverables

`SPEC.md` (frozen), `grammar.py`, `graphs.py`, `sim_patches.py`, `measure.py`,
`harness.py`, `run_patches.py`, `analyse_patches.py`, `RESULTS.md` with the
verdict table and per-grid-point tables, compressed evidence, `README.md` and a
one-page `REPORT.md`.
