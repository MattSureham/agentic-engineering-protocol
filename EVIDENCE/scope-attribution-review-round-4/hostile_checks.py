"""Reviewer-owned structured-authority adversarial CLI checks, frozen target.

PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-4/hostile_checks.py .
Only disposable local Git repositories mutate. No live probes or source transition.
"""
import json
import platform
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from reviewer_checks import TARGET, SHARED, module_at

BODY = "human:fixture-owner approved this separate authority record."
CASES = [
    "native_positive", "legacy_positive", "legacy_scope_widening", "legacy_pending_authority",
    "legacy_review_scope_widening", "legacy_review_open_findings", "legacy_review_negated_approval",
    "legacy_self_pending_anchor", "native_decision_prose_scope_conflict", "native_review_prose_scope_conflict",
    "native_independent_pending", "native_independent_unblock_pending", "native_independent_unblock_duplicate",
    "self_positive", "self_decision_declined", "self_unblock_denied", "duplicate_decision", "duplicate_review",
    "malicious_second_decision", "repeat_key", "unknown_key", "missing_key", "decision_pending", "decision_rejected",
    "decision_superseded", "boolean_count", "string_count", "decision_scope_gap", "review_scope_gap",
    "decision_missing_anchor", "decision_anchor_mismatch", "review_anchor_mismatch", "review_wrong_target",
    "review_identity_conflict", "post_review_substantive", "review_replaced_decision", "rename_scope_alias",
    "path_traversal", "path_dot_alias", "scope_directory", "fenced_decision_only", "fenced_review_only",
    "lookalike_only_marker", "duplicate_end_marker", "crlf_record", "unicode_marker_space",
    "invalid_utc", "legacy_block_after_tip", "native_anchor_outside_range", "native_partial_coverage",
]
POSITIVES = {"native_positive", "legacy_positive", "self_positive", "native_anchor_outside_range"}


def bounds(p, kind):
    return (p.DECISION_BLOCK_BEGIN, p.DECISION_BLOCK_END) if kind == "decision" else (p.REVIEW_BLOCK_BEGIN, p.REVIEW_BLOCK_END)


def extract_block(text, p, kind):
    begin, end = bounds(p, kind)
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    chunk = text[start:finish]
    return json.loads(chunk.split("```json\n", 1)[1].split("\n```", 1)[0]), chunk, start, finish


def replace_block(text, p, kind, block):
    _old, _chunk, start, finish = extract_block(text, p, kind)
    begin, end = bounds(p, kind)
    encoded = begin + "\n```json\n" + json.dumps(block, indent=2) + "\n```\n" + end
    return text[:start] + encoded + text[finish:]


def remove_block(text, p, kind):
    _block, _chunk, start, finish = extract_block(text, p, kind)
    return text[:start] + text[finish:]


