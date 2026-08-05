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
