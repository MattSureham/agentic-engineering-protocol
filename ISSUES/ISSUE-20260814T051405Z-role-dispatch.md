# Automated Role Dispatch and Rotation v1

## Metadata

- **ID:** `ISSUE-20260814T051405Z-role-dispatch`
- **Title:** Implement the authorized automated role dispatch milestone
- **Status:** `IMPLEMENTING`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-14T05:14:05Z`
- **Updated UTC:** `2026-08-14T05:30:34Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase and `MILESTONE-20260814T051405Z-role-dispatch-v1`
- **ADRs:** [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** `NONE YET`
- **Milestone:** `MILESTONE-20260814T051405Z-role-dispatch-v1`

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The accepted milestone pipeline makes transitions deterministic, but the routing between them still depends on an operator inferring the next required role, participant eligibility, and role contract from prose records. During the first pipeline milestone this manual routing worked but required reading HANDOFF and issue history at every boundary — routine intervention that durable repository state can already determine. The human technical owner has directed eliminating that intervention for already-authorized work while keeping human escalation for genuine authority gaps.

## Evidence or reproduction

- **CONFIRMED:** The first pipeline milestone completed its full lifecycle (authority → implementation → verification → two independent review rounds → fix loop → acceptance) on `2026-08-14`; every inter-boundary routing decision was made by a participant reading records manually, as preserved in [`ISSUE-20260806T013907Z-runtime-automation`](ISSUE-20260806T013907Z-runtime-automation.md) and HANDOFF activity history.
- **CONFIRMED:** The pipeline's read-only status already derives the selected milestone and per-milestone state from the accepted contract and issue-embedded state blocks; the routing inputs exist in durable form.
- **CONFIRMED:** The owner direction of `2026-08-14T05:14:05Z` authorizes this exact milestone, requires the repository-native/host-invocation execution boundary to be documented first, and prohibits simulating a host launch interface.

## Expected behavior

Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase (`DISPATCH-001`–`DISPATCH-008`), and the dispatch acceptance criteria define the expected result: codified role contracts, deterministic eligibility/independence rules, a read-only next-role dispatcher integrated with the existing pipeline, durable resumability without conversational memory, and an explicit host adapter boundary. Compatible architecture is recorded in [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md).

## Assumptions

- **CONFIRMED:** The accepted pipeline tool exposes importable contract/state parsers and a read-only status path; the dispatcher can reuse them without modifying the accepted implementation.
- **CONFIRMED:** The reusable ten-file package is out of scope; all new runtime is root-only.
- **INFERRED:** A separate read-only script is the smallest integration that does not touch the accepted pipeline tool; facts: the pipeline's parsers are importable, the dispatcher mutates nothing, and the milestone-1 ADR already established the root-only tool pattern.
- **UNKNOWN:** Whether any host exposes a durable programmatic launch interface suitable for a real adapter. Resolution path: out of scope for v1; the adapter boundary is documented for a future owner-approved milestone.

## Investigation and decision

The owner direction is recorded verbatim in HUMAN_CHECKPOINT and summarized under Owner direction below. The execution-boundary analysis required by the direction is decided in the accepted ADR: repository-native dispatch (deterministic, implemented here) versus host-specific invocation (adapter boundary, not implemented in v1, not simulated). No further product or architecture question is open.

## Change

- **Files or components:** New root `ROLE_CONTRACTS.md`; new root-only `scripts/run_dispatch.py`; new `tests/test_run_dispatch.py`; root `README.md` navigation; this issue; `HANDOFF.md`; `HUMAN_CHECKPOINT.md`; generated evidence under `EVIDENCE/`.
- **Behavior changed:** The repository gains a deterministic read-only next-role decision covering implementer, independent reviewer, recorder/coordinator, human escalation, and the terminal no-authorized-work case, with eligibility constraints and role contract references.
- **Out-of-scope work deliberately excluded:** Host session invocation or any simulation of it; changes to the accepted pipeline tool; new milestone states; reusable-package changes; the four still-`BLOCKED` capability deferrals.
- **Rollback or recovery:** Revert the immutable dispatch target while preserving this owner direction and the accepted specification/ADR records.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Second root Python tool sharing pipeline parsers | Deterministic dispatch without a competing state machine | Dispatch tests across every pipeline state; exact-target evidence | Semantic routing adequacy remains reviewer judgment |
| Root role-contract artifact | Shared durable expectations for humans, agents, and the dispatcher | Acceptance criteria require consistency with BOOTSTRAP and pipeline semantics | Prose/tool drift caught by review and tests |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-14T05:14:05Z` | `ClaudeCode/root` | Authority-boundary recording only: parsed the updated two-milestone contract with the accepted pipeline parser; verified milestone-1 digest unchanged and milestone-2 digest computed | Contract parses; milestone-1 digest `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4` unchanged; milestone-2 digest `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c` | This issue and the accepted specification/ADR | No implementation exists yet; deterministic verification begins with the first attempt |

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260814T051405Z-role-dispatch-v1",
  "authority_digest": "afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c",
  "state": "IN_PROGRESS",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-dispatch",
  "base_revision": "10d9610f8d5d6167360b6f5fd4bfdf4392971ac4",
  "target_revision": null,
  "verification_evidence": [],
  "review_references": [],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-08-14T05:14:05Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Explicit Automated Role Dispatch / Rotation v1 owner direction accepted through specification evolution with a compatible accepted ADR."
    },
    {
      "sequence": 2,
      "utc": "2026-08-14T05:30:25Z",
      "actor": "agent:ClaudeCode-dispatch",
      "from": "AUTHORIZED",
      "to": "READY",
      "reason": "Validated transition AUTHORIZED to READY."
    },
    {
      "sequence": 3,
      "utc": "2026-08-14T05:30:34Z",
      "actor": "agent:ClaudeCode-dispatch",
      "from": "READY",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 1 began from immutable base 10d9610f8d5d6167360b6f5fd4bfdf4392971ac4."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Self-review

- **Outcome:** `NOT_APPLICABLE`

This issue requires independent review of its immutable implementation target; any preparatory self-review is recorded separately and never substitutes for that gate.

## Independent review rounds

- **Required:** `YES` — the milestone adds a runtime component that reads authority-bound state and changes how already-authorized work is routed.

No independent review round has been recorded.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Owner direction

`2026-08-14T05:14:05Z` — Human technical owner `MattSureham` directed: authorize a new PROJECT_SPEC milestone for Automated Role Dispatch / Rotation v1. Eliminate routine human intervention between already-authorized pipeline transitions by making the repository able to determine the next required role, participant eligibility, and role contract from durable project state, across the lifecycle: authorized work → implementer → verify → independent reviewer → fix/re-review when required → recorder/accept → next authorized milestone → repeat. Human escalation occurs only when existing repository authority is insufficient. For v1: codify implementer, reviewer, and recorder/coordinator role contracts; codify participant eligibility and reviewer-independence rules; implement deterministic next-role/dispatch decisions from repository state; preserve all decisions and transitions durably; support interruption/resumption without conversational memory; integrate with the existing pipeline rather than creating a competing state machine. Do not assume the host can launch arbitrary agent sessions; determine and document the execution boundary between repository-native dispatch decisions and host-specific participant/session invocation first, and if the current host exposes no durable programmatic launch interface, implement and verify the repository-native dispatcher first and leave host invocation as an explicit adapter boundary rather than simulating it. No web UI, distributed scheduler, database, external tracker, or unrelated orchestration infrastructure is authorized. Record through the existing specification-evolution and ADR process, then proceed without requesting routine human approval. Use independent peer review before acceptance.

## Residual uncertainty

- Exact dispatcher output shape and role-contract wording remain implementation decisions within the accepted scope; independent review of the immutable target is the remaining gate.
- Host launch capability remains unknown and out of scope; the adapter boundary is documented instead.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-14T05:14:05Z` | `ClaudeCode/root` | `NONE` | `OPEN` | Created from the explicit owner direction after verifying the first pipeline milestone is `ACCEPTED`, both wording issues are `CLOSED`, and the repository was in its terminal wait state |
| `2026-08-14T05:14:05Z` | `ClaudeCode/root` | `OPEN` | `INVESTIGATING` | Recorded the accepted specification phase, compatible accepted ADR, contract digest `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c`, and execution-boundary decision before any implementation |
| `2026-08-14T05:30:25Z` | `agent:ClaudeCode-dispatch` | `INVESTIGATING` | `INVESTIGATING` | Pipeline AUTHORIZED -> READY. Validated transition AUTHORIZED to READY. |
| `2026-08-14T05:30:34Z` | `agent:ClaudeCode-dispatch` | `INVESTIGATING` | `IMPLEMENTING` | Pipeline READY -> IN_PROGRESS. Implementation attempt 1 began from immutable base 10d9610f8d5d6167360b6f5fd4bfdf4392971ac4. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted dispatch phase and compatible accepted ADR.
- [ ] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
