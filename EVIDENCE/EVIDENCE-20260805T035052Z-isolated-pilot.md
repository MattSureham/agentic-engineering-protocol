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

## Corrected migration validation

### Candidate state

- Validation time: `2026-08-05T08:52:54Z`
- Parent review-record commit:
  `8d753ede59d75eaf6891425bcf2ce77021b94288` (`docs: record migration review
  findings`)
- Candidate `protocol/README.md` SHA-256:
  `a110604698c2fb1f2f3dc1013cf4d7cdf6d48f8bb6064bde9e4cd32914620180`
- Candidate `protocol/BOOTSTRAP.md` SHA-256:
  `d87b814fdeb66dcc9754248270203817c213550f4b87c4405fc914163603e11b`

The following exact shell procedure exercised quoted source and target paths,
the two automatic copy paths, the five refusal cases, byte preservation, the
10/11-file inventories, symlink absence in successful copies, and fence-aware
relative links. It intentionally retains its temporary directory for inspection.

```sh
set -eu

validation_root=$(mktemp -d "/tmp/aep migration validation.XXXXXX")
source_parent="$validation_root/source with spaces"
protocol_source="$source_parent/protocol"
fresh_target="$validation_root/fresh target"
established_target="$validation_root/established target"
mkdir -p "$source_parent" "$fresh_target" "$established_target"
cp -R protocol "$protocol_source"

preflight_fresh() {
  validation_source=$1
  validation_target=$2
  [ -d "$validation_source" ] && [ -d "$validation_target" ] || return 1
  for relative_path in \
    README.md PROTOCOL_GUIDE.md BOOTSTRAP.md PROJECT_SPEC.md HANDOFF.md \
    HUMAN_CHECKPOINT.md PROMPTS.md EXAMPLE.md ADR EVIDENCE ISSUES
  do
    if [ -e "$validation_target/$relative_path" ] || [ -L "$validation_target/$relative_path" ]; then
      return 1
    fi
  done
}

preflight_established() {
  validation_source=$1
  validation_target=$2
  [ -d "$validation_source" ] && [ -d "$validation_target" ] || return 1
  [ -f "$validation_target/README.md" ] && [ ! -L "$validation_target/README.md" ] || return 1
  for relative_path in \
    PROTOCOL_GUIDE.md BOOTSTRAP.md PROJECT_SPEC.md HANDOFF.md \
    HUMAN_CHECKPOINT.md PROMPTS.md EXAMPLE.md ADR EVIDENCE ISSUES
  do
    if [ -e "$validation_target/$relative_path" ] || [ -L "$validation_target/$relative_path" ]; then
      return 1
    fi
  done
}

preflight_fresh "$protocol_source" "$fresh_target"
cp -R "$protocol_source/." "$fresh_target/"

cp LICENSE "$established_target/README.md"
app_readme_before=$(shasum -a 256 "$established_target/README.md" | awk '{print $1}')
preflight_established "$protocol_source" "$established_target"
cp \
  "$protocol_source/BOOTSTRAP.md" \
  "$protocol_source/PROJECT_SPEC.md" \
  "$protocol_source/HANDOFF.md" \
  "$protocol_source/HUMAN_CHECKPOINT.md" \
  "$protocol_source/PROMPTS.md" \
  "$protocol_source/EXAMPLE.md" \
  "$established_target/"
cp -R \
  "$protocol_source/ADR" \
  "$protocol_source/EVIDENCE" \
  "$protocol_source/ISSUES" \
  "$established_target/"
cp "$protocol_source/README.md" "$established_target/PROTOCOL_GUIDE.md"
cmp "$protocol_source/BOOTSTRAP.md" "$established_target/BOOTSTRAP.md"
cmp "$protocol_source/README.md" "$established_target/PROTOCOL_GUIDE.md"
app_readme_after=$(shasum -a 256 "$established_target/README.md" | awk '{print $1}')
test "$app_readme_before" = "$app_readme_after"

regular_alias="$validation_root/regular alias collision"
mkdir "$regular_alias"
cp LICENSE "$regular_alias/README.md"
cp LICENSE "$regular_alias/PROTOCOL_GUIDE.md"
regular_before=$(shasum -a 256 "$regular_alias/PROTOCOL_GUIDE.md" | awk '{print $1}')
if preflight_established "$protocol_source" "$regular_alias"; then exit 20; fi
regular_after=$(shasum -a 256 "$regular_alias/PROTOCOL_GUIDE.md" | awk '{print $1}')
test "$regular_before" = "$regular_after"
test "$(find "$regular_alias" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" = "2"

symlink_alias="$validation_root/symlink alias collision"
mkdir "$symlink_alias"
cp LICENSE "$symlink_alias/README.md"
cp LICENSE "$symlink_alias/application-guide.md"
ln -s application-guide.md "$symlink_alias/PROTOCOL_GUIDE.md"
symlink_before=$(shasum -a 256 "$symlink_alias/application-guide.md" | awk '{print $1}')
if preflight_established "$protocol_source" "$symlink_alias"; then exit 21; fi
symlink_after=$(shasum -a 256 "$symlink_alias/application-guide.md" | awk '{print $1}')
test "$symlink_before" = "$symlink_after"
test -L "$symlink_alias/PROTOCOL_GUIDE.md"
test "$(find "$symlink_alias" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" = "3"

core_collision="$validation_root/core collision"
mkdir "$core_collision"
cp LICENSE "$core_collision/README.md"
cp BOOTSTRAP.md "$core_collision/BOOTSTRAP.md"
core_before=$(shasum -a 256 "$core_collision/BOOTSTRAP.md" | awk '{print $1}')
if preflight_established "$protocol_source" "$core_collision"; then exit 22; fi
core_after=$(shasum -a 256 "$core_collision/BOOTSTRAP.md" | awk '{print $1}')
test "$core_before" = "$core_after"
test "$(find "$core_collision" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" = "2"

nested_collision="$validation_root/nested collision"
mkdir "$nested_collision"
cp LICENSE "$nested_collision/README.md"
mkdir "$nested_collision/ADR"
cp LICENSE "$nested_collision/ADR/TEMPLATE.md"
nested_before=$(shasum -a 256 "$nested_collision/ADR/TEMPLATE.md" | awk '{print $1}')
if preflight_established "$protocol_source" "$nested_collision"; then exit 23; fi
nested_after=$(shasum -a 256 "$nested_collision/ADR/TEMPLATE.md" | awk '{print $1}')
test "$nested_before" = "$nested_after"
test "$(find "$nested_collision" -type f | wc -l | tr -d ' ')" = "2"

reserved_alias="$validation_root/reserved alias collision"
mkdir "$reserved_alias"
cp LICENSE "$reserved_alias/PROTOCOL_GUIDE.md"
if preflight_fresh "$protocol_source" "$reserved_alias"; then exit 24; fi
test "$(find "$reserved_alias" -type f | wc -l | tr -d ' ')" = "1"

VALIDATION_ROOT="$validation_root" \
PROTOCOL_SOURCE="$protocol_source" \
FRESH_TARGET="$fresh_target" \
ESTABLISHED_TARGET="$established_target" \
python3 - <<'PY'
from pathlib import Path
import os
import re
import sys

root = Path(os.environ["VALIDATION_ROOT"])
source = Path(os.environ["PROTOCOL_SOURCE"])
fresh = Path(os.environ["FRESH_TARGET"])
established = Path(os.environ["ESTABLISHED_TARGET"])
failures = []
expected = {
    "ADR/TEMPLATE.md", "BOOTSTRAP.md", "EVIDENCE/TEMPLATE.md", "EXAMPLE.md",
    "HANDOFF.md", "HUMAN_CHECKPOINT.md", "ISSUES/TEMPLATE.md",
    "PROJECT_SPEC.md", "PROMPTS.md", "README.md",
}

source_files = {str(path.relative_to(source)) for path in source.rglob("*") if path.is_file()}
fresh_files = {str(path.relative_to(fresh)) for path in fresh.rglob("*") if path.is_file()}
established_expected = (expected - {"README.md"}) | {"README.md", "PROTOCOL_GUIDE.md"}
established_files = {str(path.relative_to(established)) for path in established.rglob("*") if path.is_file()}
if source_files != expected: failures.append("source inventory")
if fresh_files != expected: failures.append("fresh inventory")
if established_files != established_expected: failures.append("established inventory")

for tree in (source, fresh, established):
    if any(path.is_symlink() for path in tree.rglob("*")):
        failures.append(f"unexpected symlink in {tree}")
for relative in expected:
    if (source / relative).read_bytes() != (fresh / relative).read_bytes():
        failures.append(f"fresh mismatch {relative}")
for relative in expected - {"README.md"}:
    if (source / relative).read_bytes() != (established / relative).read_bytes():
        failures.append(f"established mismatch {relative}")
if (source / "README.md").read_bytes() != (established / "PROTOCOL_GUIDE.md").read_bytes():
    failures.append("guide alias mismatch")

def unfenced(text):
    active = False
    marker = None
    for line in text.splitlines():
        fence = re.match(r"^\s*((?:\x60){3,}|~{3,})", line)
        if fence:
            marks = fence.group(1)
            if not active: active, marker = True, marks[0]
            elif marks[0] == marker: active, marker = False, None
            continue
        if not active: yield line
    if active: failures.append("unbalanced fence")

link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
counts = {}
for name, tree in (("fresh", fresh), ("established", established)):
    count = 0
    for document in tree.rglob("*.md"):
        for line in unfenced(document.read_text()):
            for target in link_pattern.findall(line):
                target = target.split("#", 1)[0]
                if not target or "://" in target: continue
                count += 1
                if not (document.parent / target).resolve().exists():
                    failures.append(f"missing link {document}: {target}")
    counts[name] = count
for target in ("BOOTSTRAP.md", "PROTOCOL_GUIDE.md"):
    if not (established / target).exists(): failures.append(f"missing navigation target {target}")

print(f"validation_root={root}")
print(f"inventories=source:{len(source_files)} fresh:{len(fresh_files)} established:{len(established_files)}")
print(f"links=fresh:{counts['fresh']} established:{counts['established'] + 2} missing:0")
print("collision_refusals=regular-alias,symlink-alias,canonical-core,nested-core,reserved-alias")
print(f"failures={len(failures)}")
sys.exit(bool(failures))
PY
```

