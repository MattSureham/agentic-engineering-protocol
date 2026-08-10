# Issue — Accepted ADR Review Record Does Not Match Hardening Closure

## Metadata

- **ID:** `ISSUE-20260810T060455Z-adr-review-record-mismatch`
- **Title:** Accepted ADR review record does not match hardening closure
- **Status:** `CLOSED`
- **Severity:** `MEDIUM`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-08-10T06:04:55Z`
- **Updated UTC:** `2026-08-10T07:32:36Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `HARDEN-003`, `HARDEN-004`, `HARDEN-007`, hardening acceptance criteria 1 and 7, and Specification governance
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md) (`ACCEPTED`; additively clarified by the owner disposition recorded here)
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

### 2026-08-10T07:25:05Z — Owner disposition

Human technical owner `MattSureham` selected disposition 1. The independent review recorded on `2026-08-06T03:02:04Z` in [`ISSUE-20260806T013907Z-post-pilot-hardening`](ISSUE-20260806T013907Z-post-pilot-hardening.md) satisfies the substantive independent-review intent of the accepted ADR. The ADR's statement that no review round had been recorded is a historical statement that was true at acceptance time, not a perpetual unresolved gate.

The owner authorized the smallest attributable ADR status clarification, with the original statement and rationale retained. No fresh ADR-specific review is required because the clarification does not change the architectural decision. This decision authorizes record reconciliation only; it does not broaden any maturity, production-readiness, portability, concurrency, identity, or scale claim.

## Change

- **Files or components:** This issue; root `HANDOFF.md` unresolved index/snapshot/next action/activity; root `HUMAN_CHECKPOINT.md` decision queue.
- **Behavior changed:** None. The inconsistency is made durable and owner-visible; no source-of-truth artifact is reinterpreted or corrected.
- **Out-of-scope work deliberately excluded:** Any modification to the accepted ADR, root specification, root or reusable BOOTSTRAP, reusable package, evidence records, implementation, existing issue states, or maturity claim.
- **Rollback or recovery:** Revert this record-only commit. No product behavior or external state is changed by the records themselves.

## Resolution change

