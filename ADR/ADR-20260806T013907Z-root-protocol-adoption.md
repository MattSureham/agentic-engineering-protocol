# ADR-20260806T013907Z: Adopt a Root-Specific Protocol Instance

## Metadata

- **ID:** `ADR-20260806T013907Z-root-protocol-adoption`
- **Title:** Adopt a root-specific instance of the published protocol
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Author:** `Codex/root`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` in the human-approved Post-Pilot Hardening plan
- **Related specification:** [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), post-pilot hardening requirements
- **Related issues:** [`ISSUE-20260806T013907Z-post-pilot-hardening`](../ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md)
- **Supersedes / superseded by:** Supersedes the root BOOTSTRAP convention that HANDOFF is canonical project truth; superseded by `NONE`

Only `ACCEPTED` ADRs are authoritative. This record is accepted because the human technical owner approved the decision-complete architecture before implementation.

## Context

The repository publishes a reusable protocol under `protocol/`, but its root development mechanism predates that product. Root `BOOTSTRAP.md` treats HANDOFF as canonical project truth and gives undifferentiated repository evidence blanket precedence. Root `README.md` directs participants to HANDOFF before the authoritative specification. Meanwhile, root HANDOFF and the reusable protocol say HANDOFF is lower-precedence operational continuity. The repository therefore does not demonstrate the truth hierarchy it publishes.

The root must dogfood the protocol without allowing edits to the reusable product to silently rewrite the live governance of this repository.

## Decision

1. The root repository adopts a root-specific protocol instance for its own development.
2. Root truth precedence is:
   1. root `PROJECT_SPEC.md`;
   2. accepted root ADRs;
   3. executable contracts and tests;
   4. root `EVIDENCE/` records;
   5. root `HANDOFF.md`;
   6. current implementation;
   7. participant inference.
3. Root `HANDOFF.md` is a compact operational index. It does not own requirements, architecture decisions, verification archives, closed issue history, or project truth.
4. Root `ISSUES/`, `ADR/`, and `EVIDENCE/` own durable lifecycle, architecture, and observation records respectively. Root `HUMAN_CHECKPOINT.md` is a non-authoritative owner synchronization summary.
5. Root `BOOTSTRAP.md` and reusable `protocol/BOOTSTRAP.md` are separately governed instances. A change to either never automatically changes the other. Semantic divergence is surfaced through an issue and reviewed against each instance's specification and accepted ADRs.
6. The reusable package remains an exact ten-file, copy-ready product. Root-only governance records are not added to `protocol/`.
7. No protocol-maturity claim may rely on this hardening until an independent participant approves its immutable implementation target.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** This changes durable governance, truth ownership, record responsibilities, and the root adoption architecture.
- **Existing authorization:** The human-approved Post-Pilot Hardening plan and root `PROJECT_SPEC.md` product goals.
- **Approval evidence:** Owner-approved plan received before the `2026-08-06T01:39:07Z` implementation boundary; preserved in root HANDOFF and the related issue.

## Alternatives considered

### Keep the legacy root protocol and explain the mismatch

- **Benefits:** Smallest documentation diff.
- **Costs and risks:** Retains contradictory source-of-truth claims and fails to dogfood the product.
- **Reason not selected:** It hides rather than resolves the verified inconsistency.

### Make `protocol/BOOTSTRAP.md` govern the root directly

- **Benefits:** Avoids two BOOTSTRAP files.
- **Costs and risks:** Product edits would silently change live repository governance; target-repository placeholders and package adoption guidance would be mixed with product development state.
- **Reason not selected:** The reusable deliverable and its producing repository have separate change authority and lifecycle.

### Adopt a root-specific instance

- **Benefits:** Demonstrates the published architecture while preserving explicit governance boundaries.
- **Costs and risks:** Two normative files can semantically drift.
- **Reason selected:** Drift becomes observable and reviewable rather than automatic; each file has a clear constituency.

## Consequences

### Positive

- A fresh participant can recover truth ownership from root artifacts without chat context.
- Requirements, architecture, evidence, operational state, and history have distinct durable homes.
- Product changes cannot silently redefine the repository that produces the product.

### Negative and tradeoffs

- Root and reusable protocol semantics require explicit drift review when either changes.
- Historical HANDOFF material must be migrated and indexed without erasing provenance.

### Compatibility and migration

- Pre-hardening root files remain recoverable from Git revision `e6beeb2cb730183ca2ac13795ad367ad9d9e1099` and recorded SHA-256 digests.
- Existing issue IDs and pilot evidence content are preserved in durable records.
- The previously recorded root-file byte-preservation constraint is explicitly superseded by owner authority; it is not silently deleted.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Separate root and reusable protocol governance | Prevent product edits from silently changing live governance | Root BOOTSTRAP boundary, this ADR, link/semantic validation | Future semantic drift requires issue-based review; no automation is added |

## Evidence and assumptions

- **CONFIRMED:** Root source descriptions conflict; direct citations and hashes are in [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md).
- **CONFIRMED:** The owner approved this architecture and its independent-review gate.
- **INFERRED:** Explicit separate governance is the lightest design that both dogfoods and protects the reusable product boundary.
- **UNKNOWN:** Independent reviewer disposition and future participant compliance.

## Independent review rounds

- **Required:** `YES` — the ADR changes the repository's durable governance architecture.

No review round has been recorded. Review the immutable hardening target rather than this mutable implementation state.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `NONE` | `ACCEPTED` | `Codex/root` | Human technical owner approved the complete adoption architecture before implementation |
