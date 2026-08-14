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
- **Updated UTC:** `2026-08-14T02:40:06Z`
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
  "state": "AWAITING_PEER_REVIEW",
  "attempt": 1,
  "implementor": "agent:Codex-root",
  "base_revision": "a6f2699a4bed2e1a08c9a506bad62204bd2d0086",
  "target_revision": "6c0a3bda06686635023e334a4e644fb176372b04",
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json"
  ],
  "review_references": [],
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

No independent review round has been recorded. A fresh participant must inspect the immutable target, accepted specification/ADR, implementation, tests, and evidence directly.

## Blocker

- **Blocked from:** `NOT BLOCKED` (historically blocked from `OPEN`)
- **Blocker:** `NONE` — the previously recorded condition was satisfied on `2026-08-14T01:58:17Z`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Independent semantic correctness and disposition remain unknown. Immutable target identity and deterministic output are now confirmed by the linked evidence.
- `F1` and `F2` are implementor-assessed material findings against target `6c0a3bd`; their exact observations and resolution conditions are durable in the verification evidence. A peer must independently confirm or reject that assessment before the pipeline may enter its fix loop.
- `F3` preserves record bytes but can split the generated Activity history table in Markdown rendering; reviewer disposition is pending.
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
