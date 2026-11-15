# RESULTS: the grammar's clock

## Preregistration

SPEC.md frozen at SHA-256 `0536577d5b53790332e645f3b7810a1ec2eda00b3d6b73da75f599a57ca095d3` (31 Oct 2026), before any new simulation code ran.

## Verdicts

| Claim | Verdict | Numbers |
|---|---|---|
| **C1** (a verified cycle with span <= 2?) | **Yes** | K1b draw **19387** (closed, m=8, kr=2, kc=4, span 1.82, period 6.352) and draw **33538** (open, m=6, kr=2, kc=3, span 1.83, period 4.844). All 8 starts periodic and verified in both. |
| **S1** (CV ~ Omega^(-1/2)) | **Holds** | slope **-0.576** over Omega in {50, ..., 3200} (7 sizes), bootstrap 95% [-0.589, -0.563], inside [-0.65, -0.35]. Note: the bootstrap interval excludes -0.5 itself; the steepening comes from Omega = 50 (over Omega 400-3200 alone the slope is about -0.55, descriptive only). |
| **S2** (Omega*) | **Omega* = 100** (N = 556) | N_coh = 3.9 at Omega = 50, 14.4 at 100 |
| **S3** (stall rate falls with Omega) | **Underdetermined** | zero stalls at every size |
| **S4** (phase-structured escape) | **Underdetermined** | zero stalls at every size (< 50 needed) |
| Harness H1, H2, P1, P2, P3 | **All pass** (pytest 6/6) | see harness table |
| Part L (family 149 Lean check) | **Underdetermined (blocked)** | see Part L |

K2 headline numbers:
- **Draw 12051, rate homotopy:** lambda_max = **0.12025**, where the span is **4.41** decades. The branch ends in a **fold of cycles**: it turns in lambda as the leading nontrivial Floquet modulus passes through 1 (0.77, then 1.79 on the other side, which is the unstable cycle). The period grows from 247.5 to 340.4 on the way. Just before the fold (lambda between 0.110 and 0.115), the balance turns stable through a complex pair (real part +0.001 to -0.0006). So the stable cycle and the stable balance coexist on about [0.112, 0.120]. lambda = 1 is not reached.
- **Draw 12051, total T:** the stable cycle was continued over **T in [1.268, 15.53]** (both directions stopped at their CPU caps), with constant period 247.528860 and amplitude proportional to T. This is exact: with x = C/(C+V+L+P), the closed-level vector field is homogeneous of degree 1 (every rate is linear in one species times a function of the scale-free x). Scaling T therefore scales the orbit and leaves the period unchanged, and the stable cycle exists for **all T > 0**. No bifurcation in T.
- **K1 cycles (revision R1, see Revisions):** draw 19387 has **lambda_max = 0.012300**, span **1.797**. Draw 33538 has **lambda_max = 0.103991**, span **1.637**. Both end at a **Hopf** point: the amplitude goes to 0 with log-log exponent **0.500** and **0.501**; the period stays finite and equals 2 pi / omega of the balance's complex pair (5.615290 against 5.615290, and 4.880664 against 4.880664); and that pair's real part crosses 0. Read in reverse, these clocks are **born at a Hopf point** as the span grows. On the other side, the branch continues stably to lambda = -0.031 (span 1.88) and -0.187 (span 2.17) at the CPU cap.

## K1: where clocks live

### K1 table (per sub-run and level)

| Sub-run | Level | Draws run | Unresolved (any start) | CPU-capped | Verified cycles | Fraction | 95% bound if none |
|---|---|---|---|---|---|---|---|
| K1a | closed | 14725 | 43 | 1 | 0 | 0.00e+00 | 2.0e-04 |
| K1a | open | 14725 | 4250 | 0 | 0 | 0.00e+00 | 2.0e-04 |
| K1b | closed | 20000 | 0 | 0 | 1 | 5.00e-05 | - |
| K1b | open | 20000 | 1197 | 0 | 1 | 5.00e-05 | - |

