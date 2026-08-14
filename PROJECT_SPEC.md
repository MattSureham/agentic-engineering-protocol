You are creating a standalone, reusable engineering protocol for long-running software projects developed and maintained primarily by coding agents, with a human technical owner retaining architectural authority.

This work MUST be independent of any existing product repository.

Do NOT modify or depend on any existing project such as PCB, CAD, memory systems, or other application-specific repositories.

The output should be a self-contained template/protocol that can later be copied or initialized inside an arbitrary software repository with minimal adaptation.

# Specification status

- **Status:** `ACCEPTED`
- **Human technical owner:** `MattSureham`
- **Current accepted change:** Automated role dispatch phase approved before implementation on `2026-08-14`; the Authorized milestone pipeline phase and authority clarification approved on `2026-08-14` remain in force; prior accepted requirements remain in force except where explicitly superseded below
- **Authority record:** [`ISSUE-20260814T051405Z-role-dispatch`](ISSUES/ISSUE-20260814T051405Z-role-dispatch.md), [`ADR-20260814T051405Z-automated-role-dispatch`](ADR/ADR-20260814T051405Z-automated-role-dispatch.md), [`ISSUE-20260806T013907Z-runtime-automation`](ISSUES/ISSUE-20260806T013907Z-runtime-automation.md), [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md), [`ISSUE-20260806T013907Z-post-pilot-hardening`](ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md), and [`ADR-20260806T013907Z-root-protocol-adoption`](ADR/ADR-20260806T013907Z-root-protocol-adoption.md)

# Goal

Create a reusable "agent-native software engineering protocol" that makes development by multiple independent coding-agent instances:

* resumable
* auditable
* evidence-driven
* reviewable
* resistant to architecture drift
* resistant to compounding hallucinations
* understandable by humans despite agent development throughput exceeding human review throughput
* safe for a new agent to continue without relying on hidden conversational context

The protocol must treat agents as replaceable participants.

No participant should need access to previous chat sessions.

Repository state + protocol artifacts must be sufficient to continue work.

# Core principle

Project truth MUST NOT be inferred solely from the current implementation.

Establish this precedence order:

1. Explicit project requirements / PROJECT_SPEC
2. Accepted ADRs
3. Executable contracts and tests
4. Recorded evidence
5. HANDOFF
6. Current implementation
7. Agent inference

If implementation conflicts with a higher-level source of truth, the conflict must be surfaced rather than silently rationalized.

# Human role

The human technical owner should NOT need to inspect every implementation detail or every diff.

The protocol must therefore preserve human control at the architectural and product-decision level while allowing agents to handle routine implementation autonomously.

Define a Human Authority Boundary.

Agents may autonomously make local, reversible implementation decisions such as:

* local function decomposition
* routine bug fixes
* test organization
* implementation details that do not alter external contracts
* small refactors with preserved behavior

Agents MUST escalate before making durable architectural commitments such as:

* introducing a major abstraction
* adding significant dependencies
* changing cross-module contracts
* changing persistence or state models
* changing public APIs
* changing core data models
* introducing new background services/processes
* deleting existing capabilities
* changing security/trust boundaries
* making changes that materially increase long-term system complexity
* contradicting an accepted ADR or specification

The protocol should make these escalation rules explicit and reusable.

# Agent collaboration model

Do not assume a permanent hierarchy such as supervisor-agent vs worker-agent.

Participants should be peer-capable and replaceable.

Different instances/models may serve different temporary roles:

* Implementor
* Reviewer
* Verification Agent
* Risk Reviewer
* Architecture Reviewer

The same agent instance should NOT be considered sufficient evidence for both implementation and final independent review of its own work.

Independent review should be encouraged for meaningful changes.

# Risk / peer-review principle

The protocol should explicitly support disagreement between independent agents.

Agents should not blindly inherit assumptions from previous agents.

Every new reviewer should be encouraged to ask:

* What assumptions is the previous implementation taking for granted?
* Which claims are unsupported by evidence?
* Is the implementation merely internally consistent, or actually consistent with the specification?
* Could previous agents have converged on the same incorrect assumption?
* What alternative interpretation of the requirement exists?

Disagreement is a signal for investigation, not automatically an error.

# Evidence-first development

HANDOFF statements such as:

"Implemented feature X; looks good."

are insufficient.

Important claims should be backed by evidence such as:

