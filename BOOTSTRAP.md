# Agentic Engineering Protocol Repository Bootstrap

This is the normative entry point for every participant developing this repository. Read it completely before relying on [`HANDOFF.md`](HANDOFF.md) or changing files. Participants are peer-capable and replaceable; repository artifacts, not prior chat or session continuity, must be sufficient for safe resumption.

Project continuity MUST NOT depend on agent identity or session continuity. No participant owns project truth. Attribution is required for provenance, review independence, and approvals, but a fresh participant must be able to continue from the repository without access to prior conversation.

This root BOOTSTRAP governs development of this repository. [`protocol/BOOTSTRAP.md`](protocol/BOOTSTRAP.md) is a separately governed reusable product artifact. A change to either file never automatically changes the other. Material semantic divergence must be recorded as an issue and evaluated against root [`PROJECT_SPEC.md`](PROJECT_SPEC.md), accepted root ADRs, and the product's acceptance criteria.

Higher-priority platform, safety, legal, and explicit human instructions remain binding. When they conflict with repository instructions, stop the conflicting action and record the constraint.

## Project truth

Resolve claims about intended behavior in this order:

1. Explicit root requirements, including [`PROJECT_SPEC.md`](PROJECT_SPEC.md)
2. Accepted root records in [`ADR/`](ADR/)
3. Executable contracts and tests
4. Recorded root evidence in [`EVIDENCE/`](EVIDENCE/)
5. [`HANDOFF.md`](HANDOFF.md)
6. Current implementation
7. Participant inference

Only accepted ADRs occupy level 2. Proposed, rejected, and superseded ADRs are pending or historical records. Issue narratives, `HUMAN_CHECKPOINT.md`, README files, comments, prompts, and chat summaries are navigation or coordination aids; they do not override the hierarchy. Git history provides provenance and recovery context but does not add or reorder a truth tier.

If sources conflict, do not choose the convenient interpretation or rewrite lower-precedence records to hide it. Open or update an issue, cite both sources, classify impact, and escalate when resolution crosses the Human Authority Boundary.

Use these labels for material claims:

- `CONFIRMED`: directly supported by an identified authoritative source or reproducible evidence.
- `INFERRED`: a reasoned conclusion with recorded supporting facts and interpretation.
- `UNKNOWN`: not established; state what would resolve it.

## Artifact ownership

- `PROJECT_SPEC.md` owns product goals, requirements, contracts, constraints, non-goals, and acceptance criteria for this repository's protocol product.
- `ADR/` owns durable root architecture decisions and rationale. Only accepted ADRs are authoritative.
- Executable contracts/tests and `EVIDENCE/` own reproducible observations. Evidence supports or challenges claims; it does not authorize product or architecture decisions.
- `ISSUES/` owns detailed lifecycle, findings, disagreements, blockers, and residual uncertainty for meaningful work.
- Machine-readable milestone state, when enabled by an accepted specification and compatible accepted ADR, lives inside the owning issue. It is operational lifecycle data bound to the authoritative contract digest; it cannot add scope, requirements, architecture, approvals, or a new truth tier.
- `HANDOFF.md` owns only the current operational snapshot, compact unresolved-issue index, non-terminal background-task state, one next action, recent activity, and an archive index.
- `HUMAN_CHECKPOINT.md` is a low-bandwidth owner summary and decision queue. It cannot override the specification or accepted ADRs.
- `README.md` is repository navigation. Files under `protocol/` are the reusable product, governed by the root specification but not a replacement for root development records.

The live HANDOFF is not an issue database, decision log, evidence archive, terminal-task ledger, or chronological diary. Put durable detail in its owning artifact and link it from HANDOFF only while operationally relevant.

## Participant identity and records

Use an attributable participant label in activity, evidence, reviews, and approvals, such as `human:<role>` or `agent:<tool>-<session-label>`. Attribution supports audit and independence; it does not own truth or continuity. Use UTC ISO 8601 timestamps.

Create repository-unique immutable IDs in this form:

`TYPE-YYYYMMDDTHHMMSSZ-short-slug`

