"""Read-only assertions for Round 5 records, histories, results and scope."""
import ast
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
TARGET = "5bf73a0ab33bc851678c6adee30c45780d2bdb03"
BASE = "301bc45f1f881554054d14e67edec099e209a267"
RECOVERED = "46f63599bf329ecbf58d6d6c395e995cd9bd57d4"
ISSUE = "ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md"
EVIDENCE = "EVIDENCE/EVIDENCE-20261013T012716Z-scope-attribution-review-round-5.md"
PREFIX = "EVIDENCE/scope-attribution-review-round-5/"
A = "ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md"
B = "ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md"
sys.path.insert(0, str(ROOT / "scripts"))
import run_pipeline as p


def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True).strip()


def raw(revision, path):
    return subprocess.check_output(["git", "show", revision + ":" + path])


text = (ROOT / ISSUE).read_text()
review = p._tolerant_latest_review(text, ISSUE)
assert (review.target, review.disposition, review.material_findings, review.reviewer) == (
    TARGET, "CHANGES_REQUIRED", 3, "agent:Codex-scope-review-20261013")
assert p._metadata(text, ISSUE)["Status"] == "IMPLEMENTING"
old = raw(RECOVERED, ISSUE).decode()
rounds = old.split("\n## Independent review rounds\n", 1)[1].split("\n## Blocker", 1)[0]
assert rounds.strip() in text
history = old.split("\n## Activity history\n", 1)[1].split("\n## Closure checklist", 1)[0]
assert history.strip() in text
assert text.count("### 2026-10-13T01:28:02Z — agent:Codex-scope-review-20261013") == 1
assert "\n\n| `2026-10-13T01:28:02Z` |" not in text, "new table rows must continue their tables"
handoff = (ROOT / "HANDOFF.md").read_text()
assert re.findall(r"^## (.+)$", handoff, re.M) == [
    "Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"]
next_action = handoff.split("## Next Action\n", 1)[1].split("\n## ", 1)[0].strip()
assert len(next_action.split("\n\n")) == 1 and all(x in next_action for x in ["R2", "R3", "R5"])
history = raw(RECOVERED, "HANDOFF.md").decode().split("## Recent Activity\n", 1)[1].lstrip()
assert handoff.rstrip().endswith(history.rstrip())
old_checkpoint = raw(RECOVERED, "HUMAN_CHECKPOINT.md").decode().split("\n## ", 1)[1]
assert (ROOT / "HUMAN_CHECKPOINT.md").read_text().endswith(old_checkpoint)

context = p._load_context(ROOT)
milestone = next(m for m in context.milestones if m.milestone_id == "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1")
state = context.states[milestone.milestone_id]
assert (state["state"], state["attempt"], state["target_revision"]) == ("IN_PROGRESS", 3, None)
assert state["authority_digest"] == "c2e02b5ba533a65cc362481a89744d4574bb27601cba7170f7e31bc5a5c4c96f"
contract = (ROOT / "PROJECT_SPEC.md").read_text().split(p.CONTRACT_BEGIN, 1)[1].split(p.CONTRACT_END, 1)[0]
for revision in (BASE, TARGET, RECOVERED):
    assert (ROOT / milestone.issue).read_bytes() == raw(revision, milestone.issue)
    assert raw(revision, "PROJECT_SPEC.md").decode().split(p.CONTRACT_BEGIN, 1)[1].split(p.CONTRACT_END, 1)[0] == contract
    for issue in (A, B):
        assert (ROOT / issue).read_bytes() == raw(revision, issue)
assert len(p._parse_intervening_registry(context.issue_texts[milestone.milestone_id], milestone.issue)) == 2
assert "None — this amendment" in text and p.STATE_BEGIN not in text
expected_target = {"PROJECT_SPEC.md", "ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md",
                   "scripts/run_pipeline.py", "tests/test_run_pipeline.py", ISSUE}
assert set(git("diff", "--name-only", BASE, TARGET).splitlines()) == expected_target
assert set(git("diff", "--name-only", TARGET, RECOVERED).splitlines()) == {ISSUE, "HANDOFF.md", "HUMAN_CHECKPOINT.md"}
for path in ("PROJECT_SPEC.md", "ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md"):
    before, after = raw(BASE, path).decode().splitlines(), raw(TARGET, path).decode().splitlines()
    removed = [line[1:] for line in difflib.unified_diff(before, after) if line.startswith("-") and not line.startswith("---")]
    assert len(removed) == 1 and (removed[0].startswith("- **PIPELINE-010") or removed[0].startswith("7. Git commits"))
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

