# Human Checkpoint

This is a low-bandwidth synchronization point for the human technical owner. It is a summary and decision queue, not project truth. Read [`BOOTSTRAP.md`](BOOTSTRAP.md) for rules; accepted product requirements live in [`PROJECT_SPEC.md`](PROJECT_SPEC.md), and accepted architecture lives in [`ADR/`](ADR/).

## Checkpoint metadata

- **Generated UTC:** `2026-08-17T02:22:21Z`
- **Prepared by:** `ClaudeCode/root`
- **Period covered:** Specification audit and authority recording for the product-level autonomy owner direction of `2026-08-17`, from the rotation recorder reconciliation of `2026-08-17T01:55:00Z` through this authority record at `2026-08-17T02:12:18Z`
- **Specification status reviewed:** Root `PROJECT_SPEC.md` is `ACCEPTED`, now including the top-level Product-level autonomy objective (`AUTONOMY-001`–`AUTONOMY-006`) and the Live invocation and autonomy demonstration phase (`LIVE-001`–`LIVE-004` plus six demonstration acceptance criteria) with contract milestones 4 and 5; milestones 1–3 contract digests are unchanged
- **Implementation/reference state:** All three prior milestones remain `ACCEPTED` with owning issues `CLOSED` (pipeline target `26d890f6e27ad181265ee5417a45637d867aa2dc`, dispatch target `4a2601f04db9cf8b0f2e909fd4ca8f45666fe8c8`, rotation target `d6471f54b7e75f255b308d44885146762642b261`). Milestone 4 (`MILESTONE-20260817T021218Z-live-invocation-v1`, digest `36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea`) is `AUTHORIZED` with dependencies satisfied — the dispatcher selects it and emits `ROLE implementer`. Milestone 5 (`MILESTONE-20260817T021218Z-autonomy-demonstration-v1`, digest `f0a1700f00500125d42e832a236077b0d42e87ebc4ade284a33335e8794c0284`) is `AUTHORIZED` and dependency-blocked on milestone 4. No implementation has begun.
- **Prior checkpoint:** `2026-08-17T01:55:00Z` by `ClaudeCode/rotation-record` (superseded by this authority record)

## System mental model

This repository produces a ten-file, Markdown-first reusable engineering protocol under `protocol/`. The root repository adopts a separate root-specific instance with an accepted root-local milestone state-and-gate pipeline, an authorized read-only role dispatcher, and an evidence-bounded host adapter for automated participant rotation, all outside the reusable package. Root requirements, accepted architecture, tests/contracts, evidence, operational state, implementation, and inference retain distinct precedence and ownership.

Agents are replaceable participants. HANDOFF is a compact continuity index, not canonical truth. Product edits do not automatically rewrite root governance, and root governance edits do not automatically change the copy-ready product; material semantic divergence is reviewed explicitly.

An explicit milestone in accepted `PROJECT_SPEC.md` is prior authorization to implement, verify, fix, review, and continue within its declared bounds. Runtime state cannot create scope. Human escalation occurs when authority is missing or exhausted, not merely because a lifecycle stage changes — and participant failures (launch failure, quota exhaustion, timeout, non-advancing completion) are operational events that must never be escalated as authority gaps.

Autonomy is now a product-level acceptance boundary, not a milestone property: accepted component milestones are enabling capabilities only, and the dispatcher's terminal `ROLE none` idle state is never evidence that the objective is met. The objective is established exclusively by a demonstrated real unattended end-to-end run.

## Owner direction report (six points)