def case_run(module, old, prior, case):
    fixture = module.PipelineRepository()
    p = module.pipeline
    own = case.startswith("self_") or case == "legacy_self_pending_anchor"
    legacy = case.startswith("legacy_")
    paths = [] if own else [SHARED]
    details = {}
    try:
        outside_anchor = None
        if case == "native_anchor_outside_range":
            fixture.write_intervening_issue(decision_scope=[SHARED])
            outside_anchor = fixture.commit("authority predates current attempt and range")
        fixture.begin()
        base = fixture.commit("record running attempt")
        issue = fixture.root / module.INTERVENING_ISSUE
        # Honest legacy scope is narrow; cases explicitly record when a later
        # migration asserts a broader scope than the historical owner/reviewer.
        scope = [] if own else [SHARED]
        if case in {"legacy_scope_widening", "legacy_review_scope_widening"}:
            paths.append("AGENTS.md")
            if case == "legacy_review_scope_widening":
                scope.append("AGENTS.md")
        fixture.write_intervening_issue(review="SELF" if own else "INDEPENDENT", decision_scope=scope)
        text = issue.read_text()
        if case == "legacy_scope_widening":
            text = text.replace(BODY, "human:fixture-owner approved ONLY OTHER/amendment.md. AGENTS.md is expressly NOT authorized.")
        if case in {"legacy_pending_authority", "legacy_self_pending_anchor"}:
            text = text.replace(BODY, "human:fixture-owner has NOT approved this request; authorization is pending.")
        if case == "native_decision_prose_scope_conflict":
            text = text.replace(BODY, "human:fixture-owner approved only this record. OTHER/amendment.md is expressly NOT authorized.")
        if case == "native_independent_pending":
            text = text.replace(BODY, "human:fixture-owner has NOT approved; substantive authorization is pending.")
        if case == "self_decision_declined":
            text = text.replace(BODY, "human:fixture-owner declined the request to mark this record approved.")
        if case == "native_independent_unblock_pending":
            text = text.replace("SATISFIED - owner decision recorded in this issue", "PENDING - owner decision is unresolved")
        if case == "self_unblock_denied":
            text = text.replace("SATISFIED - owner decision recorded in this issue", "SATISFIED - approval was denied")
        if case == "native_independent_unblock_duplicate":
            text += "\n- **Unblock condition:** `PENDING - authority unresolved`\n"
        decision, _chunk, _start, _end = extract_block(text, p, "decision")
        if case == "invalid_utc":
            decision["decided_utc"] = "2026-99-99T99:99:99Z"
            text = text.replace("2026-08-14T03:10:00Z", decision["decided_utc"])
            text = replace_block(text, p, "decision", decision)
        if legacy:
            text = remove_block(text, p, "decision")
        issue.write_text(text)
        anchor = outside_anchor or fixture.commit("separate owner record before substantive work")
        details["decision_anchor"] = anchor
        details["issue_at_decision_anchor"] = fixture.git("show", anchor + ":" + module.INTERVENING_ISSUE)
        if not own:
            for name in paths:
                old.put(fixture, name, "substantive bytes for " + name + "\n")
            reviewed = fixture.commit("substantive change after claimed authority")
            if case == "rename_scope_alias":
                fixture.git("mv", SHARED, "OTHER/renamed.md")
                paths.append("OTHER/renamed.md")
                reviewed = fixture.commit("rename without authorizing destination")
            fixture.add_intervening_review(reviewed, scope=paths)
            text = issue.read_text()
            if case in {"legacy_scope_widening", "legacy_review_scope_widening"}:
                text = text.replace("- **Reviewed immutable state:**", "- **Scope:** ONLY OTHER/amendment.md. AGENTS.md is NOT reviewed.\n- **Reviewed immutable state:**")
            if case == "native_review_prose_scope_conflict":
                text = text.replace("- **Reviewed immutable state:**", "- **Scope:** Record-only review; OTHER/amendment.md is expressly NOT reviewed.\n- **Reviewed immutable state:**")
            if case == "legacy_review_open_findings":
                text = text.replace("**0**.", "**1**.")
            if case == "legacy_review_negated_approval":
                text = text.replace("**APPROVED**.", "**CHANGES_REQUIRED**. NOT APPROVED.")
            review, _chunk, _start, _end = extract_block(text, p, "review")
            if legacy:
                text = remove_block(text, p, "review")
            issue.write_text(text)
            review_anchor = fixture.commit("record separate review")
            details["review_anchor"] = review_anchor
            details["issue_at_review_anchor"] = fixture.git("show", review_anchor + ":" + module.INTERVENING_ISSUE)
            tip = review_anchor
        else:
            reviewed = anchor
            review_anchor = None
            tip = anchor
        if legacy:
            # Recreate the machine projection only; no historical commit is
            # edited. Adverse cases intentionally assert facts absent at the
            # claimed historical anchors. The gate must detect the mismatch.
            original_text = issue.read_text()
            fixture.write_intervening_issue(review="SELF" if own else "INDEPENDENT", decision_scope=paths,
                                            decision_recorded=anchor)
            _decision, decision_chunk, _start, _end = extract_block(issue.read_text(), p, "decision")
            if not own:
                fixture.add_intervening_review(reviewed, scope=paths, recorded=review_anchor)
                _review, review_chunk, _start, _end = extract_block(issue.read_text(), p, "review")
            text = original_text.replace("\n## Independent review rounds", "\n" + decision_chunk + "\n\n## Independent review rounds", 1)
            if not own:
                text = text.replace("\n## Blocker", "\n" + review_chunk + "\n\n## Blocker", 1)
            if case in {"legacy_pending_authority", "legacy_self_pending_anchor"}:
                text = text.replace("human:fixture-owner has NOT approved this request; authorization is pending.", BODY)
            if case == "legacy_review_open_findings":
                text = text.replace("**1**.", "**0**.")
            if case == "legacy_review_negated_approval":
                text = text.replace("**CHANGES_REQUIRED**. NOT APPROVED.", "**APPROVED**.")
            issue.write_text(text)
            migrated_tip = fixture.commit("later machine migration claiming historical authority and acceptance")
            if case != "legacy_block_after_tip":
                tip = migrated_tip
        else:
            text = issue.read_text()
            decision, decision_chunk, _start, _end = extract_block(text, p, "decision")
            if not own:
                review, review_chunk, _start, _end = extract_block(text, p, "review")
            if case in {"duplicate_decision", "malicious_second_decision"}:
                if case == "malicious_second_decision":
                    decision_chunk = decision_chunk.replace('"EFFECTIVE"', '"SUPERSEDED"')
                text += "\n" + decision_chunk + "\n"
            elif case == "duplicate_review":
                text += "\n" + review_chunk + "\n"
            elif case == "repeat_key":
                text = text.replace('"state": "EFFECTIVE",', '"state": "PENDING", "state": "EFFECTIVE",', 1)
            elif case == "unknown_key":
                decision["ad_hoc_exception"] = True
                text = replace_block(text, p, "decision", decision)
            elif case == "missing_key":
                del decision["unblock"]
                text = replace_block(text, p, "decision", decision)
            elif case in {"decision_pending", "decision_rejected", "decision_superseded"}:
                decision["state"] = case.split("_", 1)[1].upper()
                text = replace_block(text, p, "decision", decision)
            elif case in {"boolean_count", "string_count"}:
                review["open_material_findings"] = False if case == "boolean_count" else "0"
                text = replace_block(text, p, "review", review)
            elif case in {"decision_scope_gap", "path_traversal", "path_dot_alias", "scope_directory", "decision_anchor_mismatch"}:
                decision["scope"] = {"decision_scope_gap": ["OTHER/elsewhere.md"], "path_traversal": ["OTHER/../AGENTS.md"],
                                     "path_dot_alias": ["./OTHER/amendment.md"], "scope_directory": ["OTHER/"],
                                     "decision_anchor_mismatch": [SHARED, "AGENTS.md"]}[case]
                text = replace_block(text, p, "decision", decision)
            elif case in {"review_scope_gap", "review_anchor_mismatch"}:
                review["scope"] = ["OTHER/elsewhere.md"] if case == "review_scope_gap" else [SHARED, "AGENTS.md"]
                text = replace_block(text, p, "review", review)
            elif case == "decision_missing_anchor":
                decision["recorded_commit"] = "f" * 40
                text = replace_block(text, p, "decision", decision)
            elif case == "review_wrong_target":
                review["target"] = anchor
                text = replace_block(text, p, "review", review)
            elif case == "review_identity_conflict":
                text = text.replace("agent:intervening-reviewer", "agent:implementor")
            elif case == "review_replaced_decision":
                decision["decision_id"] += "-replacement"
                text = replace_block(text, p, "decision", decision)
            elif case in {"fenced_decision_only", "fenced_review_only"}:
                kind = "decision" if case == "fenced_decision_only" else "review"
                _block, chunk, _start, _end = extract_block(text, p, kind)
                text = text.replace(chunk, "````markdown\n" + chunk + "\n````")
            elif case == "lookalike_only_marker":
                text = text.replace("AEP-AUTHORITY-DECISION-V1", "AEP-AUTHORITY-DECISION-VI")
            elif case == "duplicate_end_marker":
                text = text.replace(p.DECISION_BLOCK_END, p.DECISION_BLOCK_END + " " + p.DECISION_BLOCK_END)
            elif case == "unicode_marker_space":
                text = text.replace("<!-- AEP-AUTHORITY", "<!--\u00a0AEP-AUTHORITY")
            elif case == "crlf_record":
                text = text.replace("\n", "\r\n")
            if text != issue.read_text():
                issue.write_bytes(text.encode())
                tip = fixture.commit("reviewer adversarial record variant")
            if case in {"post_review_substantive", "native_partial_coverage"}:
                old.put(fixture, SHARED, "unreviewed substantive change\n")
                new_tip = fixture.commit("attempt touches separately scoped path after review")
                if case == "post_review_substantive":
                    tip = new_tip
        registry_entry = old.entry(module, base, tip)
        registry_entry["paths"] = paths
        fixture.add_registry([registry_entry])
        details.update({"registry_entry": registry_entry, "final_issue": issue.read_text(),
                        "commit_graph": fixture.git("log", "--format=%H %P %s", base + "..HEAD")})
        return old.finish(module, fixture, case, "ADVANCE" if case in POSITIVES else "REFUSE", details)
    finally:
        fixture.cleanup()


def main():
    root = Path(sys.argv[1]).resolve()
    prior = module_at("round4_hostile_prior", root / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
    output = {"target": TARGET, "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "environment": {"platform": platform.platform(), "python": platform.python_version()}, "cases": []}
    with tempfile.TemporaryDirectory(prefix="aep round4 hostile ") as temporary:
        module = prior.extract(root, TARGET, Path(temporary))
        old = module_at("round4_hostile_old", Path(temporary) / "EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py")
        for case in CASES:
            result = case_run(module, old, prior, case)
            if result["requirement_met"]:
                for field in ("issue_at_decision_anchor", "issue_at_review_anchor", "final_issue"):
                    result["details"].pop(field, None)
            output["cases"].append(result)
    output["summary"] = {"cases": len(output["cases"]),
                         "mismatches": [row["case"] for row in output["cases"] if not row["requirement_met"]],
                         "all_refusals_no_mutation": all(row["refusal_no_mutation"] for row in output["cases"] if row["actual"] == "REFUSED"),
                         "all_bases_preserved": all(row["base_preserved"] for row in output["cases"])}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
