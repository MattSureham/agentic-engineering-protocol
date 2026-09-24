# Evidence — Independent review round 1 of the BLOCKED_HUMAN_AUTHORITY exit amendment and the discovery-milestone resume

- **ID:** `EVIDENCE-20260924T011904Z-blocked-exit-review-round-1`
- **Reviewer:** `agent:ClaudeCode-blocked-exit-review-20260924` (fresh instance; did not implement the target; label differs from implementor `agent:ClaudeCode-discovery-fix-3`)
- **Reviewed immutable state:** commit `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3` (amendment `47a0cb40684ad8edc1d574eba28ded610ea2ba93` plus resume/reconciliation `9e8f6b2`), branch `main`, tree clean at review start and end
- **Owning issue:** [ISSUE-20260923T013206Z-pipeline-blocked-exit](../ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md) (`Review: INDEPENDENT`)
- **UTC:** procedure executed 2026-09-24T01:05–01:19Z on Darwin arm64, Python 3 (system), repository root as cwd

## Scope

Independent review of the owner-approved blocked-exit contract amendment and the actual unblock transition only. The discovery implementation itself, prior review rounds, and Codex coverage were not re-reviewed. No Codex live probe, no discovery implementer work, no recorder/coordinator duties were performed.

## Procedure and raw results

| # | Check | Command / method | Result |
|---|---|---|---|
| 1 | Recovery | Read `BOOTSTRAP.md`, `HUMAN_CHECKPOINT.md`, both target commit diffs in full, the amendment issue, the blocker issue, the discovery issue pipeline block, HANDOFF snapshot | Authority chain confirmed: owner approval recorded in ISSUE-20260923T013206Z; bounded Codex authorization recorded in ISSUE-20260922T073608Z (Status `OPEN`, Authority `HUMAN`, nonempty unblock condition) |
| 2 | Full test suite | `python3 -m unittest discover -s tests` | `Ran 167 tests in 28.030s — OK` (exit 0) |
| 3 | Structural validator | `python3 scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)` (exit 0) |
| 4 | Edge scope | Inspect `scripts/run_pipeline.py` `TRANSITIONS`, `_legal_transition`, `_transition`, `_human_blocker_resolved`, `_blocked_entry_blocker`, `_updated_issue_text` at HEAD | Exactly one new edge `("BLOCKED_HUMAN_AUTHORITY", "IN_PROGRESS")`; no new states; entry rule (`target == BLOCKED_HUMAN_AUTHORITY` from any non-terminal state) unchanged |
| 5 | Actual transition | `git show 9e8f6b2` — state-block event 11, Blocker-section reset, issue/HANDOFF/checkpoint reconciliation | Event-11 reason string is byte-identical to the code-generated format; named blocker equals the entry-event blocker (seq 10); attempt 3 / implementor / base `88fa8359…` preserved; digest `c2e02b5…` unchanged |
| 6 | History integrity | `git show ea2d393` and `git show 610c672` for the discovery issue; compare event seq 10 at entry vs HEAD | Entry event seq 10 preserved verbatim; ROTATE-004 misclassification handled as an appended attributable self-correction in `610c672`, not a rewrite |
| 7 | New tests vs required counterexamples | Read the four new tests in `tests/test_run_pipeline.py` | Cover: resume success (attempt preserved, decision cited, blocker section cleared); unresolved blocker refused with snapshot-identical tree; missing `--blocker-issue` refused; mismatched blocker refused; dirty tree refused; flag rejected on ordinary `IN_PROGRESS`; all other target states from blocked refused without mutation |

## Findings against the review questions

