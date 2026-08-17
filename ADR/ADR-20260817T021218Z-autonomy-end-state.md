# ADR-20260817T021218Z: Adopt the Product-Level Autonomy Acceptance Boundary and Live-Operation Profile

## Metadata

- **ID:** `ADR-20260817T021218Z-autonomy-end-state`
- **Title:** Gate the autonomy objective on a demonstrated unattended end-to-end run, and bind live participant launches to a probe-verified minimal profile
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-17T02:12:18Z`
- **Author:** `ClaudeCode/root`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` through the explicit product-level autonomy owner direction received before implementation on `2026-08-17`
- **Related specification:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Product-level autonomy objective and Live invocation and autonomy demonstration phase
- **Related ADRs:** [`ADR-20260814T092504Z-host-adapter-rotation`](ADR-20260814T092504Z-host-adapter-rotation.md), [`ADR-20260814T051405Z-automated-role-dispatch`](ADR-20260814T051405Z-automated-role-dispatch.md), [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR-20260814T015817Z-authorized-milestone-pipeline.md)
- **Related issues:** [`ISSUE-20260817T021218Z-live-invocation`](../ISSUES/ISSUE-20260817T021218Z-live-invocation.md), [`ISSUE-20260817T021218Z-autonomy-demonstration`](../ISSUES/ISSUE-20260817T021218Z-autonomy-demonstration.md)
- **Supersedes / superseded by:** Supersedes nothing; interprets all prior component milestones as enabling capabilities and narrows the rotation ADR's probed-interface boundary only by extending the probe record to the minimal tool-enabled profile; superseded by `NONE`

Only `ACCEPTED` ADRs are authoritative. This record is accepted before implementation because the human technical owner approved the decision-complete direction and scope. The resulting milestones still require independent review before acceptance.

## Context

Three automation milestones are accepted and closed — the milestone pipeline, the read-only dispatcher, and the participant-rotation runner — and the dispatcher sits at the terminal `ROLE none` idle state. Yet the owner's actual objective is unmet: no real participant session has ever been launched by the system (the committed registry pins `tools` to the probed empty value, which cannot perform file-editing roles), and every lifecycle transition to date was executed by a manually started participant.

The specification audit traces this to a structural gap, not an implementation defect. Each phase scoped its acceptance criteria to component behavior; the pipeline phase explicitly made the absence of a further contract "a valid terminal result"; and the rotation phase required stub-only tests. No top-level requirement distinguished "components accepted" from "objective met", and no acceptance criterion ever required the composed system to run live. The terminal idle state was correct per contract — it prevents scope invention — but nothing prevented it from being read as completion.

The owner direction resolves this: the end state is unattended progression of already-authorized milestones through the full lifecycle, proven by a real end-to-end dogfood run with verified host invocation and multiple distinct participant roles, with stub-only execution explicitly insufficient.

## Decision

