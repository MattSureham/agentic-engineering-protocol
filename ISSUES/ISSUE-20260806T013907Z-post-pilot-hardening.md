# Post-Pilot Hardening and Root Dogfooding

## Metadata

- **ID:** `ISSUE-20260806T013907Z-post-pilot-hardening`
- **Title:** Separate root governance, operational continuity, and durable records
- **Status:** `CLOSED`
- **Severity:** `HIGH`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-06T03:02:04Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), including the owner-approved post-pilot hardening requirements to be recorded
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md)
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md); [`EVIDENCE-20260806T020056Z-hardening-validation`](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md)

## Problem

The repository does not yet dogfood the protocol it publishes. Root source-of-truth wording conflicts with the reusable hierarchy; root HANDOFF mixes a current snapshot with closed issue bodies, terminal task history, extensive evidence narrative, and diary history; and original pilot behavior is not reproducible from this repository alone.

## Evidence or reproduction

The linked audit records exact file statements, line counts, digests, Git-object checks, and external-path limitations. Baseline `e6beeb2cb730183ca2ac13795ad367ad9d9e1099` is synchronized with `origin/main`.

## Expected behavior

- Root governance follows the seven-tier precedence in the accepted adoption ADR.
- HANDOFF remains a compact operational index with explicit snapshot/staleness metadata.
- Requirements, accepted architecture, issue lifecycle, and evidence have separate durable records.
- The exact approved specification-evolution policy governs root `PROJECT_SPEC.md`.
- Pilot evidence states clone-based reproducibility limits without fabricating evidence.
- Five future capability areas remain blocked pending separately approved scope.
- Independent review approves an immutable target before closure or a maturity claim.

## Assumptions

- **CONFIRMED:** The human owner approved the complete hardening architecture and non-goals.
- **CONFIRMED:** The package must remain Markdown-first, runtime-agnostic, and exactly ten files.
- **INFERRED:** Existing historical records can be preserved through Git identity plus migrated issue/evidence files while the live HANDOFF is compacted.
- **UNKNOWN:** Independent review outcome and portability outside already tested environments.

## Investigation and decision

The verified findings are classified as follows:

| Classification | Finding |
|---|---|
| Must fix before maturity | Split root truth ownership; overloaded live HANDOFF; pilot evidence dependent on absent Git objects and local paths |
| Should improve now | Root specification evolution; reusable snapshot/staleness rules; consistent root records |
| Future separate scope | Concurrency guarantees; authenticated identity/approval; runtime automation; large-scale coordination; tracker integration |

The accepted ADR owns the root-adoption architecture. This issue owns implementation lifecycle only.

## Change

