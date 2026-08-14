# Runtime Automation

## Metadata

- **ID:** `ISSUE-20260806T013907Z-runtime-automation`
- **Title:** Implement the authorized root-local milestone pipeline
- **Status:** `IMPLEMENTING`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-14T03:55:38Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Authorized milestone pipeline phase and `MILESTONE-20260814T015817Z-authorized-pipeline-v1`; historical post-pilot hardening deferral retained as prior context
- **ADRs:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md); [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](../EVIDENCE/EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md); generated [`attempt-1 verification`](../EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json)
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
  "state": "IN_PROGRESS",
  "attempt": 2,
  "implementor": "agent:Codex-root-fix-2",
  "base_revision": "57fe35c3a397fb1d71caa466d32a62f84fd51802",
  "target_revision": null,
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json"
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

- **Pipeline verification `2026-08-14T02:31:16Z`:** [`EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `6c0a3bda06686635023e334a4e644fb176372b04`.
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

## Blocker

- **Blocked from:** `NOT BLOCKED` (historically blocked from `OPEN`)
- **Blocker:** `NONE` — the previously recorded condition was satisfied on `2026-08-14T01:58:17Z`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Independent review round 1 (`2026-08-14T03:11:06Z`, `ClaudeCode/pipeline-review`) independently reproduced the target verification and both gate findings, and recorded `CHANGES_REQUIRED` with two open material findings (`R1`/`R2`, matching implementor `F1`/`F2`) and one non-material finding (`R3`/`F3`). Immutable target identity and deterministic output remain confirmed by the linked evidence.
- `R1` and `R2` are now reviewer-confirmed material findings against target `6c0a3bd`; their resolution conditions are durable in the review round above and in the verification evidence. The within-scope fix loop is authorized without a new owner prompt.
- `F3` (reviewer `R3`) is independently classified `LOW` and non-material: it preserves record bytes but can split the generated Activity history table in Markdown rendering; it rides the authorized fix loop or an explicit accepted limitation.
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
## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [ ] Required verification is incomplete: configured checks passed, but reproduced `F1`/`F2` behaviors remain unresolved and linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies (not applicable — `Review: INDEPENDENT`).
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted specification and compatible accepted ADR.
- [ ] New complexity coverage is incomplete until `F1`/`F2` are corrected or independently rejected with evidence; identity/concurrency limits remain linked.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
