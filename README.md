# Agentic Engineering Protocol Development Repository

This repository develops a standalone, copy-ready protocol for software projects maintained by replaceable coding-agent instances under human architectural authority.

## Contributor entry point

The root files govern development of this repository and are distinct from the reusable product:

1. Read [`BOOTSTRAP.md`](BOOTSTRAP.md), the normative root collaboration protocol and truth hierarchy.
2. Read [`PROJECT_SPEC.md`](PROJECT_SPEC.md), the authoritative product specification.
3. Read relevant accepted records in [`ADR/`](ADR/), executable contracts/tests, and [`EVIDENCE/`](EVIDENCE/) before relying on lower-precedence state.
4. Read [`HANDOFF.md`](HANDOFF.md), the compact operational snapshot, unresolved-work index, and single next action; reconcile it against higher-precedence sources and the actual repository.

Root truth precedence is `PROJECT_SPEC → accepted ADRs → contracts/tests → evidence → HANDOFF → implementation → inference`. README is navigation only. Do not treat the root BOOTSTRAP as the reusable deliverable or assume a change to either BOOTSTRAP automatically changes the other; material semantic divergence is reviewed explicitly.

## Reusable package

The copy-ready protocol lives under [`protocol/`](protocol/). Its full philosophy, quick start, workflow, roles, and limitations are documented in [`protocol/README.md`](protocol/README.md).

The package is intentionally Markdown- and filesystem-based. It does not require a particular programming language, framework, model vendor, CI provider, version-control system, database, service, or orchestrator.

## Optional development validation

Repository maintainers with Python 3 may run `python3 scripts/validate_protocol.py` and `python3 -m unittest discover -s tests -v`. This root-only, read-only helper checks a bounded set of structural invariants; it is not protocol authority, does not validate human judgment, and is not included in or required by the reusable package.
