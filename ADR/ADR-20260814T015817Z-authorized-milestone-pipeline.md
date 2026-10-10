# ADR-20260814T015817Z: Adopt a Root-Local Authorized Milestone Pipeline

## Metadata

- **ID:** `ADR-20260814T015817Z-authorized-milestone-pipeline`
- **Title:** Adopt a root-local state-and-gate pipeline for specification-authorized milestones
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-14T01:58:17Z`
- **Author:** `Codex/root`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` through the explicit owner decision and approved Authorized Milestone Pipeline v1 plan received before implementation
- **Related specification:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Authorized milestone pipeline phase
- **Related issues:** [`ISSUE-20260806T013907Z-runtime-automation`](../ISSUES/ISSUE-20260806T013907Z-runtime-automation.md), [`ISSUE-20260807T022523Z-pilot-onboarding-authority-friction`](../ISSUES/ISSUE-20260807T022523Z-pilot-onboarding-authority-friction.md), and [`ISSUE-20260811T030136Z-review-disposition-vocabulary`](../ISSUES/ISSUE-20260811T030136Z-review-disposition-vocabulary.md)
- **Supersedes / superseded by:** Supersedes only the root runtime-automation deferral for the exact accepted phase and milestone; superseded by `NONE`

Only `ACCEPTED` ADRs are authoritative. This record is accepted before runtime implementation because the human technical owner approved the decision-complete architecture and scope. The resulting milestone still requires independent review before acceptance.

## Context

The repository has an independently approved structural validator but no executable mechanism that distinguishes prior milestone authorization from repeated owner prompting, verifies transition gates, or preserves machine-readable lifecycle state. Root `PROJECT_SPEC.md` historically deferred runtime automation and the corresponding issue is `BLOCKED`. The owner has now explicitly authorized a bounded automated milestone pipeline while retaining Markdown authority, independent review, and human escalation for missing authority.

The smallest useful slice is not an agent orchestrator. It is a local state-and-gate engine used by replaceable participants. It must be able to prove why a milestone may advance without turning runtime state, Git, or participant labels into product authority.

## Decision

