# Structural Protocol Validator

## Metadata

- **ID:** `ISSUE-20260811T013701Z-structural-protocol-validator`
- **Title:** Codify stable structural protocol invariants
- **Status:** `REVIEW`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `AGENT`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-11T01:37:01Z`
- **Updated UTC:** `2026-08-11T02:09:11Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), especially Scope constraints, Quality bar, `HARDEN-003`, `HARDEN-006`, and hardening acceptance criterion 5
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md)
- **Evidence:** [`EVIDENCE-20260811T013701Z-codification-gap-analysis`](../EVIDENCE/EVIDENCE-20260811T013701Z-codification-gap-analysis.md); [`EVIDENCE-20260811T020454Z-structural-validator-verification`](../EVIDENCE/EVIDENCE-20260811T020454Z-structural-validator-verification.md)

## Problem

Stable structural protocol invariants are specified in Markdown but enforced through participant memory and one-off validation harnesses. Prior evidence records useful checks as well as discarded harness failures caused by brittle capitalization, syntax, Unicode-offset, and Markdown-format assumptions. Repeating those harnesses manually increases drift and false-assurance risk.

## Evidence or reproduction

The linked codification analysis fixes the clean baseline, identifies the absence of committed validation tooling, classifies judgment and deterministic rules, and traces the existing one-off checks and limitations.

## Expected behavior

Add only a manually invoked, read-only root development checker for stable structural invariants already owned by the accepted specification and BOOTSTRAP contracts. Markdown remains authoritative; the checker reports observations and MUST NOT authorize requirements, architecture, lifecycle closure, evidence sufficiency, or review outcomes. The reusable package remains exactly ten Markdown files and usable without automation.

## Assumptions

- **CONFIRMED:** The accepted specification permits a tiny helper with obvious value, recognizes executable contracts/tests, and prohibits complex or unnecessary automation.
- **CONFIRMED:** The accepted ADR and `HARDEN-006` preserve the exact ten-file, runtime-agnostic reusable package.
- **INFERRED:** A root-only Python standard-library structural checker is local test organization rather than the shipped runtime automation deferred by [`ISSUE-20260806T013907Z-runtime-automation`](ISSUE-20260806T013907Z-runtime-automation.md).
- **UNKNOWN:** Portability beyond the tested environment and behavior on unsupported future Markdown syntax.

## Investigation and decision

Implement the smallest slice identified by the analysis: package manifest/type checks, package Markdown byte/fence integrity, supported relative-link resolution, and structural HANDOFF checks. Use stable rule IDs, deterministic output, and distinct exits for violations versus inability to evaluate. Keep semantic and authority decisions outside the checker.

No specification or ADR change is proposed. The checker stays outside `protocol/`, has no third-party dependency, performs no writes, and does not change the existing runtime-automation issue.

## Change

