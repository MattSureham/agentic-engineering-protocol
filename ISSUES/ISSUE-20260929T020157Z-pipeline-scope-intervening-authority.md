# Issue — Pipeline scope gate misattributes separately authorized intervening work to the running attempt

## Metadata

- **ID:** `ISSUE-20260929T020157Z-pipeline-scope-intervening-authority`
- **Title:** Scope validation compares raw attempt-base→target diffs and cannot distinguish durably authorized, independently accepted intervening changes from the current attempt's own changes
- **Status:** `OPEN`
- **Severity:** `HIGH`
- **Owner:** `human:MattSureham`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-09-29T02:01:57Z`
- **Updated UTC:** `2026-09-29T02:44:00Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `PIPELINE-002`, `PIPELINE-007`
- **ADRs:** [ADR-20260814T015817Z](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md) decision 7
- **Evidence:** [attempt-3 submission boundary](../EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md); [blocked-exit review round 1](../EVIDENCE/EVIDENCE-20260924T011904Z-blocked-exit-review-round-1.md)
- **Milestone:** `milestone-20260918t064510z-prompt-independent-discovery-v1` (affected running milestone; this amendment itself is pipeline-contract evolution)

## Problem

The discovery milestone's attempt 3 completed its evidence base (run 10 evaluated PASS on 2026-09-29; acceptance criteria 1–5 established), but the contract-conformant `IN_PROGRESS → AWAITING_PEER_REVIEW` transition with target `9f72d3de57085525a8ddf8a3b14bf1a3161e26e8` was refused deterministically (`AEP-PIPE-SCOPE`, no state advance). The scope gate diffs the raw attempt base→target range against the milestone's static `allowed_paths`, so unrelated changes that legally entered the authoritative branch during the attempt under separate durable authority are misattributed to the running attempt.

## Evidence or reproduction

Observed case (verified from Git): while attempt 3 was `BLOCKED_HUMAN_AUTHORITY`, the owner-approved blocked-exit amendment landed (`47a0cb4`, review persistence `79063cb`) with independent human authority, its own issue ([ISSUE-20260923T013206Z](ISSUE-20260923T013206Z-pipeline-blocked-exit.md)), and an independent APPROVED review (0 open material findings, reviewed immutable state `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3`). Its paths (`PROJECT_SPEC.md`, `ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md`, `scripts/run_pipeline.py`, `tests/test_run_pipeline.py`, its own issue) plus the human-authority record issue [ISSUE-20260922T073608Z](ISSUE-20260922T073608Z-codex-quota-authorization.md) (`Review: SELF`, owner decisions durably recorded) are outside the discovery milestone's accepted `allowed_paths`. Since the submission target must equal HEAD, no in-scope target can exclude them, so the running milestone became unsubmittable without falsifying its scope. Widening the discovery `allowed_paths` was explicitly prohibited by the owner as a false widening of discovery authority.

## Expected behavior

Milestone scope validation MUST distinguish changes attributable to the current attempt from unrelated intervening changes that entered the authoritative branch under separate durable authority. An intervening change may be excluded from the current milestone's scope accounting only when its provenance, authority, target/revision range, and required independent acceptance are durably identifiable and verifiable, and the mechanism MUST fail closed on ambiguous provenance, unresolved or unreviewed intervening work, overlapping attribution that cannot be distinguished, unrecorded commits, and owner-only ad-hoc path exceptions. Independently authorized intervening changes MUST NOT implicitly widen the milestone's `allowed_paths`; the attempt base and history remain preserved (no base rewriting); immutable history remains append-only; `target == HEAD` semantics stay unchanged; the mechanism MUST NOT let an attempt smuggle unauthorized changes by labeling them intervening work; and the solution MUST be general, not keyed to specific paths or issues.

## Assumptions

