You are creating a standalone, reusable engineering protocol for long-running software projects developed and maintained primarily by coding agents, with a human technical owner retaining architectural authority.

This work MUST be independent of any existing product repository.

Do NOT modify or depend on any existing project such as PCB, CAD, memory systems, or other application-specific repositories.

The output should be a self-contained template/protocol that can later be copied or initialized inside an arbitrary software repository with minimal adaptation.

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
