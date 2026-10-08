# Evidence — Scope-attribution amendment independent review round 2

## Metadata

- **ID:** `EVIDENCE-20261008T020134Z-scope-attribution-review-round-2`
- **Captured UTC:** `2026-10-08`; individual run capture time is in the raw JSON; disposition recorded `2026-10-08T02:04:10Z`.
- **Recorded by:** `agent:Codex-scope-review-20261008`, fresh independent reviewer; no authorship of the target, distinct from `agent:ClaudeCode-discovery-fix-3`. Label inequality is not authentication.
- **Claim challenged:** The round-2 rework closes all round-1 material findings and enforces general fail-closed intervening-authority attribution.
- **Authority:** [PROJECT_SPEC](../PROJECT_SPEC.md) PIPELINE-010 and its owner-approved 2026-09-30 change record; [accepted ADR decision 7](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md); [owning issue](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md), including the ten owner invariants and rework directive.
- **Immutable target:** `4f5e38744340fb7597222bf31483eb67187e2bbf`, parent `9000bb3d08eed6a64c8a16d136b9ada0a2c5469e`.
- **Recovered state:** clean `main`, HEAD and cached `origin/main` both `50e5994960c760457cb0f17e5bbe01a923694fd9`. Its post-target diff contains only target-pointer/parent reconciliation in HANDOFF and the owning issue. It is not the implementation target. Direct remote equality was not checked; this is not publication work.
- **Prior independent record:** [Round 1](EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md), target `6e39cea8ac46d909709ddaeeda1aa8d2df59ce08`, `CHANGES_REQUIRED`, R1–R5. Recovered from the issue and retained raw reproductions, not a conversation summary.
- **Environment:** Darwin 26.3.0 arm64, Python 3.9.6; exact Git/platform versions in [results.json](scope-attribution-review-round-2/results.json). Standard library only, no agent invocation/network dependency.
- **Disposition:** `CHANGES_REQUIRED`, **3 open material findings**: R2 HIGH, R3 HIGH, R5 MEDIUM. R1 and R4 are resolved within the independently verified bounds below.

## Method and reproducibility

