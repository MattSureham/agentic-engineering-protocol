# Structural Protocol Validator

## Metadata

- **ID:** `ISSUE-20260811T013701Z-structural-protocol-validator`
- **Title:** Codify stable structural protocol invariants
- **Status:** `CLOSED`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `AGENT`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-11T01:37:01Z`
- **Updated UTC:** `2026-08-11T03:01:36Z`
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

No independent review round has been persisted. On `2026-08-11T02:38:34Z` the human technical owner reported to the coordinator (`ClaudeCode/coordinator`) that the fresh independent review of immutable target `8690358d499aed20de6c620dc4dd4a81f1e1a126` completed with a disposition reported as "APPROVED WITH FINDINGS". The reviewer's complete round — reviewer identity, reviewed repository state, scope, commands or procedures, severity-ranked findings, limitations, residual risks, evidence, and one of the protocol dispositions `APPROVED`/`CHANGES_REQUIRED`/`BLOCKED` — has not been supplied to this record, and "APPROVED WITH FINDINGS" is not itself one of those dispositions. Per root [`BOOTSTRAP.md`](../BOOTSTRAP.md), a disposition reported outside the repository must be persisted in this owning artifact before any participant relies on it, and the closure checklist's independent-review item cannot be satisfied until the round is appended verbatim and any material findings are shown resolved or reclassified by the reviewer. This note records only the owner's report; it is not the review round and must not be treated as one.

### 2026-08-11T02:49:05Z — ClaudeCode/validator-review

This is the complete round whose completion the owner reported at `2026-08-11T02:38:34Z`, persisted by the reviewing participant without altering its conclusion.

- **Reviewed repository state:** Immutable target `8690358d499aed20de6c620dc4dd4a81f1e1a126` (tree `3c55c49d9a9572ceb01c17d1369af8f90a2bbfe4`), parent/analysis boundary `57c274641c1e779dbf95d36ed1ba0a03d7ef8fa7`, and post-target record-only commits `c89eb02f6ab685d5e6fb18090404ea145abd3ae2` and `ea2b63d0479c187b0619edddd015483eb579e7ec`. The review executed against a `git archive` extraction of the exact target in an isolated temporary directory, never against a mutated checkout; the live worktree stayed clean on `main`. The reviewer is a fresh participant instance with no authorship of the target (implementor `Codex/root`; preparatory audits `Codex/validator_audit`).
- **Scope:** The codification gap analysis, the complete validator implementation (`scripts/validate_protocol.py`), the complete test suite (`tests/test_validate_protocol.py`), the exact-target verification evidence, both HANDOFF revisions and the current one, the accepted specification and root-adoption ADR, the full target diff, and post-target drift scope.
- **Commands or procedures:** `git rev-parse` target/tree/parent and `8690358:protocol` identities; `git diff --name-status`/`--check` over `57c2746..8690358` and `8690358..ea2b63d`; `git archive 8690358 | tar -x` into an isolated temporary directory; `python3 scripts/validate_protocol.py` at the extracted target (exit `0`, exact output `PASS structural protocol validation (package_files=10 handoffs=2)`) run twice with byte-identical output; `python3 -m unittest discover -s tests` (21 tests, `OK`); `python3 -m py_compile` on both Python files; `shasum -a 256` of governed sources (`PROJECT_SPEC.md`, `BOOTSTRAP.md`, the accepted ADR, the runtime-automation issue) matching the evidence record; validator rerun against the live post-record worktree (exit `0`); `git ls-remote`/`rev-parse` remote equality at `ea2b63d`; HANDOFF section/Next Action/index inspection at the review boundary. All bytecode creation was suppressed; the isolated fixture was deleted afterward.
- **Specification compliance:** The implemented slice is exactly the analysis's "smallest useful executable slice": package manifest/file types, Markdown byte/fence integrity, supported relative-link resolution, and HANDOFF shape. No Classification A (judgment) or Classification C (future automation) item is implemented. The reusable package tree is unchanged (`4e79dd41eda4bac91329cf2fa8a88cd96bd168cb` at parent and target), preserving `HARDEN-006`. The `Authority: AGENT` classification is defensible: no new dependency, service, contract change, or specification/ADR contradiction; the specification's tiny-helper allowance and executable-contract tier cover optional root test tooling.
- **Correctness and regression findings:** No material finding. The 21-test suite covers manifest violations, symlink and non-regular entries, Markdown byte/fence invariants, broken/escaping/absolute/drive/file-URI links, unsupported-syntax exits, HANDOFF structural failures, determinism, and read-only behavior; all pass at the exact target under independent execution. The parser conservatively returns `UNSUPPORTED` (exit `2`) rather than passing ambiguous syntax.
- **Architecture and complexity findings:** The checker introduces no competing source of truth. It is a tier-3 executable contract subordinate to the Markdown authorities: read-only (proven by the before/after fixture snapshot test), standard-library only, no network or Git access, outside `protocol/`, not shipped to or required by adopters, and unable to close issues, approve work, or mutate state. Its normative constants (ten-file manifest, five HANDOFF sections, five snapshot-field labels) duplicate the Markdown authorities; the failure direction is loud, not silent redefinition (finding F2).
- **Material findings and resolution conditions:** `NONE` material. The five severity-ranked findings exactly as reported:

  | # | Severity | Finding |
  |---|---|---|
  | F1 | LOW | "Tiny helper" framing understates reality: 793-line checker + 365-line suite is the repository's largest executable artifact. Not a violation (single file, stdlib, `--root` is the entire CLI, complexity declared and test-covered), but it is a maintained component, not an incidental script. |
  | F2 | LOW | Normative constants are duplicated in code (ten-file manifest, five HANDOFF sections, five snapshot-field labels). If the Markdown authorities change those contracts, the validator goes stale. Failure direction is safe (loud), but the update obligation should travel with any such contract change. |
  | F3 | LOW | Mixed VIOLATION+UNSUPPORTED output exits `2` (documented as "inability to evaluate"), the same code as pure evaluator failure. Output lines stay accurate; only matters if automation ever consumes exit codes — none does. |
  | F4 | LOW | Codified checks cover only the package and the two HANDOFFs; root governing Markdown (BOOTSTRAP, spec, issues, evidence) still relies on one-off scans. Consistent with the approved slice; a future-slice candidate, not a defect. |
  | F5 | LOW | HANDOFF records "The owner authorized a bounded codification phase" as `CONFIRMED` without citing a discrete owner-direction record (contrast the timestamped 2026-08-07/2026-08-10 directions). Harmless because the issue stands on `AGENT` authority, but the provenance chain has a gap. |

  **Finding classification (per the recorded Next Action):** F1–F5 are accepted as residual risk/observations; none requires a durable issue or any change before closure. The review's non-binding suggestions — cite the owner codification direction (F5) and record the constants-update obligation (F2) in this issue's residual uncertainty — are carried into that section below.
- **Limitations:** The reviewer environment is the same Darwin/Python `3.9.6` class as the implementor's, so platform portability is unexamined by this round. The checker is not a CommonMark renderer and this review does not make it one. Repository-recorded identities are not cryptographically authenticated. The review ran in an isolated extraction; behavior was additionally confirmed once on the live worktree.
- **Residual risks:** A false pass could still influence future compliance claims (as the implementor's self-review noted); duplicated constants can drift from the Markdown authorities; root governing-Markdown link integrity remains a one-off check outside this slice.
- **Evidence:** This round's commands and outputs as listed; [`EVIDENCE-20260811T013701Z-codification-gap-analysis`](../EVIDENCE/EVIDENCE-20260811T013701Z-codification-gap-analysis.md); [`EVIDENCE-20260811T020454Z-structural-validator-verification`](../EVIDENCE/EVIDENCE-20260811T020454Z-structural-validator-verification.md); the Git objects cited above.
- **Disposition:** `APPROVED` — reported in session output as **APPROVED WITH FINDINGS**; because all five findings are LOW, non-material, and require no changes before closure, the protocol disposition is `APPROVED` with the findings recorded. The conclusion is unchanged by this persistence.
- **Prior-round resolution:** `FIRST ROUND` — the two `Codex/validator_audit` passes were implementor-side preparatory audits, not independent rounds; this is the first independent round.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- The exact false-positive/false-negative boundary will remain limited to the supported syntax and tested environment.
- A fresh independent participant must verify that the executable slice does not redefine protocol semantics or cross into deferred runtime automation.
- Independent review round 1 (`2026-08-11T02:49:05Z`) is `APPROVED` with five LOW findings accepted as residual risk. Two non-binding suggestions remain owned here: record the constants-update obligation whenever the Markdown authorities change the package manifest or HANDOFF contract (F2), and cite the owner codification-phase direction in a durable record if one exists (F5).

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
| `2026-08-11T02:38:34Z` | `ClaudeCode/coordinator` | `REVIEW` | `REVIEW` | Recorded the owner-reported "APPROVED WITH FINDINGS" disposition as persistence-pending; the verbatim review round and finding classification remain required before closure; no implementation change authorized or made |
| `2026-08-11T02:49:05Z` | `ClaudeCode/validator-review` | `REVIEW` | `REVIEW` | Persisted the complete independent round unchanged: protocol disposition `APPROVED` (reported as "APPROVED WITH FINDINGS"), five LOW findings classified as accepted residual risk; closure decision left to a coordinator per the recorded gate; no implementation change |
| `2026-08-11T03:01:36Z` | `ClaudeCode/coordinator` | `REVIEW` | `CLOSED` | Coordinator closure verification passed: reproduced target tree `3c55c49d9a9572ceb01c17d1369af8f90a2bbfe4`, parent `57c274641c1e779dbf95d36ed1ba0a03d7ef8fa7`, and protocol subtree `4e79dd41eda4bac91329cf2fa8a88cd96bd168cb`; confirmed post-target drift is record-only (evidence, HANDOFF, checkpoint, issue paths); reran the validator (exit `0`) and 21 tests (`OK`); confirmed the round is schema-complete, the reviewer is independent of the implementor, the `APPROVED` mapping preserves the session label verbatim, and no material finding exists; recorded the session-vocabulary friction separately as `ISSUE-20260811T030136Z-review-disposition-vocabulary` (`OPEN`, `LOW`, owner-gated) |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies (not applicable — `Review: INDEPENDENT`).
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved (round 1 of `2026-08-11T02:49:05Z` by `ClaudeCode/validator-review`; no material finding existed).
- [x] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