* exact test commands
* test output
* reproduction steps
* relevant commit hashes
* changed files
* benchmark results
* screenshots/logs where appropriate
* before/after behavior
* unresolved uncertainty

Every meaningful issue should ideally have:

Problem
→ Evidence / reproduction
→ Change
→ Verification
→ Residual uncertainty

# Required protocol artifacts

Design a minimal but robust set of reusable files.

At minimum evaluate whether the template should include:

BOOTSTRAP.md
PROJECT_SPEC.md
HANDOFF.md
HUMAN_CHECKPOINT.md
ADR/
EVIDENCE/
ISSUES/

You may alter this structure if a better design exists, but keep the system lightweight.

Avoid documentation bureaucracy.

Every artifact must justify its existence.

# BOOTSTRAP.md

This should be the primary instruction file for any new coding agent entering a repository.

It should explain:

* source-of-truth precedence
* required initial repository review
* how to inspect current state
* how to read HANDOFF
* how to identify active issues
* how to select work
* when implementation is allowed
* verification requirements
* review requirements
* evidence requirements
* ADR rules
* human escalation rules
* handoff requirements
* what to do when context/token/tool limits are approaching
* how to resume interrupted work
* prohibition against claiming success without verification

A new agent should be able to read BOOTSTRAP.md and safely participate without prior conversational context.

# HANDOFF.md

Design HANDOFF as operational continuity, not long-term project truth.

Suggested conceptual structure:

* Current State
* Active Issues
* Next Action
* Recent Activity
* Archived Summary

HANDOFF should answer:

"What does the next participant need to know to continue safely?"

Do not let it become an append-only infinite log.

Include an archival/compaction rule.

For example, once the file becomes roughly 800–1200 lines, older closed activity may be compressed into Archived Summary while preserving:

* unresolved issues
* accepted architecture decisions
* unverified assumptions
* important evidence references
* current next actions

# HUMAN_CHECKPOINT.md

Design a low-bandwidth human synchronization mechanism.

Its purpose is NOT to summarize every code change.

It should tell a technical owner:

* What changed?
* Why did it change?
* What architecture decisions were made or proposed?
* What new complexity was introduced?
* What assumptions changed?
* What should the human understand if they only have limited review time?
* What does NOT require human attention?
* What uncertainty remains?
* What decisions require human authority?
* Has architecture drift occurred?

The checkpoint should allow a human to retain a correct mental model of the system without reading every diff.

# Architecture drift control

Include a mechanism for periodic architecture re-derivation.

At meaningful milestones, an independent agent should be able to inspect primarily:

PROJECT_SPEC
ADRs
contracts/tests

and answer:

"If this subsystem were designed today from these requirements, what architecture would you expect?"

Then compare that expected architecture with the implementation.

The goal is to detect accumulated accidental complexity and architecture drift.

Do not automatically rewrite the system when differences are found.

Surface the differences and classify them.

# Unverified complexity

Introduce a lightweight concept similar to an "Unverified Complexity Budget."

Agents should treat new:

* abstractions
* dependencies
* persistent state
* configuration dimensions
* background processes
* concurrency
* cross-module coupling

as costs requiring justification and verification.

Do NOT create a fake numerical scoring system unless it is genuinely useful.

The important principle is:

complexity without contract/test/evidence coverage is technical debt.

# Issue lifecycle

Define a standard issue lifecycle suitable for agents.

For example:

OPEN
→ INVESTIGATING
→ IMPLEMENTING
→ VERIFYING
→ REVIEW
→ CLOSED

Allow BLOCKED where appropriate.

An issue must not become CLOSED merely because code was written.

Closure requires verification evidence.

# ADR discipline

ADRs should document durable architectural decisions.

Avoid writing ADRs for trivial implementation choices.

An ADR should capture:

* Context
* Decision
* Alternatives considered
* Consequences
* Evidence / assumptions
* Status

Agents may propose ADRs.

Durable/high-impact ADRs should require human approval according to the Human Authority Boundary.

# Failure handling

The protocol must explicitly cover:

* agent runs out of context
* quota expires
* terminal/network interruption
* tool failure
* partial implementation
* tests cannot be executed
* repository state is inconsistent
* prior HANDOFF is incomplete
* previous participant failed to leave evidence

In all such situations, the agent should leave the repository in the most resumable state possible rather than pretending completion.

# Fresh-agent onboarding

Include a standard prompt template for a completely new participant entering an existing project.

It should instruct the participant to:

1. read BOOTSTRAP
2. inspect repository structure
3. inspect PROJECT_SPEC / ADR / HANDOFF
4. independently review the relevant implementation
5. verify current claims where feasible
6. identify contradictions or unsupported assumptions
7. continue from the highest-priority safe next action
8. update evidence and HANDOFF before stopping

# Review prompt

Include a reusable independent-review prompt that tells a reviewer NOT to merely confirm the implementor's narrative.

The reviewer should inspect:

* specification compliance
* correctness
* regressions
* hidden assumptions
* architecture impact
* unnecessary complexity
* test sufficiency
* missing evidence
* contradictions between documentation and implementation

# Human checkpoint prompt

Include a reusable prompt that generates/updates HUMAN_CHECKPOINT.md without drowning the human in implementation details.

# Plug-and-play requirement

The final result should be usable in a new repository approximately like this:

1. copy the protocol template into the repo
2. fill in PROJECT_SPEC.md
3. give a coding agent the onboarding prompt
4. begin work

Avoid project-specific assumptions.

Do not assume a particular programming language, framework, CI provider, coding agent, or model vendor.

It should work with Codex, Claude Code, Gemini/Kimi-style coding agents, or future equivalents.

# Scope constraints

For this phase:

DO NOT build a web UI.
DO NOT build an agent orchestrator.
DO NOT build a daemon/service.
DO NOT build a complex CLI unless a tiny helper has obvious value.
DO NOT introduce databases.
DO NOT create unnecessary automation.

The primary deliverable is the protocol itself.

Prefer Markdown + simple filesystem conventions.

The protocol should remain usable even if all automation disappears and agents only have repository + shell access.

# Deliverables

Create:

1. A proposed directory structure.
2. Complete first versions of all protocol files.
3. Reusable prompts for:

   * fresh implementor/onboarding
   * resume interrupted work
   * independent reviewer
   * architecture drift review
   * human checkpoint generation
4. A README explaining:

   * what problem this protocol solves
   * philosophy
   * quick start
   * expected workflow
   * human role
   * agent role
   * limitations
5. One minimal fictitious example showing how the protocol would be initialized in a generic repository.

# Before implementation

First inspect the empty/new repository and propose the protocol architecture.

Explicitly identify:

* what artifacts you intend to create
* why each one exists
* which information belongs in which file
* how duplication between files will be avoided
* where project truth lives
* how human authority is preserved
* how agent continuity is preserved

Then implement the protocol.

# Quality bar

Optimize for:

clarity > cleverness
evidence > confidence
explicit state > conversational memory
small reversible changes > broad rewrites
contracts > inferred intent
human authority > autonomous architectural drift
independent review > self-certification
resumability > session continuity

The protocol should reduce the amount of trust required between sequential agent instances.

At completion:

* review your own generated protocol for contradictions and unnecessary complexity
* verify that a fresh agent could realistically use it without this prompt
* identify any unresolved design questions
* leave a concise final implementation report

# Post-pilot hardening requirements

The repository that develops this protocol MUST be a proof of the protocol's record architecture, not an exception to it.

## Accepted requirements

- **HARDEN-001 — Root adoption:** The root repository MUST use a root-specific adopted protocol instance with the source precedence and artifact ownership defined in accepted root ADR [`ADR-20260806T013907Z-root-protocol-adoption`](ADR/ADR-20260806T013907Z-root-protocol-adoption.md).
- **HARDEN-002 — Separate governance:** Root `BOOTSTRAP.md` and reusable `protocol/BOOTSTRAP.md` MUST remain separately governed. A change to one MUST NOT silently change the other. Material semantic divergence MUST be reviewed as an issue against the authority that governs each instance.
- **HARDEN-003 — Operational HANDOFF:** Root `HANDOFF.md` MUST remain a compact operational index with explicit snapshot metadata and staleness triggers, unresolved issues only, non-terminal background work only, exactly one next action, recent activity, and a durable archive index. It MUST NOT own requirements, architecture decisions, closed issue history, or evidence archives.
- **HARDEN-004 — Durable records:** Root architecture decisions, meaningful issue lifecycle, and substantial/review-critical evidence MUST live in root `ADR/`, `ISSUES/`, and `EVIDENCE/` records. `HUMAN_CHECKPOINT.md` MUST remain a non-authoritative owner summary and decision queue.
- **HARDEN-005 — Portable evidence claims:** Evidence MUST distinguish observations preserved in this repository from claims that depend on unavailable Git objects, external repositories, absolute local paths, or temporary artifacts. Missing external evidence MUST NOT be fabricated or described as reproducible. Production-grade, universal, or broader-portability validation MUST NOT be claimed without corresponding reproducible evidence.
- **HARDEN-006 — Package stability:** The reusable `protocol/` source bundle MUST retain its exact ten-file inventory and its Markdown-first, runtime-, language-, framework-, vendor-, CI-, and version-control-agnostic product boundary during this phase.
- **HARDEN-007 — Review gate:** The hardening implementation MUST remain in `REVIEW` and MUST NOT support a protocol-maturity claim until a fresh independent participant approves the immutable implementation target.
- **HARDEN-008 — Historical preservation:** Compaction MUST preserve prior findings, authorship, issue IDs, accepted decisions, evidence limitations, and an immutable pre-compaction revision/digest reference. Correction MUST be additive and attributable rather than silently rewriting historical evidence.

