# Post-Pilot Repository Audit

## Metadata

- **ID:** `EVIDENCE-20260806T013907Z-post-pilot-audit`
- **Title:** Repository-derived hardening findings and pilot portability audit
- **Captured UTC:** `2026-08-06T01:39:07Z`
- **Recorded by:** `Codex/root`
- **Claim supported or challenged:** Root governance is internally inconsistent, live HANDOFF is overloaded, and the pilot cannot be reproduced from this repository alone.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md); approved post-pilot hardening requirements
- **Related ADRs/issues:** [`ADR-20260806T013907Z-root-protocol-adoption`](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md); [`ISSUE-20260806T013907Z-post-pilot-hardening`](../ISSUES/ISSUE-20260806T013907Z-post-pilot-hardening.md)
- **Repository revision/state:** Clean synchronized baseline `e6beeb2cb730183ca2ac13795ad367ad9d9e1099` before the first HANDOFF edit
- **Environment:** Darwin host; Git and POSIX shell available; dedicated `markdownlint`, `markdownlint-cli2`, and `shellcheck` unavailable

## Method

- **Procedure:** Read root and reusable governance/specification/HANDOFF artifacts completely; inspect repository and remote state; compare role statements; inventory HANDOFF content; query recorded pilot commits in the root Git object database and the local sibling pilot repository.
- **Exact command/input:** `git status --short --branch`; `git rev-parse HEAD origin/main`; `git remote -v`; `git cat-file -e <commit>^{commit}`; `git -C ../aep-protocol-pilot status --short --branch`; `git -C ../aep-protocol-pilot remote -v`; `shasum -a 256 ...`; `wc -l ...`; `rg`/`sed` direct reads.
- **Exit status:** Baseline Git/status/hash reads `0`; both original pilot commit lookups `128`; published migration commit lookup `0`; sibling status/remote queries `0` with no remote output.
- **Repeatability:** Run the listed commands in a clone of this revision. The sibling-path observation is local-environment evidence and is intentionally not clone-reproducible.

## Raw observation

```text
## main...origin/main
e6beeb2cb730183ca2ac13795ad367ad9d9e1099
e6beeb2cb730183ca2ac13795ad367ad9d9e1099
origin https://github.com/MattSureham/agentic-engineering-protocol.git

git cat-file -e 3a8f3922f47dec16144493482bd2b7a150ef5b0a^{commit}: exit 128
git cat-file -e 0606979a57d821e3777d1b81e0834512d9a184d0^{commit}: exit 128
git cat-file -e f70a8ace435dd32a00f81390f82184b963bb0c0b^{commit}: exit 0

../aep-protocol-pilot status: ## main
../aep-protocol-pilot remotes: no output

BOOTSTRAP.md: 8fcfc3fe52608a1b42305bb12696d3f151be468bbbf638918cf93b651414dfe6
PROJECT_SPEC.md: 13169319e2be028c470ca96925002b25c000c58ba3a4c5420e652d291df139dd
pre-edit HANDOFF.md: e42e9605653c568e737fe371dd54db48f1c2eab49111be6370f53205ecefbe63
PILOT_EVIDENCE.md: dab1274cb74d62ec263fdb0acb86591d74f3d79efd4891e2140c08f9e314651f
protocol/PROJECT_SPEC.md: 6c7401d9ed598908225f3eb6a3bb8299cfa01a350b1853df98c7bc386eddf976

pre-edit HANDOFF.md: 764 lines
PILOT_EVIDENCE.md: 757 lines
protocol inventory: 10 regular files, no symlinks
```

Direct document observations:

- Root `BOOTSTRAP.md` says HANDOFF is the canonical project truth and that undifferentiated repository evidence always takes precedence.
- Root `README.md` calls HANDOFF canonical live development state and tells participants to read it before `PROJECT_SPEC.md`.
- Root HANDOFF itself and reusable `protocol/BOOTSTRAP.md` place HANDOFF below requirements, accepted ADRs, tests/contracts, and evidence.
- Root HANDOFF contains five closed issue bodies, eleven terminal background-task bodies, large verification narratives, 33 activity entries, and an empty archive.
- Pilot evidence names `/Users/matthew/Projects/aep-protocol-pilot` and several `/tmp` or `/var/folders` paths. The original implementation/review commits are not root Git objects.

## Interpretation

- **CONFIRMED:** Root source descriptions assign incompatible authority to HANDOFF; this is a real governance inconsistency rather than a missing-review assertion.
- **CONFIRMED:** The live HANDOFF is serving as issue database, evidence archive, terminal task ledger, and diary in addition to operational continuity.
- **CONFIRMED:** A fresh clone of this repository cannot inspect the recorded original pilot commits or rerun its five tests because those objects/files are not contained here and no durable pilot remote is recorded.
- **CONFIRMED:** Root Git history does preserve the root-side pilot narrative and later migration tests; those remain evidence of what participants recorded, not a self-contained reproduction of the original pilot repository.
- **INFERRED:** A content-addressed pilot bundle or durable remote could make the original target reproducible, but either requires separately approved scope.
- **UNKNOWN:** Whether the protocol is portable across untested operating systems, filesystems, repository shapes, or concurrent writers. Production-grade or universal validation is not established.

## Limitations and residual uncertainty

- Repository-recorded participant/owner identities are not cryptographically authenticated.
- The local sibling happened to exist during this audit, but that does not make it durable or available to a remote-only participant.
- Temporary fixture paths may no longer exist and must not be used as durable proof.
- No dedicated Markdown linter was installed; its absence is not a pass.
- This evidence does not independently review the hardening implementation, which did not yet exist at capture time.

## Integrity and provenance

- **Artifact location:** `EVIDENCE/EVIDENCE-20260806T013907Z-post-pilot-audit.md`
- **Artifact digest:** To be recorded after the authority-boundary commit; pre-hardening source digests are listed above.
- **External retention risk:** Local sibling and temporary paths are non-durable; GitHub root remote is durable only for objects actually pushed to it.
- **Supersedes / superseded by:** `NONE`

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `NONE` | `NONE` | `NONE` | `NONE` |