Use `ISSUE`, `ADR`, `EVIDENCE`, and `TASK`. Check for collisions and append a short disambiguating suffix if necessary. A title change does not change an ID. Preserve legacy IDs already recorded by this repository.

## Start or resume procedure

Before implementation:

1. Read this file completely.
2. Inspect repository structure, `git status`, current branch, upstream state, recent log, local instructions, validation entry points, and relevant boundaries.
3. Read `PROJECT_SPEC.md`, relevant accepted ADRs, executable contracts/tests, referenced evidence, and then HANDOFF, in precedence order.
4. Check HANDOFF snapshot metadata and apply every staleness trigger. Reconcile stale fields from higher-precedence sources and current repository state.
5. Reconcile each non-terminal background task through its recorded query mechanism. Mark a missing process or remote reference `ORPHANED`; never assume it remains active.
6. Inspect the files relevant to proposed work independently. Verify important HANDOFF claims rather than inheriting them.
7. Identify contradictions, unsupported assumptions, unavailable tools, incomplete work, remote divergence, and dirty files that may belong to someone else.
8. Confirm that the accepted specification authorizes the proposed behavior. An explicit current milestone in `PROJECT_SPEC.md` is prior human authorization for its declared scope; no new approval is needed merely to enter its next implementation, verification, review, or within-scope fix stage. If authority is missing, stale, or ambiguous, limit work to investigation, evidence, or an explicitly reversible proposal.
9. Treat HANDOFF's Next Action as a continuity pointer, not higher authority. Select the highest-priority safe action supported by current evidence.
10. Classify authority and review requirements, then update or create an issue for meaningful work before implementation. If an accepted milestone contract and local pipeline exist, reconcile its machine state from the owning issue and use it only for the transitions it supports.

Never discard, overwrite, or reformat unrelated participant changes merely to obtain a clean tree. Do not push across unexpected remote divergence.

## Selecting and scoping work

Prefer small, reversible changes tied to an explicit requirement or demonstrated gap. Do not broaden work for adjacent cleanup.

An external task prompt, implementation momentum, participant preference, or an inferred useful next step does not create product scope. Conversely, do not ask the owner to reapprove a milestone already explicit in the accepted specification. Continue autonomously through deterministic gates and independent review while scope and authority remain intact; stop at a real authority boundary, not at a routine lifecycle boundary.

Routine work may remain inline in HANDOFF only when it is local, reversible, contract-preserving, verified in one run, and introduces none of the complexity categories below. Meaningful, blocked, disputed, unverified, review-gated, or cross-session work uses [`ISSUES/TEMPLATE.md`](ISSUES/TEMPLATE.md) and this lifecycle:

`OPEN → INVESTIGATING → IMPLEMENTING → VERIFYING → REVIEW → CLOSED`

`BLOCKED` may replace a non-terminal state. Record the prior state, blocker, unblock owner, and observable unblock condition. Restore the appropriate state when unblocked. Reopen closed work as `OPEN` without erasing prior closure history.

Implementation is not completion. `CLOSED` requires recorded verification and every required approval/review.

## Human Authority Boundary

Agents may autonomously make local, reversible choices that preserve external contracts and accepted architecture, including routine defect fixes, test organization, local decomposition, and small behavior-preserving refactors.

Explicit accepted requirements can authorize product behavior. A compatible accepted ADR can authorize only the architecture it decides. Otherwise obtain human technical-owner approval before adopting a durable commitment involving:

- a major abstraction or material long-term complexity;
- a significant dependency;
- a public or cross-module contract;
- a core model, persistence, migration, or state-ownership change;
- a background service or process;
- deletion of a capability;
- a security, privacy, permission, identity, or trust-boundary change;
- contradiction of an accepted ADR or requirement.

Persist product behavior, scope, capabilities, and public contracts in an accepted `PROJECT_SPEC.md` update. Persist compatible architecture in an accepted ADR created from [`ADR/TEMPLATE.md`](ADR/TEMPLATE.md). A mixed change requires both. If they conflict, the specification remains authoritative and the conflict stays unresolved.

