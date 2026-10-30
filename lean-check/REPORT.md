# Lean check of openai/math: report

Status: SANDBOX / DRAFT. Not promoted. PHYS2 cloud campaign, task C (30 Oct 2026).

**What was checked.** The openai/math release at `4eaee87548250b2682affda7d05d947c05554bae` (29 Oct 2026). It was cloned outside this repository, into a scratch build directory, and was not modified. Lake's build scripts, which are third-party code, ran only in that directory.

**What is in this repository.** Reports, logs and the scripts that produced them. There are no build products.

## Verdicts

| Family | Config | Solution module and theorem(s) | Permitted axioms | `lake build` | `#print axioms` | Comparator | Scan (OAI/ and ComparatorChallenges/ closure) | Verdict |
|---|---|---|---|---|---|---|---|---|
| 149 | `MassAction` | `OAI.Analysis.MassAction.Main`: `OAI.Problem326.global_bounded_persistent_solution` | propext, Quot.sound, Classical.choice | **Stopped at the CPU cap**: 4732 of about 9000 jobs, 3.24 h wall, 6.27 CPU-h (see Budget) | not run (needs the build) | not run (needs the build) | 72 files, 7818 lines. One `sorry`, the placeholder in the challenge file (line 54). No other hit. | **Underdetermined** |
| 131 | `SwitchChain` | `OAI.Probability.SwitchChain.Main`: `OAI.Problem315.switch_chain_main`, `…switch_chain_tv_bound`, `…switch_connectivity` | same | not run: needs all of Mathlib, over the cap | not run | not run | 166 files, 22 862 lines. Three `sorry`, one placeholder per theorem in the challenge file. No other hit. | **Underdetermined** |
| 186 | `SharpThreshold` | `OAI.Combinatorics.SharpThreshold.Main`: `OAI.Problem313.sharp_threshold_width` | same | not run: same reason | not run | not run | 79 files, 7762 lines. One `sorry`, the challenge placeholder. No other hit. | **Underdetermined** |
| 176 | `SecondKahnKalai` | `OAI.Combinatorics.GraphThreshold.Main`: `OAI.LeanBlast.SecondKahnKalai.secondKahnKalaiBounds` | same | **Success**: 3251 jobs, 1253 s wall, 2425 CPU-s | `[propext, Classical.choice, Quot.sound]`, the permitted set; no `sorryAx` | **Accepted** (return code 0): "Lean default kernel accepts the solution … Your solution is okay!" 216 s wall, 319 CPU-s | 38 files, 6827 lines. One `sorry`, the challenge placeholder (line 68). No other hit. | **Verified** |
| 220 | `DirectionalBallisticity` | `OAI.Probability.Ballisticity.Main`: `OAI.DirectionalTransience.directional_transience_implies_ballisticity` | same | not run: needs all of Mathlib, over the cap | not run | not run | 514 files, 98 512 lines. One `sorry`, the challenge placeholder. No other hit. | **Underdetermined** |
| 229 | `ThreeStateSupercritical` | `OAI.Probability.ThreeState.Main`: `OAI.ThreeState.regular_supercritical`, `…poisson_supercritical` | same | not run: same reason | not run | not run | 28 files, 7799 lines. Two `sorry`, one placeholder per theorem. No other hit. | **Underdetermined** |
| 229 | `ThreeStateTreeClauses` | `OAI.Probability.ThreeStateClauses.Main`: `OAI.ThreeState.TreeClauses.Tree.regular_reconstructs_above_KS`, `…poisson_reconstructs_above_KS` | same | not run: same reason | not run | not run | 32 files, 7896 lines. Two `sorry`, one placeholder per theorem. No other hit. | **Underdetermined** |

**The scan.** Each target's import closure was taken within OAI/ and ComparatorChallenges/, from the solution and challenge modules. Comments were stripped before matching. The patterns were `sorry`, `admit`, `axiom` declarations, `@[implemented_by]`, `unsafe` and `native_decide`.
- In all seven closures, the only hits are the `sorry` proof placeholders of the challenge statement files. Their number equals the number of theorems in each config.
- No hit occurs outside a challenge file, and every other pattern counts zero.
- Per-file counts are in `logs/static_scan.json`.
- The scan reads source text, so it is weaker than `#print axioms`: it cannot see a `sorry` produced by a macro or an elaborator.

**Family 229.** Its config exists; `docs/229.md` links two, `ThreeStateSupercritical` and `ThreeStateTreeClauses`, and both are listed above.

**Family 220** has two more configs that were not among the targets: `DirectionalWalk` and `VelocityHemisphere`.

**The weaker definitional-equality check** was not needed for 176, because the comparator ran. For the other six it also needs the built environment, so it could not be done either.

## Why six targets are Underdetermined: the dependency closure against the CPU cap

The Mathlib cache was unreachable (`logs/network_check.txt`), so Mathlib had to be built from source. The closures were computed from real import headers, with comments stripped (`logs/closure_sizes.json`):
- Six targets import all of Mathlib, directly or through their solution files: 8530 Mathlib modules (2.39M lines), plus the packages under them.
- SecondKahnKalai imports 35 specific Mathlib modules, a closure of 2938 Mathlib modules.

**The first build.** It began at 03:37 UTC with MassAction. By 06:51 it had built 4336 of the 8530 Mathlib modules (1.31M lines) for 22 586 CPU-s (6.27 CPU-h), on 2 cores with `LEAN_NUM_THREADS=2`.

