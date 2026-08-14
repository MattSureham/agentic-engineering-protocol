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

The bounded participant-rotation runner is invoked with `python3 scripts/run_rotation.py` (bounds overridable with `--max-steps`, `--max-attempts`, `--max-spend-usd`). It consumes only the dispatcher's machine-readable decision, selects an eligible participant from [`ROTATION_PARTICIPANTS.json`](ROTATION_PARTICIPANTS.json) after independence filtering, launches it through the probe-verified host CLI interface, classifies the result into the accepted failure taxonomy (participant failures never become human-authority escalations), and appends every step to the append-only [`ROTATION_LOG.jsonl`](ROTATION_LOG.jsonl) ledger. It exits `0` after a clean bounded stop (terminal decision, human-authority decision, no eligible participant, or an exhausted bound) and `2` on invalid input or unrecognized decision/envelope shapes, failing closed. Its tests use a stub launcher and never launch real sessions.