For a boundary-crossing decision, gather evidence; record exact proposed wording or a proposed ADR; explain alternatives, consequences, compatibility, complexity, and uncertainty; add a concise owner decision request to `HUMAN_CHECKPOINT.md`; and stop the affected implementation until approval is durably recorded. A chat approval must be persisted in the owning artifact before later participants rely on it.

Changes to root authority, precedence, record ownership, or required gates cross this boundary. Product-protocol changes follow the root specification and its acceptance criteria.

When `PROJECT_SPEC.md` defines an accepted milestone, it authorizes execution only within that milestone's recorded scope and constraints. Deterministic verification proves only the checks it ran. Independent review supplies a separate disposition but cannot expand the milestone. Human escalation remains required when specification text must change, scope or accepted architecture would change, a human-gated blocker must be resolved, evidence cannot establish authority, review exposes a material unresolved ambiguity, or a high-impact external action lacks prior authorization.

If independent review returns material findings whose resolution remains inside the accepted milestone, return to implementation and repeat verification/review without seeking another routine owner approval. After `APPROVED` and all acceptance gates, the next dependency-satisfied milestone already present in the accepted specification may begin without a new prompt. If none exists, the valid next action is to stop; never manufacture one in runtime state.

## Review requirements

Meaningful issues have separate `Authority` and `Review` fields:

- `Authority: AGENT` or `HUMAN` identifies who may adopt the decision.
- `Review: SELF` or `INDEPENDENT` identifies who validates the resulting work.

Use `SELF` only for local, reversible, contract- and architecture-preserving work with no material dispute or independent-review risk. Record reviewed state, scope, authority, checks, findings, limitations, risks, and outcome. Self-verification is not independent review.

Independent review is required before closing changes that affect external behavior/contracts, dependencies, persistent state, security/trust, concurrency, background processes, cross-module coupling, governance architecture, or material long-term complexity.

An independent reviewer must be a different participant or fresh agent instance that did not implement the target. It inspects the specification, accepted ADRs, tests/contracts, implementation, and evidence directly and challenges unsupported assumptions, alternate interpretations, regressions, unnecessary complexity, and drift.

Append each review round with reviewer identity, immutable reviewed state, scope, procedures, findings, limitations, residual risks, evidence, and exactly one disposition: `APPROVED`, `CHANGES_REQUIRED`, or `BLOCKED`. Use that exact vocabulary in session-facing verdicts as well as durable records; put qualifiers such as non-blocking findings in findings and residual risks, not in a fourth disposition. Never replace an earlier round. If no reviewer is available, leave the issue in `REVIEW` or `BLOCKED`; do not self-certify closure.

For a pipeline-managed milestone, also record the exact reviewed target and the nonnegative count of open material findings in the owning issue. Recorded implementor and reviewer labels must differ, but label inequality is not authenticated identity. `APPROVED` requires zero open material findings. `CHANGES_REQUIRED` prevents acceptance and returns within-scope work to implementation. `BLOCKED` never maps to approval and must identify what authority or evidence is missing.

## Evidence and verification

Meaningful work preserves:

`Problem → Evidence or reproduction → Change → Verification → Residual uncertainty`

Evidence records the exact procedure/input, UTC time, environment and revision, exit status and concise raw output or durable artifact, interpretation, limitations, skipped checks, and uncertainty as applicable. Use [`EVIDENCE/TEMPLATE.md`](EVIDENCE/TEMPLATE.md) for substantial, reusable, externally stored, or review-critical proof. Small routine evidence may remain in the owning issue or HANDOFF.

Do not commit secrets, credentials, personal data, or needlessly large generated logs. If evidence relies on an external path or artifact, state its retention and access limits and what would make it reproducible. External or missing evidence cannot support a stronger claim than a fresh participant can inspect.

If a check cannot run, record `NOT RUN`, the attempted command when applicable, the reason, and consequence. Unavailable, skipped, flaky, partial, or inspection-only checks are not passes. Preserve original observations and append attributable corrections rather than silently rewriting them.

## Unverified complexity

Every abstraction, dependency, persistent state element, configuration dimension, background process, concurrency mechanism, and cross-module coupling is a cost requiring justification, requirement ownership, failure-mode analysis, and contract/test/evidence coverage.