**The projection.** The remaining 4269 modules (1.03M lines), at the measured rate, project to about 4.8 CPU-h more: about 11.1 CPU-h for the first target's build alone, against the 10 CPU-h cap for the whole task. The other five closures need the same remainder.

**What was done.** The build was stopped by PID at 06:51. SecondKahnKalai was then built, since only 338 of its modules (99k lines) were still missing. Its build, `#print axioms` and comparator completed in 0.77 CPU-h.

The six whole-Mathlib targets are Underdetermined for budget, not because of any failure in their proofs. No build, axiom or comparator failure was observed in this session.

## Family 149 and the 12 October disagreement

**The positions.** The disagreement as given in the brief is DeepSeek's "sorry" against Astra. The release history decides one part of it at the level of source text:
- At every commit of the release (06, 07, 12, 26 and 29 Oct), family 149's 71 solution files under `OAI/Analysis/MassAction/` contain no `sorry` once comments are stripped.
- The only `sorry` anywhere in its closure is line 54 of `ComparatorChallenges/MassAction.lean`. That is the statement file, where `sorry` is the expected proof placeholder that the comparator replaces with the solution.

**Which side this supports.** It supports Astra's side, if a reading of "contains `sorry`" rested on that placeholder or on a raw grep of the tree. It does not establish that the proof is complete. That needs `#print axioms` (no `sorryAx`) and the comparator, and neither could run within the budget. **For 149 the verdict stays Underdetermined.**

**Comparison with 176.** SecondKahnKalai's closure has the same pattern: one challenge placeholder and no `sorry` in the solution. It was verified by both checks, which shows that the release's statement files carry `sorry` by design.

**formalization.yaml entry.** At this commit, `lean/formalization.yaml` has no entry for family 149. Its 208 `comparator_config` entries (out of 418 configs) do not include `MassAction`, nor the identifier `OAI.Problem326`, nor the 149 paper titles, and no earlier commit's yaml mentions MassAction either. Family 149 does have `docs/149.md` and a comparator config (`ComparatorChallenges/MassAction.json`). Among the seven targets, only `SecondKahnKalai` and `DirectionalBallisticity` have yaml entries.

## Environment (`logs/environment.txt`)

**Machine.** Linux 6.18.44, a Firecracker cloud container with 4 vCPUs (Xeon, 2.8 GHz) and 15 GB RAM. Task C ran on cores 0–1 (`taskset`), with `LEAN_NUM_THREADS=2` and `GLIBC_TUNABLES=glibc.malloc.mmap_max=0:glibc.malloc.arena_max=1`.

**Lean.**
- Lean 4.34.1 (commit 5045d005), with Lake 5.0.0, the release's `lean-toolchain`.
- `elan` could not download the toolchain from release.lean-lang.org (blocked). The GitHub release tarball was fetched instead (allowed) and linked with `elan toolchain link`.
- Mathlib is at `d13f23b723b8a846827a245b89c10fc7d3f11612`, as pinned by the release.

**Comparator tools**, at their last commits pinned to Lean v4.34.0; HEAD needs Lean ≥ 4.35, where the comparator moved into Lake:
- comparator `d03acab154d269c06e60e4de7e4cc85deebff94b`;
- lean4export `076e8e57707e813375e8f9da8bf989799ace9680`;
- landrun `ec104f6` (v0.1.18, Go 1.24.7).

**Landlock** is available: `CONFIG_SECURITY_LANDLOCK=y`, ABI version 7. The comparator ran with its landrun sandbox.

**The release's own patches.** The release's `lakefile.lean` applies compatibility patches to 11 git dependencies, at configuration time (`run_cmd`) and after `post_update`: belyi, elliptic-curves, formal-schemes, genl, heights, iut, oka, orbicurve-cores, pi1, tate-curves-theta and tempered-fundamental-groups. Lake therefore warns that those packages "have local changes". This is the release's own build behaviour; nothing in the release was patched for this check.

**Network** (`logs/network_check.txt`).
- Blocked:
  - lakecache.blob.core.windows.net (the Mathlib cache);
  - mathlib4.lean-cache.cloud;
  - release.lean-lang.org;
  - reservoir.lean-lang.org (all refused at the proxy);
  - github.com web pages and codeload (403).
- Reachable: GitHub release assets, raw.githubusercontent.com, and git over HTTPS, which fetched the release and its 41 git dependencies.

## Budget (CPU-hours; cap 10)

| Item | CPU-h |
|---|---|
| MassAction build (stopped) | 6.27 |
| SecondKahnKalai: build 0.674, `#print axioms` 0.004, comparator 0.089 | 0.77 |
| Tool builds (comparator, lean4export, landrun), toolchain unpacking, scans | not timed; a few CPU-minutes |
| **Total** | **≈ 7.1** |

## Files

| Path | Content |
|---|---|
| `logs/build_MassAction.log.gz`, `logs/build_MassAction.json` | The stopped MassAction build (log, and wall time, CPU and return code −15) |
| `logs/SecondKahnKalai/` | Build log (gz), `axioms.log`, comparator log (gz), probe file, records |
| `logs/static_scan.json` | Configs, closures, scan counts and hits for all seven, family 229's configs, the yaml check, and 149 over the release history |
| `logs/closure_sizes.json` | Import-closure sizes and unbuilt modules per target |
| `logs/network_check.txt`, `logs/environment.txt` | As named |
| `logs/pipeline_stdout_SecondKahnKalai.txt` | Pipeline summary line |
| `scripts/` | `c_pipeline.py` (build, axioms, comparator, scan), `c_static.py` (no-build steps), `timed.py`, `c_chain.sh` |
