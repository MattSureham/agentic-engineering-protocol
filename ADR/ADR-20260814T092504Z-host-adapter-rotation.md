# ADR-20260814T092504Z: Adopt an Evidence-Bounded Host Adapter for Automated Participant Rotation

## Metadata

- **ID:** `ADR-20260814T092504Z-host-adapter-rotation`
- **Title:** Execute dispatcher decisions through the probe-verified host CLI launch interface with a durable participant registry, rotation ledger, and failure taxonomy
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-14T09:25:04Z`
- **Author:** `ClaudeCode/root`
- **Human technical owner:** `MattSureham`
- **Owner approval:** `APPROVED` through the explicit host adapter / automated participant rotation owner direction received before implementation on `2026-08-14`
- **Related specification:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Host adapter and participant rotation phase
- **Related ADRs:** [`ADR-20260814T051405Z-automated-role-dispatch`](ADR-20260814T051405Z-automated-role-dispatch.md), [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR-20260814T015817Z-authorized-milestone-pipeline.md), [`ADR-20260806T013907Z-root-protocol-adoption`](ADR-20260806T013907Z-root-protocol-adoption.md)
- **Related issues:** [`ISSUE-20260814T092504Z-host-adapter-rotation`](../ISSUES/ISSUE-20260814T092504Z-host-adapter-rotation.md)
- **Related evidence:** [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md)
- **Supersedes / superseded by:** Supersedes the manual-only adapter stance of [`ADR-20260814T051405Z-automated-role-dispatch`](ADR-20260814T051405Z-automated-role-dispatch.md) decision 1 solely for the milestone defined in the rotation phase; that ADR's precondition ("a host that exposes a genuine durable launch interface") is now evidence-satisfied; superseded by `NONE`

Only `ACCEPTED` ADRs are authoritative. This record is accepted before implementation because the human technical owner approved the decision-complete direction and scope. The resulting milestone still requires independent review before acceptance.

## Context

The accepted dispatch milestone emits a deterministic next-role decision but deliberately stops at the adapter boundary: in v1 the operator starts each session by hand. The owner has now directed continuing toward automated participant rotation, with explicit constraints: do not invent a Paseo/session API that has not been verified to exist; establish the host capability boundary from evidence first; keep repository state authoritative; adapters execute dispatch decisions and never redefine scope, eligibility, or semantics; participant failures (including quota exhaustion) must not be escalated as human-authority gaps; if no programmatic interface exists, implement only the actually-supported boundary.

The capability question is now answered by live probe evidence ([`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md)): no `paseo` binary or project exists on this host; the Claude Code CLI at version `2.1.118` provides programmatic headless sessions (`claude -p`) returning structured JSON result envelopes with exit-code signaling, per-session durable identity with `--resume`, budget caps, and a machine-readable budget-exhaustion class (`error_max_budget_usd`, exit `1`, `is_error: true`) that is distinct from any authority gap. Because a genuine durable launch interface is verified, the accepted dispatch ADR's conditional extension point applies.

## Decision

1. **Evidence-bounded interface.** The adapter targets exactly the probed behavior of the host CLI: headless launch with a prompt, `--output-format json` result envelopes, `--max-budget-usd` spend caps, `--tools` restriction, exit-code plus `subtype` outcome classification, and `--resume` session re-entry. Any envelope shape or behavior outside the probe record is unrecognized input and must fail closed. No Paseo or other unverified session API is referenced anywhere.
2. **Dispatcher is the sole routing authority.** The rotation runner consumes `scripts/run_dispatch.py --json` and nothing else for routing. It substitutes a concrete eligible participant label into the emitted expected commands; it never re-derives role, milestone, eligibility, or scope, and never issues transitions the dispatcher did not emit.
3. **Registry plus independence filtering.** Eligible participants are declared in root `ROTATION_PARTICIPANTS.json` with per-participant launch configuration. Before any launch, candidates are filtered against the dispatcher's emitted eligibility constraints (reviewer ≠ attempt implementor; recorder ≠ both). An exhausted pool is an explicit stop outcome, not an escalation.
4. **Failure taxonomy without false escalation.** Outcomes are classified as `success_advancing`, `launch_failure`, `quota_exhausted`, `session_error`, `timeout`, or `non_advancing`. Participant failures trigger bounded retry or rotation only; they never produce a `BLOCKED_HUMAN_AUTHORITY` transition. Human escalation remains exactly what the pipeline and dispatcher already emit.
5. **Append-only rotation ledger.** Every step — launch, classification, retry, rotation, stop — is appended to root `ROTATION_LOG.jsonl` with participant label, session identity where reported, outcome class, and cost where reported. The ledger is adapter-owned operational evidence; pipeline state in the owning issue remains authoritative.
6. **Repository-state recovery.** After interruption, the runner re-reads the dispatcher decision and reconciles against the ledger. A session recorded as launched but with no recorded outcome is treated as an in-flight attempt to be classified by re-reading repository state (did the expected transition land?) before any retry; duplicate transitions are forbidden.
7. **Declared bounds.** Maximum attempts per decision, maximum steps per invocation, and maximum spend per invocation are explicit runner inputs with registry defaults. Exhaustion stops the runner with a recorded reason.
8. **Tests never launch real sessions.** The suite injects a stub launcher producing each probed envelope class; real launches are operational use only. The runner is Python 3.9, standard library, root-only, with no daemon, scheduler, database, web UI, or tracker, and no reusable-package change.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** This changes how already-authorized work is executed by letting a repository tool launch host sessions that act as participants, and adds a new maintained runtime component that spends host quota.
- **Existing authorization:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Host adapter and participant rotation phase, approved through the explicit owner direction of `2026-08-14` and recorded through the specification-evolution mechanism with the capability probe as supporting evidence.
- **Approval evidence:** Human technical owner `MattSureham` directed automated participant rotation with its capability list, evidence-first constraint, adapter-subordination constraint, failure-escalation constraint, and exclusions; the accepted specification change and this ADR persist that authority.