## Explicit non-goals and deferred scope

This phase MUST NOT implement or claim:

- guarantees for non-cooperating concurrent writers;
- cryptographically authenticated participant identity or approval;
- runtime automation, an orchestrator, daemon, service, database, or complex CLI;
- large-scale coordination fitness;
- external issue-tracker integration.

Each topic requires a separate issue and a new human-approved specification before investigation can adopt a solution. Recording a limitation does not authorize implementation.

## Hardening acceptance criteria

The hardening target is ready for independent review only when:

1. Root precedence, artifact ownership, Human Authority Boundary, issue lifecycle, evidence rules, and review rules are internally consistent.
2. Root HANDOFF satisfies its compact snapshot/index contract and links migrated durable records.
3. The reusable HANDOFF template and BOOTSTRAP contain compatible snapshot-metadata and staleness rules without changing the ten-file package inventory.
4. The isolated pilot evidence is preserved byte-for-byte in its durable evidence record, a root compatibility pointer resolves, and limitations match a Git-object audit.
5. Root and reusable relative links, Markdown integrity, package inventory, symlink absence, and isolated copy readiness are actually checked and recorded.
6. Unavailable tools and unperformed broader validation remain explicit.
7. An immutable target commit is supplied to a fresh independent reviewer; only a recorded `APPROVED` disposition can satisfy the maturity gate.

# Authorized milestone pipeline phase

This phase adds a bounded executable proof without changing the authority of Markdown requirements or making automation mandatory for adopters. The historical post-pilot prohibition on runtime automation remains true for that completed hardening phase. It is superseded only for the root-local capability and exact milestone defined below; all other hardening deferrals remain binding.

## Owner authority clarification

A milestone explicitly defined in an `ACCEPTED` `PROJECT_SPEC.md` is prior human authorization to begin and continue that milestone. It MUST NOT require a new human approval merely because implementation begins, verification completes, review begins, a within-scope fix is required, or the next already-authorized milestone becomes ready.

Autonomous continuation is permitted only while:

- the work remains within the milestone's accepted scope;
- the accepted specification and compatible accepted ADRs remain unchanged;
- no unresolved product or architecture ambiguity requires a new decision;
- no human checkpoint or blocked issue prevents the transition;
- every required deterministic verification passes; and
- a participant independent of the implementation instance reviews the immutable target before acceptance.

Human authority is required when the specification must change, scope would expand, an accepted architecture or invariant must change, a human-gated issue must be resolved, review exposes an ambiguity not answerable from existing authority, evidence cannot establish authorization, or an irreversible/high-impact external action lacks prior authorization. Implementation momentum, participant preference, an external task prompt, or an inferred useful next step does not create scope authority.

## Accepted pipeline requirements

