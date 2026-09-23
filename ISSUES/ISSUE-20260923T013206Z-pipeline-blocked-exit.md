# Issue — Pipeline contract lacks an exit from BLOCKED_HUMAN_AUTHORITY

## Metadata

- **ID:** `ISSUE-20260923T013206Z-pipeline-blocked-exit`
- **Title:** Accepted pipeline contract defines entry into BLOCKED_HUMAN_AUTHORITY but no exit edge; discovery milestone is machine-blocked with the human gate satisfied
- **Status:** `OPEN`
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

### Owner decision recorded 2026-09-23T01:32:06Z (approval) — implemented 2026-09-23

Human technical owner `MattSureham` **approved** the proposed amendment with explicit bounds: add only `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS`, gated on (1) the producing human-authority decision durably recorded in the blocker issue, (2) that decision satisfying the original authority condition, (3) transition evidence citing the owner decision, and (4) no other unresolved human-authority blocker. The owner also formalized: every enterable blocking state must have a verifiable exit; the unblock resolves only the authority blocker and authorizes no separately gated execution, resource budget, or paid operation; independent execution gates survive the unblock; quota exhaustion alone is a participant/resource failure and must not produce `BLOCKED_HUMAN_AUTHORITY` (the 2026-09-22 record is preserved with an attributable correction, not rewritten); and the amendment must not expand to new states or redesign the state machine.

**Implementation (this change):**

- `scripts/run_pipeline.py`: `TRANSITIONS` gains `("BLOCKED_HUMAN_AUTHORITY", "IN_PROGRESS")`. The resume requires `--blocker-issue` naming the blocker recorded in the entry event, validated by `_human_blocker_resolved` (Authority `HUMAN`, Status no longer `BLOCKED`, nonempty unblock condition) and `_blocked_entry_blocker` (named blocker must match the entry record); the interrupted attempt, implementor, and base revision are preserved; the transition reason cites the recorded decision; the owning issue's Blocker section is reset. `--blocker-issue` remains rejected for every other `IN_PROGRESS` entry.
- `PROJECT_SPEC.md`: PIPELINE-003 references the exit; new PIPELINE-009 formalizes the exit-semantics, no-side-effect-authorization, and quota-failure principles; change-record row appended.
- `ADR-20260814T015817Z`: decision 5 amended with the exit edge and gates; status-history row appended.
- `tests/test_run_pipeline.py`: deterministic coverage for resume success (attempt preserved, decision cited, blocker section cleared), unresolved-blocker refusal without mutation, missing/mismatched blocker refusal, dirty-tree refusal, `--blocker-issue` rejection on ordinary `IN_PROGRESS`, and refusal of all other target states from `BLOCKED_HUMAN_AUTHORITY`.

**Review status:** per this issue's `Review: INDEPENDENT`, the amendment awaits an independent review round; none has occurred.

### Original proposal (superseded by the recorded approval above)

Proposed minimal contract amendment, as submitted for owner approval:

1. Add transition `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` (and, if the owner prefers, `BLOCKED_HUMAN_AUTHORITY → CHANGES_REQUIRED`), gated on: the blocking issue records a dated owner decision satisfying its unblock condition, the working tree is clean, and the transition command carries the blocker issue ID.
2. Record the gate check in the milestone's activity history exactly as other transitions do.
3. No other state-machine semantics change; `ROTATE-004`'s prohibition on quota-driven `BLOCKED_HUMAN_AUTHORITY` entries is reaffirmed, and entry validation should reject quota/participant-failure rationales.

## Change

