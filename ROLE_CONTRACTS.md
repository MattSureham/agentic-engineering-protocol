# Role Contracts

This artifact codifies the durable expectations for the three participant roles plus the human-escalation path used by the accepted Automated role dispatch phase of [`PROJECT_SPEC.md`](PROJECT_SPEC.md) and by accepted [`ADR-20260814T051405Z-automated-role-dispatch`](ADR/ADR-20260814T051405Z-automated-role-dispatch.md). It is normative guidance subordinate to the root specification and accepted ADRs: it creates no scope, overrides no gate, and never substitutes for the human technical owner. The read-only dispatcher (`scripts/run_dispatch.py`) derives the next required role from durable repository state and references these contracts; the pipeline (`scripts/run_pipeline.py`) remains the only mutation path for milestone state.

## Shared participant rules

- A participant acts under exactly one attributable label per durable record. Labels are operational assertions, not authenticated identity.
- Every role works from durable repository state — the accepted contract, issue-embedded pipeline state, evidence, and review rounds — never from conversational memory.
- No role may modify the accepted specification, accepted ADRs, or the reusable `protocol/` package unless an accepted milestone's allowed paths say so.
- No role may perform another role's completion conditions for the same attempt where an independence rule applies.
- Any participant who finds existing repository authority insufficient must stop and follow the Human escalation path rather than improvising scope.

## Implementer

**Purpose:** Advance the selected milestone's authorized scope from durable authorization to a verified immutable target ready for independent review.

**Required inputs:**

- The selected milestone's accepted contract entry: scope, allowed paths, acceptance checks, and review requirement.
- The owning issue, including its pipeline state block, open material findings when the state is `CHANGES_REQUIRED`, and prior activity.
- [`HANDOFF.md`](HANDOFF.md) reconciled against higher-precedence sources.

**Permitted actions:**

- Record the `AUTHORIZED` → `READY` and `READY` → `IN_PROGRESS` transitions under the implementer's own label.
- Create or modify only paths inside the milestone's `allowed_paths`.
- Run the milestone's acceptance checks and the structural validator.
- Commit the implementation and record the `IN_PROGRESS` → `AWAITING_PEER_REVIEW` transition with the full immutable target revision.
- After a `CHANGES_REQUIRED` round, begin a new attempt (`IN_PROGRESS`) and change only what the open material findings and authorized scope require.

**Required durable outputs:**

- Implementation confined to the allowed paths, committed as an immutable target whose parent is the attempt's base revision.
- Passing verification evidence written by the pipeline's submission gate.
- Issue and [`HANDOFF.md`](HANDOFF.md) reconciliation so a fresh participant can resume without conversational memory.

**Completion conditions:**

- The pipeline records `AWAITING_PEER_REVIEW` with the implementer's target and passing evidence, and the repository is clean including ignored paths.

**Eligibility and independence:**

- Any valid participant label may implement an attempt. The implementer label is bound to the attempt at `IN_PROGRESS` and constrains later roles: the independent reviewer label must differ from it, and the recorder label must differ from both the implementer and reviewer labels.
- The implementer never reviews, accepts, or records acceptance of their own attempt.

## Independent reviewer

**Purpose:** Independently verify the immutable target of the attempt under review and persist exactly one protocol disposition.

**Required inputs:**

- The immutable target revision recorded in the owning issue's pipeline state, its base revision, and the complete target diff.
- The accepted contract entry, the owning issue including prior review rounds, and the verification evidence generated at submission.

**Permitted actions:**

- Extract and examine the target read-only; run its checks at the extraction.
- Write and run independent adverse reproductions; inspect durable records.
- Persist exactly one review round in the owning issue with `Reviewed target`, `Open material findings`, and `Disposition` (`APPROVED`, `CHANGES_REQUIRED`, or `BLOCKED`).
- Record the `AWAITING_PEER_REVIEW` → `CHANGES_REQUIRED` transition when the persisted disposition is `CHANGES_REQUIRED` with at least one open material finding.

**Required durable outputs:**

- The persisted review round naming the reviewed target, the count of open material findings, resolution conditions for each finding, limitations, and the disposition.
- For `CHANGES_REQUIRED`, the matching recorded pipeline transition.
- [`HANDOFF.md`](HANDOFF.md) reconciliation naming the next single action.

**Completion conditions:**

- The round is durable, mechanically parseable by the pipeline, and any required `CHANGES_REQUIRED` transition is recorded. The reviewer does not implement fixes, does not record acceptance, and does not modify the target, implementation, tests, specification, or ADRs.

**Eligibility and independence:**

- The reviewer label must differ from the implementor label of the attempt under review.
- The reviewer must be independent in substance: no shared authorship of the change under review, and resolution claims of prior rounds are reproduced independently rather than trusted.

## Recorder and coordinator

**Purpose:** Record closure of an independently approved attempt and reconcile operational records, without re-reviewing and without modifying implementation.

**Required inputs:**

- The persisted latest review round with disposition `APPROVED` and zero open material findings on the verified target.
- The owning issue's closure checklist, the pipeline's acceptance gates, and the post-target record-only drift boundary.