1. **Why the previous specification allowed premature terminal `ROLE none` states.** Each phase scoped its acceptance criteria to component behavior; the pipeline phase explicitly made the absence of a further contract "a valid terminal result"; the rotation phase required stub-only tests; and no top-level requirement distinguished "components accepted" from "objective met". The terminal idle state was correct contract behavior — it prevents scope invention — but nothing prevented it from being read as completion. This was a structural specification gap, not an implementation defect.
2. **The exact normative requirement now recorded.** Root `PROJECT_SPEC.md`, "Product-level autonomy objective": `AUTONOMY-001` (unattended progression of already-authorized milestones through implementation, verification, independent review, fix loops, and acceptance with no owner routing, prompt copying, participant launching, routine transition approval, interruption recovery, or participant retrying); `AUTONOMY-002` (stops only for genuine new HUMAN authority, exhausted declared bounds, or absence of authorized work); `AUTONOMY-003` (repository records are the sole authority); `AUTONOMY-004` (acceptance boundary: one bounded runner invocation producing a real unattended dogfood run with at least three distinct launched participant roles progressing a real authorized milestone `AUTHORIZED` → `ACCEPTED`; stub-only or simulated execution is insufficient); `AUTONOMY-005` (objective evidence: the append-only ledger, pipeline events, review round, and reconciliation records, auditable after acceptance); `AUTONOMY-006` (component acceptance and terminal idle states are never presented as objective completion).
3. **Capabilities already satisfied (enabling, accepted, history preserved).** Milestone pipeline (`26d890f`), deterministic read-only role dispatcher (`4a2601f`), and bounded participant-rotation runner with registry and append-only ledger (`d6471f5`) — all `ACCEPTED` with owning issues `CLOSED`; probed host launch interface (headless JSON envelopes, budget caps, machine-readable budget exhaustion, session resume).
4. **Capabilities remaining unsatisfied.** No real participant session has ever been launched by the system (the committed registry pins `tools: ""`, which cannot perform file-editing roles); headless permission behavior with tools enabled is unprobed; the runner is not conformed to a verified live profile; no milestone has ever progressed without manual routing; no demonstration evidence exists.
5. **The milestone dependency chain.** Milestone 4 `MILESTONE-20260817T021218Z-live-invocation-v1` (probe and verify the minimal tool-enabled headless profile; conform runner/registry/role contracts; preserve stub-only tests; fail-closed on anything unprobed) → milestone 5 `MILESTONE-20260817T021218Z-autonomy-demonstration-v1` (the gated dogfood: its own lifecycle is the unattended run, carrying the root `ISSUES/TEMPLATE.md` activity-gate conformance fix as its vehicle). The dependency ordering ensures a live-operation failure is absorbed by milestone 4's fix loop, keeping the demonstration's acceptance evidence clean.
6. **The objective evidence that will prove the end state.** The append-only `ROTATION_LOG.jsonl` naming the launched participant labels; the demonstration issue's pipeline events naming those same labels across implementer, independent-reviewer, and recorder legs; the launched fresh reviewer's `APPROVED` round with zero open material findings on the immutable target; the recorder's closure verification of all legs from durable records; the assembled demonstration evidence record under `EVIDENCE/`; and the durable account showing no owner or operator routing occurred.

## Material changes since the prior checkpoint

| Change | Why | Product/architecture effect | Evidence and review |
|---|---|---|---|
| Authorize the product-level autonomy objective | Intermediate automation milestones reached `ACCEPTED` while the owner's actual automation objective remained unmet | Top-level `AUTONOMY-001`–`AUTONOMY-006`; component milestones reclassified as enabling capabilities; terminal idle can no longer be read as completion | Explicit owner direction `2026-08-17`; [`PROJECT_SPEC.md`](PROJECT_SPEC.md) change record `2026-08-17T02:12:18Z`; [`ADR-20260817T021218Z-autonomy-end-state`](ADR/ADR-20260817T021218Z-autonomy-end-state.md) |
| Authorize the live-invocation capability milestone | Real roles require a probe-verified tool-enabled launch profile before the demonstration can run | Milestone 4 contract (`LIVE-001`–`LIVE-004`); probe-before-reliance, minimal verified profile, adapter conformance, fail-closed continuity | [`ISSUE-20260817T021218Z-live-invocation`](ISSUES/ISSUE-20260817T021218Z-live-invocation.md), pipeline state `AUTHORIZED` |
| Authorize the autonomy demonstration milestone | The objective requires a mandatory real unattended dogfood run as its acceptance boundary | Milestone 5 contract; six demonstration acceptance criteria; self-vehicle change (root `ISSUES/TEMPLATE.md` gate conformance); depends on milestone 4 | [`ISSUE-20260817T021218Z-autonomy-demonstration`](ISSUES/ISSUE-20260817T021218Z-autonomy-demonstration.md), pipeline state `AUTHORIZED` |

(Prior milestone history — adoption, hardening, structural validator, pipeline, dispatch, rotation — is unchanged and indexed in the immutable Git record and the superseded checkpoints.)

## Architecture decisions

### Accepted, rejected, or superseded

