# Prompt-Independent Protocol Discovery and Activation

## Metadata

- **ID:** `ISSUE-20260918T064510Z-prompt-independent-discovery`
- **Title:** Make supported fresh participants discover and activate adopted protocol without task-level reminders
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `agent:Codex-discovery-authority`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-09-18T06:45:10Z`
- **Updated UTC:** `2026-09-22T07:51:33Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `DISCOVERY-001`–`DISCOVERY-006`, discovery acceptance and order-5 contract
- **ADRs:** Accepted [four-layer discovery boundary](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md)
- **Evidence:** [Authority/gap analysis](../EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md); [authority validation](../EVIDENCE/EVIDENCE-20260918T065750Z-discovery-authority-validation.md); [independent review round 1](../EVIDENCE/EVIDENCE-20260921T013125Z-discovery-review-round-1.md)
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
| `2026-09-21T11:20:00Z` | `agent:ClaudeCode-discovery-fix` | `python3 -m unittest discover -s tests`; `python3 scripts/validate_protocol.py` | 151 tests `OK`, exit `0`; validator `PASS` (package_files=10, handoffs=2), zero findings across 75 tracked Markdown files | This record and the attempt-2 immutable target commit | Darwin arm64/Python 3.9.6; deterministic checks only |
| `2026-09-21T11:20:00Z` | `agent:ClaudeCode-discovery-fix` | Live conformance program attempt 2: 34 bounded headless sessions (3 capability, 28 matrix, 3 characterization reruns) via the hardened `tests/probe_discovery.py` (schema `aep-discovery-probe/v2`) against the rebuilt faithful fixture; uniform frozen-oracle re-evaluation of every retained record | Codex CLI root start 3/3 PASS with all negative cases PASS (root-only claim supported); Codex subdirectory 1/3 (both failures writable-scope denials, not claimed); Claude Code positive_root 3/3 PASS and positive_subdir 3/4 evaluated PASS, but `negative_conflicting_authority` and `negative_nested` FAIL 2/2 each — systematic behavioral failures, Claude profile claim NOT established | [Attempt-2 live conformance evidence](../EVIDENCE/EVIDENCE-20260921T110848Z-discovery-live-conformance-attempt-2.md) with per-run JSON records, manifests, event chronologies, launch-vs-frozen classification table | Single host/model per harness; Codex model/cost not exposed; two mid-matrix oracle corrections disclosed in the evidence |

