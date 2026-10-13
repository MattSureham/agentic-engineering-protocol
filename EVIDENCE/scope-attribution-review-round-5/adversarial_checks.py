"""Independent Round 5 counterexamples. All submissions use disposable Git repos.

Run: PYTHONDONTWRITEBYTECODE=1 python3 <this-file> .
No production patch, allowlist widening, source transition, or live agent.
"""
import json
import platform
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from replay_checks import TARGET, module_at

SHARED = "OTHER/amendment.md"
BODY = "human:fixture-owner approved this separate authority record."
SATISFIED = "SATISFIED - owner decision recorded in this issue"
PENDING = "PENDING - awaiting owner approval"
CASES = [
    "native_positive", "legacy_positive",
    "legacy_only_scope_widening", "legacy_only_review_widening", "legacy_only_scope_merge",
    "native_only_scope_conflict", "native_anchor_pending_rewritten",
    "native_review_anchor_conflict_rewritten", "self_native_anchor_pending_rewritten",
    "self_legacy_unblock_rewritten", "self_native_unblock_rewritten",
    "self_current_not_authorized", "native_revocation_erased",
    "same_path_foreign_effect", "sibling_authority_control", "duplicate_structured_control",
]


def run_case(module, old, prior, helpers, case):
    fixture = module.PipelineRepository()
    p = module.pipeline
    own = case.startswith("self_")
    legacy = case.startswith("legacy_") or case == "self_legacy_unblock_rewritten"
    wide = case in {"legacy_only_scope_widening", "legacy_only_review_widening",
                    "legacy_only_scope_merge", "native_only_scope_conflict"}
    paths = [] if own else [SHARED] + (["AGENTS.md"] if wide else [])
    details = {}
    try:
        fixture.begin()
        base = fixture.commit("record running attempt")
        issue = fixture.root / module.INTERVENING_ISSUE
        if case == "sibling_authority_control":
            fixture.git("switch", "-c", "foreign-side")
            old.put(fixture, SHARED, "side work before authority\n")
            details["foreign_commit"] = fixture.commit("substantive side work without authority ancestor")
            fixture.git("switch", "main")
        fixture.write_intervening_issue(review="SELF" if own else "INDEPENDENT", decision_scope=paths)
        text = issue.read_text()
        if case in {"legacy_only_scope_widening", "legacy_only_scope_merge", "native_only_scope_conflict"}:
            text = text.replace(BODY, "human:fixture-owner approved ONLY OTHER/amendment.md.")
        if case in {"native_anchor_pending_rewritten", "self_native_anchor_pending_rewritten"}:
            text = text.replace(BODY, "human:fixture-owner has NOT approved this request; authorization is pending.")
        if case in {"self_legacy_unblock_rewritten", "self_native_unblock_rewritten"}:
            text = text.replace(SATISFIED, PENDING)
        if case == "self_current_not_authorized":
            text = text.replace(BODY, "human:fixture-owner has NOT authorized this authority record.")
        if case == "same_path_foreign_effect":
            text = text.replace(BODY, "human:fixture-owner approved ONLY the alpha spelling correction in OTHER/amendment.md.")
        decision, decision_chunk, _, _ = helpers.extract_block(text, p, "decision")
        if legacy:
            text = helpers.remove_block(text, p, "decision")
        issue.write_text(text)
        anchor = fixture.commit("record claimed authority before substantive work")
        details["decision_anchor"] = anchor
        details["issue_at_decision_anchor"] = fixture.git("show", anchor + ":" + module.INTERVENING_ISSUE)
        if case == "native_revocation_erased":
            revoked = dict(decision, state="REJECTED")
            issue.write_text(helpers.replace_block(text, p, "decision", revoked))
            details["revocation_commit"] = fixture.commit("record rejection of authority before work")
            details["revocation_record"] = issue.read_text()
            # No new owner/UTC/identity: resurrect the original now-rejected block.
            issue.write_text(text)
            fixture.commit("restore stale authority without a new decision")
        if case == "legacy_only_scope_merge":
            fixture.git("switch", "-c", "foreign-side")
            old.put(fixture, "AGENTS.md", "foreign branch work outside the only authorized file\n")
            details["foreign_commit"] = fixture.commit("foreign work after narrow authority")
            fixture.git("switch", "main")
        if not own:
            if case == "sibling_authority_control":
                fixture.git("merge", "--no-ff", "foreign-side", "-m", "merge sibling work")
                reviewed = fixture.git("rev-parse", "HEAD")
            else:
                for name in paths:
                    if case == "legacy_only_scope_merge" and name == "AGENTS.md":
                        continue
                    old.put(fixture, name, "authorized alpha spelling correction\n" if case == "same_path_foreign_effect" else "substantive " + name + "\n")
                reviewed = fixture.commit("substantive separate work")
            if case == "same_path_foreign_effect":
                details["authorized_change"] = reviewed
                old.put(fixture, SHARED, "unrelated beta behavior expansion\n")
                reviewed = fixture.commit("attempt-owned beta expansion after narrowly authorized alpha change")
                details["foreign_commit"] = reviewed
            if case == "legacy_only_scope_merge":
                fixture.git("merge", "--no-ff", "foreign-side", "-m", "merge unauthorized path into review target")
                reviewed = fixture.git("rev-parse", "HEAD")
            if case in {"legacy_only_scope_merge", "sibling_authority_control"}:
                details["merge_paths_explicit_parents"] = prior.explicit_parent_paths(fixture.root, reviewed)
                details["merge_paths_implementation"] = p._commit_paths(fixture.root, reviewed)
                assert details["merge_paths_explicit_parents"] == details["merge_paths_implementation"]
            fixture.add_intervening_review(reviewed, scope=paths)
            text = issue.read_text()
            if case == "legacy_only_review_widening":
                text = text.replace("- **Reviewed immutable state:**", "- **Scope:** ONLY OTHER/amendment.md.\n- **Reviewed immutable state:**")
            if case == "same_path_foreign_effect":
                text = text.replace("- **Reviewed immutable state:**", "- **Scope:** Only the alpha spelling correction. Commit " + reviewed + " is NOT reviewed.\n- **Reviewed immutable state:**")
            if case == "native_review_anchor_conflict_rewritten":
                text = text.replace("**0**.", "**1**.").replace("**APPROVED**.", "**CHANGES_REQUIRED**.")
            review, review_chunk, _, _ = helpers.extract_block(text, p, "review")
            if legacy:
                text = helpers.remove_block(text, p, "review")
            issue.write_text(text)
            review_anchor = fixture.commit("record review including its original narrative")
            details["review_anchor"] = review_anchor
            details["issue_at_review_anchor"] = fixture.git("show", review_anchor + ":" + module.INTERVENING_ISSUE)
            tip = review_anchor
        else:
            tip = anchor
        text = issue.read_text()
        if legacy:
            # Append projections, anchored to earlier prose; the old Git records remain.
            decision["recorded_commit"] = anchor
            decision_chunk = helpers.replace_block(decision_chunk, p, "decision", decision)
            text = text.replace("\n## Independent review rounds", "\n" + decision_chunk + "\n\n## Independent review rounds", 1)
            if not own:
                review["recorded_commit"] = review_anchor
                review_chunk = helpers.replace_block(review_chunk, p, "review", review)
                text = text.replace("\n## Blocker", "\n" + review_chunk + "\n\n## Blocker", 1)
        if case in {"native_anchor_pending_rewritten", "self_native_anchor_pending_rewritten"}:
            text = text.replace("human:fixture-owner has NOT approved this request; authorization is pending.", BODY)
        if case in {"self_legacy_unblock_rewritten", "self_native_unblock_rewritten"}:
            text = text.replace(PENDING, SATISFIED)
        if case == "native_review_anchor_conflict_rewritten":
            text = text.replace("**1**.", "**0**.").replace("**CHANGES_REQUIRED**.", "**APPROVED**.")
        if case == "duplicate_structured_control":
            conflicting = dict(decision, state="REJECTED")
            text += "\n" + helpers.replace_block(decision_chunk, p, "decision", conflicting) + "\n"
        if text != issue.read_text():
            issue.write_text(text)
            tip = fixture.commit("append migration or retrospectively alter current prose")
        entry = old.entry(module, base, tip)
        entry["paths"] = paths
        fixture.add_registry([entry])
        details.update({"registry_entry": entry, "final_issue": issue.read_text(),
                        "commit_graph": fixture.git("log", "--format=%H %P %s", base + "..HEAD")})
        return old.finish(module, fixture, case, "ADVANCE" if case in {"native_positive", "legacy_positive"} else "REFUSE", details)
    finally:
        fixture.cleanup()