1. Root `PROJECT_SPEC.md` owns milestone authorization. An accepted, schema-valid milestone entry is prior human authorization; absence, ambiguity, or contract-digest drift blocks autonomous continuation.
2. The normative machine contract is embedded between unique markers in `PROJECT_SPEC.md`. Its canonical JSON SHA-256 binds lower-precedence state to the accepted scope without copying requirements into runtime state.
3. Each automated milestone uses an `aep-pipeline-state/v1` JSON block inside its owning issue. The block stores only operational state, attribution, immutable revisions, evidence/review references, and append-only events. The issue remains the durable lifecycle and review record; the state block is not a new truth tier.
4. The root-only Python tool exposes read-only status and explicit validated transitions. It may update only the owning issue and generated evidence records. Issue replacement uses a same-directory temporary file plus `os.replace`; evidence is written before an advancing issue update, so interruption may leave safe orphan evidence but cannot advance without evidence.
5. The supported primary sequence is `AUTHORIZED → READY → IN_PROGRESS → AWAITING_PEER_REVIEW → ACCEPTED`. `CHANGES_REQUIRED → IN_PROGRESS` implements the fix loop. A nonterminal milestone may enter `BLOCKED_HUMAN_AUTHORITY` only with a linked `BLOCKED` issue whose `Authority` is `HUMAN` and whose unblock condition is nonempty. *(Amended 2026-09-23, owner-approved; see status history.)* Every state a milestone may enter MUST have a defined, verifiable exit; no machine state may be enterable yet impossible to leave through a legal transition. `BLOCKED_HUMAN_AUTHORITY` returns to `IN_PROGRESS` only when the linked blocker issue durably records the human technical owner's decision satisfying its unblock condition (its status is no longer `BLOCKED`), the transition names the blocker recorded at entry, and the transition reason cites that recorded decision. The resume preserves the interrupted attempt rather than opening a new one. Exiting `BLOCKED_HUMAN_AUTHORITY` resolves only the authority blocker; it authorizes no separately gated execution, resource budget, or external side effect, whose own conditions remain in force. Quota, budget, or other participant/resource failures MUST NOT by themselves produce `BLOCKED_HUMAN_AUTHORITY` (see `ROTATE-004`).
6. Orientation and submission call the existing structural validator in-process. Milestone acceptance checks are exact argv arrays from the accepted contract, executed locally with `shell=False`, the repository root as working directory, captured output, and bounded timeout. No failed, timed-out, unsupported, or unavailable check advances state.
7. Git commits identify immutable targets for this root proof. Submission requires a clean target commit containing the same accepted contract and compares its implementation range with the contract path allowlist. This is not a reusable protocol requirement. *(Amended 2026-09-29 and strengthened 2026-09-30, 2026-10-08, and 2026-10-10, owner-approved; see status history.)* The implementation-range comparison MUST distinguish changes attributable to the current attempt from unrelated intervening changes that entered the authoritative branch under separate durable authority while the attempt was open. The milestone issue MAY carry an optional machine-readable intervening-authority registry whose entries name a separately authorized owning issue, an exclusive-to-inclusive commit range, and a declared exclusion scope (`paths`); a present registry is validated on every submission, and a malformed, null, or unverifiable registry is rejected, never silently ignored, even when the target is otherwise in scope. Each entry is verified fail-closed at submission. The machine-critical authority and review facts of the owning issue are carried by strict machine-readable blocks, not inferred from human-oriented Markdown prose: exactly one `aep-authority-decision/v1` block records the decision identity, authority `HUMAN`, state (`EFFECTIVE` required; `PENDING`, `REJECTED`, or `SUPERSEDED` refuses), an exact-file `scope` of substantive repository paths the decision authorizes (empty for records that authorize no substantive paths), `unblock` `SATISFIED`, the decision UTC, the deciding human owner label, and an anchor commit (explicit `recorded_commit` or the issue-history commit that introduced the decision identity); and, for independently reviewed entries, exactly one `aep-review-round/v1` block records the round identity and UTC, a reviewer label differing from the current implementor label, the full reviewed target revision, disposition `APPROVED`, zero open material findings as a bare integer, an exact-file `scope` of reviewed substantive files, and an anchor commit. Duplicate, malformed, or schema-divergent blocks refuse; an issue lacking a required block refuses rather than falling back to prose inference. Each anchor commit is an ancestor of or equal to the entry's range tip; the issue content at each anchor verifiably carries the recorded decision or round (either the block itself with identical identity fields, so post-anchor edits to machine facts re-anchor or refuse, or the attributable historical prose record the migration cites); every commit in the range touching substantive work descends from or equals the decision anchor, so the effective authority predates the work it exempts; and the reviewed target is an ancestor of or equal to the review anchor. The owning issue is a distinct repository issue (never the milestone's own) recording human authority and an unambiguous resolved status from the fixed issue-status vocabulary (missing, `BLOCKED`, or unrecognized statuses refuse). The declared exclusion scope consists of exact file paths (never directory prefixes) equal to the range's Git-derived substantive work (every touched path other than the owning issue record, record-keeping files, `EVIDENCE/` records, issue records, or already-allowed paths) AND, for independently reviewed entries, is non-empty and a subset of the decision block's authorized `scope` AND of the review block's reviewed `scope`, so a declaration can neither omit substantive range work, claim untouched paths, nor exceed what the separate owner decision and independent review actually covered; self-reviewed human-authority records declare no exclusion paths, record an empty decision `scope`, and may exclude only their own issue file. The range is non-empty and ancestor-consistent with the submission target, with every post-review commit in the range restricted merge-aware to record-keeping paths. The human-readable narrative remains consistent with the blocks — exactly one recorded owner-decision section whose UTC, attribution, and positive decision match the decision block (a self-reviewed record's prose additionally carries no negated, pending, or contradictory language), exactly one unblock condition field whose `SATISFIED` prefix and remainder match the block, and exactly one unfenced review-rounds section with a uniquely determinable latest round whose fields equal the review block; contradictory, malformed, duplicated, or example-fenced prose refuses rather than silently overriding or substituting for the blocks. Entries' exclusion scopes are pairwise disjoint. A path outside the allowlist is excluded from scope accounting only when every commit touching it in the attempt window — enumerated merge-aware across all parents and without path-limited history simplification — belongs to a verified range whose exclusion scope covers that path. Records authored before the machine-readable requirement are migrated by an explicit attributable edit that appends the blocks while preserving the existing prose and anchors them to the commits whose content already carries the recorded decisions and review rounds; a migration never recreates authority, and an unmigrated record fails closed. The mechanism fails closed on ambiguous provenance, unresolved or unreviewed intervening work, ambiguous or contradictory review records, overlapping attribution that cannot be distinguished, unrecorded commits, and ad-hoc owner-only path exceptions; it must not implicitly widen the allowlist, rewrite the attempt base or history, change `target == HEAD` semantics, or let an attempt smuggle unauthorized changes by labeling them intervening work or widening a registered range over attempt-owned changes. Every exclusion is recorded in the submission verification evidence with its touching commits and covering-entry provenance for the milestone's independent reviewer.
8. Independent review remains a human/agent judgment activity performed outside the pipeline. The durable issue round must identify the target, reviewer, exact protocol disposition, and count of open material findings. The pipeline only checks recorded-label inequality, target equality, schema, and gate consistency; it does not authenticate identity or judge review quality.
9. `APPROVED` plus zero open material findings permits acceptance without another owner prompt. `CHANGES_REQUIRED` prevents acceptance and returns the milestone to within-scope implementation. `BLOCKED` never maps to approval. Informal verdict labels are invalid; qualifiers belong in findings and residual risks.
10. After acceptance, status may select the next dependency-satisfied milestone already present in the same accepted contract. No entry means no work. Runtime state cannot create the next milestone.
11. The executable remains outside `protocol/`. The reusable ten-file Markdown package gains compatible normative guidance and templates but no runtime dependency or automation guarantee.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** This changes the product/architecture authority boundary for milestone execution and introduces a local runtime, state representation, Git-backed immutable targets, subprocess verification, and automated lifecycle transitions.
- **Existing authorization:** Root `PROJECT_SPEC.md`, Authorized milestone pipeline phase, approved through the evidence-backed specification-evolution mechanism.
- **Approval evidence:** Human technical owner `MattSureham` explicitly authorized the phase and approved the decision-complete Authorized Milestone Pipeline v1 plan before implementation on `2026-08-14`; the accepted specification change and this ADR persist that authority.

