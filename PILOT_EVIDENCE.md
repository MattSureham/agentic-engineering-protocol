# Isolated Real-Repository Pilot Evidence

## Metadata

- **Pilot ID:** `AEP-20260805T035052Z-real-repository-pilot`
- **Coordinator:** `Codex/root`
- **Started UTC:** `2026-08-05T03:50:52Z`
- **Completed UTC:** `2026-08-05T04:17:16Z`
- **Target:** `/Users/matthew/Projects/aep-protocol-pilot`
- **Authorization:** The human technical owner selected an isolated local fixture
  and accepted `REQ-ORDER-001` at `2026-08-05T03:48:23Z`.
- **Safety boundary:** Local-only and non-production; no remote, push,
  dependency, credentials, production access, persistence, networking, or
  additional public interface authorized.

## Source state

- Root release state before mutation: `99ed41874157b0da537b1399bef907c82454fb1e`
- Immutable protocol release commit:
  `a6270ebeb02f936184895dcad32269d8a16a0da5`
- Protocol Git tree: `935cdb22f4472daa61b91d64f26f8893c4046fbf`
- Root worktree before pilot: clean, branch `main`, tracking `origin/main` at
  the same `99ed41874157b0da537b1399bef907c82454fb1e` revision.

The Git tree is the reproducible identifier for the copied package. The older
aggregate SHA-256 in HANDOFF has no recorded aggregation procedure and is not
treated as independently reproducible.

## Target initialization

### Durable revisions

- Seed fixture: `0491081c7d700ac354b3031342308d6b29d12aca`
- Protocol initialization: `abb8ce26e31dc90d676ec9df9c7fb69003e68e7a`
- Remote configuration: none (`git remote -v` produced no output).

### Migration preflight

The destination was checked for every package path before copying. Nine paths
were clear and `README.md` was the only collision. The application README was
preserved; the byte-identical package README was copied as
`PROTOCOL_GUIDE.md`, and the application README received navigation links.
The other eight unchanged artifacts plus the HANDOFF template matched their
release-package source bytes after copying. The target-specific
`PROJECT_SPEC.md` was then filled from the accepted owner decision.

This demonstrates a `LOW` usability friction: the quick start warns against
overwriting existing files but supplies no canonical migration name or merge
procedure for the conventional application `README.md` collision.

### Baseline reproduction

Command:

```sh
python3 -m unittest discover -s tests -v
```

Result: exit `1`; five tests ran and exactly one failed.

```text
test_preserves_first_occurrence_order ... FAIL
['alpha', 'beta', 'gamma'] != ['beta', 'alpha', 'gamma']
Ran 5 tests
FAILED (failures=1)
```

The observation confirms that the seeded implementation violates accepted
encounter order while the duplicate-equality, whitespace/empty-string,
empty-input, and input-nonmutation scenarios pass.

## Fresh-participant tasks

### Implementor

- Task reference: `/root/pilot_implementor`
- Lifecycle ID: `TASK-20260805T035313Z-fresh-pilot-implementor`
- Context: spawned without inherited conversation and given the filled Fresh
  implementor prompt, target path, accepted scope, and safety boundary.
- Terminal result: `SUCCEEDED`. It produced implementation target
  `0606979a57d821e3777d1b81e0834512d9a184d0` and clean target HANDOFF commit
  `6a2c0e5d6f3959de7e0648d5ee8494626fff12f0`, leaving the issue in `REVIEW`.

### Independent reviewer

- Task reference: `/root/pilot_reviewer`
- Lifecycle ID: `TASK-20260805T040210Z-pilot-independent-review`
- Context: a different context-free participant received the Independent
  reviewer prompt and directly inspected authoritative sources, implementation,
  tests, evidence, and Git state.
- Terminal result: `SUCCEEDED` with disposition `APPROVED`. It closed the target
  issue and produced review-record commit
  `3a8f3922f47dec16144493482bd2b7a150ef5b0a`.

The reviewer also spawned terminal child tasks
`/root/pilot_reviewer/authority_contracts` and
`/root/pilot_reviewer/implementation_edges`. Both returned `SUCCEEDED` before
the parent completed and their findings were synthesized into the review round.
The target HANDOFF nevertheless claims that the reviewer started no background
work. Root HANDOFF now preserves both recovered task references, bounded start
windows, terminal states, and evidence.

## Coordinator verification

Coordinator checks at clean target HEAD
`6a2c0e5d6f3959de7e0648d5ee8494626fff12f0` independently established:

- The implementation diff against `abb8ce26e31dc90d676ec9df9c7fb69003e68e7a`
  is exactly one expression: `sorted(set(values))` became
  `list(dict.fromkeys(values))`.
