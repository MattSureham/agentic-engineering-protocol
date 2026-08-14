# ADR-20260814T051405Z: Adopt Automated Role Dispatch With an Explicit Host Adapter Boundary

## Metadata

- **ID:** `ADR-20260814T051405Z-automated-role-dispatch`
- **Title:** Adopt deterministic repository-native role dispatch and leave host session invocation as an adapter boundary
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-14T05:14:05Z`
- **Author:** `ClaudeCode/root`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` through the explicit Automated Role Dispatch / Rotation v1 owner direction received before implementation on `2026-08-14`
- **Related specification:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase
- **Related ADRs:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR-20260814T015817Z-authorized-milestone-pipeline.md), [`ADR-20260806T013907Z-root-protocol-adoption`](ADR-20260806T013907Z-root-protocol-adoption.md)
- **Related issues:** [`ISSUE-20260814T051405Z-role-dispatch`](../ISSUES/ISSUE-20260814T051405Z-role-dispatch.md)
- **Supersedes / superseded by:** Supersedes nothing; extends the accepted pipeline architecture with a read-only decision layer; superseded by `NONE`

Only `ACCEPTED` ADRs are authoritative. This record is accepted before implementation because the human technical owner approved the decision-complete direction and scope. The resulting milestone still requires independent review before acceptance.

## Context

The accepted milestone pipeline (`MILESTONE-20260814T015817Z-authorized-pipeline-v1`, independently approved and accepted on `2026-08-14`) makes lifecycle transitions deterministic and durable, but the space *between* transitions still depends on operator judgment: after every recorded boundary, someone must infer which role is needed next, who is eligible to fill it, and what that participant must produce. During the pipeline milestone itself, those routing decisions were made by reading HANDOFF prose and review records by hand — workable, but exactly the kind of routine intervention the owner has now directed the repository to eliminate for already-authorized work.

The owner direction requires the repository to determine the next required role, participant eligibility, and role contract from durable project state, across the lifecycle: authorized work → implementer → verify → independent reviewer → fix/re-review when required → recorder/accept → next authorized milestone → repeat. Human escalation occurs only when existing repository authority is insufficient.

A hard constraint shapes the architecture: the host environment cannot be assumed to launch agent sessions programmatically. The owner direction explicitly requires the execution boundary between repository-native dispatch decisions and host-specific participant/session invocation to be determined and documented first, and prohibits simulating a launch interface that may not exist.

## Decision

1. **Execution boundary split.** Dispatch has two halves with different authorities. Repository-native dispatch — selecting the milestone, reading its durable state, and emitting the next-role decision with its contract — is implemented in this repository and is deterministic. Host-specific invocation — starting a session that performs the emitted role — is an adapter boundary owned by the operator/host and is not implemented in v1. v1's adapter is a documented manual step: the operator starts the next session and supplies the emitted role contract.
2. **Role contracts are durable root records.** Implementer, independent reviewer, and recorder/coordinator contracts live in root `ROLE_CONTRACTS.md`: required inputs, permitted actions, required durable outputs, and completion conditions per role. The artifact is normative guidance subordinate to `PROJECT_SPEC.md` and accepted ADRs; it does not create scope and does not enter the reusable ten-file package.
3. **Eligibility is deterministic and label-based.** The reviewer label must differ from the implementor label of the attempt under review; the recorder/acceptance label must differ from both. These are operational assertions, not authenticated identity, exactly as in the accepted pipeline ADR.
4. **The dispatcher is read-only.** It loads the accepted contract and issue-embedded pipeline state through the existing pipeline implementation, emits a decision, and changes no repository bytes. It never advances, creates, or overrides milestone state; the pipeline transitions remain the only mutation path.
5. **One decision per repository state.** The emitted decision names exactly one next role — implementer, independent reviewer, recorder, human escalation, or terminal no-authorized-work — plus the selected milestone, current state, eligibility constraints that bind the next participant, the role contract reference, and the concrete records/commands the next participant is expected to produce. Identical repository state produces byte-identical machine-readable output; the output carries no timestamps or environment data.
6. **No competing state machine.** The dispatcher adds no milestone states, no shadow issue store, and no duplicate authority source. When the pipeline reports no selected milestone, dispatch reports the terminal result rather than inventing work.
7. **Host invocation is not simulated.** No code path pretends to launch a participant. The adapter boundary is documented so a host with a genuine durable launch interface can implement it later without changing repository-native dispatch.
8. **Bounded root-only tool.** Python 3.9, standard library, no network, no Git mutation, no daemon/service/scheduler/database/web UI/tracker, and no change to the reusable package.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** This changes how already-authorized work is routed between participants and adds a new maintained runtime component that reads authority-bound state.
- **Existing authorization:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase, approved through the explicit owner direction of `2026-08-14T05:14:05Z` and recorded through the specification-evolution mechanism.
- **Approval evidence:** Human technical owner `MattSureham` directed Automated Role Dispatch / Rotation v1 with its goal, lifecycle, v1 scope, execution-boundary requirement, and exclusions; the accepted specification change and this ADR persist that authority.

