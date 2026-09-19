# Prompt-Independent Discovery With Repository-Owned Authority

## Metadata

- **ID:** `ADR-20260918T064510Z-protocol-discovery-boundary`
- **Title:** Separate protocol authority, adoption signal, host discovery adapter, and manual fallback
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-09-18T06:45:10Z`
- **Author:** `agent:Codex-discovery-authority`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` through the decision-complete Prompt-independent discovery requirement/authority plan, recorded at this UTC boundary before any adapter implementation
- **Related specification:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `DISCOVERY-001`–`DISCOVERY-006` and discovery milestone
- **Related issues:** [Discovery issue](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Related evidence:** [Authority/gap analysis](../EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md)
- **Supersedes / superseded by:** Supersedes no prior ADR; extends their repository-authority/adapter boundary with a pre-work discovery contract. Earlier manual-entry/product wording is explicitly superseded in PROJECT_SPEC. Superseded by `NONE`.

This ADR records the owner-approved abstract boundary, not a claim that an adapter is implemented or independently approved. No vendor instruction filename, hook API, or global configuration becomes normative protocol authority.

## Context

The owner reports adoption failures when an ordinary work prompt does not repeat protocol instructions. Existing records prescribe recovery after entry, but the guide requires a human-supplied onboarding prompt. Rotation solves a different problem by injecting role/recovery prompts into launched sessions. Neither establishes ordinary fresh-session discovery. Official host documents expose different startup mechanisms, so a single universal vendor convention cannot be assumed.

## Decision

1. **Repository-native authority:** Preserve the seven-tier truth hierarchy and separately governed root/product instances. Requirements and accepted ADRs remain authoritative; tests/evidence, operational records and implementation retain their existing roles. An adapter cannot grant task authority, assign itself review eligibility, or bypass review/evidence/handoff gates.
2. **Adoption/discovery signal:** Formal adoption must leave a repository-resident declaration, governed scope, and resolvable canonical normative entry. It must distinguish an adopted repository from a copy-ready template, example, or unrelated nested repository. The declaration records adoption/entry location, not duplicate workflow rules or milestone scope. This boundary does not mandate a new core file or a vendor-specific filename.
3. **Host-specific adapter:** Use only documented and actually verified native project-loading facilities for the supported profile, preferably a minimal repository-local bridge to the canonical entry. Host filenames, import syntax and load timing remain adapter details. One-time installation may add/merge peripheral host files after collision/authority checks; it must preserve existing project instructions. No global personal configuration, hidden conversational memory, new service/runtime, or permission bypass is a prerequisite for the first slice. New trust, dependency, or architectural requirements need fresh owner authority.
4. **Unsupported-host fallback:** Keep the existing explicit onboarding/manual entry path. Missing or disabled loading is not automatically supported behavior. An unavailable adapter cannot erase repository authority; a participant given repository/shell access can still recover manually. Manual recovery is not a passing automatic-activation test.
5. **Support is evidence-bounded:** The initial implementation/conformance scope is Codex CLI and Claude Code, each represented by exact tested version/mode/configuration/directory profiles. Names or official documentation are not support certification. Real fresh-session evidence must show recovery before task implementation without task-level reminders; inability to establish this leaves the claim unverified, not silently weakened.
6. **Distribution and compatibility:** Retain the exact ten Markdown source files and self-contained adoption instructions. Host-specific installation snippets/details may be carried by the existing guide/example without duplicating BOOTSTRAP semantics. Installed host files are peripheral adapter artifacts, not an eleventh normative core file. Existing adopters retain manual operation until their one-time discovery migration and required validation are complete; do not retroactively claim old copies comply.
7. **Existing machinery remains unchanged:** Discovery precedes role execution; it does not replace pipeline transitions, dispatcher routing, participant independence, or rotation failure/budget semantics. The new milestone is selected before the unstarted demonstration; the latter retains its original scope and unattended-run acceptance conditions.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** Public adoption/compatibility contract and a new entry-path boundary; implementation authority and milestone priority change.
- **Existing authorization:** Owner-approved requirement/authority plan, now recorded in PROJECT_SPEC and the owning issue.
- **Approval evidence:** Human technical owner `MattSureham` explicitly chose Codex CLI plus Claude Code and discovery-first priority, then approved the complete plan before this recording. Attribution is repository provenance, not cryptographic authentication.

## Alternatives considered

| Alternative | Benefit | Cost/risk and decision |
|---|---|---|
| Require the onboarding prompt for every task | No new integration work | Retains the demonstrated product gap; rejected by owner direction |
| Rely on README/BOOTSTRAP presence alone | Smallest documentation change | No demonstrated host entry path; cannot establish activation |
| Declare one vendor filename the universal protocol authority | Simple-looking installation | Host mechanisms differ and authority would be duplicated or displaced; rejected |
| Require global hooks/configuration or an orchestrator | Centralized integration | Hidden dependencies and unnecessary security/runtime complexity; excluded from this slice |
| Repository-owned authority with thin profile-specific discovery | Preserves recoverability and permits evidence-bounded support | Adds migration and conformance obligations; selected at the abstract boundary without pre-certifying any mechanism |

## Consequences

### Positive

- Ordinary task prompts no longer carry supported-host onboarding duties.
- Host replacement/removal does not destroy project authority or state.
- Activation and autonomous role rotation have separate, falsifiable proof standards.

### Negative and tradeoffs

- Supported profiles require real-session evidence, version/configuration provenance and revalidation after material changes.
- Instruction loading does not itself enforce semantic compliance; failure remains visible and blocks the corresponding support claim.
- Existing project instructions and nested scopes require careful migration rather than bulk overwrite.

### Compatibility and migration

Root adoption, pipeline, dispatcher, rotation and autonomy ADRs remain intact. Product onboarding/plug-and-play wording evolves explicitly in the specification; the reusable package's current prompt-dependent instructions remain an open implementation obligation of the discovery issue, not a silently completed change. The current authority participant changes no BOOTSTRAP or package files.

Demonstration contract order changes from 5 to 6 only. Its accepted requirements, dependency, ID, initial event and attempt 0 are preserved; the digest rebinding is documented as owner-authorized specification migration, not a new pipeline transition. First four accepted milestone entries/digests remain unchanged.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Adoption declaration and scoped entry reference | Let hosts locate repository authority without becoming it | DISCOVERY requirements; future template/nesting/collision tests | [Discovery issue](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md) |
| Per-profile adapters and support evidence | Native loading mechanisms differ | Real cold-session and fallback acceptance, independent review | Same issue; no profile verified yet |
| Prospective milestone reordering | Owner selected discovery priority | Canonical digest comparison and read-only dispatcher validation | No new runtime state/schema or scheduler |

## Evidence and assumptions

- **CONFIRMED:** Existing prompt-dependent entry and prompt-injected rotation are visible at baseline `58fa281`; the owner approved this boundary.
- **INFERRED:** Native project-local loading is the smallest candidate bridge. Implementation must test rather than assume it works.
- **UNKNOWN:** Actual profile conformance, incident reproduction, behavior across future host upgrades; owned by the discovery issue.

## Independent review rounds

- **Required:** `YES` — the future immutable discovery target must be reviewed with this ADR, specification evolution, migration and actual activation evidence in scope.

No independent review is recorded. Accepted owner architecture authority is distinct from implementation acceptance. Do not launch a reviewer or claim approval during this authority-only phase.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-09-18T06:45:10Z` | `NONE` | `ACCEPTED` | `human:MattSureham`, recorded by `agent:Codex-discovery-authority` | Owner approved the requirement/authority plan, four-layer boundary, first two harnesses and discovery-first ordering; owning issue preserves the decision and limitations |
