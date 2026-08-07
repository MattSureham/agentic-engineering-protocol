# Issue — Pilot Onboarding Authority Friction

## Metadata

- **ID:** `ISSUE-20260807T022523Z-pilot-onboarding-authority-friction`
- **Title:** External task pressure versus terminal owner-wait state in fresh-participant onboarding
- **Status:** `OPEN`
- **Severity:** `LOW`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-08-07T02:25:23Z`
- **Updated UTC:** `2026-08-07T02:25:23Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) post-pilot hardening requirements and specification-evolution policy; reusable protocol freshness/onboarding requirements
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md) (governance context only)
- **Evidence:** Inline verification record below; no separate evidence file

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The first real-world pilot application of this repository's protocol began from an external instruction directing a fresh participant to "complete a meaningful engineering task," while the repository's authoritative state (accepted specification plus `HANDOFF.md` Next Action) was terminal: the hardening issue is `CLOSED` with independent `APPROVED`, and all five remaining issues are `BLOCKED` on new owner-approved specifications. No implementation work was authorized.

The protocol resolved the tension correctly: the root BOOTSTRAP treats HANDOFF's Next Action as a continuity pointer rather than higher authority, limits unauthorized work to investigation, evidence, or explicitly reversible proposals, and routes everything else to the Human Authority Boundary. However, a participant under delivery pressure from an external prompt could rationalize manufacturing unauthorized work. Neither the root nor the reusable BOOTSTRAP explicitly states that external prompts or task instructions do not grant authority, or names the terminal owner-wait state as a valid, expected repository condition that must be preserved rather than "fixed" by inventing work.

## Evidence or reproduction

Fresh-participant session `2026-08-07T02:25:23Z`, participant `ClaudeCode/pilot-1`, starting from repository state only with no prior conversation:

| Procedure | Result | Exit |
|---|---|---|
| `git rev-parse HEAD` / `HEAD^` | `774b2e0237c6814cc7b4b491f495ba7965e8e0e4` / `bee42f788c77c51fea62e7e74f4fbdd7f5b3084f` (declared closure commit is a direct child of the published review handoff) | `0` |
| `git status --short --branch` | clean; `main...origin/main` | `0` |
| `git diff --name-only bee42f7..HEAD` | exactly `HANDOFF.md`, `HUMAN_CHECKPOINT.md`, `ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md` (matches the declared three-file closure set) | `0` |
| `git ls-remote origin refs/heads/main` | `774b2e0237c6814cc7b4b491f495ba7965e8e0e4` (local/remote equality; the push left unverified by the closing participant is now CONFIRMED) | `0` |
| `find protocol -type f` / symlink count | exactly ten regular files, zero symlinks (package inventory claim CONFIRMED) | `0` |
| Issue status scan of `ISSUES/` | five `BLOCKED` deferrals, six `CLOSED` including the hardening issue (matches HANDOFF Active Issues) | `0` |
| HANDOFF structure check | five ordered top-level sections, 283 lines, exactly one Next Action item | `0` |

All staleness triggers in the `2026-08-06T03:02:04Z` snapshot were checked; none fired. The snapshot's self-referential closure-commit verification procedure executed exactly as written — a positive finding for the protocol design.

## Expected behavior

Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) specification-evolution policy: a requirement or product-wording change evolves through evidence-backed proposal and explicit human technical-owner approval; implementation drift is not authorization. This issue is the evidence-backed proposal record. Any resulting change to reusable `protocol/BOOTSTRAP.md` wording requires owner approval and must preserve the ten-file package inventory (`HARDEN-006`).

## Assumptions

- **CONFIRMED:** No implementation work was authorized at session start; all snapshot claims verified above directly.
- **CONFIRMED:** The external pilot instruction is not a repository authority source; only the accepted specification, accepted ADRs, and recorded owner approvals are.
- **INFERRED:** The tension between delivery pressure and a terminal wait state is a generalizable onboarding hazard, not specific to this session. Supporting facts: the reusable BOOTSTRAP's work-selection rules address authorization but do not name the terminal-state case; the root resolution required combining three separate rules (continuity pointer, investigation-only fallback, authority boundary).
- **UNKNOWN:** Whether the owner judges the current implicit coverage sufficient or wants explicit wording in the reusable BOOTSTRAP, the root BOOTSTRAP, both, or neither. Resolution path: owner decision recorded here or in a specification change.

## Investigation and decision

No implementation is proposed by this issue. Candidate owner options, recorded for decision only:

1. Accept implicit coverage and close this issue with rationale.
2. Approve explicit wording in the reusable `protocol/BOOTSTRAP.md` stating that external prompts do not grant authority and that a terminal owner-wait state is a valid condition to preserve; follow the specification-evolution policy and independent-review gate for the product change.
3. Approve equivalent wording in the root `BOOTSTRAP.md` only, accepting root/product divergence to be reviewed under the separate-governance rule.

## Change

- **Files or components:** This issue file; `HANDOFF.md` and `HUMAN_CHECKPOINT.md` index/queue updates only.
- **Behavior changed:** None. No protocol source, specification, ADR, or evidence body was modified.
- **Out-of-scope work deliberately excluded:** Any BOOTSTRAP wording change; any implementation against the five `BLOCKED` deferrals.
- **Rollback or recovery:** Delete this issue file and revert the two index files; no external state was touched.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| `NONE` | Record-only finding; no abstraction, dependency, state, process, or coupling introduced | This file plus HANDOFF/checkpoint index entries | NONE |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-07T02:25:23Z` | `ClaudeCode/pilot-1` | Procedures listed under Evidence or reproduction | All passed, exit `0`; snapshot claims CONFIRMED; no staleness trigger fired | Inline table above | Dedicated Markdown linters not run; single-participant observation |

## Self-review

- **Participant:** `ClaudeCode/pilot-1`
- **Reviewed UTC:** `2026-08-07T02:25:23Z`
- **Reviewed repository state:** `774b2e0237c6814cc7b4b491f495ba7965e8e0e4`, clean worktree, plus this session's record-only diff
- **Scope and authority references:** One new issue file and two index updates; root BOOTSTRAP artifact-ownership and HANDOFF-maintenance rules; accepted specification specification-evolution policy
- **Checks and evidence reviewed:** Verification row above
- **Findings and corrections:** NONE
- **Limitations:** Self-review of a record-only finding; no independent review is required because no external behavior, contract, dependency, state, security, concurrency, or governance architecture changes
- **Residual risks:** The owner may judge this finding out of scope; closure then requires only a recorded rationale
- **Outcome:** `COMPLETE`

## Independent review rounds

- **Required:** `NO` — record-only finding with no change to external behavior, contracts, dependencies, persistent state, security/trust, concurrency, background processes, cross-module coupling, or governance architecture. If the owner approves option 2 or 3 under Investigation and decision, the resulting wording change is a separate meaningful change with its own review gate.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE` — closure requires only an owner decision on the three recorded options
- **Unblock owner:** Human technical owner (`MattSureham`)
- **Unblock condition:** Recorded owner decision selecting option 1, 2, or 3 (or rejecting the finding with rationale)

## Residual uncertainty

- Whether implicit protocol coverage of terminal owner-wait states is sufficient; owned by the human technical owner via the decision above.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-07T02:25:23Z` | `ClaudeCode/pilot-1` | `NONE` | `OPEN` | Created from the first fresh-participant pilot session after verifying all snapshot staleness triggers; records the external-pressure/terminal-state tension and a positive finding on the self-referential closure-verification procedure |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