- **Files or components:** `scripts/run_pipeline.py` (exit edge + `_human_blocker_resolved` + `_blocked_entry_blocker` + resume branch + Blocker-section reset), `PROJECT_SPEC.md` (PIPELINE-003 wording, new PIPELINE-009, change-record row), `ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md` (decision 5 amendment + status-history row), `tests/test_run_pipeline.py` (four new deterministic tests).
- **Behavior changed:** A milestone in `BLOCKED_HUMAN_AUTHORITY` can now return to `IN_PROGRESS` when the entry blocker issue records the owner decision (Status no longer `BLOCKED`, Authority `HUMAN`, nonempty unblock condition) and the transition names that same blocker; the interrupted attempt is preserved and the reason cites the recorded decision. All other transitions are unchanged.
- **Out-of-scope work deliberately excluded:** Any hand-edit of milestone state blocks; any transition executed outside `run_pipeline.py`; any Codex live launch; any new pipeline state or state-machine redesign; entry-validation changes beyond the ROTATE-004 reaffirmation in spec text.
- **Rollback or recovery:** Revert the amendment commit; the discovery milestone's pre-amendment state and all historical records are untouched.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| One transition edge plus two small validators | The only contract-conformant way to leave a state the milestone legitimately occupies | 4 new deterministic tests (success, unresolved/missing/mismatched blocker, dirty tree, flag misuse, other-target refusal); 27 pipeline tests OK | Semantic adequacy of "decision satisfies the unblock condition" remains human/reviewer judgment — the machine checks only durable recording signals |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-09-23T01:32:06Z` | `agent:ClaudeCode-discovery-fix-3` | Source inspection of `scripts/run_pipeline.py` (`TRANSITIONS`, `_legal_transition`) against the recorded owner decision | No exit edge from `BLOCKED_HUMAN_AUTHORITY` exists; gap confirmed without mutating state | This issue | Inspection only; no dynamic probe of the transition validator was run |
| `2026-09-23` | `agent:ClaudeCode-discovery-fix-3` | `python3 -m unittest tests.test_run_pipeline -v` | 27 tests OK (exit 0), including the four new blocked-exit tests | This issue | Fixture-based; the real milestone resume is exercised separately by the actual transition |

## Pipeline state (optional)

NOT APPLICABLE.

## Self-review

- **Outcome:** `NOT_APPLICABLE` (this issue's authority gate is the owner decision recorded above; the amendment's own quality gate is the required independent review, still pending).

## Independent review rounds

- **Required:** YES — the owner approved the contract amendment on 2026-09-23; the amendment changes the accepted pipeline contract and must follow the ordinary specification-evolution review path. No round has been recorded.

## Blocker

- **Blocked from:** `RESOLVED` — the owner approved the amendment and it is implemented and tested; the discovery milestone's resume transition is executable.
- **Blocker:** `NONE (owner approval recorded 2026-09-23; amendment implemented)`.
- **Unblock owner:** `human:MattSureham`
- **Unblock condition:** SATISFIED — the owner recorded approval of the proposed amendment with bounded scope, and the amendment is implemented in `run_pipeline.py`, PROJECT_SPEC PIPELINE-003/PIPELINE-009, and ADR-20260814T015817Z decision 5 with deterministic test coverage. Independent review of the amendment remains outstanding and is tracked by this issue's Review field.

## Residual uncertainty

- The owner selected `IN_PROGRESS` as the sole exit target; a future need for `BLOCKED_HUMAN_AUTHORITY → CHANGES_REQUIRED` would require separate owner-approved evolution.
- Independent review of the amendment has not yet occurred; findings could require fixes within this issue's scope.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-23T01:32:06Z` | `agent:ClaudeCode-discovery-fix-3` | `NONE` | `BLOCKED` | Recorded the contract gap discovered while persisting the owner's bounded Codex authorization: no machine exit from `BLOCKED_HUMAN_AUTHORITY` exists, and the 2026-09-22 entry misapplied `ROTATE-004`. Proposed a minimal exit-edge amendment; awaiting owner decision. No state block was hand-edited and no Codex session was launched. |
| `2026-09-23` | `human:MattSureham` (recorded by `agent:ClaudeCode-discovery-fix-3`) | `BLOCKED` | `OPEN` | Owner approved the amendment with explicit bounds (exit only to `IN_PROGRESS`; recorded-decision gates; no side-effect authorization; ROTATE-004 reaffirmed; no new states). Implemented the amendment in `run_pipeline.py`, PROJECT_SPEC (PIPELINE-003 reference + new PIPELINE-009 + change record), and ADR-20260814T015817Z decision 5, with four new deterministic tests (27 pipeline tests OK). Independent review of the amendment remains outstanding. No Codex session launched. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source (owner-approved PIPELINE-009 and amended ADR decision 5).
- [x] The change or resolution is recorded (this issue, spec change record, ADR status history).
- [x] Required verification ran and evidence is linked (27 pipeline tests OK; full suite and validator run at reconciliation).
- [x] If `Review: SELF`, the Self-review outcome is recorded — NOT APPLICABLE here (`Review: INDEPENDENT`).
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved — PENDING; no round yet.
- [x] Required human authority is recorded in the owning artifact (owner approval recorded above).
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action — updated at reconciliation with the milestone resume.
