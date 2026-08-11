# Codification Gap Analysis

## Metadata

- **ID:** `EVIDENCE-20260811T013701Z-codification-gap-analysis`
- **Title:** Classify protocol rules and bound the first executable validation slice
- **Captured UTC:** `2026-08-11T01:37:01Z`
- **Recorded by:** `Codex/root`
- **Claim supported or challenged:** Stable structural protocol invariants can be checked by optional root development tooling without moving authority out of Markdown or adding automation to the reusable package.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), especially Scope constraints, Quality bar, `HARDEN-003`, `HARDEN-006`, and hardening acceptance criterion 5
- **Related ADRs/issues:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ISSUE-20260811T013701Z-structural-protocol-validator`](../ISSUES/ISSUE-20260811T013701Z-structural-protocol-validator.md); [`ISSUE-20260806T013907Z-runtime-automation`](../ISSUES/ISSUE-20260806T013907Z-runtime-automation.md)
- **Repository revision/state:** Clean, synchronized `main` baseline `3dc8902f5ccd9fb67330e25e57380c119f717f25`; analysis record initially prepared as an uncommitted addition to that baseline
- **Environment:** Darwin workspace; `/usr/bin/python3` reports Python `3.9.6`; `markdownlint` and `markdownlint-cli2` are not available

## Method

- **Procedure:** Read the accepted specification, root and reusable BOOTSTRAP files, root HANDOFF, accepted root ADR, every unresolved issue, reusable templates, and the two recent hardening evidence records. Compare normative statements with the repository tree and prior one-off validation procedures. Classify rules by whether a reproducible observation can decide them without interpreting intent.
- **Exact command/input:** `git status --short --branch`; `git rev-parse HEAD origin/main`; `git fetch origin main`; `git ls-tree -r --name-only 3dc8902`; `find protocol -type f -print | sort`; `find protocol -type l -print`; targeted `rg` reads for automation, validation, lifecycle, HANDOFF, and package-inventory rules; `python3 --version`; `command -v markdownlint`; `command -v markdownlint-cli2`
- **Exit status:** Baseline, fetch, ancestry, inventory, and source-inspection commands exited `0`; both Markdown-linter lookups returned no executable path
- **Repeatability:** Check out baseline `3dc8902f5ccd9fb67330e25e57380c119f717f25`, run the commands above, and read the linked sources in truth-precedence order.

## Raw observation

- `HEAD` and fetched `origin/main` both resolved to `3dc8902f5ccd9fb67330e25e57380c119f717f25`; the worktree was clean.
- No tracked `scripts/`, `tests/`, validator, or validation entry point existed at that baseline.
- `protocol/` contained exactly the ten paths required by `HARDEN-006` and the accepted ADR, and `find protocol -type l` returned no path.
- Both root and reusable HANDOFF files contained the five ordered top-level operational sections.
- Prior hardening evidence records successful one-off Python and shell checks, but also records discarded harness failures caused by capitalization assumptions, Python syntax, Unicode byte/string offsets, and Markdown-format assumptions. No reusable checker preserves those lessons as executable regression cases.

## Classification A — Human or agent judgment

These rules remain review and decision responsibilities. A tool may expose supporting facts but MUST NOT emit a compliance pass for them.

| Existing rule | Current enforcement method | Proposed validation method | Risk of over-automation |
|---|---|---|---|
| Interpret requirements, source conflicts, and specification sufficiency | Source-precedence reading, issue record, human escalation where required | No automated disposition; optionally report the sources inspected | A phrase or precedence match can conceal a substantive contradiction |
| Approve requirement evolution, scope, and durable architecture | Human technical-owner approval in `PROJECT_SPEC.md` and accepted ADRs | No automated approval | Metadata or checked boxes cannot authenticate authority or make a proposal accepted |
| Decide whether work is routine, meaningful, reversible, material, or architecture-preserving | Participant analysis under root BOOTSTRAP | No automated classification | Mechanical labels can weaken review gates or authorize work incorrectly |
| Establish reviewer independence and review quality | Attributable fresh-participant review of an immutable target | No automated pass; tools may only compare recorded identifiers as evidence | Different strings do not prove independent reasoning or identity |
| Judge evidence truth, adequacy, reproducibility, certainty, and proportionate verification | Direct reproduction plus reviewer interpretation | Tools may reproduce commands but cannot decide sufficiency | Successful execution can be irrelevant, incomplete, or based on the wrong artifact |
| Judge complexity justification, accepted debt, and architecture drift | Issue/ADR review using `ALIGNED`, `JUSTIFIED_DEVIATION`, `UNJUSTIFIED_DRIFT`, or `UNKNOWN` | No automated classification | Counting files or dependencies does not establish architectural fitness |
| Decide semantic snapshot staleness, HANDOFF compactness, or whether one action is bounded | Participant reconciliation against higher authority and live state | Validate only structural fields and nonempty content | Fresh timestamps and a single paragraph can still describe stale or unbounded work |

## Classification B — Deterministic invariants

The proposed method is intentionally narrower than the rule where interpretation remains necessary.

| Existing invariant | Current enforcement method | Proposed validation method | Risk of over-automation |
|---|---|---|---|
| Exact ten-file reusable-package inventory, regular files, and zero symlinks | Repeated `find`, Git-tree, and one-off Python checks | **First slice:** compare the filesystem with the authoritative ten-path manifest and reject symlinks/non-regular entries | Apply only to the source bundle; established-repository adoption deliberately has a different inventory |
| Package Markdown is UTF-8, ends with LF, has no trailing whitespace, and has balanced fences | One-off structural checker recorded in hardening evidence | **First slice:** deterministic byte and line scan | This is structural integrity, not CommonMark conformance or prose correctness |
| Relative links in the copy-ready bundle resolve | One-off fence-aware scans | **First slice:** parse supported inline links outside code, reject bundle escapes and symlink traversal, and return unsupported rather than pass ambiguous syntax | A resolving link can still target the wrong authoritative artifact; anchors remain semantic |
| HANDOFF has five unique ordered sections, snapshot labels, and one nonempty Next Action | Manual reads and one-off assertions | **First slice:** inspect root and reusable HANDOFF headings and required labels | Presence does not establish current evidence, compactness, or a substantively bounded action |
| IDs, filenames, timestamps, metadata enums, and required record sections agree | Templates and participant review | Future deterministic validation after a versioned schema is approved | Legacy `AEP-*` IDs and additive historical exceptions make an inferred schema brittle |
| Issue lifecycle, blocker fields, closure checklist, and HANDOFF issue index are structurally coherent | Issue template, manual review, bespoke assertions | Future validation after lifecycle grammar and exception behavior are explicit | Checked boxes do not prove authority, evidence, review quality, or closure |
| Recorded Git revision, branch, upstream, dirty state, and cited objects match the current repository | Start/resume commands and participant reconciliation | Future contextual snapshot command that reports observations only | Git is optional for adopters; remote equality and staleness are time-dependent |
| An isolated package copy preserves bytes, inventory, and navigation | Manual temporary-directory dry run | Future deterministic copy test using the same structural rules | A synthetic copy does not establish real-world adoption or migration safety |

## Classification C — Future automation candidates

| Candidate | Current enforcement method | Proposed validation method | Risk of over-automation |
|---|---|---|---|
| Agent orchestration, scheduling, and runtime coordination | Explicitly absent and deferred | None in this phase; requires a new accepted capability specification and compatible ADR | Would change the protocol from repository convention into a runtime system |
| Non-cooperating concurrent-writer guarantees | `BLOCKED` issue and cooperative Git checks | None in this phase | Local validation cannot supply locking, merge, or consistency guarantees |
| Authenticated identity and approval | Attributable text with explicit non-cryptographic limitation | None in this phase | Participant labels are provenance, not authenticated identity |
| Daemon, service, database, or complex CLI | Explicit non-goals | None | Adds lifecycle, persistence, failure, security, and portability obligations |
| Large-scale coordination and external tracker integration | Separate `BLOCKED` issues | None | Introduces synchronization authority and failure modes absent from the specification |

## Smallest useful executable slice

A manually invoked, read-only root checker can codify four already-stable structural families: the source-bundle manifest and file types, basic Markdown byte/fence integrity, supported relative-link resolution inside the bundle, and root/template HANDOFF shape. It will have deterministic rule identifiers and separate exits for violations and inability to evaluate. Tests will preserve the prior false-harness cases as regression inputs.

The checker will live outside `protocol/`, use only the Python 3 standard library, require no network or Git, write no project files, and remain optional. It will not ship with copied protocol files or become an adopter runtime dependency.

## Authority interpretation

- **CONFIRMED:** Root `PROJECT_SPEC.md` places executable contracts/tests in the truth hierarchy, permits a tiny helper where value is obvious, requires usefulness without automation, and prohibits a complex CLI or unnecessary automation.
- **CONFIRMED:** `HARDEN-006` and the accepted root-adoption ADR require the reusable `protocol/` bundle to remain exactly ten Markdown files with no runtime or language dependency.
- **INFERRED:** A root-only, standard-library, read-only structural test helper is local test organization authorized to validate existing contracts. It does not adopt the runtime/orchestrator capability deferred by [`ISSUE-20260806T013907Z-runtime-automation`](../ISSUES/ISSUE-20260806T013907Z-runtime-automation.md).
- **CONFIRMED:** Because the helper becomes an executable contract and a false pass could distort later compliance claims, the implementation issue uses independent review before closure even though no product or architecture authority change is proposed.

## Interpretation

- **CONFIRMED:** Stable deterministic invariants exist and currently depend on repeated participant-authored harnesses.
- **INFERRED:** The proposed slice is the smallest one that reuses prior evidence, catches common structural drift, and preserves the Markdown-first product boundary.
- **UNKNOWN:** Portability beyond the tested Python/Darwin environment, full CommonMark coverage, and the rate of false positives or negatives on future protocol prose.

## Limitations and residual uncertainty

- This analysis does not authorize a reusable CLI, adopter dependency, CI requirement, orchestration, or any deferred capability.
- Structural link resolution cannot prove semantic correctness or anchor validity.
- A dedicated Markdown linter is unavailable; the proposed checker is not a replacement for one.
- No claim is made about issue-lifecycle automation, production-grade validation, universal portability, participant compliance, or protocol maturity beyond the already approved hardening target.

## Integrity and provenance

- **Artifact location:** This file
- **Artifact digest:** To be captured after the analysis-boundary commit
- **External retention risk:** `NOT APPLICABLE`; source observations and limitations are repository-contained
- **Supersedes / superseded by:** `NONE`

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `NONE` | `NONE` | `NONE` | `NONE` |
