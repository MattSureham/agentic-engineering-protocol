# Structural Validator Verification

## Metadata

- **ID:** `EVIDENCE-20260811T020454Z-structural-validator-verification`
- **Title:** Verify the immutable minimal structural-validator target
- **Captured UTC:** `2026-08-11T02:04:54Z`
- **Recorded by:** `Codex/root`
- **Claim supported or challenged:** Immutable target `8690358d499aed20de6c620dc4dd4a81f1e1a126` implements only the analysis-bounded, root-local structural checker; it passes its executable suite without changing the reusable package or governed Markdown sources.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), especially Scope constraints, Quality bar, `HARDEN-003`, `HARDEN-006`, and hardening acceptance criterion 5
- **Related ADRs/issues:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ISSUE-20260811T013701Z-structural-protocol-validator`](../ISSUES/ISSUE-20260811T013701Z-structural-protocol-validator.md); [`EVIDENCE-20260811T013701Z-codification-gap-analysis`](EVIDENCE-20260811T013701Z-codification-gap-analysis.md)
- **Repository revision/state:** Implementation target `8690358d499aed20de6c620dc4dd4a81f1e1a126`; tree `3c55c49d9a9572ceb01c17d1369af8f90a2bbfe4`; direct parent/analysis boundary `57c274641c1e779dbf95d36ed1ba0a03d7ef8fa7`; clean worktree immediately after target commit
- **Environment:** Darwin workspace; `/usr/bin/python3` version `3.9.6`; Git worktree on `main`; dedicated `markdownlint` and `markdownlint-cli2` executables unavailable

## Method

- **Procedure:** Run the checker and full standard-library test suite against the exact checked-out target; compile both Python files; compare repeated checker output; inspect the target diff and governed-source identities; validate package inventory and symlink absence; scan changed paths for credential-shaped material; run a separate repository-wide structural relative-link scan; confirm whitespace and Git state.
- **Exact command/input:** `python3 -m unittest discover -s tests -v`; `python3 -m py_compile scripts/validate_protocol.py tests/test_validate_protocol.py`; `python3 scripts/validate_protocol.py`; `cmp <(python3 scripts/validate_protocol.py) <(python3 scripts/validate_protocol.py)`; `git diff --check 57c2746..8690358`; `git diff --name-status 57c2746..8690358`; `git rev-parse` for commit/tree/package identities; `shasum -a 256` for governed root sources; standard-library package inventory/symlink check; bounded credential-pattern `rg`; fence-aware repository-relative-link scan
- **Exit status:** All executed exact-target checks exited `0`. Dedicated Markdown linters were queried and returned `NOT_AVAILABLE` rather than a test result.
- **Repeatability:** Check out `8690358d499aed20de6c620dc4dd4a81f1e1a126` and run the commands above from its repository root. The unit suite creates and removes isolated temporary fixtures itself and requires no network or Git access.

## Raw observation

```text
Ran 21 tests in 1.636s

