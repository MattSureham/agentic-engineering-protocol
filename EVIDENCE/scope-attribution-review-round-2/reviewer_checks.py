"""Offline independent review of frozen PIPELINE-010 round-2 target.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py . [--suite]
Only temporary fixture repositories receive edits or transitions. No live probes.
Exit zero means procedures completed, NOT that the amendment conforms.
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

TARGET = "4f5e38744340fb7597222bf31483eb67187e2bbf"
BASELINE = "6e39cea8ac46d909709ddaeeda1aa8d2df59ce08"
CANDIDATE = "9f72d3de57085525a8ddf8a3b14bf1a3161e26e8"
DISCOVERY = "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1"
SHARED = "OTHER/amendment.md"
OLD_CASES = [
    "positive_independent", "positive_self", "unapproved_review", "wrong_authority",
    "identity_conflict", "wrong_range", "partial_coverage", "self_substantive",
    "dirty_authority", "unrecorded_file", "AGENTS_after_valid_range",
    "merge_post_review", "merge_hidden_attempt_touch", "wide_range_attempt_AGENTS",
    "ambiguous_count", "ambiguous_target", "self_awaiting_decision",
    "malformed_in_scope", "null_registry_in_scope", "same_issue_registry",
    "blocked_independent", "overlapping_unrelated_ranges",
]
NEW_CASES = [
    "declared_AGENTS_widening", "declared_prefix_widening", "same_path_range_widening",
    "foreign_substantive_control", "review_unknown_zero", "review_negated_zero",
    "review_41_hex_target", "review_duplicate_sections", "review_missing_status",
    "review_unresolved_status", "self_pending_heading", "self_empty_heading",
    "self_fenced_heading", "self_blocked_control", "overlapping_scopes",
    "unused_declared_path", "merge_parent_asymmetry", "octopus_record_only",
    "octopus_substantive", "absent_registry_control",
]


def git(root, *args):
    return subprocess.check_output(["git"] + list(args), cwd=root, text=True).strip()


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract(root, revision, directory):
    raw = subprocess.check_output(["git", "archive", "--format=tar", revision], cwd=root)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        archive.extractall(directory)
    # Test helper imports run_pipeline by name. Ensure each revision gets its own.
    sys.modules.pop("run_pipeline", None)
    return module_at("fixture_" + revision[:7], directory / "tests/test_run_pipeline.py")


def explicit_parent_paths(root, revision):
    parents = git(root, "show", "-s", "--format=%P", revision).split()
    assert parents, "review fixtures/window do not include repository root commits"
    return sorted(set().union(*[
        set(git(root, "diff", "--name-only", parent, revision).splitlines())
        for parent in parents
    ]))


def replay(old, module, case, v2):
    original_entry = old.entry
    original_write = module.PipelineRepository.write_intervening_issue
    if v2:
        def entry(m, base, tip, issue=None):
            value = original_entry(m, base, tip, issue)
            if case in {"positive_self", "self_awaiting_decision", "self_substantive"}:
                paths = []
            elif case == "same_issue_registry":
                paths = ["AGENTS.md"]
            elif issue and issue != m.INTERVENING_ISSUE:
                paths = ["OTHER/second.md"]
            else:
                paths = [SHARED]
            value["paths"] = paths
            return value
        old.entry = entry

        def write(self, *args, **kwargs):
            # v2's fixture helper added decision=True. Preserve the original
            # absent-decision adversarial precondition instead of bypassing it.
            kwargs["decision"] = case == "positive_self"
            return original_write(self, *args, **kwargs)
        module.PipelineRepository.write_intervening_issue = write
    try:
        if case != "null_registry_in_scope":
            return old.reproduction(module, case)
        # Original harness called the parser before submission; v2 now raises.
        # Preserve null bytes but exercise the actual CLI and no-mutation oracle.
        fixture = module.PipelineRepository()
        try:
            fixture.begin()
            fixture.commit("record running attempt")
            fixture.add_registry([])
            path = fixture.issue_path()
            text = path.read_text()
            begin = text.index(module.pipeline.INTERVENING_BEGIN) + len(module.pipeline.INTERVENING_BEGIN)
            end = text.index(module.pipeline.INTERVENING_END, begin)
            path.write_text(text[:begin] + "\n```json\nnull\n```\n" + text[end:])
            return old.finish(module, fixture, case, "REFUSE")
        finally:
            fixture.cleanup()
    finally:
        old.entry = original_entry
        module.PipelineRepository.write_intervening_issue = original_write


def new_case(old, module, case):
    fixture = module.PipelineRepository()
    p = module.pipeline
    details = {}
    try:
        fixture.begin()
        base = fixture.commit("record running attempt")
        if case == "absent_registry_control":
            return old.finish(module, fixture, case, "ADVANCE")
        own = case.startswith("self_")
        paths = [] if own else [SHARED]
        if case in {"declared_AGENTS_widening", "declared_prefix_widening", "same_path_range_widening", "foreign_substantive_control"}:
            unauthorized = {"declared_prefix_widening": "OTHER/unapproved.md", "same_path_range_widening": SHARED}.get(case, "AGENTS.md")
            old.put(fixture, unauthorized, "unauthorized current-attempt work\n")
            details["attempt_owned_commit"] = fixture.commit("current-attempt unauthorized work")
            if case == "declared_AGENTS_widening":
                paths.append("AGENTS.md")
            elif case == "declared_prefix_widening":
                paths = ["OTHER/"]
        fixture.write_intervening_issue(review="SELF" if own else "INDEPENDENT", status="BLOCKED" if case == "self_blocked_control" else "OPEN")
        issue = fixture.root / module.INTERVENING_ISSUE
        text = issue.read_text().replace(
            "human:fixture-owner approved this separate authority record.",
            "human:fixture-owner approves only this issue's records." if own else
            "human:fixture-owner approves ONLY OTHER/amendment.md for the later separate intervention; "
            "AGENTS.md, OTHER/unapproved.md and all earlier current-attempt changes (including any to "
            "OTHER/amendment.md) are expressly NOT authorized or accepted here.",
        )
        if case == "self_pending_heading":
            text = text.replace("human:fixture-owner approves only this issue's records.", "Owner has NOT approved. Awaiting decision; no authorization exists.")
            text = text.replace("SATISFIED - owner decision recorded in this issue", "Awaiting owner approval; decision NOT RECORDED")
        elif case == "self_empty_heading":
            text = text.replace("human:fixture-owner approves only this issue's records.", "")
        elif case == "self_fenced_heading":
            text = text.replace("### Owner decision recorded 2026-08-14T03:10:00Z\n\nhuman:fixture-owner approves only this issue's records.",
                                "No owner decision exists. The following is only an example:\n\n```markdown\n### Owner decision recorded 2026-08-14T03:10:00Z\n```")
        elif case == "review_missing_status":
            text = text.replace("- **Status:** `OPEN`\n", "")
        elif case == "review_unresolved_status":
            text = text.replace("- **Status:** `OPEN`", "- **Status:** `UNRESOLVED`")
        issue.write_text(text)
        if not own:
            old.put(fixture, SHARED, "approved separate amendment bytes\n")
        reviewed = fixture.commit("separate intervention limited to its recorded authority")
        if not own:
            fixture.add_intervening_review(reviewed)
            text = issue.read_text().replace("- **Reviewed immutable state:**", "- **Scope:** Only OTHER/amendment.md and this issue for the separate intervention; earlier attempt work is NOT reviewed.\n- **Reviewed immutable state:**")
            if case == "review_unknown_zero":
                text = text.replace("**0**.", "UNKNOWN (lower bound 0); actual open count not established.")
            elif case == "review_negated_zero":
                text = text.replace("**0**.", "NOT 0; material findings remain.")
            elif case == "review_41_hex_target":
                text = text.replace("`" + reviewed + "` (fixture intervening amendment).", "`" + reviewed + "0`")
            elif case == "review_duplicate_sections":
                text += "\n## Independent review rounds\n\n### 2026-08-14T03:26:00Z — agent:intervening-reviewer\n\n- **Reviewed immutable state:** `" + reviewed + "`\n- **Open material findings:** **1**.\n- **Disposition:** **CHANGES_REQUIRED**.\n"
            issue.write_text(text)
            tip = fixture.commit("limited independent review")
        else:
            tip = reviewed
        if case == "unused_declared_path":
            paths.append("OTHER/never-touched.md")
        if case == "merge_parent_asymmetry":
            fixture.git("switch", "-c", "asymmetric-side", base)
            old.put(fixture, "EVIDENCE/side.md", "record\n")
            fixture.commit("side lacking reviewed implementation")
            fixture.git("switch", "main")
            fixture.git("merge", "--no-ff", "--no-commit", "asymmetric-side")
            tip = fixture.commit("post-review merge agrees with first parent only")
        elif case.startswith("octopus_"):
            fork = tip
            for branch in ("side-a", "side-b"):
                fixture.git("switch", "-c", branch, fork)
                old.put(fixture, "EVIDENCE/" + branch + ".md", "record\n")
                fixture.commit(branch)
            fixture.git("switch", "main")
            old.put(fixture, "EVIDENCE/main.md", "record\n")
            fixture.commit("main record")
            fixture.git("merge", "--no-ff", "--no-commit", "side-a", "side-b")
            if case == "octopus_substantive":
                old.put(fixture, SHARED, "unreviewed octopus resolution\n")
            tip = fixture.commit("octopus resolution")
        if case == "merge_parent_asymmetry" or case.startswith("octopus_"):
            details.update({"parents": git(fixture.root, "show", "-s", "--format=%P", tip).split(),
                            "first_parent_paths": git(fixture.root, "diff", "--name-only", tip + "^1", tip).splitlines(),
                            "explicit_parent_paths": explicit_parent_paths(fixture.root, tip),
                            "implementation_paths": p._commit_paths(fixture.root, tip)})
            assert details["explicit_parent_paths"] == details["implementation_paths"]
        registered = old.entry(module, base, tip)
        registered["paths"] = paths
        entries = [registered]
        if case == "overlapping_scopes":
            second_issue = "ISSUES/ISSUE-20260814T030051Z-other-authority.md"
            fixture.write_intervening_issue(path=second_issue)
            old.put(fixture, "OTHER/second.md", "second intervention\n")
            second_target = fixture.commit("second intervention")
            fixture.add_intervening_review(second_target, path=second_issue)
            second_tip = fixture.commit("second review")
            second = old.entry(module, base, second_tip, second_issue)
            second["paths"] = ["OTHER/"]
            entries.append(second)
        fixture.add_registry(entries)
        details.update({"authority_and_review_record": issue.read_text(), "registry_entries": entries})
        return old.finish(module, fixture, case, "ADVANCE" if case == "octopus_record_only" else "REFUSE", details)
    finally:
        fixture.cleanup()


def real_case(root, module):
    p = module.pipeline
    source = lambda rev, name: git(root, "show", rev + ":" + name)
    milestone = next(m for m in p._parse_contract_text(source(TARGET, "PROJECT_SPEC.md"), "PROJECT_SPEC.md") if m.milestone_id == DISCOVERY)
    text = source(TARGET, milestone.issue)
    state = p._parse_state(text, milestone)
    registry = p._parse_intervening_registry(text, milestone.issue)
    assert len(registry) == 2
    entries = []
    provenance = []
    for item in registry:
        record = source(TARGET, item["issue"])
        assert (root / item["issue"]).read_text().rstrip() == record
        verified = p._verify_intervening_entry(SimpleNamespace(root=root), state["implementor"], item, CANDIDATE, milestone.issue, milestone.raw["allowed_paths"])
        entries.append(verified)
        provenance.append({"issue": item["issue"], "metadata": p._metadata(record, item["issue"]),
                           "review": vars(p._tolerant_latest_review(record, item["issue"])) if verified["review"] == "INDEPENDENT" else None,
                           "owner_heading_timestamps": p.OWNER_DECISION_RE.findall(record)})
    base = state["base_revision"]
    window = {commit: explicit_parent_paths(root, commit) for commit in git(root, "rev-list", base + ".." + CANDIDATE).splitlines()}
    assert all(paths == p._commit_paths(root, commit) for commit, paths in window.items())
    outside = sorted(name for name in git(root, "diff", "--name-only", base + ".." + CANDIDATE).splitlines() if not p._path_allowed(name, milestone.raw["allowed_paths"]))
    rows = []
    for name in outside:
        touches = sorted(commit for commit, paths in window.items() if name in paths)
        support = [{key: entry[key] for key in ("issue", "from", "to", "review")} for entry in entries
                   if p._path_allowed(name, entry["excludable"]) and set(touches) <= entry["commits"]]
        rows.append({"path": name, "touching_commits": touches, "support": support})
    parent = git(root, "rev-parse", TARGET + "^")
    contract = lambda rev: p._extract_json_block(source(rev, "PROJECT_SPEC.md"), p.CONTRACT_BEGIN, p.CONTRACT_END, "PROJECT_SPEC.md")
    return {"candidate": CANDIDATE, "base": base, "state": state,
            "boundary": "Historical read-only component characterization, NOT a submission or target==HEAD bypass.",
            "unchanged_contract": contract(parent) == contract(TARGET),
            "unchanged_machine_state": state == p._parse_state(source(parent, milestone.issue), milestone),
            "registry_entries": registry, "provenance": provenance, "paths": rows,
            "all_parent_oracle_agrees": True,
            "uncovered": [row["path"] for row in rows if not row["support"]],
            "entry_removal_uncovered": {item["issue"]: [row["path"] for row in rows if not any(s["issue"] != item["issue"] for s in row["support"])] for item in entries},
            "hypothetical_AGENTS_supported_by_existing_entries": any(p._path_allowed("AGENTS.md", item["excludable"]) for item in entries)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--suite", action="store_true")
    args = parser.parse_args()
    root = args.repository.resolve()
    output = {"target": TARGET, "baseline": BASELINE,
              "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "environment": {"platform": platform.platform(), "python": platform.python_version(), "git": git(root, "--version")},
              "checks": []}
    with tempfile.TemporaryDirectory(prefix="aep round2 review ") as directory:
        work = Path(directory)
        target_dir = work / "target"
        baseline_dir = work / "baseline"
        target_dir.mkdir()
        baseline_dir.mkdir()
        module = extract(root, TARGET, target_dir)
        old = module_at("round1_reviewer", target_dir / "EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py")
        baseline_module = extract(root, BASELINE, baseline_dir)
        if args.suite:
            for argv in [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_run_pipeline.py", "-v"],
                         [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                         [sys.executable, "scripts/validate_protocol.py"]]:
                result = subprocess.run(argv, cwd=target_dir, capture_output=True, text=True, timeout=180, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                output["checks"].append({"argv": argv, "exit": result.returncode, "stdout": result.stdout, "stderr_tail": result.stderr.splitlines()[-5:]})
                assert result.returncode == 0, result.stdout + result.stderr
        output["baseline_replays"] = [replay(old, baseline_module, case, False) for case in OLD_CASES]
        output["v2_replays"] = [replay(old, module, case, True) for case in OLD_CASES]
        output["new_cases"] = [new_case(old, module, case) for case in NEW_CASES]
        output["real_case"] = real_case(root, module)
        output["summary"] = {
            group: {"cases": len(output[group]),
                    "requirement_violations": [row["case"] for row in output[group] if not row["requirement_met"]],
                    "all_refusals_preserve_files_and_state": all(row["refusal_no_mutation"] for row in output[group] if row["actual"] == "REFUSED")}
            for group in ("baseline_replays", "v2_replays", "new_cases")
        }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