def octopus_migrated(old, prior, module):
    """One explicit fixture-only positive calibration; no expected result changed.

    R2's original parenthesis literally names the claimed path in a negative
    clause. In the record-only octopus control there IS no earlier attempt
    change. Remove only that ambiguous parenthesis before its commit. The
    same negative clause still excludes AGENTS/other/earlier attempt work.
    """
    original = module.PipelineRepository.commit

    def commit(self, message):
        if message == "separate intervention limited to its recorded authority":
            issue = self.root / module.INTERVENING_ISSUE
            text = issue.read_text()
            before = "all earlier current-attempt changes (including any to OTHER/amendment.md)"
            assert before in text
            issue.write_text(text.replace(before, "all earlier current-attempt changes"))
        return original(self, message)

    module.PipelineRepository.commit = commit
    try:
        return prior.new_case(old, module, "octopus_record_only")
    finally:
        module.PipelineRepository.commit = original


def main():
    root = Path(sys.argv[1]).resolve()
    prior = module_at("round5_prior_loader", root / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
    output = {"target": TARGET, "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "environment": {"python": platform.python_version(), "platform": platform.platform()}, "cases": []}
    with tempfile.TemporaryDirectory(prefix="aep round5 adversarial ") as temporary:
        frozen = Path(temporary)
        module = prior.extract(root, TARGET, frozen)
        old = module_at("round5_old", frozen / "EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py")
        prior = module_at("round5_prior", frozen / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
        sys.modules["reviewer_checks"] = module_at("round5_four", frozen / "EVIDENCE/scope-attribution-review-round-4/reviewer_checks.py")
        helpers = module_at("round5_helpers", frozen / "EVIDENCE/scope-attribution-review-round-4/hostile_checks.py")
        for case in CASES:
            output["cases"].append(run_case(module, old, prior, helpers, case))
            print("completed " + case, file=sys.stderr, flush=True)
        output["octopus_fixture_calibration"] = octopus_migrated(old, prior, module)
    output["summary"] = {
        "cases": len(output["cases"]),
        "mismatches": [r["case"] for r in output["cases"] if not r["requirement_met"]],
        "all_refusals_no_mutation": all(r["refusal_no_mutation"] for r in output["cases"] if r["actual"] == "REFUSED"),
        "all_bases_preserved": all(r["base_preserved"] for r in output["cases"]),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