Cycles found:

| Sub-run | Draw | Level | m | kr | kc | Span | Period | C range | starts periodic / verified | nontrivial moduli |
|---|---|---|---|---|---|---|---|---|---|---|
| K1b | 19387 | closed | 8 | 2 | 4 | 1.82 | 6.3524 | [0.702, 1.532] | 8 / 8 | 2.3e-01, 3.3e-07 |
| K1b | 33538 | open | 6 | 2 | 3 | 1.83 | 4.8439 | [0.218, 1.293] | 8 / 8 | 5.9e-01, 2.4e-01, 3.7e-02 |

### Census (all-neighbours variants, PR 4 draws 0-41099 + K1a draws 41100-99999)

| Level | PR 4 draws | PR 4 cycles | K1a draws | K1a cycles | Total draws | Total cycles | Fraction |
|---|---|---|---|---|---|---|---|
| closed | 10275 | 1 | 14725 | 0 | 25000 | 1 | 4.0e-05 |
| open | 10275 | 0 | 14725 | 0 | 25000 | 0 | 0.0e+00 |

### K1c second pass

| Source | Level | Draws processed | CPU-capped draws | Starts re-integrated | Outcome of the second pass | Verified cycles |
|---|---|---|---|---|---|---|
| K1a | closed | 43 | 1 | 181 | balance 6, unresolved 175 | 0 |
| K1a | open | 4250 | 1 | 33028 | balance 13136, unresolved 19892 | 0 |
| K1b | open | 1197 | 0 | 8670 | balance 8307, unresolved 363 | 0 |
| PR4 | closed | 65 | 2 | 230 | balance 1, unresolved 229 | 0 |
| PR4 | open | 6032 | 0 | 46602 | balance 18400, unresolved 28202 | 0 |

K1 summary: `{"sub": {"K1b": {"complete": true, "note": "before restart"}, "K1a": {"complete": true, "note": "before restart"}, "K1c": {"complete": true, "done": 11535, "cpu": 1263.496000999999}}, "K1c_queue": {"closed": 108, "K1b": 1197, "open": 10282}, "K1c_resumed_skip": 52, "cpu_total": 3877.890626392999, "capped": 2, "wall": 659.0479502677917}`


Notes:
- K1 total CPU: 3878 s, within the 2 h cap. K1b, K1a and K1c all ran to completion. Five draws hit the 120 s cap: K1a closed draw 41199, the PR 4 stall draw, which the cap now handles as intended; and four K1c re-integrations (PR 4 draws 16817 and 29205, K1a draws 51795 and 57582). The `capped` count in `k1_summary.json` covers only the resumed part.
- A container restart at about 03:22 UTC killed K1c after 52 draws. It was resumed by skipping the finished draws (`K1C_RESUME`, logged in `evidence/k1_log.txt`). The CPU of the chunks in flight at the restart was lost from the tally (an undercount of at most about 2 x 50 draws).
- **C1 bound:** not needed, since there was a hit. In K1a (0 / 14 725 per level) the 95% upper bound on the hit fraction is 3/n = 2.0e-4. In the K1c second pass (0 new cycles from 11 587 re-integrated draws) every re-integrated end state went to a balance or stayed unresolved.
- The census confirms PR 4. On the all-neighbours count over draws 0-99 999, the closed level has 1 cycle in 25 000 draws (12051), and the open level has 0 in 25 000 (95% bound 1.2e-4). In the moderate-rate box (span <= 2) the hit rate is 1 / 20 000 per level, about the same per draw as the census closed level. So clocks are rare but not confined to extreme rates.

### K2 continuation

