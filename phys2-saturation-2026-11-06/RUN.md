# RUN log

SPEC.md SHA-256 (declared before checks.py was written): cc7ac93a1740b46be66acd2418567917823264359693a8d63c409801def9eb09
Recorded: 2026-11-06T16:16:22Z

## R1 — declared 2026-11-06T16:17:15Z, before checks.py was written or any check run

N1's planted failure, as declared (dC += k3·C², dV unchanged), is not guaranteed to grow without bound in the declared rate box: when D/k3 is large compared with the Contact a run reaches, creation never outruns the losses. Its flag rate would then measure the planted model, not the checker. R1 keeps the declared planted model and reports its flag rate with no criterion. It adds a second planted model, replication faster than every Contact loss: dC += (2·(k1 + k2 + k7) + 1)·C, dV unchanged. That model is unbounded by construction, and the ≥ 95% criterion moves to it. No other line of the SPEC changes.

## Results (run 6 Nov; checks.py unchanged from its first version)

- N0 harness: pass (19387 period 6.352409, 33538 period 4.843917).
- N1: 2400/2400 runs completed, 0 violations; planted R1 flagged 200/200 (pass); planted as declared flagged 173/200 (reported).
- N2: pass (max relative error 6.4e-16).
- N3: kr = 1 one balance in 910/910 open and 971/971 closed draws (kill not met); kr >= 2 three balances in 73/4090 open, 59/4029 closed; planted cubic 3 roots.
- N4: 0/300 sign changes (kill not met). Exploratory lag table in result_N4.json.

Added after the run, report only (not declared): example_stability.py (eigenvalues at N3's three-balance example); diag_n1_mean.py (why N1's second-half mean Contact departs from the throughput pin in some runs; S2 was declared as cited, not tested).

## Report-only diagnosis (after the run; not declared)

diag_n1_mean.py and diag_n1_followup.py, run on the 600 first starts of N1. Over the declared window, 83 runs have mean C more than 5% off the pin. 79 of them are below the pin and still filling: the window identity holds to 1e-6, and all 79 move toward the pin over [10, 20] x t_end. The other 4 come from sampling: the 2001-point grid is too coarse for the k3·C² motion, and integrating ∫C dt restores the identity to 1e-11. N1's bound check runs at output times only, as declared. No declared result changes.

## Jev claim-ledger pass (6 Nov, after filing; wording only)

The pass ran from ~/GENERAL/phys2-claim-ledger with --model jev-1.13.0 on 62 claims. Output is in ledger-out-saturation/ there. The note was revised for wording and scope: S1's hypotheses were restored in the plain-words summary, open-level scope was added where a result holds only there, exploratory results were marked as such, the reason for R1 was corrected, and N3's "never two" was dropped. That count is forced odd by the method, so it was not a finding. No proof, check or number changed. SPEC.md is unchanged.
