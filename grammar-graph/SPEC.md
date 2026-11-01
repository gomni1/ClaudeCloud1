# SPEC: the grammar on a graph (PHYS2, 1 Nov 2026)

Preregistration. This file is frozen by recording its SHA-256 in RESULTS.md before any simulation
code runs (stochastic or mean-field). After the freeze no target, grid, threshold or criterion changes;
a revision is a new claim, logged in RESULTS.md, and every failure stays on the record. Code bug fixes
are logged in RESULTS.md as bug fixes.

**Register.** The continuous-time Markov chain below is an effective-register summary of step
processes; it is not claimed to be the underlying process, only a coarse-grained description of it.
Time is the simulator's clock. Labels are neutral: C (Contact-active), V (Void-active), L (Loosened),
P (persistence-locked).

## 0. Fixed inputs (the whole rule; nothing is added)

- Graph G fixed during a run. Each site i holds one role. x_i = (number of graph neighbours of i in
  role C) / deg(i) (all-neighbours count). F_j(x) = Pr[Bin(m, x) >= j].
- Rates at site i: C->L k1; C->V k2 + k11 F_kc(x_i); C->P k7; V->C k10 + k3 F_kr(x_i); L->V k5;
  L->C k6; P->V k8. No other transition, no mobility, no extra rate.
- Draw 19387 (PR 7), closed level, m = 8, kr = 2, kc = 4, rates (k1, k2, k3, k5, k6, k7, k8, k9, k10,
  k11, k12) = (1.1104700305441388, 3.392924979396869, 6.841291178912343, 0.24399914028161648,
  0.2564493936497987, 4.507911093539853, 3.4671282746997387, 9.305812659924678, 0.17271135353305755,
  0.10361090436515946, 6.769536427560776); k9, k12 unused.
- Rate homotopy (PR 7): ln k(lam) = (1 - lam) ln k + lam mean(ln k), the mean over the 9 rates in use.
- T0 = 6.3524 (well-mixed period at lam = 0) is the unit "period" at every lam.
- Code reuse: the xoshiro256** RNG and the propensity conventions (rate order, threshold tables) of
  `grammar-clock/csrc/ssa.c` (PR 7, itself from PR 3) are copied with an attribution header into
  `grammar-graph/csrc/gg.c`; the selection structure is new (per-site sum tree).

## 1. Simulation (exact)

- General graphs: Gillespie direct method over sites. Each site's total exit rate is held in a binary
  sum tree (parents recomputed from children on every update); a site is chosen with probability
  proportional to its rate, then its transition with probability proportional to the transition rate.
  When a site enters or leaves C, every neighbour's rate is recomputed. Threshold values are tabulated
  exactly for each (degree, C-neighbour count).
- K (complete graph): the chain is lumped exactly on the role counts (all sites exchangeable). For a C
  site x = (n_C - 1)/(N - 1); for any other site x = n_C/(N - 1).
- Initial roles i.i.d. from the well-mixed balance fractions at the run's lam. Seeds are fixed
  functions of (part, class, lam index, replicate).

## 2. Graph classes (combinatorial; no coordinates)

- K: complete graph. R: random 8-regular graph by the configuration model with sequential rejection
  (Steger-Wormald: pick two random free stubs; pair them unless that makes a self-loop or a multi-edge;
  restart the whole pairing if no admissible pair remains). C0: ring circulant, N sites in cyclic order,
  each joined to the 4 nearest on each side. C5: C0 rewired Watts-Strogatz style: each edge (i, i+j),
  j = 1..4, with probability 0.05 has its far end moved to a uniformly chosen site that is not i and
  not already a neighbour of i.
- S: random triangulation of the sphere. Start from a tetrahedron with consistently oriented faces.
  Insert vertices into uniformly chosen faces (face -> 3 faces, orientation kept) until N vertices.
  Then 20 E flip attempts (E = 3N - 6), each on a uniformly chosen edge; an attempt is rejected if the
  new edge already exists or an endpoint of the old edge has degree 3. Rejected attempts count toward
  the 20 E. S is topologically two-dimensional by construction. It is a declared comparison class, not
  an assumption about the substrate.
- Planted sphere (harness only): an n x n grid of square cells on labels (i, j), each cell split by
  the diagonal (i, j)-(i+1, j+1), plus one apex vertex joined to every boundary vertex. The labels are
  combinatorial; no graph is built from points in a space. P1-P3 use n = 60.
- Reported for every graph: N, mean degree, mean local clustering coefficient (degree < 2 counts 0),
  diameter (exact, BFS from every vertex), and d_g = slope of ln M(r) against ln r, where M(r) is the
  mean over vertices of the radius-r ball size, over integer r from 2 to floor(diameter/2) (n/a if fewer
  than 2 radii).

