# Post-Pilot Hardening and Root Dogfooding

## Metadata

- **ID:** `ISSUE-20260806T013907Z-post-pilot-hardening`
- **Title:** Separate root governance, operational continuity, and durable records
- **Status:** `IMPLEMENTING`
- **Severity:** `HIGH`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-06T01:39:07Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), including the owner-approved post-pilot hardening requirements to be recorded
- **ADRs:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md)
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md)

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

- **Files or components:** Root governance/specification/README/HANDOFF; root `ADR/`, `ISSUES/`, `EVIDENCE/`, and `HUMAN_CHECKPOINT.md`; reusable `protocol/BOOTSTRAP.md` and `protocol/HANDOFF.md`.
- **Behavior changed:** Root HANDOFF ceases to be represented as canonical truth and becomes a compact index; durable records move to their owning artifacts; snapshot staleness becomes explicit.
- **Out-of-scope work deliberately excluded:** Runtime/orchestrator, daemon/service, database, complex CLI, external issue tracker, concurrent-writer guarantee, cryptographic authentication, large-scale coordination.
- **Rollback or recovery:** Inspect or restore the pre-hardening state from Git revision `e6beeb2cb730183ca2ac13795ad367ad9d9e1099`; do not erase the issue/ADR/evidence trail.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Separate root and package governance | Prevent silent authority coupling | Accepted ADR and semantic validation | Future drift remains review-dependent |

## Verification

No implementation verification has run yet. Baseline observations are in the linked audit and do not count as completion.

## Self-review

- **Participant:** `Codex/root`
- **Reviewed UTC:** `PENDING`
- **Reviewed repository state:** `PENDING`
- **Scope and authority references:** `PENDING`
- **Checks and evidence reviewed:** `PENDING`
- **Findings and corrections:** `PENDING`
- **Limitations:** `PENDING`
- **Residual risks:** `PENDING`
- **Outcome:** `NOT_APPLICABLE` for closure because independent review is required

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

## Closure checklist

- [x] Expected behavior is tied to owner-approved requirements and an accepted ADR.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] The latest independent review round is `APPROVED` and prior material findings are resolved.
- [x] Human authority is recorded in the accepted ADR and HANDOFF authorization boundary.
- [ ] New complexity is covered, removed, or linked to accepted open debt.
- [ ] Residual uncertainty is explicitly owned.
- [ ] HANDOFF reflects the resulting state and exactly one next action.
