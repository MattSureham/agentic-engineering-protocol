"""Read-only validation of the independent round-3 reviewer records."""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
TARGET = "4dda31e9945000b51e950f4ac01ec7f82ffb15bf"
RECOVERED = "b0ea36f51123d77d7d0293b8be5d65c4a6188b8f"
ISSUE = "ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md"
EVIDENCE = "EVIDENCE/EVIDENCE-20261009T015211Z-scope-attribution-review-round-3.md"
PREFIX = "EVIDENCE/scope-attribution-review-round-3/"
sys.path.insert(0, str(ROOT / "scripts"))
import run_pipeline as p


def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True).strip()


text = (ROOT / ISSUE).read_text()
review = p._tolerant_latest_review(text, ISSUE)
assert (review.target, review.disposition, review.material_findings, review.reviewer) == (
    TARGET, "CHANGES_REQUIRED", 3, "agent:Codex-scope-review-20261009")
assert p._metadata(text, ISSUE)["Status"] == "IMPLEMENTING"
old = git("show", RECOVERED + ":" + ISSUE)
rounds = old.split("## Independent review rounds\n", 1)[1].split("\n## Blocker", 1)[0]
assert rounds.strip() in text
handoff = (ROOT / "HANDOFF.md").read_text()
assert re.findall(r"^## (.+)$", handoff, re.M) == ["Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"]
next_action = handoff.split("## Next Action\n", 1)[1].split("\n## ", 1)[0].strip()
assert len(next_action.split("\n\n")) == 1 and all(x in next_action for x in ["R2", "R3", "R5"])
old_activity = git("show", RECOVERED + ":HANDOFF.md").split("## Recent Activity\n", 1)[1].lstrip()
assert handoff.rstrip().endswith(old_activity)
context = p._load_context(ROOT)
milestone = next(m for m in context.milestones if m.milestone_id == "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1")
state = context.states[milestone.milestone_id]
assert state == p._parse_state(git("show", TARGET + ":" + milestone.issue), milestone)
assert (state["state"], state["attempt"], state["target_revision"]) == ("IN_PROGRESS", 3, None)
assert (ROOT / milestone.issue).read_bytes() == subprocess.check_output(["git", "show", TARGET + ":" + milestone.issue])
assert len(p._parse_intervening_registry(context.issue_texts[milestone.milestone_id], milestone.issue)) == 2
changed = set(git("diff", "--name-only", RECOVERED).splitlines()) | set(git("ls-files", "--others", "--exclude-standard").splitlines())
assert all(n in {ISSUE, EVIDENCE, "HANDOFF.md", "HUMAN_CHECKPOINT.md"} or n.startswith(PREFIX) for n in changed), changed
links = 0
for name in sorted(changed):
    path = ROOT / name
    assert path.is_file() and not path.is_symlink(), name
    data = path.read_bytes()
    assert data.endswith(b"\n") and all(line.rstrip(b" \t") == line for line in data.splitlines()), name
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
        if "://" not in destination and not destination.startswith(("#", "mailto:")):
            assert (path.parent / destination.split("#", 1)[0]).resolve().exists(), (name, destination)
            links += 1
results = json.loads((ROOT / PREFIX / "results.json").read_text())
assert results["target"] == TARGET and len(results["checks"]) == 3
assert all(r["exit"] == 0 for r in results["checks"])
for group, size in [("round1_replays", 22), ("round2_replays", 20), ("hostile_variants", 15)]:
    assert len(results[group]) == size
    assert all(r["refusal_no_mutation"] for r in results[group] if r["actual"] == "REFUSED")
    assert all(r["base_preserved"] for r in results[group])
    if group != "hostile_variants":
        assert all(r["requirement_met"] for r in results[group])
assert sum(not r["requirement_met"] for r in results["hostile_variants"]) == 9
real = results["real_case"]
assert len(real["paths"]) == 6 and not real["uncovered"]
assert sorted(map(len, real["entry_removal_uncovered"].values())) == [1, 5]
assert real["unchanged_contract"] and real["unchanged_machine_state"] and real["all_parent_oracle_agrees"]
assert not real["hypothetical_AGENTS_supported_by_existing_entries"]
for revision in ["6e39cea", "4f5e387", "9000bb3", "0cb370f", "47a0cb4", "79063cb"]:
    subprocess.run(["git", "merge-base", "--is-ancestor", revision, TARGET], check=True)
for name in ["_commit_paths", "_verify_target_scope", "_parse_intervening_registry"]:
    bodies = []
    for revision in ["4f5e387", TARGET]:
        tree = ast.parse(git("show", revision + ":scripts/run_pipeline.py"))
        bodies.append(ast.dump(next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)))
    assert bodies[0] == bodies[1], name
print("PASS review: 4dda31e CHANGES_REQUIRED material=3 issue=IMPLEMENTING; both prior rounds preserved")
print("PASS HANDOFF: five sections, one bounded Next Action, authored activity preserved")
print("PASS reviewer-only changes; local links=" + str(links) + "; regular files/fences/newlines/whitespace")
print("PASS discovery: issue bytes/state unchanged; IN_PROGRESS attempt=3 target=null registry_entries=2")
print("PASS evidence: prior 42 conform; 15 new variants reproduce 9 unsafe advances; refusals no mutation")
print("PASS real A/B: six paths covered, removal loses five/one; contract/base/history unchanged")
print("PASS R1/R4 function ASTs unchanged from 4f5e387; immutable history remains append-only")