## Alternatives considered

### Keep the documented manual adapter permanently

- **Benefits:** No new runtime component, no quota spend by tooling, no launch-failure modes.
- **Costs and risks:** Preserves the routine human routing the owner has now twice directed to remove, even though the launch interface is verified to exist.
- **Reason not selected:** The owner explicitly directed automated rotation, and the dispatch ADR's precondition for a real adapter is now evidence-satisfied.

### Assume a Paseo or higher-level session API

- **Benefits:** Would abstract host details if it existed.
- **Costs and risks:** No such interface is verified to exist on this host; building against it would be exactly the simulation the owner prohibited.
- **Reason not selected:** Probe evidence records `paseo` as absent. Only probed behavior may be relied upon.

### Extend `run_pipeline.py` or `run_dispatch.py` with launch behavior

- **Benefits:** Fewer root scripts.
- **Costs and risks:** Modifies two independently reviewed and accepted tools, couples the read-only decision layer to process execution, and enlarges both review surfaces.
- **Reason not selected:** A separate runner consuming the dispatcher read-only integrates without touching either accepted tool, matching the dispatch ADR's own integration reasoning.

### Build a general scheduler or orchestrator

- **Benefits:** Concurrency, queues, long-running supervision.
- **Costs and risks:** Exactly the infrastructure class excluded by every accepted phase so far.
- **Reason not selected:** Explicitly excluded by the owner direction and by ROTATE-008.

## Consequences

### Positive

- Already-authorized milestones can advance from decision to executed participant session without routine human routing, while every durable authority record remains produced by the accepted pipeline and issue records.
- Failure handling becomes honest: quota exhaustion, launch failure, and timeouts are operational events with bounded responses, never disguised as authority gaps.
- Every rotation step is auditable after the fact from the ledger, and recovery needs no conversational memory — only dispatcher output plus the ledger.
- The interface boundary is pinned to evidence; host upgrades that change envelope behavior fail closed instead of silently misbehaving.

### Negative and tradeoffs

- The root repository gains a third maintained Python component plus two durable data files (registry, ledger); drift between runner behavior, registry contents, and role-contract prose is a reviewed risk.
- Launched sessions spend real quota and act with real host credentials; bounds mitigate but do not eliminate that operational risk.
- Label-based eligibility remains an operational assertion, not authentication, now with automated consequences.
- The probed interface is single-host, single-version; portability is not claimed.

### Compatibility and migration

- The accepted pipeline and dispatcher tools, their tests, and their accepted issue records are unchanged; the runner consumes them read-only except for executing dispatcher-emitted transition commands.
- `ROLE_CONTRACTS.md` gains adapter/rotation guidance within the milestone's allowed paths; the reusable ten-file package is untouched and adopters may continue manual routing indefinitely.
- The ledger is additive operational evidence; no existing evidence, issue, or ADR record is rewritten.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| Third root Python tool plus registry and ledger files | Execute dispatch decisions through the verified host interface without touching accepted tools | Rotation acceptance criteria, stub-launcher tests across every outcome class, probe evidence | Semantic adequacy of participant prompts and recovery wording remains reviewer judgment |
| Real quota spend driven by tooling | Participants must actually run to close the loop | Declared spend/step/attempt bounds; budget-exhaustion classification from probe evidence | Host rate limits and concurrency behavior remain unprobed (`UNKNOWN` in the probe record) |
| Automated use of label-based eligibility | Independence must hold without a human in the loop | Pre-launch filtering tests; existing executable pipeline gates unchanged | Authentication remains [`ISSUE-20260806T013907Z-authenticated-identity-approval`](../ISSUES/ISSUE-20260806T013907Z-authenticated-identity-approval.md) |

## Evidence and assumptions

- **CONFIRMED:** The host launch interface exists and behaves as recorded in [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md): launch, JSON envelope, budget cap, budget-exhaustion signaling, session resume; `paseo` is absent.
- **CONFIRMED:** The dispatcher emits byte-identical machine-readable decisions with eligibility constraints and expected commands, verified by the accepted dispatch milestone's tests and independent review.
- **CONFIRMED:** The owner direction prohibits inventing unverified session APIs, requires evidence-first capability bounding, keeps repository state authoritative, subordinates adapters to dispatch decisions, and forbids mapping participant failure to human-authority escalation.
- **INFERRED:** A single-host adapter with a stub-injected launcher is the smallest design satisfying the direction without modifying accepted tools.
- **UNKNOWN:** Host rate limits, concurrent-session behavior, long-running session stability, authentication-mode variation, CLI envelope stability across versions, and portability to any other host.

## Independent review rounds

- **Required:** `YES` — the milestone adds a runtime component that spends host quota and launches sessions that act on authority-bound state.

No independent review round has been recorded. Review the immutable rotation implementation target and the complete owning-issue round together. An `APPROVED` round on that target may satisfy this ADR's review intent when its scope explicitly includes this decision.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-14T09:25:04Z` | `NONE` | `ACCEPTED` | Human technical owner `MattSureham`, recorded by `ClaudeCode/root` | Explicit host adapter / automated participant rotation owner direction; accepted root specification change and capability probe evidence record the product authority |