Result: exit `0`.

```text
validation_root=/tmp/aep migration validation.bEqHIX
inventories=source:10 fresh:10 established:11
links=fresh:23 established:25 missing:0
collision_refusals=regular-alias,symlink-alias,canonical-core,nested-core,reserved-alias
failures=0
```

The first syntax-check harness used a fence extractor that failed to match
indented Markdown fences and therefore found zero shell blocks; that result was
discarded. The corrected exact command was:

```sh
python3 - <<'PY'
from pathlib import Path
import re
import subprocess
import sys

guide = Path("protocol/README.md").read_text()
tick = chr(96)
pattern = (
    r"^[ \t]*" + re.escape(tick * 3) + r"sh[ \t]*\n"
    r"(.*?)"
    r"^[ \t]*" + re.escape(tick * 3) + r"[ \t]*$"
)
blocks = re.findall(pattern, guide, re.M | re.S)
failures = []
for index, block in enumerate(blocks, 1):
    result = subprocess.run(["sh", "-n"], input=block, text=True, capture_output=True)
    if result.returncode:
        failures.append(f"block {index}: {result.stderr.strip()}")
print(f"shell_blocks={len(blocks)} syntax_failures={len(failures)}")
for failure in failures: print("FAIL", failure)
sys.exit(bool(failures) or len(blocks) != 3)
PY
```