1. **Edge fidelity** — CONFIRMED. The implementation adds only `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS`, gated exactly as the owner approved: recorded owner decision in the blocker issue, transition names the entry blocker, reason cites the decision, interrupted attempt preserved.
2. **Exit only on resolved durable blocker** — CONFIRMED. `_require_clean` runs before the resume branch, so the blocker issue's decision must be committed (durable); `_human_blocker_resolved` refuses `Status` missing/`BLOCKED`, non-`HUMAN` authority, or empty/`NONE`/`UNKNOWN`/`PENDING` unblock condition. Semantic adequacy of "decision satisfies the unblock condition" is human judgment, as disclosed in the issue's complexity table.
3. **Fail-closed blocker identity** — CONFIRMED. `_blocked_entry_blocker` raises when no entry event or no parseable linked blocker exists; a named blocker that differs from the recorded entry blocker is refused (`does not match the recorded entry blocker`), so one resolved human issue cannot unblock a milestone blocked on another. Refusals were tested to leave the repository snapshot-identical.
4. **Resume preservation** — CONFIRMED. The resume branch skips `attempt += 1`, implementor reassignment, and base/target reset; the actual state block shows attempt 3, implementor `agent:ClaudeCode-discovery-fix-3`, base `88fa8359ec3a62f200096d0d96bd04a88ebd118a` unchanged, with event seq 11 appended under that actor.
5. **No implicit authorization** — CONFIRMED. PIPELINE-009 and amended ADR decision 5 state the unblock resolves only the authority blocker; the reconciliation records consistently show the armed Codex budget (2 cases, ≤6 sessions) still awaiting the owner's distinct execute-now instruction; background-task section records no Codex session launched or scheduled. No contradicting evidence found.
6. **Quota/participant failure cannot alone produce the state** — CONFIRMED at contract level. PIPELINE-009 reaffirms ROTATE-004. Residual (non-material, O2 below): entry-side machine validation still cannot mechanically reject a quota-rationale entry; this was deliberately excluded from the owner-approved amendment scope.
7. **Exit-semantics invariant and scope** — CONFIRMED with one wording observation (O1 below). PIPELINE-009 defines the invariant; the change adds one edge and no states; all other transitions and gates are unchanged.
8. **Deterministic test coverage** — CONFIRMED. Success, unresolved blocker, wrong blocker, missing flag, dirty tree, flag misuse, and wrong-target refusals are covered with no-mutation assertions; independently re-run (check 2): 167 tests OK.
9. **Actual transition conformance** — CONFIRMED. Event 11's reason matches the machine format exactly (evidence the pipeline, not a hand edit, performed it); the Blocker-section reset matches `_updated_issue_text`'s `resolved_blocker` replacements exactly; the milestone is `IN_PROGRESS` while the separately gated Codex execution budget remains armed-but-unconsumed.
10. **History not rewritten** — CONFIRMED. The 2026-09-22 ROTATE-004 misuse stands as event seq 10 with its original reason; the correction is an appended, attributable record in `610c672`; no historical event, review round, or evidence record was rewritten in the inspected diffs.

## Non-material observations (0 open material findings)

- **O1 (wording):** PIPELINE-009's first sentence says "every milestone state the pipeline may enter MUST have a defined, verifiable exit," which read literally includes the terminal `ACCEPTED` state (no exit edge by design). The owner's recorded bound was "every enterable blocking state," and the heading plus following sentences make the blocking-state intent clear. A future participant could note the imprecision; it authorizes nothing and changes no behavior.
- **O2 (residual, disclosed):** Entry-side validation does not mechanically reject quota/participant-failure rationales for `BLOCKED_HUMAN_AUTHORITY`; ROTATE-004 enforcement at entry remains spec-level/human judgment. Deliberately excluded from the approved amendment scope and consistent with the issue's disclosed "machine checks only durable recording signals" limitation.
- **O3 (residual, disclosed):** `_human_blocker_resolved` treats any non-`BLOCKED` status with a nonempty unblock-condition field as resolved; it cannot judge whether the recorded decision semantically satisfies the condition. Disclosed in the issue; independent review (this round) supplies that judgment for the actual transition and finds the ISSUE-20260922T073608Z decision does satisfy the recorded unblock condition.

## Disposition

**APPROVED** — reviewed target `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3`, open material findings: **0**.

## Limitations and residual risks

- Label inequality is not authenticated identity (PIPELINE-005); this review is a fresh instance but cannot prove it.
- "No Codex session launched" is verified from durable records consistency, not from external Codex account telemetry, which this reviewer did not access.
- Markdown linter unavailable; link/fragment targets outside the structural validator were not checked.
- This disposition covers the amendment and the resume transition only; it is not acceptance of the discovery milestone, whose Codex coverage gap and owner execution gate are unchanged.
