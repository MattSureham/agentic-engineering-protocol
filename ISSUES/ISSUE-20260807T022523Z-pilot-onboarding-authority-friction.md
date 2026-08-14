# Issue — Pilot Onboarding Authority Friction

## Metadata

- **ID:** `ISSUE-20260807T022523Z-pilot-onboarding-authority-friction`
- **Title:** External task pressure versus terminal owner-wait state in fresh-participant onboarding
- **Status:** `IMPLEMENTING`
- **Severity:** `LOW`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-07T02:25:23Z`
- **Updated UTC:** `2026-08-14T02:24:27Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) specification-evolution policy and Authorized milestone pipeline phase; reusable protocol freshness/onboarding requirements
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** Inline verification record below; [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md)

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

The preceding options are preserved as the original investigation. On `2026-08-14T01:58:17Z`, the owner selected a bounded form of option 2 plus aligned root wording: accepted specification milestones are prior authorization within their exact bounds, while external prompts, implementation momentum, participant preference, and inferred useful work are not. The terminal no-authorized-work state remains valid. No broader onboarding redesign is selected.

## Change

- **Files or components:** Root and reusable `BOOTSTRAP.md`, reusable prompts/README guidance, this issue, `HANDOFF.md`, and `HUMAN_CHECKPOINT.md`.
- **Behavior changed:** Fresh participants are now told explicitly to distinguish prior authorization in an accepted milestone from external or inferred task pressure and to preserve a valid terminal no-work state.
- **Out-of-scope work deliberately excluded:** Broader onboarding redesign; any implementation against the four still-`BLOCKED` capability deferrals; runtime inside the reusable package.
- **Rollback or recovery:** Revert the shared immutable pipeline wording target while preserving this owner decision and the original pilot observation.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| `NONE` | Record-only finding; no abstraction, dependency, state, process, or coupling introduced | This file plus HANDOFF/checkpoint index entries | NONE |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-07T02:25:23Z` | `ClaudeCode/pilot-1` | Procedures listed under Evidence or reproduction | All passed, exit `0`; snapshot claims CONFIRMED; no staleness trigger fired | Inline table above | Dedicated Markdown linters not run; single-participant observation |
| `2026-08-14T02:24:27Z` | `Codex/root` | Inspect root/reusable BOOTSTRAP, reusable onboarding/resumption prompts, accepted milestone authority, and candidate structural/full unit checks | Explicit authority distinction is present in both normative documents and prompts; 39 repository tests pass | Shared pipeline candidate worktree; immutable evidence pending | Implementor inspection cannot satisfy independent review |

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

The historical self-review above covered creation of the finding only. Implementor `Codex/root` inspected the bounded wording at `2026-08-14T02:24:27Z`; no broader onboarding behavior was added, and this preparatory check does not satisfy the now-required independent review.

## Independent review rounds

- **Required:** `NO` — record-only finding with no change to external behavior, contracts, dependencies, persistent state, security/trust, concurrency, background processes, cross-module coupling, or governance architecture. If the owner approves option 2 or 3 under Investigation and decision, the resulting wording change is a separate meaningful change with its own review gate.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE` — the bounded owner decision is recorded; verification and independent review remain
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Owner direction

`2026-08-07T02:31:47Z` — Human technical owner (`MattSureham`) directed: retain this finding `OPEN`; do not close it; do not modify the reusable `protocol/` package or root BOOTSTRAP at this time. This selects none of the three recorded options now; it preserves the finding as accepted open record-keeping with no authorized implementation. The decision queue in `HUMAN_CHECKPOINT.md` was updated accordingly.

### 2026-08-14T01:58:17Z — Superseding bounded direction

Human technical owner `MattSureham` explicitly authorized codification of the milestone authority model and approved the decision-complete implementation plan. The accepted rule now states that implementation momentum, participant preference, an external task prompt, or an inferred useful next step does not create scope authority, while an explicit milestone in an accepted specification is prior authorization within its bounds.

This supersedes the earlier "do not modify at this time" direction only for that exact clarification in root and reusable BOOTSTRAP wording. It does not authorize broader onboarding changes or immediate closure. Because the wording changes governance semantics, this issue now requires independent review of the shared immutable pipeline target before closure.

## Residual uncertainty

- Exact wording compatibility and independent disposition remain pending. The authority distinction itself is no longer uncertain.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-07T02:25:23Z` | `ClaudeCode/pilot-1` | `NONE` | `OPEN` | Created from the first fresh-participant pilot session after verifying all snapshot staleness triggers; records the external-pressure/terminal-state tension and a positive finding on the self-referential closure-verification procedure |
| `2026-08-07T02:31:47Z` | `ClaudeCode/pilot-1` | `OPEN` | `OPEN` | Recorded owner direction: keep the finding open, do not close, do not modify protocol source at that time; approved push of the pilot-resumption record `276e55491da800a4b37d52ae76842a4ec4c0a647` was completed and remote-verified |
| `2026-08-14T01:58:17Z` | Human technical owner `MattSureham`, recorded by `Codex/root` | `OPEN` | `INVESTIGATING` | Current owner decision supersedes the prior hold only for the exact accepted-milestone versus inferred-scope clarification; wording implementation and independent review are now authorized |
| `2026-08-14T02:06:16Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Began the exact root/reusable authority clarification from committed boundary `a6f2699`; broader onboarding changes remain excluded |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the historical record-only Self-review outcome is `COMPLETE`; it does not satisfy the newly required independent review of governance wording.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted pipeline phase and compatible ADR.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