OK
PASS structural protocol validation (package_files=10 handoffs=2)
package_files=10 symlinks=0
markdownlint=NOT_AVAILABLE
markdownlint_cli2=NOT_AVAILABLE
```

The target range changed exactly:

```text
M .gitignore
M HANDOFF.md
M HUMAN_CHECKPOINT.md
M ISSUES/ISSUE-20260811T013701Z-structural-protocol-validator.md
M README.md
A scripts/validate_protocol.py
A tests/test_validate_protocol.py
```

The protocol tree at both parent and target is `4e79dd41eda4bac91329cf2fa8a88cd96bd168cb`. Governed-source SHA-256 values remain:

```text
022c70a126d6acad2955b815397a7d4e5280930a696e931700bfd195f5a312cd  PROJECT_SPEC.md
a0a1c09cbcd36c6d9404e0a8f41da79ea09b52def51105eead6184aca08414e0  BOOTSTRAP.md
76849583a4fc0553ee1cbdb2a4c225f6f64bd26248739c19c786f3c3b4ab25a0  ADR/ADR-20260806T013907Z-root-protocol-adoption.md
bd222ada0af7b699c704e64b44563199511c1eec1af54664bb467b499e5ad427  ISSUES/ISSUE-20260806T013907Z-runtime-automation.md
```

A separate structural scan before this evidence file was added covered 38 Markdown files and 150 relative links with zero missing targets. After all review-handoff records were prepared, the scan covered 39 Markdown files and 159 relative links with zero missing targets.

## Implemented rule boundary

| Rule family | Mechanically established | Explicitly not established |
|---|---|---|
| `AEP-PKG-*` | Exact source manifest, expected directories, regular entries, and no symlinks | Correctness of established-repository migration layouts |
| `AEP-MD-*` | UTF-8, final newline, trailing whitespace, balanced supported fences, and supported relative-link target existence/containment | Full CommonMark, anchor correctness, semantic target correctness, or unsupported reference/indented-container syntax |
| `AEP-HANDOFF-*` | Five ordered headings outside fences, required snapshot-field presence, and one nonempty Next Action section | Snapshot truth/freshness, compactness, or whether the action is substantively bounded |
| `AEP-TOOL-*` | Distinct evaluator/unsupported exit `2` rather than false success | Universal environment or filesystem-failure behavior |

## Preparatory findings and corrections

The issue preserves two adversarial pre-review rounds and all corrections. Initial findings exposed fenced HANDOFF false structure, an indented-list link false pass, nested-code false violations, local-path classification, traversal-error handling, and CLI-summary behavior. A follow-up exposed inline masking across a blank block, list-item fence handling, and ambiguous one-letter URI classification. Regression tests were added for every reported case.

One intermediate corrected-suite run exited `1` because multiline masking also replaced newline characters and triggered a caught evaluator `IndexError`; the implementation was corrected to preserve line boundaries. One combined shell harness was `NOT RUN` because the execution layer rejected its temporary cleanup form before process creation. Neither event is represented as a protocol failure or a successful check; subsequent safe exact-target commands provide the results above.

One post-record scope assertion exited `1` because it used `git diff --name-only`, which does not list an untracked evidence file. The corrected assertion derived paths from `git status --short --untracked-files=all` and confirmed exactly the intended four review-handoff records. This was a harness-selection error, not a repository-scope failure.

The final bounded preparatory recheck reported all three follow-up findings resolved, all 21 tests passing, and no remaining HIGH or MEDIUM regression within that recheck. This was implementation preparation, not the required independent review of the immutable target.

## Interpretation

- **CONFIRMED:** Target `8690358d499aed20de6c620dc4dd4a81f1e1a126` provides a deterministic, read-only root validation entry point and standard-library regression suite for the approved structural slice.
- **CONFIRMED:** The reusable `protocol/` bundle is byte-identical by Git-tree identity to the analysis-boundary package and remains exactly ten regular Markdown files with zero symlinks.
- **CONFIRMED:** Root `PROJECT_SPEC.md`, root `BOOTSTRAP.md`, the accepted ADR, and the blocked runtime-automation issue retain their recorded SHA-256 values.
- **INFERRED:** The target remains local test organization rather than product runtime automation because no executable enters `protocol/`, no adopter dependency or background lifecycle is created, and the Markdown authorities remain higher precedence.
- **UNKNOWN:** Fresh independent review disposition, behavior outside Python `3.9.6` on Darwin, and future Markdown syntax outside the tested subset.

## Limitations and residual uncertainty

- The validator is deliberately not a CommonMark parser. Reference-style links and link-like syntax in indented containers return unsupported exit `2`; semantic link destinations and anchors remain judgment/review concerns.
- The tests demonstrate read-only behavior for captured fixture trees and static inspection found no write, network, Git, or child-process operation in the validator itself. They do not prove behavior against every filesystem implementation.
- No CI requirement, adopter runtime, reusable CLI, service, daemon, database, orchestration, identity, concurrency, scale, or external-tracker capability is implemented or authorized.
- The separate repository-wide link scan is a structural supplemental harness, not a Markdown renderer.
- Dedicated Markdown linting and broader platform testing were unavailable and are not passes.
- The implementation issue remains `REVIEW`; this evidence cannot satisfy its independent-review gate.

## Integrity and provenance

- **Artifact location:** This file; immutable implementation is Git commit `8690358d499aed20de6c620dc4dd4a81f1e1a126`
- **Artifact digest:** Implementation tree `3c55c49d9a9572ceb01c17d1369af8f90a2bbfe4`; this evidence file's Git blob is supplied by its containing review-handoff commit
- **External retention risk:** `NOT APPLICABLE` for committed source and test evidence; preparatory agent messages are summarized durably in the owning issue and this record
- **Supersedes / superseded by:** `NONE`

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `NONE` | `NONE` | `NONE` | `NONE` |
