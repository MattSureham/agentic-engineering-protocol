"""Reviewer-owned offline reproductions; never transitions the source repository.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 <this-file> <repository> [--suite]
Code and fixture helpers are extracted from TARGET, not imported from HEAD.
Only disposable local Git repositories receive transitions or fixture edits.
An observed defect is a successful reproduction, not protocol conformance.
"""

import argparse
import importlib.util
import io
import json
import os
import platform
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace


TARGET = "6e39cea8ac46d909709ddaeeda1aa8d2df59ce08"
CANDIDATE = "9f72d3de57085525a8ddf8a3b14bf1a3161e26e8"
DISCOVERY = "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1"
SHARED = "OTHER/amendment.md"


def git(root, *args):
    return subprocess.check_output(["git"] + list(args), cwd=root, text=True).strip()


def put(fixture, path, content):
    destination = fixture.root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def entry(module, base, tip, issue=None):
    return {
        "issue": issue or module.INTERVENING_ISSUE,
        "from": base,
        "to": tip,
        "recorded_utc": "2026-09-30T01:51:59Z",
        "recorded_by": "agent:review-fixture-recorder",
    }


def finish(module, fixture, case, expected, details=None, target=None):
    target = target or fixture.make_target()
    before = module.AuthorizedMilestonePipelineTests.snapshot(fixture.root)
    state_before = fixture.state()
    result = fixture.submit(target)
    after = module.AuthorizedMilestonePipelineTests.snapshot(fixture.root)
    evidence = [json.loads(path.read_text()) for path in (fixture.root / "EVIDENCE").glob("*.json")]
    accepted = result.returncode == 0
    return {
        "case": case,
        "expected": expected,
        "actual": "ADVANCED" if accepted else "REFUSED",
        "requirement_met": accepted == (expected == "ADVANCE"),
        "exit": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "state": fixture.state()["state"],
        "refusal_no_mutation": (before == after and state_before == fixture.state()) if not accepted else None,
        "base_preserved": state_before["base_revision"] == fixture.state()["base_revision"],
        "scope_exclusions": [record.get("scope_exclusions") for record in evidence],
        "details": details or {},
    }


