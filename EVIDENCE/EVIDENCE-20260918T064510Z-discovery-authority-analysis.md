# Prompt-Independent Discovery — Authority and Gap Analysis

## Metadata

- **ID:** `EVIDENCE-20260918T064510Z-discovery-authority-analysis`
- **Captured UTC:** `2026-09-18T06:45:10Z` (authority-recording phase start; source investigation also occurred during the immediately preceding planning phase)
- **Recorded by:** `agent:Codex-discovery-authority`
- **Claim supported or challenged:** The accepted product lacks a supported-host, prompt-independent entry contract; existing recovery and launcher evidence does not prove that behavior.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `DISCOVERY-001`–`DISCOVERY-006`
- **Related ADR/issue:** [Discovery boundary ADR](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md); [owning issue](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Repository revision/state:** Clean `main` at `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b` before authority-record changes; cached and direct remote matched
- **Environment:** Darwin arm64, Python `3.9.6`; installed `codex-cli 0.153.4` and Claude Code `2.1.118`

## Method and raw observations

Read root BOOTSTRAP, specification, the five accepted ADRs, active issues, prior onboarding/pilot and live-invocation evidence, HANDOFF/checkpoint, package onboarding/guide/template, role contracts, dispatcher and rotation implementation. Inspect Git rather than relying on the historical HANDOFF snapshot. No agent session or runner was launched.

| Command or inspection | Observation | Scope/limitation |
|---|---|---|
| `git status --short --branch`; `git log -3 --oneline` | Clean `main...origin/main`; HEAD `58fa281`; parent `5b614f7`; prior `a2b39fd` | Exit `0`; baseline before writes |
| `git ls-remote origin refs/heads/main` | `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b` | Exit `0`; external check at orientation, not a timeless remote claim |
| `git show -1 --format='commit %H%nparent %P%n%s' --name-only` | Documentation repair contains exactly HANDOFF, HUMAN_CHECKPOINT, README, ROLE_CONTRACTS; parent is `5b614f749fc8227eedb48bf26eec465f3aab3172` | Matches the baseline snapshot's containing-commit test |
| `codex --version`; `claude --version`; `python3 --version`; `uname -sm` | `codex-cli 0.153.4`; `2.1.118 (Claude Code)`; `Python 3.9.6`; `Darwin arm64` | Exit `0`; binary presence/version is not activation evidence |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json` during planning | Selected `MILESTONE-20260817T021218Z-autonomy-demonstration-v1`, state `AUTHORIZED`, role `implementer`, digest `f0a1700f00500125d42e832a236077b0d42e87ebc4ade284a33335e8794c0284` | Exit `0`; read-only, no READY transition |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py` during planning | `PASS structural protocol validation (package_files=10 handoffs=2)` | Exit `0`; structural, not behavioral |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` during planning | `Ran 97 tests in 25.101s` / `OK` | Exit `0`; runner tests use stub participants, not discovery probes |

The owner described a real adopted project where a fresh participant bypassed recovery unless explicitly reminded in the task. **CONFIRMED:** this report was supplied and the owner approved the requirement-evolution plan. **UNKNOWN:** the external repository/revision, full prompt, host configuration, and incident trace. The report is motivation and owner input, not independently reproduced failure evidence.

## Requirement coverage and gap matrix

All baseline references can be reproduced with `git show 58fa281:<path>`.

| Area | Existing coverage | Verified gap / consequence |
|---|---|---|
| Fresh-agent recovery | Root/product BOOTSTRAP requires reading authority, actual repository state and HANDOFF before implementation | Prescribes behavior after entry, but does not ensure entry without prompting |
| Plug-and-play | Specification step 3 says to give the onboarding prompt; package README step 6 repeats that requirement | Task delivery remains coupled to protocol activation |
| Onboarding prompts | Five reusable role prompts point to BOOTSTRAP | Useful manual entry, not evidence that a generic task discovers the protocol |
| Core package | Ten Markdown files; README advises optional tool-specific pointers without duplicating rules | No adoption-signal contract, supported-profile definition, or verified installation/activation criterion |
| Host compatibility | Specification names Codex, Claude Code and Gemini/Kimi-style agents as compatibility intent | No version/mode/configuration-bound support claims or conformance matrix |
| Closed onboarding-authority issue | Clarifies accepted-milestone authority versus external task pressure, explicitly excludes broader redesign | Does not cover discovery; preserve closure and create a distinct issue |
| Dispatcher | Reads already-known authority/state and emits a role | Does not make an arbitrary entering host discover this machinery |
| Rotation | `build_prompt` explicitly injects BOOTSTRAP, recovery, role contract and dispatcher decision | Prompt-injected launches cannot pass the new task-only acceptance test |
| Live invocation probes | Establish tool/permission/envelope behavior on one host | Do not establish prompt-independent protocol activation |
| Autonomy demonstration | Authorized, attempt 0, no execution events beyond initial authorization | Reorder prospectively under owner authority; do not rewrite execution history or claim completion |

## Official capability observations

Official pages inspected on `2026-09-18` during planning:

- [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) describes startup discovery of project instructions along the project-root/current-directory path, file precedence and size limits. This establishes a documented adapter candidate, not compliance of installed `0.153.4` with this protocol.
- [Claude Code project memory](https://code.claude.com/docs/en/memory) describes loading project instructions, file imports, directory-dependent loading, and the distinction between context and enforcement. Its documented entry mechanism differs from Codex's. No automatic activation outcome is inferred from either page.
- [Gemini CLI context](https://geminicli.com/docs/cli/gemini-md/) illustrates another hierarchical mechanism and configurable filenames. It informs neutrality only; Gemini is not in the first implementation milestone.

These are mutable external documentation references, not vendored capability guarantees. Recheck the installed version and actual startup behavior before reliance; upgrades/configuration changes invalidate affected support claims until revalidated. Kimi, Pi, Astra, IDE/cloud variants and other untested hosts have no support claim from this evidence. A model name is not a harness profile.

## Authority interpretation

The owner-approved plan is durably transcribed in the owning issue and accepted specification/ADR. It authorizes the requirement, four-layer boundary, first two harness families, and discovery-first ordering. It does not make a particular vendor file or mechanism protocol authority.

The new milestone will depend on accepted live invocation and occupy order 5. The unstarted demonstration changes only its order to 6 in the contract; its initial machine event and attempt/state remain intact, with the new digest bound explicitly through owner-authorized specification evolution. This is authority migration, not a supported pipeline transition; no fabricated AUTHORIZED-to-AUTHORIZED machine event is added.

The existing pipeline/parser/dispatcher require no implementation change for six milestones. The first four canonical entry digests must remain unchanged. The exact old/new demonstration digest and new discovery digest are recorded with subsequent authority validation.

## Boundary and future proof requirements

Repository authority stays complete without an adapter. An adoption signal locates that authority and its scope; host-specific mechanisms only transport that pointer. Unsupported hosts retain honest manual fallback. A source template or nested repository cannot establish adoption or extend scope merely by sharing a filename.

The first-slice implementation must supply the real cold-session tests specified in PROJECT_SPEC: at least three independent fresh sessions per supported profile, root/subdirectory coverage, exact task-only input, observable recovery before task mutation, negative/migration cases, durable traces, and independent review. Approved requirements do not mean implemented behavior. A file-existence check, a stub, a launcher success envelope, or an agent's assertion is insufficient.

## Limitations and residual uncertainty

- Real prompt-independent activation: **NOT RUN**. No support profile is certified by this authority phase.
- Original incident: **NOT REPRODUCED**; no external project was accessed or changed.
- Dedicated Markdown linter availability will be checked during authority validation; ad-hoc checks must not be described as a dedicated linter.
- No universal model compliance, security enforcement, authenticated identity, concurrency, production readiness, or autonomous-demonstration completion follows from this analysis.
- Discovery and rotation are distinct: successful prompt-injected rotation cannot substitute for discovery evidence, and discovery conformance cannot substitute for AUTONOMY-004.

## Integrity and provenance

- **Artifact location:** This repository record; original baseline documents remain in Git at `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b`.
- **Artifact digest:** Recover exact bytes from the containing Git commit; no self-referential digest is claimed.
- **External retention risk:** Official documentation may change; incident trace is unavailable. Future live traces must be preserved in clone-recoverable evidence, not only temporary paths.
- **Supersedes / superseded by:** `NONE`; prior evidence remains unchanged.