Result: exit `0`, `shell_blocks=3 syntax_failures=0`.

### Candidate structural validation

The remaining candidate checks used these exact commands:

```sh
find protocol -type f -print | sort
find . -path ./.git -prune -o -type l -print
shasum -a 256 BOOTSTRAP.md PROJECT_SPEC.md protocol/README.md protocol/BOOTSTRAP.md
git diff --name-only 8d753ede59d75eaf6891425bcf2ce77021b94288
git diff --name-only 8d753ede59d75eaf6891425bcf2ce77021b94288 -- protocol
git diff --check 8d753ede59d75eaf6891425bcf2ce77021b94288
sed -n '9,19p' protocol/BOOTSTRAP.md
python3 - <<'PY'
from pathlib import Path
import re
import sys

root = Path(".")
paths = list((root / "protocol").rglob("*.md"))
paths += [root / "HANDOFF.md", root / "PILOT_EVIDENCE.md"]
failures = []
for path in paths:
    text = path.read_text()
    if not text.endswith("\n"):
        failures.append(f"missing final newline {path}")
    for number, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            failures.append(f"trailing whitespace {path}:{number}")
    if len(re.findall(r"^[ \t]*((?:\x60){3,}|~{3,})", text, re.M)) % 2:
        failures.append(f"unbalanced fences {path}")

handoff = (root / "HANDOFF.md").read_text()
sections = re.findall(
    r"^## (Current State|Active Issues|Next Action|Recent Activity|Archived Summary)$",
    handoff,
    re.M,
)
next_action = handoff.split("## Next Action\n", 1)[1].split("\n## Recent Activity", 1)[0].strip()
tick = chr(96)
nonterminal = any(
    "- **State:** " + tick + state + tick in handoff
    for state in ("QUEUED", "RUNNING")
)
if sections != ["Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"]:
    failures.append(f"HANDOFF sections {sections}")
if not next_action or "\n\n" in next_action:
    failures.append("HANDOFF Next Action")
if nonterminal:
    failures.append("nonterminal task remains")

print(f"markdown_files={len(paths)} handoff_sections={len(sections)} next_actions=1 nonterminal_tasks={int(nonterminal)}")
print(f"failures={len(failures)}")
for failure in failures:
    print("FAIL", failure)
sys.exit(bool(failures))
PY
```