baseline, fourth, new = [json.loads((ROOT / PREFIX / name).read_text()) for name in (
    "baseline-results.json", "round4-results.json", "adversarial-results.json")]
assert baseline["target"] == fourth["target"] == new["target"] == TARGET
assert len(baseline["checks"]) == 3 and all(r["exit"] == 0 for r in baseline["checks"])
assert any("Ran 57 tests" in s for s in baseline["checks"][0]["stderr_tail"])
assert any("Ran 202 tests" in s for s in baseline["checks"][1]["stderr_tail"])
assert baseline["summary"]["round1_unadapted"]["requirement_mismatches"] == ["positive_independent"]
assert baseline["summary"]["round2_replays"]["requirement_mismatches"] == ["octopus_record_only"]
assert len(baseline["round2_replays"]) == 20
for group, size in [("round1_migrated", 22), ("round3_replays", 15)]:
    assert len(baseline[group]) == size and all(r["requirement_met"] for r in baseline[group])
assert new["octopus_fixture_calibration"]["actual"] == "ADVANCED"
assert len(fourth["cases"]) == 50 and not fourth["summary"]["mismatches"]
assert sum(r["actual"] == "ADVANCED" for r in fourth["cases"]) == 4
assert len(new["cases"]) == 16 and len(new["summary"]["mismatches"]) == 11
assert sum(r["actual"] == "ADVANCED" for r in new["cases"]) == 13
for rows in [baseline[g] for g in baseline if g.startswith("round")] + [fourth["cases"], new["cases"]]:
    assert all(r["refusal_no_mutation"] for r in rows if r["actual"] == "REFUSED")
    assert all(r["base_preserved"] for r in rows)
    assert all(r["exit"] == 0 and r["state"] == "AWAITING_PEER_REVIEW" for r in rows if r["actual"] == "ADVANCED")
real = baseline["real_case"]
assert len(real["paths"]) == 6 and not real["uncovered"]
assert sorted(map(len, real["entry_removal_uncovered"].values())) == [1, 5]
assert real["unchanged_contract"] and real["unchanged_machine_state"] and real["all_parent_oracle_agrees"]
assert not real["hypothetical_AGENTS_supported_by_existing_entries"]
assert real["state"] == state
anchors = []
for issue in (A, B):
    content = (ROOT / issue).read_text()
    decision = p._parse_authority_decision(content, issue)
    review_block = p._parse_review_round_block(content, issue) if issue == A else None
    anchors.append({"issue": issue, "decision": decision, "review": review_block})
for revision in ["6e39cea", "4f5e387", "4dda31e", "d9bd6d8", "9000bb3", "0cb370f", "b80ccda", "301bc45", "47a0cb4", "79063cb"]:
    subprocess.run(["git", "merge-base", "--is-ancestor", revision, TARGET], check=True)
for name in ["_commit_paths", "_verify_target_scope", "_parse_intervening_registry"]:
    bodies = []
    for revision in (BASE, TARGET):
        tree = ast.parse(raw(revision, "scripts/run_pipeline.py").decode())
        bodies.append(ast.dump(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)))
    assert bodies[0] == bodies[1], name

print("PASS Round 5: 5bf73a0 CHANGES_REQUIRED material=3 issue=IMPLEMENTING; four prior rounds/activity preserved")
print("PASS HANDOFF/checkpoint: five sections, one bounded Next Action, authored history preserved")
print("PASS reviewer-only changes; links=" + str(links) + "; regular files/fences/newlines/whitespace")
print("PASS discovery/A/B bytes and contract unchanged: IN_PROGRESS attempt=3 target=null registry_entries=2")
print("PASS evidence: 57/202 target tests + validator; 50 Round-4 and 15 Round-3 expected outcomes")
print("PASS earlier replays: 22 migrated Round-1 conform; two original fixture mismatches retained; calibrated octopus advances")
print("PASS new evidence: 16 cases, 11 unsafe advances, 2 controls, 3 no-mutation refusals; all bases preserved")
print("PASS real A/B: six covered paths, removal five/one, no hypothetical AGENTS, independent parent oracle agrees")
print("PASS R1/R4 ASTs unchanged, target five files, reconciliation three files, specification delta bounded, ancestry preserved")
print("Actual A/B block facts manually compared to historical Git records (not a generic verifier-safety claim):")
print(json.dumps(anchors, indent=2, sort_keys=True))