- **Files or components:** Root-only `scripts/validate_protocol.py`, `tests/test_validate_protocol.py`, Python cache exclusions in `.gitignore`, concise root README navigation, this issue, evidence, HANDOFF, and HUMAN_CHECKPOINT
- **Behavior changed:** Repository participants gain an optional repeatable structural check with stable diagnostics and exits `0`/`1`/`2`; reusable package behavior and adoption remain unchanged
- **Out-of-scope work deliberately excluded:** Product-shipped tooling, issue closure automation, authority/review/evidence judgments, orchestration, scheduling, concurrent-writer guarantees, authenticated identity, daemon/service/database, complex CLI, CI integration, large-scale coordination, and external trackers
- **Rollback or recovery:** Revert the root-only checker, tests, and navigation while retaining this issue and evidence as historical records

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Optional Python 3 development entry point | Standard-library implementation is the smallest safe way to preserve prior structural checks and regression cases | Planned unit/integration tests and verification evidence | Shipped or required automation remains blocked by [`ISSUE-20260806T013907Z-runtime-automation`](ISSUE-20260806T013907Z-runtime-automation.md) |
| Bounded Markdown link scanner | Links must be checked without a third-party parser or false pass on unsupported syntax | Planned fenced/indented/inline-code, Unicode, escaping, and unsupported-syntax tests | Full CommonMark and semantic-target validation remain explicitly unclaimed |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-11T01:37:01Z` | `Codex/root` | Baseline Git/fetch/ancestry, tree inventory, governing-source hashes, package tree identity, Python/linter availability | Clean synchronized baseline `3dc8902`; exact ten-file/no-symlink package; Python `3.9.6`; dedicated Markdown linters unavailable | [`EVIDENCE-20260811T013701Z-codification-gap-analysis`](../EVIDENCE/EVIDENCE-20260811T013701Z-codification-gap-analysis.md) | No implementation existed or ran at this point |
| `2026-08-11T01:58:37Z` | `Codex/root` | `python3 scripts/validate_protocol.py`; `python3 -m unittest discover -s tests -v`; `python3 -m py_compile ...`; `git diff --check` | Corrected implementation passes: validator exit `0`; 20 tests exit `0`; compilation and whitespace checks exit `0` | Inline output; durable exact-target evidence will follow the implementation commit | Current Darwin/Python `3.9.6` only; no CommonMark claim |
| `2026-08-11T01:58:37Z` | `Codex/validator_audit` | Read-only adversarial pre-review of the uncommitted checker and tests | Found two HIGH, three MEDIUM, and one LOW implementation/harness gaps: fenced HANDOFF false structure, indented-list false pass, nested-code false violations, local-absolute link skip, traversal error classification, and missing CLI summary | Attributable agent report summarized here; follow-up requested after corrections | Preparatory audit only, not the required independent disposition |
| `2026-08-11T01:58:37Z` | `Codex/root` | Correct the audit findings and rerun the expanded suite | First post-refactor suite exited `1`: multiline masking replaced newline characters and caused a caught `IndexError`/tool exit `2` in one test. The newline-preserving correction then passed all 20 tests and repository validation. | Inline command output; regression cases retained in `tests/test_validate_protocol.py` | Discarded failing harness run is not a protocol failure or a pass; exact-target rerun remains pending |
| `2026-08-11T02:03:55Z` | `Codex/validator_audit` | First correction follow-up against all original findings | Original findings were resolved, but the audit found one new HIGH and two MEDIUM parser cases: inline code incorrectly crossing a blank block boundary, list-item fences misparsed as violations, and one-letter external URI schemes misclassified as drive paths | Attributable agent report and added regression cases | Preparatory audit only; no review disposition |
| `2026-08-11T02:03:55Z` | `Codex/root` | Block-aware inline masking, list-container fence handling, narrower drive-path recognition, and expanded regression suite | Validator exit `0`; all 21 tests pass; the three new cases now produce the intended violation/pass/pass results | Inline output and `tests/test_validate_protocol.py` | Full CommonMark remains out of scope; indented link-like syntax is conservatively unsupported |
| `2026-08-11T02:03:55Z` | `Codex/validator_audit` | Narrow final recheck of the three new findings | All three resolved; all 21 tests, repository validation, and `git diff --check` pass; no remaining HIGH or MEDIUM regression found in that bounded recheck | Attributable agent report | Still not the required independent review of an immutable target |
| `2026-08-11T02:03:55Z` | `Codex/root` | Initial combined pre-target shell harness | `NOT RUN`: execution layer rejected the command before process creation because temporary cleanup used a prohibited removal form; checks were rerun in smaller non-destructive commands | Direct tool rejection plus subsequent rows/commands | Rejection establishes neither pass nor repository failure |
| `2026-08-11T02:04:54Z` | `Codex/root` | Exact-target suite at `8690358d499aed20de6c620dc4dd4a81f1e1a126`: tests, compilation, validator, deterministic-output comparison, ranged whitespace/path review, package/Git-tree identity, governed-source digests, symlink and credential scans | All executed checks exit `0`: 21 tests pass; validator pass; target range is the declared seven paths; protocol tree unchanged at `4e79dd4`; package ten files/zero symlinks; governed hashes unchanged | [`EVIDENCE-20260811T020454Z-structural-validator-verification`](../EVIDENCE/EVIDENCE-20260811T020454Z-structural-validator-verification.md) | Dedicated Markdown linters unavailable; Darwin/Python `3.9.6`; no CommonMark or broader portability claim |
| `2026-08-11T02:09:11Z` | `Codex/root` | Post-record tests, validator, 39-file fence-aware structural link scan, HANDOFF structure/status, four-path review-handoff scope, governed-source exclusion, and `git diff --check` | Corrected run exits `0`: 21 tests pass; validator pass; 159 relative links/zero missing; five HANDOFF sections/one Next Action; exact four record paths; governed sources unchanged | Inline output plus verification evidence/HANDOFF | Preliminary path assertion exited `1` only because `git diff --name-only` omits untracked evidence; rerun used `git status --short` and passed |

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `2026-08-11T01:58:37Z`
- **Reviewed repository state:** Immutable implementation target `8690358d499aed20de6c620dc4dd4a81f1e1a126`, tree `3c55c49d9a9572ceb01c17d1369af8f90a2bbfe4`
- **Scope and authority references:** Root-only checker/tests/navigation against the accepted specification's tiny-helper allowance, `HARDEN-006`, accepted root-adoption ADR, and linked analysis
- **Checks and evidence reviewed:** Exact-target validator result, 21-test suite, compilation, deterministic output, ranged diff/whitespace, governed-source and package identities, credential/symlink scans, and both adversarial pre-review rounds
- **Findings and corrections:** Corrected the initial two HIGH/three MEDIUM/one LOW audit findings, the follow-up HIGH/two MEDIUM findings, and the intermediate newline-mask regression; the final narrow pre-review recheck found no remaining HIGH or MEDIUM regression
- **Limitations:** This issue requires independent review; implementor self-review and adversarial preparation cannot satisfy that gate. Dedicated Markdown linting and non-Darwin portability remain unavailable.
- **Residual risks:** False passes could incorrectly influence future compliance claims.
- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES` — the checker becomes an executable contract below the accepted Markdown authorities, and its over-automation boundary warrants fresh challenge before closure.

