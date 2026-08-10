# Issue — Accepted ADR Review Record Does Not Match Hardening Closure

## Metadata

- **ID:** `ISSUE-20260810T060455Z-adr-review-record-mismatch`
- **Title:** Accepted ADR review record does not match hardening closure
- **Status:** `BLOCKED`
- **Severity:** `MEDIUM`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-08-10T06:04:55Z`
- **Updated UTC:** `2026-08-10T06:12:48Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `HARDEN-003`, `HARDEN-004`, `HARDEN-007`, hardening acceptance criteria 1 and 7, and Specification governance
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md) (`ACCEPTED`; affected record, not modified)
- **Evidence:** Inline repository and Git observations below; no separate evidence file

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The accepted root-adoption ADR requires independent review but still states, "No review round has been recorded." The related hardening issue is `CLOSED` and contains an independent review round with disposition `APPROVED`; that round names the accepted ADR in its review scope. Lower-precedence operational records consequently describe the root adoption and hardening as independently approved.

These facts leave one unresolved governance question: whether the hardening issue's review round satisfies the ADR's own required review gate, or whether the ADR requires a distinct review record or an explicitly accepted exception. The records cannot answer that question consistently as written.

## Evidence or reproduction

At published baseline `9f4bd8f529b5b250b20e8142bb9d9321f5cbc13d`:

| Artifact or procedure | Observed result |
|---|---|
| [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md), **Independent review rounds** | Says review is required and "No review round has been recorded." Git history shows the ADR has not changed since its creation in `7dea5457828b6590f9ab2a643b58047b032e53d1`. |
| [`ISSUE-20260806T013907Z-post-pilot-hardening`](ISSUE-20260806T013907Z-post-pilot-hardening.md), **Independent review rounds** | Records a `2026-08-06T03:02:04Z` independent round by `ClaudeCode/hardening-review`, explicitly includes the accepted ADR in scope, and gives disposition `APPROVED`. The issue then transitions from `REVIEW` to `CLOSED`. |
| Root [`HANDOFF.md`](../HANDOFF.md) | Describes the hardening/root adoption review gate as satisfied while remaining lower-precedence operational continuity. |
| Root [`HUMAN_CHECKPOINT.md`](../HUMAN_CHECKPOINT.md) | Describes the accepted root adoption as independently approved while remaining a non-authoritative owner summary. |
| Search of `ISSUES/`, `HANDOFF.md`, `HUMAN_CHECKPOINT.md`, and the ADR | Found no existing issue that owns this exact review-record mismatch. |

The ADR's SHA-256 at discovery was `f3c49151ddf4e9a96737b64252aebe70cfa0dc96f0245cf966d7eba339ec18d5`. Preserve this identity until the owner authorizes a separate resolution.

## Expected behavior

Root [`BOOTSTRAP.md`](../BOOTSTRAP.md) requires source conflicts to remain visible in an issue and requires human technical-owner approval before contradicting an accepted ADR or changing a required governance gate. Root `PROJECT_SPEC.md` requires evidence-backed, attributable correction and a fresh independent approval before a maturity claim. Lower-precedence issue, HANDOFF, and checkpoint statements must not be used to silently reinterpret the accepted ADR.

## Assumptions

- **CONFIRMED:** The ADR text and the hardening issue review record differ as described above at baseline `9f4bd8f529b5b250b20e8142bb9d9321f5cbc13d`.
- **CONFIRMED:** The human technical owner authorized recording this inconsistency but explicitly prohibited modifying the ADR or resolving the inconsistency in this change.
- **INFERRED:** The mismatch concerns review-record ownership or sufficiency, not proof that the independent review itself failed to occur; the hardening issue contains a complete attributable round.
- **UNKNOWN:** Whether the existing hardening review satisfies the ADR's required review gate. Only the owner decision below can establish the authorized interpretation.

## Investigation and decision

No correction is adopted. Interpreting or changing an accepted ADR's review requirement crosses the Human Authority Boundary, and the current authorization is limited to evidence-first issue recording and operational indexing.

The human technical owner must select one disposition:

1. Decide that the existing hardening review satisfies the ADR's review gate and authorize a separate reconciliation of the affected records.
2. Require a fresh, ADR-specific independent review before any reconciliation or maturity claim.
3. Keep the mismatch as accepted open debt, with an explicit rationale and boundaries on any maturity claim.

## Change

