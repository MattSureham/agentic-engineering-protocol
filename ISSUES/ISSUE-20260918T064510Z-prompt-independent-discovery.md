# Prompt-Independent Protocol Discovery and Activation

## Metadata

- **ID:** `ISSUE-20260918T064510Z-prompt-independent-discovery`
- **Title:** Make supported fresh participants discover and activate adopted protocol without task-level reminders
- **Status:** `IMPLEMENTING`
- **Severity:** `HIGH`
- **Owner:** `agent:Codex-discovery-authority`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-09-18T06:45:10Z`
- **Updated UTC:** `2026-09-20T07:43:11Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `DISCOVERY-001`–`DISCOVERY-006`, discovery acceptance and order-5 contract
- **ADRs:** Accepted [four-layer discovery boundary](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md)
- **Evidence:** [Authority/gap analysis](../EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md); [authority validation](../EVIDENCE/EVIDENCE-20260918T065750Z-discovery-authority-validation.md)
- **Milestone:** `MILESTONE-20260918T064510Z-prompt-independent-discovery-v1`

## Problem

Human technical owner `MattSureham` reports a real adopted project where a fresh coding agent can start ordinary implementation unless the task prompt repeats protocol/onboarding instructions. This is a product-level entry-path gap, not assumed to be an isolated agent mistake. The affected project's identity, revision, harness configuration, and trace have not been supplied; the exact incident has not been independently reproduced.

## Evidence or reproduction

- **CONFIRMED:** The owner's report and approved plan request prompt-independent activation, vendor-neutral authority, initial Codex CLI plus Claude Code conformance, and discovery priority over the unstarted autonomy demonstration.
- **CONFIRMED:** At baseline `58fa281`, Fresh-agent onboarding and Plug-and-play in the specification require a supplied onboarding prompt; reusable README quick-start step 6 does likewise. `scripts/run_rotation.py:build_prompt` injects BOOTSTRAP/recovery/role instructions. These entry paths do not demonstrate prompt-independent discovery.
- **CONFIRMED:** The closed [onboarding-authority issue](ISSUE-20260807T022523Z-pilot-onboarding-authority-friction.md) addressed scope pressure after entry, explicitly excluding broader onboarding redesign. It is not reopened or broadened.
- **UNKNOWN:** Exact incident reproduction and actual fresh-session conformance of either first-slice harness.

## Expected behavior

An adopted repository MUST be discovered and its authority/durable state recovered by a supported fresh participant receiving only an ordinary work request, before task implementation. Discovery grants no scope, role eligibility, review approval, or exemption from evidence/handoff duties. Durable repository authority survives adapter removal.

## Assumptions

- **CONFIRMED:** The owner approved the decision-complete requirement/authority-recording plan before this record; no adapter implementation is part of this participant's task.
- **INFERRED:** Native project instruction loading can provide a small host-specific bridge; official capability descriptions alone cannot establish behavioral conformance.
- **CONFIRMED (2026-09-20):** Concrete first-slice profiles and their demonstrated reliability are now recorded in the [live conformance evidence](../EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md): Claude Code `2.1.118` root and subdirectory start; Codex CLI `0.153.4` root start only.

## Investigation and decision

### Owner decision recorded 2026-09-18T06:45:10Z

Human technical owner `MattSureham` authorized this product requirement through specification evolution and approved the four-layer boundary: repository-native authority, adoption/discovery signal, subordinate host adapter, and unsupported-host manual fallback. The owner selected **Codex CLI plus Claude Code** as the first conformance scope and **discovery first** ahead of the still-unstarted demonstration. This recording timestamp is not an invented timestamp for the original incident.

The approved phase persists specification, compatible accepted ADR, a bounded implementation milestone, evidence, and continuity records, then stops. It does not select a vendor mechanism as normative protocol authority, implement shims, launch sessions, or close this issue. Required independent review of the later immutable target must include the accepted requirements and this phase's architecture/compatibility consequences.

## Change

