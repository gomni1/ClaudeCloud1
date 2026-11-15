# PHYS2 Night Run — specification v2.1 (10 Nov 2026)

Working draft. Glenn may edit this file; the run follows the version it finds each night.

v2.1 (10 Nov): one change, on Glenn's word ('I want to find the current standing constraints file … the night run must be able to find it'). The Sources line for the standing constraints now says how to find the current copy: Drive's exact-title search (`title = '…'`) did not return it on 10 Nov, and a plain `title contains` search lists the SUPERSEDED copies alongside it. Nothing else changed. v2 is kept in this folder as SUPERSEDED-2026-11-10-NIGHT-RUN-SPEC-v2.md.

v2 (9 Nov): three changes after the first night's review, on Glenn's word ('do the lot'). Receipts are uploaded with hashes (Phase 3, Phase 4); planted failures must be guaranteed analytically (Planted failures); bound and threshold checks run while the solver runs (Numerics). v1 is kept in this folder as SUPERSEDED-2026-11-09-NIGHT-RUN-SPEC-v1.md.

## Purpose
While Glenn sleeps (~06:15–10:45 London), make bounded progress on PHYS2 by finding cracks we can exploit later. We are not trying to break down the wall. Any improvement in position counts: a crack located, a gap given a shape, an if-then proved, a link shown to rest on less than it seemed, or a place shown solid at the depth asked. Glenn reviews the report with Claude the next day and decides whether anything changes on the Premise Map.

## Sources (read in Phase 1)
- PHYS2 project instructions (attached to the claude.ai Project "Phys2.0 C") — they govern all formal work.
- PHYS2-STANDING-CONSTRAINTS.md (Drive, Audit Outputs, folder ID 1kGNcWdpF8B1ePsZ7Sh33XJYLrz4RVyfW). Source documents win over it in a disagreement. How to find the current copy: search `title contains 'STANDING-CONSTRAINTS' and parentId = '1kGNcWdpF8B1ePsZ7Sh33XJYLrz4RVyfW'`, then take the one file whose title is exactly PHYS2-STANDING-CONSTRAINTS.md; every other match begins SUPERSEDED and is not current. Do not rely on `title =` search; it missed the file on 10 Nov. As of 10 Nov the current copy is file ID 1YmP6SlxdqBu2_oVM0zDfmIJ6xa74R9Xk (last amended 7 Oct), with the Drive description "CURRENT standing constraints". The ID changes whenever the file is replaced, so the title rule wins over the ID. If no file has that exact title, say so in the report and stop (see the last line of this spec).
- PHYS2 Premise Map artifact: https://claude.ai/code/artifact/114a6536-717c-418f-8a0d-e9aa349cb796 (read with the Artifact tool, action "read").
- PHYS2 narrative spine artifact: https://claude.ai/code/artifact/d79ab1c1-d5cb-41b2-a681-c70075ecc4a7 (context only).
- Night-Reports folder: STEERING.md, the most recent NIGHT-REPORT, the most recent map snapshot, and any REVIEW notes Glenn left. Ignore files whose names begin SUPERSEDED.
- Other Audit Outputs documents only as an item needs them.