- **PIPELINE-001 — Authority separation:** The pipeline MUST distinguish authorization, execution, deterministic verification, independent peer review, acceptance, and human escalation. Runtime state MUST NOT create or modify requirements or architecture.
- **PIPELINE-002 — Inspectable contracts:** Authorized milestones MUST be declared in the machine-readable contract below while the surrounding specification is `ACCEPTED`. The pipeline MUST reject missing, duplicate, malformed, unsupported, or digest-mismatched contracts rather than infer authorization.
- **PIPELINE-003 — Lifecycle:** The supported milestone states are `AUTHORIZED`, `READY`, `IN_PROGRESS`, `AWAITING_PEER_REVIEW`, `CHANGES_REQUIRED`, `ACCEPTED`, and `BLOCKED_HUMAN_AUTHORITY`. Only the transitions defined by the compatible accepted ADR are permitted.
- **PIPELINE-004 — Verification:** Orientation and submission MUST reuse the existing structural validator. Every milestone acceptance command MUST pass without a shell, with bounded runtime, and produce durable evidence. Failed or unavailable checks MUST NOT advance the milestone.
- **PIPELINE-005 — Peer review:** The reviewer label MUST differ from the recorded implementor label, the reviewed immutable target MUST match the verified target, and the disposition MUST be exactly `APPROVED`, `CHANGES_REQUIRED`, or `BLOCKED`. `APPROVED` requires zero open material findings. This label comparison is an operational check, not authenticated identity.
- **PIPELINE-006 — Fix and continuation:** Material findings MUST prevent acceptance and MAY return the milestone to implementation without human approval when their resolution remains within accepted scope. After acceptance, the pipeline MAY select the next dependency-satisfied milestone already present in this accepted contract without another human gate.
- **PIPELINE-007 — Durable resumability:** Machine state MUST be repository-resident, attributable, append-only in history, bound to the milestone contract digest, and recoverable without conversational memory. Human-readable issue and HANDOFF records MUST remain synchronized with it.
- **PIPELINE-008 — Bounded first slice:** The first implementation MUST be a Python 3.9-compatible, standard-library, root-only development tool. It MUST NOT enter the reusable ten-file package, invoke agents, commit or push, use the network, add a daemon/service/database/web UI, coordinate multiple hosts, integrate an external tracker, or claim cryptographic identity or concurrent-writer safety.

## Authorized milestone contract

The JSON object between the exact markers is normative content of this accepted specification. List order is milestone selection order. `scope` and `allowed_paths` bound work; runtime state may reference their canonical SHA-256 digest but MUST NOT copy or override them. `acceptance_checks` are owner-authorized local argv arrays executed with `shell=False`. An edit to this block is a material specification change.

<!-- AEP-AUTHORIZED-MILESTONES-V1:BEGIN -->
```json
{
  "schema": "aep-authorized-milestones/v1",
  "milestones": [
    {
      "id": "MILESTONE-20260814T015817Z-authorized-pipeline-v1",
      "order": 1,
      "title": "Root-local authorized milestone pipeline v1",
      "issue": "ISSUES/ISSUE-20260806T013907Z-runtime-automation.md",
      "depends_on": [],
      "scope": [
        "Codify the accepted milestone-authorization, review-loop, and human-escalation semantics in the root protocol and reusable Markdown templates.",
        "Implement and verify one root-only local state-and-gate pipeline capable of advancing authorized milestones without creating scope authority."
      ],
      "allowed_paths": [
        "BOOTSTRAP.md",
        "HANDOFF.md",
        "HUMAN_CHECKPOINT.md",
        "README.md",
        "ISSUES/ISSUE-20260806T013907Z-runtime-automation.md",
        "ISSUES/ISSUE-20260807T022523Z-pilot-onboarding-authority-friction.md",
        "ISSUES/ISSUE-20260811T030136Z-review-disposition-vocabulary.md",
        "ISSUES/TEMPLATE.md",
        "EVIDENCE/",
        "scripts/",
        "tests/",
        "protocol/BOOTSTRAP.md",
        "protocol/ISSUES/TEMPLATE.md",
        "protocol/PROJECT_SPEC.md",
        "protocol/PROMPTS.md",
        "protocol/README.md"
      ],
      "acceptance_checks": [
        {
          "id": "repository-unit-tests",
          "argv": [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v"
          ],
          "timeout_seconds": 120
        }
      ],
      "review": "INDEPENDENT"
    },
    {
      "id": "MILESTONE-20260814T051405Z-role-dispatch-v1",
      "order": 2,
      "title": "Automated role dispatch and rotation v1",
      "issue": "ISSUES/ISSUE-20260814T051405Z-role-dispatch.md",
      "depends_on": [
        "MILESTONE-20260814T015817Z-authorized-pipeline-v1"
      ],
      "scope": [
        "Codify implementer, independent-reviewer, and recorder/coordinator role contracts plus participant-eligibility and reviewer-independence rules in a durable root artifact.",
        "Implement and verify one root-only read-only dispatcher that derives the next required role decision from the accepted milestone contract and issue-embedded pipeline state, leaving host session invocation as an explicit adapter boundary."
      ],
      "allowed_paths": [
        "ROLE_CONTRACTS.md",
        "HANDOFF.md",
        "HUMAN_CHECKPOINT.md",
        "README.md",
        "ISSUES/ISSUE-20260814T051405Z-role-dispatch.md",
        "EVIDENCE/",
        "scripts/run_dispatch.py",
        "tests/test_run_dispatch.py"
      ],
      "acceptance_checks": [
        {
          "id": "repository-unit-tests",
          "argv": [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v"
          ],
          "timeout_seconds": 120
        }
      ],
      "review": "INDEPENDENT"
    }
  ]
}
```
<!-- AEP-AUTHORIZED-MILESTONES-V1:END -->