- `python3 -m unittest discover -s tests -v` exited `0`; all five accepted
  scenarios passed on Python `3.9.6`.
- `git diff --check abb8ce26e31dc90d676ec9df9c7fb69003e68e7a..HEAD`
  exited `0` with no output.
- The target worktree was clean; `git remote -v`, dependency-manifest scan,
  and symlink scan produced no findings.
- Fifty-two relative Markdown links resolved; no trailing whitespace, missing
  final newline, or unbalanced fence was found.
- HANDOFF contained the five ordered sections and exactly one bounded action to
  obtain independent review.

The independent reviewer then established:

- Exact target `0606979a57d821e3777d1b81e0834512d9a184d0`, tree
  `1fa8942170b8c280d417efb7e8686cdaca6e84db`, parent
  `abb8ce26e31dc90d676ec9df9c7fb69003e68e7a`, with no post-target product drift.
- The exact baseline archive reproduced exit `1` and one order failure; the
  target archive passed all five accepted tests.
- A manual first-occurrence reference comparison passed 19,608 bounded cases,
  including output-identity and input-nonmutation assertions. Direct
  distinct-but-equal and fresh-empty-result checks also passed.
- A commit-ranged `git diff --check` passed; no remote, dependency manifest,
  non-template ADR, hidden caller, prohibited complexity, or security surface
  was found.
- Disposition `APPROVED`, no material finding, and two low limitations described
  below.

Final coordinator checks at clean target HEAD
`3a8f3922f47dec16144493482bd2b7a150ef5b0a` reran the five-test suite and
commit-ranged whitespace check, resolved 56 Markdown links with zero missing,
found no newline/whitespace/fence, symlink, dependency, or remote issue, and
confirmed the five HANDOFF sections, terminal action, `CLOSED` issue, and
`APPROVED` review. Root `protocol/` remained unchanged at Git tree
`935cdb22f4472daa61b91d64f26f8893c4046fbf`.

## Findings and disposition

### Reusable-package defect

- **LOW — Established-repository README migration gap:** the quick start warns
  against overwriting conflicts but gives no standard merge or alternate-name
  procedure for the package/application `README.md` collision. This is tracked
  as `AEP-20260805T041340Z-readme-migration-gap`; no protocol source was changed.

### Target-specific limitations, not package defects

- **LOW — Regression sensitivity:** the five accepted tests use repeated string
  literals and never assert result-object identity. Incorrect identity-only and
  selective-aliasing mutants passed the suite, although the reviewed
  implementation passed direct identity/equality checks and 19,608 reference
  cases.
- **LOW — Historical evidence precision:** the implementor described an
  un-ranged/path-scoped diff check too broadly. The independent reviewer resolved
  target cleanliness with the exact parent-to-target commit range.
- **LOW — Participant lifecycle recording:** the reviewer used two child review
  tasks but did not record them in target HANDOFF and instead claimed no
  background work. Both children completed before the reviewer, their reports
  were incorporated, and the coordinator reconciled their durable references in
  root HANDOFF; no task is orphaned or non-terminal. The reusable BOOTSTRAP
  already states the required lifecycle rule, so this is participant
  noncompliance rather than a demonstrated package defect.

These limitations demonstrate the protocol's independent-review value. They do
not contradict current target correctness and do not require further product
work under the accepted pilot scope.

### Result

The pilot completed successfully with independent disposition `APPROVED`. No
material protocol or target defect was observed within this repository and
scope. The result does not establish universal portability; the single LOW
README migration issue remains open for a separately authorized protocol
evolution proposal.

## Limitations

- A single small Python 3.9 fixture cannot establish universal portability.
- Local Git and collaboration-task metadata cannot authenticate participant or
  human identity cryptographically.
- The target path is an additional inspection aid; this root record must remain
  sufficient to understand the result if that sibling directory is absent.

## Migration follow-up review

### Reviewed state

- Parent checkpoint: `087c665e3eb50bfff56f74bb9b32c6280e0423ee`
- Migration implementation: `98fe67c8cf99f53157f3273cc1defdfb81c46773`
- Review-handoff HEAD: `a3cd51fd5285384f70a97c8790f96d4c2fbebd1c`
- Migration protocol tree: `68a0204766a90ec9d9cb4e8e39cb988f10708677`
- Review time: `2026-08-05T08:43:41Z`

The narrow README-only case remained valid: the recorded fresh and established
copies contained 10 and 11 files, the guide alias was byte-identical, and a
fence-aware check resolved 48 relative links with zero missing. The independent
review nevertheless returned `CHANGES_REQUIRED` because the general migration
instructions did not preserve the same safety outside that narrow fixture.