## Alternatives considered

### Require a human prompt at every milestone boundary

- **Benefits:** No runtime authority interpretation.
- **Costs and risks:** Repeats decisions already made in the accepted specification, prevents autonomous fix/re-review cycles, and makes conversational continuity an operational dependency.
- **Reason not selected:** The owner explicitly rejected redundant approval when scope is already accepted.

### Put mutable scope in a standalone state file

- **Benefits:** Simple parsing and updates.
- **Costs and risks:** Creates a competing requirements source and permits implementation state to silently redefine scope.
- **Reason not selected:** It violates source precedence and the owner's explicit runtime-state boundary.

### Build an agent orchestrator or service

- **Benefits:** Could schedule and invoke participants automatically.
- **Costs and risks:** Adds process lifecycle, concurrency, security, persistence, and portability commitments unnecessary for the first gate engine.
- **Reason not selected:** Explicitly outside scope.

### Keep all state in free-form Markdown

- **Benefits:** No embedded schema.
- **Costs and risks:** Deterministic transition checks would depend on fragile inference and could not reliably distinguish authorization, verification, and review.
- **Reason not selected:** A small JSON projection inside the owning Markdown issue preserves both mechanical inspection and record ownership.

## Consequences

### Positive

- Already-authorized work can advance through deterministic gates and independent review without repeated human prompts.
- Scope remains in the accepted specification, while operational state is durable and resumable.
- Review findings and failures stop acceptance mechanically without delegating judgment to the tool.

### Negative and tradeoffs

- The root repository gains a maintained Python component, embedded JSON schemas, subprocess execution, and Git-specific behavior.
- Contract constants can drift unless changes update tests and tooling together.
- Recorded participant-label inequality does not prove identity or independence.
- Cooperative same-file replacement does not provide non-cooperating concurrent-writer safety.

### Compatibility and migration

- Existing issues without pipeline state remain valid and are ignored by the tool unless referenced by an accepted milestone.
- The source `protocol/` manifest remains ten Markdown files; adopters may continue manually with no Python, Git, or pipeline.
- The historical hardening deferrals remain preserved; only the runtime-automation item is unblocked for the exact new phase.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Embedded milestone and state JSON schemas | Deterministic authorization/state binding | Parser/state-machine tests and exact-target evidence | Semantic scope adequacy remains reviewer judgment |
| Local subprocess verification | Execute accepted deterministic gates | `shell=False`, timeout, output/evidence, failure tests | Commands are trusted because they are accepted specification content |
| Git-backed immutable targets | Bind verification and review to exact root code | Temporary-repository and target/diff tests | Reusable portability is not claimed |
| Recorded implementor/reviewer labels | Enforce a minimal independence condition | Equality and mismatch tests | Authentication remains [`ISSUE-20260806T013907Z-authenticated-identity-approval`](../ISSUES/ISSUE-20260806T013907Z-authenticated-identity-approval.md) |
| Cooperative atomic issue replacement | Keep machine and human lifecycle state in one artifact | Interruption/no-partial-write tests | Concurrent-writer guarantees remain [`ISSUE-20260806T013907Z-concurrent-writer-guarantees`](../ISSUES/ISSUE-20260806T013907Z-concurrent-writer-guarantees.md) |

## Evidence and assumptions

- **CONFIRMED:** The accepted specification previously blocked runtime automation and now explicitly authorizes this bounded phase through its change record.
- **CONFIRMED:** The existing structural validator exposes a callable `validate_repository` function and has an independently approved 21-test baseline.
- **CONFIRMED:** The reusable package is ten tracked Markdown files and contains no runtime component.
- **INFERRED:** An issue-embedded JSON projection is the smallest design that avoids a shadow issue database while supporting deterministic transitions.
- **UNKNOWN:** Portability beyond the recorded Darwin/Python environment, behavior under non-cooperating writers, and whether later projects need a supported optional companion distribution.

