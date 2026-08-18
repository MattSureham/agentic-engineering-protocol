# Agentic Engineering Protocol Development Repository

This repository develops a standalone, copy-ready protocol for software projects maintained by replaceable coding-agent instances under human architectural authority.

## Contributor entry point

The root files govern development of this repository and are distinct from the reusable product:

1. Read [`BOOTSTRAP.md`](BOOTSTRAP.md), the normative root collaboration protocol and truth hierarchy.
2. Read [`PROJECT_SPEC.md`](PROJECT_SPEC.md), the authoritative product specification.
3. Read relevant accepted records in [`ADR/`](ADR/), executable contracts/tests, and [`EVIDENCE/`](EVIDENCE/) before relying on lower-precedence state.
4. Read [`HANDOFF.md`](HANDOFF.md), the compact operational snapshot, unresolved-work index, and single next action; reconcile it against higher-precedence sources and the actual repository.
5. Read [`ROLE_CONTRACTS.md`](ROLE_CONTRACTS.md) when acting as or dispatching to an implementer, independent reviewer, or recorder/coordinator for an authorized milestone.

Root truth precedence is `PROJECT_SPEC → accepted ADRs → contracts/tests → evidence → HANDOFF → implementation → inference`. README is navigation only. Do not treat the root BOOTSTRAP as the reusable deliverable or assume a change to either BOOTSTRAP automatically changes the other; material semantic divergence is reviewed explicitly.

## Reusable package

The copy-ready protocol lives under [`protocol/`](protocol/). Its full philosophy, quick start, workflow, roles, and limitations are documented in [`protocol/README.md`](protocol/README.md).

The package is intentionally Markdown- and filesystem-based. It does not require a particular programming language, framework, model vendor, CI provider, version-control system, database, service, or orchestrator.

## Optional development validation

Repository maintainers with Python 3 may run `python3 scripts/validate_protocol.py` and `python3 -m unittest discover -s tests -v`. This root-only, read-only helper checks a bounded set of structural invariants; it is not protocol authority, does not validate human judgment, and is not included in or required by the reusable package.

The accepted root milestone pipeline is invoked with `python3 scripts/run_pipeline.py status` (add `--json` for machine-readable output) and `python3 scripts/run_pipeline.py transition --milestone ID --actor ID --to STATE`. Exit `0` means the requested status/gate passed, `1` means a deterministic gate denied advancement, and `2` means the invocation or evaluation could not produce a valid result. It validates and records lifecycle gates for milestones already declared in the accepted root `PROJECT_SPEC.md`; it cannot add scope, implement work, perform peer review, authenticate participant identity, commit, push, use the network, or replace the reusable package's manual workflow. Run `python3 scripts/run_pipeline.py --help` for transition-specific inputs.

The read-only next-role dispatcher is invoked with `python3 scripts/run_dispatch.py` (add `--json` for machine-readable output). It derives exactly one next role — implementer, independent reviewer, recorder/coordinator, human escalation, or the terminal no-authorized-work result — from the accepted contract and issue-embedded pipeline state, with eligibility constraints and the [`ROLE_CONTRACTS.md`](ROLE_CONTRACTS.md) reference. Identical repository state yields byte-identical output; it mutates nothing and does not launch or simulate launching a participant.

The bounded participant-rotation runner is invoked with `python3 scripts/run_rotation.py` (bounds overridable with `--max-steps`, `--max-attempts`, `--max-spend-usd`). It consumes only the dispatcher's machine-readable decision, selects an eligible participant from [`ROTATION_PARTICIPANTS.json`](ROTATION_PARTICIPANTS.json) after independence filtering, launches it through the probe-verified host CLI interface using the minimal probe-verified tool-enabled profile (`Read,Edit,Write,Bash` with the matching permission grant), classifies the result into the accepted failure taxonomy (participant failures — including machine-readable headless permission denials — never become human-authority escalations), and appends every step to the append-only [`ROTATION_LOG.jsonl`](ROTATION_LOG.jsonl) ledger. It exits `0` after a clean bounded stop (terminal decision, human-authority decision, no eligible participant, or an exhausted bound) and `2` on invalid input or unrecognized decision/envelope shapes, failing closed. Its tests use a stub launcher and never launch real sessions.

## Running the authorized autonomy demonstration (live)