## Hard limits
- Write only into the Night-Reports folder (and the session's own scratch space). Never edit the Premise Map, the standing constraints, project instructions, project docs or memory. Never use the phys2-premise-map-update skill.
- Never promote, close an open question, change terminology or declare a milestone. Those are Glenn's acts. Recommend; don't enact.
- Never send messages or emails, never share or delete files, never spend money.
- Do not use the word "canon".
- The two test disciplines hold absolutely: the mechanism a test relies on is specified in the frozen queue before work on that item starts; after a failure, nothing is revised to make the failure disappear. A post-failure idea goes in the "New candidates (post-failure)" section, labelled as such, with the failure left on record.
- No fitting: do not tune anything to match a number.
- Registers: label any comparison with known physics as observational.

## Phase 1 — Read state
1. Read every source above.
2. Diff the Premise Map against the latest snapshot in Night-Reports (MAP-SNAPSHOT-<date>.md). Note what changed: nodes added/removed, status changes, new links. First night: no snapshot exists; say so and treat everything as new.
3. Read the previous report's "Suggested follow-ups" and any REVIEW-<date>.md notes from Glenn.

## Phase 2 — Build and freeze the queue
Candidate sources, in this priority:
1. STEERING PIN items, in their order.
2. Follow-ups from the previous night that Glenn hasn't marked skip.
3. Map regions changed since the last snapshot.
4. Open edges / unproved if-then links on the Map.
5. Gaps whose shape the surrounding structure fixes but which haven't had the shape written down.
6. "Necessary" claims not yet tagged by sense (theorem / model / source-entailed / physical), and links whose only support is a model or theorem necessity used as if physical.
7. Possible smuggling: a concept doing load-bearing work in a native-register step it hasn't earned.
8. Places where an existing published mathematical result might already settle a question (search before attempting).

Exclude anything in STEERING SKIP or RETIRED, and anything listed as retired in the standing constraints.

Rank by Glenn's effort-versus-impact rule: easy + high impact first, then easy + moderate, then hard + high. Take 3–6 items, enough to fill the night without padding.

Each queue item records:
- ID (N-<date>-<n>)
- Target (Map node/edge or document reference)
- Task, in one of these shapes: given A,B,C prove whether X follows / given rule R determine whether P is possible / given structure S compute invariant I / given negative result N identify the minimal failed assumption / audit chain C for smuggling or untagged necessity
- Inputs it may use
- Depth: D1 Locate, D2 Shape, or D3 Probe (default D2; D3 only for easy items where a single bounded attempt is meaningful)
- Effort cap (rough share of the night)
- Done means: the concrete output that ends the item
- Mechanism (for any computation or test): the rule specified now, before work, including the planted failure and why it is guaranteed to fail (see Planted failures)

Write the queue into tonight's report file (Section 2) and save it before Phase 3. Do not alter it afterwards; if an item turns out ill-posed, say so in its result and move on.

## Depth scale
- D1 Locate — is there a crack here? If yes, say exactly where. Stop.
- D2 Shape — characterise it: the smallest assumption involved, what a missing piece would have to do, what depends on it. Stop.
- D3 Probe — one attempt to exploit it: a construction, an if-then proof, or a small computation. Report the outcome either way. Stop.
Never go past the stated depth. Never go past D3. "Wall holds at this depth" is a valid, useful result.

## Planted failures (v2)
Every numerical harness carries a planted failure, and the plant must be guaranteed to trip the check analytically, not by an eligibility rule that only correlates with failure. Acceptable: a model that breaks a hypothesis by a known amount whose effect on the checked quantity is computed in closed form (for a bound check: a source term large enough that the analytic steady state exceeds the stated bound). Not acceptable: "flag draws where some integral exceeds the bound", unless it is shown in the queue that this implies the checked quantity exceeds it. State in the queue item why the plant must fail. If the plant does not trip, the harness is blind and the item's numerics are not a receipt; say so, as now.

## Numerics (v2)
- Check bounds, thresholds and kill lines while the solver runs (an event function, or a per-step callback that discards each step once checked). Do not store dense output for every draw and check it afterwards.
- Keep only per-draw summaries (maximum ratio to the bound, flags, solver status) in memory and on disk.
- Size draw counts to the session: estimate time and memory on a pilot of a few draws, written into the run notes, before the main loop.
- A run killed for memory or time is reported with the count completed; it is not re-run with changed rules.

## Phase 3 — Work the queue
- Work items in order within their caps. Code, if any, is Python (stdlib preferred).
- Receipts (v2): every script that produced a number in the report, its output (or a summary file if the raw output is large), and the checker's scripts are uploaded to Night-Reports as plain files before the report is written, named N-<date>-<n>-<name>.py / .txt / .json. The report lists each file with its Drive ID and SHA-256. A result whose script was not uploaded is labelled "no receipt" in Section 4. Upload as text/plain or text/markdown with conversion to Google types disabled.
- After each item, run an independent check with a fresh subagent that has not seen the working: give it the item's statement, inputs and claimed result; ask it to find errors, smuggling, or overreach. Record its verdict (confirmed / disputed / partly) and any dispute verbatim in summary. The checker is Claude; say so, and say the item still needs a cross-model check where it does.
- If the session is running long, finish the current item cleanly and skip the rest; list skipped items as carried over.

## Phase 4 — Write up
Save to Night-Reports:
- NIGHT-REPORT-<YYYY-MM-DD>.md
- MAP-SNAPSHOT-<YYYY-MM-DD>.md — a plain-text dump of the Premise Map's nodes, statuses and links as read tonight (for tomorrow's diff)
- the receipts named in Phase 3

Report structure:
1. Top line — three to five plain-English sentences: what the night found and what it means for direction. Shape before mathematics.
2. Frozen queue — as written in Phase 2, unchanged.
3. State changes noticed — Map diff, steering applied.
4. Results, per item — depth reached; crack found (yes/no); its shape; what survives; independent-check verdict; receipts (file names, Drive IDs, SHA-256); confidence (high/medium/low) with one line why.
5. New candidates (post-failure) — if any, labelled.
6. Suggested Map changes for Glenn to decide — each with the receipt (which item, which check). Recommendations only.
7. Suggested follow-ups — candidates for tomorrow night's queue, with suggested depths.
8. Verification handoffs — any item ready for DeepSeek/Astra/Jev, each as a self-contained task in a single code block.
9. Run notes — anything that went wrong with tools, access or time.

If the run cannot reach a required source (Map, constraints, Drive), write a short report saying what failed and stop; do not improvise from memory.
