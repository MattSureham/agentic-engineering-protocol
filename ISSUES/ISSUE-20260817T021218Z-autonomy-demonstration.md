# Unattended Autonomy Demonstration

## Metadata

- **ID:** `ISSUE-20260817T021218Z-autonomy-demonstration`
- **Title:** Execute the gated end-to-end unattended autonomy demonstration
- **Status:** `INVESTIGATING`
- **Severity:** `HIGH`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-17T02:12:18Z`
- **Updated UTC:** `2026-08-17T02:12:18Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Product-level autonomy objective (`AUTONOMY-001`–`AUTONOMY-006`), Live invocation and autonomy demonstration phase (demonstration acceptance criteria), and `MILESTONE-20260817T021218Z-autonomy-demonstration-v1`
- **ADRs:** [`ADR-20260817T021218Z-autonomy-end-state`](../ADR/ADR-20260817T021218Z-autonomy-end-state.md); [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md)
- **Evidence:** To be produced by the run itself: the append-only [`ROTATION_LOG.jsonl`](../ROTATION_LOG.jsonl), this issue's pipeline events, the launched reviewer's round, and a demonstration evidence record under `EVIDENCE/`
- **Milestone:** `MILESTONE-20260817T021218Z-autonomy-demonstration-v1`

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The product-level autonomy objective (`AUTONOMY-001`–`AUTONOMY-006`) is unproven: no real participant has ever been launched by the system, and no authorized milestone has ever progressed without manual routing. This milestone is the gated demonstration. Its own lifecycle is the dogfood run: after one bounded runner invocation, launched implementer, independent-reviewer, and recorder participants must progress it from `AUTHORIZED` to `ACCEPTED` with no owner or operator routing, and the durable records must prove it.

## Evidence or reproduction

- **CONFIRMED:** Every lifecycle transition to date was executed by a manually started participant; the dispatcher's terminal `ROLE none` at `ffdd275e70798318cdbfb74f13f1cb864ea65924` is an idle state, not autonomy evidence (`AUTONOMY-006`).
- **CONFIRMED:** The vehicle change is real and bounded: the accepted pipeline's activity gate (`scripts/run_pipeline.py`, "Activity history must contain only a Markdown table") rejects the prose line under `## Activity history` in root [`ISSUES/TEMPLATE.md`](TEMPLATE.md), as recorded in the rotation milestone's review records.
- **CONFIRMED:** This milestone depends on `MILESTONE-20260817T021218Z-live-invocation-v1`; it cannot begin implementation until that capability is accepted.

## Expected behavior

Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), demonstration acceptance criteria 1–6: the vehicle change implemented within allowed paths with the reusable package untouched; the full lifecycle executed by runner-launched participants under three distinct labels; the append-only ledger and pipeline events naming those labels; durable evidence making any owner/operator routing visible and recording that there was none; an assembled independently checkable demonstration evidence record; and a launched fresh independent reviewer whose `APPROVED` round with zero open material findings permits `ACCEPTED`.

## Assumptions

- **CONFIRMED:** The accepted runner, registry, dispatcher, and pipeline provide every mechanism the run needs; this milestone changes no tooling (runner changes belong to the live-invocation milestone).
- **CONFIRMED:** The reusable ten-file package is out of scope; the vehicle change touches only root `ISSUES/TEMPLATE.md`.
- **INFERRED:** One bounded runner invocation suffices for three role legs plus any bounded fix loops. Facts: the runner loops decisions until a stop reason; attempt/step/spend bounds are declared; recovery re-reads repository state.
- **UNKNOWN:** Whether the first unattended run completes within declared bounds on the live host. Resolution path: the run itself; exhaustion stops are recorded, classified, and never escalated as authority gaps.

## Investigation and decision

The owner direction is recorded through specification evolution and summarized in [`HUMAN_CHECKPOINT.md`](../HUMAN_CHECKPOINT.md). The demonstration architecture is decided in the accepted ADR: the milestone is its own vehicle, the durable records are the proof standard, and the recorder verifies the implementer and reviewer legs from durable records at closure. No further product or architecture question is open.

