# Authorized Milestone Pipeline Attempt-2 Verification

## Metadata

- **ID:** `EVIDENCE-20260814T040812Z-authorized-pipeline-fix-verification`
- **Title:** Exact-target verification and review handoff for pipeline fix attempt 2
- **Captured UTC:** `2026-08-14T04:08:12Z`
- **Recorded by:** `Codex/root-fix-2`
- **Claim supported or challenged:** Immutable target `26d890f6e27ad181265ee5417a45637d867aa2dc` implements the recorded resolution conditions for independent-review findings `R1`/`R2` and non-material `R3`, passes the authorized deterministic gate, and is ready for fresh independent review. This evidence does not approve or accept the milestone.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `PIPELINE-004`, `PIPELINE-007`, and pipeline acceptance criteria
- **Related ADRs/issues:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md); [`ISSUE-20260806T013907Z-runtime-automation`](../ISSUES/ISSUE-20260806T013907Z-runtime-automation.md)
- **Prior evidence:** [`EVIDENCE-20260814T023224Z-authorized-pipeline-verification`](EVIDENCE-20260814T023224Z-authorized-pipeline-verification.md)
- **Generated evidence:** [`EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json`](EVIDENCE-20260814T040644Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-2.json)
- **Repository revision/state:** Target `26d890f6e27ad181265ee5417a45637d867aa2dc`, tree `86b53f3d5bd55697f3324350026015d5b791da53`, direct parent/attempt boundary `87cf4acd222ce280d9f5d5ced301212e5ec4cc09`, state after submission `AWAITING_PEER_REVIEW`
- **Environment:** Darwin `25.3.0` arm64; Python `3.9.6`; Apple Git `2.50.1`; standard library only

## Problem and review boundary

Independent round 1 against target `6c0a3bd` recorded `CHANGES_REQUIRED` with two material findings:

- `R1`: accepted commands could mutate HEAD, tracked/untracked/ignored worktree content, or loaded authority/state sources without a post-command check, yet submission could advance.
- `R2`: a missing ownership check on root `EVIDENCE/` allowed a symlinked directory to receive generated JSON outside the repository and poison later state loading.

The same round classified `R3` as a non-material Markdown rendering defect: generated activity rows could be separated from their table and verification prose could touch the next heading.

The accepted specification authorizes correction and re-review inside the existing milestone. It does not authorize new scope, a specification/ADR change, package runtime, identity authentication, or concurrent-writer guarantees.

## Change

- Review submission captures the expected target plus exact loaded `PROJECT_SPEC.md` and owning-issue bytes, rejects pre-existing ignored artifacts, and records four ordered post-command conditions: HEAD identity, tracked/untracked/ignored cleanliness, authority-source bytes, and issue-source bytes.
- Failed accepted commands or failed repository postconditions produce bounded `FAIL` evidence when `EVIDENCE/` remains safe, and never advance issue state. Observed command side effects are preserved rather than silently reverted.
- Orientation and output creation both require root `EVIDENCE/` to be an existing, contained, real non-symlink directory. Atomic writes no longer create a missing parent implicitly.
- Prose and activity-table insertion are separate. Activity history retains every row and order while removing only blank lines that split the table; generated prose retains a blank line before the next heading.
- No CLI command or option changed. Generated `aep-pipeline-verification/v1` evidence gains the lower-precedence `repository_postconditions` observation field.

## Verification method and observations

| Check | Exact procedure | Result |
|---|---|---|
| Authorized pipeline submission | `python3 scripts/run_pipeline.py transition --milestone MILESTONE-20260814T015817Z-authorized-pipeline-v1 --actor agent:Codex-root-fix-2 --to AWAITING_PEER_REVIEW --target 26d890f6e27ad181265ee5417a45637d867aa2dc` | Exit `0`; state advanced only from `IN_PROGRESS` to `AWAITING_PEER_REVIEW`; generated evidence result `PASS` |
| Accepted command | Pipeline-executed `python3 -m unittest discover -s tests -v` with bounded timeout, `shell=False`, credential-bearing environment fragments removed, and bytecode disabled | Exit `0`; `Ran 44 tests in 17.135s`; `OK`; stdout `0` bytes, stderr `5,083` bytes, neither truncated |
| Repository postconditions | Inspect generated attempt-2 JSON | Four ordered `PASS` results: `head-unchanged`, `worktree-clean`, `authority-source-unchanged`, and `issue-source-unchanged` |
| Exact-target reproduction | Extract `git archive 26d890f...` into a temporary path containing spaces; rerun the full suite and structural validator | `Ran 44 tests in 17.391s`; `OK`; `PASS structural protocol validation (package_files=10 handoffs=2)` |
| Mutation regressions | Isolated local Git fixtures for ordinary untracked output, ignored `.DS_Store`, an accepted-command Git commit, and exact specification/issue byte edits hidden with `skip-worktree` | Each submission fails with `AEP-PIPE-VERIFY`, creates `FAIL` evidence when the evidence boundary is safe, and retains `IN_PROGRESS` state |
| Evidence-boundary regressions | Missing path, regular file, baseline symlink to a sibling directory, and accepted-command replacement of the directory with a symlink before output | Orientation/pre-write returns exit `2`; no outside evidence file appears; issue state does not advance |
| Ignored baseline | A real root `.DS_Store` was visible through the new ignored-path query but absent from ordinary short status | Artifact was verified as Apple Desktop Services metadata and moved recoverably to `/Users/matthew/.Trash/agentic-engineering-protocol-root-DS_Store-20260814T035900Z`; strict submission then passed |
| Markdown continuity | Fixture begins with a deliberately split activity table, traverses lifecycle submission, then checks table/prose boundaries | All table rows are contiguous; blank-line separation before following headings passes; historical row content/order is retained |
| Compilation | `python3 -m py_compile` for both scripts and both test modules with `PYTHONPYCACHEPREFIX` in a temporary directory | Exit `0`; four source files compiled; temporary cache removed automatically |
| Package copy | Copy `protocol/` plus root HANDOFF to an isolated path containing spaces; compare SHA-256 per package file and run structural validation | Ten files; byte-identical; zero symlinks; validation passes |
| Repository Markdown/links | UTF-8, final-newline, trailing-whitespace, fence, supported relative-link, containment, and existence scan outside fenced/inline code | `43` Markdown files; `216` relative links; zero findings |
| Scope and governed sources | `git diff --check 57fe35c..26d890f`; compare changed paths with accepted allowlist; compare specification, BOOTSTRAP, ADR, reusable package, README, templates, and both wording issues with baseline | Whitespace passes; exactly five allowed paths changed; governed sources and wording change sets are unchanged |
| Credential-shaped content | Standard-library byte regex over the exact `57fe35c..26d890f` diff | `63,234` diff bytes scanned; zero matches |