## Pipeline acceptance criteria

The authorized milestone is ready for peer review only when:

1. The accepted specification, accepted pipeline ADR, owning issue, machine state, and implementation agree on the milestone ID and contract digest.
2. The root-only tool exposes deterministic human- and machine-readable status plus validated state transitions without changing specification or ADR content.
3. Tests exercise the complete lifecycle, material-finding fix loop, reviewer-label separation, dependency-based next selection, human escalation, failure non-advancement, and stale-authority refusal.
4. The existing structural validator is reused rather than reimplemented, and the exact ten-file reusable bundle remains Markdown-only and copy-ready.
5. Verification evidence identifies the immutable target and records exact commands, outputs, limits, and unavailable checks.
6. A fresh independent participant reviews the immutable target. Only `APPROVED` with zero open material findings permits `ACCEPTED`; `CHANGES_REQUIRED` returns within-scope work to implementation, and `BLOCKED` cannot be mapped to approval.

No second real repository milestone is authorized by this phase. Multi-milestone continuation MUST be demonstrated with isolated fixtures; after this milestone is accepted, absence of another contract is a valid terminal result rather than permission to invent work.

# Automated role dispatch phase

This phase removes routine human intervention between already-authorized pipeline transitions by making the next required role, participant eligibility, and role contract deterministically decidable from durable repository state. It reuses the accepted milestone pipeline as the single state machine; it adds no new milestone states, no competing orchestration, and no host-specific session invocation. The pipeline phase's terminal note about the absence of a second contract is superseded only for the exact milestone defined below; all other deferrals remain binding.

The target lifecycle is: authorized work → implementer → verify → independent reviewer → fix/re-review when required → recorder/accept → next authorized milestone → repeat. Human escalation occurs only when existing repository authority is insufficient.

## Execution boundary

Repository-native dispatch ends at an emitted, deterministic next-role decision with its role contract. Host-specific participant or session invocation is an explicit adapter boundary outside this milestone's implementation. If the current host exposes no durable programmatic launch interface, the adapter remains a documented manual step and MUST NOT be simulated.

## Accepted dispatch requirements

- **DISPATCH-001 — Role contracts:** Implementer, independent reviewer, and recorder/coordinator role contracts MUST be codified in a durable root artifact stating each role's required inputs, permitted actions, required durable outputs, and completion conditions. The contracts MUST agree with root `BOOTSTRAP.md` and the accepted pipeline requirements and ADRs; runtime tools remain subordinate to them.
- **DISPATCH-002 — Eligibility and independence:** Participant eligibility MUST be deterministic from durable state. The independent-reviewer label MUST differ from the implementor label of the attempt under review, and the recorder/acceptance label MUST differ from both. No participant may review or accept its own implementation. Labels remain unauthenticated operational assertions, not identity.
- **DISPATCH-003 — Deterministic next-role decision:** Given only repository state, the dispatcher MUST select the next dependency-satisfied milestone through the existing pipeline and emit exactly one next-role decision — implementer, independent reviewer, recorder, human escalation, or terminal no-authorized-work — with the role contract reference, the eligibility constraints that bind the next participant, and the concrete records or commands that participant is expected to produce. Identical repository state MUST produce an identical decision.
- **DISPATCH-004 — Read-only decisions, durable transitions:** The dispatcher MUST NOT mutate repository state, create scope, or advance milestones. Decisions are derived on demand from durable state; transitions and their attribution remain recorded exclusively through the existing pipeline transitions and issue/HANDOFF records.
- **DISPATCH-005 — Interruption and resumption:** A fresh participant without conversational memory MUST be able to obtain the current dispatch decision in one read-only invocation, in human-readable and machine-readable form.
- **DISPATCH-006 — Integration, not competition:** The dispatcher MUST consume the accepted milestone contract and issue-embedded pipeline state through the existing pipeline implementation. It MUST NOT introduce a second state machine, duplicate authority sources, new milestone states, or a shadow issue database.
- **DISPATCH-007 — Host adapter boundary:** v1 MUST NOT assume a durable programmatic launch interface, invoke agents, or simulate invocation. The adapter boundary MUST be documented explicitly so a host with a genuine launch interface can implement it later without changing repository-native dispatch.
- **DISPATCH-008 — Bounded slice:** The dispatcher MUST be a Python 3.9-compatible, standard-library, root-only tool. It MUST NOT enter the reusable ten-file package, use the network, commit or push, mutate Git, or add a daemon, service, scheduler, database, web UI, or external tracker integration.