- **Files or components:** Root specification, new ADR and evidence, this issue, demonstration authority-rebinding record, HANDOFF, HUMAN_CHECKPOINT, and necessary root README navigation.
- **Behavior changed:** Requirement and implementation authorization only; runtime/product implementation remains unchanged in this authority phase.
- **Out-of-scope work deliberately excluded:** Adapters/shims/package changes now; pipeline/dispatcher/rotation changes; other harness implementations; new infrastructure; the four blocked capability deferrals.
- **Rollback or recovery:** Recover from Git plus linked authority records. A material requirement rollback needs owner authority; never silently restore an obsolete digest or erase history.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Adoption signal, host support profiles, and thin discovery adapters | Remove recurring operator onboarding burden without duplicating authority | Approved DISCOVERY requirements and future cold-session/negative-case acceptance | This issue; no conformance is claimed yet |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-09-18T06:45:10Z` | `agent:Codex-discovery-authority` | Git recovery, complete root BOOTSTRAP read, source/spec/ADR/issue inspection; `git ls-remote origin refs/heads/main` | Clean main at `58fa281`; direct remote equals local/cached baseline; exit `0` | Baseline Git and this record | No live activation test; authority recording not yet complete |
| `2026-09-19T21:37:43Z` | `agent:Codex-discovery-finalize` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; execute the persisted authority audit | 97 tests in 23.916s, `OK`, exit `0`; audit `PASS`, exit `0` | Linked authority validation, including exact reproduction procedure | Deterministic authority checks only; Darwin arm64/Python 3.9.6; dedicated Markdown linter unavailable; real activation NOT RUN |
| `2026-09-19T21:37:43Z` | `agent:Codex-discovery-finalize` | Fetch/direct-remote recovery and protected-byte/history audit against `58fa281` | Local/cached/direct baseline equal; exactly nine record paths; all other baseline bytes unchanged; original activity retained | Linked authority validation and containing commit diff | Publication equality must be verified from Git; no implementation transition, review or acceptance |
| `2026-09-20T08:44:32Z` | `agent:ClaudeCode-discovery` | `python3 -m unittest discover -s tests -v`; `python3 scripts/validate_protocol.py`; `git diff --check` | 124 tests `OK`, exit `0`; validator `PASS`; clean diff | This record and the immutable target commit | Darwin arm64/Python 3.9.6; deterministic checks only |
| `2026-09-20T08:44:32Z` | `agent:ClaudeCode-discovery` | Live conformance program: 57 bounded headless sessions (2 capability, 25 initial, 2 validation, 28 final) launched via `tests/probe_discovery.py` against isolated fixture copies, exact task prompt `实现下一个已经授权的任务。` | Final matrix (identical final fixture bytes): Claude Code 12 PASS + manual-fallback PASS + 1 OBSERVE, root and subdirectory start; Codex CLI 12 PASS + manual-fallback PASS + 1 OBSERVE at root, subdirectory start 2/3 and not claimed; all negative cases behaved | [Live conformance evidence](../EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md) with per-run JSON records, manifests and event chronologies | Single host/model per harness; Codex model and cost not exposed; loader internals inferred from tool chronology |

## Pipeline state

Operational projection of the accepted contract; this block does not authorize scope. Attempt 1 implementation and live conformance are complete at the frozen target; independent review and acceptance have not occurred. New digest: `c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f`.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1",
  "authority_digest": "c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f",
  "state": "IN_PROGRESS",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-discovery",
  "base_revision": "d140634673439a0853dc6a931e5de1fa835a4f19",
  "target_revision": null,
  "verification_evidence": [],
  "review_references": [],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-09-18T06:45:10Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Owner approved prompt-independent discovery requirements, four-layer architecture, Codex CLI plus Claude Code first slice, and discovery-first order through specification evolution."
    },
    {
      "sequence": 2,
      "utc": "2026-09-20T07:43:11Z",
      "actor": "agent:ClaudeCode-discovery",
      "from": "AUTHORIZED",
      "to": "READY",
      "reason": "Validated transition AUTHORIZED to READY."
    },
    {
      "sequence": 3,
      "utc": "2026-09-20T07:43:11Z",
      "actor": "agent:ClaudeCode-discovery",
      "from": "READY",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 1 began from immutable base d140634673439a0853dc6a931e5de1fa835a4f19."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Self-review

- **Participant:** `agent:Codex-discovery-authority`
- **Reviewed UTC:** `2026-09-18T06:45:10Z`
- **Reviewed repository state:** Baseline `58fa281` plus the authority-recording worktree
- **Scope and authority references:** Owner-approved requirement/authority plan only
- **Checks and evidence reviewed:** Verification table; complete validation pending
- **Findings and corrections:** New requirement is distinct from the closed onboarding-authority clarification
- **Limitations:** No implementation, fresh-session behavioral test, or independent review
- **Residual risks:** Support profiles and activation reliability remain unverified
- **Outcome:** `NOT_APPLICABLE`

### Resumed authority-record verification — 2026-09-19T21:37:43Z

`agent:Codex-discovery-finalize` reproduced the full suite and persisted audit, checked the accepted owner scope, six parseable contracts, preserved historical records and the exact nine-path authority-only diff. All performed checks pass as linked above. This is attributable record verification, not independent peer review or approval of an implementation target. The earlier pending-validation observation remains historical; implementation/conformance uncertainty remains open, and the machine block is unchanged at AUTHORIZED attempt 0.

## Independent review rounds

- **Required:** `YES` — public adoption contract, governance boundary, and host integration; review the future immutable implementation target plus its accepted authority and durable evidence.

No round is recorded. Owner acceptance of requirements is not peer approval of implementation.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE` — accepted requirement and compatible ADR authorize the next implementation participant; this owner/specification participant stops at AUTHORIZED after record verification
- **Unblock owner:** `NOT APPLICABLE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- First-slice activation evidence now exists (see Verification): Claude Code `2.1.118` root and subdirectory start, Codex CLI `0.153.4` root start, on the probed host configuration. Codex subdirectory start passed only 2 of 3 final runs (and 1 of 2 initial runs) and is not claimed. Unsupported hosts, other models/versions, and this host after upgrades remain manual-only or unverified, not implicitly supported.
- No production-grade reliability, authenticated identity, concurrent-writer safety, or autonomous-demonstration completion is claimed.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-18T06:45:10Z` | `agent:Codex-discovery-authority` | `NONE` | `OPEN` | Recorded owner-reported failure and repository-verified requirement gap without claiming incident reproduction |
| `2026-09-18T06:45:10Z` | `human:MattSureham`, recorded by `agent:Codex-discovery-authority` | `OPEN` | `INVESTIGATING` | Owner approved requirement evolution, four-layer boundary, two-harness first slice, discovery-first ordering, and authority-only stop boundary |
| `2026-09-18T06:45:10Z` | `agent:Codex-discovery-authority` | `INVESTIGATING` | `INVESTIGATING` | Persisted DISCOVERY-001–006, compatible accepted ADR, order-5 contract and initial AUTHORIZED projection; deterministic authority validation follows before handoff; no implementation or runtime transition |
| `2026-09-19T21:37:43Z` | `agent:Codex-discovery-finalize` | `INVESTIGATING` | `INVESTIGATING` | Resumed interrupted final verification: 97 tests and persisted authority audit pass; linked evidence/HANDOFF/checkpoint reconciled for publication; no machine event added, implementation attempted, review recorded or issue closed |
| `2026-09-20T07:43:11Z` | `agent:ClaudeCode-discovery` | `INVESTIGATING` | `INVESTIGATING` | Pipeline AUTHORIZED -> READY. Validated transition AUTHORIZED to READY. |
| `2026-09-20T07:43:11Z` | `agent:ClaudeCode-discovery` | `INVESTIGATING` | `IMPLEMENTING` | Pipeline READY -> IN_PROGRESS. Implementation attempt 1 began from immutable base d140634673439a0853dc6a931e5de1fa835a4f19. |
| `2026-09-20T08:44:32Z` | `agent:ClaudeCode-discovery` | `IMPLEMENTING` | `IMPLEMENTING` | Implemented the authorized slice within contract allowed paths: root `AGENTS.md`/`CLAUDE.md` adoption-declaration bridges with an explicit governed-scope rule; package onboarding/adoption documentation evolution (one-time bridge installation, onboarding prompt demoted to manual fallback); `tests/test_discovery.py` deterministic coverage, `tests/probe_discovery.py` bounded live harness and `tests/fixtures/discovery/`; 57-session live conformance program with per-run durable records under `EVIDENCE/discovery-conformance/`. One nested-scope misidentification finding was repaired via the bridge scope sentence and re-verified before the final matrix. |

## Closure checklist

- [ ] Expected behavior is tied to durable accepted requirements and architecture.
- [ ] The implementation is recorded at an immutable target within accepted scope.
- [ ] Required deterministic and real fresh-session verification ran; evidence is durable.
- [ ] Fresh independent review is `APPROVED` with zero open material findings.
- [ ] Recorder verifies closure and the pipeline records acceptance.
- [ ] Complexity and residual uncertainty are covered or explicitly owned.
- [ ] HANDOFF reflects the resulting state and one next action.
