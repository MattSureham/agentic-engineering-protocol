# Review Disposition Vocabulary Versus Session Verdict Labels

## Metadata

- **ID:** `ISSUE-20260811T030136Z-review-disposition-vocabulary`
- **Title:** Review session verdict labels versus the three protocol dispositions
- **Status:** `CLOSED`
- **Severity:** `LOW`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-11T03:01:36Z`
- **Updated UTC:** `2026-08-14T05:03:21Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `PIPELINE-005`; root [`BOOTSTRAP.md`](../BOOTSTRAP.md) review requirements; and [`ISSUES/TEMPLATE.md`](TEMPLATE.md) review-round schema
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`ISSUE-20260811T013701Z-structural-protocol-validator`](ISSUE-20260811T013701Z-structural-protocol-validator.md) (owner-report note of `2026-08-11T02:38:34Z` and persisted independent round 1 of `2026-08-11T02:49:05Z`); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md); [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md)

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
| `2026-08-14T02:32:24Z` | `Codex/root` | Inspect published target `6c0a3bd`, generated transition evidence, review-template/prompt wording, and peer-gate test cases | Exact disposition contract and executable rejections pass at immutable target | [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md) | Independent semantic review and identity authentication remain pending/out of scope respectively |
| `2026-08-14T05:03:21Z` | `ClaudeCode/coordinator` | Coordinator closure verification on the accepted target: `git diff` of this issue's wording change set (root/reusable BOOTSTRAP, both issue templates, reusable review prompt) between reviewed target `6c0a3bd` and accepted target `26d890f` is empty; post-target drift on `scripts/`, `tests/`, `protocol/`, and templates is record-only; re-inspected gate enforcement `DISPOSITIONS = {"APPROVED", "CHANGES_REQUIRED", "BLOCKED"}` at `scripts/run_pipeline.py:69`; reran full suite at HEAD | Wording bytes unchanged; executable rejection contract intact; 44 tests pass; structural validator `PASS` | This record; `scripts/run_pipeline.py` at accepted target | The independent round's scoped `APPROVED` is relied on for semantics; this verification confirms only that the fix loop did not alter the reviewed wording or the vocabulary gate |

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

The historical self-review above covered creation of the record only. Implementor `Codex/root` inspected the owner-authorized wording and executable schema at immutable target `6c0a3bda06686635023e334a4e644fb176372b04` through `2026-08-14T02:32:24Z`; this preparatory check does not satisfy the now-required independent review.

## Independent review rounds

- **Required:** `YES` — the owner-authorized wording is now part of the shared governance/pipeline target and must be independently checked for compatibility with existing review semantics.

### 2026-08-14T03:11:06Z — ClaudeCode/pipeline-review

- **Reviewed repository state:** Immutable shared target `6c0a3bda06686635023e334a4e644fb176372b04` (parent `a6f2699a4bed2e1a08c9a506bad62204bd2d0086`), extracted via `git archive` into a fresh temporary directory; post-target records through `d85223b95de7564567316087efbb86d80d76597c`
- **Reviewed target:** `6c0a3bda06686635023e334a4e644fb176372b04`
- **Open material findings:** `0`
- **Scope:** This issue's change set only — root and reusable BOOTSTRAP review-requirements wording, both issue templates' review-round schema, the reusable independent-review prompt, and the executable review-gate rejection cases at the shared target
- **Commands or procedures:** Full read of the target-range wording diffs; comparison against the owner decision recorded at `2026-08-14T01:58:17Z`; reproduction of the complete suite at the extracted target (`Ran 39 tests ... OK`), including executable rejection of the informal label `APPROVED WITH FINDINGS`, same-label review, target mismatch, `BLOCKED`, and approval with material findings
- **Specification compliance:** The exact three-value vocabulary appears in every intended artifact and no fourth disposition is introduced anywhere; `PIPELINE-005`, both BOOTSTRAP review sections, and both template schemas agree; the owner decision is implemented without scope growth
- **Correctness and regression findings:** `NONE` within this issue's scope
- **Architecture and complexity findings:** `NONE`; no new complexity introduced
- **Material findings and resolution conditions:** `NONE` within this issue's wording scope. The shared target carries two material pipeline-gate findings (`R1`/`R2`) recorded in [`ISSUE-20260806T013907Z-runtime-automation`](ISSUE-20260806T013907Z-runtime-automation.md); they do not touch this issue's change set
- **Limitations:** This round approves only the disposition-vocabulary wording and schema at the shared target; it does not accept the milestone. If the authorized fix loop alters any file in this issue's change set, closure verification must re-check the wording on the accepted target
- **Residual risks:** Session-facing reporters may still improvise labels until they adopt the clarified prompts; the protocol records, rather than prevents, that behavior
- **Evidence:** Target-range diffs; the extracted-target suite run; the runtime-automation issue's review round of `2026-08-14T03:11:06Z`
- **Disposition:** `APPROVED`
- **Prior-round resolution:** `FIRST ROUND`

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- None blocking. The independent disposition is persisted and the reviewed wording is confirmed unchanged on the accepted target. Session-facing reporters may still improvise labels until they adopt the clarified prompts; the protocol records, rather than prevents, that behavior (residual risk owned by the independent round).

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | `NONE` | `OPEN` | Recorded the review-reporting vocabulary friction surfaced during validator-milestone reconciliation; no protocol change proposed |
| `2026-08-14T01:58:17Z` | Human technical owner `MattSureham`, recorded by `Codex/root` | `OPEN` | `INVESTIGATING` | Selected exact protocol vocabulary for all review verdict reporting; authorized bounded wording changes and independent review |
| `2026-08-14T02:06:16Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Began exact-vocabulary wording and schema changes from committed authority boundary `a6f2699`; no new disposition is introduced |
| `2026-08-14T02:32:24Z` | `Codex/root` | `IMPLEMENTING` | `VERIFYING` | Frozen shared target `6c0a3bd`; completed exact-vocabulary, schema, rejection-path, link, and full-suite verification |
| `2026-08-14T02:32:24Z` | `Codex/root` | `VERIFYING` | `REVIEW` | Published immutable target and complete evidence; fresh independent review is the remaining gate |
| `2026-08-14T05:03:21Z` | `ClaudeCode/coordinator` | `REVIEW` | `CLOSED` | Closure verification on the accepted target passed: scoped `APPROVED` round of `2026-08-14T03:11:06Z` persisted with zero open material findings, wording change set byte-identical between reviewed target `6c0a3bd` and accepted target `26d890f`, vocabulary gate enforcement intact, 44 tests and structural validator pass |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source (root BOOTSTRAP review requirements and the issue template).
- [x] The wording change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the historical record-only Self-review outcome is `COMPLETE`; it does not satisfy the newly required independent review of governance wording.
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved (round of `2026-08-14T03:11:06Z` by `ClaudeCode/pipeline-review`, `FIRST ROUND` with zero open material findings; recorder confirmed the reviewed wording is byte-identical on the accepted target `26d890f` on `2026-08-14T05:03:21Z`).
- [x] Required human authority is recorded in the accepted specification and compatible ADR.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (none introduced).
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