- **CONFIRMED:** The owner authorized this specification evolution on 2026-09-29 with the invariants above, prohibiting discovery `allowed_paths`/digest widening, acceptance-criteria or oracle changes, live-agent sessions, and any revert/rewrite of the approved blocked-exit amendment.
- **CONFIRMED:** The discovery milestone's digest `c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f` is computed over the milestone contract mapping; prose-level requirement additions outside the contract block do not change it.
- **INFERRED:** Review-persistence commits (a reviewer's own round records) legitimately postdate the reviewed target within an intervening range and touch only record-keeping paths.

## Investigation and decision

### Owner decision recorded 2026-09-29T02:01:57Z

Human technical owner `MattSureham` confirmed the run-10 discovery conformance result as valid, classified the `AEP-PIPE-SCOPE` refusal as a new protocol contract gap (not a discovery scope failure), and authorized this amendment with the ten recorded invariants: distinguish attempt-attributable from separately authorized intervening changes; no implicit `allowed_paths` widening; preserved attempt base/history; exclusion only with durably verifiable provenance, authority, revision range, and required acceptance; fail-closed on ambiguity/unreviewed work/overlap/unrecorded commits/ad-hoc path exceptions; no smuggling via mislabeled intervening work; append-only history; unchanged `target == HEAD`; general mechanism; no rerun of run 10 or existing evidence.

**Design (minimal):** the milestone's owning issue gains an optional machine-readable `aep-intervening-authority/v1` registry block whose entries name a separately authorized owning issue and an exclusive→inclusive commit range. The pipeline verifies each entry fail-closed: the linked issue carries `Authority: HUMAN`; its required acceptance is verifiably satisfied per its own `Review` field (`INDEPENDENT`: latest review round `APPROVED` with zero open material findings, reviewed target an ancestor-or-equal of the range tip, any post-review commits within the range restricted to record-keeping paths, and reviewer label differing from the current milestone's implementor; `SELF`: recorded owner decision with the blocker-resolution gate, and only the issue's own file is excludable); ranges are ancestor-consistent with the submission target. A path outside `allowed_paths` is excluded from scope accounting only when every commit touching it in the attempt window belongs to a verified range under which that path is excludable; all exclusions are recorded in the verification evidence for the milestone's independent reviewer. Everything else about scope checking is unchanged.

## Change

- **Files or components:** `PROJECT_SPEC.md` (new PIPELINE-010 plus change-record row; milestone contract block untouched), `ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md` (PIPELINE-010 mirror plus status-history row), `scripts/run_pipeline.py` (registry parsing, entry verification, exclusion accounting, evidence field), `tests/test_run_pipeline.py` (positive and adversarial deterministic tests), this issue, the discovery issue's registry block (entries for the blocked-exit amendment and the quota-authorization record), HANDOFF/HUMAN_CHECKPOINT reconciliation.
- **Behavior changed:** `IN_PROGRESS → AWAITING_PEER_REVIEW` scope validation distinguishes verified separately authorized intervening ranges; refusal behavior for unaccounted out-of-scope changes is unchanged.
- **Out-of-scope work deliberately excluded:** Discovery `allowed_paths`/digest changes; discovery acceptance criteria or frozen-oracle changes; any live-agent session; history rewrite; target-semantics changes; authenticated identity.
- **Rollback or recovery:** Recover from Git; a material rollback needs owner authority. The discovery milestone state machine is untouched (still `IN_PROGRESS` attempt 3) until this amendment is accepted and the submission is retried.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Registry parsing, entry verification, per-path commit-coverage accounting | Fail-closed distinction of separately authorized intervening work without contract widening | Deterministic positive/adversarial tests plus a read-only evaluation of the real discovery case | This issue |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-09-29T02:01:57Z` | `agent:ClaudeCode-discovery-fix-3` | Git archaeology of `88fa8359…`→`9f72d3d`: per-path commit attribution for all six refused paths; pipeline refusal reproduction `python3 scripts/run_pipeline.py transition --milestone MILESTONE-20260918T064510Z-prompt-independent-discovery-v1 --actor agent:ClaudeCode-discovery-fix-3 --to AWAITING_PEER_REVIEW --target 9f72d3de…` | `AEP-PIPE-SCOPE` refusal reproduced, exit `1`, no state advance (status remained `IN_PROGRESS` attempt 3); four amendment paths touched only by `47a0cb4`; blocked-exit issue touched only by `610c672`/`47a0cb4`/`79063cb`; quota-authorization issue touched by attempt-era record-keeping commits | This record and the attempt-3 evidence | Deterministic attribution only; no live sessions |
| `2026-09-29T02:44:00Z` | `agent:ClaudeCode-discovery-fix-3` | Implemented the registry mechanism (`_parse_intervening_registry`, `_verify_intervening_entry`, per-path commit-coverage accounting in `_verify_target_scope`, `scope_exclusions` evidence field); `python3 -m unittest discover -s tests`; `python3 scripts/validate_protocol.py`; `PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/discovery-review-round-2/reviewer_probes.py .`; read-only real-case evaluation of the discovery registry against target `9f72d3de…` via the pipeline's own verification functions | 178 tests OK (exit `0`) including 6 new registry tests (positive INDEPENDENT and SELF exclusion with evidence records; SELF substantive-path smuggling refused; 4 authority/decision refusals; 13 fail-closed range/review/overlap mutations; 7 malformed-registry mutations); validator PASS (exit `0`); 19/19 reviewer probes non-PASS (11 FAIL, 8 UNVERIFIED); real case: both entries verify, all six previously refused paths covered (four amendment paths + blocked-exit issue via Entry A INDEPENDENT, quota issue via Entry B SELF), zero uncovered; with Entry A removed the same evaluation leaves the five amendment paths uncovered (fail-closed); a hypothetical attempt-attributable `AGENTS.md` change is uncoverable (no smuggling); discovery digests unchanged (`status` PASS) | This record; suite output; read-only evaluation output (no state written, no transition invoked) | Evaluation is deterministic attribution over recorded signals, not authenticated authorship; the eventual discovery reviewer judges the exclusion records |

## Pipeline state (optional)

None — this amendment is owner-approved contract evolution tracked at issue level, following the blocked-exit amendment precedent ([ISSUE-20260923T013206Z](ISSUE-20260923T013206Z-pipeline-blocked-exit.md)); it does not create a new authorized milestone.

## Self-review

- **Outcome:** `NOT_APPLICABLE` — `Review: INDEPENDENT` applies.

## Independent review rounds

- **Required:** YES — the amendment changes accepted pipeline verification semantics (scope accounting) and must follow the ordinary specification-evolution review path, as with the blocked-exit amendment.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE (owner approval recorded 2026-09-29T02:01:57Z)`
- **Unblock owner:** `human:MattSureham`
- **Unblock condition:** SATISFIED — the owner authorized this amendment with recorded invariants; implementation proceeds within those bounds.

## Residual uncertainty

- The trust model remains recorded-signals: machine gates verify durable attribution and review records, not cryptographic authorship (consistent with the accepted pipeline's disclosed limitation).
- Whether the discovery milestone's eventual reviewer accepts the exclusion records is a review judgment; the mechanism only makes them transparent and verifiable.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-29T02:01:57Z` | `agent:ClaudeCode-discovery-fix-3` | `NONE` | `OPEN` | Recorded the owner-confirmed contract gap (run-10 PASS milestone unsubmittable because the scope gate misattributes the separately approved blocked-exit amendment and human-authority record issue to the running attempt), the owner decision with its ten invariants, and the minimal registry design; no implementation yet |
| `2026-09-29T02:44:00Z` | `agent:ClaudeCode-discovery-fix-3` | `OPEN` | `OPEN` | Implemented the owner-approved design: PIPELINE-010 in `PROJECT_SPEC.md` (contract block untouched, digests unchanged) with change-record row; ADR-20260814T015817Z decision 7 amended plus status-history row; registry parsing/verification/exclusion accounting in `scripts/run_pipeline.py` with `scope_exclusions` recorded in submission evidence; 6 new deterministic test groups (13 fail-closed + 7 malformed mutations); `aep-intervening-authority/v1` entries A (blocked-exit, INDEPENDENT) and B (quota record, SELF) registered in the discovery issue; read-only real-case evaluation proves the blocked-exit amendment is correctly identified as separately authorized intervening work while discovery-attributable paths remain under the original `allowed_paths`. Full suite 178 OK, validator PASS, 19/19 reviewer probes non-PASS. No live sessions, no state transition, no self-review; stopped at the independent-review boundary. |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is recorded (`NOT_APPLICABLE`) and no independent-review risk category applies to this record-keeping issue.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: the owner decision is recorded in "Investigation and decision" (2026-09-29T02:01:57Z).
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (NONE added beyond this issue).
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