Do not assign decorative scores. Uncovered complexity must be removed, covered, or linked to an open issue explicitly accepted as debt by the human owner; it does not disappear when the originating issue closes.

## Architecture drift review

At releases, subsystem milestones, significant ADRs, accumulated complexity, or owner request, an independent reviewer first derives expected architecture from the specification, accepted ADRs, and executable contracts/tests—not from implementation. Compare it to implementation and classify each material difference:

- `ALIGNED`
- `JUSTIFIED_DEVIATION`
- `UNJUSTIFIED_DRIFT`
- `UNKNOWN`

Record differences as evidence and issues. Drift review surfaces differences; it never automatically authorizes a rewrite.

Root/product protocol divergence follows the same rule: compare each BOOTSTRAP against its owning requirements and accepted decisions, then record material semantic differences. Byte identity is neither required nor sufficient for alignment.

## Background and asynchronous work

Do not start work that may outlive the session unless another participant can query and reconcile it. Before yielding, record task ID, purpose, owner, start UTC, process or durable remote reference, exact query/recovery method, last observation, state, and terminal evidence location. States are `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, and `ORPHANED`.

HANDOFF carries only non-terminal tasks. When a task becomes terminal, move durable details to its issue/evidence record and retain at most a concise recent-activity/archive link.

## Failure and interruption handling

When context, quota, time, or tool limits approach, stop early enough to leave a coherent repository. Record complete and partial work, exact file/revision state, commands/results, unavailable checks, issue status, uncertainty, background-task data, and one bounded next action.

For interruptions, partial implementation, inconsistent state, missing evidence, or an incomplete prior HANDOFF, preserve what is verified and label the rest `UNKNOWN`. Do not repair by guessing or close work to make the handoff tidy.

## HANDOFF maintenance

Keep exactly these five ordered top-level sections in [`HANDOFF.md`](HANDOFF.md):

1. Current State
2. Active Issues
3. Next Action
4. Recent Activity
5. Archived Summary

Current State starts with snapshot metadata:

- snapshot updated UTC;
- repository revision, branch/upstream, and dirty-state description;
- evidence cutoff UTC or revision;
- timestamps/results for external checks that affect the snapshot;
- explicit staleness triggers.

A snapshot is stale when the checked-out revision/branch differs, dirty files are not represented, newer linked evidence changes a claim, an external reference has changed or exceeded its declared check interval, a supposedly live task has not been reconciled, or a recorded constraint/next action conflicts with higher authority. Mark affected claims `UNKNOWN` until reconciled; do not refresh only the timestamp.

Current State is concise and present-tense. Active Issues indexes unresolved `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `BLOCKED` records only. Next Action has exactly one bounded item. Recent Activity is newest first and attributable. Archived Summary indexes durable history and compaction provenance.

Participants may correct shared snapshot/index fields from evidence and must add their own activity entry. Never rewrite another participant's authored activity/evidence or erase disagreement.

When HANDOFF approaches 1,000 lines or becomes hard to scan, compact it. Preserve at least the ten newest entries and any additional entry required by unresolved work. Move closed issue bodies, long verification narratives, terminal tasks, and old diary entries to their owning durable records or immutable Git history; link them from Archived Summary. Record the compaction itself, source revision/digest, and migration destinations.

## Before stopping

1. Re-read the diff and remove accidental scope.
2. Run proportionate verification and record exact results.
3. Obtain required human authority and independent review.
4. Update specification, ADR, issue, evidence, and checkpoint records at their source of ownership.
5. Reconcile background tasks.
6. Reconcile HANDOFF metadata, snapshot, unresolved index, recent activity, archive, and exactly one next action.
7. Reconcile any accepted milestone's issue-embedded machine state with its human-readable issue lifecycle and HANDOFF pointer; a conflict is a failure, not permission to choose the convenient record.
8. Commit coherent milestones when authorized; before pushing, check upstream divergence and never overwrite unexpected remote work.
9. Report changes, verification, unavailable checks, limitations, and uncertainty without overstating completion.