One preliminary credential-scan command is not claimed: zsh rejected its inline regular expression with `bad pattern` before scanning. The same intended patterns were rerun over the exact diff with Python's standard-library regex engine; only that successful rerun supplies the result above.

## Finding-resolution mapping

| Finding | Resolution evidence | Current classification |
|---|---|---|
| `R1` / `F1` | Pre-submit ignored-artifact refusal; four post-command checks; machine-readable failed-result evidence; ordinary, ignored, HEAD, authority-byte, and issue-byte regressions | Implementor evidence says resolved at `26d890f`; remains an open acceptance finding until fresh independent review |
| `R2` / `F2` | Real-directory/containment validation at orientation and immediately before write; missing/file/baseline-symlink/transition-swap regressions; no implicit parent creation | Implementor evidence says resolved at `26d890f`; remains an open acceptance finding until fresh independent review |
| `R3` / `F3` | Specialized prose/table insertion, historical whitespace-only normalization, and rendering-continuity regression | Implementor evidence says resolved at `26d890f`; fresh reviewer should confirm |

## Integrity and provenance

- Generated evidence SHA-256: `33f756c77a5f33c02083a524e0bf19a16cb057b4589b9754ee224153e5d77246`.
- Target `scripts/run_pipeline.py` SHA-256: `a9f2af2ea83903ac8cc78f4dab023bd25a43d2294e46861ff797b190b2d26f11`.
- Target `tests/test_run_pipeline.py` SHA-256: `4b8ea98a0c763653d9f0c136cc517d46fbb59ae77deb247159e90903a467cfb9`.
- Unchanged target `PROJECT_SPEC.md` SHA-256: `efafb0a257d3507f375e2ce08125aaee899615d5a6f205d631ceaaaa15b12ecf`.
- Unchanged pipeline ADR SHA-256: `f24c15f28dd3ed9e3926ae3fec103560d257abd21102170b1d804149746e136a`.
- Target reusable-package tree: `70cf91821a3ae7651b2eea2644aea2a62d29aaf6`, unchanged from attempt 1.
- Target range from attempt-2 base changes exactly `HANDOFF.md`, `HUMAN_CHECKPOINT.md`, the owning runtime issue, `scripts/run_pipeline.py`, and `tests/test_run_pipeline.py`.

## Limitations and residual uncertainty

- This is implementor verification, not independent review. It supplies no disposition and cannot accept or close the milestone.
- Validation is limited to Darwin arm64, Python `3.9.6`, and Apple Git `2.50.1`; no broader portability claim is made.
- `markdownlint` and `markdownlint-cli2` remain `NOT AVAILABLE`; the repository scan is not claimed as full CommonMark conformance.
- Participant labels remain unauthenticated assertions. Non-cooperating concurrent writers and the filesystem TOCTOU window remain outside the accepted failure model and linked to blocked issues.
- Owner-authorized commands are still trusted executable content. The tool detects their persisted repository mutations; it does not prove their semantic safety or undo their effects.
- If an accepted command destroys or redirects `EVIDENCE/`, the pipeline refuses to write outside the repository and cannot preserve a JSON failure record there. The CLI error and unchanged issue state are then the observable failure boundary.
- The Trash recovery path is local and non-durable; it is recorded only to make the removal recoverable in this environment, not as project evidence required by future clones.

## Interpretation

- **CONFIRMED:** Target `26d890f` passes all owner-authorized deterministic checks and the new explicit repository postconditions.
- **CONFIRMED:** The reusable ten-file package and all accepted authority artifacts are unchanged.
- **CONFIRMED:** Pipeline state is `AWAITING_PEER_REVIEW`; no implementation or authority file changed after the target.
- **INFERRED:** The exact independent resolution conditions for `R1`/`R2` and the selected correction for `R3` are implemented completely.
- **UNKNOWN:** Fresh independent disposition and milestone acceptance.
