# Structural Protocol Validator

## Metadata

- **ID:** `ISSUE-20260811T013701Z-structural-protocol-validator`
- **Title:** Codify stable structural protocol invariants
- **Status:** `INVESTIGATING`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `AGENT`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-11T01:37:01Z`
- **Updated UTC:** `2026-08-11T01:37:01Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), especially Scope constraints, Quality bar, `HARDEN-003`, `HARDEN-006`, and hardening acceptance criterion 5
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md)
- **Evidence:** [`EVIDENCE-20260811T013701Z-codification-gap-analysis`](../EVIDENCE/EVIDENCE-20260811T013701Z-codification-gap-analysis.md)

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

- **Files or components:** Planned root-only `scripts/validate_protocol.py`, `tests/test_validate_protocol.py`, concise root README navigation, this issue, evidence, HANDOFF, and HUMAN_CHECKPOINT
- **Behavior changed:** Repository participants gain an optional repeatable structural check; reusable package behavior and adoption remain unchanged
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

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `NOT YET PERFORMED`
- **Reviewed repository state:** `NOT YET AVAILABLE`
- **Scope and authority references:** `NOT YET REVIEWED`
- **Checks and evidence reviewed:** `NOT YET REVIEWED`
- **Findings and corrections:** `NOT YET REVIEWED`
- **Limitations:** This issue requires independent review; implementor self-review will prepare but cannot satisfy that gate.
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

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [ ] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
