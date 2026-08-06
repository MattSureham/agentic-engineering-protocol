# External Tracker Integration

## Metadata

- **ID:** `ISSUE-20260806T013907Z-external-tracker-integration`
- **Title:** Evaluate external issue-tracker integration separately
- **Status:** `BLOCKED`
- **Severity:** `LOW`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-06T01:39:07Z`
- **Requirements:** Post-pilot hardening explicit deferral in root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md)
- **ADRs:** `NONE`
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md)

## Problem

An external issue tracker could duplicate or split lifecycle truth, introduce credentials/network dependencies, and reduce copy-ready portability unless synchronization semantics are explicitly designed.

## Evidence or reproduction

The current protocol uses repository-native issue files and has no tracker connector, sync contract, credential model, or conflict policy.

## Expected behavior

Keep repository artifacts authoritative for the current version. Any integration requires explicit ownership, synchronization, offline, failure, authentication, and portability requirements.

## Assumptions

- **CONFIRMED:** External tracker integration is explicitly excluded from this phase.
- **UNKNOWN:** Whether future adopters would accept a specific vendor or a generic mapping contract.

## Investigation and decision

No tracker integration or vendor dependency is adopted.

## Change

- **Files or components:** `NONE`
- **Behavior changed:** `NONE`
- **Out-of-scope work deliberately excluded:** External API, webhook, connector, sync job, vendor-specific mapping.
- **Rollback or recovery:** `NOT APPLICABLE`

## Verification

`NOT RUN` — no implementation or authorized contract exists.

## Independent review rounds

- **Required:** `YES` if approved because synchronization and external trust boundaries are meaningful architecture.

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** No human-approved integration contract or vendor/portability boundary.
- **Unblock owner:** Human technical owner
- **Unblock condition:** Accepted specification and compatible accepted ADR define authority and synchronization behavior.

## Residual uncertainty

- Value, portability, failure behavior, and truth-conflict handling remain unknown.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `OPEN` | Recorded deferred integration concern |
| `2026-08-06T01:39:07Z` | `Codex/root` | `OPEN` | `BLOCKED` | External integration requires separate owner-approved scope |
