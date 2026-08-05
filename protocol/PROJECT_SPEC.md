# Project Specification

> This file is the authoritative requirements template for the repository that adopts the protocol. Replace instructional placeholders with project facts. Do not put workflow rules here; those belong in `BOOTSTRAP.md`.

## Authority and status

- **Status:** `DRAFT`
- **Human technical owner:** `[name or accountable role]`
- **Accepted by:** `[owner identity or NOT ACCEPTED]`
- **Acceptance date:** `[UTC timestamp or NOT ACCEPTED]`
- **Supersedes:** `[prior specification reference or NONE]`
- **Last material change:** `[UTC timestamp, author, and reason]`

Allowed statuses are `DRAFT` and `ACCEPTED`. `DRAFT` authorizes only investigation, evidence gathering, and clearly disposable prototypes; it does not authorize affected product implementation. Set the status to `ACCEPTED` only with attributable human-owner approval and a UTC timestamp. Chat or an ADR cannot substitute for acceptance of product requirements. Preserve material changes in version history when available and summarize their consequences here or in a compatible linked ADR.

## Product intent

### Problem

`[What real problem exists, for whom, and why it is worth solving.]`

### Desired outcomes

- `[Observable outcome.]`
- `[Observable outcome.]`

### Users and stakeholders

| User or stakeholder | Need | Authority or responsibility |
|---|---|---|
| `[role]` | `[need]` | `[responsibility]` |

## Scope

### In scope

- `[Capability or behavior included in this project.]`

### Out of scope

- `[Explicit non-goal or deferred capability.]`

## Functional requirements

Give each requirement a stable ID. Describe externally observable behavior and acceptance conditions rather than inferred implementation.

### REQ-[stable-id] — [short title]

- **Requirement:** `[The system MUST/SHOULD ...]`
- **Rationale:** `[Why this requirement exists.]`
- **Acceptance evidence:** `[Test, contract, demonstration, or measurement that proves it.]`
- **Dependencies:** `[Other requirement/ADR/external dependency or NONE.]`

## Interfaces and executable contracts

Define public APIs, inputs and outputs, file or wire formats, user-visible behavior, compatibility guarantees, and error semantics. Link executable contracts or tests when they exist.

| Interface or contract | Required behavior | Compatibility requirement | Executable reference |
|---|---|---|---|
| `[name]` | `[behavior]` | `[guarantee]` | `[path or NOT YET AVAILABLE]` |

## Data, state, and ownership

- **Core data concepts:** `[models and invariants or NONE]`
- **Persistent state:** `[what persists, where, lifecycle, and owner or NONE]`
- **Data retention/deletion:** `[rules or NOT APPLICABLE]`
- **Migration requirements:** `[compatibility/migration behavior or NONE]`
- **System-of-record boundaries:** `[authoritative sources or NONE]`

## Quality and operational constraints

Record only constraints applicable to this project. Use `NOT APPLICABLE` rather than inventing a requirement.

- **Security and trust boundaries:** `[constraints]`
- **Privacy and sensitive data:** `[constraints]`
- **Reliability and recovery:** `[constraints]`
- **Performance and capacity:** `[measurable constraints]`
- **Accessibility and usability:** `[constraints]`
- **Compatibility and portability:** `[constraints]`
- **Operations and observability:** `[constraints]`
- **Legal or compliance:** `[constraints]`

## Architectural constraints already authorized

List constraints decided by the owner, not speculative design preferences. Link accepted ADRs for durable details.

- `[Constraint and authority reference, or NONE.]`

## Failure behavior

| Failure condition | Required system behavior | Required evidence |
|---|---|---|
| `[condition]` | `[observable response/recovery]` | `[test or procedure]` |

## Verification and release acceptance

Define the minimum evidence required to consider the specified product or milestone accepted.

- `[Required test suite, contract, review, demonstration, or measurement.]`
- `[Required compatibility, security, migration, or recovery check.]`

State any allowed omissions and who may accept them:

- `[Omission, consequence, owner authority, or NONE.]`

## Assumptions and open decisions

Label each statement `CONFIRMED`, `INFERRED`, or `UNKNOWN`. An unresolved item that can materially change behavior, architecture, security, or scope blocks the affected implementation.

| Certainty | Statement | Evidence or decision needed | Owner |
|---|---|---|---|
| `UNKNOWN` | `[open assumption or decision]` | `[what resolves it]` | `[owner]` |

## Specification evolution

`PROJECT_SPEC.md` is authoritative but not immutable.

A specification change MAY be proposed when evidence demonstrates that:

- an existing requirement is ambiguous, incomplete, or internally inconsistent;
- real-world usage exposes a requirement that was not previously represented;
- an existing requirement no longer serves the project's stated goals; or
- a new capability has been explicitly accepted into project scope.

Evidence supports a proposal; it does not by itself authorize a change to an `ACCEPTED` specification. `PROJECT_SPEC.md` MUST evolve through evidence-backed requirement change, not implementation drift. Existing implementation is not, by itself, sufficient evidence that the specification should change to match it. When implementation conflicts with an `ACCEPTED` `PROJECT_SPEC.md`, the default is to correct the implementation and preserve the conflict record until any specification change is approved.

Every material requirement change requires explicit human technical-owner approval. This includes changes that materially alter product scope, compatibility, core invariants, authorized architectural constraints, or the product/architecture authority boundary. A change affecting both product requirements and architecture requires both an accepted specification update and a compatible accepted ADR. If they conflict, `PROJECT_SPEC.md` remains authoritative and the conflict remains unresolved.

Relevant evidence, issue records, and ADRs SHOULD be referenced where appropriate so that the reason for the specification change remains auditable.

## Specification change record

Material requirement changes require human-owner authority. Keep exact proposed wording in an issue or decision request until approved; do not edit an accepted requirement into an unapproved state that appears authoritative. After approval, update the affected requirement and append its change record together. An ADR may explain compatible architecture but cannot override, delete, or fill an unknown requirement. Do not use this log as a substitute for updating the affected requirement.

| UTC time | Change | Reason | Approved by | References |
|---|---|---|---|---|
| `[time]` | `[change]` | `[reason]` | `[owner]` | `[links]` |
