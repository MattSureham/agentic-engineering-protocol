# Host Adapter and Participant Rotation v1

## Metadata

- **ID:** `ISSUE-20260814T092504Z-host-adapter-rotation`
- **Title:** Implement the authorized host adapter and participant rotation milestone
- **Status:** `INVESTIGATING`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-14T09:25:04Z`
- **Updated UTC:** `2026-08-14T09:25:04Z`
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

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260814T092504Z-host-rotation-v1",
  "authority_digest": "a38bb7bfd1511045e8e09b4a0dc6af7893f24a8a833e9a3faa444660cc3b977b",
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
      "utc": "2026-08-14T09:25:04Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Explicit host adapter and automated participant rotation owner direction accepted through specification evolution with a compatible accepted ADR and live host-capability probe evidence."
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

No independent review round has been recorded. Review begins after the first immutable implementation target is submitted through the pipeline.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NOT APPLICABLE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Host rate limits, concurrency, long-running session stability, authentication-mode variation, and CLI envelope stability across versions remain `UNKNOWN` and are owned by this issue's adapter fail-closed requirement; the owner accepts this residual risk within the authorized slice.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-14T09:25:04Z` | `human:MattSureham` | `NONE` | `INVESTIGATING` | Owner direction authorized the host adapter and participant rotation phase; specification evolution, accepted ADR, probe evidence, and this owning issue recorded; pipeline state `AUTHORIZED` |

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
