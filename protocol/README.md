# Agent-Native Software Engineering Protocol

This package is a lightweight, repository-native operating system for long-running software work performed by replaceable coding-agent instances under a human technical owner. It makes work resumable, auditable, evidence-driven, independently reviewable, and resistant to architecture drift without requiring an orchestrator, service, database, or hidden conversation history.

> **Agent continuity without agent identity.**
>
> **Agents are ephemeral; project state is durable.**
>
> *牲口没有身份，磨盘有记忆。*

Project continuity MUST NOT depend on agent identity or session continuity. Individual coding-agent sessions are replaceable, and no agent instance owns project truth. Durable state belongs in repository artifacts: `PROJECT_SPEC.md`, accepted ADRs, executable tests and contracts, recorded evidence, `HANDOFF.md`, and Git history when available. A fresh participant must be able to resume from those artifacts without prior conversational context. Continuity belongs to the project, not to an agent session.

Participant attribution still matters for auditability, independent-review provenance, and human approvals; it does not confer ownership of project truth. Git history preserves provenance and recovery context, but it does not create a new source-of-truth tier or change the precedence defined by this protocol.

## The problem it solves

Agent throughput can exceed a human owner's ability to read every diff. Sequential agents can also amplify an unsupported assumption until an internally consistent implementation diverges from the actual requirement. Chat transcripts, agent memory, and code alone are poor continuity mechanisms.

This protocol keeps authority and evidence in the repository. It gives agents enough operational state to continue safely while reserving durable product and architecture decisions for explicit human authority.

## Philosophy

- Requirements and accepted decisions outrank whatever code happens to exist.
- Evidence is more useful than confidence or polished summaries.
- Agents are temporary peer participants, not permanent supervisors or trusted narrators.
- Local reversible implementation can move quickly; durable commitments cross a human authority boundary.
- Review is proportionate to risk: low-risk local work records self-review, while contract, architecture, security, state, dependency, concurrency, coupling, and material-complexity changes require an independent participant.
- Complexity without contract, test, or evidence coverage remains visible debt.
- A coherent handoff is more valuable than squeezing one more change into a failing session.

The exact operational rules and truth hierarchy live in [`BOOTSTRAP.md`](BOOTSTRAP.md).

## Package contents

| Artifact | Purpose |
|---|---|
| [`BOOTSTRAP.md`](BOOTSTRAP.md) | Normative instructions for starting, working, verifying, reviewing, escalating, and handing off. |
| [`PROJECT_SPEC.md`](PROJECT_SPEC.md) | Human-owned requirements and acceptance template. |
| [`HANDOFF.md`](HANDOFF.md) | Compact current operational state and resumability record. |
| [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md) | Low-bandwidth architecture and decision synchronization for the owner. |
| [`ADR/`](ADR/) | Durable architectural decisions and rationale. |
| [`ISSUES/`](ISSUES/) | Detailed lifecycle records for meaningful work and uncertainty. |
| [`EVIDENCE/`](EVIDENCE/) | Reproducible proof and provenance for important claims. |
| [`PROMPTS.md`](PROMPTS.md) | Fresh, resume, review, drift, and checkpoint prompts. |
| [`EXAMPLE.md`](EXAMPLE.md) | A synthetic minimal initialization walkthrough. |

## Quick start

1. Preflight every package path and choose the applicable migration path.

   For a new or deliberately prepared repository with no conflicts, copy the package contents into its root:

   ```sh
   cp -R /path/to/agentic-engineering-protocol/protocol/. /path/to/your-repository/
   ```

   For an established repository, do not use that bulk-copy command. Instead:

   1. Inventory existing specifications, architecture records, agent instructions, handoff history, issues, evidence, and application documentation.
   2. Preserve the application `README.md`. When that path already exists, copy this package guide under the canonical migration name `PROTOCOL_GUIDE.md`:

      ```sh
      cp /path/to/agentic-engineering-protocol/protocol/README.md /path/to/your-repository/PROTOCOL_GUIDE.md
      ```

   3. Add a short navigation section to the application README without removing its existing content:

      ```markdown
      ## Agent-Native Engineering Protocol

      Participants must read [BOOTSTRAP.md](BOOTSTRAP.md) before working in this repository. Adoption guidance is in [PROTOCOL_GUIDE.md](PROTOCOL_GUIDE.md).
      ```

   4. Copy only non-conflicting protocol artifacts. Deliberately merge or map every collision, preserving existing authority, authorship, HANDOFF history, ADRs, issues, and evidence. Never overwrite them merely to complete installation.
   5. Keep `PROTOCOL_GUIDE.md` at the repository root and verify that the application README links to both it and `BOOTSTRAP.md`; the guide's package-relative links must also resolve there.

