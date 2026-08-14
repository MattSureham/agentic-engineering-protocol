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
- **Updated UTC:** `2026-08-14T02:24:27Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Authorized milestone pipeline phase and `MILESTONE-20260814T015817Z-authorized-pipeline-v1`; historical post-pilot hardening deferral retained as prior context
- **ADRs:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md); [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](../EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md)
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
  "attempt": 1,
  "implementor": "agent:Codex-root",
  "base_revision": "a6f2699a4bed2e1a08c9a506bad62204bd2d0086",
  "target_revision": null,
  "verification_evidence": [],
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

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `2026-08-14T02:24:27Z`
- **Reviewed repository state:** `PENDING immutable target`
- **Scope and authority references:** Accepted milestone, specification change, and pipeline ADR linked above
- **Checks and evidence reviewed:** Candidate 37-test suite, live status output, accepted specification/ADR, path allowlist, package boundary, and diff integrity
- **Findings and corrections:** Corrected metadata parsing to distinguish root specification status from issue metadata; rejected ambiguous path spellings; added resolution and authority checks for evidence/review references; all corrections were rerun through the complete suite.
- **Limitations:** Implementor self-review cannot satisfy this issue's independent-review gate.
- **Residual risks:** Python/Git portability beyond the recorded environment, output sensitivity of owner-authorized checks, unauthenticated participant labels, cooperative-only issue replacement, and independent semantic review remain.
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

- Implementation correctness, immutable target identity, exact verification output, and independent disposition remain unknown until subsequent lifecycle stages.
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

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies (not applicable — `Review: INDEPENDENT`).
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the accepted specification and compatible accepted ADR.
- [x] New complexity is covered by the accepted ADR and candidate tests or linked to the existing blocked identity/concurrency issues.
- [x] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
