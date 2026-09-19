# Discovery Authority Validation — Not Activation Evidence

## Metadata

- **ID:** `EVIDENCE-20260918T065750Z-discovery-authority-validation`
- **Captured UTC:** `2026-09-18T06:57:50Z`; subsequent reruns/publication observations appended below
- **Recorded by:** `agent:Codex-discovery-authority`
- **Baseline:** `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b`
- **Scope:** Owner-authorized specification/ADR/issue/continuity records only
- **Related issue:** [Discovery](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Environment:** Darwin arm64, Python 3.9.6
- **Limitation:** Self-verification of authority recording, not implementation review or real activation conformance

## Commands and observed results

| Command/procedure | Observed result | Limitation |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | Exit 0; `Ran 97 tests in 25.402s` / `OK` | Existing deterministic suite; no real participant launched |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py` | Exit 0; `PASS structural protocol validation (package_files=10 handoffs=2)` | Supported structural rules only |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_pipeline.py status --json` | Exit 0; six entries; first four ACCEPTED, discovery and demonstration AUTHORIZED | Read-only; no lifecycle gate invoked |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json` | Exit 0; discovery selected; role implementer; emitted READY command not executed | Dispatcher host_adapter remains its existing manual value; runtime unchanged |
| Root/package Markdown pass through existing checker, containment root = repository | Exit 0; 57 Markdown files, zero findings before this validation record was added | Relative file/directory targets checked; external URLs and fragments are skipped by the checker, not claimed validated |
| `git diff --check` | Exit 0; no output | Whitespace only |
| `command -v markdownlint markdownlint-cli2 pymarkdown` | No executable found | Dedicated Markdown linter NOT RUN; do not equate the structural check with full CommonMark conformance |
| Fresh supported-host task-only activation, migration behavior and independent review | NOT RUN | Belong to the next implementation/review phase; no supported profile or completion claim |

## Reproducible authority/scope audit

Run from the repository root with bytecode writes disabled. This is a read-only evidence procedure, not new product tooling or a lifecycle transition. It checks exact contract and state preservation, protected bytes, relative links/Markdown, HANDOFF, isolated package copy readiness, deterministic dispatch and absence of file mutation. It uses the existing checker/parser rather than redefining them. External URLs and Markdown fragments are not checked.

Execute the first Python block below, for example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
path = Path("EVIDENCE/EVIDENCE-20260918T065750Z-discovery-authority-validation.md")
source = path.read_text(encoding="utf-8").split("\x60\x60\x60python\n", 1)[1].split("\x60\x60\x60", 1)[0]
exec(compile(source, str(path), "exec"))
PY
```

```python
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

root = Path.cwd().resolve()
sys.path.insert(0, str(root / "scripts"))
import run_pipeline as pipeline
import validate_protocol as validator

base = "58fa281ee6cb93abc2fea81dd46f8ddef2d8612b"
new_id = "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1"
new_issue = "ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md"
demo_id = "MILESTONE-20260817T021218Z-autonomy-demonstration-v1"
demo_issue = "ISSUES/ISSUE-20260817T021218Z-autonomy-demonstration.md"
allowed = {
    "PROJECT_SPEC.md", "README.md", "HANDOFF.md", "HUMAN_CHECKPOINT.md",
    new_issue, demo_issue,
    "ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md",
    "EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md",
    "EVIDENCE/EVIDENCE-20260918T065750Z-discovery-authority-validation.md",
}
def git(*args):
    return subprocess.check_output(["git", *args], cwd=root)
def original(name):
    return git("show", base + ":" + name)
def tracked_and_new():
    data = git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return sorted(set(data.decode().strip("\0").split("\0")))
def snapshot():
    return {n: hashlib.sha256((root / n).read_bytes()).hexdigest()
            for n in tracked_and_new() if n}

before = snapshot()
old = pipeline._parse_contract_text(original("PROJECT_SPEC.md").decode(), "PROJECT_SPEC.md")
context = pipeline._load_context(root)
current = context.milestones
assert len(old) == 5 and len(current) == 6
assert [m.raw for m in current[:4]] == [m.raw for m in old[:4]]
assert [m.digest for m in current[:4]] == [m.digest for m in old[:4]]
assert all(context.states[m.milestone_id]["state"] == "ACCEPTED" for m in current[:4])
assert current[4].milestone_id == new_id and current[4].raw["order"] == 5
expected_demo = dict(old[4].raw, order=6)
assert current[5].raw == expected_demo
assert current[5].milestone_id == demo_id
old_state = pipeline._parse_state(original(demo_issue).decode(), old[4])
expected_state = dict(old_state, authority_digest=current[5].digest)
assert context.states[demo_id] == expected_state
state = context.states[new_id]
assert state["state"] == "AUTHORIZED" and state["attempt"] == 0
assert all(state[k] is None for k in ("implementor", "base_revision", "target_revision"))
assert state["verification_evidence"] == state["review_references"] == []
assert len(state["events"]) == 1 and state["events"][0]["from"] is None
assert state["events"][0]["actor"] == "human:MattSureham"
assert pipeline._selected(context) == new_id
print("PASS six contracts; four accepted entries/digests unchanged; demonstration order-only/state-digest-only migration")
for m in current:
    print(m.raw["order"], m.milestone_id, m.digest)

changed = set(git("diff", "--name-only", base).decode().splitlines())
changed.update(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
assert changed == allowed, sorted(changed ^ allowed)
base_files = git("ls-tree", "-r", "--name-only", base).decode().splitlines()
for name in base_files:
    if name not in allowed:
        assert (root / name).read_bytes() == original(name), name
assert not (root / "AGENTS.md").exists() and not (root / "CLAUDE.md").exists()
print("PASS exact nine record paths; all other baseline bytes protected; no entry shim created")

spec = (root / "PROJECT_SPEC.md").read_text()
assert re.findall(r"^- \*\*(DISCOVERY-\d+) ", spec, re.M) == [
    "DISCOVERY-{:03d}".format(n) for n in range(1, 7)]
policy = lambda text: text.split("## Specification evolution\n", 1)[1].split("## Specification change record", 1)[0]
assert policy(spec) == policy(original("PROJECT_SPEC.md").decode())
old_log = original("PROJECT_SPEC.md").decode().split("## Specification change record", 1)[1].strip()
assert old_log in spec
assert "实现下一个已经授权的任务。" in spec
print("PASS six stable discovery IDs; specification-evolution policy and prior change rows preserved")

findings = []
names = tracked_and_new()
for name in names:
    if name.endswith(".md"):
        findings.extend(validator._validate_markdown_file(root, root, root / name))
assert not findings, "\n".join(f.render() for f in findings)
assert not validator.validate_repository(root)
handoff = (root / "HANDOFF.md").read_text()
recent = lambda text: text.split("## Recent Activity\n", 1)[1].split("## Archived Summary", 1)[0].strip()
assert recent(original("HANDOFF.md").decode()) in recent(handoff)
sections = re.findall(r"^## (.+)$", handoff, re.M)
assert sections == list(validator.EXPECTED_HANDOFF_SECTIONS)
active = handoff.split("## Active Issues\n", 1)[1].split("## Next Action", 1)[0]
rows = [line for line in active.splitlines() if line.startswith("| [")]
assert len(rows) == 6 and all("CLOSED" not in row for row in rows)
assert sum("BLOCKED" in row for row in rows) == 4
action = handoff.split("## Next Action\n", 1)[1].split("## Recent Activity", 1)[0].strip()
assert action and len(action.split("\n\n")) == 1
assert len(re.findall(r"^### ", recent(handoff), re.M)) >= 10
assert handoff.split("## Archived Summary", 1)[1].strip()
print("PASS Markdown/relative paths", len([n for n in names if n.endswith(".md")]),
      "; five HANDOFF sections; six unresolved rows; one action; prior authored activity intact")

with tempfile.TemporaryDirectory(prefix="aep-discovery-authority-") as temporary:
    isolated = Path(temporary)
    shutil.copytree(root / "protocol", isolated / "protocol")
    shutil.copy2(root / "HANDOFF.md", isolated / "HANDOFF.md")
    assert not validator.validate_repository(isolated)
    for name in validator.EXPECTED_PROTOCOL_FILES:
        assert (root / "protocol" / name).read_bytes() == (isolated / "protocol" / name).read_bytes()
print("PASS isolated ten-file package copy; bytes unchanged; zero symlinks through manifest check")

env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
command = [sys.executable, "scripts/run_dispatch.py", "--json"]
first = subprocess.check_output(command, cwd=root, env=env)
second = subprocess.check_output(command, cwd=root, env=env)
assert first == second
decision = json.loads(first)
assert decision["selected_milestone"] == new_id
assert decision["state"] == "AUTHORIZED" and decision["role"] == "implementer"
assert decision["expected_commands"][0][-1] == "READY"
assert snapshot() == before
subprocess.run(["git", "diff", "--check"], cwd=root, check=True)
print("PASS byte-identical dispatch; no tracked/untracked file-content mutation; diff whitespace")
print("PASS authority audit; no live activation, transition, independent review or acceptance performed")
```

## Audit execution and immutable authority boundary

The procedure above is preserved before execution. Results and exact authority commit will be appended after the checks actually run; no PASS is claimed here in advance.

### Resumed execution — 2026-09-19T21:37:43Z

Recorded by `agent:Codex-discovery-finalize` from current Git and artifacts, not prior conversational assumptions. The preceding pending-execution statement is preserved as historical. No implementation or milestone transition was run.

| Check | Observed result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | Exit `0`; `Ran 97 tests in 23.916s`; `OK` |
| Execute the Python audit block above using the reproduction command | Exit `0`; all seven PASS summaries; six contracts parsed and four accepted entries/digests unchanged |
| Discovery and demonstration projections | Discovery order 5, AUTHORIZED attempt 0, empty implementor/base/target/review/evidence fields; demonstration order 6 and digest-only state amendment, original events unchanged |
| Scope and authority preservation | Exactly nine intended record paths; every other baseline file byte-identical, including both BOOTSTRAP files, prior accepted ADRs, executable tooling/tests, role contracts, registry/ledger, other issue/evidence records and ten-file reusable package; no AGENTS.md/CLAUDE.md created |
| Record structure and relative paths | 58 Markdown documents pass the existing supported checker; five HANDOFF sections, one action, six unresolved rows/four blocked deferrals, nonempty archive, all prior authored activity preserved |
| Isolated copy and read-only behavior | Ten-file package copy validates with identical bytes/zero symlinks; repeated dispatcher output byte-identical; no tracked/untracked file-content mutation from audit |
| Git/remote orientation | Normal fetch succeeded; local HEAD, cached `origin/main` and direct `refs/heads/main` all `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b`; expected HTTPS origin retained |
| Environment and whitespace | Darwin arm64; Python 3.9.6; `git diff --check` exit `0`; dedicated `markdownlint`, `markdownlint-cli2`, `pymarkdown` unavailable |

The current parser and dispatcher select `MILESTONE-20260918T064510Z-prompt-independent-discovery-v1`, state `AUTHORIZED`, role `implementer`, with READY as the next expected transition. This is observed output, not an executed action. HANDOFF exposes that action only for the next participant after publication verification; this participant stops at the owner/specification boundary.

After finalization record updates, the same full-suite command passed again (`Ran 97 tests in 23.948s`, `OK`, exit `0`). The persisted audit, direct structural validator, read-only pipeline status/dispatcher and `git diff --check` also passed again. Final diff inspection confirms only the nine recorded paths; a bounded scan for private-key headers and GitHub/AWS/OpenAI-style credential patterns found no matches (not exhaustive secret detection). The pre-discovery HANDOFF digest was independently reproduced from baseline Git as `14df0acd0879099cda5fca2490516f57f2d5cfdf9424cdf94bfbbd5424220a7b`.

The immutable authority record is the containing commit titled `docs: authorize prompt-independent discovery`, directly after baseline `58fa281ee6cb93abc2fea81dd46f8ddef2d8612b`. Recover its full SHA from `git log --format=fuller` and inspect its exact nine-path diff against that parent; a commit cannot embed its own SHA. This record is prepared before committing, so it does not claim a future push succeeded. Publication requires a fresh no-divergence fetch, normal non-force push to `origin/main`, then equality of `git rev-parse HEAD`, `git rev-parse origin/main` and `git ls-remote origin refs/heads/main`, plus an empty `git status --porcelain=v1 --untracked-files=all`. The final response reports those observed results without introducing a follow-up implementation cycle.

## Residual uncertainty and exclusions

- Actual fresh-session conformance and implementation remain NOT RUN/not started. No independent-review disposition or milestone acceptance is recorded by this participant.
- Existing tests/probes do not prove automatic entry or AUTONOMY-004.
- Dedicated Markdown linting is unavailable. The supported structural/link subset is not full CommonMark or external-link availability validation.
- The original real-use incident remains owner-reported without an independently reproducible external trace.