No independent review round has been recorded.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- The exact false-positive/false-negative boundary will remain limited to the supported syntax and tested environment.
- A fresh independent participant must verify that the executable slice does not redefine protocol semantics or cross into deferred runtime automation.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-11T01:37:01Z` | `Codex/root` | `NONE` | `OPEN` | Created the meaningful codification issue before implementation |
| `2026-08-11T01:37:01Z` | `Codex/root` | `OPEN` | `INVESTIGATING` | Completed repository recovery and bounded the candidate slice through linked evidence |
| `2026-08-11T01:44:13Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Began only the approved root-local checker, tests, and non-authoritative README navigation after committing analysis boundary `57c2746` |
| `2026-08-11T01:58:37Z` | `Codex/root` | `IMPLEMENTING` | `VERIFYING` | The bounded implementation and expanded regression suite pass after attributable pre-review corrections; exact-target evidence remains required |
| `2026-08-11T02:03:55Z` | `Codex/root` | `VERIFYING` | `VERIFYING` | Preserved follow-up findings and corrections additively; 21 tests and final bounded pre-review recheck pass |
| `2026-08-11T02:04:54Z` | `Codex/root` | `VERIFYING` | `REVIEW` | Committed immutable target `8690358`, reran exact-target validation successfully, and linked durable evidence; only fresh independent disposition can close the issue |
| `2026-08-11T02:09:11Z` | `Codex/root` | `REVIEW` | `REVIEW` | Preserved and corrected the untracked-path harness assumption; final review-handoff structural checks pass |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