def reproduction(module, case):
    fixture = module.PipelineRepository()
    p = module.pipeline
    try:
        fixture.begin()
        base = fixture.commit("record running attempt")
        expected = "REFUSE"
        details = {}
        if case == "same_issue_registry":
            put(fixture, "AGENTS.md", "Unauthorized attempt-owned change; not a separate issue.\n")
            reviewed = fixture.commit("attempt-owned unauthorized change")
            fixture.add_review(reviewed, "APPROVED", 0)
            tip = fixture.commit("review label cannot widen milestone scope")
            fixture.add_registry([entry(module, base, tip, fixture.milestones[0]["issue"])])
            return finish(module, fixture, case, expected, {"registry_issue_equals_milestone_issue": True})
        if case in {"malformed_in_scope", "null_registry_in_scope"}:
            fixture.add_registry([], schema="unsupported")
            if case == "null_registry_in_scope":
                path = fixture.issue_path()
                text = path.read_text()
                begin = text.index(p.INTERVENING_BEGIN) + len(p.INTERVENING_BEGIN)
                end = text.index(p.INTERVENING_END, begin)
                path.write_text(text[:begin] + "\n```json\nnull\n```\n" + text[end:])
                details["parsed_null_registry"] = p._parse_intervening_registry(path.read_text(), str(path))
            return finish(module, fixture, case, expected, details)

        self_entry = case in {"positive_self", "self_awaiting_decision", "self_substantive"}
        if case == "wide_range_attempt_AGENTS":
            put(fixture, "AGENTS.md", "Attempt-owned unauthorized instructions; not approved by intervening issue.\n")
            details["attempt_owned_commit"] = fixture.commit("unauthorized attempt AGENTS change")
        if case == "merge_hidden_attempt_touch":
            fixture.git("switch", "-c", "intervening")
        fixture.write_intervening_issue(
            authority="AGENT" if case == "wrong_authority" else "HUMAN",
            review="SELF" if self_entry else "INDEPENDENT",
            status="BLOCKED" if case == "blocked_independent" else "OPEN",
            unblock="Awaiting owner approval; decision NOT RECORDED" if case == "self_awaiting_decision" else "SATISFIED - owner decision recorded",
        )
        issue = fixture.root / module.INTERVENING_ISSUE
        if case != "self_awaiting_decision":
            issue.write_text(issue.read_text().replace(
                "## Independent review rounds",
                "## Owner decision\n\n2026-09-30T01:00:00Z human:fixture-owner: approved only "
                + ("this issue's authority record" if self_entry else SHARED + " and this issue")
                + "; AGENTS.md and other attempt work are NOT authorized.\n\n## Independent review rounds",
            ))
        if not self_entry or case == "self_substantive":
            put(fixture, SHARED, "approved bytes\n")
        reviewed = fixture.commit("separately scoped intervening work")
        if not self_entry:
            fixture.add_intervening_review(
                reviewed,
                disposition="CHANGES_REQUIRED" if case == "unapproved_review" else "APPROVED",
                reviewer="agent:implementor" if case == "identity_conflict" else "agent:intervening-reviewer",
            )
            text = issue.read_text().replace(
                "- **Reviewed immutable state:**",
                "- **Scope:** Only " + SHARED + " and this issue; AGENTS.md and other attempt changes are NOT reviewed.\n- **Reviewed immutable state:**",
            )
            if case == "ambiguous_count":
                text = text.replace("**0**.", "**0 resolved; 1 still open**.")
            if case == "ambiguous_target":
                text = text.replace("(fixture intervening amendment).", "or `" + base + "`; target NOT disambiguated.")
            issue.write_text(text)
            tip = fixture.commit("intervening review record")
        else:
            tip = reviewed

        if case == "merge_post_review":
            fixture.git("switch", "-c", "record-side")
            put(fixture, "EVIDENCE/side.md", "side record\n")
            fixture.commit("side record")
            fixture.git("switch", "main")
            put(fixture, "EVIDENCE/main.md", "main record\n")
            fixture.commit("main record")
            fixture.git("merge", "--no-ff", "--no-commit", "record-side")
            put(fixture, SHARED, "unreviewed substantive merge edit\n")
            tip = fixture.commit("merge with unreviewed substantive change")
            details = {
                "reviewed_target": reviewed,
                "merge_commit": tip,
                "implementation_commit_paths": p._commit_paths(fixture.root, tip),
                "first_parent_changed_paths": fixture.git("diff", "--name-only", tip + "^1", tip).splitlines(),
                "final_substantive_content": (fixture.root / SHARED).read_text(),
            }
        if case == "merge_hidden_attempt_touch":
            fixture.git("switch", "main")
            put(fixture, SHARED, "unauthorized attempt change\n")
            unauthorized = fixture.commit("unregistered attempt touches same path")
            merge = subprocess.run(
                ["git", "merge", "--no-ff", "--no-commit", "intervening"],
                cwd=fixture.root, capture_output=True, text=True,
            )
            assert merge.returncode == 1 and "CONFLICT" in merge.stdout
            put(fixture, SHARED, "approved bytes\n")
            merged = fixture.commit("resolve merge to reviewed bytes")
            simplified = fixture.git("rev-list", base + ".." + merged, "--", SHARED).splitlines()
            full = fixture.git("rev-list", "--full-history", base + ".." + merged, "--", SHARED).splitlines()
            registered = fixture.git("rev-list", base + ".." + tip).splitlines()
            details = {
                "unregistered_touch": unauthorized,
                "simplified_touches": simplified,
                "full_history_touches": full,
                "unregistered_touch_in_range": unauthorized in registered,
            }
            assert unauthorized not in simplified and unauthorized in full and unauthorized not in registered
        if case == "partial_coverage":
            put(fixture, SHARED, "attempt change after accepted range\n")
            fixture.commit("attempt-owned change outside registered range")
        if case == "AGENTS_after_valid_range":
            put(fixture, "AGENTS.md", "attempt-owned out of scope\n")
            fixture.commit("unregistered AGENTS change")
        if case == "wrong_range":
            base, tip = tip, base
        entries = [entry(module, base, tip)]
        if case == "overlapping_unrelated_ranges":
            other_issue = "ISSUES/ISSUE-20260814T030051Z-other-authority.md"
            fixture.write_intervening_issue(path=other_issue)
            other = fixture.root / other_issue
            other.write_text(other.read_text().replace(
                "## Independent review rounds",
                "## Owner decision\n\nhuman:fixture-owner authorizes ONLY OTHER/second.md and this issue; "
                + SHARED + " and the other issue are NOT authorized here.\n\n## Independent review rounds",
            ))
            put(fixture, "OTHER/second.md", "second independently scoped work\n")
            second_target = fixture.commit("separate second intervention")
            fixture.add_intervening_review(second_target, path=other_issue, reviewer="agent:second-reviewer")
            other.write_text(other.read_text().replace(
                "- **Reviewed immutable state:**",
                "- **Scope:** ONLY OTHER/second.md and this issue; no other work reviewed.\n- **Reviewed immutable state:**",
            ))
            second_tip = fixture.commit("second scoped review")
            # Overlap the first range despite the second issue expressly
            # excluding that work from both its authority and review scope.
            entries.append(entry(module, base, second_tip, other_issue))
            details = {"ranges_overlap": True, "second_authority_expressly_excludes_first_work": True}
        fixture.add_registry(entries)
        if case in {"positive_independent", "positive_self"}:
            expected = "ADVANCE"
        if case in {"dirty_authority", "unrecorded_file"}:
            target = fixture.make_target()
            if case == "dirty_authority":
                issue.write_text(issue.read_text() + "\nUncommitted authority amendment.\n")
            else:
                put(fixture, "unrecorded.txt", "not committed\n")
            return finish(module, fixture, case, expected, details, target)
        return finish(module, fixture, case, expected, details)
    finally:
        fixture.cleanup()