- **Files or components:** Root `BOOTSTRAP.md`, `PROJECT_SPEC.md`, `README.md`, `HANDOFF.md`, `HUMAN_CHECKPOINT.md`, `PILOT_EVIDENCE.md`, and templates/records under `ADR/`, `ISSUES/`, and `EVIDENCE/`; reusable `protocol/BOOTSTRAP.md` and `protocol/HANDOFF.md`.
- **Behavior changed:** Root governance now uses the accepted seven-tier hierarchy and separate root/product instances. At the immutable target, root HANDOFF is a 248-line operational index with metadata/staleness rules, unresolved issues only, no terminal task ledger, one next action, 15 recent entries, and a nonempty archive. Durable decision/lifecycle/evidence history lives in owning records. The reusable HANDOFF contract now requires the same snapshot reliability behavior.
- **Out-of-scope work deliberately excluded:** Runtime/orchestrator, daemon/service, database, complex CLI, external issue tracker, concurrent-writer guarantee, cryptographic authentication, large-scale coordination.
- **Rollback or recovery:** Inspect or restore the pre-hardening state from Git revision `e6beeb2cb730183ca2ac13795ad367ad9d9e1099`; do not erase the issue/ADR/evidence trail.
- **Immutable implementation target:** Commit `5eceae0f7d45fdcbe0fad7a7aa965a16e0e537fb`; parent/authority boundary `7dea5457828b6590f9ab2a643b58047b032e53d1`; full tree `3d718626b361535a7086a45fae868e69a7da9196`; protocol tree `4e79dd41eda4bac91329cf2fa8a88cd96bd168cb` (parent protocol tree `8676b85d292676b7e198d10414961bf3657bf578`).

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Separate root and package governance | Prevent silent authority coupling | Accepted ADR and semantic validation | Future drift remains review-dependent |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-06T02:00:56Z` | `Codex/root` | Corrected standard-library Markdown/semantic suite | `PASS`, exit `0`: 33 Markdown files, 94 relative links/zero missing, ten package files/zero symlinks, seven tiers, exact policy match, two scoped package edits, pilot bytes preserved | [Validation evidence](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md) | Structural/fence-aware, not complete CommonMark |
| `2026-08-06T02:00:56Z` | `Codex/root` | Legacy issue extraction comparison against `git show 7dea545:HANDOFF.md` | `PASS`, exit `0`: five of five issue bodies byte-match | [Validation evidence](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md) | Immutable source is Git-dependent by design |
| `2026-08-06T02:00:56Z` | `Codex/root` | Isolated `protocol/` copy, `diff -qr`, manifest/link/entrypoint checks | `PASS`, exit `0`: 10 files, 23 links/zero missing | [Validation evidence](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md) | One Darwin/filesystem run; fixture not durable |
| `2026-08-06T02:00:56Z` | `Codex/root` | `command -v` availability query | `markdownlint`, `markdownlint-cli2`, and `shellcheck` `NOT_AVAILABLE` | [Validation evidence](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md) | Not counted as passed checks |
| `2026-08-06T02:05:56Z` | `Codex/root` | Complete post-record semantic/Markdown suite plus `git diff --check` | `PASS`, exit `0`: 34 Markdown files/105 links, ten package files/zero symlinks, HANDOFF contract, exact policy, seven tiers, pilot and five legacy bodies | [Validation evidence](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md) | One syntax-error harness attempt produced no result and is explicitly discarded; independent review still pending |
| `2026-08-06T02:09:38Z` | `Codex/root` | Exact-target checker at `5eceae0f7d45fdcbe0fad7a7aa965a16e0e537fb` plus `git diff --check 7dea545..5eceae0` | `IMMUTABLE_TARGET_PASS`, exit `0`: clean checkout equals target; 34 Markdown files/106 links/zero missing; ten package files/zero symlinks; five-section/one-action HANDOFF; exact policy; pilot/five legacy bodies | This issue row and review HANDOFF preserve the post-target observation | First checker invocation stopped at the same reporting f-string syntax error and supplied no result; corrected full rerun passed; independent review still pending |

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `2026-08-06T02:00:56Z`
- **Reviewed repository state:** Authority parent `7dea5457828b6590f9ab2a643b58047b032e53d1` plus uncommitted candidate hashes in validation evidence
- **Scope and authority references:** All approved hardening paths; `HARDEN-001` through `HARDEN-008`; accepted root-adoption ADR
- **Checks and evidence reviewed:** Full diff/scope; semantic/Markdown suite; historical byte preservation; isolated copy; explicit deferrals and unavailable tools
- **Findings and corrections:** One validator-only capitalization assumption was corrected and the complete suite reran to pass. No material candidate finding remains in self-review.
- **Limitations:** Self-review cannot establish independence; no dedicated Markdown linter; no broader pilot/portability/concurrency/identity/scale validation.
- **Residual risks:** Participant compliance and future root/product semantic drift require judgment; independent disposition remains unknown.
- **Outcome:** `COMPLETE` as preparatory self-review only; independent review remains mandatory for closure

## Independent review rounds

- **Required:** `YES` — root governance and the reusable HANDOFF contract change.

### 2026-08-06T03:02:04Z — ClaudeCode/hardening-review

- **Reviewed repository state:** Immutable target `5eceae0f7d45fdcbe0fad7a7aa965a16e0e537fb` (tree `3d718626b361535a7086a45fae868e69a7da9196`, protocol tree `4e79dd41eda4bac91329cf2fa8a88cd96bd168cb`), parent/authority boundary `7dea5457828b6590f9ab2a643b58047b032e53d1`, plus post-target record-keeping commits `fad48a1a7c35a1aba4f2943430603d92df628cd0` (HANDOFF + this issue only) and `bee42f788c77c51fea62e7e74f4fbdd7f5b3084f` (HANDOFF only), clean worktree on `main`.
- **Scope:** Root `BOOTSTRAP.md`, `PROJECT_SPEC.md`, `README.md`, `HANDOFF.md` (target revision), `HUMAN_CHECKPOINT.md`, `PILOT_EVIDENCE.md`, accepted ADR, all root templates, the five migrated legacy issue files, one blocked deferral issue, both evidence records, the complete ranged diff, and both reusable package diffs. This reviewer is a fresh participant instance with no implementation involvement; all checks below were executed independently rather than inherited from the implementor's narrative.
- **Commands or procedures:** `git rev-parse` target/tree/parent/protocol-tree identity; `git diff --stat`/`--name-only`/`--check` over `7dea545..5eceae0` and both post-target ranges; `git show e6beeb2:PILOT_EVIDENCE.md | shasum -a 256` against the migrated evidence file; awk-based byte extraction of all five legacy issue bodies from `git show 7dea545:HANDOFF.md` compared to the migrated files; `sed`/`diff` exact comparison of the specification-evolution policy between root and reusable specifications; a standard-library relative-link scan over every Markdown file outside `.git`; `find` package inventory and symlink count; isolated `cp -R protocol/` copy with `diff -qr`; `git cat-file -e` for both recorded pilot commits; `shasum -a 256` of `git show 7dea545:HANDOFF.md` and `git show 7dea545:EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md`; `git rev-parse 7dea545:...audit.md` blob identity; target HANDOFF heading/line/entry counts.
- **Specification compliance:** `HARDEN-001` root adoption verified — the root BOOTSTRAP seven-tier precedence matches ADR decision 2 exactly. `HARDEN-002` separate governance verified — root and reusable BOOTSTRAP differ intentionally and cross-reference the divergence rule. `HARDEN-003` verified — target HANDOFF has exactly the five ordered sections, snapshot metadata with staleness triggers, six unresolved-only issue rows, no terminal task ledger, one Next Action, 248 lines, and a nonempty archive. `HARDEN-004` verified — durable records exist in owning directories; checkpoint declares itself non-authoritative. `HARDEN-005` verified — pilot bytes SHA-256 `dab1274cb74d62ec263fdb0acb86591d74f3d79efd4891e2140c08f9e314651f` match the pre-hardening blob; the compatibility pointer resolves; both recorded pilot commits return exit `128` from `git cat-file -e`, matching the audit's absence claim; no reproducibility claim exceeds this. `HARDEN-006` verified — ten regular package files, zero symlinks, isolated copy byte-identical, exactly two package paths changed with snapshot/staleness semantics compatible with the root rules. `HARDEN-007` — this round is the required fresh independent disposition. `HARDEN-008` verified — all five legacy bodies byte-match their `7dea545` extractions (8/10/10/34/47 lines, matching the validation evidence); the pre-compaction HANDOFF digest `884a69a2fc99ceddd7840be87135ef2ee5ed5ad4647d9566a2d90c81020c6a4e` and the audit blob `615c790050b8abb99d0c29399e28193bb8db3dd8`/SHA-256 `af011e0bdf961920362b9d18ca925e2be6a71fef4740f5480e2eef1f79d9ffc0` both reproduce. Acceptance criteria 1–7 are each satisfied by directly reproduced observations.
- **Correctness and regression findings:** No content loss detected in any migration. The ranged diff touches exactly the declared change set (20 paths). `git diff --check` exits `0`. The one edit to a pre-existing evidence file completes that file's own forward-declared digest placeholder and preserves the superseded version immutably at the authority boundary; this is additive provenance, not a silent rewrite. The reusable diffs add snapshot/staleness rules without altering existing authority, lifecycle, or review semantics.
- **Architecture and complexity findings:** The only new architectural cost is separate root/product governance, covered by the accepted ADR with its residual-drift gap explicitly owned. No runtime, dependency, or new abstraction was introduced; all five deferred capabilities remain `BLOCKED` with observable owner-gated unblock conditions.
- **Material findings and resolution conditions:** `NONE`. One non-material observation: root `HUMAN_CHECKPOINT.md` (generated `2026-08-06T02:00:56Z`) still describes the candidate as uncommitted even though the target was committed at `2026-08-06T02:09:38Z`; the checkpoint is explicitly non-authoritative and names this independent disposition as its own regeneration trigger, so this is a bounded staleness note, not a defect. A separate apparent missing link (`PROTOCOL_GUIDE.md` from `protocol/README.md`) was traced to an indented fenced snippet illustrating a target repository's navigation block, where that file exists by construction; it is not a package link defect.
- **Limitations:** No dedicated Markdown linter (`markdownlint`, `markdownlint-cli2`) or `shellcheck` is installed in this environment; structural checks are fence-aware but not a CommonMark renderer. Reviewer environment is the same Darwin host class as the implementor's, so platform-portability claims remain unexamined by this round. Repository-recorded identities are not cryptographically authenticated. Semantic judgments (e.g., what counts as material divergence) cannot be mechanically proven.
- **Residual risks:** Future root/product semantic drift remains review-dependent; participant compliance with the compact-HANDOFF contract is a behavioral risk no document can eliminate; broader portability, concurrency, identity, and scale remain correctly unclaimed.
- **Evidence:** This round's commands and outputs; [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md); [`EVIDENCE-20260806T020056Z-hardening-validation`](../EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md); Git objects cited above.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** `FIRST ROUND` — no earlier independent round exists; the implementor's self-review is preparatory only and was not relied upon.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Broader portability beyond the tested Darwin/POSIX environment and future participant compliance remain unknown; both are explicitly unclaimed. The independent review gate is satisfied as of `2026-08-06T03:02:04Z`.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `INVESTIGATING` | Recovered clean synchronized baseline and verified findings from repository evidence |
| `2026-08-06T01:39:07Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Human-approved architecture and accepted ADR authorize bounded hardening |
| `2026-08-06T02:00:56Z` | `Codex/root` | `IMPLEMENTING` | `VERIFYING` | Root/product governance, durable migration, and reusable snapshot changes are implemented; initial corrected validation passed |
| `2026-08-06T02:09:38Z` | `Codex/root` | `VERIFYING` | `REVIEW` | Immutable target `5eceae0f7d45fdcbe0fad7a7aa965a16e0e537fb` passed implementor verification; fresh independent approval is the remaining closure gate |
| `2026-08-06T03:02:04Z` | `ClaudeCode/hardening-review` | `REVIEW` | `CLOSED` | Fresh independent review round 1 returned `APPROVED` with no material findings; every closure-checklist item is satisfied and recorded verification plus required review exist |

## Closure checklist

- [x] Expected behavior is tied to owner-approved requirements and an accepted ADR.
- [x] The change or resolution is recorded.
- [x] Required implementor verification ran and evidence is linked; unavailable checks remain explicit.
- [x] The latest independent review round is `APPROVED` and prior material findings are resolved.
- [x] Human authority is recorded in the accepted ADR and HANDOFF authorization boundary.
- [x] New complexity is covered, removed, or linked to accepted open debt.
- [x] Residual uncertainty is explicitly owned.
- [x] HANDOFF reflects the immutable target and exactly one independent-review action.