## 3. Well-mixed references

The mean-field ODE of the rule on K (fractions c, v, l, p). At each lam: the balance (c*, v*) (interior
fixed point, continued by Newton from lam = 0); at lam where a stable cycle exists, s_c and s_v = the
time standard deviations of c and v over one period of the attracting cycle. For lam past the Hopf
point (the cycle is absent), s_c and s_v are those at lam = 0. Expected at lam = 0: period 6.3524,
balance (0.0812, 0.6332, 0.1801, 0.1055), c in [0.0545, 0.119], v in [0.5445, 0.7235]; Hopf at
lam_H = 0.0123. A mismatch is logged as a bug or discrepancy before any harness verdict.

## 4. Measurements

- Local fields: for each site j, filtered indicators y_j^C, y_j^V obey dy/dt = (1[role_j = C] - y)/0.6,
  integrated exactly between events, y(0) = initial indicator. c_i, v_i = means of y^C, y^V over the
  radius-2 ball of i (including i). (Equal to filtering the ball fractions; the filter is linear.)
  Frames every 0.4 time units (t = 0.4, 0.8, ...). Phases and amplitudes are computed in double
  precision; quantisation to 256 levels is used only for stored snapshots.
- phi_i = atan2((v_i - v*)/s_v, (c_i - c*)/s_c); a_i = sqrt(((c_i - c*)/s_c)^2 + ((v_i - v*)/s_v)^2).
- Triangles: on S and the planted sphere, the faces of the triangulation, oriented by the construction
  (non-facial 3-cycles are excluded so that the total-winding identity holds). On R, C0, C5: all
  3-cliques, oriented (i < j < k); their total winding is reported, not tested. On K: not enumerated;
  all local fields coincide (the radius-2 ball is the whole graph), so every winding is 0; the count
  C(N, 3) is reported.
- Winding: w = (1/2pi) sum over the three oriented edges (a -> b) of wrap(phi_b - phi_a), wrap into
  (-pi, pi]; an exact tie at +-pi is +pi if index(a) < index(b), else -pi (antisymmetric). A defect is a
  triangle with w != 0. Identity: on S and the planted sphere the sum of w over all faces is 0 in every
  frame; it is checked on every frame of every run, and any violation fails the harness.
- Triangle distance D(T, T') = min over vertex pairs of the hop distance in G.
- Tracks: a defect d (sign s) at frame f continues to d' at frame f+1 iff d' is the only sign-s defect
  at f+1 with D <= 2 from d, and d is the only sign-s defect at f with D <= 2 from d'. Otherwise d's
  track dies at f and d' starts a new track. (Same-sign matching within hop distance 2; identity is
  kept only when unambiguous. Nearest-first greedy matching would keep identities on pure noise at
  density 1/4, which P2 forbids.) Only frames in the analysis window are tracked. Lifetime = (last frame
  - first frame) x 0.4. "Lasting at least 20 periods": lifetime >= 20 T0 = 127.048. Tracks present in
  the first (last) analysed frame are left- (right-) censored; their observed lifetime is used for D1.
- Replacement: for each track lasting >= 20 periods, B = union of the radius-2 balls of the three
  vertices of its triangle at its first frame; reported value = fraction of sites in B that changed role
  at least once between its first and last frames.
- Global (analysis window, frames): A = std of the global C fraction / s_c; coherence Rbar = mean over
  frames of |mean_i exp(i phi_i)|; defect density = mean over frames of (defects / triangles); longest
  track; mean global (c, v).

## 5. Harness G1 (must pass before G2 or G3 results count; cap 0.5 CPU-hours)

- H1 (mean field): K, N = 10^4, lam = 0, 130 periods; discard the first 30. Global C fraction sampled
  every 0.05. Period = mean interval between upward crossings of 0.0868 (re-armed when the series falls
  below 0.0768). Range = (mean over complete cycles of the cycle minimum, of the cycle maximum) of the
  series after a centred moving average over 0.2 time units. Pass: |period - 6.3524| <= 3% of 6.3524,
  and each range endpoint within 10% (relative) of 0.0545 and 0.119.
- H2 (exactness): k3 = k11 = 0, lam = 0. Graph simulator on one S graph (N = 10^4) and lumped K
  (N = 10^4). Snapshots at t = 100, 150, ..., 2050 (40 snapshots). Pooled role counts against the exact
  stationary distribution of the four-state chain: chi-square with 3 degrees of freedom, pass if
  p >= 0.001, and every pooled role fraction within 4 standard errors.