Results: the package inventory was the exact 10 expected files; the symlink
scan and both `git diff --check` output streams were empty; the root governing
hashes remained `8fcfc3fe...` and `13169319...`; only `HANDOFF.md`,
`PILOT_EVIDENCE.md`, `protocol/BOOTSTRAP.md`, and `protocol/README.md` changed
from the review-record parent, and only the latter two changed under
`protocol/`. All seven precedence lines remained present in order. The Python
check exited `0`:

```text
markdown_files=12 handoff_sections=5 next_actions=1 nonterminal_tasks=0
failures=0
```

The dedicated Markdown linters remained unavailable and were not counted as
passed.

## Independent approval and coordinator closure

Fresh reviewer `/root/migration_final_review` reviewed exact target
`f70a8ace435dd32a00f81390f82184b963bb0c0b` against parent
`8d753ede59d75eaf6891425bcf2ce77021b94288` and committed its HANDOFF-only
record as `52044a2322c0f295739f6e694b67db18d6b7ee8e`. Disposition was `APPROVED`
with no material finding; all four findings from the first round were resolved.

The reviewer preserved one evidence correction: the earlier corrected harness
reported `25` established links by validating 23 installed links and two virtual
navigation targets. It did not perform the manual README append. The reviewer
then performed that real append independently and obtained 25 actual links with
zero missing while preserving the prior README bytes as a prefix.

At `2026-08-05T09:17:02Z`, the coordinator applied the exact documented
navigation block with `apply_patch` to retained fixture
`/tmp/aep migration validation.bEqHIX/established target/README.md`, then ran
these Git identity commands and the following closure checker:

```sh
git diff --name-only 52044a2322c0f295739f6e694b67db18d6b7ee8e^..52044a2322c0f295739f6e694b67db18d6b7ee8e
git rev-parse f70a8ace435dd32a00f81390f82184b963bb0c0b:protocol
git rev-parse 52044a2322c0f295739f6e694b67db18d6b7ee8e:protocol
git diff --check 8d753ede59d75eaf6891425bcf2ce77021b94288..f70a8ace435dd32a00f81390f82184b963bb0c0b
git diff --check df4f5eeb020d3db8ef02665707afcb5c082e0b33..52044a2322c0f295739f6e694b67db18d6b7ee8e
git ls-remote --heads origin refs/heads/main
python3 - <<'PY'
from pathlib import Path
import hashlib
import re
import sys

repo = Path(".")
target = Path("/tmp/aep migration validation.bEqHIX/established target")
failures = []
original = (repo / "LICENSE").read_bytes()
readme = (target / "README.md").read_bytes()
if not readme.startswith(original):
    failures.append("application README prefix")
if readme.count(b"](BOOTSTRAP.md)") != 1:
    failures.append("BOOTSTRAP navigation count")
if readme.count(b"](PROTOCOL_GUIDE.md)") != 1:
    failures.append("guide navigation count")

active = False
marker = None
links = 0
pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
for document in target.rglob("*.md"):
    for line in document.read_text().splitlines():
        fence = re.match(r"^\s*((?:\x60){3,}|~{3,})", line)
        if fence:
            marks = fence.group(1)
            if not active:
                active, marker = True, marks[0]
            elif marks[0] == marker:
                active, marker = False, None
            continue
        if active:
            continue
        for link in pattern.findall(line):
            link = link.split("#", 1)[0]
            if not link or "://" in link:
                continue
            links += 1
            if not (document.parent / link).resolve().exists():
                failures.append(f"missing link {document}: {link}")

expected_hashes = {
    "regular alias collision/PROTOCOL_GUIDE.md": "ef17493a3cdad8270fc4f697c691d10065accdec701149cdd0ef2d0a3c692ad9",
    "symlink alias collision/application-guide.md": "ef17493a3cdad8270fc4f697c691d10065accdec701149cdd0ef2d0a3c692ad9",
    "core collision/BOOTSTRAP.md": "8fcfc3fe52608a1b42305bb12696d3f151be468bbbf638918cf93b651414dfe6",
    "nested collision/ADR/TEMPLATE.md": "ef17493a3cdad8270fc4f697c691d10065accdec701149cdd0ef2d0a3c692ad9",
    "reserved alias collision/PROTOCOL_GUIDE.md": "ef17493a3cdad8270fc4f697c691d10065accdec701149cdd0ef2d0a3c692ad9",
}
fixture_root = target.parent
for relative, expected in expected_hashes.items():
    actual = hashlib.sha256((fixture_root / relative).read_bytes()).hexdigest()
    if actual != expected:
        failures.append(f"changed collision sentinel {relative}")

print(f"actual_established_inventory={sum(path.is_file() for path in target.rglob('*'))}")
print(f"actual_links={links} missing=0 prefix_preserved={readme.startswith(original)}")
print(f"collision_sentinels={len(expected_hashes)} unchanged")
print(f"failures={len(failures)}")
sys.exit(bool(failures))
PY
```

The review commit changed only `HANDOFF.md`; target and review protocol trees
both resolved to `f332761a54a3e8bf3f2bcbe5d231f1795e999377`; both ranged whitespace
checks exited `0`. The direct remote check still reported pre-publication
`origin/main` at `a3cd51fd5285384f70a97c8790f96d4c2fbebd1c`.

The corrected closure checker exited `0`:

```text
actual_established_inventory=11
actual_links=25 missing=0 prefix_preserved=True
collision_sentinels=5 unchanged
failures=0
```

One preliminary coordinator assertion assigned the LICENSE sentinel hash to the
intentional legacy `BOOTSTRAP.md` core-collision fixture; it failed without
changing any file. The corrected rerun used the fixture's recorded governing
BOOTSTRAP hash and produced the pass above. Dedicated Markdown/shell linters,
non-POSIX native environments, concurrent external mutation, broader repository
portability, and cryptographic participant identity remain outside the evidence.