- **Pipeline verification `2026-09-20T09:35:35Z`:** [`EVIDENCE/EVIDENCE-20260920T093535Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260920T093535Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `074678d080fc6c1d57d2912314ae21296b618612`.

- **Independent review, persisted `2026-09-21T01:31:25Z`:** `agent:Codex-discovery-review-20260921` completed the read-only review before this persistence task. Frozen-target checks passed 124 tests in 25.952s and the structural validator; independent adverse checks established R1–R3 below. [Reviewer evidence](../EVIDENCE/EVIDENCE-20260921T013125Z-discovery-review-round-1.md) preserves commands, outcomes, attribution, limitations and corrections. The earlier implementor support claims are historical observations on a simplified fixture, not independent confirmation of delivered-protocol conformance. No implementation repair or live rerun was performed by the reviewer.

- **Pipeline verification `2026-09-22T01:22:57Z`:** [`EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json`](../EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json) — deterministic structural and accepted-command gates passed for `cc7961187f067cbc7b337b8f80a64505693f7bc6`.

## Pipeline state

Operational projection of the accepted contract; this block does not authorize scope. Attempt 1 remains bound to frozen target `074678d080fc6c1d57d2912314ae21296b618612`. Round 1 was committed at `d8a7f0b7c148342fd8f19ae5c3b0acbc872f9745`; the reviewer then recorded CHANGES_REQUIRED through the pipeline at `2026-09-21T01:38:51Z`, with three open material findings. Attempt 2 began from immutable base `bd3e00f2dc5c261b12653ddb3912eb834c92645c` at `2026-09-21T09:06:56Z`; the implementor recorded R1–R3 resolutions and attempt-2 verification above and submitted a new immutable target for fresh independent review. No acceptance occurred. Digest remains `c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f`.

Round 2 was committed as `7d4b01ac7a44ebb5201aebca6ade0bd19a114678`; at `2026-09-22T02:09:43Z` the reviewer recorded CHANGES_REQUIRED through the pipeline (event 8). Attempt 2, its target/base/implementor and verification evidence remain fixed. Issue IMPLEMENTING is the fix-required mapping; attempt 3 has not started.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1",
  "authority_digest": "c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f",
  "state": "BLOCKED_HUMAN_AUTHORITY",
  "attempt": 3,
  "implementor": "agent:ClaudeCode-discovery-fix-3",
  "base_revision": "88fa8359ec3a62f200096d0d96bd04a88ebd118a",
  "target_revision": null,
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260920T093535Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-1.json",
    "EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json"
  ],
  "review_references": [
    "ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-21t013125z--agentcodex-discovery-review-20260921",
    "ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-22t020117z--agentcodex-discovery-review-20260922"
  ],
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
    },
    {
      "sequence": 4,
      "utc": "2026-09-20T09:35:35Z",
      "actor": "agent:ClaudeCode-discovery",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target 074678d080fc6c1d57d2912314ae21296b618612 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260920T093535Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-1.json."
    },
    {
      "sequence": 5,
      "utc": "2026-09-21T01:38:51Z",
      "actor": "agent:Codex-discovery-review-20260921",
      "from": "AWAITING_PEER_REVIEW",
      "to": "CHANGES_REQUIRED",
      "reason": "Independent review ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-21t013125z--agentcodex-discovery-review-20260921 recorded 3 open material finding(s); within-scope fixes are required."
    },
    {
      "sequence": 6,
      "utc": "2026-09-21T09:06:56Z",
      "actor": "agent:ClaudeCode-discovery-fix",
      "from": "CHANGES_REQUIRED",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 2 began from immutable base bd3e00f2dc5c261b12653ddb3912eb834c92645c."
    },
    {
      "sequence": 7,
      "utc": "2026-09-22T01:22:57Z",
      "actor": "agent:ClaudeCode-discovery-fix",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target cc7961187f067cbc7b337b8f80a64505693f7bc6 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json."
    },
    {
      "sequence": 8,
      "utc": "2026-09-22T02:09:43Z",
      "actor": "agent:Codex-discovery-review-20260922",
      "from": "AWAITING_PEER_REVIEW",
      "to": "CHANGES_REQUIRED",
      "reason": "Independent review ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-22t020117z--agentcodex-discovery-review-20260922 recorded 3 open material finding(s); within-scope fixes are required."
    },
    {
      "sequence": 9,
      "utc": "2026-09-22T02:35:41Z",
      "actor": "agent:ClaudeCode-discovery-fix-3",
      "from": "CHANGES_REQUIRED",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 3 began from immutable base 88fa8359ec3a62f200096d0d96bd04a88ebd118a."
    },
    {
      "sequence": 10,
      "utc": "2026-09-22T07:51:33Z",
      "actor": "agent:ClaudeCode-discovery-fix-3",
      "from": "IN_PROGRESS",
      "to": "BLOCKED_HUMAN_AUTHORITY",
      "reason": "Human authority is required; linked blocker ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md defines the unblock condition."
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

The preceding no-round statement is retained as the initial authority-phase observation. It is superseded by the following attributable round, not by owner acceptance or the implementor's summary.

### 2026-09-21T01:31:25Z — agent:Codex-discovery-review-20260921

- **Reviewed target:** `074678d080fc6c1d57d2912314ae21296b618612`
- **Open material findings:** `3`
- **Reviewed repository state:** Attempt 1, base `d140634673439a0853dc6a931e5de1fa835a4f19`; published recovery HEAD `e6fda49be42cbc523faacb4ed86fd0e80267619d` with only submission evidence and this owning issue after target. Clean local/tracking/direct remote equality was confirmed during recovery. No implementation drift was found.
- **Independence:** Reviewer did not author the target and differs from `agent:ClaudeCode-discovery`. This is the same independent review completed in the preceding read-only session, now persisted after the platform write restriction was removed; no second review or inherited implementor judgment is claimed. Participant labels are not authenticated identities.
- **Scope:** DISCOVERY-001–006 and all discovery acceptance criteria; accepted discovery ADR and retained root adoption/pipeline/dispatch/rotation/autonomy boundaries; role contracts; base-to-target allowed scope; root/package bridges and installation guidance; deterministic tests, probe oracle, fixture, raw conformance evidence, submission evidence, HANDOFF and post-target drift.
- **Procedures and evidence:** Direct specification/ADR/implementation/raw-record inspection, immutable-target extraction, complete deterministic suite (124 tests, OK, exit 0), validator PASS, five adverse oracle inputs, isolated package/full-reference installation reproductions, 28 final manifest/raw-event comparisons, Markdown/scope/protected-byte/Git checks. Exact commands and observed limitations are in [review evidence](../EVIDENCE/EVIDENCE-20260921T013125Z-discovery-review-round-1.md). These completed review checks were not rerun as a new review during persistence.
- **Confirmed strengths:** Accepted repository-native authority and seven-tier precedence remain unchanged; root bridges confer no new scope/role/approval authority; changes stay within allowed paths and the ten-file package remains Markdown-only; no post-target implementation drift; retained pre-fix failures, corrective nested reruns and final matrix are distinct.
- **Material findings and resolution conditions:** R1–R3 in the table below remain OPEN. Passing structural/unit checks does not establish their resolution. Fixes are within the existing milestone boundary; any proposed scope/trust/architecture change still needs owner authority.
- **Non-material findings:** N1 MEDIUM: final Codex subdirectory run 3 failed on a writable-scope denial, not the summary's memory-diversion explanation; append the correction without erasing raw/history. N2 LOW: HANDOFF's IMPLEMENTING row and no-live-session assertion were stale against REVIEW and retained probes; reconcile shared current fields. N3 LOW: two misconfigured runs were discarded; their raw evidence and total-launch accounting cannot be independently recovered. These are excluded from the three-material-finding count.
- **Limitations and residual risks:** No new reviewer live probes; deterministic counterexamples do not assert those adverse actions occurred in every live run. Codex effective model is UNKNOWN; single-host profiles, dedicated Markdown-linter unavailability and discarded-trace limits remain. Codex final subdirectory 2/3 is compatible with the explicitly root-only claim and is not a fourth material finding; overall conformance remains unapproved because of R1–R3. No closure checklist item is completed by this reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** `FIRST ROUND`

| Finding | Severity / materiality | State | Evidence and required resolution |
|---|---|---|---|
| R1 — Live evidence does not verify the delivered full protocol / bridge | HIGH / material | IMPLEMENTOR-RESOLVED `2026-09-21` — pending review | Attempt 2 rebuilt `tests/fixtures/discovery/adopted_repo` as a faithful adopted instance of the delivered ten-file package (verbatim `BOOTSTRAP.md`/`PROMPTS.md`/`EXAMPLE.md`/`README.md`/`HUMAN_CHECKPOINT.md`/templates; filled spec/HANDOFF/issue), and generated the fixture bridges by executing the delivered `protocol/README.md` installation snippet so tested bytes equal shipped bytes. 34 fresh sessions ran against it; recovery obligations are oracle-enforced. See [attempt-2 evidence](../EVIDENCE/EVIDENCE-20260921T110848Z-discovery-live-conformance-attempt-2.md). |
| R2 — Probe classifier/oracle admits reproducible false positives | HIGH / material | IMPLEMENTOR-RESOLVED `2026-09-21` — pending review | Oracle rewritten fail-closed (schema `aep-discovery-probe/v2`): successful-read chronology for `BOOTSTRAP.md`/`PROJECT_SPEC.md`/issue/`HANDOFF.md` before first mutation, shell unwrapping with read whitelist and write-idiom detection, full manifest diff, exact result bytes, post-mutation verification read, handoff/issue update checks, KEEP.txt byte check, UNVERIFIED on gaps. The reviewer's five adverse inputs are regression tests and classify non-PASS; 151 unit tests pass. Every attempt-2 record re-evaluated uniformly with the frozen oracle (SHA-256 `46263f3a…` in the evidence). |
| R3 — Bridge installation is not self-contained and maps scope incorrectly | MEDIUM / material | IMPLEMENTOR-RESOLVED `2026-09-21` — pending review | `protocol/README.md` now embeds the canonical bridge body in a create-or-merge installer whose only input is the adopting repository path; deterministic tests prove package-only installation (cwd inside a copied `protocol/`, no external reference), collision preservation of existing instruction files, canonical-byte equality, and zero `_validate_markdown_file` findings on installed bridges. The development-scope note remains only on this repository's root bridges. |

Non-material findings handled in attempt 2: N1 corrected by an attributable correction appended to the [attempt-1 evidence](../EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md) (original text retained); N2 continuity fields reconciled in HANDOFF during attempt-2 submission; N3 preserved as an explicit limitation in the attempt-2 evidence (no records discarded in attempt 2; attempt-1 discarded runs remain unreconstructible).

### 2026-09-22T02:01:17Z — agent:Codex-discovery-review-20260922

- **Reviewed target:** `cc7961187f067cbc7b337b8f80a64505693f7bc6`
- **Open material findings:** `3`
- **Reviewed repository state:** Attempt 2, base `bd3e00f2dc5c261b12653ddb3912eb834c92645c`; clean recovery HEAD `09a39cf9a314ecf029a0066344f8fef7942bb6f0` on main, two commits ahead of cached/direct origin/main. Post-target changes are limited to submission evidence, this issue and HANDOFF. Authority digest remains `c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f`.
- **Independence:** Fresh instance with no target authorship, no implementation judgment inherited, no previous conversation or memory recall used. Label differs from implementor `agent:ClaudeCode-discovery-fix`; labels are not authenticated identities. Dispatcher independently confirmed the reviewer role and exact target before work.
- **Scope:** DISCOVERY-001–006, all discovery acceptance criteria and both initial harnesses; accepted discovery/root-adoption/pipeline/dispatch/rotation/autonomy authority; complete base-to-target diff; prior round; portable bridge and package installation; fixture fidelity; oracle/regressions; capability, launch/frozen and raw final/characterization evidence; submission evidence; history, operational consistency and accidental artifacts.
- **Procedures and evidence:** Immutable-target extraction; full suite (151 tests, 25.946s, OK, exit 0); validator PASS; 19 reviewer-owned local oracle probes; actual package-only/fresh/existing/collision installer executions; all 34 pre-manifest and raw-record reclassifications; 57 historical raw records and protected authority/machinery byte checks; 55 allowed changed paths; 76 Markdown files, zero checker findings. [Round-2 evidence](../EVIDENCE/EVIDENCE-20260922T020117Z-discovery-review-round-2.md) and its retained scripts/results preserve exact procedures and limitations. No live matrix rerun.
- **Authority adjudication:** PROJECT_SPEC line 418 explicitly forbids silently narrowing the two-harness milestone; acceptance criteria 4–5 and the machine contract require conformance evidence for both. Accepted discovery ADR decision 5 bounds support wording, not milestone scope. A Codex-only profile with Claude unsupported cannot satisfy this milestone. Root-only Codex directory scope is permitted; unclaimed subdirectory behavior is not an acceptance failure for that bounded directory scope.
- **Support assessment:** Codex root 3/3, required negative outcomes and manual fallback are substantiated observations; effective model/configuration provenance remains UNKNOWN and R2 remains open, so "all acceptance criteria satisfied" is not independently established. Claude positive_root 3/3 and positive_subdir three passes out of four launches do not cancel conflicting-authority and nested failures, 2/2 each. Timeout and historical launch failures remain retained; reruns do not replace them.
- **Prior-round resolution:** R1 PARTIALLY RESOLVED (full-package/bridge byte fidelity fixed; required Codex profile provenance remains open); R2 OPEN (material false positives reproduced); R3 CLOSED (self-contained portable installer, mappings, installed links and collision preservation independently verified). The earlier table's IMPLEMENTOR-RESOLVED wording was substituted by the attempt-2 implementor; it is not a new disposition by the round-1 reviewer. Original wording remains in base `bd3e00f` and round-1 evidence. This attribution correction is additive; the received earlier round is not rewritten.
- **Material findings and resolution conditions:** R1, R2 and new R4 below are OPEN, counted once each. R4 concerns failed Claude behavior; R1's remaining component concerns profile provenance, not duplicate counting of R4.
- **Human Authority Boundary:** Existing milestone scope authorizes corrections to product entry/recovery/adoption text, scoped adapters, oracle/tests and evidence that implement the accepted requirements. A text fix does not inherently amend root authority. No owner decision is required merely because these probes failed. Reducing the two-harness scope, waiving required negatives, changing precedence/gates or adding trust/permission/architecture mechanisms would require owner-approved specification evolution and an ADR where applicable; this reviewer adopts none of those changes.
- **Non-material findings:** Attempt-2 summaries incorrectly call some Codex record-maintenance cases "No mutation" and describe subdirectory refusals as observed enforcement denials; raw records support narrower wording. Timeout stdout is absent, not proof of no emitted events. Two capability event lists are truncated relative to the frozen extractor; reclassification must start from raw data. Earlier review-table authorship was overwritten by implementor claims; recover original wording from Git and append future corrections. README/blocker/current snapshot prose had stale statements. See the evidence's attributable corrections; no additional material count is assigned.
- **Limitations and residual risks:** No new reviewer live sessions; oracle counterexamples are local reproductions, not invented host traces. Single-host evidence, unknown Codex model, absent timeout stdout and discarded attempt-1 runs remain explicit. Dedicated Markdown linters unavailable; no full CommonMark/external URL/fragment, cross-host, authenticated identity, production-reliability or autonomy claim. Closure checklist is untouched.
- **Disposition:** `CHANGES_REQUIRED`

| Finding | Severity / materiality | State | Independent evidence and required resolution |
|---|---|---|---|
| R1 — Profile provenance component of delivered-protocol proof remains incomplete | HIGH / material | OPEN; fidelity component resolved | Every Codex attempt-2 record leaves effective model unknown; no model/configuration record binds the sessions. DISCOVERY-003, criterion 5 and round-1 resolution require it. Preserve observed root success but identify the effective profile from durable proof or new bounded evidence; do not infer past model identity from current defaults. |
| R2 — Oracle still certifies unsupported recovery, verification and records | HIGH / material | OPEN | Filename-only rg listing, first-line/metadata reads, failed cat masked by true, unread applicable ADR, echo-only verification, garbage handoff/issue and empty negative success-envelope cases admit PASS. Retained reviewer probes demonstrate nine adverse false positives. Fail closed on insufficient scoped read/result/chronology/verification/handoff/stop evidence, add regressions and uniformly re-evaluate raw records; rerun affected cases only when needed. |
| R3 — Portable package installation | MEDIUM / material in round 1 | CLOSED | Actual package-only installer produces fixture-identical bridges; fresh/existing guide mapping and links pass; regular/symlink/directory host collisions preserve existing entries with documented manual merge. This closes the distribution defect, not R4's live scope behavior. |
| R4 — Required Claude conflicting-authority and nested-scope conformance | HIGH / material | OPEN | Each required negative creates the forbidden result in both original and characterization runs. Correct behavior within the accepted product/adapter boundary and provide affected real conformance evidence; preserve failures and require re-review. Positives or an unsupported label cannot waive two-harness acceptance. |

## Attempt-3 implementation resolution (appended 2026-09-22T07:36:08Z, agent:ClaudeCode-discovery-fix-3)

This section is the implementor's resolution claim for round 2, appended separately per the round-2 attribution correction; the reviewer-owned findings table above is unchanged.

- **R1 (profile provenance):** Codex sessions now launch with explicit `--model gpt-6-astra`, recorded per record as `bounds.codex_model_flag` and `model`; schema `aep-discovery-probe/v3` records `required_extra_reads`, `post_record_contents`, and captured read/shell outputs; the timeout handler retains decoded bytes stdout/stderr (round-2 correction 3). Evidence: [attempt-3 evidence](../EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md).
- **R2 (oracle):** strict content-read whitelist with first/last content-marker binding, conservative compound-command attribution, post-state record structural validation (defect `FAIL` / missing `UNVERIFIED`), negative stop evidence, and spec-linked ADR required reads. All nine round-2 adverse classes are unit regressions; the reviewer's 19-probe script classifies 0 PASS against the frozen oracle (SHA-256 `e991d148…`, recorded in the evidence). 163 unit tests and the structural validator pass. One mid-attempt refinement is disclosed: a failed strict read of a required path genuinely absent from the pre-run manifest counts as engagement evidence (the missing-entry stop requires exactly that probe); it flips one launch-time classification (`claude negative_missing_entry run1`, UNVERIFIED→PASS) under the uniform final re-evaluation and is regression-tested.
- **R4 (Claude conflicting-authority + nested negatives):** conflict-stop and scope-isolation wording strengthened in `protocol/BOOTSTRAP.md`, root `BOOTSTRAP.md`, bridge rule 3 in `protocol/README.md` and both root bridges; fixture regenerated from the delivered bytes. Result: `negative_conflicting_authority` 2/2 PASS and `negative_nested` 2/2 PASS (both were 2/2 FAIL in attempt 2).
- **Attempt-2 records:** all 34 retained records uniformly re-extracted and reclassified under the final oracle ([`attempt-2-reclassification-v3.json`](../EVIDENCE/discovery-conformance/attempt-2-reclassification-v3.json)); downgrade causes (unretained evidence classes) are disclosed in the attempt-3 evidence.
- **Attempt-2 evidence corrections:** attributable corrections for round-2 non-material items 1–3 appended to the attempt-2 evidence without altering original text.
- **Live coverage status:** Claude profile coverage complete (3 evaluated PASS per positive case of 7 launched each; all negatives PASS; manual fallback PASS; adapter-auto OBSERVE). Codex root: `positive_root` 3/7 PASS, five negatives PASS — but `negative_collision` and `adapter_removed_manual` remain UNVERIFIED (single run each, sole gap: no recorded verification read) after two account-quota exhaustions. On the owner's 2026-09-22 directive all further Codex launches are cancelled pending explicit authorization; the minimal remaining run set (2 cases, estimated 2–6 sessions) is documented in [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUE-20260922T073608Z-codex-quota-authorization.md). The Codex profile claim is therefore not established, and this milestone is not submitted for review.

## Owner decision persisted (appended 2026-09-23T01:32:06Z, agent:ClaudeCode-discovery-fix-3)

- **Bounded authorization recorded:** the human technical owner authorized the minimal Codex supplementary verification set in [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUE-20260922T073608Z-codex-quota-authorization.md): only `codex negative_collision` and `codex adapter_removed_manual`, one evaluated PASS per case under the frozen v3 oracle then stop, at most 6 new Codex live sessions total, failures preserved without unbounded retry, stop at the cap and return to the human/review boundary, no repetition inflation, no wakeups or auto-relaunch, no specification change. **Execution is separately gated:** the owner explicitly deferred execution pending a distinct "execute the authorized Codex supplementary verification now" instruction. No Codex session has been launched or scheduled under this authorization.
- **Self-correction (ROTATE-004):** the 2026-09-22T07:51:33Z `IN_PROGRESS → BLOCKED_HUMAN_AUTHORITY` transition misapplied the contract — quota exhaustion is a participant failure that MUST NOT produce `BLOCKED_HUMAN_AUTHORITY`. The genuine human gate was the owner's resource directive, which is now satisfied by the recorded decision. The state block is never hand-edited; this correction fixes the record, not the machine state.
- **Contract gap:** the accepted pipeline contract (ADR-20260814T015817Z decision 5, PROJECT_SPEC `PIPELINE-003`) defines no exit edge from `BLOCKED_HUMAN_AUTHORITY`, so `run_pipeline.py` refuses every transition out of it even though the human gate is satisfied. Resolution requires owner-approved contract evolution and is tracked in [ISSUE-20260923T013206Z-pipeline-blocked-exit](ISSUE-20260923T013206Z-pipeline-blocked-exit.md). The milestone's machine state remains `BLOCKED_HUMAN_AUTHORITY` until that amendment lands; no review submission has occurred.

## Blocker

- **Blocked from:** `IN_PROGRESS`
- **Blocker:** `Linked human-authority issue ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md` (authorization gate ISSUE-20260922T073608Z is satisfied by the recorded owner decision; the machine-exit contract gap and the owner's deferred execution trigger remain)
- **Unblock owner:** `Human technical owner`
- **Unblock condition:** `The owner decides the proposed pipeline-contract amendment in ISSUE-20260923T013206Z-pipeline-blocked-exit, and separately issues the explicit "execute the authorized Codex supplementary verification now" instruction before any Codex launch consumes the authorized budget.`

## Residual uncertainty

- **Independent review correction `2026-09-22T02:01:17Z`:** Round 2 supersedes the implementation assessments below for current acceptance. R1 profile provenance, R2 oracle soundness and R4 mandatory Claude conformance are open; R3 is closed and fixture/bridge fidelity is verified. Codex root observations are useful, but complete supported-profile acceptance is not established. Both harnesses remain required. Existing authority permits bounded repairs; this is not BLOCKED_HUMAN_AUTHORITY.
- **Attempt-2 live result `2026-09-21T11:20:00Z`:** Codex CLI `0.153.4` root-start profile satisfies the acceptance criteria on this host (3/3 positives, all negatives PASS, manual fallback PASS). The Claude Code `2.1.118` profile does NOT: `negative_conflicting_authority` and `negative_nested` failed 2/2 sessions each (systematic; participant resolves the conflict per the truth hierarchy and implements, and descends into an adopted nested repository from an unadopted outer root, respectively). Per acceptance criterion 5 the Claude support claim is not established and milestone acceptance is prevented unless a fresh independent review adjudicates otherwise. Remediation may cross the Human Authority Boundary (normative-text semantics); this issue takes no position.
- Attempt-1 historical profile observations do not certify the delivered protocol; they are superseded for conformance by the attempt-2 evidence.
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
| `2026-09-20T09:35:35Z` | `agent:ClaudeCode-discovery` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target 074678d080fc6c1d57d2912314ae21296b618612 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260920T093535Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-1.json. |
| `2026-09-21T01:31:25Z` | `agent:Codex-discovery-review-20260921` | `REVIEW` | `REVIEW` | Persisted the already-completed independent round: CHANGES_REQUIRED, three open material findings R1 HIGH/R2 HIGH/R3 MEDIUM, non-material N1–N3 and exact reproduction evidence. Earlier read-only platform restriction prevented persistence; no re-review, implementation fix, acceptance or next-role action. Commit this round before the reviewer invokes the pipeline transition. |
| `2026-09-21T01:38:51Z` | `agent:Codex-discovery-review-20260921` | `REVIEW` | `IMPLEMENTING` | Pipeline AWAITING_PEER_REVIEW -> CHANGES_REQUIRED. Independent review ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-21t013125z--agentcodex-discovery-review-20260921 recorded 3 open material finding(s); within-scope fixes are required. |
| `2026-09-21T09:06:56Z` | `agent:ClaudeCode-discovery-fix` | `IMPLEMENTING` | `IMPLEMENTING` | Pipeline CHANGES_REQUIRED -> IN_PROGRESS. Implementation attempt 2 began from immutable base bd3e00f2dc5c261b12653ddb3912eb834c92645c. |
| `2026-09-21T11:20:00Z` | `agent:ClaudeCode-discovery-fix` | `IMPLEMENTING` | `IMPLEMENTING` | Attempt-2 implementation within contract allowed paths: R3 self-contained portable bridge installer in `protocol/README.md`; R2 fail-closed oracle rewrite (schema v2, adverse regressions); R1 faithful adopted fixture bound to delivered bytes; N1 attributable correction appended to attempt-1 evidence; 34-session live program with frozen-oracle re-evaluation. Result: Codex root profile satisfies the acceptance criteria; Claude profile does not (systematic `negative_conflicting_authority` and `negative_nested` failures, 2/2 each), recorded honestly in the attempt-2 evidence without claiming support. 151 unit tests and validator pass. |
| `2026-09-22T01:22:57Z` | `agent:ClaudeCode-discovery-fix` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target cc7961187f067cbc7b337b8f80a64505693f7bc6 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json. |
| `2026-09-22T02:01:17Z` | `agent:Codex-discovery-review-20260922` | `REVIEW` | `REVIEW` | Fresh independent round on attempt-2 target: CHANGES_REQUIRED, three open material findings R1/R2/R4; R3 closed. Reproduced complete target checks, 19 adverse/control probes, package installation and 34-record raw reclassification. Two-harness authority remains binding; bounded fixes do not require a new owner decision. Commit this round before the reviewer-only pipeline transition; no implementation/acceptance/next-role work. |
| `2026-09-22T02:09:43Z` | `agent:Codex-discovery-review-20260922` | `REVIEW` | `IMPLEMENTING` | Pipeline AWAITING_PEER_REVIEW -> CHANGES_REQUIRED. Independent review ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md#2026-09-22t020117z--agentcodex-discovery-review-20260922 recorded 3 open material finding(s); within-scope fixes are required. |
| `2026-09-22T02:35:41Z` | `agent:ClaudeCode-discovery-fix-3` | `IMPLEMENTING` | `IMPLEMENTING` | Pipeline CHANGES_REQUIRED -> IN_PROGRESS. Implementation attempt 3 began from immutable base 88fa8359ec3a62f200096d0d96bd04a88ebd118a. |
| `2026-09-22T07:36:08Z` | `agent:ClaudeCode-discovery-fix-3` | `IMPLEMENTING` | `IMPLEMENTING` | Attempt-3 implementation within contract allowed paths: R1 explicit Codex `--model gpt-6-astra` provenance plus schema-v3 records and timeout capture fix; R2 oracle rehardening (strict marker-bound reads, record validation, stop evidence, ADR reads; 19 reviewer probes all non-PASS; 163 unit tests OK); R4 conflict-stop/scope wording in product text and bridges with fixture regeneration; both R4 failure modes now 2/2 PASS. 42 live records retained plus 11 quota-aborted launches preserved separately. Owner paused further Codex live runs; `codex negative_collision`/`adapter_removed_manual` coverage outstanding — see ISSUE-20260922T073608Z-codex-quota-authorization. No review submission. |
| `2026-09-22T07:51:33Z` | `agent:ClaudeCode-discovery-fix-3` | `IMPLEMENTING` | `BLOCKED` | Pipeline IN_PROGRESS -> BLOCKED_HUMAN_AUTHORITY. Human authority is required; linked blocker ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md defines the unblock condition. |
| `2026-09-23T01:32:06Z` | `human:MattSureham` (recorded by `agent:ClaudeCode-discovery-fix-3`) | `BLOCKED` | `BLOCKED` | Owner granted the bounded Codex supplementary verification authorization (2 cases, 1 evaluated PASS each, ≤6 sessions, no auto-retry/inflation/wakeups) in ISSUE-20260922T073608Z and explicitly deferred execution pending a distinct "execute now" instruction. Self-correction recorded: the 2026-09-22 blocked entry misapplied ROTATE-004. The pipeline contract has no exit edge from BLOCKED_HUMAN_AUTHORITY, so the machine state is unchanged pending the owner-decided contract amendment in ISSUE-20260923T013206Z-pipeline-blocked-exit. No Codex session launched or scheduled; no review submission. |

## Closure checklist

- [ ] Expected behavior is tied to durable accepted requirements and architecture.
- [ ] The implementation is recorded at an immutable target within accepted scope.
- [ ] Required deterministic and real fresh-session verification ran; evidence is durable.
- [ ] Fresh independent review is `APPROVED` with zero open material findings.
- [ ] Recorder verifies closure and the pipeline records acceptance.
- [ ] Complexity and residual uncertainty are covered or explicitly owned.
- [ ] HANDOFF reflects the resulting state and one next action.