- H3 (exactness with interaction; added here): graph simulator on the octahedron (6 sites, 4^6 states),
  lam = 0, full rule. Time-weighted mean of each role fraction and of (n_C/6)^2 over a run of 2 x 10^5
  time units, standard errors by 50 batch means, against the exact stationary values from the
  4096-state generator. Pass: every quantity within 4 standard errors.
- P1 (planted defects): planted sphere, phi = sum_k s_k arg((i - i_k) + sqrt(-1) (j - j_k)) on grid
  vertices, apex phase = circular mean of the boundary phases. Vortex points at centroids
  (i0 + 2/3, j0 + 1/3) of lower triangles (i0, j0), (i0+1, j0), (i0+1, j0+1). One fixed configuration
  (+ at (15,15), (45,30), (20,45); - at (30,15), (45,45), (15,30)) and 20 random neutral configurations
  of 2, 4 or 6 vortices, pairwise label distance >= 10 and >= 12 from the boundary; configurations
  whose boundary phases span an arc >= pi are redrawn (test-setup validity). Expected: w = s_k on the
  face containing vortex k, 0 elsewhere. Pass: detector output equal to expected in every
  configuration, and the identity holds in every frame.
- P2 (planted noise): phases i.i.d. uniform at every vertex and frame, 3970 frames (the G2 analysis
  window), 3 replicates, on the planted sphere and on one S graph (N = 10^4). Exact expectation of
  density = 1/4 (three independent uniform phases wind with probability 1/4). Pass: |mean density -
  1/4| <= 4 standard errors (from per-frame densities), the identity holds, and D1's criterion FAILS
  (fewer than 2 of the 3 replicates have a track lasting >= 20 periods).
- P3 (planted motion): planted sphere; lower face L(i, j) = (i, j), (i+1, j), (i+1, j+1); upper face
  U(i, j) = (i, j), (i+1, j+1), (i, j+1). The + vortex sits at the centroid of the faces L(14,20),
  U(15,20), L(15,20), U(16,20), ... (moving right); the - vortex at the centroids of L(46,26), U(46,26),
  L(45,26), U(45,26), ... (moving left); each advances one face every 5 frames, 64 faces, 320 frames;
  the pair passes at label distance >= 5.6. Pass: exactly two tracks, each spanning all frames (lifetime
  >= 20 periods), each on the planted face in every frame, no identity swaps.

## 6. G2 (main, class S; cap 3 CPU-hours)

N = 10^4; lam in {0, 0.006, 0.02}; 3 replicates (replicate r uses S graph r at every lam). Run 300 T0
(1905.72 time units); analysis window t > 50 T0 (frames 795..4764, 3970 frames). Pooled over the 3
replicates unless stated.
- D1 (persistent localised integer), lam = 0: PASS if a track lasts >= 20 periods in >= 2 of 3
  replicates; KILL if no track lasts 20 periods in any replicate; otherwise underdetermined.
- D2 (cores at local zeros), lam = 0: ratio = (mean over defect-frames of the mean amplitude of the
  defect triangle's three vertices) / (mean over frames and all triangles of the same). PASS ratio <=
  0.5; KILL ratio > 0.5; UNDERDETERMINED if fewer than 1000 defect-frames.
- D3 (pairing is local), lam = 0: births = first frames of non-left-censored tracks; deaths = last
  frames of non-right-censored tracks. An event (sign s, triangle T, frame f) is paired if an
  opposite-sign birth or death exists at frame f-1, f or f+1 with D <= 3. PASS if >= 80% of births and
  >= 80% of deaths are paired; KILL if either fraction < 50%; otherwise (or with no events)
  underdetermined.
- D4 (report only): over tracks lasting >= 20 periods, MSD(tau) = mean of D(T(f), T(f + tau))^2 over
  all f, at lags tau = 0.4 n, n in round(geomspace(1, 318, 20)); exponent = slope of ln MSD against
  ln tau over T0 <= tau <= 10 T0.
- Per lam: A, Rbar, mean global (c, v), defect density, longest track, number of tracks >= 20 periods,
  mean replacement fraction.

## 7. G3 (comparison; cap 1.5 CPU-hours)

Classes K, R, C0, C5 at lam = 0, N = 10^4, 2 replicates, same run length and window as G2. Report
Rbar, A, triangle count, defect density, longest track. C-report (no kill): which classes host defect
tracks lasting >= 20 periods.

## 8. Order, budget, evidence

G1 before G2, G2 before G3. CPU time measured with getrusage and logged per part against the caps; a
part stops at its cap and reports what it has. Evidence (gzipped): per-run JSON summaries, per-frame
global series, long-track tables, and a few quantised phase snapshots.
