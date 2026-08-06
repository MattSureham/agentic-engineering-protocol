# Authenticated Identity and Approval

## Metadata

- **ID:** `ISSUE-20260806T013907Z-authenticated-identity-approval`
- **Title:** Define authenticated participant identity and owner approval
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

Protocol records require attributable participant and owner identities, but repository text and ordinary Git metadata do not cryptographically authenticate the actor or approval.

## Evidence or reproduction

Existing reviews repeatedly disclose unauthenticated repository attribution. No signing, identity provider, trust root, or validation contract is configured.

## Expected behavior

Do not describe repository attribution as authenticated identity. Any future assurance requires explicit trust, threat, key-management, revocation, and recovery requirements.

## Assumptions

- **CONFIRMED:** Attribution remains useful audit metadata but does not own project truth.
- **UNKNOWN:** Which identity system, if any, a future protocol version should support.

## Investigation and decision

No authentication design is adopted. The topic crosses the security/trust Human Authority Boundary.

## Change

- **Files or components:** `NONE`
- **Behavior changed:** `NONE`
- **Out-of-scope work deliberately excluded:** Commit signing policy, PKI, identity provider, approval service.
- **Rollback or recovery:** `NOT APPLICABLE`

## Verification

`NOT RUN` — no implementation or authorized contract exists.

## Independent review rounds

- **Required:** `YES` if approved because identity and approval authentication change the security boundary.

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** No human-approved threat model, trust root, or authentication scope.
- **Unblock owner:** Human technical owner
- **Unblock condition:** An accepted specification and compatible accepted ADR define the trust boundary and supported mechanism.

## Residual uncertainty

- Current attribution can be forged by a repository writer; no stronger claim is made.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-06T01:39:07Z` | `Codex/root` | `NONE` | `OPEN` | Recorded verified authentication limitation |
| `2026-08-06T01:39:07Z` | `Codex/root` | `OPEN` | `BLOCKED` | Security/trust scope requires explicit owner authority |
