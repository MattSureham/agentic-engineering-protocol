# Runtime Automation

## Metadata

- **ID:** `ISSUE-20260806T013907Z-runtime-automation`
- **Title:** Implement the authorized root-local milestone pipeline
- **Status:** `REVIEW`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-14T04:41:08Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Authorized milestone pipeline phase and `MILESTONE-20260814T015817Z-authorized-pipeline-v1`; historical post-pilot hardening deferral retained as prior context
- **ADRs:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md); [`attempt-1 verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md) and generated [`attempt-1 JSON`](../EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json); [`attempt-2 verification`](../EVIDENCE/EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification.md) and generated [`attempt-2 JSON`](../EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json)
- **Milestone:** `MILESTONE-20260814T015817Z-authorized-pipeline-v1`

## Problem

Some protocol checks could be automated, but a runtime, orchestrator, daemon, service, database, or complex CLI would materially change the product's Markdown-first, runtime-agnostic boundary.

## Evidence or reproduction

The current package consists of ten Markdown files and intentionally requires no executable dependency. No accepted requirement asks for automation.

The preceding sentence is preserved as the observation at creation time. On `2026-08-14`, the human technical owner explicitly accepted a bounded root-local pipeline capability while preserving the package's ten-file Markdown-only boundary. The accepted specification and ADR linked above now provide the requirement and architecture that were previously absent.

## Expected behavior

Keep the current protocol runtime-free. Consider automation only under a separately accepted capability specification with portability, dependency, lifecycle, and failure requirements.

That historical expected behavior remains applicable to the copy-ready package. The current accepted behavior is a root-only state-and-gate tool outside `protocol/`, with no adopter dependency, agent orchestration, service, database, network use, concurrent-writer guarantee, authenticated identity claim, or arbitrary scope expansion.

## Assumptions

- **CONFIRMED:** Runtime automation was explicitly excluded from the completed hardening phase; the accepted pipeline phase supersedes only that deferral for its exact root-local milestone.
- **CONFIRMED:** The owner selected root dogfood first; no supported adopter runtime is authorized.
- **UNKNOWN:** Whether future adopters need an optional distributed companion and which additional portability contract would be required.

## Investigation and decision

At creation, no runtime component was adopted or prototyped. The `2026-08-14` owner decision satisfies the recorded blocker through an accepted specification update and compatible accepted ADR. The selected design binds machine state to the canonical digest of the milestone entry, stores operational state inside this owning issue, reuses the structural validator, executes only accepted local argv checks with `shell=False`, and leaves judgment/review outside the tool.

The implementation is independently reviewed because it changes governance semantics, introduces subprocess execution and Git coupling, and can mechanically advance issue state. Acceptance remains impossible until a fresh reviewer records `APPROVED` with zero open material findings on the immutable target.

## Change

- **Files or components:** Root/reusable governance wording and templates; root-only pipeline script/tests; generated evidence; this issue/HANDOFF/checkpoint. Exact allowed paths are in the accepted milestone contract.
- **Behavior changed:** Before, no runtime capability was authorized. After the reviewed target, already-authorized milestones can advance through deterministic local gates and independent review without repeated owner prompts.
- **Attempt-2 correction:** Review submission now captures its expected HEAD and exact specification/owning-issue bytes, rejects pre-existing ignored artifacts, reruns deterministic repository postconditions after accepted commands, writes a machine-readable `FAIL` record without advancing when the safe evidence boundary remains available, and refuses missing, non-directory, symlinked, or escaping `EVIDENCE/` boundaries during orientation and immediately before output creation. Activity rows and verification prose use separate insertion paths so generated Markdown retains table and heading continuity.
- **Out-of-scope work deliberately excluded:** Runtime inside `protocol/`; agent invocation; daemon/service/database/web UI; distributed scheduler; external tracker; multi-host coordination; authenticated identity; concurrent-writer guarantee; automatic Git commit/push/network action.
- **Rollback or recovery:** Revert the implementation target and retain this authority/decision history; manual protocol operation remains valid because the reusable package has no runtime dependency.

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260814T015817Z-authorized-pipeline-v1",
  "authority_digest": "36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4",
  "state": "AWAITING_PEER_REVIEW",
  "attempt": 2,
  "implementor": "agent:Codex-root-fix-2",
  "base_revision": "57fe35c3a397fb1d71caa466d32a62f84fd51802",
  "target_revision": "26d890f6e27ad181265ee5417a45637d867aa2dc",
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json",
    "EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json"
  ],
  "review_references": [
    "ISSUES/ISSUE-20260806T013907Z-runtime-automation.md#2026-08-14t031106z--claudecodepipeline-review"
  ],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-08-14T01:58:17Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Accepted PROJECT_SPEC milestone and compatible accepted ADR satisfy the prior blocker."
    },
    {
      "sequence": 2,
      "utc": "2026-08-14T02:06:16Z",
      "actor": "agent:Codex-root",
      "from": "AUTHORIZED",
      "to": "READY",
      "reason": "Accepted contract, dependencies, structural baseline, issue blocker, and authority digest were reconciled."
    },
    {
      "sequence": 3,
      "utc": "2026-08-14T02:06:16Z",
      "actor": "agent:Codex-root",
      "from": "READY",
      "to": "IN_PROGRESS",
      "reason": "Implementation began from immutable authority boundary a6f2699a4bed2e1a08c9a506bad62204bd2d0086."
    },
    {
      "sequence": 4,
      "utc": "2026-08-14T02:31:16Z",
      "actor": "agent:Codex-root",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target 6c0a3bda06686635023e334a4e644fb176372b04 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json."
    },
    {
      "sequence": 5,
      "utc": "2026-08-14T03:18:19Z",
      "actor": "agent:ClaudeCode-pipeline-review",
      "from": "AWAITING_PEER_REVIEW",
      "to": "CHANGES_REQUIRED",
      "reason": "Independent review ISSUES/ISSUE-20260806T013907Z-runtime-automation.md#2026-08-14t031106z--claudecodepipeline-review recorded 2 open material finding(s); within-scope fixes are required."
    },
    {
      "sequence": 6,
      "utc": "2026-08-14T03:55:38Z",
      "actor": "agent:Codex-root-fix-2",
      "from": "CHANGES_REQUIRED",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 2 began from immutable base 57fe35c3a397fb1d71caa466d32a62f84fd51802."
    },
    {
      "sequence": 7,
      "utc": "2026-08-14T04:06:44Z",
      "actor": "agent:Codex-root-fix-2",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target 26d890f6e27ad181265ee5417a45637d867aa2dc passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Verification

The authority-boundary statement that no implementation existed is preserved here. Candidate implementation verification is recorded additively below and will be superseded by immutable-target evidence when the state advances to `AWAITING_PEER_REVIEW`.

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-14T02:24:27Z` | `Codex/root` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; `python3 scripts/run_pipeline.py status --json` repeated through both supported root-option positions; `git diff --check` | `39` tests pass; live contract/state status passes with digest `36fba5d...`; repeated JSON output has identical SHA-256 `6565d689...`; diff check passes | Candidate worktree output; immutable evidence pending | Candidate is not an immutable target; independent review and broader platform/CommonMark validation remain pending |
| `2026-08-14T02:39:53Z` | `Codex/root` | Two safe temporary-repository reproductions: an accepted command writes an unexpected worktree file; a committed baseline `EVIDENCE` symlink targets a sibling temporary directory | Both submissions incorrectly exit `0` and enter `AWAITING_PEER_REVIEW`; the first leaves the unexpected file, the second creates JSON outside the repository | [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md), Post-target implementor findings `F1`/`F2` | Target remains immutable; reviewer must independently classify; fixes are not present |
| `2026-08-14T04:02:07Z` | `Codex/root-fix-2` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; structural validator; read-only pipeline status; targeted adversarial fixture runs; `git diff --check` | `44` tests pass; structural validation passes; status reports attempt-2 `IN_PROGRESS`; ordinary/ignored/HEAD/specification/issue mutations produce failure evidence without state advancement; unsafe evidence directories cannot receive output; generated Markdown remains contiguous | Candidate worktree plus independent round-1 resolution conditions | Candidate is not yet an immutable target and implementor verification is not independent review |
| `2026-08-14T04:08:12Z` | `Codex/root-fix-2` | Pipeline submission against target `26d890f`; generated-evidence inspection; exact-target `git archive` rerun; compilation, isolated copy, repository Markdown/link, scope, governed-source, whitespace, and credential scans | Pipeline and exact-target suite pass 44 tests; all four postconditions pass; exact 10-file package/zero symlinks; 43 Markdown files/216 relative links/zero findings; five allowed target paths; zero credential-shaped matches | [`EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification`](../EVIDENCE/EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification.md) and generated [`attempt-2 JSON`](../EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json) | Implementor evidence cannot satisfy fresh independent review; Darwin/Python/Git and Markdown-linter limits remain explicit |

- **Pipeline verification `2026-08-14T02:31:16Z`:** [`EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `6c0a3bda06686635023e334a4e644fb176372b04`.

- **Pipeline verification `2026-08-14T04:06:44Z`:** [`EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json`](../EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json) — deterministic structural and accepted-command gates passed for `26d890f6e27ad181265ee5417a45637d867aa2dc`.

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `2026-08-14T02:24:27Z`
- **Reviewed repository state:** Immutable implementation target `6c0a3bda06686635023e334a4e644fb176372b04`; subsequent issue/evidence/HANDOFF records contain no implementation change
- **Scope and authority references:** Accepted milestone, specification change, and pipeline ADR linked above
- **Checks and evidence reviewed:** 39-test immutable-target rerun, live status/transition output, generated bounded JSON, accepted specification/ADR, exact path allowlist, isolated package, repository Markdown/links, source identities, compile, diff, credential scan, and publication checks in [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md)
- **Findings and corrections:** Before target, corrected metadata parsing, ambiguous path acceptance, and evidence/review reference checks. After target, reproduced unresolved `MEDIUM` findings `F1` (verification-command mutation is not rechecked) and `F2` (baseline `EVIDENCE` symlink permits an escaping write), plus `LOW` `F3` (generated activity-table spacing). Exact resolution conditions are in the linked evidence; no post-target implementation was changed.
- **Limitations:** Implementor self-review cannot satisfy this issue's independent-review gate.
- **Residual risks:** Unresolved `F1`/`F2` gate-boundary findings and `F3` rendering defect; Python/Git portability beyond the recorded environment; output sensitivity of owner-authorized checks; unauthenticated participant labels; cooperative-only issue replacement; and independent semantic review.
- **Outcome:** `NOT_APPLICABLE`

### Attempt 2 implementor verification — not an independent review

- **Participant:** `Codex/root-fix-2`
- **Captured UTC:** `2026-08-14T04:02:07Z`
- **Problem:** Independent round 1 established material `R1`/`R2` gate-boundary defects and non-material `R3` rendering discontinuity at target `6c0a3bd`.
- **Evidence or reproduction:** The new fixture matrix preserves the original failing shapes and additionally covers ignored artifacts, HEAD mutation, exact authority/issue byte mutation hidden from ordinary status, missing/non-directory evidence paths, and evidence-directory replacement between orientation and output creation.
- **Change:** Added ordered repository postconditions and bounded evidence fields; safe-directory checks at orientation and pre-write; no implicit evidence-directory creation; separate prose/table record insertion; historical activity-table whitespace normalization without changing row content or order.
- **Verification:** Full candidate suite reports `Ran 44 tests ... OK`; structural validator and live read-only pipeline status pass; whitespace check passes. Exact-target verification and generated attempt-2 evidence remain pending.
- **Remaining uncertainty:** Fresh independent review must determine whether the new immutable target satisfies `R1`/`R2` and whether `R3` is fully resolved. TOCTOU behavior under non-cooperating writers, authenticated identity, broader platform portability, and semantic safety of owner-authorized commands remain outside the accepted boundary.
- **Boundary:** This is attributable implementor evidence only. It records no peer-review disposition and cannot satisfy the independent-review gate.

#### Immutable target result

Pipeline submission at `2026-08-14T04:06:44Z` bound attempt 2 to target `26d890f6e27ad181265ee5417a45637d867aa2dc`, generated a `PASS` record with all four repository postconditions `PASS`, and advanced only to `AWAITING_PEER_REVIEW`. The complete exact-target matrix and integrity hashes are in [`EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification`](../EVIDENCE/EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification.md). This additive result supersedes only the candidate-pending statement above; it does not supply an independent disposition.

## Independent review rounds

- **Required:** `YES` — accepted implementation affects governance semantics, runtime lifecycle, subprocess execution, Git coupling, and automated acceptance gates.

### 2026-08-14T03:11:06Z — ClaudeCode/pipeline-review

- **Reviewed repository state:** Immutable target `6c0a3bda06686635023e334a4e644fb176372b04` (direct parent and authority boundary `a6f2699a4bed2e1a08c9a506bad62204bd2d0086`), extracted via `git archive` into a fresh temporary directory; post-target record range through `d85223b95de7564567316087efbb86d80d76597c` (local `main` equals cached `origin/main`); live worktree clean before and after every review command
- **Reviewed target:** `6c0a3bda06686635023e334a4e644fb176372b04`
- **Open material findings:** `2`
- **Scope:** Accepted root `PROJECT_SPEC.md` Authorized milestone pipeline phase (owner authority clarification, `PIPELINE-001`–`PIPELINE-008`, authorized milestone contract, six pipeline acceptance criteria); accepted [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md); complete `scripts/run_pipeline.py` and `tests/test_run_pipeline.py`; every governance wording diff in the target range (root and reusable BOOTSTRAP, both issue templates, reusable PROJECT_SPEC/PROMPTS/README, root README); all three `REVIEW` issues; [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md) and the generated attempt-1 JSON; implementor findings `F1`–`F3`
- **Commands or procedures:** `git archive 6c0a3bda06686635023e334a4e644fb176372b04 | tar -x` into a fresh temporary directory; at the extracted target `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` produced `Ran 39 tests in 12.752s` / `OK`; independent recomputation of the milestone contract digest from the target's `PROJECT_SPEC.md` (canonical-JSON SHA-256 equals the recorded `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4`); read-only `python3 scripts/run_pipeline.py status --json` at `d85223b` exited `0` with state `AWAITING_PEER_REVIEW` and matching digest; SHA-256 verification of all five artifact digests recorded in the verification evidence (generated JSON `04823c30...`, `run_pipeline.py` `7f8de45c...`, `test_run_pipeline.py` `e938313c...`, `PROJECT_SPEC.md` `efafb0a2...`, pipeline ADR `f24c15f2...` — all match); Git checks confirming the target's parent is exactly `a6f2699`, the target is an ancestor of HEAD, the target range touches exactly the 15 contract `allowed_paths`, and the post-target range is seven record-only paths; two independent temporary-repository reproductions using the target's own fixture harness (quoted below)
- **Specification compliance:** Target scope, parent binding, and contract digest conform to the contract and acceptance criterion 1. `PIPELINE-001`/`002`/`003`/`005`/`006`/`008` behave as specified and are covered by the 18 pipeline scenarios (authority/digest/schema refusal, lifecycle and dependency ordering, label separation, exact disposition vocabulary, fix/re-review loop, next-milestone selection, human-escalation blocker requirements, no package runtime, no network or Git mutation). `PIPELINE-004` and `PIPELINE-007` are implemented but their gate boundary is incomplete — see material findings R1/R2. Acceptance criteria 2–5 are met for the configured checks; criterion 6 is this round. The governance wording matches the three owner decisions recorded at `2026-08-14T01:58:17Z` in all intended artifacts, and the executable review gate rejects informal dispositions, self-review labels, target mismatch, approval with material findings, and any `BLOCKED`-to-approval mapping.
- **Correctness and regression findings:** 39/39 tests reproduce at the exact extracted target. R1 reproduced independently: with the fixture's accepted argv configured as a Python one-liner writing `work/reviewer-side-effect.txt`, submission exited `0` and advanced to `AWAITING_PEER_REVIEW` while the unexpected file persisted untracked; no gate rechecks worktree state after `_run_checks`, because `_require_clean` runs only before the accepted commands. R2 reproduced independently: with a committed baseline `EVIDENCE` symlink to a sibling temporary directory, `status` and submission both exited `0`, the state advanced, and the generated JSON was written outside the repository; observed beyond the implementor's report, every subsequent pipeline invocation then fails closed with `AEP-PIPE-STATE` ("verification evidence does not resolve safely"), leaving the milestone in a poisoned state that requires manual repair. R3 confirmed by direct byte inspection of this issue: the generated `2026-08-14T02:31:16Z` activity row is separated from its table by a blank line, and the generated Verification bullet is immediately adjacent to the following heading.
- **Architecture and complexity findings:** No new truth tier is introduced: machine state is digest-bound and explicitly subordinate in both BOOTSTRAP documents, and the reusable package remains ten Markdown files with no runtime (isolated-copy validation passes at the target). One accepted-ADR limitation is recorded for future specification evolution rather than counted as a finding: `BLOCKED_HUMAN_AUTHORITY` has no exit transition, so once a milestone escalates, the tool cannot express resumption after the owner supplies authority; this matches ADR decision 5 and `PIPELINE-003` as accepted. The environment scrub also strips `GIT_AUTHOR_*`/`GIT_COMMITTER_*` variables through the `AUTH` fragment; harmless for the current contract. The R1 hole is partially bounded but not closed at acceptance time: `_post_target_drift` and `_require_clean` would catch a side effect committed outside record-only paths, but a mutating check that writes under `EVIDENCE/`, an `ISSUES/*.md` record, or the owning issue could pass the drift gate as apparent record content.
- **Material findings and resolution conditions:** R1 (implementor `F1`; independently assessed MEDIUM, material): submission advances after the accepted commands even when they mutate the repository, so verification evidence can be recorded against an immutable target that no longer matches the verified working state; resolution — after the accepted commands complete, recheck HEAD identity, worktree cleanliness (accounting for ignored paths such as `.DS_Store` or `__pycache__`, which plain porcelain output does not report), and the authority/issue source bytes, record a failed result without advancement on any mismatch, and add regression tests. R2 (implementor `F2`; independently assessed MEDIUM, material): the evidence write path never verifies that `EVIDENCE/` is a real directory contained in the repository, so generated evidence can escape the ownership boundary at creation time and later operation fails closed with a poisoned state; resolution — reject a symlinked or escaping evidence directory during orientation and before writing, and add baseline and transition regression tests. Non-material: R3 (implementor `F3`; LOW): `_append_section_line` separates generated activity rows from their table with a blank line and omits the blank line before the following heading; bytes are preserved and machine gates are unaffected; resolve in the fix loop by specializing section/table insertion with a rendering-continuity test, or record an explicit accepted limitation.
- **Limitations:** Single environment (Darwin arm64, Python `3.9.6`, Apple Git `2.50.1`); no dedicated CommonMark linter was available; participant labels are unauthenticated by design and were not authenticated here; adequacy of human-facing wording is judgment, not proof; usefulness in a second real repository remains undemonstrated.
- **Residual risks:** The two material findings define the acceptance gate; after their resolution a fresh independent round on the new immutable target is required. Python/Git portability, non-cooperating concurrent writers, authenticated identity, and semantic safety of owner-authorized check commands remain outside the verified boundary as recorded in the ADR and verification evidence.
- **Evidence:** Reproduction outputs quoted inline above; [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md); generated [`attempt-1 verification`](../EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json); this issue's Verification section and Activity history bytes.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** `FIRST ROUND`

### 2026-08-14T04:41:08Z — ClaudeCode/pipeline-review-2

- **Reviewed repository state:** Immutable attempt-2 target `26d890f6e27ad181265ee5417a45637d867aa2dc` (direct parent and attempt boundary `87cf4acd222ce280d9f5d5ced301212e5ec4cc09`; attempt-2 base `57fe35c3a397fb1d71caa466d32a62f84fd51802`), extracted via `git archive` into a fresh temporary directory; post-target record range through `f9f9a20288231f177feb162378659def57cc9d6b` (local `main` equals cached `origin/main` and direct remote `refs/heads/main`); live worktree clean before and after every review command
- **Reviewed target:** `26d890f6e27ad181265ee5417a45637d867aa2dc`
- **Open material findings:** `0`
- **Scope:** The round-1 resolution conditions for material `R1`/`R2` and the selected correction for non-material `R3` only: the complete attempt-2 diff `57fe35c..26d890f` (exactly `scripts/run_pipeline.py`, `tests/test_run_pipeline.py`, the owning issue, `HANDOFF.md`, `HUMAN_CHECKPOINT.md`); the generated attempt-2 JSON and full verification evidence; the owning issue's regenerated activity-table and pipeline-state bytes; carryover of both wording change sets; contract digest and scope discipline. The accepted specification, both accepted ADRs, and the reusable package are unchanged at this target and were reviewed in round 1.
- **Commands or procedures:** `git archive 26d890f6e27ad181265ee5417a45637d867aa2dc | tar -x` into a fresh temporary directory; at the extracted target `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` produced `Ran 44 tests in 17.810s` / `OK`; SHA-256 verification of every digest recorded in the attempt-2 evidence (generated JSON `33f756c7...`, `run_pipeline.py` `a9f2af2e...`, `test_run_pipeline.py` `4b8ea98a...`, unchanged `PROJECT_SPEC.md` `efafb0a2...`, unchanged pipeline ADR `f24c15f2...` — all match); Git checks confirming the target's parent is exactly `87cf4ac`, base `57fe35c` is an ancestor, the base-to-target range touches exactly five allowed paths, and the post-target range is five record-only paths; a nine-scenario adverse-reproduction harness written independently by this reviewer against the extracted target's own fixture harness (results quoted below); direct byte inspection of the owning issue's activity table; byte comparison of both wording change sets between `6c0a3bd` and the reviewed target.
- **Specification compliance:** `PIPELINE-004` and `PIPELINE-007` now hold at the gate boundary: review submission refuses pre-existing ignored artifacts, snapshots exact specification/issue bytes at orientation, rechecks HEAD identity and full worktree cleanliness (tracked, untracked, and ignored paths) after the accepted commands, and records bounded `FAIL` evidence without advancing on any mutation; the evidence-ownership boundary is validated at orientation and immediately before writing, and atomic writes no longer create a missing parent. The contract digest remains `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4`; no CLI command, option, allowed path, acceptance check, or disposition vocabulary changed. Acceptance criteria 1–5 reproduce at the exact target; criterion 6 is this round.
- **Correctness and regression findings:** `NONE`. All nine independent adverse scenarios behave as the resolution conditions require. Mutation classes — accepted-command untracked side effect, ignored `.DS_Store`, accepted-command empty commit, specification-byte edit, and issue-byte edit — each exit `1` with `AEP-PIPE-VERIFY`, write `FAIL` evidence carrying the four ordered postconditions (`head-unchanged`, `worktree-clean`, `authority-source-unchanged`, `issue-source-unchanged`), preserve the observed side effects rather than reverting them, and leave machine state `IN_PROGRESS`. Boundary classes — committed baseline `EVIDENCE` symlink, accepted-command directory-to-symlink swap, and missing `EVIDENCE` directory — each exit `2` with `AEP-PIPE-SCOPE`, write zero bytes outside the repository, and do not recreate the directory. The clean control submission exits `0`, advances to `AWAITING_PEER_REVIEW`, and records four `PASS` postconditions, so the new gates do not over-block.
- **Architecture and complexity findings:** `NONE` new. Postconditions are ordered, lower-precedence additive data in the existing `aep-pipeline-verification/v1` schema; fail-closed behavior when the evidence boundary is destroyed is explicit and bounded. The round-1 observation that record-path drift could mask a mutating check is closed for the configured contract: submission now compares specification and owning-issue bytes directly and refuses any tracked, untracked, or ignored residue regardless of path.
- **Material findings and resolution conditions:** `NONE` open. `R1` resolution confirmed by independent reproduction of every recorded mutation class plus the ignored-artifact pre-submit refusal and regression coverage. `R2` resolution confirmed by independent reproduction of the baseline, transition-swap, and missing-directory boundary classes plus regression coverage. `R3` (non-material) confirmed on the real artifact: all fourteen activity rows in the owning issue are contiguous, exactly one blank line precedes the following heading, and historical row content and order are retained.
- **Limitations:** Single environment (Darwin arm64, Python `3.9.6`, Apple Git `2.50.1`); no dedicated CommonMark linter was available; participant labels are unauthenticated assertions; a byte-restoring accepted command remains indistinguishable from no mutation, and the filesystem TOCTOU window remains outside the accepted failure model exactly as recorded in round 1 and the ADR; implementor evidence was treated as a claim to challenge, not as proof.
- **Residual risks:** Non-cooperating concurrent writers, authenticated identity, and semantic safety of owner-authorized commands remain outside the verified boundary per the accepted ADR; none requires a new owner gate for this milestone.
- **Evidence:** Reproduction outputs quoted inline above; [`EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification`](../EVIDENCE/EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification.md); generated [`attempt-2 JSON`](../EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json); the owning issue's activity-table and pipeline-state bytes at HEAD.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** Round-1 material findings `R1` and `R2` are resolved at the reviewed target by independent adverse reproduction of every recorded mutation and boundary class plus a clean control submission; round-1 non-material finding `R3` is confirmed corrected on the real issue bytes; the round-1 scoped approvals of both wording issues carry because their change sets are byte-identical between `6c0a3bd` and the reviewed target.

## Blocker

- **Blocked from:** `NOT BLOCKED` (historically blocked from `OPEN`)
- **Blocker:** `NONE` — the previously recorded condition was satisfied on `2026-08-14T01:58:17Z`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Independent review round 1 (`2026-08-14T03:11:06Z`, `ClaudeCode/pipeline-review`) independently reproduced the target verification and both gate findings, and recorded `CHANGES_REQUIRED` with two open material findings (`R1`/`R2`, matching implementor `F1`/`F2`) and one non-material finding (`R3`/`F3`). Immutable target identity and deterministic output remain confirmed by the linked evidence.
- Independent review round 2 (`2026-08-14T04:41:08Z`, `ClaudeCode/pipeline-review-2`) independently reproduced all recorded mutation and boundary classes against extracted target `26d890f` and recorded `APPROVED` with zero open material findings: `R1` and `R2` are resolved, and `R3` is confirmed corrected on this issue's bytes. The validated `ACCEPTED` transition and closure-checklist completion remain with the next recorder.
- Broader portability and any supported adopter distribution remain unknown and unclaimed.
- Recorded label inequality cannot authenticate participant identity; concurrent writers remain outside the failure model.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `OPEN` | Recorded deferred capability without prototyping |
| `2026-08-06T01:39:07Z` | `Codex/root` | `OPEN` | `BLOCKED` | Product-boundary change lacks approved scope |
| `2026-08-14T01:58:17Z` | Human technical owner `MattSureham`, recorded by `Codex/root` | `BLOCKED` | `OPEN` | Explicit owner decision plus accepted specification and compatible accepted ADR satisfy the exact unblock condition; only the root-local milestone is authorized |
| `2026-08-14T01:58:17Z` | `Codex/root` | `OPEN` | `INVESTIGATING` | Recorded the accepted contract digest, architecture, boundaries, failure model, and implementation/review gates before adding runtime behavior |
| `2026-08-14T02:06:16Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Committed authority boundary `a6f2699`; reconciled deterministic readiness and began attempt 1 without a new owner gate |
| `2026-08-14T02:31:16Z` | `agent:Codex-root` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target 6c0a3bda06686635023e334a4e644fb176372b04 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json. |
| `2026-08-14T02:40:06Z` | `Codex/root` | `REVIEW` | `REVIEW` | Appended post-target self-audit findings `F1`–`F3` without changing implementation or inventing a peer disposition; independent classification remains required. |
| `2026-08-14T03:18:19Z` | `agent:ClaudeCode-pipeline-review` | `REVIEW` | `IMPLEMENTING` | Pipeline AWAITING_PEER_REVIEW -> CHANGES_REQUIRED. Independent review ISSUES/ISSUE-20260806T013907Z-runtime-automation.md#2026-08-14t031106z--claudecodepipeline-review recorded 2 open material finding(s); within-scope fixes are required. |
| `2026-08-14T03:55:38Z` | `agent:Codex-root-fix-2` | `IMPLEMENTING` | `IMPLEMENTING` | Pipeline CHANGES_REQUIRED -> IN_PROGRESS. Implementation attempt 2 began from immutable base 57fe35c3a397fb1d71caa466d32a62f84fd51802. |
| `2026-08-14T04:02:07Z` | `Codex/root-fix-2` | `IMPLEMENTING` | `IMPLEMENTING` | Implemented candidate resolutions for `R1`/`R2` and `R3`; 44 tests, structural validation, live status, and whitespace checks pass; immutable target submission and fresh review remain. |
| `2026-08-14T04:06:44Z` | `agent:Codex-root-fix-2` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target 26d890f6e27ad181265ee5417a45637d867aa2dc passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json. |
| `2026-08-14T04:08:12Z` | `Codex/root-fix-2` | `REVIEW` | `REVIEW` | Recorded exact-target reproduction, generated-postcondition inspection, scope/package/Markdown/integrity evidence, and limitations without supplying or inferring a peer disposition. |
| `2026-08-14T04:41:08Z` | `ClaudeCode/pipeline-review-2` | `REVIEW` | `REVIEW` | Recorded independent review round 2 on immutable target `26d890f`: `APPROVED` with zero open material findings after a nine-scenario adverse reproduction; the `ACCEPTED` transition and closure-checklist completion remain with the next recorder. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required deterministic and exact-target verification passes and is linked; unavailable checks remain explicit. Fresh independent confirmation is tracked by the separate review-gate item below.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies (not applicable — `Review: INDEPENDENT`).
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted specification and compatible accepted ADR.
- [x] New attempt-2 complexity is covered by deterministic mutation, ownership-boundary, failure-evidence, and rendering tests; identity/concurrency limits remain linked and explicitly outside scope.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