2. Replace the placeholders in `PROJECT_SPEC.md`. The human technical owner records acceptance before agents implement affected product behavior.
3. Give a fresh participant the **Fresh implementor or onboarding** prompt from `PROMPTS.md`.
4. The participant inspects the repository, replaces the template HANDOFF snapshot with evidence-backed state, identifies active work, and begins from one bounded safe action.
5. Keep the protocol files in version control when available. Git is useful but not required; record hashes or other durable file state when commits are unavailable.

See [`EXAMPLE.md`](EXAMPLE.md) for a small filled-in illustration.

## Expected workflow

1. A participant reads BOOTSTRAP and independently inspects current truth.
2. It selects or creates an issue and classifies authority and review requirements.
3. It reproduces or establishes the problem before changing behavior.
4. It implements a small scoped change and records proportional verification.
5. Low-risk local work records attributable self-review; the risk categories defined in BOOTSTRAP require independent review, and durable architecture requires prior human authority.
6. Durable facts stay in the specification, ADR, contracts, or evidence. HANDOFF retains only what the next participant needs operationally.
7. Before stopping, the participant reconciles background work and leaves exactly one next action.

Temporary roles can include Implementor, Reviewer, Verification Agent, Risk Reviewer, and Architecture Reviewer. They are roles for a task, not a permanent hierarchy.

## Human technical owner

The owner defines requirements, accepts durable architectural commitments, decides major tradeoffs, and periodically checks the system mental model through `HUMAN_CHECKPOINT.md`. The owner should not need to inspect every local refactor or routine defect fix.

The checkpoint concentrates attention on changed boundaries, complexity, assumptions, drift, uncertainty, and explicit decisions. Product decisions are persisted into `PROJECT_SPEC.md`, architecture decisions into an ADR, and mixed decisions into both so later agents do not depend on missing chat.

## Agent participants

Agents handle investigation, routine implementation, tests, evidence capture, issue maintenance, review, and resumable handoff. They may decide local reversible details within accepted contracts. They must surface contradictions and escalate durable commitments rather than treating implementation momentum as authority.

Independent reviewers should challenge the premise of a change, not just its mechanics. Disagreement creates an investigation path; it is neither erased nor automatically treated as an error.

## Adopting in an existing repository

- Use the established-repository migration path in Quick start. Keep the application README, the canonical `PROTOCOL_GUIDE.md` alias, and links to both the guide and normative `BOOTSTRAP.md`.
- Inventory current specifications, architecture records, issue trackers, agent instructions, and handoff documents before copying anything.
- Preserve authorship and useful history. Map existing authoritative requirements into `PROJECT_SPEC.md` and durable accepted decisions into ADRs.
- Record unresolved contradictions instead of choosing a source silently.
- Start HANDOFF as a present snapshot with links; do not paste an entire historical changelog into it.
- Keep external issue trackers or CI systems if useful, but preserve enough durable repository context that an agent without those sessions can identify and safely resume work.
- Add model- or tool-specific instruction shims only as optional pointers to `BOOTSTRAP.md`; do not fork the normative rules across vendors.

## Limitations

- Markdown cannot enforce compliance; participants and reviewers must follow the protocol.
- The protocol improves evidence quality but cannot prove that tests, specifications, or human decisions are themselves correct.
- Independent review reduces correlated error but does not eliminate it.
- Concurrent participants can still create merge conflicts; repository-unique timestamp IDs reduce record allocation collisions but do not coordinate code edits.
- Sensitive or very large evidence may require an external durable store with retention and access controls.
- A human owner remains necessary for product ambiguity, risk acceptance, and durable architectural authority.
- The templates require initial adaptation. An unfilled `DRAFT` specification intentionally blocks unsupported product implementation.

## Evolving the protocol

Treat changes to source precedence, authority boundaries, required records, or review gates as durable architecture changes. Propose them with compatibility and migration consequences, obtain owner approval, and preserve prior records. Local wording improvements that do not change meaning should still be attributable and reviewed for contradiction.
