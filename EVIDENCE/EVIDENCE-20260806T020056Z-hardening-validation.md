# Post-Pilot Hardening Validation

## Metadata

- **ID:** `EVIDENCE-20260806T020056Z-hardening-validation`
- **Title:** Structural, semantic, preservation, and isolated-copy validation
- **Captured UTC:** `2026-08-06T02:00:56Z`
- **Recorded by:** `Codex/root`
- **Claim supported or challenged:** The hardening candidate implements the accepted record architecture without changing package inventory, losing historical records, breaking links, or overstating pilot portability.
- **Related requirements:** [`HARDEN-001` through `HARDEN-008`](../PROJECT_SPEC.md)
- **Related ADRs/issues:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ISSUE-20260806T013907Z-post-pilot-hardening`](../ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md)
- **Repository revision/state:** Parent/authority boundary `7dea5457828b6590f9ab2a643b58047b032e53d1` plus the intended uncommitted hardening worktree; immutable implementation target pending
- **Environment:** Darwin; Git; Python 3 standard library; POSIX shell; dedicated Markdown/shell linters unavailable

## Method

Validation was layered so an individual failed assertion did not obscure its cause:

1. Inspect the complete diff, status, inventory, and whitespace.
2. Run a standard-library Markdown/semantic checker over every repository Markdown file outside `.git`.
3. Compare the root specification-evolution policy byte-for-byte with the approved reusable policy body.
4. Compare the migrated pilot record byte-for-byte with `PILOT_EVIDENCE.md` at `e6beeb2`.
5. Compare each migrated legacy issue body byte-for-byte with its source section in `HANDOFF.md` at `7dea545`.
6. Copy `protocol/` into an isolated temporary directory; compare bytes, inventory, links, entrypoint, onboarding, and snapshot contract; then move the fixture to Trash because direct recursive removal was tool-policy rejected.
7. Query dedicated lint-tool availability without installing anything.

### Exact commands or procedures

Simple checks:

```sh
git diff --check
git diff --stat 7dea545
git diff --name-status 7dea545
git status --short --branch
rg --files -g '!**/.git/**' | sort
shasum -a 256 BOOTSTRAP.md PROJECT_SPEC.md protocol/BOOTSTRAP.md protocol/HANDOFF.md EVIDENCE/EVIDENCE-20260805T035052Z-isolated-pilot.md
git show e6beeb2:BOOTSTRAP.md | shasum -a 256
git show e6beeb2:PROJECT_SPEC.md | shasum -a 256
```

The semantic checker used `pathlib`, `re`, and `subprocess` only. It:

- required the exact ten-path package manifest and zero symlinks;
- decoded all Markdown as UTF-8 and required final newlines, no trailing whitespace, and balanced backtick/tilde fences;
- ignored fenced code while resolving relative Markdown links;
- required exactly the five ordered HANDOFF sections, one nonempty single-line Next Action, at least ten recent entries, populated metadata, no `CLOSED` active issue, no terminal task state in live Current State, and a nonempty archive;
- extracted text between `## Specification evolution` and `## Specification change record` from root and reusable specifications and required exact equality;
- required the ordered seven root truth tiers, root/product governance boundary, continuity rule, authority/review/failure/drift semantics, `HARDEN-001` through `HARDEN-008`, all five deferrals, and reusable snapshot/staleness language;
- required all five legacy issue IDs/files, byte-identical pilot evidence, and exactly two changed reusable paths (`protocol/BOOTSTRAP.md` and `protocol/HANDOFF.md`).

Legacy issue preservation was independently checked by extracting each `### AEP-...` block through its next peer/top-level heading from `git show 7dea545:HANDOFF.md` and comparing it with the same marker-to-EOF body in its migrated file.

The isolated-copy procedure was:

```sh
copy_root=$(mktemp -d /tmp/aep-hardening-copy.XXXXXX)
cp -R protocol/. "$copy_root"/
diff -qr protocol "$copy_root"
```

A standard-library checker inside that directory required the ten exact files, regular files only, all relative links resolved inside the copy, `BOOTSTRAP.md` present with `## Start or resume procedure`, and HANDOFF snapshot metadata. The observed fixture was `/tmp/aep-hardening-copy.zD6bKT`. Direct `rm -rf` cleanup was rejected by tool policy; the exact directory was moved recoverably to `/Users/matthew/.Trash/aep-hardening-copy.zD6bKT` after confirming the destination did not exist.

Tool availability was queried with `command -v` for `markdownlint`, `markdownlint-cli2`, and `shellcheck`.

## Raw observation

Corrected semantic run:

```text
markdown_files=33 relative_links=94 missing_links=0
protocol_inventory=10 symlinks=0 handoff_lines=222 recent_entries=13
policy_exact_match=True precedence_tiers=7 protocol_changed_files=2 pilot_byte_preserved=True
PASS
```

Legacy extraction:

```text
AEP-20260805T020501Z-protocol-v1 byte_body_match=True lines=8
AEP-20260805T031247Z-release-preparation byte_body_match=True lines=10
AEP-20260805T035052Z-real-repository-pilot byte_body_match=True lines=10
AEP-20260805T041340Z-readme-migration-gap byte_body_match=True lines=34
AEP-20260805T095724Z-specification-evolution byte_body_match=True lines=47
legacy_issue_extraction=PASS
```

Isolated copy:

```text
inventory=10 links=23 missing=0
inventory_exact=True
regular_files_only=True
links_resolve=True
entrypoint_present=True
onboarding_present=True
snapshot_contract_present=True
isolated_copy=PASS
temporary copy moved to Trash
```

Recorded hashes:

```text
root BOOTSTRAP candidate: a0a1c09cbcd36c6d9404e0a8f41da79ea09b52def51105eead6184aca08414e0
root PROJECT_SPEC candidate: 022c70a126d6acad2955b815397a7d4e5280930a696e931700bfd195f5a312cd
protocol/BOOTSTRAP candidate: d2f087044efbcd8c0ed1c8cb7f4612e0cf87d14a0c0e304ab3910eeb27e26513
protocol/HANDOFF candidate: 7162c79976d4dd596bb6d292e4d522f9d266ba5ddfbc49b9874d77a312a879c7
migrated pilot: dab1274cb74d62ec263fdb0acb86591d74f3d79efd4891e2140c08f9e314651f
pre-hardening root BOOTSTRAP: 8fcfc3fe52608a1b42305bb12696d3f151be468bbbf638918cf93b651414dfe6
pre-hardening root PROJECT_SPEC: 13169319e2be028c470ca96925002b25c000c58ba3a4c5420e652d291df139dd
```

Tool availability:

```text
markdownlint=NOT_AVAILABLE
markdownlint-cli2=NOT_AVAILABLE
shellcheck=NOT_AVAILABLE
```

## Interpretation

- **CONFIRMED:** All repository-relative links visible outside fenced code resolved; Markdown structural checks passed; package inventory and no-symlink contract remained intact.
- **CONFIRMED:** The root specification-evolution policy body exactly matches the previously approved reusable policy and retains evidence/ADR/human-authority semantics.
- **CONFIRMED:** The pilot move and each legacy issue extraction preserve their historical content byte-for-byte at the stated boundaries.
- **CONFIRMED:** An isolated copy contains every package artifact and all package links resolve without root files.
- **CONFIRMED:** Root and reusable BOOTSTRAP files are distinct; exactly two reusable files changed in the approved scope.
- **UNKNOWN:** Independent review disposition, full CommonMark rendering, broader platform/filesystem/repository portability, concurrency behavior, authenticated identity, and scale.

## Limitations and residual uncertainty

- The first semantic run produced one false failure because its expected phrase used lowercase `root/product` while the document contained capitalized `Root/product`. The content already contained the required rule. That failed harness result was discarded; the corrected assertion reran the complete suite and passed.
- The structural checker is fence-aware but not a full CommonMark implementation. Dedicated Markdown linters were unavailable and were not counted as passed.
- The isolated copy proves package self-containment for this filesystem/run only; the temporary fixture itself is not durable evidence.
- Original pilot tests/commits remain absent from this repository; no production-grade, universal, concurrent, authenticated, or large-scale claim follows.
- This is attributable implementor verification. It cannot satisfy the required fresh independent review.

## Integrity and provenance

- **Artifact location:** `EVIDENCE/EVIDENCE-20260806T020056Z-hardening-validation.md`
- **Artifact digest:** Identified by the containing immutable implementation target once committed; a file cannot contain its own final digest.
- **External retention risk:** The isolated fixture is recoverably in local Trash and is not required to reproduce the documented copy procedure.
- **Supersedes / superseded by:** Supplements [`EVIDENCE-20260806T013907Z-post-pilot-audit`](EVIDENCE-20260806T013907Z-post-pilot-audit.md); final post-record rerun will be appended below.

## Corrections and final reruns

| UTC time | Participant | Correction or rerun | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-06T02:00:56Z` | `Codex/root` | Discarded the initial case-sensitive phrase failure and reran the complete corrected suite to `PASS` | The required `Root/product protocol divergence` rule was present; only the checker expectation differed in capitalization |
| `2026-08-06T02:05:56Z` | `Codex/root` | Discarded a post-record validation attempt that stopped at a Python f-string syntax error before performing assertions | The attempt produced no semantic result; a following shell whitespace command cannot convert it into a pass |
| `2026-08-06T02:05:56Z` | `Codex/root` | Corrected the reporting expression and reran the complete post-record suite to `PASS`; `git diff --check` also exited `0` | `markdown_files=34 links=105 missing=0 whitespace_fence_failures=0`; package `10`, symlinks `0`, HANDOFF `236` lines/5 sections/1 action/14 activities/6 unresolved issues/nonempty archive, seven tiers, exact policy, pilot bytes, and five legacy bodies all passed |