The currently authorized demonstration is `MILESTONE-20260817T021218Z-autonomy-demonstration-v1`. The canonical operator command is:

    python3 scripts/run_rotation.py

**This is live execution, not a dry run; there is no dry-run mode.** The runner launches real headless participant sessions that read, edit, and write files, run shell commands (including Git), and commit record changes on this repository; the recorder role's emitted records include a normal non-force push to the shared remote. Every launch consumes real quota and budget. Do not run the command unless you intend the demonstration to act on this repository.

- **`--root`:** selects the repository root and defaults to the parent of `scripts/` — this repository — so the canonical command needs no flag in a normal checkout.
- **Bounds:** one invocation performs at most `max_steps` launches (registry default `8`), at most `max_attempts_per_decision` launches per dispatcher decision (default `2`, counted durably in the ledger across restarts), and stops before the next launch once reported spend reaches `max_spend_usd` (default `5.0` per invocation). `--max-steps`, `--max-attempts`, and `--max-spend-usd` override these per invocation. Each single launch is capped host-side at `max_budget_usd` (default `1.0`, passed as `--max-budget-usd`) and `timeout_seconds` (default `1800`). The canonical command uses the accepted registry defaults.
- **Participants and eligibility:** launch labels come from [`ROTATION_PARTICIPANTS.json`](ROTATION_PARTICIPANTS.json) after the dispatcher's emitted eligibility constraints are applied (for example, the reviewer label must differ from the attempt implementor). The committed registry declares `agent:rotation-alpha`, `agent:rotation-beta`, and `agent:rotation-gamma` with the probe-verified profile (`tools` and `allowed_tools` both `Read,Edit,Write,Bash`). Per-participant `max_budget_usd`, `tools`, and `allowed_tools` may override the defaults.
- **Host prerequisites:** the probe-verified boundary is this host's Claude Code CLI `2.1.118` headless interface (`claude -p`, JSON result envelopes, `--max-budget-usd`, `--tools`, `--allowedTools`) on an OAuth/subscription Darwin host; `paseo` does not exist here. Only probed behavior is relied upon; anything else fails closed. Cross-version envelope stability, rate limits, concurrency, long-running session stability, and other authentication modes are `UNKNOWN`.
- **Ledger:** every launch, outcome classification, and stop is appended to [`ROTATION_LOG.jsonl`](ROTATION_LOG.jsonl) with participant label, session identity, outcome class, and cost where reported. The ledger is append-only operational evidence; pipeline state in the owning issue remains authoritative.
- **Stop and recovery:** the runner stops cleanly with a recorded reason — `terminal_no_authorized_work`, `human_authority_required`, `no_eligible_participant`, `attempts_exhausted`, `steps_exhausted`, or `spend_exhausted` — and exits `0`; invalid input or unrecognized decision/envelope shapes exit `2`. To stop early, interrupt the process; recovery is re-running the same command. A launch left with no recorded outcome is reconciled from repository state before any retry (advancement landed records `success_advancing`; otherwise `session_error`), so no pipeline transition is duplicated and per-decision attempt counts survive restarts. `UNKNOWN`: the behavior of an in-flight headless session orphaned by a mid-launch kill is unverified — after a mid-launch stop, confirm no orphaned `claude` session is still acting on the repository before restarting. Whether a run restarted after bound exhaustion still satisfies the demonstration's acceptance criteria is determined by that milestone's independent review, not by this document.
- **Failure behavior and authority separation:** launch failure, quota/budget exhaustion, timeout, session error, permission denial, and non-advancing completion are participant failures with bounded retry/rotation. They never produce a human-authority escalation. The runner stops for the owner only when the dispatcher emits a genuine human-authority decision or a declared bound is exhausted.
- **Commits and pushes:** the runner itself never commits, pushes, or executes pipeline transitions. Launched participants commit their role-required records and run the dispatcher-emitted pipeline transition commands with their own label substituted; pushes to the shared remote are performed by launched participants where their role's emitted records require publication (the recorder leg), never by the runner.
- **Successful unattended completion:** the runner launches distinct participants for the implementer, independent-reviewer, and recorder legs of the demonstration milestone and, once the milestone is `ACCEPTED`, stops with `terminal_no_authorized_work`. Acceptance is determined only by the pipeline gates and the independent review round recorded in the owning issue — never by the runner.
