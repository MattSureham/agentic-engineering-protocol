# Human Checkpoint

This is an owner synchronization summary, not project truth. Read [BOOTSTRAP](BOOTSTRAP.md); requirements live in [PROJECT_SPEC](PROJECT_SPEC.md), architecture in accepted ADRs.

## Checkpoint metadata

- **Generated UTC:** `2026-09-19T21:37:43Z` (resumed authority finalization; deterministic validation complete)
- **Prepared by:** `agent:Codex-discovery-finalize`, preserving the preceding `agent:Codex-discovery-authority` decisions
- **Period covered:** Owner-approved prompt-independent discovery requirement evolution from clean synchronized `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b`
- **Specification status reviewed:** `ACCEPTED`; DISCOVERY-001–006 and the discovery milestone are authorized, not implemented or independently accepted
- **Implementation/reference state:** Tooling and ten-file reusable package unchanged; four accepted milestones retained; discovery order 5 and demonstration order 6 are AUTHORIZED at attempt 0
- **Prior checkpoint:** Exact prior owner summary remains recoverable with `git show 58fa281:HUMAN_CHECKPOINT.md`; prior accepted decisions/reviews are not rewritten

## System mental model

The product remains a Markdown-first, repository-native engineering protocol. Its root development instance is separately governed from the reusable ten-file package. The seven-tier truth hierarchy, authority/review distinction, evidence ownership, lifecycle and role separation remain unchanged.

Discovery is a new **entry** requirement: a supported fresh participant must find the adopted protocol from normal repository startup/interaction with only an ordinary work request. Discovery never grants implementation authority. Pipeline/dispatcher/rotation are existing root execution mechanisms after recovery, not a substitute for entry discovery.

## Material changes since the prior checkpoint

| Change | Reason and authority | Consequence |
|---|---|---|
| DISCOVERY-001–006 plus explicit onboarding/plug-and-play supersession | Owner reports real usage failure and approved the requirement/authority plan; [gap analysis](EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md) distinguishes verified repository gaps from the unreproduced external incident | Onboarding prompt becomes fallback/diagnostic, not a normal supported-host prerequisite; no retroactive support claim |
| Four-layer discovery boundary | [Accepted ADR](ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md), owner-approved before implementation | Repository-native authority → scoped adoption signal → subordinate host adapter; unsupported hosts retain manual fallback |
| First implementation/conformance scope | Owner selected Codex CLI plus Claude Code | Both require real fresh-session evidence; neither is currently certified by this record |
| Discovery-first scheduling | Owner explicitly chose new work before the unstarted demonstration | New order-5 contract; demonstration order 5→6 and digest rebinding only; first four accepted entries/digests and all old ADR originals remain unchanged |

## Architecture decisions

- **Accepted now:** `ADR-20260918T064510Z-protocol-discovery-boundary` defines responsibilities and compatibility. It does not make AGENTS.md, CLAUDE.md, a hook, a skill or any other host convention normative protocol authority.
- **Retained:** Root adoption, authorized pipeline, dispatch, rotation and autonomy ADRs; source precedence and role/state-machine interfaces.
- **Implementation boundary:** Thin repository-local entry bridges, necessary root/package adoption/onboarding guidance, deterministic/real conformance tests and durable records. Ten Markdown core files remain self-contained; peripheral host artifacts preserve existing instructions. No global personal configuration or new infrastructure is required.
- **Escalation boundary:** A needed security/trust, dependency, scope or architecture change not covered by this contract requires owner authority. Routine work within the accepted milestone does not.
- **Proposed/disputed decisions:** None pending within the accepted slice. Specific host loading details must be verified before reliance, not invented.

## Complexity and architecture drift

New complexity is limited to scoped adoption declarations, profile-specific loading/migration and maintained conformance evidence, owned by the [discovery issue](ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md). No runtime/interface change has been made.

The current reusable package still requires explicit onboarding. That mismatch with the newly accepted target behavior is an explicit implementation gap, not silently fixed semantics or an approval claim. The next immutable target requires independent review including this authority boundary and root/product alignment.

## Assumptions and uncertainty that changed

| Certainty | Statement | Consequence |
|---|---|---|
| CONFIRMED | Existing onboarding/launcher prompts contain explicit protocol reminders | Their success does not establish task-independent discovery |
| CONFIRMED | Owner approved initial two-harness scope and discovery-first order | Requirements, ADR and contracts now carry durable authority |
| UNKNOWN | Exact external incident reproduction | Report is attributed to owner; no trace or external repository evidence fabricated |
| UNKNOWN | Candidate profiles actually activate reliably | Required real fresh-session acceptance is NOT RUN; supported profiles cannot yet be claimed |
| UNKNOWN | Unattended AUTONOMY-004 demonstration | Still unperformed; component acceptance and discovery conformance cannot substitute for it |

## Confidence and verification

- Baseline Git recovery and owner approval are recorded; the resumed full suite passes all 97 tests (23.916s, exit `0`) on Darwin arm64/Python 3.9.6.
- [Persisted authority audit](EVIDENCE/EVIDENCE-20260918T065750Z-discovery-authority-validation.md) passes: six contracts, four accepted digests unchanged, demonstration order-only/digest-only rebinding, discovery AUTHORIZED attempt 0, deterministic implementer dispatch, 58 Markdown documents/relative paths, history and protected-tree preservation, isolated ten-file copy and whitespace checks.
- This checkpoint is a pre-commit publication snapshot for `docs: authorize prompt-independent discovery` directly after `58fa281`. A normal push and equality of local/cached/direct remote refs must be established from Git before the next participant consumes it; the containing commit supplies its own immutable identity.
- No adapter, instruction shim, reusable-package change, live probe, rotation run, implementation attempt, independent review or recorder acceptance is performed in this phase.
- Dedicated Markdown linters are unavailable; full CommonMark, external URLs and fragment targets are outside the performed structural checks. Live discovery acceptance is NOT RUN. Cross-host/version reliability, original incident reproduction, authenticated identity, concurrent writers, scale and production readiness are not established.

## Human attention required

No further routine decision is required to implement the accepted discovery milestone. The owner has approved the requirement and abstract architecture, two-harness initial scope, priority change and phase stop boundary. Escalate only if implementation exposes authority not covered by those records; do not convert a failed probe or ordinary fix/re-review loop into redundant human approval.

Four prior deferrals remain BLOCKED: concurrent-writer guarantees, authenticated identity/approval, large-scale coordination and external tracker integration. Nothing here resolves or expands them.

## No human attention required

The next implementation participant may follow the existing dispatcher and role contract through the accepted discovery scope, deterministic verification and independent fix/re-review loop. It must preserve real conformance evidence and must not certify its own target. The present authority participant stops before READY.

The demonstration retains its original lifecycle acceptance conditions: when selected later, runner-launched participants must perform the complete lifecycle; no manual transition is authorized as a shortcut to its evidence.

## Next checkpoint trigger

- **Trigger:** Missing authority, material review ambiguity, proposed boundary expansion, conformance evidence unable to support the intended contract, or milestone acceptance
- **Expected owner action before then:** NONE; after authority-record validation/publication, the next participant follows the discovery implementer decision. No live runner invocation occurs in this owner/specification phase.
