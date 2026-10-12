"""Read-only assertions for independent round-4 records and immutable scope."""
import ast
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
TARGET = "d9bd6d806e0f1160df4b6893154017e9d287cc4e"
PARENT = "b80ccda21826073ae214f960877536c0e0348b98"
RECOVERED = "500df768721aa751d3826715429e9b56bf6dab39"
ISSUE = "ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md"
EVIDENCE = "EVIDENCE/EVIDENCE-20261012T015542Z-scope-attribution-review-round-4.md"
PREFIX = "EVIDENCE/scope-attribution-review-round-4/"
A = "ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md"
B = "ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md"
sys.path.insert(0, str(ROOT / "scripts"))
import run_pipeline as p


def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True).strip()


text = (ROOT / ISSUE).read_text()
review = p._tolerant_latest_review(text, ISSUE)
assert (review.target, review.disposition, review.material_findings, review.reviewer) == (
    TARGET, "CHANGES_REQUIRED", 3, "agent:Codex-scope-review-20261012")
assert p._metadata(text, ISSUE)["Status"] == "IMPLEMENTING"
old = git("show", RECOVERED + ":" + ISSUE)
rounds = old.split("\n## Independent review rounds\n", 1)[1].split("\n## Blocker", 1)[0]
assert rounds.strip() in text
handoff = (ROOT / "HANDOFF.md").read_text()
assert re.findall(r"^## (.+)$", handoff, re.M) == ["Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"]
next_action = handoff.split("## Next Action\n", 1)[1].split("\n## ", 1)[0].strip()
assert len(next_action.split("\n\n")) == 1 and all(x in next_action for x in ["R2", "R3", "R5"])
history = git("show", RECOVERED + ":HANDOFF.md").split("## Recent Activity\n", 1)[1].lstrip()
assert handoff.rstrip().endswith(history)
context = p._load_context(ROOT)
milestone = next(m for m in context.milestones if m.milestone_id == "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1")
state = context.states[milestone.milestone_id]
assert (state["state"], state["attempt"], state["target_revision"]) == ("IN_PROGRESS", 3, None)
for revision in (PARENT, TARGET, RECOVERED):
    assert (ROOT / milestone.issue).read_bytes() == subprocess.check_output(["git", "show", revision + ":" + milestone.issue])
    then_spec = git("show", revision + ":PROJECT_SPEC.md")
    assert p._extract_json_block(then_spec, p.CONTRACT_BEGIN, p.CONTRACT_END, "PROJECT_SPEC.md") == p._extract_json_block((ROOT / "PROJECT_SPEC.md").read_text(), p.CONTRACT_BEGIN, p.CONTRACT_END, "PROJECT_SPEC.md")
assert len(p._parse_intervening_registry(context.issue_texts[milestone.milestone_id], milestone.issue)) == 2
expected_target = {"PROJECT_SPEC.md", "ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md", "scripts/run_pipeline.py", "tests/test_run_pipeline.py", ISSUE, A, B}
assert set(git("diff", "--name-only", PARENT, TARGET).splitlines()) == expected_target
assert set(git("diff", "--name-only", TARGET, RECOVERED).splitlines()) == {ISSUE, "HANDOFF.md", "HUMAN_CHECKPOINT.md"}
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
baseline = json.loads((ROOT / PREFIX / "baseline-results.json").read_text())
hostile = json.loads((ROOT / PREFIX / "hostile-results.json").read_text())
assert baseline["target"] == hostile["target"] == TARGET
assert len(baseline["checks"]) == 3 and all(r["exit"] == 0 for r in baseline["checks"])
assert baseline["summary"]["round1_unadapted"]["requirement_mismatches"] == ["positive_independent"]
for group, size in [("round1_migrated", 22), ("round2_replays", 20), ("round3_replays", 15)]:
    assert len(baseline[group]) == size and all(r["requirement_met"] for r in baseline[group])
for rows in [baseline[g] for g in baseline if g.startswith("round")] + [hostile["cases"]]:
    assert all(r["refusal_no_mutation"] for r in rows if r["actual"] == "REFUSED")
    assert all(r["base_preserved"] for r in rows)
assert len(hostile["cases"]) == 50 and len(hostile["summary"]["mismatches"]) == 15
assert sum(r["actual"] == "ADVANCED" for r in hostile["cases"]) == 19
real = baseline["real_case"]
assert len(real["paths"]) == 6 and not real["uncovered"]
assert sorted(map(len, real["entry_removal_uncovered"].values())) == [1, 5]
assert real["unchanged_contract"] and real["unchanged_machine_state"] and real["all_parent_oracle_agrees"]
assert not real["hypothetical_AGENTS_supported_by_existing_entries"]
migrations = []
for issue in (A, B):
    before = git("show", PARENT + ":" + issue).splitlines()
    after = git("show", TARGET + ":" + issue).splitlines()
    removed = [line[1:] for line in difflib.unified_diff(before, after) if line.startswith("-") and not line.startswith("---")]
    assert len(removed) == 1 and removed[0].startswith("- **Updated UTC:**"), (issue, removed)
    assert (ROOT / issue).read_bytes() == subprocess.check_output(["git", "show", TARGET + ":" + issue])
    content = (ROOT / issue).read_text()
    decision = p._parse_authority_decision(content, issue)
    review_block = p._parse_review_round_block(content, issue) if issue == A else None
    migrations.append({"issue": issue, "decision": decision, "review": review_block,
                       "historical_prose_preserved_except_updated_utc": True})
for revision in ["6e39cea", "4f5e387", "4dda31e", "9000bb3", "0cb370f", "b80ccda", "47a0cb4", "79063cb"]:
    subprocess.run(["git", "merge-base", "--is-ancestor", revision, TARGET], check=True)
for name in ["_commit_paths", "_verify_target_scope", "_parse_intervening_registry"]:
    bodies = []
    for revision in [PARENT, TARGET]:
        tree = ast.parse(git("show", revision + ":scripts/run_pipeline.py"))
        bodies.append(ast.dump(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)))
    assert bodies[0] == bodies[1], name
print("PASS review: d9bd6d8 CHANGES_REQUIRED material=3 issue=IMPLEMENTING; three prior rounds preserved")
print("PASS HANDOFF: five sections, one bounded Next Action, authored activity preserved")
print("PASS reviewer-only changes; links=" + str(links) + "; regular files/fences/newlines/whitespace")
print("PASS discovery bytes/contract/state unchanged: IN_PROGRESS attempt=3 target=null registry_entries=2")
print("PASS evidence: 56/201 target tests and validator pass; 57 migrated replays conform; old missing-block positive refuses")
print("PASS new cases: 50 total, 4 controls, 31 no-mutation refusals, 13 material false advances and 2 non-material parser gaps")
print("PASS real A/B: six paths covered; removal five/one; no AGENTS attribution; no live or discovery transition")
print("PASS R1/R4 ASTs unchanged; target seven files, post-target reconciliation three files; preserved ancestry")
print("Migration projections independently inspected against historical Git content (not a general verifier-safety claim):")
print(json.dumps(migrations, indent=2, sort_keys=True))