## Independent review rounds

- **Required:** `YES` — the target changes governance semantics and introduces runtime state, subprocess execution, Git coupling, and automated acceptance gates.

No independent review round has been recorded. Review the immutable pipeline implementation target and the complete owning-issue round together. An `APPROVED` round on that target may satisfy this ADR's review intent when its scope explicitly includes this decision.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-14T01:58:17Z` | `NONE` | `ACCEPTED` | Human technical owner `MattSureham`, recorded by `Codex/root` | Explicit owner decision plus approved Authorized Milestone Pipeline v1 plan; accepted root specification change records the product authority |
| `2026-09-23T01:32:06Z` | `ACCEPTED` | `ACCEPTED` (decision 5 amended) | Human technical owner `MattSureham`, recorded by `agent:ClaudeCode-discovery-fix-3` | Owner-approved contract evolution adding the `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` exit with recorded-decision gates and the general blocked-state exit-semantics principle; gap and approval recorded in [`ISSUE-20260923T013206Z-pipeline-blocked-exit`](../ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md) |
| `2026-09-29T02:01:57Z` | `ACCEPTED` | `ACCEPTED` (decision 7 amended) | Human technical owner `MattSureham`, recorded by `agent:ClaudeCode-discovery-fix-3` | Owner-approved contract evolution adding intervening-authority scope accounting: fail-closed registry-based distinction of separately authorized intervening changes from attempt-attributable changes, with per-path commit coverage, INDEPENDENT/SELF entry classes, and exclusions recorded in submission evidence; gap, owner invariants, and approval recorded in [`ISSUE-20260929T020157Z-pipeline-scope-intervening-authority`](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) |
| `2026-09-30T03:07:32Z` | `ACCEPTED` | `ACCEPTED` (decision 7 strengthened) | Human technical owner `MattSureham`, recorded by `agent:ClaudeCode-discovery-fix-3` | Owner-directed rework resolving all five material findings of independent review round 1 without shrinking the approved invariants: declared exclusion scopes bound to verified acceptance, validation on every submission, unambiguous review-record parsing, non-blocked status consistency, durable owner decisions for SELF records, clean-range and pairwise-disjointness refusals, merge-aware complete touching-commit accounting, and provenance-carrying exclusion records; findings and authority recorded in [`ISSUE-20260929T020157Z-pipeline-scope-intervening-authority`](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [round-1 evidence](../EVIDENCE/EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md) |
| `2026-10-08T03:08:54Z` | `ACCEPTED` | `ACCEPTED` (decision 7 strengthened) | Human technical owner `MattSureham`, recorded by `agent:ClaudeCode-discovery-fix-3` | Owner-directed rework resolving the three still-open material findings of independent review round 2 without shrinking the approved invariants or loosening fail-closed semantics: declared exclusion scopes bound to durable Git-derived authority (exact-file equality with the range's derived substantive work; substantive commits must postdate the owning record's introduction), uniquely determinable review provenance (single unfenced section, uniquely latest round, boundary-delimited revision, bare integer count, fixed status vocabulary), and verifiably effective SELF owner decisions (attributed positive bodies outside fenced examples; satisfied unblock condition); findings and authority recorded in [`ISSUE-20260929T020157Z-pipeline-scope-intervening-authority`](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [round-2 evidence](../EVIDENCE/EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md) |
| `2026-10-10T09:20:43Z` | `ACCEPTED` | `ACCEPTED` (decision 7 strengthened) | Human technical owner `MattSureham`, recorded by `agent:ClaudeCode-discovery-fix-3` | Owner-directed rework resolving the three still-open material findings of independent review round 3 at their shared root cause without shrinking the approved invariants or loosening fail-closed semantics: machine-critical authority and review facts are carried by strict machine-readable `aep-authority-decision/v1` and `aep-review-round/v1` blocks (exactly one each; schema-validated; duplicate/malformed/absent refuses) instead of prose inference, each bound to an anchor commit whose issue content verifiably carries the recorded decision or round; the declared exclusion scope must equal the range's Git-derived substantive work and be a subset of both the decision's authorized scope and the review's reviewed scope; every substantive range commit must descend from the decision anchor; human-readable prose remains as narrative under fail-closed consistency cross-checks; pre-existing records migrate by explicit attributable block appends anchored to the commits whose content already carries the recorded decisions, and unmigrated records fail closed; findings and authority recorded in [`ISSUE-20260929T020157Z-pipeline-scope-intervening-authority`](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [round-3 evidence](../EVIDENCE/EVIDENCE-20261009T015211Z-scope-attribution-review-round-3.md) |
