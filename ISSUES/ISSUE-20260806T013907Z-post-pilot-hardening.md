# Post-Pilot Hardening and Root Dogfooding

## Metadata

- **ID:** `ISSUE-20260806T013907Z-post-pilot-hardening`
- **Title:** Separate root governance, operational continuity, and durable records
- **Status:** `REVIEW`
- **Severity:** `HIGH`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-06T02:09:38Z`
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

No round has been recorded.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Independent disposition, broader portability, and participant compliance remain unknown.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `INVESTIGATING` | Recovered clean synchronized baseline and verified findings from repository evidence |
| `2026-08-06T01:39:07Z` | `Codex/root` | `INVESTIGATING` | `IMPLEMENTING` | Human-approved architecture and accepted ADR authorize bounded hardening |
| `2026-08-06T02:00:56Z` | `Codex/root` | `IMPLEMENTING` | `VERIFYING` | Root/product governance, durable migration, and reusable snapshot changes are implemented; initial corrected validation passed |
| `2026-08-06T02:09:38Z` | `Codex/root` | `VERIFYING` | `REVIEW` | Immutable target `5eceae0f7d45fdcbe0fad7a7aa965a16e0e537fb` passed implementor verification; fresh independent approval is the remaining closure gate |

## Closure checklist

- [x] Expected behavior is tied to owner-approved requirements and an accepted ADR.
- [x] The change or resolution is recorded.
- [x] Required implementor verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] The latest independent review round is `APPROVED` and prior material findings are resolved.
- [x] Human authority is recorded in the accepted ADR and HANDOFF authorization boundary.
- [x] New complexity is covered, removed, or linked to accepted open debt.
- [x] Residual uncertainty is explicitly owned.
- [x] HANDOFF reflects the immutable target and exactly one independent-review action.