## Alternatives considered

### Require a human routing decision at every role boundary

- **Benefits:** No new runtime component.
- **Costs and risks:** Repeats a decision that durable state already determines, keeps conversational continuity an operational dependency, and preserves the exact friction the owner directed to remove.
- **Reason not selected:** The owner explicitly directed deterministic dispatch from repository state for already-authorized work.

### Extend the accepted pipeline tool with a dispatch subcommand

- **Benefits:** One entry point for status, transitions, and dispatch.
- **Costs and risks:** Modifies the independently approved and accepted pipeline tool, enlarging its review surface and coupling a read-only decision feature to the mutation-path tool.
- **Reason not selected:** A separate read-only script that imports the pipeline's parsers integrates without touching the accepted implementation; a subcommand remains possible in a later milestone if operation proves it preferable.

### Implement host-specific session invocation now

- **Benefits:** Would close the loop end to end on hosts that support it.
- **Costs and risks:** Assumes a durable programmatic launch interface the current host is not verified to expose, couples repository authority to one vendor's session machinery, and risks simulating capability that does not exist.
- **Reason not selected:** The owner direction explicitly forbids assuming or simulating the launch interface and requires the adapter boundary instead.

### Build a general agent orchestrator or scheduler

- **Benefits:** Could manage concurrent participants and retries.
- **Costs and risks:** Process lifecycle, concurrency, persistence, and security commitments far beyond the directed scope.
- **Reason not selected:** Explicitly excluded by the owner direction and by the accepted scope constraints.

## Consequences

### Positive

- A fresh participant or operator can learn the next required role, its contract, and its eligibility constraints in one read-only invocation, with no conversational memory.
- Routing decisions become reproducible and auditable: the same repository state always yields the same decision, and every acted-on transition is already recorded by the pipeline.
- Human attention is reserved for genuine authority gaps; routine sequencing no longer waits on an operator reading HANDOFF prose.
- The host adapter boundary keeps the repository honest about what it cannot do, and leaves a clean extension point.

### Negative and tradeoffs

- The root repository gains a second maintained Python component whose output must stay consistent with pipeline gates and role-contract prose; drift between them is a reviewed risk.
- Dispatch decisions are only as fresh as the durable records they read; an unrecorded local change is invisible to them by design.
- Label-based eligibility remains an operational assertion, not authentication.
- The loop is not closed: an operator still starts each session manually in v1.

### Compatibility and migration

- The accepted pipeline tool, its tests, and its accepted issue records are unchanged; the dispatcher consumes them read-only.
- Existing non-pipeline issues are unaffected; dispatch selects only contract milestones.
- The reusable package remains ten Markdown files with no runtime; adopters may continue manual routing indefinitely.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Second root Python tool sharing pipeline parsers | Deterministic next-role decisions without a competing state machine | Dispatch tests across every pipeline state plus exact-target evidence | Semantic adequacy of routing remains reviewer judgment |
| Root role-contract artifact | Durable, reviewable role expectations shared by humans, agents, and the dispatcher | Acceptance criteria require consistency with BOOTSTRAP and pipeline semantics | Prose/tool drift must be caught by review and tests |
| Label-based eligibility extension to recorder | Minimal independence condition for acceptance recording | Emitted-constraint tests and existing executable gate agreement | Authentication remains [`ISSUE-20260806T013907Z-authenticated-identity-approval`](../ISSUES/ISSUE-20260806T013907Z-authenticated-identity-approval.md) |

## Evidence and assumptions

- **CONFIRMED:** The accepted pipeline exposes importable contract/state parsers and a read-only status path used successfully for the full first milestone lifecycle.
- **CONFIRMED:** The first milestone's inter-transition routing was performed manually from HANDOFF and issue records; that observation motivates this phase and is preserved in the accepted issue's activity history.
- **CONFIRMED:** The owner direction prohibits a web UI, distributed scheduler, database, external tracker, and unrelated orchestration infrastructure, and requires the adapter boundary over simulation.
- **INFERRED:** A read-only decision script is the smallest design that satisfies the direction without modifying the accepted pipeline tool.
- **UNKNOWN:** Whether any current or future host exposes a durable programmatic launch interface suitable for a real adapter; portability beyond the recorded Darwin/Python environment; behavior under non-cooperating writers (unchanged from the pipeline failure model).

## Independent review rounds

- **Required:** `YES` — the milestone adds a runtime component that reads authority-bound state and changes how already-authorized work is routed.

No independent review round has been recorded. Review the immutable dispatch implementation target and the complete owning-issue round together. An `APPROVED` round on that target may satisfy this ADR's review intent when its scope explicitly includes this decision.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-14T05:14:05Z` | `NONE` | `ACCEPTED` | Human technical owner `MattSureham`, recorded by `ClaudeCode/root` | Explicit Automated Role Dispatch / Rotation v1 owner direction; accepted root specification change records the product authority |