def real_case(root, module):
    p = module.pipeline
    source = lambda revision, path: git(root, "show", revision + ":" + path)
    milestones = p._parse_contract_text(source(TARGET, "PROJECT_SPEC.md"), "PROJECT_SPEC.md")
    milestone = next(item for item in milestones if item.milestone_id == DISCOVERY)
    text = source(TARGET, milestone.issue)
    state = p._parse_state(text, milestone)
    registry = p._parse_intervening_registry(text, milestone.issue)
    entries = []
    for item in registry:
        assert (root / item["issue"]).read_text().rstrip() == source(TARGET, item["issue"])
        entries.append(p._verify_intervening_entry(SimpleNamespace(root=root), state["implementor"], item, CANDIDATE, milestone.issue))
    base = state["base_revision"]
    outside = sorted(path for path in git(root, "diff", "--name-only", base + ".." + CANDIDATE).splitlines() if not p._path_allowed(path, milestone.raw["allowed_paths"]))
    # Independent enumeration: inspect every reachable commit against every
    # parent (-m), without Git's path-limited history simplification.
    commit_paths = {
        commit: set(git(root, "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", commit).splitlines())
        for commit in git(root, "rev-list", base + ".." + CANDIDATE).splitlines()
    }
    rows = []
    for path in outside:
        touches = sorted(commit for commit, paths in commit_paths.items() if path in paths)
        supports = [item for item in entries if path in item["excludable"] and set(touches) <= item["commits"]]
        rows.append({
            "path": path, "touches": touches,
            "support": [{key: item[key] for key in ("issue", "from", "to", "review")} for item in supports],
        })
    removals = {
        item["issue"]: [row["path"] for row in rows if not any(support["issue"] != item["issue"] for support in row["support"])]
        for item in entries
    }
    parent = git(root, "rev-parse", TARGET + "^")
    before_contract = p._extract_json_block(source(parent, "PROJECT_SPEC.md"), p.CONTRACT_BEGIN, p.CONTRACT_END, "PROJECT_SPEC.md")
    after_contract = p._extract_json_block(source(TARGET, "PROJECT_SPEC.md"), p.CONTRACT_BEGIN, p.CONTRACT_END, "PROJECT_SPEC.md")
    before_state = p._parse_state(source(parent, milestone.issue), milestone)
    return {
        "candidate": CANDIDATE, "base": base,
        "state": state["state"], "attempt": state["attempt"], "implementor": state["implementor"],
        "target_revision": state["target_revision"], "digest": milestone.digest,
        "unchanged_contract": before_contract == after_contract,
        "unchanged_machine_state": before_state == state,
        "registry_entries": registry, "paths": rows, "entry_removal_uncovered": removals,
        "uncovered": [row["path"] for row in rows if not row["support"]],
        "boundary": "Read-only component attribution at historical candidate, NOT a submission or target==HEAD bypass.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--suite", action="store_true")
    parser.add_argument("--supplemental", action="store_true", help="Only same-issue, unresolved-issue and overlapping-provenance probes")
    args = parser.parse_args()
    root = args.repository.resolve()
    raw = subprocess.check_output(["git", "archive", "--format=tar", TARGET], cwd=root)
    output = {
        "target": TARGET,
        "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "git": git(root, "--version")},
        "checks": [],
    }
    with tempfile.TemporaryDirectory(prefix="aep scope reviewer ") as directory:
        extracted = Path(directory)
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            archive.extractall(extracted)
        if args.suite:
            for argv in [
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_run_pipeline.py", "-v"],
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                [sys.executable, "scripts/validate_protocol.py"],
            ]:
                result = subprocess.run(argv, cwd=extracted, capture_output=True, text=True, timeout=180, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                output["checks"].append({"argv": argv, "exit": result.returncode, "stdout": result.stdout, "stderr_tail": result.stderr.splitlines()[-5:]})
                assert result.returncode == 0, result.stdout + result.stderr
        spec = importlib.util.spec_from_file_location("review_target_fixture", extracted / "tests/test_run_pipeline.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cases = [
            "positive_independent", "positive_self", "unapproved_review", "wrong_authority",
            "identity_conflict", "wrong_range", "partial_coverage", "self_substantive",
            "dirty_authority", "unrecorded_file", "AGENTS_after_valid_range",
            "merge_post_review", "merge_hidden_attempt_touch", "wide_range_attempt_AGENTS",
            "ambiguous_count", "ambiguous_target", "self_awaiting_decision",
            "malformed_in_scope", "null_registry_in_scope",
        ]
        if args.supplemental:
            cases = ["same_issue_registry", "blocked_independent", "overlapping_unrelated_ranges"]
        output["probes"] = [reproduction(module, case) for case in cases]
        output["real_case"] = real_case(root, module)
        output["summary"] = {
            "cases": len(cases),
            "requirement_violations": [row["case"] for row in output["probes"] if not row["requirement_met"]],
            "all_refusals_preserve_files_and_state": all(row["refusal_no_mutation"] for row in output["probes"] if row["actual"] == "REFUSED"),
        }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