## Dispatch acceptance criteria

The dispatch milestone is ready for peer review only when:

1. The role-contract artifact covers implementer, independent reviewer, and recorder/coordinator and is consistent with root `BOOTSTRAP.md`, the accepted pipeline requirements and ADR, and the accepted pipeline issue's recorded lifecycle.
2. Dispatch decisions for every pipeline state — authorized/ready, in-progress, awaiting peer review, the fix/re-review loop, human escalation, post-acceptance continuation, and the terminal no-authorized-work case — are covered by deterministic tests, and repeated invocations over unchanged state produce byte-identical machine-readable output.
3. Eligibility and independence rules appear in emitted decisions and agree with the executable pipeline gates.
4. Dispatcher invocation changes no repository bytes, including issue, HANDOFF, specification, evidence, and Git state.
5. The host adapter boundary is documented as an explicit non-implemented interface; no simulated invocation exists anywhere.
6. A fresh independent participant reviews the immutable target. Only `APPROVED` with zero open material findings permits `ACCEPTED`; `CHANGES_REQUIRED` returns within-scope work to implementation, and `BLOCKED` cannot be mapped to approval.

# Specification governance

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
| `2026-08-05` | Accepted the initial standalone reusable protocol requirements | Establish the product contract | Human technical owner (`MattSureham`) | Pre-hardening specification at Git revision `e6beeb2cb730183ca2ac13795ad367ad9d9e1099`, SHA-256 `13169319e2be028c470ca96925002b25c000c58ba3a4c5420e652d291df139dd` |
| `2026-08-06T01:39:07Z` | Added accepted post-pilot hardening requirements, deferrals, acceptance criteria, and the approved specification-evolution policy | Resolve repository-verified dogfooding, record-separation, HANDOFF reliability, and evidence-portability gaps without expanding product runtime scope | Human technical owner (`MattSureham`) | [`ISSUE-20260806T013907Z-post-pilot-hardening`](ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md), [`ADR-20260806T013907Z-root-protocol-adoption`](ADR/ADR-20260806T013907Z-root-protocol-adoption.md), [`EVIDENCE-20260806T013907Z-post-pilot-audit`](EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md), authority boundary `7dea545` |
| `2026-08-14T01:58:17Z` | Accepted prior authorization for explicitly declared milestones and the bounded root-local automated pipeline phase | Allow deterministic implementation, verification, independent review, fix loops, and continuation without repeated human prompts while preserving explicit scope and escalation boundaries | Human technical owner (`MattSureham`) | [`ISSUE-20260806T013907Z-runtime-automation`](ISSUES/ISSUE-20260806T013907Z-runtime-automation.md), [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md), [`EVIDENCE-20260814T015817Z-pipeline-authority-analysis`](EVIDENCE/EVIDENCE-20260814T015817Z-pipeline-authority-analysis.md) |
| `2026-08-14T05:14:05Z` | Accepted the automated role dispatch phase and a second contract milestone for role contracts, eligibility rules, and a deterministic read-only next-role dispatcher with an explicit host adapter boundary | Eliminate routine human intervention between already-authorized pipeline transitions while keeping the accepted pipeline as the single state machine and leaving host session invocation outside repository authority | Human technical owner (`MattSureham`) | [`ISSUE-20260814T051405Z-role-dispatch`](ISSUES/ISSUE-20260814T051405Z-role-dispatch.md), [`ADR-20260814T051405Z-automated-role-dispatch`](ADR/ADR-20260814T051405Z-automated-role-dispatch.md) |