| Branch | Points | Parameter range | Period range | End | Span at end | Type | CPU-s |
|---|---|---|---|---|---|---|---|
| Tdown | 66 | [1.26827, 5.56151] | [247.5, 247.5] | cpu cap at p = 1.26827 | 5.012 | unclassified | 600 |
| Tup | 108 | [5.56151, 15.5283] | [247.5, 247.5] | cpu cap at p = 15.5283 | 5.012 | unclassified | 603 |
| lam12051 | 16 | [0, 0.120249] | [239.7, 340.4] | parameter turns (fold) at p = 0.120247 | 4.409 | fold of cycles | 181 |
| lamK1_0 | 9 | [0, 0.00849992] | [5.839, 6.352] | parameter turns (fold) at p = 0.00822882 | 1.805 | turn, unclassified (no Floquet modulus near 1) | 31 |
| lamK1_1 | 9 | [0, 0.100533] | [4.837, 4.879] | parameter turns (fold) at p = 0.100533 | 1.643 | turn, unclassified (no Floquet modulus near 1) | 25 |
| rev1_lamK1_0 | 224 | [-0.0313624, 0.0123002] | [5.615, 8.628] | cpu cap at p = -0.0313624 | 1.877 | unclassified | 603 |
| rev1_lamK1_1 | 228 | [-0.186599, 0.10399] | [4.837, 5.495] | cpu cap at p = -0.186599 | 2.168 | unclassified | 604 |


### K2 table notes

- `lamK1_0` and `lamK1_1` are the preregistered runs. Both stopped at the "parameter turns" rule with no Floquet modulus near 1, so they are unclassified under the preregistered rule. Their step size had grown to 0.2 near a Hopf point, and the branch folded back numerically.
- `rev1_*` are revision R1 runs (ds_max 0.01, no turn stop). They passed through amplitude 0 at the Hopf point and then traced the same family back to negative lambda, so their "parameter range" column spans both sides. The Hopf fits are in `evidence/k2_rev1_hopf_fit.json`.
- `Tup` and `Tdown` stopped at their CPU caps. Their classification is "unclassified" because no end was reached, which is consistent with the exact homogeneity argument above.
- K2 CPU: 181 + 603 + 600 + 31 + 25 + 603 + 604 = 2647 s, within the 1 h cap.

### K3 sizes

| Omega | N | Ticks | Tbar | CV | N_coh | Stalls | Stall rate / period | Visits to D | Events | CPU-s |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 56 | 1000 | 17.99 | 2.4274 | 0.17 | 0 | 0 | 1 | 1.21e+06 | 0.0 |
| 25 | 139 | 1000 | 83.59 | 1.0623 | 0.89 | 0 | 0 | 0 | 1.36e+07 | 0.4 |
| 50 | 278 | 1000 | 190.75 | 0.5045 | 3.93 | 0 | 0 | 0 | 6.23e+07 | 1.8 |
| 100 | 556 | 1000 | 240.33 | 0.2633 | 14.42 | 0 | 0 | 0 | 1.56e+08 | 4.3 |
| 200 | 1112 | 1000 | 249.09 | 0.1808 | 30.58 | 0 | 0 | 0 | 3.24e+08 | 8.9 |
| 400 | 2225 | 1000 | 252.38 | 0.1297 | 59.42 | 0 | 0 | 0 | 6.57e+08 | 17.7 |
| 800 | 4449 | 1000 | 248.22 | 0.0876 | 130.22 | 0 | 0 | 0 | 1.29e+09 | 34.4 |
| 1600 | 8898 | 1000 | 248.39 | 0.0595 | 282.51 | 0 | 0 | 0 | 2.58e+09 | 70.3 |
| 3200 | 17797 | 1000 | 247.69 | 0.0417 | 575.28 | 0 | 0 | 0 | 5.15e+09 | 138.1 |


