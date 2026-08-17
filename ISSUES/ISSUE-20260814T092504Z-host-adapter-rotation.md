# Host Adapter and Participant Rotation v1

## Metadata

- **ID:** `ISSUE-20260814T092504Z-host-adapter-rotation`
- **Title:** Implement the authorized host adapter and participant rotation milestone
- **Status:** `CLOSED`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-14T09:25:04Z`
- **Updated UTC:** `2026-08-17T01:50:59Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Host adapter and participant rotation phase and `MILESTONE-20260814T092504Z-host-rotation-v1`
- **ADRs:** [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md); [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md) (live host capability probes establishing the launch-interface boundary)
- **Milestone:** `MILESTONE-20260814T092504Z-host-rotation-v1`

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The accepted dispatcher emits a deterministic next-role decision, but every decision still requires an operator to start the next participant session by hand and supply the role contract. The human technical owner has directed continuing toward automated participant rotation: consume the dispatch decision, select an eligible participant, invoke it through the host adapter where a real supported interface exists, distinguish participant unavailability from missing authority, handle quota exhaustion and failure without incorrectly escalating to human authority, retry or rotate when permitted, preserve role independence, recover from interruption via durable repository state, continue already-authorized transitions without routine human approval, and stop cleanly on the terminal decision or genuine human-authority need.

## Evidence or reproduction

- **CONFIRMED:** The dispatcher currently terminates with `ROLE none` on this repository; both authorized milestones are `ACCEPTED` and their owning issues `CLOSED` at synchronized revision `cc19209ec5a95e769f80834ec614f1db95c4c690`.
- **CONFIRMED:** [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md) establishes from live probes that this host's Claude Code CLI `2.1.118` supports programmatic headless sessions with JSON result envelopes, budget caps, a machine-readable budget-exhaustion class (`error_max_budget_usd`, exit `1`), and resumable session identity, and that no `paseo` binary or project exists.
- **CONFIRMED:** The accepted dispatch ADR conditions a real adapter on "a host that exposes a genuine durable launch interface"; that precondition is now evidence-satisfied, and the owner direction of `2026-08-14T09:25:04Z` authorizes this exact milestone.

## Expected behavior

Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Host adapter and participant rotation phase (`ROTATE-001`–`ROTATE-008`), and the rotation acceptance criteria define the expected result: a root-only rotation runner that consumes only dispatcher decisions, a durable participant registry with pre-launch independence filtering, an append-only rotation ledger, a failure taxonomy that never maps participant failure to `BLOCKED_HUMAN_AUTHORITY`, declared retry/step/spend bounds, repository-state recovery, clean termination, and a stub-launcher test suite. Compatible architecture is recorded in [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md).

## Assumptions

- **CONFIRMED:** The dispatcher exposes `--json` machine-readable decisions with eligibility constraints and expected commands; the runner can consume them without modifying the accepted dispatcher or pipeline tools.
- **CONFIRMED:** The reusable ten-file package is out of scope; all new runtime is root-only.
- **INFERRED:** A single-host adapter with a stub-injected launcher is the smallest design satisfying the direction. Facts: the launch interface is probed, the dispatcher decision is machine-readable, and the registry/ledger require only files.
- **UNKNOWN:** Host rate limits, concurrent-session behavior, long-running session stability, authentication-mode variation, and CLI envelope stability across versions. Resolution path: outside the authorized slice; the adapter must fail closed on unrecognized envelope behavior.

## Investigation and decision

The owner direction is recorded through specification evolution and summarized in [`HUMAN_CHECKPOINT.md`](../HUMAN_CHECKPOINT.md). The capability-boundary analysis required by the direction is recorded in the probe evidence; the execution architecture is decided in the accepted ADR: dispatcher as sole routing authority, evidence-bounded interface, registry with independence filtering, failure taxonomy without false escalation, append-only ledger, repository-state recovery, declared bounds, and stub-only tests. No further product or architecture question is open.

## Change