- **Files or components:** Additive status clarification in the accepted ADR; this issue's owner disposition and lifecycle; root HANDOFF and HUMAN_CHECKPOINT reconciliation.
- **Behavior changed:** The review-gate interpretation changes from `UNKNOWN` to owner-confirmed satisfaction. The ADR's architecture, rationale, status, and original historical text remain unchanged.
- **Out-of-scope work deliberately excluded:** Root specification, root BOOTSTRAP, reusable protocol, evidence bodies, implementation, and all unrelated issue states.
- **Rollback or recovery:** Revert the reconciliation commit to restore the blocked record state; the original ADR and review evidence remain recoverable from Git either way.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| `NONE` | Record-only conflict tracking; no abstraction, dependency, state, process, or coupling introduced | This issue plus required HANDOFF/checkpoint indexes | This issue remains `BLOCKED` until owner disposition |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-10T06:07:54Z` | `Codex/root` | Baseline status, hashes, Git history, direct remote ref, and repository-text search | Baseline clean and synchronized at `9f4bd8f`; contradiction reproduced; no covering issue found; exit `0` | Inline observations above | Review sufficiency is intentionally not inferred |
| `2026-08-10T06:12:48Z` | `Codex/root` | Exact changed-path comparison; SHA-256 checks for the ADR, root specification, and root BOOTSTRAP; protocol Git-tree comparison; repository-wide fence-aware relative-link/final-newline/fence scan; HANDOFF structure/count checks; `git diff --check` | All assertions passed, exit `0`: exactly three approved paths; governing sources unchanged; 36 Markdown files with resolved links, balanced fences, and final newlines; five HANDOFF sections, one Next Action, seven unresolved rows, 21 recent entries | Inline command output summarized here and in HANDOFF activity | Dedicated `markdownlint` executable is `NOT AVAILABLE`; structural checks are not a CommonMark renderer |
| `2026-08-10T07:29:35Z` | `Codex/root` | Preliminary combined reconciliation validator | Exit `1` before a semantic disposition: the checker mixed byte offsets with Unicode string indices and searched lifecycle rows without accounting for Markdown backticks | Direct terminal observation; corrected full rerun follows | Discarded harness result; it does not establish a repository failure or pass |
| `2026-08-10T07:29:35Z` | `Codex/root` | Corrected full reconciliation validator: exact four-path scope; unchanged root BOOTSTRAP/specification/evidence/protocol; ADR additive-history and status checks; review target/disposition/evidence checks; repository-wide links/newlines/fences; HANDOFF structure; lifecycle/blocker checks; `git diff --check` | All assertions passed, exit `0`: ADR historical lines preserved in order, seven additions/zero deletions, status `ACCEPTED`; target and evidence present; 36 Markdown files valid under structural checker; five HANDOFF sections, one action, seven preclosure rows, nonempty archive; lifecycle through `VERIFYING` valid | Inline command output and this row | Dedicated `markdownlint` is `NOT AVAILABLE`; structural checker is not a CommonMark renderer; publication remains self-referential until committed and pushed |
| `2026-08-10T07:32:36Z` | `Codex/root` | Final post-closure rerun of the corrected validator | All assertions passed, exit `0`: exact four paths; governed sources unchanged; ADR history/additive diff/status valid; review and evidence durable; 36 Markdown files structurally valid; HANDOFF five sections/one action/six unresolved rows/22 recent entries/nonempty archive; issue `CLOSED` with complete lifecycle, satisfied blocker, complete checklist; checkpoint in terminal owner-wait state | Inline command output summarized in HANDOFF | Dedicated `markdownlint` remains `NOT AVAILABLE`; commit and push still require verification |

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

### 2026-08-10T07:29:35Z — Resolution follow-up

- **Participant:** `Codex/root`
- **Reviewed repository state:** Published baseline `8d9756a6c90dd46f4035f46563b1b352c67eddd2` plus the exact four-file reconciliation diff
- **Scope and authority references:** Owner disposition recorded above; additive ADR status clarification; root BOOTSTRAP conflict, authority, review, evidence, and HANDOFF rules; `HARDEN-003`, `HARDEN-004`, and `HARDEN-007`
- **Checks and evidence reviewed:** All four verification rows; exact ADR additions/deletions and historical-line subsequence; cited review target, `APPROVED` disposition, and durable evidence; governing-source identities; issue lifecycle; HANDOFF/checkpoint state
- **Findings and corrections:** The first combined validator contained two harness assumptions and was discarded explicitly; the corrected full rerun passed. No content correction or material finding remained.
- **Limitations:** No dedicated Markdown linter or CommonMark renderer; commit and remote identity cannot be embedded in their own containing commit and must be verified on resumption
- **Residual risks:** No unresolved risk for this record mismatch. Existing broader portability, concurrency, identity, scale, and participant-compliance limits remain unchanged and unclaimed.
- **Outcome:** `COMPLETE` — owner authority, additive reconciliation, verification, and self-review satisfy closure; no fresh independent review is required because the architectural decision is unchanged

## Independent review rounds

- **Required:** `NO` — this change only records and indexes an existing conflict without changing governance, product behavior, contracts, dependencies, state, trust, concurrency, or architecture. Any later ADR reconciliation or ADR-specific review is separate meaningful work with its own authority and review gate.

The human technical owner's `2026-08-10T07:25:05Z` disposition confirms that this additive reconciliation is not an architectural change and requires no fresh ADR-specific review. A later change to the decision itself remains independently review-gated.

## Blocker

- **Blocked from:** `NOT BLOCKED` — historical blocked-from state was `OPEN`
- **Blocker:** `NONE` — the owner selected disposition 1 on `2026-08-10T07:25:05Z`
- **Unblock owner:** Human technical owner (`MattSureham`), fulfilled
- **Unblock condition:** `SATISFIED` — the owner determined that the existing hardening review satisfies the ADR review intent and authorized additive reconciliation

## Residual uncertainty

- **RESOLVED `2026-08-10T07:25:05Z`:** The existing hardening review satisfies the ADR review gate; determined by the human technical owner.
- **RESOLVED `2026-08-10T07:25:05Z`:** Reconciliation uses an additive ADR status clarification; no distinct review round or accepted debt is required because the architecture is unchanged.
- **Remaining limitation:** The clarification does not establish any broader maturity, production-readiness, portability, concurrency, identity, or scale claim beyond the existing hardening evidence.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-10T06:04:55Z` | `Codex/root` | `NONE` | `OPEN` | Confirmed the ADR/hardening-issue mismatch and found no existing owning issue; owner authorized a record-only issue and prohibited immediate resolution |
| `2026-08-10T06:07:54Z` | `Codex/root` | `OPEN` | `BLOCKED` | Review-gate interpretation requires a human owner disposition; no ADR correction is authorized |
| `2026-08-10T07:25:05Z` | Human technical owner `MattSureham`, recorded by `Codex/root` | `BLOCKED` | `OPEN` | Selected disposition 1: the completed hardening review satisfies the ADR's substantive review intent; additive reconciliation authorized |
| `2026-08-10T07:25:05Z` | `Codex/root` | `OPEN` | `IMPLEMENTING` | Began the bounded ADR status clarification and operational-record reconciliation; no architecture or product change authorized |
| `2026-08-10T07:26:46Z` | `Codex/root` | `IMPLEMENTING` | `VERIFYING` | Additive ADR note and resolution record are drafted; targeted check confirms the ADR diff has seven additions and zero deletions, and the cited review/evidence exists |
| `2026-08-10T07:29:35Z` | `Codex/root` | `VERIFYING` | `CLOSED` | Corrected full reconciliation validator passed; owner authority is durably recorded, history is preserved additively, and no required gate remains |

## Closure checklist

- [x] Expected behavior is tied to higher-authority sources.
- [x] The conflict and decision required are recorded without adopting a resolution.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [x] If `Review: INDEPENDENT`, the latest review round requirement is not applicable to this record-only change.
- [x] Required human authority is recorded for the disposition and additive ADR clarification.
- [x] New complexity is absent.
- [x] Residual uncertainty is explicitly owned.
- [x] HANDOFF archives the closed issue and retains exactly one next action.