From a clone retaining the target and baseline commits:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py . --suite
```

Exit `0` means the reproduction procedure completed, **not** protocol conformance. The exact procedure is retained in [reviewer_checks.py](scope-attribution-review-round-2/reviewer_checks.py); [results.json](scope-attribution-review-round-2/results.json) is its captured output. It extracts code/test helpers from the exact Git targets, never substitutes current HEAD implementation, and runs real pipeline CLI submissions only in disposable local fixture repositories. Fixture Git hashes/timestamps and durations vary on rerun; predicates and outcomes are reproducible. It reuses the retained round-1 reviewer scenario code rather than trusting the implementer's regression assertions.

Fixture-only v2 adaptations are explicit: add the declared `paths` matching each original separate scope; SELF declares none; same-issue test declares AGENTS; a second authority declares its own second path. Prevent the new helper's default `decision=True` from silently supplying the missing decision in an adverse scenario; positive SELF gets the required dated decision heading. The old null case's diagnostic parser call now raises, so the same JSON-null fixture is instead submitted through the actual CLI to check refusal and no mutation. Neither production code nor fixtures' accepted milestone allowlists are patched to obtain an outcome.

The optional `--suite` executes these exact argv forms inside the frozen target extraction (the absolute Python executable is recorded in JSON):

```sh
python3 -m unittest discover -s tests -p test_run_pipeline.py -v
python3 -m unittest discover -s tests -v
python3 scripts/validate_protocol.py
```

Independent Git inspection also used `git status --short --branch`, `git log --oneline -8`, `git diff 9000bb3 4f5e387`, and `git diff 4f5e387..HEAD`. Reviewed the changed source/tests directly, authority records, root role contract, both registered issues and their original owner/review records. The amendment is ordinary issue-level work with no pipeline state; the discovery dispatcher is not the authority for assigning this review.

## Raw observation

All three frozen-target checks exit `0`:

```text
Ran 42 tests in 47.658s
OK
Ran 187 tests in 55.064s
OK
PASS structural protocol validation (package_files=10 handoffs=2)
```

An earlier independent extraction in this session also passed 42 pipeline tests, 187 total tests and the validator; the recorded reproducible harness run above is the retained check evidence.

| Scenario group | Cases | Valid advances | Expected refusals observed | Unsafe advances |
|---|---:|---:|---:|---:|
| Original baseline `6e39cea` | 22 | 2 | 9 | 11 |
| Same scenarios adapted to v2 `4f5e387` | 22 | 2 | 20 | 0 |
| New v2 variants | 20 | 2 | 7 | 11 |

Every refusal preserved all fixture non-Git files and pipeline state. Every case preserved the original attempt base. Unsafe cases actually advanced to `AWAITING_PEER_REVIEW`, emitted submission evidence, and exited `0`; these are not merely permissive helper return values. Raw records include submitted registry entries, contradictory authority/review text, excluded paths, touching commits, covering ranges and stdout/stderr.

## Material findings and required follow-up

### R2 — HIGH — Declared scope remains unbound to separate authority and review

**Still open, not a new finding.** `scripts/run_pipeline.py` `_verify_intervening_entry` (target lines 789–881) treats caller-controlled `entry["paths"]` as the exclusion authority. Touched-path and foreign-path checks bind a declaration to Git content, not to the separate issue's authorized scope, reviewed range or review scope.

Three new submissions advance despite explicit owner/reviewer records excluding the earlier attempt-owned work:

- `declared_AGENTS_widening`: widen the range over an earlier unauthorized AGENTS commit and add `AGENTS.md` to `paths`. All gates pass. The paired `foreign_substantive_control`, with the same unauthorized path omitted from the declaration, correctly refuses. Thus arbitrary declaration, not separate authority, decides the outcome.
- `declared_prefix_widening`: declare `OTHER/`, swallowing earlier `OTHER/unapproved.md` although the separate authority/review only covers `OTHER/amendment.md`.
- `same_path_range_widening`: an earlier unauthorized attempt-owned change to `OTHER/amendment.md` is absorbed by widening the range; the later review expressly excludes earlier attempt work. This works without adding any extra path to the legitimate declaration.

**Impact:** the no-smuggling invariant still fails under valid v2 schema. Passing the original AGENTS regression by declaring only the legitimate path did not close the finding. A single untrusted declaration can make the range appear clean and supply apparent full commit coverage.

**Required:** bind both range ownership and each declared exclusion spec to verifiable separate durable authorization and applicable independent acceptance; reject unsupported broader prefixes, widened ranges over attempt-owned commits, and conflicting scope evidence. Preserve the original base/history, allowlist and HEAD semantics. Add these adverse cases and a legitimate separately scoped positive case. This review does not prescribe or authorize a new architecture/trust model; escalate if remediation requires one.

### R3 — HIGH — Review ambiguity still resolves to approval

**Still open.** `_tolerant_latest_review` (target lines 706–761) counts regex matches instead of validating an unambiguous value and only examines the first `Independent review rounds` section. Status validation (line 806) rejects only missing status and the exact token `BLOCKED`.

Five new submissions advance:

- `review_unknown_zero`: `UNKNOWN (lower bound 0); actual open count not established.` becomes zero.
- `review_negated_zero`: `NOT 0; material findings remain.` becomes zero.
- `review_41_hex_target`: a malformed 41-hex-character token becomes its first 40 characters and resolves to the approved ancestor.
- `review_duplicate_sections`: the first section's APPROVED/0 is selected while a second section contains a later CHANGES_REQUIRED/1 round. Ambiguous applicable review is silently ignored.
- `review_unresolved_status`: explicit `Status: UNRESOLVED` is accepted as resolved/nonblocked. The missing-status and exact-BLOCKED controls refuse.

**Required:** unambiguous section/round selection, exact bounded revision resolution, a positively established nonnegative finding count equal to zero, and consistent valid resolution status. Unknown, negated, duplicate/conflicting or malformed evidence must refuse before mutation. Preserve compatible *unambiguous* historical prose; do not treat extraction of a plausible token as proof. Authenticated authorship is not requested.

### R5 — MEDIUM — A heading is still substituted for an owner decision

**Still open.** The SELF branch (target lines 883–894) accepts any matching owner-decision heading anywhere in the text plus a mostly unconstrained nonempty unblock condition. It does not establish a positive attributable decision.

`self_pending_heading`, `self_empty_heading`, and `self_fenced_heading` all advance: respectively a dated heading whose body explicitly says the owner has NOT approved and the unblock condition is awaiting approval; a heading with no decision body; and a heading appearing only inside a fenced example introduced as no real decision. Each excludes the SELF issue file as if separately authorized. `self_blocked_control` refuses, and SELF cannot directly exclude a substantive path; that limits impact but does not establish the required owner authority.

**Required:** validate a real, positive, attributable durable owner decision satisfying the authority condition, outside examples/templates, with pending/absent/contradictory records refused. Preserve the no-declared-paths/own-file-only bound and add these variants. Merely adding the expected heading is not closure.

## Prior-round resolution and confirmed strengths

- **R1 resolved within this review's bounds:** `_commit_paths` now unions diffs against every parent and `_verify_target_scope` enumerates the entire commit window without path-limited simplification. Both original merge counterexamples refuse. The new asymmetric merge agrees with its first parent but differs substantively from another parent: it refuses. A three-parent record-only octopus advances; a three-parent substantive resolution refuses. Independently enumerated `git diff <parent> <commit>` unions agree with implementation touch sets for these merges and every commit in the real historical window. This is not an exhaustive proof over every possible Git graph.
- **R4 resolved:** old malformed-schema/null cases now refuse even for wholly in-scope targets; absence still passes. The frozen suite additionally exercises unverifiable present entries, malformed schema/ranges and refusal no-mutation cases. Registry verification executes before outside-path accounting.
- **R2 partial improvements:** distinct-issue/self-reference, unused declared path, foreign substantive path, overlapping equal/prefix scopes, partial coverage and cross-entry contradictory-range controls refuse. R2 remains open for the authority-binding variants above.
- **R3 partial improvements:** multiple hash/count tokens, unapproved review, label equality, missing status and exact BLOCKED cases refuse. These checks do not cure the remaining ambiguity cases.
- **R5 partial improvements:** absent decision heading and declared SELF substantive scope refuse; own-file restriction remains enforced.
- **Scope and history:** target changes are the eight expected root files (specification, pipeline ADR, implementation/tests, amendment/discovery records, HANDOFF/checkpoint); no product package, dependency, live runner or accidental fixture artifacts. Only registry schema/paths/timestamp changed in the discovery record, not its machine state. Spec/ADR strengthen the original approved invariants consistently, with no new state edge or target==HEAD change. Original target, round-1 record commit and accepted intervening commits remain ancestors; no rewrite/rebase/revert was used. The mechanism is general, not hard-coded to the real six paths/issues/hashes.

## Real discovery case — read-only characterization only

The harness reads both registered authority issues at the frozen target, checks their current bytes equal those versions, verifies entries using frozen code, then independently computes every touching commit using explicit diffs against every parent. It evaluates the historical candidate `9f72d3de57085525a8ddf8a3b14bf1a3161e26e8` from original base `88fa8359ec3a62f200096d0d96bd04a88ebd118a`. It does **not** invoke a transition on this repository or bypass target==HEAD.

- A: blocked-exit issue, HUMAN/INDEPENDENT; dated owner approval for the amendment, latest round `2026-09-24T01:19:04Z` by `agent:ClaudeCode-blocked-exit-review-20260924`, APPROVED/0 on `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3`, inside `ea2d393…79063cb`. The post-review commit is record-only. Its four declared substantive paths match the actual approved amendment; its own issue is the fifth exclusion.
- B: quota issue, HUMAN/SELF, dated positive owner decision `2026-09-23T01:32:06Z` and subsequent bounded decisions/outcomes; no declared paths, only its own issue excluded in `88fa835…9f72d3d`. The current OPEN status represents pending ordinary closure, not an unresolved approval for those historical records. This audit grants no new live authorization.
- All six original outside paths have exactly one covering entry and full touching-commit coverage. Removing A exposes its five paths; removing B exposes its one issue file. Existing A/B declarations cannot cover a hypothetical AGENTS change. Original milestone contract/digest, attempt base/events/state remain unchanged.

The exact six paths, full ranges, every touching hash and parsed provenance are in `real_case` in the raw JSON. Honest existing entries work; that does not close generic R2, whose forged/widened declaration is tested separately.

## Non-material observations

- **O1 LOW — Premature closure language / continuity:** HANDOFF and the implementer checkpoint call all R1–R5 resolved before independent confirmation. This review supersedes the current-state claim and appends an attributable correction, retaining authored history. Amendment metadata remains IMPLEMENTING; it has no separate pipeline machine state. The dispatcher still names the discovery implementer, but its generic submit action is not safe while this amendment has material findings.
- **O2 LOW — Exclusion audit convenience:** v2 materially improves evidence with each path, all touching commits, and a unique issue/from/to/review-class record after disjointness checks. Exact review target/round/reviewer or owner-decision reference still requires reconstructing the issue at the immutable submission target. That reconstruction is possible for valid A/B; this is not an extra blocker. Records cannot compensate for falsely verified provenance in R2/R3/R5.
- **O3 LOW — Inherited role wording:** implementer role contract says target parent equals attempt base, while higher-authority PIPELINE-010 requires preserved ancestor base across intervening work. Not introduced by this target and not used to reject the amendment. Reconcile through an authorized documentation change; no lower-tier wording overrides the accepted contract.

## Disposition, boundaries and limitations

`CHANGES_REQUIRED`: R2 HIGH, R3 HIGH, R5 MEDIUM remain open, not accepted debt. R1/R4 have independent resolution evidence. The issue remains IMPLEMENTING for bounded rework and a subsequent fresh review. No amendment machine state exists, so there is no lawful amendment pipeline transition to execute; discovery remains IN_PROGRESS attempt 3 with target null. Do not submit discovery, add another registry entry or perform acceptance/closure/recorder work based on this review.

No implementation/specification/ADR/test/product/bridge/discovery-issue changes, no live-agent probes, no discovery conformance/oracle rerun, no owner-identity authentication, no dependency install, no publication or remote mutation. Synthetic fixture hashes refer to disposable repositories, not retained Git objects; retained exact scripts and inputs reproduce them. The original repository history and both target revisions are required. No exhaustive hostile Git object/path universe or non-cooperating concurrency claim. Dedicated Markdown linters are unavailable (`command -v markdownlint markdownlint-cli2 pymarkdown` produced no path); local structural/link/fence/newline checks are used and do not replace a full Markdown linter. Broader portability is unverified.

## Governance verification and integrity

Reviewer-only records: this evidence, the reproduction/results and governance-check artifacts, appended owning-issue round, reconciled HANDOFF, and an appended human checkpoint. Exact post-write reads and final governance outputs are retained in [governance-readback.json](scope-attribution-review-round-2/governance-readback.json). Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-2/check_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
```

The governance check asserts the exact review target/disposition/count, preserved prior round/history, five HANDOFF sections and one Next Action, reviewer-only diff, unchanged discovery bytes/state and exactly two entries, raw-result counts, six-path audit and ancestry. Artifact identity is supplied by the eventual reviewer commit tree (resolve with `git log --` on this file); no unverifiable aggregate digest is claimed. External retention risk: none for these clone-resident records; ephemeral fixture objects are deliberately not retained.

## Attributable corrections

`2026-10-08T02:04:10Z`, `agent:Codex-scope-review-20261008`: the implementer's `2026-09-30T03:14:19Z` claim that all five material findings are resolved is not sustained. Original tests and exact original examples now pass/refuse correctly, but the general authority/review/SELF invariants still fail in eleven new variants. Preserve that authored summary as history; current disposition is CHANGES_REQUIRED with R2/R3/R5 open. No prior evidence is overwritten or reclassified.
