"""Frozen-target offline review. Only disposable fixture repositories mutate.

PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-3/reviewer_checks.py . --suite
Exit 0 means reproduction completed, not that the target conforms.
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

TARGET = "4dda31e9945000b51e950f4ac01ec7f82ffb15bf"
SHARED = "OTHER/amendment.md"
BODY = "human:fixture-owner approved this separate authority record."
CASES = [
    "post_introduction_foreign", "draft_introduction", "deleted_readded_authority",
    "mixed_authority_merge", "side_work_before_introduction", "merge_introduction_positive",
    "rename_positive", "delete_readd_post_review", "review_long_fence_example",
    "review_malformed_latest", "review_duplicate_timestamp", "self_contracted_negation",
    "self_positive_pending_control", "self_satisfied_pending", "self_duplicate_unblock",
]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hostile(old, prior, module, case):
    fixture = module.PipelineRepository()
    p = module.pipeline
    own = case.startswith("self_")
    details = {}
    try:
        fixture.begin()
        base = fixture.commit("record running attempt")
        issue = fixture.root / module.INTERVENING_ISSUE
        paths = [] if own else [SHARED]
        if case == "merge_introduction_positive":
            fixture.git("switch", "-c", "authority-side")
        if case == "side_work_before_introduction":
            fixture.git("switch", "-c", "foreign-side")
            old.put(fixture, "AGENTS.md", "unauthorized attempt work predating separate authority\n")
            details["foreign_commit"] = fixture.commit("foreign side attempt work")
            fixture.git("switch", "main")
        fixture.write_intervening_issue(review="SELF" if own else "INDEPENDENT")
        text = issue.read_text()
        if not own:
            text = text.replace(BODY, "human:fixture-owner approved ONLY OTHER/amendment.md and this issue; "
                                "AGENTS.md and all current-attempt-owned work are expressly NOT authorized here.")
        if case in {"draft_introduction", "deleted_readded_authority"}:
            text = text.replace("- **Authority:** `HUMAN`", "- **Authority:** `AGENT`")
            text = text.replace("human:fixture-owner approved ONLY OTHER/amendment.md and this issue; "
                                "AGENTS.md and all current-attempt-owned work are expressly NOT authorized here.",
                                "Proposal only. No owner authority exists yet.")
        if case == "self_contracted_negation":
            text = text.replace(BODY, "human:fixture-owner hasn't approved this authority record.")
        elif case == "self_positive_pending_control":
            text = text.replace(BODY, "human:fixture-owner approved preparation only; authorization is pending.")
        elif case == "self_satisfied_pending":
            text = text.replace("SATISFIED - owner decision recorded in this issue", "SATISFIED is false; awaiting owner authorization")
        elif case == "self_duplicate_unblock":
            text += "\n- **Unblock condition:** `PENDING - owner authorization is unresolved`\n"
        issue.write_text(text)
        introduced = fixture.commit("introduce separate issue record")
        details["initial_issue_commit"] = introduced
        if case == "merge_introduction_positive":
            fixture.git("switch", "main")
            old.put(fixture, "EVIDENCE/main.md", "main record\n")
            fixture.commit("record concurrent main history")
            fixture.git("merge", "--no-ff", "authority-side", "-m", "merge authority record before work")
        if case == "deleted_readded_authority":
            fixture.git("rm", module.INTERVENING_ISSUE)
            fixture.commit("delete unauthoritative proposal record")
        if case in {"post_introduction_foreign", "draft_introduction", "deleted_readded_authority"}:
            old.put(fixture, "AGENTS.md", "unauthorized current-attempt work, excluded by separate owner and review\n")
            details["foreign_commit"] = fixture.commit("attempt-owned foreign substantive work")
            paths.append("AGENTS.md")
        if case in {"draft_introduction", "deleted_readded_authority"}:
            fixture.write_intervening_issue()
            issue.write_text(issue.read_text().replace(BODY, "human:fixture-owner approved ONLY OTHER/amendment.md "
                                                       "and this issue; the preceding AGENTS.md work is NOT authorized."))
            details["actual_authority_commit"] = fixture.commit("owner authorizes later separate work only")
        if case == "mixed_authority_merge":
            fixture.git("switch", "-c", "foreign-side")
            old.put(fixture, "AGENTS.md", "foreign work expressly outside separate authority\n")
            details["foreign_commit"] = fixture.commit("foreign branch work after issue introduction")
            fixture.git("switch", "main")
        if not own:
            old.put(fixture, SHARED, "approved separate amendment bytes\n")
            reviewed = fixture.commit("separately scoped substantive amendment")
        else:
            reviewed = introduced
        if case in {"mixed_authority_merge", "side_work_before_introduction"}:
            fixture.git("merge", "--no-ff", "foreign-side", "-m", "merge foreign work before narrowly scoped review")
            reviewed = fixture.git("rev-parse", "HEAD")
            paths.append("AGENTS.md")
            details["merge_paths_explicit_parents"] = prior.explicit_parent_paths(fixture.root, reviewed)
            assert details["merge_paths_explicit_parents"] == p._commit_paths(fixture.root, reviewed)
        if case == "rename_positive":
            renamed = "OTHER/renamed.md"
            fixture.git("mv", SHARED, renamed)
            issue.write_text(issue.read_text().replace("ONLY OTHER/amendment.md", "ONLY OTHER/amendment.md and OTHER/renamed.md (authorized rename)"))
            reviewed = fixture.commit("authorized exact-file rename")
            paths.append(renamed)
        if not own:
            fixture.add_intervening_review(reviewed)
            text = issue.read_text().replace("- **Reviewed immutable state:**", "- **Scope:** Only the separate amendment and its authorized rename, if any. AGENTS.md and current-attempt work are NOT reviewed.\n- **Reviewed immutable state:**")
            if case == "review_long_fence_example":
                begin = text.index("## Independent review rounds")
                end = text.index("\n## Blocker", begin)
                text = text[:begin] + "## Example only; no actual review exists\n\n````markdown\n```example\n" + text[begin:end] + "\n````\n" + text[end:]
            elif case == "review_malformed_latest":
                text = text.replace("\n## Blocker", "\n### 2026-08-14T03:26:00Z - agent:latest-reviewer\n\nLatest review is BLOCKED; required authority is unresolved. Do not use the earlier approval.\n\n## Blocker")
            issue.write_text(text)
            if case == "review_duplicate_timestamp":
                fixture.add_intervening_review(reviewed, reviewer="agent:other-reviewer", utc="2026-08-14T03:25:00Z")
            tip = fixture.commit("persist scoped review provenance")
        else:
            tip = reviewed
        if case == "delete_readd_post_review":
            fixture.git("rm", SHARED)
            fixture.commit("unreviewed deletion")
            old.put(fixture, SHARED, "approved separate amendment bytes\n")
            tip = fixture.commit("unreviewed readdition of identical final bytes")
        entry = old.entry(module, base, tip)
        entry["paths"] = paths
        fixture.add_registry([entry])
        details.update({"registry_entry": entry, "authority_and_review_record": issue.read_text(),
                        "introduction_selected": p._issue_introduction(fixture.root, module.INTERVENING_ISSUE, fixture.milestones[0]["issue"]),
                        "commit_graph": fixture.git("log", "--format=%H %P %s", base + "..HEAD")})
        expected = "ADVANCE" if case in {"merge_introduction_positive", "rename_positive"} else "REFUSE"
        return old.finish(module, fixture, case, expected, details)
    finally:
        fixture.cleanup()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--suite", action="store_true")
    args = parser.parse_args()
    root = args.repository.resolve()
    output = {"target": TARGET, "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "environment": {"platform": platform.platform(), "python": platform.python_version(),
                              "git": subprocess.check_output(["git", "--version"], text=True).strip()}, "checks": []}
    raw = subprocess.check_output(["git", "archive", "--format=tar", TARGET], cwd=root)
    with tempfile.TemporaryDirectory(prefix="aep round3 review ") as temporary:
        extracted = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            archive.extractall(extracted)
        module = module_at("round3_target_fixture", extracted / "tests/test_run_pipeline.py")
        prior = module_at("round2_reviewer", extracted / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
        old = module_at("round1_reviewer", extracted / "EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py")
        # Retarget only the review harness's source-record lookup; production
        # code, fixture milestone contracts and historical scenario inputs stay intact.
        prior.TARGET = TARGET
        if args.suite:
            for argv in [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_run_pipeline.py", "-v"],
                         [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                         [sys.executable, "scripts/validate_protocol.py"]]:
                result = subprocess.run(argv, cwd=extracted, text=True, capture_output=True, timeout=240,
                                        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                output["checks"].append({"argv": argv, "exit": result.returncode, "stdout": result.stdout,
                                         "stderr_tail": result.stderr.splitlines()[-5:]})
                assert result.returncode == 0, result.stdout + result.stderr
        output["round1_replays"] = [prior.replay(old, module, case, True) for case in prior.OLD_CASES]
        output["round2_replays"] = [prior.new_case(old, module, case) for case in prior.NEW_CASES]
        output["hostile_variants"] = [hostile(old, prior, module, case) for case in CASES]
        output["real_case"] = prior.real_case(root, module)
        output["summary"] = {
            group: {"cases": len(output[group]),
                    "requirement_violations": [row["case"] for row in output[group] if not row["requirement_met"]],
                    "all_refusals_preserve_files_and_state": all(row["refusal_no_mutation"] for row in output[group] if row["actual"] == "REFUSED"),
                    "all_bases_preserved": all(row["base_preserved"] for row in output[group])}
            for group in ("round1_replays", "round2_replays", "hostile_variants")
        }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
