# Large-Scale Coordination

## Metadata

- **ID:** `ISSUE-20260806T013907Z-large-scale-coordination`
- **Title:** Specify large-scale coordination claims and limits
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

The protocol supports replaceable participants and bounded review, but no evidence establishes behavior at large team, issue, repository, or throughput scale.

## Evidence or reproduction

The only completed pilot was one bounded local repository with a small number of participants and five tests. No scale model or benchmark exists.

## Expected behavior

Do not claim large-scale coordination fitness. Future work must first define scale dimensions, success criteria, workload, failure modes, and acceptable operational cost.

## Assumptions

- **CONFIRMED:** Existing evidence is bounded and does not establish scale.
- **UNKNOWN:** Which scale limits matter to intended adopters.

## Investigation and decision

No coordination architecture or scaling claim is adopted.

## Change

- **Files or components:** `NONE`
- **Behavior changed:** `NONE`
- **Out-of-scope work deliberately excluded:** Scheduler, coordinator hierarchy, queueing system, multi-repository control plane.
- **Rollback or recovery:** `NOT APPLICABLE`

## Verification

`NOT RUN` — no accepted scale contract or implementation exists.

## Independent review rounds

- **Required:** `YES` if approved because scale claims need independent evidence and may alter architecture.

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** No human-approved scale contract or evaluation scope.
- **Unblock owner:** Human technical owner
- **Unblock condition:** Accepted specification defines scale dimensions and verification criteria.

## Residual uncertainty

- Performance, coordination overhead, and failure behavior at scale remain unknown.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `OPEN` | Recorded absence of scale evidence |
| `2026-08-06T01:39:07Z` | `Codex/root` | `OPEN` | `BLOCKED` | No accepted scale contract exists |