### Existing alias overwrite reproduction

Command, run from the repository root:

```sh
alias_case=$(mktemp -d /tmp/aep-alias-review.XXXXXX)
cp LICENSE "$alias_case/PROTOCOL_GUIDE.md"
shasum -a 256 "$alias_case/PROTOCOL_GUIDE.md"
cp protocol/README.md "$alias_case/PROTOCOL_GUIDE.md"
shasum -a 256 "$alias_case/PROTOCOL_GUIDE.md" protocol/README.md
```

Concise result: the destination changed from
`ef17493a3cdad8270fc4f697c691d10065accdec701149cdd0ef2d0a3c692ad9` to
`5ce51973d0ce619d1f4eaf383674cadc832052c5ea55ca1949ae385fc447bbe5`,
the source-guide hash. The documented `cp` therefore overwrote the existing
alias.

### Alias symlink overwrite reproduction

Command, run from the repository root:

```sh
symlink_case=$(mktemp -d /tmp/aep-alias-symlink-review.XXXXXX)
cp LICENSE "$symlink_case/application-guide.md"
ln -s application-guide.md "$symlink_case/PROTOCOL_GUIDE.md"
shasum -a 256 "$symlink_case/application-guide.md"
cp protocol/README.md "$symlink_case/PROTOCOL_GUIDE.md"
shasum -a 256 "$symlink_case/application-guide.md" protocol/README.md
```

Concise result: the symlink target changed from the same `ef17493a...` sentinel
hash to the source-guide hash `5ce51973...`. The command followed the destination
symlink and modified its target.

### Link-clean but incorrect mapping reproduction

Command, run from the repository root:

```sh
mapping_case=$(mktemp -d /tmp/aep-map-review.XXXXXX)
cp -R protocol/. "$mapping_case/"
mv "$mapping_case/BOOTSTRAP.md" "$mapping_case/AEP_BOOTSTRAP.md"
mv "$mapping_case/README.md" "$mapping_case/PROTOCOL_GUIDE.md"
cp BOOTSTRAP.md "$mapping_case/BOOTSTRAP.md"
shasum -a 256 \
  "$mapping_case/BOOTSTRAP.md" \
  "$mapping_case/AEP_BOOTSTRAP.md" \
  protocol/BOOTSTRAP.md
MAPPING_CASE="$mapping_case" python3 - <<'PY'
from pathlib import Path
import os
import re

root = Path(os.environ["MAPPING_CASE"])
links = 0
missing = []
for document in root.rglob("*.md"):
    in_fence = False
    marker = None
    for line in document.read_text().splitlines():
        fence = re.match(r"^\s*((?:\x60){3,}|~{3,})", line)
        if fence:
            marks = fence.group(1)
            if not in_fence:
                in_fence, marker = True, marks[0]
            elif marks[0] == marker:
                in_fence, marker = False, None
            continue
        if in_fence:
            continue
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", line):
            target = target.split("#", 1)[0]
            if not target or "://" in target:
                continue
            links += 1
            if not (document.parent / target).resolve().exists():
                missing.append(f"{document.relative_to(root)} -> {target}")
print(f"links={links} missing={len(missing)}")
raise SystemExit(bool(missing))
PY
```

A fence-aware relative-link procedure checked every unfenced Markdown link in
the fixture and reported `23` links with `0` missing. Despite that structural
pass, canonical `BOOTSTRAP.md` had root-governing hash `8fcfc3fe...`, while both
`AEP_BOOTSTRAP.md` and the intended reusable protocol had hash `359bb5e2...`.
The guide therefore linked to the wrong normative entry point. Link existence
alone cannot validate an alternate artifact mapping.

### Evidence limitations and process finding

- The earlier implementation entry reports a corrected aggregate suite but
  preserves no exact harness command, script, or complete output. Its individual
  claims were independently reimplemented, but the historical aggregate run and
  its preliminary failures are not reproducible from durable state. This is a
  participant evidence-recording failure against root HANDOFF's command-recording
  constraint, not a demonstrated package-content regression.
- `markdownlint` and `markdownlint-cli2` remained unavailable. Fence, link,
  whitespace, and newline checks are structural checks, not full CommonMark lint.
- Root governing `BOOTSTRAP.md` has no final newline in every audited revision.
  Its unchanged recorded hash proves that condition predates this migration; no
  repository-wide final-newline pass is claimed.
- Broader portability remains unverified.

### Review disposition

`CHANGES_REQUIRED`. Automatic migration must preflight the complete resolved
destination manifest, refuse existing or symlinked alias/core destinations
before any write, preserve human authority over normative-record mappings, and
prove canonical references—not merely existing links—before the issue can
return to review.
