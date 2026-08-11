# Review Disposition Vocabulary Versus Session Verdict Labels

## Metadata

- **ID:** `ISSUE-20260811T030136Z-review-disposition-vocabulary`
- **Title:** Review session verdict labels versus the three protocol dispositions
- **Status:** `OPEN`
- **Severity:** `LOW`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-08-11T03:01:36Z`
- **Updated UTC:** `2026-08-11T03:01:36Z`
- **Requirements:** Root [`BOOTSTRAP.md`](../BOOTSTRAP.md) review requirements (dispositions are exactly `APPROVED`/`CHANGES_REQUIRED`/`BLOCKED`) and [`ISSUES/TEMPLATE.md`](TEMPLATE.md) review-round schema
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md)
- **Evidence:** [`ISSUE-20260811T013701Z-structural-protocol-validator`](ISSUE-20260811T013701Z-structural-protocol-validator.md) (owner-report note of `2026-08-11T02:38:34Z` and persisted independent round 1 of `2026-08-11T02:49:05Z`)

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

None yet. Awaiting owner direction, as with [`ISSUE-20260807T022523Z-pilot-onboarding-authority-friction`](ISSUE-20260807T022523Z-pilot-onboarding-authority-friction.md).

## Change

- **Files or components:** None; record-only issue.
- **Behavior changed:** None.
- **Out-of-scope work deliberately excluded:** Any edit to root BOOTSTRAP, the reusable protocol package, templates, or review gates.
- **Rollback or recovery:** Close or retain per owner direction; the record remains accurate either way.

## Unverified complexity

None introduced.

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | Coordinator closure verification of the validator milestone: target/tree/parent identity reproduction, post-target drift scope, validator and 21-test rerun, round-schema completeness check | All checks pass; details recorded in the validator issue activity history and HANDOFF | [`ISSUE-20260811T013701Z-structural-protocol-validator`](ISSUE-20260811T013701Z-structural-protocol-validator.md) | The session output itself is not a repository artifact; the verbatim label survives only inside the persisted round |

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

## Independent review rounds

- **Required:** `NO` — record-only observation with no implementation, contract, or authority impact; any resulting protocol wording change would separately require owner approval and independent review per the Human Authority Boundary.

No independent review round has been recorded.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Whether the owner wants a reporting-vocabulary clarification, and if so in which governed artifact; this issue stays `OPEN` until the owner directs a disposition.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | `NONE` | `OPEN` | Recorded the review-reporting vocabulary friction surfaced during validator-milestone reconciliation; no protocol change proposed |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source (root BOOTSTRAP review requirements and the issue template).
- [x] The change or resolution is recorded (record-only; no change).
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved (not applicable — `Review: SELF`).
- [ ] Required human authority is recorded in the owning artifact (pending owner direction; this issue remains `OPEN`).
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (none introduced).
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