| ADR | Status | Decision and consequence | Owner authority evidence |
|---|---|---|---|
| [`ADR-20260806T013907Z-root-protocol-adoption`](ADR/ADR-20260806T013907Z-root-protocol-adoption.md) | `ACCEPTED` | Adopt a separately governed root protocol instance and compact record architecture | Human-approved post-pilot hardening plan; authority boundary `7dea545` |
| [`ADR-20260814T015817Z-authorized-milestone-pipeline`](ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md) | `ACCEPTED` | Bind autonomous milestone transitions to accepted spec contracts while keeping operational state subordinate | Explicit `2026-08-14` owner decision and approved decision-complete plan; independent target review completed and milestone accepted |
| [`ADR-20260814T051405Z-automated-role-dispatch`](ADR/ADR-20260814T051405Z-automated-role-dispatch.md) | `ACCEPTED` | Deterministic repository-native next-role dispatch with durable role contracts; host session invocation stays an explicit, non-simulated adapter boundary | Explicit `2026-08-14T05:14:05Z` owner direction; independent round 1 `APPROVED`; milestone accepted |
| [`ADR-20260814T092504Z-host-adapter-rotation`](ADR/ADR-20260814T092504Z-host-adapter-rotation.md) | `ACCEPTED` | Execute dispatcher decisions through the probe-verified host CLI interface with a participant registry, append-only rotation ledger, failure taxonomy without false escalation, and declared bounds | Explicit `2026-08-14` owner direction with live probe evidence; independent round 1 `APPROVED`; milestone accepted |
| [`ADR-20260817T021218Z-autonomy-end-state`](ADR/ADR-20260817T021218Z-autonomy-end-state.md) | `ACCEPTED` | Autonomy is a product-level acceptance boundary proven only by a demonstrated unattended run; terminal idle is not completion; live launches use a minimal probe-verified profile; the demonstration milestone is its own vehicle; human authority is unchanged; dependency ordering prevents premature completion readings | Explicit product-level autonomy owner direction of `2026-08-17` recorded through specification evolution |

### Proposed or disputed

No architecture proposal or disputed architectural decision awaits owner action.

## Complexity and architecture drift

### New or retired complexity

| Cost | Why introduced/removed | Coverage | Residual debt |
|---|---|---|---|
| Separate root/product protocol governance | Prevent silent authority coupling | Accepted ADR, semantic/link validation, independent review | Future divergence still requires judgment and review |
| Optional root Python structural checker | Make stable package/HANDOFF invariants repeatable | Standard-library tests plus completed independent review; five LOW findings accepted as residual risk | Full CommonMark, semantic correctness, portability, and shipped automation remain outside scope |
| Root-local milestone state/gate engine | Mechanically enforce stable authorization, verification, review, and escalation transitions | Accepted contract/ADR plus pipeline tests at target `26d890f`; independent round 2 `APPROVED`; milestone `ACCEPTED` | Python/Git portability, unauthenticated labels, cooperative-only writers, semantic safety of owner-authorized commands |
| Root role-contract artifact and read-only dispatcher | Remove routine human routing between already-authorized transitions | Accepted dispatch phase/ADR; 19 dispatch tests; independent round 1 `APPROVED`; milestone `ACCEPTED` | Prose/tool drift must be caught by review and tests; label-based eligibility remains an operational assertion |
| Host adapter, participant registry, and rotation ledger | Execute dispatcher decisions through the verified host interface | Accepted rotation phase/ADR and probe evidence; 26 stub-launcher tests; independent round 1 `APPROVED`; milestone `ACCEPTED` | Real quota spend by tooling; host rate limits, concurrency, envelope stability unprobed |
| Live tool-enabled launch profile (milestone 4, authorized not implemented) | Real roles require file and shell capability | To be covered by new probe evidence plus stub-suite conformance tests | Headless permission behavior and session stability only become known through the probes |
| Self-demonstrating acceptance evidence (milestone 5, authorized not implemented) | The dogfood needs real authorized work; the milestone's own lifecycle is the smallest real vehicle | Demonstration acceptance criteria plus recorder closure verification | Post-hoc assembly completeness remains reviewer judgment |

### Drift assessment