- **Files or components:** This issue; root `HANDOFF.md` unresolved index/snapshot/next action/activity; root `HUMAN_CHECKPOINT.md` decision queue.
- **Behavior changed:** None. The inconsistency is made durable and owner-visible; no source-of-truth artifact is reinterpreted or corrected.
- **Out-of-scope work deliberately excluded:** Any modification to the accepted ADR, root specification, root or reusable BOOTSTRAP, reusable package, evidence records, implementation, existing issue states, or maturity claim.
- **Rollback or recovery:** Revert this record-only commit. No product behavior or external state is changed by the records themselves.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| `NONE` | Record-only conflict tracking; no abstraction, dependency, state, process, or coupling introduced | This issue plus required HANDOFF/checkpoint indexes | This issue remains `BLOCKED` until owner disposition |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-10T06:07:54Z` | `Codex/root` | Baseline status, hashes, Git history, direct remote ref, and repository-text search | Baseline clean and synchronized at `9f4bd8f`; contradiction reproduced; no covering issue found; exit `0` | Inline observations above | Review sufficiency is intentionally not inferred |
| `2026-08-10T06:12:48Z` | `Codex/root` | Exact changed-path comparison; SHA-256 checks for the ADR, root specification, and root BOOTSTRAP; protocol Git-tree comparison; repository-wide fence-aware relative-link/final-newline/fence scan; HANDOFF structure/count checks; `git diff --check` | All assertions passed, exit `0`: exactly three approved paths; governing sources unchanged; 36 Markdown files with resolved links, balanced fences, and final newlines; five HANDOFF sections, one Next Action, seven unresolved rows, 21 recent entries | Inline command output summarized here and in HANDOFF activity | Dedicated `markdownlint` executable is `NOT AVAILABLE`; structural checks are not a CommonMark renderer |

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `2026-08-10T06:12:48Z`
- **Reviewed repository state:** Published baseline `9f4bd8f529b5b250b20e8142bb9d9321f5cbc13d` plus the record-only working-tree diff
- **Scope and authority references:** This issue, HANDOFF, and HUMAN_CHECKPOINT only; root BOOTSTRAP conflict handling and Human Authority Boundary; `HARDEN-003`, `HARDEN-004`, and `HARDEN-007`
- **Checks and evidence reviewed:** Both verification rows above; exact diff and source hashes; issue metadata, blocker, decision options, and index/checkpoint wording
- **Findings and corrections:** Corrected one checkpoint table cell that still characterized the accepted ADR itself as independently approved; it now distinguishes owner approval from the unresolved review-record interpretation. No other finding remained.
- **Limitations:** Self-review establishes only accurate issue creation and indexing; it cannot decide whether the prior review satisfies the accepted ADR
- **Residual risks:** The governance record remains inconsistent until the human owner selects a disposition and any separately authorized follow-up completes
- **Outcome:** `COMPLETE` for the record-only creation and indexing change; the owner-gated inconsistency remains unresolved by design

## Independent review rounds

- **Required:** `NO` — this change only records and indexes an existing conflict without changing governance, product behavior, contracts, dependencies, state, trust, concurrency, or architecture. Any later ADR reconciliation or ADR-specific review is separate meaningful work with its own authority and review gate.

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** No authorized interpretation of whether the hardening issue's independent review satisfies the accepted ADR's review requirement.
- **Unblock owner:** Human technical owner (`MattSureham`)
- **Unblock condition:** A durable owner decision selects disposition 1, 2, or 3 above and authorizes any resulting follow-up scope.

## Residual uncertainty

- Whether the existing hardening review satisfies the ADR review gate; owned by the human technical owner.
- Whether any later reconciliation requires editing the ADR, adding a distinct review round elsewhere, or retaining explicit debt; determined only after the owner disposition.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-10T06:04:55Z` | `Codex/root` | `NONE` | `OPEN` | Confirmed the ADR/hardening-issue mismatch and found no existing owning issue; owner authorized a record-only issue and prohibited immediate resolution |
| `2026-08-10T06:07:54Z` | `Codex/root` | `OPEN` | `BLOCKED` | Review-gate interpretation requires a human owner disposition; no ADR correction is authorized |

## Closure checklist

- [x] Expected behavior is tied to higher-authority sources.
- [x] The conflict and decision required are recorded without adopting a resolution.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [x] If `Review: INDEPENDENT`, the latest review round requirement is not applicable to this record-only change.
- [ ] Required human authority is recorded for the eventual disposition.
- [x] New complexity is absent.
- [x] Residual uncertainty is explicitly owned.
- [x] HANDOFF reflects the blocked issue and exactly one next action.