## Change

- **Files or components:** Root `ISSUES/TEMPLATE.md` (vehicle fix); this issue; `EVIDENCE/` (demonstration evidence); `ROTATION_LOG.jsonl` (append-only run ledger); `ROTATION_PARTICIPANTS.json` (only if the live-invocation milestone's verified profile requires registry entries here); `HANDOFF.md`; `HUMAN_CHECKPOINT.md`; `README.md`.
- **Behavior changed:** The root issue template conforms to the pipeline's table-only activity gate; the repository gains its first unattended full-lifecycle run as durable evidence.
- **Out-of-scope work deliberately excluded:** Any tooling change (runner, dispatcher, pipeline); the reusable package; new milestones beyond the demonstration; the four still-`BLOCKED` capability deferrals.
- **Rollback or recovery:** Revert the immutable vehicle-fix target while preserving the owner direction and accepted records. The ledger is append-only operational evidence and is never rewritten; a failed run is evidence, not an error to erase.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| First live unattended run on the real repository | The objective cannot be demonstrated otherwise | Demonstration acceptance criteria; ledger, events, and review round as durable proof | Host rate limits and long-running stability remain `UNKNOWN`; bounded stops govern |
| Post-hoc evidence assembly | The demonstration is complete only after acceptance | Recorder closure verification plus the assembled evidence record | Completeness judgment remains with the launched reviewer and recorder as recorded |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-17T02:12:18Z` | `ClaudeCode/root` | Authority-boundary recording only: parsed the updated five-milestone contract with the accepted pipeline parser; verified milestones 1–3 digests unchanged and milestone 5 digest computed | Contract parses; milestones 1–3 unchanged (`36fba5d8…`, `afe72580…`, `a38bb7bf…`); milestone-5 digest `f0a1700f00500125d42e832a236077b0d42e87ebc4ade284a33335e8794c0284` | This issue and the accepted specification/ADR | No run has occurred; the demonstration produces its own verification records |

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260817T021218Z-autonomy-demonstration-v1",
  "authority_digest": "f0a1700f00500125d42e832a236077b0d42e87ebc4ade284a33335e8794c0284",
  "state": "AUTHORIZED",
  "attempt": 0,
  "implementor": null,
  "base_revision": null,
  "target_revision": null,
  "verification_evidence": [],
  "review_references": [],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-08-17T02:12:18Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Explicit product-level autonomy owner direction accepted through specification evolution with a compatible accepted ADR."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Self-review

- **Participant:** `ClaudeCode/root`
- **Reviewed UTC:** `2026-08-17T02:12:18Z`
- **Reviewed repository state:** Authority-boundary records only; synchronized baseline `ffdd275e70798318cdbfb74f13f1cb864ea65924` plus the records created by this phase
- **Scope and authority references:** Root `PROJECT_SPEC.md` autonomy objective and demonstration criteria, accepted ADR; no run has occurred
- **Checks and evidence reviewed:** Contract digest parse (row above); vehicle-fix scope confirmed against the pipeline gate text
- **Findings and corrections:** NONE
- **Limitations:** No implementation or run to review; this self-review covers authority-recording consistency only
- **Residual risks:** NONE beyond the declared UNKNOWNs
- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES` — this milestone is the product-level proof of the autonomy objective; the reviewing participant is itself launched by the runner per demonstration criterion 6.

No independent review round has been recorded. Review begins after the launched implementer submits the first immutable target through the pipeline.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE` (implementation cannot begin until dependency `MILESTONE-20260817T021218Z-live-invocation-v1` is `ACCEPTED`; the pipeline enforces dependency selection order)
- **Unblock owner:** `NOT APPLICABLE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Whether the first unattended run completes within declared bounds is `UNKNOWN` and owned by this issue; bound exhaustion is a recorded stop, never an authority escalation.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-17T02:12:18Z` | `human:MattSureham` | `NONE` | `INVESTIGATING` | Owner direction authorized the product-level autonomy objective and this demonstration milestone; specification evolution, accepted ADR, and this owning issue recorded; pipeline state `AUTHORIZED` |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [ ] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