**Permitted actions:**

- Independently confirm the acceptance preconditions from durable records (round validity, reviewer/implementor label inequality, reviewed-target equality, checklist completion, record-only drift).
- Complete evidence-supported closure-checklist items with attributable notes.
- Record the `AWAITING_PEER_REVIEW` → `ACCEPTED` transition under the recorder's own label.
- Reconcile the owning issue, [`HANDOFF.md`](HANDOFF.md), and [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md), and publish records with normal non-force pushes and remote equality verification.

**Required durable outputs:**

- The pipeline-validated `ACCEPTED` transition and the `CLOSED` owning issue.
- A HANDOFF exposing exactly one next action, or the explicit terminal wait state when no authorized milestone remains.

**Completion conditions:**

- The milestone state is `ACCEPTED`, records are reconciled and published, and local/cached/direct remote references are verified equal.

**Eligibility and independence:**

- The recorder label must differ from both the implementor label of the attempt and the reviewer label of the approving round.
- The recorder never re-performs the review and never changes implementation bytes.

## Human escalation

**Purpose:** Route genuine authority gaps to the human technical owner — and only those.

**When required:**

- The selected milestone's state is `BLOCKED_HUMAN_AUTHORITY`.
- Any participant finds that existing repository authority is insufficient for the work the dispatcher or records imply (including a review disposition of `BLOCKED`).

**Required durable outputs:**

- A linked `BLOCKED` issue stating the blocker, unblock owner, and unblock condition, and the recorded `BLOCKED_HUMAN_AUTHORITY` transition (recordable by any participant label).
- Resolution requires the human technical owner's decision recorded through specification evolution or an explicit owner direction; routine lifecycle progression never requires it.

## Host adapter boundary

The dispatcher emits the next-role decision; starting a session that performs the role is host-specific invocation and is **not** repository-native dispatch. The dispatch milestone's manual adapter step remains the fallback: an operator starts the next participant session and supplies the emitted role, eligibility constraints, role-contract reference, and expected records and commands. No repository code simulates a launch interface.

## Host adapter and participant rotation

The Host adapter and participant rotation phase ([`PROJECT_SPEC.md`](PROJECT_SPEC.md), `ROTATE-001`–`ROTATE-008`) authorizes one real adapter for hosts where probe evidence has verified a launch interface. Root `scripts/run_rotation.py` executes dispatcher decisions through the probed `claude -p` headless interface; [`EVIDENCE-20260814T092504Z-host-capability-probe`](EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md) and [`EVIDENCE-20260817T023721Z-live-profile-probe`](EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md) together are the capability boundary.

- **Routing authority:** The runner consumes only `scripts/run_dispatch.py --json`. It never re-derives role, milestone, eligibility, or scope, and it executes no pipeline transitions itself — launched participants receive the dispatcher-emitted commands with their own label substituted and run them as their role requires.
- **Registry:** Eligible participants are declared in `ROTATION_PARTICIPANTS.json` with per-participant launch configuration and default bounds. Before any launch the runner filters candidates against the dispatcher's emitted eligibility constraints; an exhausted pool is an explicit `no_eligible_participant` stop, never a human-authority escalation.
- **Probed interface only:** Launches use exactly the probed flags (`-p`, `--output-format json`, `--max-budget-usd`, `--tools`, `--allowedTools`, `--resume`). The verified live profile is `tools` and `allowed_tools` both `Read,Edit,Write,Bash` per [`EVIDENCE-20260817T023721Z-live-profile-probe`](EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md); the originally probed `tools ""` profile remains valid with an empty `allowed_tools`, in which case the `--allowedTools` flag is omitted. Headless permission denial is machine-readable: a success-shaped envelope with a non-empty `permission_denials` array and absent work product. Any launch configuration beyond a probed profile requires new recorded probe evidence before reliance; unrecognized envelope shapes fail closed as `session_error`.
- **Failure taxonomy:** `launch_failure`, `quota_exhausted`, `timeout`, `session_error`, `permission_denied`, and `non_advancing` are participant failures with bounded retry/rotation. They never produce a `BLOCKED_HUMAN_AUTHORITY` transition; human escalation remains exactly what the pipeline and dispatcher emit.
- **Ledger:** Every launch, outcome, and stop is appended to `ROTATION_LOG.jsonl` with participant label, session identity, outcome class, and cost where reported. The ledger is append-only operational evidence; it is never rewritten, and pipeline state in the owning issue remains authoritative.
- **Recovery:** After interruption the runner re-reads the dispatcher decision and reconciles the ledger tail: a launch with no recorded outcome is classified from repository state (advancement landed → `success_advancing`; otherwise `session_error`) before any retry, so no transition is duplicated.
- **Bounds:** Maximum attempts per decision, steps per invocation, and spend per invocation are declared in the registry and overridable per invocation. Exhaustion stops the runner with the recorded reason; unbounded loops and unbounded spend are forbidden.
- **Reconciliation:** Launched participants own the role-required durable records (issue updates, HANDOFF reconciliation, commits). Because the pipeline's cleanliness gate rejects a dirty tree, participants commit ledger and record changes as part of their role before recording transitions.
