# Issue — Pipeline contract lacks an exit from BLOCKED_HUMAN_AUTHORITY

## Metadata

- **ID:** `ISSUE-20260923T013206Z-pipeline-blocked-exit`
- **Title:** Accepted pipeline contract defines entry into BLOCKED_HUMAN_AUTHORITY but no exit edge; discovery milestone is machine-blocked with the human gate satisfied
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `human:MattSureham`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-09-23T01:32:06Z`
- **Updated UTC:** `2026-09-23T01:32:06Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `PIPELINE-003`, `ROTATE-004`
- **ADRs:** [ADR-20260814T015817Z](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md) decision 5
- **Evidence:** [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUE-20260922T073608Z-codex-quota-authorization.md) (owner decision recorded 2026-09-23T01:32:06Z)
- **Milestone:** `milestone-20260918t064510z-prompt-independent-discovery-v1`

## Problem

The accepted pipeline state machine (ADR-20260814T015817Z decision 5; PROJECT_SPEC `PIPELINE-003`) defines transitions *into* `BLOCKED_HUMAN_AUTHORITY` but no transition *out of* it. `scripts/run_pipeline.py` therefore refuses every transition away from that state, and the dispatcher under `BLOCKED_HUMAN_AUTHORITY` emits only the `human-escalation` role. The discovery milestone entered `BLOCKED_HUMAN_AUTHORITY` at 2026-09-22T07:51:33Z over the owner's Codex quota directive. The owner has now recorded the bounded authorization decision in [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUE-20260922T073608Z-codex-quota-authorization.md) — the human gate is satisfied — but no contract-conformant machine exit exists, and machine state blocks are never hand-edited.

Self-correction recorded with this issue: the 2026-09-22 entry transition also misapplied the contract. `ROTATE-004` classifies quota/budget exhaustion as a participant failure that MUST NOT produce a `BLOCKED_HUMAN_AUTHORITY` transition. The genuine human gate was the owner's resource directive (a human authority decision), so the *state* was arguably reachable on that ground, but the recorded reason conflated the quota failure with the owner directive. This correction does not change the current state; it corrects the record.

## Evidence or reproduction

1. `scripts/run_pipeline.py` `TRANSITIONS` contains no key with source `BLOCKED_HUMAN_AUTHORITY`.
2. Attempted and refused: any `run_pipeline.py transition … --from BLOCKED_HUMAN_AUTHORITY` exits with the illegal-transition error (observed 2026-09-23 when reconciling the recorded owner decision against machine state; no state mutation occurred).
3. Milestone state block in [ISSUE-20260918T064510Z](ISSUE-20260918T064510Z-prompt-independent-discovery.md) shows `BLOCKED_HUMAN_AUTHORITY` since `2026-09-22T07:51:33Z` while its blocker issue's unblock condition is now satisfied by the recorded owner decision.

## Expected behavior

When the human authority gate that produced `BLOCKED_HUMAN_AUTHORITY` is resolved by a recorded owner decision in the blocking issue, a contract-conformant transition returns the milestone to an executable state (for example `IN_PROGRESS` or `CHANGES_REQUIRED` as applicable), so ordinary pipeline work can resume under the recorded owner bounds.

## Assumptions

- **CONFIRMED:** The machine contract has no exit edge from `BLOCKED_HUMAN_AUTHORITY` (source inspection).
- **CONFIRMED:** The owner decision satisfying the human gate is durably recorded (linked issue).
- **INFERRED:** Adding the exit edge is a contract/specification change requiring owner approval; no participant may amend the pipeline contract unilaterally.

## Investigation and decision

Proposed minimal contract amendment, submitted for owner approval (not implemented):

1. Add transition `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` (and, if the owner prefers, `BLOCKED_HUMAN_AUTHORITY → CHANGES_REQUIRED`), gated on: the blocking issue records a dated owner decision satisfying its unblock condition, the working tree is clean, and the transition command carries the blocker issue ID.
2. Record the gate check in the milestone's activity history exactly as other transitions do.
3. No other state-machine semantics change; `ROTATE-004`'s prohibition on quota-driven `BLOCKED_HUMAN_AUTHORITY` entries is reaffirmed, and entry validation should reject quota/participant-failure rationales.

The owner may approve, amend, or reject this proposal, or direct a different disposition. No code or specification change has been made under this issue.

## Change

- **Files or components:** None yet — pending owner decision on the proposed amendment.
- **Behavior changed:** None.
- **Out-of-scope work deliberately excluded:** Any hand-edit of milestone state blocks; any transition executed outside `run_pipeline.py`; any Codex live launch.
- **Rollback or recovery:** NOT APPLICABLE (no mutation performed).

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| NONE | — | — | — |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-09-23T01:32:06Z` | `agent:ClaudeCode-discovery-fix-3` | Source inspection of `scripts/run_pipeline.py` (`TRANSITIONS`, `_legal_transition`) against the recorded owner decision | No exit edge from `BLOCKED_HUMAN_AUTHORITY` exists; gap confirmed without mutating state | This issue | Inspection only; no dynamic probe of the transition validator was run |

## Pipeline state (optional)

NOT APPLICABLE.

## Self-review

- **Outcome:** `NOT_APPLICABLE` (no implementation change; this issue proposes a contract amendment for owner decision).

## Independent review rounds

- **Required:** YES if the owner approves a contract amendment — the amendment changes the accepted pipeline contract and must follow the ordinary specification-evolution review path. This record-keeping issue itself launches no change.

## Blocker

- **Blocked from:** any transition out of `BLOCKED_HUMAN_AUTHORITY` for the discovery milestone.
- **Blocker:** The accepted pipeline contract lacks the exit edge; adding it requires owner-approved contract evolution.
- **Unblock owner:** `human:MattSureham`
- **Unblock condition:** The owner records a decision on the proposed amendment (approve/amend/reject). On approval, an implementer amends ADR-20260814T015817Z (or a superseding ADR), PROJECT_SPEC `PIPELINE-003`, and `scripts/run_pipeline.py` under ordinary change control, then executes the unblocked transition for the discovery milestone.

## Residual uncertainty

- Whether the owner prefers `IN_PROGRESS` or `CHANGES_REQUIRED` as the exit target for milestones whose human gate is resolved mid-attempt is UNKNOWN until the decision is recorded. The proposal defaults to `IN_PROGRESS` (work resumes under recorded bounds).

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-23T01:32:06Z` | `agent:ClaudeCode-discovery-fix-3` | `NONE` | `BLOCKED` | Recorded the contract gap discovered while persisting the owner's bounded Codex authorization: no machine exit from `BLOCKED_HUMAN_AUTHORITY` exists, and the 2026-09-22 entry misapplied `ROTATE-004`. Proposed a minimal exit-edge amendment; awaiting owner decision. No state block was hand-edited and no Codex session was launched. |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is recorded — NOT APPLICABLE here (`Review: INDEPENDENT` if the amendment is approved).
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: the owner decision on the amendment is pending and is the purpose of this issue.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (NONE added).
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
