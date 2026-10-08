"""Read-only checks for the round-2 review records, not implementation fixes."""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
TARGET = "4f5e38744340fb7597222bf31483eb67187e2bbf"
RECOVERED = "50e5994960c760457cb0f17e5bbe01a923694fd9"
ISSUE = "ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md"
EVIDENCE = "EVIDENCE/EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md"
PREFIX = "EVIDENCE/scope-attribution-review-round-2/"
sys.path.insert(0, str(ROOT / "scripts"))
import run_pipeline as p


def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True).strip()


text = (ROOT / ISSUE).read_text()
review = p._parse_latest_review(text, ISSUE)
assert (review.target, review.material_findings, review.disposition, review.reviewer) == (
    TARGET, 3, "CHANGES_REQUIRED", "agent:Codex-scope-review-20261008")
assert p._metadata(text, ISSUE)["Status"] == "IMPLEMENTING"
old = git("show", RECOVERED + ":" + ISSUE)
old_round = old.split("### 2026-09-30T01:59:49Z — agent:Codex-scope-review-20260930\n", 1)[1].split("\n## Blocker", 1)[0]
assert old_round.strip() in text
handoff = (ROOT / "HANDOFF.md").read_text()
assert re.findall(r"^## (.+)$", handoff, re.M) == ["Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"]
next_action = handoff.split("## Next Action\n", 1)[1].split("\n## ", 1)[0].strip()
assert len(next_action.split("\n\n")) == 1 and "R2" in next_action and "R3" in next_action and "R5" in next_action
history = git("show", RECOVERED + ":HANDOFF.md").split("## Recent Activity\n", 1)[1].lstrip()
assert handoff.rstrip().endswith(history)
context = p._load_context(ROOT)
milestone = next(m for m in context.milestones if m.milestone_id == "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1")
state = context.states[milestone.milestone_id]
assert state == p._parse_state(git("show", TARGET + ":" + milestone.issue), milestone)
assert (state["state"], state["attempt"], state["target_revision"]) == ("IN_PROGRESS", 3, None)
assert len(p._parse_intervening_registry(context.issue_texts[milestone.milestone_id], milestone.issue)) == 2
assert (ROOT / milestone.issue).read_bytes() == subprocess.check_output(["git", "show", TARGET + ":" + milestone.issue])
changed = set(git("diff", "--name-only", RECOVERED).splitlines())
new = set(git("ls-files", "--others", "--exclude-standard").splitlines())
allowed = {"HANDOFF.md", "HUMAN_CHECKPOINT.md", ISSUE, EVIDENCE}
assert all(name in allowed or name.startswith(PREFIX) for name in changed | new), changed | new
links = 0
for name in sorted(changed | new):
    path = ROOT / name
    assert path.is_file() and not path.is_symlink(), name
    data = path.read_bytes()
    assert data.endswith(b"\n"), name
    assert not any(line.rstrip(b" \t") != line for line in data.splitlines()), name
    if path.suffix != ".md":
        continue
    body = data.decode()
    fence = None
    for line in body.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            mark, tail = match.groups()
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence) and not tail.strip():
                fence = None
    assert fence is None, name
    for destination in re.findall(r"\]\(([^)]+)\)", body):
        if "://" in destination or destination.startswith(("mailto:", "#")):
            continue
        assert (path.parent / destination.split("#", 1)[0]).resolve().exists(), (name, destination)
        links += 1
results = json.loads((ROOT / PREFIX / "results.json").read_text())
assert results["target"] == TARGET
assert all(row["exit"] == 0 for row in results["checks"]) and len(results["checks"]) == 3
assert len(results["baseline_replays"]) == 22 and sum(not r["requirement_met"] for r in results["baseline_replays"]) == 11
assert len(results["v2_replays"]) == 22 and all(r["requirement_met"] for r in results["v2_replays"])
assert len(results["new_cases"]) == 20
assert sum(not r["requirement_met"] for r in results["new_cases"]) == 11
for group in ("baseline_replays", "v2_replays", "new_cases"):
    assert all(r["refusal_no_mutation"] for r in results[group] if r["actual"] == "REFUSED")
    assert all(r["base_preserved"] for r in results[group])
real = results["real_case"]
assert len(real["paths"]) == 6 and not real["uncovered"] and real["all_parent_oracle_agrees"]
assert sorted(map(len, real["entry_removal_uncovered"].values())) == [1, 5]
assert not real["hypothetical_AGENTS_supported_by_existing_entries"]
assert real["unchanged_contract"] and real["unchanged_machine_state"]
for revision in ["6e39cea8ac46d909709ddaeeda1aa8d2df59ce08", "9000bb3d08eed6a64c8a16d136b9ada0a2c5469e", "47a0cb40684ad8edc1d574eba28ded610ea2ba93", "79063cb2201517567c3a8fe9702fd59ca41e9e5d"]:
    subprocess.run(["git", "merge-base", "--is-ancestor", revision, TARGET], check=True)
print("PASS review: target=4f5e387 CHANGES_REQUIRED material=3 issue=IMPLEMENTING; round 1 unchanged")
print("PASS HANDOFF: five ordered sections, one bounded Next Action; authored history preserved")
print("PASS discovery: IN_PROGRESS attempt=3 target=null; issue bytes/state/registry unchanged; entries=2")
print("PASS reviewer-only diff; regular files; local links=" + str(links) + "; fences/newlines/trailing whitespace")
print("PASS evidence: baseline 22/11 unsafe; v2 replays 22/0 unsafe; new variants 20/11 unsafe; refusals no mutation")
print("PASS real case: six paths covered; A/B removal loses five/one; original contract/state/history preserved")
