# Automated Role Dispatch and Rotation v1

## Metadata

- **ID:** `ISSUE-20260814T051405Z-role-dispatch`
- **Title:** Implement the authorized automated role dispatch milestone
- **Status:** `REVIEW`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-14T05:14:05Z`
- **Updated UTC:** `2026-08-14T08:45:05Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase and `MILESTONE-20260814T051405Z-role-dispatch-v1`
- **ADRs:** [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json) (pipeline-generated submission record, result `PASS`) plus the verification table below
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
| `2026-08-14T05:43:14Z` | `agent:ClaudeCode-dispatch` | `python3 -m unittest discover -s tests -v` | 63 tests `OK` (44 retained pipeline/structural tests plus 19 new dispatch tests), exit `0` | `tests/test_run_dispatch.py` and this row | Fixture-based; runs on the recorded Darwin/Python 3.9 environment only |
| `2026-08-14T05:43:14Z` | `agent:ClaudeCode-dispatch` | `python3 scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)`, exit `0` | Inline | Structural invariants only; no semantic judgment |
| `2026-08-14T05:43:14Z` | `agent:ClaudeCode-dispatch` | Live read-only check on this repository: `python3 scripts/run_dispatch.py --json` twice, compared byte-for-byte; `git status --porcelain` before and after | Byte-identical decision (role `implementer`, state `IN_PROGRESS`, milestone 2 selected); worktree status unchanged, confirming no mutation | Inline | Single live state exercised; the fixture suite covers every other state |
| `2026-08-14T05:43:14Z` | `agent:ClaudeCode-dispatch` | Fixture coverage across every dispatch-relevant state: `AUTHORIZED`, `READY`, `IN_PROGRESS`, `AWAITING_PEER_REVIEW` (no round, stale-target round, `APPROVED` round, `CHANGES_REQUIRED` round, `BLOCKED` round), `CHANGES_REQUIRED`, `BLOCKED_HUMAN_AUTHORITY`, all-`ACCEPTED` terminal, and dependency-ordered selection | Each routes to exactly the one expected role with the expected eligibility constraints and commands; byte-identity, timestamp-free output, and no-mutation assertions pass | `tests/test_run_dispatch.py` (19 tests) | Semantic adequacy of routing wording remains reviewer judgment |