- **Files or components:** New root-only `scripts/run_rotation.py`; new `ROTATION_PARTICIPANTS.json`; new append-only `ROTATION_LOG.jsonl`; new `tests/test_run_rotation.py`; root `ROLE_CONTRACTS.md` adapter/rotation guidance; root `README.md` navigation; this issue; `HANDOFF.md`; `HUMAN_CHECKPOINT.md`; generated evidence under `EVIDENCE/`.
- **Behavior changed:** The repository gains automated execution of dispatcher decisions through the probe-verified host CLI interface, with bounded retry/rotation and durable per-step records.
- **Out-of-scope work deliberately excluded:** Any unprobed session API (including anything named Paseo); changes to the accepted pipeline or dispatcher tools; new milestone states; daemons, schedulers, databases, web UIs, or tracker integrations; reusable-package changes; the four still-`BLOCKED` capability deferrals; real agent launches inside the test suite.
- **Rollback or recovery:** Revert the immutable rotation target while preserving this owner direction, the accepted specification/ADR records, and the probe evidence. `ROTATION_LOG.jsonl` is append-only operational evidence and is never rewritten.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Third root Python tool plus registry and ledger files | Execute dispatch decisions without touching accepted tools | Rotation acceptance criteria; stub-launcher tests across every outcome class | Semantic adequacy of participant prompts and recovery wording remains reviewer judgment |
| Real quota spend driven by tooling | Participants must actually run to close the loop | Declared spend/step/attempt bounds; budget-exhaustion classification from probe evidence | Host rate limits and concurrency behavior remain unprobed |
| Automated label-based independence enforcement | Independence must hold without a human in the loop | Pre-launch filtering tests; existing executable pipeline gates unchanged | [`ISSUE-20260806T013907Z-authenticated-identity-approval`](ISSUE-20260806T013907Z-authenticated-identity-approval.md) |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-14T09:25:04Z` | `ClaudeCode/root` | Authority-boundary recording only: parsed the updated three-milestone contract with the accepted pipeline parser; verified milestone-1 and milestone-2 digests unchanged and milestone-3 digest computed | Contract parses; milestone-1 digest `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4` unchanged; milestone-2 digest `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c` unchanged; milestone-3 digest `a38bb7bfd1511045e8e09b4a0dc6af7893f24a8a833e9a3faa444660cc3b977b` | This issue and the accepted specification/ADR | No implementation exists yet; deterministic verification begins with the first attempt |
| `2026-08-14T09:25:04Z` | `ClaudeCode/root` | Live host capability probes in `/tmp/aep-host-probe` (launch, budget exhaustion, resume; presence probe for `paseo` and `claude`) | Launch exit `0` (`subtype: success`); budget exhaustion exit `1` (`subtype: error_max_budget_usd`); resume exit `0` with identical `session_id`; `paseo` absent; `claude` `2.1.118` | [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md) | Single host, single CLI version; rate limits and concurrency unprobed |
| `2026-08-14T10:03:49Z` | `agent:ClaudeCode-rotation` | `python3 -m unittest discover -s tests -v` | 89 tests `OK` (63 retained pipeline/structural/dispatch tests plus 26 new rotation tests), exit `0` | `tests/test_run_rotation.py` and this row | Stub launcher only; no real session launched; recorded Darwin/Python 3.9 environment |
| `2026-08-14T10:03:49Z` | `agent:ClaudeCode-rotation` | `python3 scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)`, exit `0` | Inline | Structural invariants only |
| `2026-08-14T10:03:49Z` | `agent:ClaudeCode-rotation` | Rotation acceptance-criteria coverage: stubbed-decision routing; every probed failure class (launch failure, budget exhaustion, timeout, session error, non-advancing); pre-launch independence filtering for reviewer/recorder/bound-implementor; exhausted-pool stop without escalation; crash truncation with restart at ledger steps; append-only ledger fields; attempt/step/spend bounds; CLI end-to-end against the real dispatcher binary on a fixture repository in the terminal state | Each maps to the expected outcome class or stop reason with ledger records; no scenario produces a `BLOCKED_HUMAN_AUTHORITY` transition; unrecognized eligibility constraints and envelope shapes fail closed | `tests/test_run_rotation.py` (26 tests) | Live runner invocation against this repository deliberately not exercised: the live decision is this attempt's own implementer role, and a real launch is operational use, not verification |

- **Pipeline verification `2026-08-14T10:13:57Z`:** [`EVIDENCE/EVIDENCE-20260814T101357Z-milestone-20260814t092504z-host-rotation-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T101357Z-milestone-20260814t092504z-host-rotation-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `d6471f54b7e75f255b308d44885146762642b261`.

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260814T092504Z-host-rotation-v1",
  "authority_digest": "a38bb7bfd1511045e8e09b4a0dc6af7893f24a8a833e9a3faa444660cc3b977b",
  "state": "ACCEPTED",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-rotation",
  "base_revision": "a21997dabfcc555c2b82458789aa75871f787055",
  "target_revision": "d6471f54b7e75f255b308d44885146762642b261",
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260814T101357Z-milestone-20260814t092504z-host-rotation-v1-attempt-1.json"
  ],
  "review_references": [
    "ISSUES/ISSUE-20260814T092504Z-host-adapter-rotation.md#2026-08-17t014005z--claudecoderotation-review"
  ],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-08-14T09:25:04Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Explicit host adapter and automated participant rotation owner direction accepted through specification evolution with a compatible accepted ADR and live host-capability probe evidence."
    },
    {
      "sequence": 2,
      "utc": "2026-08-14T09:52:19Z",
      "actor": "agent:ClaudeCode-rotation",
      "from": "AUTHORIZED",
      "to": "READY",
      "reason": "Validated transition AUTHORIZED to READY."
    },
    {
      "sequence": 3,
      "utc": "2026-08-14T09:52:19Z",
      "actor": "agent:ClaudeCode-rotation",
      "from": "READY",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 1 began from immutable base a21997dabfcc555c2b82458789aa75871f787055."
    },
    {
      "sequence": 4,
      "utc": "2026-08-14T10:13:57Z",
      "actor": "agent:ClaudeCode-rotation",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target d6471f54b7e75f255b308d44885146762642b261 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T101357Z-milestone-20260814t092504z-host-rotation-v1-attempt-1.json."
    },
    {
      "sequence": 5,
      "utc": "2026-08-17T01:50:59Z",
      "actor": "agent:ClaudeCode-rotation-record",
      "from": "AWAITING_PEER_REVIEW",
      "to": "ACCEPTED",
      "reason": "Independent review ISSUES/ISSUE-20260814T092504Z-host-adapter-rotation.md#2026-08-17t014005z--claudecoderotation-review approved the verified target with zero open material findings."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Self-review

- **Participant:** `ClaudeCode/root`
- **Reviewed UTC:** `2026-08-14T09:25:04Z`
- **Reviewed repository state:** Authority-boundary records only; synchronized baseline `cc19209ec5a95e769f80834ec614f1db95c4c690` plus the records created by this issue's phase
- **Scope and authority references:** Root `PROJECT_SPEC.md` rotation phase, accepted ADR, probe evidence; no implementation exists
- **Checks and evidence reviewed:** Contract digest parse (row above); probe evidence completeness against the owner direction's capability list
- **Findings and corrections:** NONE
- **Limitations:** No implementation to review; this self-review covers authority-recording consistency only
- **Residual risks:** NONE beyond the declared UNKNOWNs
- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES` — the milestone adds a runtime component that spends host quota and launches sessions acting on authority-bound state.

### 2026-08-17T01:40:05Z — ClaudeCode/rotation-review

- **Reviewed repository state:** Clean synchronized `c1e0ab2f23507737f7430014783d79f5472081ad` (local HEAD, cached `origin/main`, and direct remote `refs/heads/main` equal); dispatcher routing to `independent-reviewer` for `AWAITING_PEER_REVIEW` milestone 3; read-only `git archive` extraction of the target at `/tmp/aep-rotation-review`.
- **Reviewed target:** `d6471f54b7e75f255b308d44885146762642b261`
- **Open material findings:** `0`
- **Scope:** Accepted rotation phase (`ROTATE-001`–`ROTATE-008`, six acceptance criteria, milestone-3 contract) in root `PROJECT_SPEC.md`; accepted [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md); [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md); the complete base→target diff (`scripts/run_rotation.py`, `tests/test_run_rotation.py`, `ROTATION_PARTICIPANTS.json`, `ROTATION_LOG.jsonl`, `ROLE_CONTRACTS.md`, `README.md`, this issue, `HANDOFF.md`); the generated submission evidence; the dispatcher and pipeline tools the runner integrates with; raw probe envelopes at `/tmp/aep-host-probe`.
- **Commands or procedures:** `git log/diff/diff --check/merge-base` over `a21997dabfcc555c2b82458789aa75871f787055..d6471f54b7e75f255b308d44885146762642b261` and post-target range; `git archive` extraction then `python3 -m unittest discover -s tests` (89 tests `OK`) and `python3 scripts/validate_protocol.py` (`PASS`) at the extraction; milestone digests recomputed at the target with the accepted pipeline parser (milestone 3 `a38bb7bfd1511045e8e09b4a0dc6af7893f24a8a833e9a3faa444660cc3b977b`, milestones 1/2 unchanged); an independent eight-scenario adverse harness (`/tmp/aep_rotation_adverse.py`, run against the extraction, all `PASS`): R1 every real dispatcher decision across `AUTHORIZED`/`READY`/`IN_PROGRESS`/`AWAITING_PEER_REVIEW` (no round, `APPROVED`, `CHANGES_REQUIRED`, `BLOCKED`) fed through `parse_constraints`/`select_participant` with correct independence filtering; R2 the three raw captured probe envelopes classified (`success`, `quota_exhausted`, `success`); R3 end-to-end on a real fixture repository with the real dispatcher binary and a stub participant executing the emitted transitions — the runner advanced `AUTHORIZED`→`READY`→`IN_PROGRESS`, mutated only the ledger itself, and stopped `steps_exhausted`; R4 `launch_failure`/`timeout`/`quota_exhausted` sequence exhausted the durable attempts bound with no `BLOCKED_HUMAN_AUTHORITY` anywhere in the ledger and durability across restart; R5 deceptive envelopes (success+`is_error`, success+exit 1, missing `subtype`, wrong `type`, budget subtype without `is_error`) all failed closed to `session_error`; R6 malformed ledger line fails closed with exit `2`/`AEP-ROTATE-SCHEMA`; R7 prompt built from a real dispatcher decision substitutes the participant label with no residual placeholder; R8 crash after the participant's transition landed but before the outcome append recovers as `success_advancing` with no duplicate transition and no duplicate launch.
- **Specification compliance:** `ROTATE-001` (dispatcher sole routing authority — the runner calls `run_dispatch.py --json`, rejects non-conforming output, and never executes transitions itself; R3 confirmed transitions land only through participant-executed emitted commands), `ROTATE-002` (launch uses exactly the probed flags `-p`, `--output-format json`, `--tools`, `--max-budget-usd`; R2 confirmed probed envelopes classify; unrecognized shapes fail closed), `ROTATE-003` (registry schema validation, label validity via the pipeline's `ACTOR_RE`, uniqueness; pre-launch independence filtering confirmed for reviewer, recorder, and bound implementor in R1), `ROTATE-004` (failure taxonomy exhaustive and fail-closed; R4/R5 confirmed no participant failure produces or approaches `BLOCKED_HUMAN_AUTHORITY`), `ROTATE-005` (attempts bound durable in the ledger, steps/spend per invocation; R4 and the implementer's bounds tests), `ROTATE-006` (append-only ledger with label/session/outcome/cost; repository-state recovery without duplicate transitions confirmed in R8), `ROTATE-007` (clean stops for terminal, human-authority, no-eligible-participant, and each exhausted bound), `ROTATE-008` (stdlib Python 3.9, root-only, no daemon/scheduler/db/web UI/tracker, no package change, stub-only tests — the CLI test launches nothing and asserts it). All six rotation acceptance criteria are satisfied by the suite plus the independent reproductions above.
- **Correctness and regression findings:** None. The extracted-target suite passes 89 tests; the structural validator passes; digests, base ancestry (target parent is the `IN_PROGRESS` record `aef0201`, base `a21997d` an ancestor, matching the accepted pattern), allowed-path scope (eight paths, all inside the contract), and record-only post-target drift (evidence, HANDOFF, owning issue) all reproduce.
- **Architecture and complexity findings:** None material. The runner adds no state machine, no second authority source, and no Git mutation beyond the ledger; the accepted pipeline gates remain the single mutation path (R3 exercised them end-to-end).
- **Material findings and resolution conditions:** `NONE`.
- **Limitations:** Live runner invocation against this repository was deliberately not exercised (it would launch real sessions — operational use, not review); host rate limits, concurrency, long-running stability, and cross-version envelope stability remain unprobed as recorded; the fixture end-to-end used a perfect stub participant, so real participant behavior is not evidence-covered; review ran on Darwin/Python 3.9.6 only.
- **Residual risks:** (1) The implementer's suite covered `parse_constraints` only with synthetic eligibility strings — the coverage gap is real but independently closed by R1 against the genuine dispatcher in every state; drift between dispatcher templates and runner regexes remains caught by review and tests. (2) Ledger appends dirty the worktree between launches, so participants must commit the ledger before pipeline transitions (documented in `ROLE_CONTRACTS.md` and this issue's residual uncertainty); the pipeline gate fails closed otherwise. (3) `<participant-label>` substitution is string-exact against the accepted dispatcher's stable placeholder. (4) Participant-prompt wording adequacy remains semantic judgment, as recorded.
- **Evidence:** Implementor verification rows and generated submission evidence above; independent reproduction outputs quoted under Commands or procedures (extraction suite/validator, digest recomputation, eight-scenario harness `TOTAL 8 FAILED 0`).
- **Disposition:** `APPROVED`
- **Prior-round resolution:** `FIRST ROUND`

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NOT APPLICABLE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Host rate limits, concurrency, long-running session stability, authentication-mode variation, and CLI envelope stability across versions remain `UNKNOWN` and are owned by this issue's adapter fail-closed requirement; the owner accepts this residual risk within the authorized slice.
- Participant-prompt wording and recovery-message wording are implementation decisions now frozen in the target; their semantic adequacy remains reviewer judgment, as recorded under Unverified complexity.
- The runner interprets the dispatcher's emitted eligibility strings against the accepted dispatcher's exact stable templates and fails closed on any unrecognized phrasing; drift between the two tools' wording is caught by the dispatch milestone's byte-identity tests plus this suite's routing tests.
- `ISSUES/TEMPLATE.md` carries a prose line under `## Activity history` that the accepted pipeline's activity-table gate rejects; the owning issue dropped that line to conform (commit `a9a7fb0`). The template itself is outside this milestone's allowed paths, so the template/tool drift is recorded here for owner visibility rather than fixed.
- The runner executes no transitions itself; launched participants run the dispatcher-emitted commands and commit their record changes, because the pipeline's cleanliness gate rejects a dirty tree. This division is recorded in `ROLE_CONTRACTS.md` and remains reviewer judgment.
- Independent review round 1 (`2026-08-17T01:40:05Z`) is `APPROVED` with zero open material findings; its residual risks (synthetic-only constraint coverage in the implementer suite, ledger/tree-dirtiness coupling, string-exact placeholder substitution, prompt-wording judgment) are recorded in the round and accepted as non-material.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-14T09:25:04Z` | `human:MattSureham` | `NONE` | `INVESTIGATING` | Owner direction authorized the host adapter and participant rotation phase; specification evolution, accepted ADR, probe evidence, and this owning issue recorded; pipeline state `AUTHORIZED` |
| `2026-08-14T09:52:19Z` | `agent:ClaudeCode-rotation` | `INVESTIGATING` | `INVESTIGATING` | Pipeline AUTHORIZED -> READY. Validated transition AUTHORIZED to READY. |
| `2026-08-14T09:52:19Z` | `agent:ClaudeCode-rotation` | `INVESTIGATING` | `IMPLEMENTING` | Pipeline READY -> IN_PROGRESS. Implementation attempt 1 began from immutable base a21997dabfcc555c2b82458789aa75871f787055. |
| `2026-08-14T10:03:49Z` | `agent:ClaudeCode-rotation` | `IMPLEMENTING` | `IMPLEMENTING` | Implemented attempt 1 within the contract allowed paths: `scripts/run_rotation.py` (dispatcher-consuming bounded runner with stub-injectable launcher, probed-envelope taxonomy, independence filtering, recovery, append-only ledger), `ROTATION_PARTICIPANTS.json` registry, empty durable `ROTATION_LOG.jsonl`, 26-test `tests/test_run_rotation.py`, `ROLE_CONTRACTS.md` adapter/rotation guidance, `README.md` navigation; owning-issue activity section conformed to the pipeline table gate (`a9a7fb0`); 89 tests and the structural validator pass; verification rows recorded above |
| `2026-08-14T10:13:57Z` | `agent:ClaudeCode-rotation` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target d6471f54b7e75f255b308d44885146762642b261 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T101357Z-milestone-20260814t092504z-host-rotation-v1-attempt-1.json. |
| `2026-08-17T01:40:05Z` | `ClaudeCode/rotation-review` | `REVIEW` | `REVIEW` | Independent review round 1 persisted: target `d6471f54b7e75f255b308d44885146762642b261`, disposition `APPROVED`, zero open material findings, after extracted-target verification and an eight-scenario adverse reproduction including real-dispatcher constraint parsing, real probe-envelope classification, end-to-end stub-participant advancement, failure-taxonomy non-escalation, and crash recovery without duplicate transitions. |
| `2026-08-17T01:52:00Z` | `ClaudeCode/rotation-record` | `REVIEW` | `REVIEW` | Recorder verification before acceptance, without re-review: dispatcher routes to the recorder role and this label differs from both prior labels; the persisted round is mechanically parseable with disposition `APPROVED` and zero open material findings on the exact verified target `d6471f54b7e75f255b308d44885146762642b261`; reviewer/implementor label inequality holds; base ancestry reproduced; post-target drift through `1be3a2c` is record-only; local HEAD, cached `origin/main`, and direct remote are equal with a clean worktree; completed the two evidence-supported closure-checklist items. |
| `2026-08-17T01:50:59Z` | `agent:ClaudeCode-rotation-record` | `REVIEW` | `CLOSED` | Pipeline AWAITING_PEER_REVIEW -> ACCEPTED. Independent review ISSUES/ISSUE-20260814T092504Z-host-adapter-rotation.md#2026-08-17t014005z--claudecoderotation-review approved the verified target with zero open material findings. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies. — `NOT_APPLICABLE`: review is `INDEPENDENT`.
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved. — Round 1 of `2026-08-17T01:40:05Z` by `ClaudeCode/rotation-review` is `APPROVED` with zero open material findings on verified target `d6471f54b7e75f255b308d44885146762642b261` (`FIRST ROUND`, so no prior material findings exist to resolve). Recorder `ClaudeCode/rotation-record` independently confirmed from durable records on `2026-08-17T01:52:00Z` without re-reviewing: the persisted round carries exactly one `Reviewed target`, `Open material findings`, and `Disposition` field each; the reviewed target equals the pipeline state block's `target_revision`; reviewer label `ClaudeCode/rotation-review` differs from implementor `agent:ClaudeCode-rotation`; base `a21997dabfcc555c2b82458789aa75871f787055` is an ancestor of the target; post-target drift through `1be3a2c50422de16a287b1460fa602d75608cecd` is record-only (`EVIDENCE/`, `HANDOFF.md`, this issue); and local HEAD, cached `origin/main`, and direct remote `refs/heads/main` are equal with a clean worktree.
- [x] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action. — `ClaudeCode/rotation-record` reconciles HANDOFF and `HUMAN_CHECKPOINT.md` in the record-only reconciliation commit immediately following the pipeline-validated `ACCEPTED` transition, leaving the dispatcher's resulting decision as the single exposed next action; this item is checked against that committed reconciliation.