K3 notes:
- The tick rule is preregistered. At small Omega it fires on noise: Tbar = 18.0 at Omega = 10 and 83.6 at Omega = 25, against 247.5 for the deterministic cycle. CV > 1 there, so the period is not well defined below Omega*. Because noise crossings keep ticking, no gap ever exceeds 5 x 247.53. That is why stalls are 0 at every size, and S3 and S4 are underdetermined, not killed.
- At Omega >= 100, Tbar is within 3% of 247.53. D (n_C = n_L = 0) was visited once, at Omega = 10.
- K3 CPU: harness 112 s, sizes 276 s (including the projections). The pytest rerun was about 50 s. Total well within the 3 h cap.

### Harness

| Check | Key numbers | Pass | CPU-s |
|---|---|---|---|
| P1 renewal | `[[0.05, 0.0499, 401.59], [0.3, 0.3016, 11.0]]` | True | 0.0 |
| P3 scripted stalls | `{"n_expected": 4, "n_found": 4, "phases_expected": [0.3, 0.72, 0.115, 0.55], "phases_found": [0.3, 0.72, 0.115, 0.55]}` | True | 67.6 |
| H1 drift | `{"omega": 100000.0, "N": 556151, "max_dev_C": 0.008294798469626663, "bound": 0.01146, "period": 246.77546761407237, "period_rel_err": 0.003048246216327848, "events": 160270341}` | True | 12.5 |
| H2 exact | `{"omega": 5, "N": 28, "n_states": 4495, "tv_pooled_exact": 0.001425237998322794, "tv_half_half": 0.003058235336849397, "events_per_chain": 10000000}` | True | 4.9 |
| H2 exact | `{"omega": 10, "N": 56, "n_states": 32509, "tv_pooled_exact": 0.0018515252074930765, "tv_half_half": 0.0049687144226502646, "events_per_chain": 10000000}` | True | 13.5 |
| P2 Brusselator quasi-cycles | `{"slope_all": 0.013, "cv": [[100, 0.45, 4.93], [400, 0.446, 5.03], [1600, 0.447, 5.01], [6400, 0.479, 4.36]]}` | True | 13.1 |

## Revisions log

- **R0 (code fix, no criterion changed).** The first K3 size sweep crashed before producing any result. The cost-projection run allocated its sample buffer for t_max = 1e9. It was fixed to t_max = 1e6/Omega, which still covers 1e6 events, and rerun. Only the buffer was wrong; no K3 result came from the failed run.
- **R1 (new claim, K2).** The preregistered continuations of the two K1 cycles stopped at the "parameter turns" rule with no Floquet modulus near 1: unclassified under the preregistered rule, and that result stays on the record (`k2_lamK1_*.json`). R1 reran them with ds_max = 0.01 and without the turn stop, classifying Hopf from the amplitude exponent and the balance's complex pair regardless of the end reason. R1 is what supports "Hopf" for these two; the preregistered verdict for them is "unclassified".

## Observational register

As analogy only: a stable cycle in this grammar resembles a bound, persisting oscillator, a "particle as a bounded trajectory". The finite-size threshold Omega* plays a role like the size below which such an object's identity (its ticking) cannot be told apart from fluctuation. No identification with any physical particle is claimed.

## Part L: family 149 (Lean)

**Underdetermined (blocked).** The setup step was denied by this session's permission policy before it ran. That step downloaded the elan installer and the Lean 4.34.1 tarball, cloned openai/math and the comparator tools, and built them. Nothing was built, and no axiom check or comparator run happened. 30 GB of disk was free, so disk was not the reason. Following the instruction not to work around a denial, no alternative route was tried.

## CPU table

| Part | CPU-s | Cap |
|---|---|---|
| K1 (K1b + K1a + K1c, children's CPU) | 3878 (plus lost in-flight chunks at the restart, < about 50 s) | 7200 |
| K1 smoke test (draw 12051 + 6 K1b draws, before launch) | about 95 | - |
| K2 (7 branches) | 2647 | 3600 |
| K3 harness | 112 | (in K3) |
| K3 sizes | 276 | (in K3) |
| K3 pytest rerun | about 50 | (in K3) |
| Part L | 0 | - |

Cores: Part K ran on cores 2-3 (taskset).
