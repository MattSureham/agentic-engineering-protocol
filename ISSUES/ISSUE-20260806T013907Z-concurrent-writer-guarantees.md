# Concurrent-Writer Guarantees

## Metadata

- **ID:** `ISSUE-20260806T013907Z-concurrent-writer-guarantees`
- **Title:** Define guarantees for non-cooperating concurrent writers
- **Status:** `BLOCKED`
- **Severity:** `MEDIUM`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-06T01:39:07Z`
- **Updated UTC:** `2026-08-06T01:39:07Z`
- **Requirements:** Post-pilot hardening explicit deferral in root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md)
- **ADRs:** `NONE`
- **Evidence:** [`EVIDENCE-20260806T013907Z-post-pilot-audit`](../EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md)

## Problem

The Markdown/filesystem protocol coordinates cooperative participants but makes no proven atomicity or locking guarantee against non-cooperating processes changing files between inspection and write.

## Evidence or reproduction

Prior migration review explicitly retained concurrent external mutation as unverified. No concurrent-write test, contract, or implementation exists in this repository.

## Expected behavior

Do not claim concurrent-writer safety. Any future guarantee requires an accepted specification defining actors, failure model, atomicity, recovery, platform support, and compatibility.

## Assumptions

- **CONFIRMED:** Current scope is Markdown-first and has no runtime coordination mechanism.
- **UNKNOWN:** Whether a future solution should be purely procedural, version-control-based, or automated.

## Investigation and decision

No solution is adopted. Investigation is blocked pending a separately approved specification and scope.

## Change

- **Files or components:** `NONE`
- **Behavior changed:** `NONE`
- **Out-of-scope work deliberately excluded:** Locks, transactions, merge service, runtime coordinator.
- **Rollback or recovery:** `NOT APPLICABLE`

## Verification

`NOT RUN` — no implementation or authorized contract exists.

## Independent review rounds

- **Required:** `YES` if scope is approved because concurrency guarantees affect correctness and coordination architecture.

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** No human-approved requirement, failure model, or implementation scope.
- **Unblock owner:** Human technical owner
- **Unblock condition:** An accepted specification update defines the guarantee and authorizes investigation/implementation.

## Residual uncertainty

- All concurrent-writer behavior remains unspecified and unverified.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `OPEN` | Recorded verified limitation without expanding scope |
| `2026-08-06T01:39:07Z` | `Codex/root` | `OPEN` | `BLOCKED` | Separate human-approved specification is required |
