# Review Disposition Vocabulary Versus Session Verdict Labels

## Metadata

- **ID:** `ISSUE-20260811T030136Z-review-disposition-vocabulary`
- **Title:** Review session verdict labels versus the three protocol dispositions
- **Status:** `IMPLEMENTING`
- **Severity:** `LOW`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-11T03:01:36Z`
- **Updated UTC:** `2026-08-14T02:24:27Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `PIPELINE-005`; root [`BOOTSTRAP.md`](../BOOTSTRAP.md) review requirements; and [`ISSUES/TEMPLATE.md`](TEMPLATE.md) review-round schema
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`ISSUE-20260811T013701Z-structural-protocol-validator`](ISSUE-20260811T013701Z-structural-protocol-validator.md) (owner-report note of `2026-08-11T02:38:34Z` and persisted independent round 1 of `2026-08-11T02:49:05Z`); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md)

## Problem

Independent reviewers report session-level verdicts in informal vocabulary. On `2026-08-11` a reviewer reported "APPROVED WITH FINDINGS" in session output while the protocol defines exactly three round dispositions. The owner received the informal label first; the coordinator could not classify findings or evaluate closure until the complete round was persisted and the reviewer mapped the label to `APPROVED` with justification. The mapping succeeded, but it required an extra coordination cycle and depended on the reviewer performing the mapping correctly after the fact.

## Evidence or reproduction

- **CONFIRMED:** The validator issue records the owner-reported informal disposition as persistence-pending at `2026-08-11T02:38:34Z` and the complete round with the reviewer's mapping justification at `2026-08-11T02:49:05Z`; the round preserves the session label verbatim, so no information was lost.
- **CONFIRMED:** Root BOOTSTRAP and the issue template define only `APPROVED`, `CHANGES_REQUIRED`, and `BLOCKED`; neither addresses informal session verdicts reported outside the repository.
- **INFERRED:** The friction is generalizable to any future review whose session output reaches the owner before the durable round.

## Expected behavior

The human technical owner decides whether any clarification is warranted — for example, guidance that reviewers should express session-level verdicts in protocol disposition vocabulary and map any informal label before reporting — or whether the existing persistence discipline is sufficient. This issue proposes no protocol change itself; any wording change to root BOOTSTRAP or the template remains owner-gated.

## Assumptions

- **CONFIRMED:** The record layer worked as designed: the informal label was never treated as a disposition, and the durable round uses protocol vocabulary.
- **INFERRED:** A small reporting-vocabulary clarification would have avoided one coordination round-trip.
- **UNKNOWN:** Whether the owner considers the friction worth a protocol wording change.

## Investigation and decision

On `2026-08-14T01:58:17Z`, human technical owner `MattSureham` supplied the decision: reviewers MUST use exactly `APPROVED`, `CHANGES_REQUIRED`, or `BLOCKED`; informal session verdicts do not become additional dispositions. Descriptive qualifiers and non-blocking findings belong in the finding/residual-risk fields. The root and reusable instructions/templates will receive only this clarification and will share the pipeline target's independent-review gate.

## Change

- **Files or components:** Root/reusable BOOTSTRAP review wording, issue templates, review prompt, this issue, HANDOFF/checkpoint.
- **Behavior changed:** Session-facing and durable review verdicts must both use the existing three protocol dispositions; findings remain separate data.
- **Out-of-scope work deliberately excluded:** New dispositions, changed materiality rules, changed reviewer independence, or automatic judgment of finding severity.
- **Rollback or recovery:** Revert the wording target while preserving this owner decision and original observation.

## Unverified complexity

None introduced.

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | Coordinator closure verification of the validator milestone: target/tree/parent identity reproduction, post-target drift scope, validator and 21-test rerun, round-schema completeness check | All checks pass; details recorded in the validator issue activity history and HANDOFF | [`ISSUE-20260811T013701Z-structural-protocol-validator`](ISSUE-20260811T013701Z-structural-protocol-validator.md) | The session output itself is not a repository artifact; the verbatim label survives only inside the persisted round |
| `2026-08-14T02:24:27Z` | `Codex/root` | Inspect root/reusable BOOTSTRAP, both issue templates, independent-review prompt, and executable review-round rejection cases | Exact three-value vocabulary appears in all intended artifacts; tests reject informal, self-reviewed, target-mismatched, `BLOCKED`, and material-finding approval cases; 39 repository tests pass | Shared pipeline candidate worktree; immutable evidence pending | Implementor inspection cannot satisfy independent review or authenticate labels |

## Self-review

- **Participant:** `ClaudeCode/coordinator`
- **Reviewed UTC:** `2026-08-11T03:01:36Z`
- **Reviewed repository state:** HEAD `f06982573ae0743f5feb7c51858ff96822dc9714` plus this record-only addition
- **Scope and authority references:** This issue record only; no protocol source, gate, or authority change
- **Checks and evidence reviewed:** The two cited issue sections, root BOOTSTRAP review-requirements text, and the issue template disposition line
- **Findings and corrections:** None
- **Limitations:** Record-only; the owner may judge the friction not worth any clarification
- **Residual risks:** Future informal verdict labels may recur until the owner directs otherwise
- **Outcome:** `COMPLETE`

The historical self-review above covered creation of the record only. Implementor `Codex/root` inspected the owner-authorized wording and executable schema at `2026-08-14T02:24:27Z`; this preparatory check does not satisfy the now-required independent review.

## Independent review rounds

- **Required:** `YES` — the owner-authorized wording is now part of the shared governance/pipeline target and must be independently checked for compatibility with existing review semantics.

No independent review round has been recorded for the wording target.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Exact wording correctness and independent disposition remain pending. The owner decision itself is no longer uncertain.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | `NONE` | `OPEN` | Recorded the review-reporting vocabulary friction surfaced during validator-milestone reconciliation; no protocol change proposed |
| `2026-08-14T01:58:17Z` | Human technical owner `MattSureham`, recorded by `Codex/root` | `OPEN` | `INVESTIGATING` | Selected exact protocol vocabulary for all review verdict reporting; authorized bounded wording changes and independent review |
| `2026-08-14T02:06:16Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Began exact-vocabulary wording and schema changes from committed authority boundary `a6f2699`; no new disposition is introduced |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source (root BOOTSTRAP review requirements and the issue template).
- [x] The wording change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the historical record-only Self-review outcome is `COMPLETE`; it does not satisfy the newly required independent review of governance wording.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the accepted specification and compatible ADR.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (none introduced).
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