1. **Autonomy is a product-level acceptance boundary, not a milestone property.** The objective is established exclusively by demonstrated live operation (`AUTONOMY-004`): one bounded runner invocation, multiple distinct launched roles, at least one real authorized milestone progressed `AUTHORIZED` → `ACCEPTED`. Component milestones remain enabling capabilities; their acceptance can never be presented as objective completion (`AUTONOMY-006`).
2. **Terminal idle is not completion.** `ROLE none` remains the correct terminal result of the contract model — absence of authorized work must never invent work — but before the demonstration exists it is an idle state, not evidence of autonomy.
3. **Live launches use a minimal probe-verified profile.** The evidence-bounded interface rule extends unchanged: any launch configuration beyond the originally probed `tools ""` profile requires new recorded probe evidence (including tool-enabled operation and headless permission behavior) before reliance, and the live profile is the smallest set that lets a launched participant perform the role contracts. Unrecognized behavior fails closed through the existing taxonomy; participant-side failure never gains a new escalation path to human authority.
4. **The demonstration milestone is its own vehicle.** `MILESTONE-20260817T021218Z-autonomy-demonstration-v1` carries a small real change (root `ISSUES/TEMPLATE.md` activity-section conformance with the pipeline's table-only gate — a drift already recorded by the rotation review) and is itself progressed by runner-launched implementer, reviewer, and recorder participants. The durable ledger, pipeline events, review round, and reconciliation records are the objective proof standard (`AUTONOMY-005`); the recorder verifies the implementer and reviewer legs from durable records at closure, and the complete account remains auditable after acceptance.
5. **Human authority is unchanged.** The system stops for the owner only on genuine new authority needs, exhausted declared bounds, or absence of authorized work. Publication, scope, and architecture authority stay exactly where the accepted phases put them.
6. **Dependency ordering prevents premature completion readings.** The demonstration milestone depends on the live-invocation milestone: if the runner cannot operate live, the capability milestone — not the dogfood run — absorbs the fix loop, keeping the demonstration's acceptance evidence clean.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** This elevates unattended multi-role automation to a product-level requirement and authorizes real launched participants that edit, commit, and record transitions on authority-bound state with widened (probe-verified) tool access.
- **Existing authorization:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Product-level autonomy objective and Live invocation and autonomy demonstration phase, approved through the explicit owner direction of `2026-08-17` and recorded through the specification-evolution mechanism.
- **Approval evidence:** Human technical owner `MattSureham` directed the end state, its stop conditions, the mandatory real dogfood acceptance criterion, the audit-and-evolve method, and the preservation of prior milestone history; the accepted specification change and this ADR persist that authority.

## Alternatives considered

### Declare the objective met by the accepted components

- **Benefits:** No further work.
- **Costs and risks:** Asserts a capability never exercised: zero live launches, zero unattended progressions, and a committed registry whose profile cannot edit files.
- **Reason not selected:** The owner direction explicitly rejects component existence as completion and requires a real dogfood run.

### Fold capability probing into the demonstration milestone

- **Benefits:** One fewer milestone.
- **Costs and risks:** If tool-enabled headless operation behaves unexpectedly, the dogfood run itself enters fix loops, contaminating the acceptance evidence that is supposed to prove clean unattended operation.
- **Reason not selected:** Evidence-first ordering — probe and conform the profile, then demonstrate — keeps the demonstration's evidence interpretable; two milestones is the minimum honest decomposition.

### Demonstrate on a synthetic fixture repository instead of this one

- **Benefits:** No live automation acts on the real governance records during the first run.
- **Costs and risks:** A fixture demonstration would not establish the product claim "the system progresses this repository's authorized milestones"; it would re-create exactly the simulation gap the owner direction closes.
- **Reason not selected:** This repository is the dogfood by design; fixture-based testing remains the unit-test strategy, not the product proof.

### Add a supervising orchestrator for the live run

- **Benefits:** Could manage long-running supervision concerns.
- **Costs and risks:** The excluded infrastructure class (daemon/scheduler) and a second authority path.
- **Reason not selected:** The accepted bounded runner plus durable ledger already covers bounded execution and recovery; the owner direction adds no such scope.

## Consequences

### Positive

- The specification now distinguishes enabling capability from objective completion, so future terminal idle states cannot be misread as autonomy.
- The acceptance proof is durable and independently checkable from repository records alone: ledger, pipeline events, review round, and reconciliation.
- The live profile is pinned to evidence, keeping the fail-closed adapter discipline intact as capability widens.
- Prior milestone history is untouched; their acceptance records remain valid as enabling capabilities.

### Negative and tradeoffs

- The first live run spends real quota and lets launched sessions edit and commit on the real repository within allowed paths; declared bounds and the pipeline's gates mitigate but do not eliminate that operational risk.
- The self-demonstrating milestone's acceptance evidence is partly assembled post-hoc by the recorder; its completeness is a review responsibility recorded in the demonstration criteria.
- Widened tool profiles enlarge the probed surface; each widening requires its own probe record, adding operational ceremony.

### Compatibility and migration

- All accepted tools, contracts, and records are unchanged; the live-invocation milestone may modify only its allowed paths.
- The reusable package remains ten Markdown files with no runtime; the vehicle fix touches only the root `ISSUES/TEMPLATE.md`.
- The four `BLOCKED` capability deferrals remain deferred.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Live tool-enabled participant launches | The objective cannot be demonstrated otherwise | New probe evidence plus stub-suite conformance under the live-invocation milestone | Headless permission behavior and long-running session stability only become known through the probes; residual UNKNOWNs stay owned by the live-invocation issue |
| Self-demonstrating acceptance evidence | Minimal decomposition: the dogfood needs real authorized work, and the milestone's own lifecycle is the smallest real vehicle | Demonstration acceptance criteria plus recorder closure verification | Post-hoc assembly completeness remains reviewer judgment |

## Evidence and assumptions

- **CONFIRMED:** All three component milestones are `ACCEPTED` with owning issues `CLOSED`; the dispatcher emits `ROLE none`; no real participant has ever been launched by the system; the committed registry pins `tools: ""`.
- **CONFIRMED:** The owner direction requires the recorded end state, its stop conditions, a mandatory real dogfood acceptance criterion, audit-before-implementation, preservation of prior milestone history, and a six-point completion report.
- **CONFIRMED:** The pipeline gate requires the root issue template's activity section to contain only a Markdown table, and the root `ISSUES/TEMPLATE.md` carries a prose line there — a real, bounded vehicle change recorded by the rotation milestone's review.
- **INFERRED:** Two milestones — capability then demonstration — are the minimum decomposition that keeps the demonstration's acceptance evidence clean. Facts: the live profile is unprobed today; the demonstration must run on a conformed profile; the dependency ordering enforces that sequence.
- **UNKNOWN:** Whether the minimal tool-enabled headless profile behaves as the probes will establish; host rate limits and long-running session stability; whether the first unattended run completes within declared bounds.

## Independent review rounds

- **Required:** `YES` — both resulting milestones change how authority-bound state is acted upon (live profile) or constitute the product-level proof (demonstration).

No independent review round has been recorded. Each milestone's immutable target is reviewed under the standard gate; the demonstration milestone's review scope explicitly includes this decision and the AUTONOMY-005 evidence account.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-17T02:12:18Z` | `NONE` | `ACCEPTED` | Human technical owner `MattSureham`, recorded by `ClaudeCode/root` | Explicit product-level autonomy owner direction; accepted root specification change records the product authority |
