# MAP-SNAPSHOT-2026-11-13

Plain-text dump of the PHYS2 Premise Map (artifact 114a6536-717c-418f-8a0d-e9aa349cb796, version 1794517273-62fd) as read by the night run on 13 Nov 2026. Fields: id | type | shelf | code | title | promoted | merged-into | deps | x (collisions) | tests. For tomorrow's diff. The version string differs from 12 Nov's (1794437936-384c).

Node count: 180. By type: {'assumed': 12, 'cand': 28, 'conseq': 38, 'floor': 10, 'known': 54, 'open': 19, 'outcome': 19}. By shelf: {'archive': 60, 'live': 97, 'reserve': 15, 'reservoir': 8}.

Changed since the 12 Nov snapshot: one node added, E_ntau (conseq, live). K_restless retitled and its code changed ('Astra · 11 Nov · night run 12 Nov'). Text dated 12 Nov added to C_seed, P_period, O_drift, K_mid and K_restless. No node removed; no type or shelf changed.

F_ladder | floor | live | P2.7-03 §§1–3 | Ladder principle |  |  | deps= | x= | tests=
F_identity | floor | live | P2.6-03 §1 | Identity = invariant of the parallel organisation |  |  | deps=F_time | x= | tests=
F_persist | floor | live | settled | Persistence is identity through replacement |  |  | deps= | x= | tests=
F_time | floor | live | P2.1 DD3/DD4 · P2.3 DD2 | Time is co-emergent, not added after space |  |  | deps= | x= | tests=
F_foot | floor | live | P2.1 hard floor · placed 2 Nov | The foot of the ladder: the timeless possibility structure |  |  | deps= | x= | tests=F_cv,F_ladder,F_same,F_time,P_fedbelow,P_hex
F_same | floor | live | settled | Perfect sameness cannot seed difference |  |  | deps= | x= | tests=
F_OP | floor | live | P2.7-03 §6 | Observed Permissibility = retention, not selection |  |  | deps= | x= | tests=
F_monism | floor | live | axiom · P2.1, restated 4 Oct | Monism — one substrate, nothing outside it |  |  | deps= | x= | tests=
F_relational | floor | live | axiom | Relational primacy; labels are not physical |  |  | deps= | x= | tests=
F_cv | floor | live | P2.3 → Reinterpretation 02 | Contact and Void are scale-relative roles |  |  | deps= | x= | tests=
A_RA1 | assumed | live | RA1 v0.1 | RA1 — common local probabilistic dynamics |  |  | deps=F_persist,F_same | x= | tests=
A_posit | assumed | live | P3A-09 RA2 | Renewal Posit: persistence = sufficiency against a rate over a window |  |  | deps=F_persist,F_identity,F_time | x= | tests=
A_rates | assumed | live | decision | Demands are sustained rates |  |  | deps=A_posit | x= | tests=
A_avgsus | assumed | live | cl. 3–5 | Formation read on AVG, maintenance on SUS |  |  | deps=A_posit,A_rates | x= | tests=
A_share | assumed | live | amended 15 Sep | Shared supply within aggregate capacity; each unit counted once |  |  | deps=A_posit,K_alloc | x= | tests=
A_A3 | cand | live | A3 v0.1 · demoted 5 Oct | A3 Selection — minimise Σ τ(e)·f(e) |  |  | deps=F_ladder,F_OP,A_avgsus | x= | tests=
A_admit | assumed | live | starting point · 5 Oct | Admitted arrangements; some ignorance retained |  |  | deps=F_OP,F_ladder | x= | tests=A_A3
A_rung | assumed | live | P3-04 | The active rung is the composite rung |  |  | deps=F_ladder | x= | tests=
A_steps | assumed | live | principle · 26 Sep | Steps at every scale; smoothness is coarse-graining |  |  | deps=F_time,F_persist | x= | tests=
A_pattern | assumed | live | adopted 31 Oct · merged | The thing is the pattern: the substrate hosts capacity, the pattern carries bias |  |  | deps=F_monism,F_persist,F_identity,A_steps,F_cv | x= | tests=C_turnoverloop,O_own
A_occ | conseq | archive | if floor · 25 Sep | Occupancy is not substrate — follows from the floor |  | →K_little | deps=A_A3,K_little,F_identity,F_persist | x= | tests=
K_slack | known | reserve | P3A-04 | Equal total slack is not equal capacity to respond |  |  | deps= | x= | tests=
K_alloc | known | live | P3A-05/06 | Two-role allocation condition |  |  | deps= | x= | tests=
K_energy | known | reserve | P3A-08 | Irrecoverable loss bounds renewal count |  |  | deps= | x= | tests=
K_markov | known | live | P3A-10 | Preparation-erasing Markov sufficiency eliminated |  |  | deps= | x= | tests=A_RA1
K_kinetics | known | live | P3A-10A/B | Basins do not fix kinetics |  |  | deps= | x= | tests=P_stat
K_cut | known | live | P3A-11 | Boundary cut function complete — static, one commodity |  |  | deps= | x= | tests=
K_gap | known | live | k ≥ 3 | Multi-class: cut condition not sufficient |  |  | deps= | x= | tests=
K_horizon | known | live | r_AVG(H) | With a horizon, the static invariant fails at every channel count |  |  | deps=A_avgsus | x= | tests=
K_boundary | known | live | H¹ / m−n+1 | Boundary data does not fix interior structure |  |  | deps=K_cut,K_loop | x= | tests=
K_loop | known | live | P3A-10C · T1 | Loop state cannot be one scalar per participant | P:12 Oct |  | deps= | x= | tests=
K_Hstar | known | live | H* | Formation window diverges as slack vanishes |  |  | deps=A_avgsus,K_horizon | x= | tests=
K_afford | known | live | F1 §2 | Window feasibility implies affordability |  |  | deps=A_avgsus | x= | tests=
K_route | known | live | AVG | Route preference is window-invariant under AVG |  |  | deps=A_avgsus | x=C_C1 | tests=
K_T1step | known | live | T1 at step level · proved 26 Sep | Step-level invariance: only participant moves preserve compatibility | P:12 Oct |  | deps=K_loop,A_steps | x= | tests=
C_turnoverloop | conseq | live | if relation-level turnover | Relation-level turnover generates loop state |  |  | deps=K_T1step,O_own | x= | tests=
K_A3 | known | archive | A3 §4 | A3 ranks; it cannot create |  | →A_A3 | deps=A_A3 | x= | tests=
K_little | known | live | Little | Σ τf = mean response activity in progress |  |  | deps= | x= | tests=
C_C1 | outcome | archive | C1 · refuted | Shorter window changes the route, not just throughput |  |  | deps=A_posit,A_avgsus | x=K_route | tests=
C_C2 | outcome | archive | C2 · struck 26 Sep | Maintenance has a reach |  |  | deps=A_avgsus | x= | tests=
C_C3 | outcome | archive | C3 · struck 26 Sep | Formation degrades smoothly; maintenance cuts off |  |  | deps=A_avgsus,C_C2 | x= | tests=
C_asym | conseq | archive | if one process · 26 Sep | Formation has the edge; maintenance has the tail |  | →G_onedyn | deps=C_oneprocess,A_avgsus,A_steps | x= | tests=
P_stepform | cand | archive | 26 Sep | Formation is stepped: gears meshing |  | →G_onedyn | deps=C_oneprocess,C_asym,P_ladder_sieve | x= | tests=
C_bottleneck | conseq | archive | if stepped · 26 Sep | Bottlenecks set the pace |  | →G_onedyn | deps=P_stepform | x= | tests=
C_lossy | conseq | live | cl. 11 | Cross-scale reduction is lossy | P:31 Oct |  | deps=K_cut,K_gap,K_horizon | x= | tests=
C_band | conseq | archive | regimes | Maintainable-but-not-formable band exists |  | →G_onedyn | deps=K_Hstar,A_avgsus | x=P_growth | tests=
G_onedyn | conseq | live | collapsed 12 Oct · one process | One dynamics: formation and maintenance differ by start and horizon |  |  | deps=K_Hstar,A_avgsus,E_bounds,F_same,A_steps,K_horizon,P_growth,P_ladder_sieve | x= | tests=O_formdyn,C_seed,P_growth
C_A3f | conseq | archive | if A3 | No metastable higher-burden persistence |  | →A_A3 | deps=A_A3 | x=P_growth | tests=
R_grammar | outcome | archive | retired | Compact trans-scalar grammar |  |  | deps=C_lossy | x= | tests=
R_S1 | outcome | archive | RA1-S1 | Four-operations toy law — 0/20 |  |  | deps=A_RA1 | x= | tests=
R_service | outcome | archive | assignment | Service-model composite |  |  | deps=A_A3,A_rung,A_share | x= | tests=
R_config | outcome | archive | stopped | Configuration-requirement candidate |  |  | deps=A_A3,R_service | x= | tests=
R_R01 | outcome | archive | R01 | Detailed-balance occupation as renewal mechanism |  |  | deps=K_kinetics | x= | tests=
R_OPform | outcome | live | F3 stop | Formation pass 01 |  |  | deps=K_afford,O_own | x= | tests=
R_ordertest | outcome | archive | Q12 test · 5 Oct | Order test in the toy grammar — framing rejected |  |  | deps=O_Q12 | x=F_identity | tests=
O_own | open | live | OPEN | State ownership through replacement |  |  | deps=F_persist,K_loop | x= | tests=
O_composite | open | live | OPEN | What makes a composite |  |  | deps=R_service,A_rung | x= | tests=
O_credit | open | reserve | OPEN | Credited boundary transaction criterion |  |  | deps=R_service | x= | tests=
O_substrate | open | reserve | OPEN | Response-to-substrate map |  |  | deps=K_little | x= | tests=
O_Q12 | open | live | P2.7-Q12 | Non-commuting refractory order |  |  | deps= | x= | tests=
O_disp | open | reserve | UNVERIFIED | Dispersion rate law |  |  | deps=K_loop | x= | tests=
O_common | open | reserve | unasked | Commonality at programme level |  |  | deps=A_RA1,K_markov,R_S1 | x= | tests=
O_formdyn | open | live | OPEN | Dynamical formation |  |  | deps=K_afford,R_OPform | x= | tests=
O_sat | open | archive | IN WORDS · 13 Oct | The saturation mechanism itself |  | →K_sat | deps=P_growth,F_monism | x= | tests=O_ratelaw,P_growth
O_regime | open | archive | UNDECIDED | Two readings or two engines? |  | →G_onedyn | deps=C_band | x= | tests=P_growth
O_S1cause | outcome | archive | dropped 22 Sep | Why RA1-S1 ran away |  |  | deps=R_S1 | x= | tests=
O_focus | open | live | FOCUS · 23 Sep | Why is the set of persistent closures discrete? |  |  | deps=K_sat,G_species,F_persist,F_identity | x= | tests=
O_scale | open | live | OPEN · 24 Sep | Where do the large pure ratios come from? |  |  | deps=P_numbers,O_focus,F_time | x= | tests=
O_CVG | open | reserve | CVG-C1 | Nested window hierarchy |  |  | deps= | x= | tests=
O_H1B | open | reserve | H1-B′ | Six-item pre-run gate |  |  | deps= | x= | tests=
O_A3audit | known | archive | P3A-14 · 26 Sep | A3 removability audit: A3 carries almost nothing on its own |  | →A_A3 | deps=A_A3 | x= | tests=
P_growth | cand | live | NOT ADOPTED | Self-limiting growth |  |  | deps=F_persist,F_ladder | x= | tests=A_A3
C_seed | conseq | live | if growth + ladder | Growth depletes the rung beneath |  |  | deps=P_growth,F_ladder | x= | tests=A_share,K_sat
C_decay | outcome | archive | dropped 22 Sep | Decay = persistence reorganising |  |  | deps=P_growth | x= | tests=
C_noage | conseq | archive | if growth + constant escape | Exponential lifetimes — no ageing |  | →G_lifetime | deps=P_growth | x=P_migrate | tests=
G_lifetime | conseq | live | collapsed 12 Oct · if growth + escape | Lifetimes: memoryless, ensemble-scaled, phase-structured when cycling |  |  | deps=K_persist,P_stat,P_traj | x=P_migrate | tests=P_growth,G_express,E_bounds
C_species | conseq | archive | if growth + data | The attractor does not drift; registration may cycle |  | →G_species | deps=C_noage | x= | tests=
C_mix | conseq | archive | observational register | Mixing is registration, not drift |  | →G_express | deps=C_species,P_traj,C_indist | x= | tests=
C_phase | conseq | archive | if cycling | Escape hazard depends on phase |  | →G_lifetime | deps=P_growth,P_traj | x= | tests=
C_indist | conseq | live | if identity = invariant | Indistinguishability follows | P:12 Oct |  | deps=F_identity,F_persist,F_relational | x= | tests=
C_expressed | conseq | archive | identity vs properties | Identity fixed, expressed properties environment-relative |  | →G_express | deps=C_indist,C_env,C_mix | x= | tests=
G_express | conseq | live | collapsed 12 Oct · identity vs properties | What varies is expression, not identity |  |  | deps=C_indist,G_species,P_traj,P_growth,C_seed | x= | tests=
C_ident | conseq | archive | if growth + data | One species per attractor |  | →G_species | deps=P_growth,C_species,C_indist,C_expressed,A_steps | x= | tests=
G_species | conseq | live | re-rooted 9 Nov · isolation half · if attractor = species | A species is an isolated invariant (read as shares and period) |  |  | deps=C_indist,A_steps,G_lifetime,K_bal | x= | tests=K_closedcount,O_drift,P_growth
C_env | conseq | archive | if growth + data | The bound is shared, and the interface is the dial |  | →G_express | deps=P_growth,C_seed | x= | tests=
C_silent | conseq | live | limit | Silent on which things are stable |  |  | deps=P_growth | x= | tests=
P_traj | conseq | live | follows from floor · re-rooted 12 Oct | A particle as a bounded trajectory | P:12 Oct |  | deps=K_persist,P_stat,F_persist | x= | tests=P_growth,E_bounds
P_migrate | outcome | archive | dropped 22 Sep | Migration through a family of balances |  |  | deps=P_traj | x= | tests=
P_numbers | cand | reservoir | 23 Sep | Not all numbers are equal under interaction |  |  | deps=O_focus | x= | tests=
P_generations | cand | reservoir | correlation · 24 Sep | Lepton generations as coexisting attractors |  |  | deps=G_species,O_focus | x= | tests=
P_spin | cand | reservoir | loose · 26 Sep | Spin as nested recurrence across rungs (wheels within wheels) |  |  | deps=O_Q12,F_ladder,F_persist | x= | tests=
P_ladder_sieve | cand | reservoir | shape · 24 Sep | The ladder as a sieve on the number landscape |  |  | deps=P_numbers,F_ladder | x= | tests=
C_oneprocess | cand | archive | cl. 3–5 · 24 Sep | One process, two times |  | →G_onedyn | deps=A_avgsus,K_horizon,P_growth | x= | tests=
P_occmass | cand | reservoir | bridge · 25 Sep | Occupancy as mass-like burden |  |  | deps=K_little,O_scale,A_A3 | x= | tests=
P_A3weak | cand | archive | weaker A3 | A3 as a statistical tendency |  | →A_A3 | deps=A_A3,P_growth | x= | tests=
P_void | cand | reservoir | exploratory | Contact/Void as saturation balance |  |  | deps=P_growth,F_cv | x= | tests=
P_period | cand | reservoir | conjecture | Emergent period |  |  | deps=F_time | x= | tests=
P_grains | cand | archive | Glenn's picture · 5–6 Oct | The thing is the pattern: a moving pattern is not moving grains |  | →A_pattern | deps=F_monism,F_persist,F_identity,A_steps,F_cv,P_motion | x= | tests=C_turnoverloop,O_own
C_cvrole | conseq | live | if grains + roles · 5 Oct | Contact/Void role is read off a grain's place among its neighbours |  |  | deps=A_pattern,F_cv | x= | tests=
P_super | cand | live | 5 Oct | Signals add; some lock into exclusions |  |  | deps=A_pattern | x= | tests=O_Q12
O_excl | open | live | OPEN · 5 Oct | Exclusion: is Pauli in the grain picture? |  |  | deps=P_super,A_pattern | x= | tests=P_spin
P_hex | cand | reservoir | mental model · P2.1, 5 Oct | The elongated hexagon: a mental model of the primitive |  |  | deps=A_pattern,F_relational | x= | tests=P_spin,O_excl,O_Q12
K_P0 | known | live | P0 · 6 Sep · provisional pass | P0: closure renewed through replacement in a network of fixed centres |  |  | deps=F_persist | x= | tests=O_Q12,A_pattern
K_replace | known | live | audits · Sep | Persistence through complete replacement is mechanically possible |  |  | deps=F_persist | x= | tests=F_identity,A_pattern
K_memory | known | reserve | Section 9 · 9 Sep | Static reduction is exact; dynamic reduction needs memory |  |  | deps= | x= | tests=C_lossy,R_grammar,K_boundary
K_spinledger | known | reserve | Appendix E · 9 Sep | Local accounts close only when rotation is included |  |  | deps= | x= | tests=A_pattern
K_coherence | known | reserve | Sections 6, 8 · Sep | Preserving labels is not preserving coherence |  |  | deps= | x= | tests=P_spin,O_excl
K_exclstat | known | reserve | GQ §9 · App I · Sep | Exclusion is not exchange statistics |  |  | deps= | x= | tests=O_excl,P_super
K_handed | known | reserve | P2.3 Addendum A · sandbox | Relational handedness needs three unlike interfaces |  |  | deps= | x= | tests=O_Q12,R_ordertest,P_spin
K_compat | known | reserve | Laminar Flow · GQ · 10 Sep | Transfer completes only within a compatibility margin |  |  | deps= | x= | tests=P_kernel
R_sbfclaims | outcome | archive | audits · Sep | SBF's quantitative claims, closed as stated |  |  | deps= | x= | tests=
P_motion | cand | archive | P2.3 · working picture | Motion: the substrate hosts capacity, the pattern carries bias |  | →A_pattern | deps=F_persist,F_identity,F_cv | x= | tests=
P_kernel | outcome | archive | audit synthesis · 11 Sep · retired 7 Oct | One handoff build with a complete ledger |  |  | deps=K_P0,K_replace | x=F_identity,P_stat | tests=
P_stat | assumed | live | adopted 12 Oct · ruling 6–7 Oct | The handoff is statistical: the count sits in a basin |  |  | deps=F_identity,F_persist | x=P_kernel | tests=
E_bounds | conseq | live | ext 149 · if cyclic | Cyclic, rate-proportional turnover stays within bounds |  |  | deps=P_stat | x= | tests=O_sat,P_growth,G_onedyn,K_kinetics,G_species,C_indist,G_lifetime,P_traj,A_A3
E_swap | conseq | live | ext 131 · if free swap | Free swapping keeps only the degree sequence |  |  | deps=F_persist,F_relational | x= | tests=P_stat,C_turnoverloop,O_sat,G_express,C_cvrole,C_indist
E_drift | conseq | live | ext 220 · if fixed medium | Biased re-locking in a fixed random medium: no net travel, or a definite velocity |  |  | deps=A_pattern | x= | tests=A_pattern,G_express,P_traj
E_ladder | conseq | live | ext 229 · if link copying | What survives a many-to-one ladder: fan-in × fidelity² > 1 |  |  | deps=F_ladder,C_lossy | x= | tests=R_grammar,A_pattern
E_switch | conseq | live | ext 186 · if free relations | Label-free properties switch on abruptly |  |  | deps=F_relational | x= | tests=O_formdyn,G_onedyn
C_deficiency | conseq | reserve | if 149 class · deficiency | Cycling needs a deficient turnover network |  |  | deps=E_bounds,G_species | x= | tests=G_species,G_lifetime,P_traj,P_period
C_siphon | conseq | archive | if 149 class · start | Formation needs a seed at a trapped absence |  | →G_onedyn | deps=E_bounds,F_same | x= | tests=C_band,O_formdyn,C_seed,P_growth
C_lifescale | conseq | archive | if 149 + small-number escape | Lifetime grows exponentially with the sustaining ensemble |  | →G_lifetime | deps=E_bounds,C_noage | x= | tests=C_phase,P_growth,C_env
C_moveinv | conseq | live | if 131 + identity | Identity must be an invariant of the turnover move |  |  | deps=E_swap,F_persist,C_indist | x= | tests=C_turnoverloop,C_cvrole,G_express,O_own,P_stat
K_cvgret | known | live | return-path audit · 12 Oct | As written, the Contact/Void turnover grammar is not in 149's class |  |  | deps=F_cv | x= | tests=O_sat,P_growth,G_onedyn
O_returns | outcome | live | inferred from necessity [model] | Three return paths would close the turnover grammar |  |  | deps=K_cvgret | x= | tests=P_growth,F_ladder,O_sat,O_formdyn,E_bounds
O_returns2 | cand | archive | inferred from necessity [model] · rulings of 1 Nov | Two return paths keep a level alive: seeding templated from below, and supply from below |  | →P_fedbelow | deps=K_cvgret,P_ready,F_cv | x= | tests=K_seedbelow,K_persist,K_clock,P_growth,E_bounds
P_fedbelow | assumed | live | adopted 2 Nov · merged from the two-path set and the readiness candidate | Each level is fed and seeded by the level beneath it |  |  | deps=F_cv,F_ladder,A_pattern,K_cvgret | x= | tests=K_ladder,K_persist,K_clock,P_growth,P_ladder_sieve,P_spin,C_seed,K_medium
O_ratelaw | open | live | OPEN · narrowed 13 Oct | What rate law do threshold triggers give over the ensemble? |  |  | deps=K_cvgret,P_stat | x= | tests=G_express
K_closedcount | known | archive | closed-grammar count · proved 13 Oct | One level of the closed grammar holds one balance, and every start goes to it |  |  | deps=O_returns,K_cvgret | x= | tests=G_species,C_deficiency,O_sat,O_focus,P_traj
P_names | assumed | live | Astra · method · adopted 26 Oct | Nothing acts because of what we call it |  |  | deps=F_relational,F_identity,P_stat,K_boundary | x= | tests=O_own,A_A3,C_moveinv,O_ratelaw
N_whole | cand | live | P2.9A-02 · 20 Aug | A nucleon as one closed recurrence with a three-sector envelope |  |  | deps=F_identity,F_persist,F_ladder,A_pattern | x= | tests=O_composite
N_strata | cand | live | P2.9A-02 §25 | U and D as symmetry strata of the section-state space |  |  | deps=N_whole | x= | tests=P_spin
N_charge | conseq | live | if three equal sectors · binary | Charge from three sectors: 2 : −1 only at baseline one | P:3 Nov |  | deps=N_whole,N_strata | x= | tests=
N_conv | outcome | archive | §27 rider · failed under unrestricted moves · 31 Oct | The integer invariant changes only at a symmetry-restoring section |  |  | deps=N_whole,N_strata,K_strata | x= | tests=C_decay
N_stab | conseq | live | if phase cancellation · toy · 26 Oct | Phase cancellation favours the nucleon with two pinned registrations |  |  | deps=N_strata | x= | tests=N_charge
K_strata | known | live | section strata · PR #2 · 27 Oct | A half-twist needs an even-symmetry section, and is protected only by rigidity |  |  | deps= | x= | tests=N_strata,N_conv,N_stab,N_whole,P_spin,N_zero
O_protect | open | live | OPEN · fork 28 Oct | Is the integer's passage forbidden or rare? |  |  | deps=K_strata,N_whole | x= | tests=N_zero,G_lifetime
R_twistcharge | outcome | archive | §18 · retired 27 Oct | Charge as the unpaired half-twist (P2.9A-02 §18) |  |  | deps=N_strata | x=N_charge | tests=
K_exit | known | archive | exit-time run · computed 28 Oct | In the closed grammar, dissolution is exponentially rare in the ensemble; switching expression is nearly free |  |  | deps=K_closedcount,O_returns,O_ratelaw | x= | tests=G_lifetime,G_express,O_protect
P_idsize | cand | live | reading of the exit-time run · 29 Oct | Identity gains content with size: below a threshold, persisting and being replaced look the same |  |  | deps=K_exit,F_ladder,F_persist | x= | tests=G_lifetime,C_indist
E_cavity | conseq | live | ext · PRB 23 Oct · if model holds | A cavity's mode polarisation can reverse which phase of a Kondo lattice gains |  |  | deps=G_express | x= | tests=P_dial,K_handed
P_dial | cand | live | Astra · Watch · 30 Oct · not adopted | The dial has a direction: surroundings may select among organisations by orientation |  |  | deps=G_express,E_cavity | x= | tests=
K_tot | known | live | instability search · PR #4 · 30 Oct | Counting all neighbours, one level can keep time and form patterns; counting only Contact and Void, it cannot |  |  | deps=O_ratelaw,P_fedbelow | x= | tests=P_traj,G_lifetime,P_idsize
P_idroutes | cand | archive | for further exploration · 31 Oct | Identity and size, through coupled routes: which change of expression risks identity depends on its direction |  |  | deps=P_idsize,K_exit,F_persist | x= | tests=G_express,F_ladder
P_idroutes2 | cand | archive | new candidate · 1 Nov | Identity and size, through coupled routes — tested on the whole distribution |  |  | deps=P_idsize,K_exit,F_persist | x= | tests=P_idroutes,G_express
P_idroutes3 | cand | archive | third candidate · killed 1 Nov | Identity and size, through coupled routes — tested on the unconditioned distribution |  |  | deps=P_idsize,K_exit,F_persist | x= | tests=P_idroutes,P_idroutes2,G_express
N_zero | cand | live | recast §27 rider · 31 Oct | The integer invariant changes only at a local zero of the mode that carries it |  |  | deps=N_whole,N_strata,K_strata | x= | tests=C_decay,O_protect
K_decayledger | known | live | P2.8-A1 · decay ledger | Conservation closes the decay ledger; the energy released does not set the rate |  |  | deps=F_persist,F_identity | x= | tests=N_zero,O_protect,G_lifetime,E_bmumu,P_count,P_stepbal
E_bmumu | conseq | live | ext · observational benchmark · LHCb, 3 Nov | Two near-equal parents reach the same daughters at rates thirty times apart |  |  | deps= | x= | tests=K_decayledger,N_zero,O_protect,G_lifetime,G_express,P_count
P_count | cand | live | Claude · 4 Nov · new candidate after the Q⁵ failure | Counted by daughter arrangements, a decay's rate is a count times a weight per arrangement |  |  | deps=K_decayledger,A_admit | x= | tests=K_decayledger,E_bmumu,E_pilnu
E_pilnu | conseq | live | ext · observational benchmark · 4 Nov | One parent, two daughter pairs: the pair with fewer arrangements wins eight thousand to one |  |  | deps= | x= | tests=P_count,K_decayledger
E_ntau | conseq | live | ext · observational discriminator · 12 Nov | Beam and bottle disagree on the neutron's lifetime, and the beam's field has never been varied |  |  | deps= | x= | tests=K_decayledger,G_lifetime,G_express,N_whole
P_stepbal | cand | live | Claude's prompt · run 6 Nov · SANDBOX/DRAFT | A pattern's steps all go at full speed; its velocity is their imbalance, and a decay reads their directions |  |  | deps=A_steps,F_persist,P_count | x= | tests=E_pilnu,P_count,K_decayledger
K_telegraph | known | live | prior art · re-derived 6 Nov | In one dimension, two flip rates give a pattern its mass, a slowed clock and E² − p² = m² |  |  | deps=A_steps,F_time | x= | tests=P_stepbal,P_occmass
K_clock | known | live | clock run · PR #7 · 31 Oct | Clocks exist at moderate rates, are born at a Hopf point, and keep time in proportion to their size |  |  | deps=K_tot,O_ratelaw,P_fedbelow | x= | tests=G_lifetime,P_idsize,P_traj,G_express,P_period
K_medium | known | live | collapsed 2 Nov · PR 8, Claude Science, Claude | One level pulls itself into one clock, and its windings do not last |  |  | deps=K_clock,K_persist | x= | tests=P_traj,A_pattern,N_zero,K_strata,P_hex,G_lifetime,P_fedbelow
K_persist | known | live | persistence proof · 1 Nov | One level of the grammar persists under threshold rates, whatever the neighbour count |  |  | deps=P_fedbelow,K_cvgret,O_ratelaw | x= | tests=P_fedbelow,G_lifetime,P_growth,K_sat
K_sat | known | live | saturation · proved 6 Nov | Growth pays for itself in Void: with seeding, a level is bounded under any recruitment law; on a closed level, cycling needs a route through L or P |  |  | deps=P_fedbelow,K_cvgret,O_ratelaw | x= | tests=P_growth,C_seed,G_express,P_traj,O_focus
K_bal | known | live | night run N-5 · proved 9 Nov | One level holds at most three balances under threshold recruitment |  |  | deps=K_sat,P_fedbelow,O_ratelaw | x= | tests=G_species,O_focus,G_express,O_drift
O_drift | open | live | OPEN · split 9 Nov | Does a species' attractor drift in the working grammar? |  |  | deps=G_species,G_lifetime | x= | tests=O_focus,G_express
K_mid | known | live | night runs 10–11 Nov · DeepSeek 11 Nov | The middle of three balances is always unstable, on open and closed levels |  |  | deps=K_bal,P_fedbelow,O_ratelaw | x= | tests=O_drift,G_species,O_focus,K_sat,P_period,K_restless
K_restless | known | live | Astra · 11 Nov · night run 12 Nov | Closed levels with no stable balance can tick: five verified clocks |  |  | deps=K_mid,P_fedbelow,O_ratelaw | x= | tests=P_period,K_clock,O_drift,G_species,O_focus,P_traj,A_admit
K_lock | known | archive | coupled levels · computed 1 Nov | Through supply alone, a ticking level entrains the level above only near equal speeds |  | →K_ladder | deps=K_clock,F_ladder | x= | tests=P_ladder_sieve,P_spin
P_ready | cand | archive | inferred from Glenn's picture · 1 Nov | A lower organisation is recruitable upward in proportion to how Contact-active it is |  | →P_fedbelow | deps=F_cv,F_ladder,A_pattern | x= | tests=P_ladder_sieve,P_spin,C_seed
K_ready | known | archive | readiness coupling · computed 1 Nov | Coupled through readiness, levels lock strongly; at partial strength, the upper level locks slower at 1:2, 1:3 and 1:4 |  | →K_ladder | deps=P_ready,K_clock,K_lock | x= | tests=P_ladder_sieve,P_spin
K_ladder | known | live | collapsed 2 Nov · Claude, SPEC2 and SPEC7–12 | A level is set by three things: throughput, the coordination beneath it, and its own |  |  | deps=P_fedbelow,K_clock,F_ladder | x= | tests=P_ladder_sieve,P_spin,F_cv,K_persist,G_lifetime,P_idsize,C_lossy,K_medium
K_seedbelow | known | archive | seeding from below · computed 1 Nov | With seeding templated from below, a level keeps its Contact on any coordination beneath it and loses it on none; its Void reserve takes the strain |  | →K_ladder | deps=P_ready,O_returns2,K_ready,K_clock | x= | tests=O_returns2,P_ready,F_cv,K_persist
K_seedfinite | known | archive | finite size · computed 1 Nov | At finite size a weakly based level keeps its Contact, more steadily than a fully coordinated one; between the two, noise sets off bursts |  | →K_ladder | deps=K_seedbelow,O_returns2 | x= | tests=O_returns2,P_ready,G_lifetime,P_idsize
K_seedfinite2 | known | archive | both levels finite · computed 1 Nov | With both levels at finite size, a weakly based level keeps its Contact and keeps its base's time |  | →K_ladder | deps=K_seedfinite,O_returns2 | x= | tests=O_returns2,P_ready,G_lifetime,P_idsize,F_ladder
K_ladder3 | known | archive | three levels · computed 1 Nov | Up a weakly coordinated ladder, the bottom level's rhythm reaches two levels up while coordination thins |  | →K_ladder | deps=K_seedfinite2,O_returns2 | x= | tests=O_returns2,P_ready,F_ladder,C_lossy
K_literal | known | archive | literal readiness · computed 2 Nov | Taken literally, readiness carries a rhythm up only if the lower organisations are already in step; the level above does not pull them into step |  | →K_ladder | deps=P_ready,O_returns2,K_ladder3 | x= | tests=P_ready,O_returns2,K_ladder3,K_sync,F_ladder
R_inherit | outcome | archive | inheritance route · killed 2 Nov | Inheritance alone does not carry a rhythm up a weakly coordinated ladder: inherited phase erodes before the organisations leave |  | →K_ladder | deps=K_literal,P_ready | x= | tests=P_ready,K_ladder3,O_returns2
K_graph | known | archive | grammar on a graph · PR #8 · 1 Nov | With one unit per site, a level does not keep time on a sparse graph, and its phase defects are noise |  | →K_medium | deps=K_clock,K_persist | x= | tests=P_traj,A_pattern,N_zero,K_strata
K_patches | known | archive | coupled patches · Claude Science · 1 Nov | Ensembles at every site tick, but coupling through the count damps them, and no winding persists |  | →K_medium | deps=K_clock,K_graph | x= | tests=P_traj,N_zero,A_pattern
K_sync | known | archive | noiseless coupled clocks · computed 1 Nov | Without noise, coupling through the count pulls a level of clocks into one clock, and every winding annihilates |  | →K_medium | deps=K_clock,K_patches | x= | tests=P_traj,N_zero,A_pattern,P_ready
K_twist | known | archive | twist at the Hopf point · computed 1 Nov | The grammar's medium has a twist: near the clock's birth, its period depends on amplitude and its coupling is dispersive |  | →K_medium | deps=K_clock,K_sync | x= | tests=P_hex,P_traj,N_zero
K_bigsphere | known | archive | large medium · computed 1 Nov | At weak coupling, windings in the grammar's medium last tens of periods, then annihilate; the twist does not hold them |  | →K_medium | deps=K_sync,K_twist | x= | tests=P_traj,N_zero,A_pattern,P_hex
K_phase | known | archive | phase-structured escape · Claude Science · 1 Nov | A clock's excursions are phase-structured, and more sharply so as it grows |  | →K_medium | deps=K_clock | x= | tests=G_lifetime
K_tradeless | known | live | timing–extent trade · run 10 Nov | With positive-weight turnover, sharper timing does not cost extent: driving harder narrows both |  |  | deps=K_telegraph,P_stepbal | x= | tests=
O_signed | open | live | shaped gap · logged 10 Nov | Signed or phased handoff contributions |  |  | deps=K_tradeless | x= | tests=