- **Last independent drift review:** Independent round 1 of the rotation target `d6471f5` completed `2026-08-17T01:40:05Z` with disposition `APPROVED` and zero open material findings; prior rounds as recorded in the superseded checkpoint.
- **Classification:** No new drift. The autonomy evolution adds requirements and milestones; it modifies no accepted component behavior and rewrites no milestone history.
- **Owner-relevant differences:** None outstanding. The rotation ADR's probed-interface boundary is narrowed only by extending the probe record to the minimal tool-enabled profile under milestone 4.
- **Codification boundary:** The checker remains a lower-tier structural observer; pipeline, dispatcher, and rotation runner are unchanged by this authority record; the reusable package remains runtime-free.

## Assumptions and uncertainty that changed

| Certainty | Earlier understanding | Current understanding | Consequence and evidence |
|---|---|---|---|
| `CONFIRMED` | Accepted component milestones could be read as automation completion | Component milestones are enabling capabilities only; the objective requires a demonstrated unattended run | Owner direction `2026-08-17`; `AUTONOMY-004`/`AUTONOMY-006` |
| `CONFIRMED` | Terminal `ROLE none` ended the automation program | Terminal idle is a correct idle state, never autonomy evidence | `AUTONOMY-006`; ADR decision 2 |
| `CONFIRMED` | The probed `tools ""` launch profile sufficed for rotation acceptance | It cannot perform file-editing roles; a minimal tool-enabled profile must be probe-verified before reliance | [`ISSUE-20260817T021218Z-live-invocation`](ISSUES/ISSUE-20260817T021218Z-live-invocation.md) problem statement |
| `UNKNOWN` | Headless permission behavior with tools enabled, long-running session stability, host rate limits | Still unestablished; milestone 4's probes resolve or fail closed | Owned by the live-invocation issue |
| `UNKNOWN` | Whether the first unattended run completes within declared bounds | Still unestablished; bound exhaustion is a recorded stop, never an authority escalation | Owned by the autonomy-demonstration issue |

## Confidence and verification

- **What is directly verified:** The updated five-milestone contract parses with the accepted pipeline parser; milestones 1–3 digests are unchanged (`36fba5d8…`, `afe72580…`, `a38bb7bf…`); milestone 4 digest `36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea` and milestone 5 digest `f0a1700f00500125d42e832a236077b0d42e87ebc4ade284a33335e8794c0284` match their owning issues' state blocks; `run_pipeline.py status --json` selects milestone 4 and reports milestone 5 dependency-unsatisfied; the dispatcher emits `ROLE implementer` for milestone 4; the structural validator passes; the full unittest suite passes.
- **What was independently reviewed:** Prior targets as recorded in the superseded checkpoint (hardening, wording, structural validator, pipeline, dispatch, rotation — all `APPROVED`). The new milestones' immutable targets will each require fresh independent review before acceptance; the demonstration milestone's reviewer is itself launched by the runner per demonstration criterion 6.
- **What was not run or remains unverified:** No real participant launch has occurred; no probe of tool-enabled headless operation exists yet; no implementation for milestones 4 or 5 exists. Dedicated Markdown linting remains unavailable; broader portability, CommonMark conformance, concurrency guarantees, authenticated identity, and large-scale coordination remain unverified.
- **Known regressions or unresolved risks:** None blocking. Four deferred capability areas remain `BLOCKED`.

## Human attention required

No owner decision is currently pending. The owner direction of `2026-08-17` is fully recorded: the accepted specification carries the product-level autonomy objective and the two-milestone decomposition, the compatible ADR is accepted, and both owning issues hold `AUTHORIZED` pipeline state. An executor can continue milestone 4 without another routine owner approval. New owner authority is still required for scope beyond the accepted milestones, package runtime distribution, unprobed host APIs, human-blocker resolution, concurrent-writer guarantees, authenticated identity, large-scale coordination, or tracker integration.

## No human attention required

- Implementation, deterministic verification, fix/re-review cycles, and transitions within milestones 4 and 5 need no new owner prompt while every accepted gate remains satisfied.
- The demonstration run's participant launches, rotations, retries within declared bounds, and recoveries are operational events governed by the accepted failure taxonomy; exhaustion stops are recorded, never escalated as authority gaps.

## Next checkpoint trigger

- **Trigger:** Material independent-review ambiguity, missing/exhausted milestone authority, proposed scope/architecture change, participant-failure patterns the accepted taxonomy cannot classify, demonstration-run completion or bound exhaustion, or owner request
- **Expected owner action before then:** `NONE`; milestone 4 is authorized and routed to an implementer by the dispatcher