- **Pipeline verification `2026-08-14T05:48:59Z`:** [`EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8`.

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260814T051405Z-role-dispatch-v1",
  "authority_digest": "afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c",
  "state": "AWAITING_PEER_REVIEW",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-dispatch",
  "base_revision": "10d9610f8d5d6167360b6f5fd4bfdf4392971ac4",
  "target_revision": "4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8",
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json"
  ],
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
    },
    {
      "sequence": 4,
      "utc": "2026-08-14T05:48:59Z",
      "actor": "agent:ClaudeCode-dispatch",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target 4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json."
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

### 2026-08-14T08:45:05Z — ClaudeCode/dispatch-review

- **Reviewed repository state:** Immutable target `4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8` (parent `aac09a9ef6cae6699b248523cde75e9b8f861016`; base `10d9610f8d5d6167360b6f5fd4bfdf4392971ac4` confirmed ancestor), extracted via `git archive` into a fresh temporary directory; post-target records through `0625264a9fd7eff018b80053b3d87a98dd8762bd`, where local HEAD, cached `origin/main`, and direct remote `refs/heads/main` are equal with a clean worktree
- **Reviewed target:** `4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8`
- **Open material findings:** `0`
- **Scope:** The complete attempt-1 target — root `ROLE_CONTRACTS.md`, read-only `scripts/run_dispatch.py`, `tests/test_run_dispatch.py` (19 tests), root `README.md` navigation, and the target-range record changes to this issue and `HANDOFF.md` — plus agreement between emitted decisions and the executable pipeline gates. This scope explicitly includes the execution-boundary decision of [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md), so an approving round satisfies that ADR's stated review intent.
- **Commands or procedures:** Target parent/base/ancestry verification; base-to-target path set equals exactly six contract-allowed paths; post-target drift is record-only (`EVIDENCE/`, `HANDOFF.md`, this issue); independent recomputation of both milestone digests with the accepted pipeline parser (milestone 1 `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4` unchanged, milestone 2 `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c` matches the state block and generated evidence); full suite at the `git archive` extraction (`Ran 63 tests ... OK`); structural validator `PASS`; `git diff --check` clean over the target range; a fifteen-scenario independent adverse harness on a disposable clone mutating this issue's real bytes; byte-identity, no-timestamp, and zero-mutation assertions in every scenario; clone baseline output byte-compared against the live repository decision.
- **Specification compliance:** `DISPATCH-001` — `ROLE_CONTRACTS.md` codifies implementer, independent-reviewer, recorder/coordinator, and human-escalation contracts with required inputs, permitted actions, durable outputs, and completion conditions, and agrees with root `BOOTSTRAP.md` (exact three-disposition vocabulary, label-inequality rule, subordination to specification/ADRs). `DISPATCH-002` — eligibility is deterministic from durable state and emitted in every decision; the recorder constraint names both prior labels. `DISPATCH-003` — exactly one next-role decision with contract reference, eligibility, and expected records/commands; identical state produced byte-identical output in every scenario, and the clone baseline is byte-identical to the live decision. `DISPATCH-004` — zero mutation reproduced in every scenario; the script contains no write, subprocess, network, or Git-mutation path. `DISPATCH-005` — one read-only invocation in human and `--json` forms. `DISPATCH-006` — the dispatcher imports the pipeline's `_load_context`, `_selected`, and `_parse_latest_review` rather than reimplementing them; it adds no states and no shadow store. `DISPATCH-007` — `host_adapter` is `manual`; no launch or simulated launch exists. `DISPATCH-008` — Python 3.9 standard library only; the reusable ten-file package is untouched. Dispatch acceptance criteria 1–6 are each satisfied; criterion 6 is this round.
- **Correctness and regression findings:** `NONE`. Routing is correct across `AUTHORIZED`, `READY`, `IN_PROGRESS`, `AWAITING_PEER_REVIEW` (no round, stale-target round, valid `APPROVED`, `CHANGES_REQUIRED`, `BLOCKED`), `CHANGES_REQUIRED`, `BLOCKED_HUMAN_AUTHORITY`, and the all-accepted terminal case, independently reproduced against real record bytes. The emitted `CHANGES_REQUIRED` and `ACCEPTED` commands were executed against the real pipeline gate in the clone and behave exactly as emitted, including post-transition re-routing (fix attempt 2; terminal `none` after acceptance).
- **Architecture and complexity findings:** `NONE`. The declared complexity (second root tool sharing pipeline parsers; role-contract artifact) is covered by the 19 new tests and this round's independent reproduction; no competing state machine was introduced.
- **Material findings and resolution conditions:** `NONE`.
- **Limitations:** The dispatcher requires a Git repository: on a bare `git archive` extraction it fails closed with a stable `AEP-PIPE-STATE` error because the pipeline's state validation requires locally resolvable revisions — consistent with the accepted pipeline's own behavior, not a false pass. The router deliberately does not pre-validate a persisted round's reviewer/implementor label inequality: it routes to the recorder and the pipeline gate rejects the transition (`reviewer label equals implementor label` reproduced); overall behavior is fail-closed, with the gate — not the router — remaining the single enforcement point. A malformed round (including the informal label `APPROVED WITH FINDINGS`) is treated as no round and routes to a fresh independent reviewer, which is fail-safe though its reason text does not distinguish "malformed" from "absent". The pipeline's cross-checks between issue metadata and machine state (status mapping, durable review reference, matching verification evidence) were exercised incidentally and fail closed. Routing-wording adequacy remains human judgment; labels remain unauthenticated operational assertions.
- **Residual risks:** `ROLE_CONTRACTS.md` says an implementer's immutable target's parent "is the attempt's base revision", while the accepted pipeline pattern in both milestones records the `IN_PROGRESS` transition commit as the target's direct parent with the base as an ancestor; the binding gate enforces ancestry and both accepted targets share this shape, so this is a non-material prose imprecision requiring no change before acceptance. Portability beyond the recorded Darwin/Python 3.9.6 environment is unestablished, unchanged from the pipeline milestone.
- **Evidence:** Extracted-target suite and validator runs; the fifteen-scenario adverse harness (disposable clone `/tmp/aep-adverse`, all checks `PASS`); digest recomputation output; identity/scope/drift command outputs quoted in this round; generated submission evidence [`EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json) whose fields the pipeline's own loader re-validates against state authority on every invocation.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** `FIRST ROUND`

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Owner direction

`2026-08-14T05:14:05Z` — Human technical owner `MattSureham` directed: authorize a new PROJECT_SPEC milestone for Automated Role Dispatch / Rotation v1. Eliminate routine human intervention between already-authorized pipeline transitions by making the repository able to determine the next required role, participant eligibility, and role contract from durable project state, across the lifecycle: authorized work → implementer → verify → independent reviewer → fix/re-review when required → recorder/accept → next authorized milestone → repeat. Human escalation occurs only when existing repository authority is insufficient. For v1: codify implementer, reviewer, and recorder/coordinator role contracts; codify participant eligibility and reviewer-independence rules; implement deterministic next-role/dispatch decisions from repository state; preserve all decisions and transitions durably; support interruption/resumption without conversational memory; integrate with the existing pipeline rather than creating a competing state machine. Do not assume the host can launch arbitrary agent sessions; determine and document the execution boundary between repository-native dispatch decisions and host-specific participant/session invocation first, and if the current host exposes no durable programmatic launch interface, implement and verify the repository-native dispatcher first and leave host invocation as an explicit adapter boundary rather than simulating it. No web UI, distributed scheduler, database, external tracker, or unrelated orchestration infrastructure is authorized. Record through the existing specification-evolution and ADR process, then proceed without requesting routine human approval. Use independent peer review before acceptance.

## Residual uncertainty

- Independent review round 1 (`2026-08-14T08:45:05Z`, `ClaudeCode/dispatch-review`) is persisted with disposition `APPROVED` and zero open material findings; the recorder's acceptance gates and closure-checklist completion are the remaining work.
- Host launch capability remains unknown and out of scope; the adapter boundary is documented instead.
- Broader platform portability beyond the recorded Darwin/Python 3.9 environment is unestablished, unchanged from the pipeline milestone.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-14T05:14:05Z` | `ClaudeCode/root` | `NONE` | `OPEN` | Created from the explicit owner direction after verifying the first pipeline milestone is `ACCEPTED`, both wording issues are `CLOSED`, and the repository was in its terminal wait state |
| `2026-08-14T05:14:05Z` | `ClaudeCode/root` | `OPEN` | `INVESTIGATING` | Recorded the accepted specification phase, compatible accepted ADR, contract digest `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c`, and execution-boundary decision before any implementation |
| `2026-08-14T05:30:25Z` | `agent:ClaudeCode-dispatch` | `INVESTIGATING` | `INVESTIGATING` | Pipeline AUTHORIZED -> READY. Validated transition AUTHORIZED to READY. |
| `2026-08-14T05:30:34Z` | `agent:ClaudeCode-dispatch` | `INVESTIGATING` | `IMPLEMENTING` | Pipeline READY -> IN_PROGRESS. Implementation attempt 1 began from immutable base 10d9610f8d5d6167360b6f5fd4bfdf4392971ac4. |
| `2026-08-14T05:43:14Z` | `agent:ClaudeCode-dispatch` | `IMPLEMENTING` | `IMPLEMENTING` | Implemented attempt 1 within the contract allowed paths: root `ROLE_CONTRACTS.md` (implementer, independent-reviewer, recorder/coordinator, human-escalation contracts plus the documented manual host adapter boundary), read-only `scripts/run_dispatch.py` reusing the accepted pipeline parsers, and 19-test `tests/test_run_dispatch.py` covering every dispatch-relevant state; `README.md` navigation updated; 63 tests and the structural validator pass; verification rows recorded above |
| `2026-08-14T05:48:59Z` | `agent:ClaudeCode-dispatch` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target 4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T054859Z-milestone-20260814t051405z-role-dispatch-v1-attempt-1.json. |
| `2026-08-14T08:45:05Z` | `ClaudeCode/dispatch-review` | `REVIEW` | `REVIEW` | Recorded independent review round 1 on immutable target `4a2601f`: `APPROVED` with zero open material findings after extracted-target verification and a fifteen-scenario adverse reproduction; the `ACCEPTED` transition and closure-checklist completion remain with the next recorder, whose label must differ from `agent:ClaudeCode-dispatch` and `ClaudeCode/dispatch-review`. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies. — `NOT_APPLICABLE`: review is `INDEPENDENT`.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted dispatch phase and compatible accepted ADR.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
