#!/usr/bin/env python3
"""Emit the deterministic next-role decision for already-authorized milestone work.

This root-only helper is read-only: it loads the accepted milestone contract and
issue-embedded pipeline state through the accepted pipeline implementation and
prints exactly one next-role decision. It never advances, creates, or overrides
milestone state, never writes repository bytes, never uses the network, and
never launches or simulates launching a participant; host session invocation is
the documented manual adapter step recorded in ROLE_CONTRACTS.md. Identical
repository state produces byte-identical output with no timestamps or
environment data.
"""

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from run_pipeline import (
    Context,
    Milestone,
    PipelineError,
    ReviewRound,
    _load_context,
    _parse_latest_review,
    _selected,
)


DECISION_SCHEMA = "aep-dispatch-decision/v1"
ROLE_CONTRACTS_PATH = "ROLE_CONTRACTS.md"
HOST_ADAPTER = "manual"
ROLE_ANCHORS = {
    "implementer": "implementer",
    "independent-reviewer": "independent-reviewer",
    "recorder": "recorder-and-coordinator",
    "human-escalation": "human-escalation",
}

IMPLEMENTER_STATES = ("AUTHORIZED", "READY", "IN_PROGRESS", "CHANGES_REQUIRED")


def _transition_command(milestone_id: str, *extra: str) -> List[str]:
    return [
        "python3", "scripts/run_pipeline.py", "transition",
        "--milestone", milestone_id,
        "--actor", "<participant-label>",
    ] + list(extra)


def _decision(
    role: str,
    reason: str,
    eligibility: List[str],
    expected_records: List[str],
    expected_commands: List[List[str]],
    milestone: Optional[Milestone] = None,
    state: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "selected_milestone": milestone.milestone_id if milestone is not None else None,
        "state": state,
        "issue": milestone.issue if milestone is not None else None,
        "authority_digest": milestone.digest if milestone is not None else None,
        "role": role,
        "role_contract": "{}#{}".format(ROLE_CONTRACTS_PATH, ROLE_ANCHORS[role]) if role in ROLE_ANCHORS else None,
        "host_adapter": HOST_ADAPTER,
        "reason": reason,
        "eligibility": eligibility,
        "expected_records": expected_records,
        "expected_commands": expected_commands,
    }


def _implementer(milestone: Milestone, state: Dict[str, Any]) -> Dict[str, Any]:
    status = state["state"]
    milestone_id = milestone.milestone_id
    eligibility = [
        "Use one valid participant label; it becomes the implementor label of attempt {}.".format(state["attempt"] if status == "IN_PROGRESS" else state["attempt"] + 1),
        "The implementer may not review or record acceptance of the same attempt.",
    ]
    if status == "AUTHORIZED":
        return _decision(
            "implementer",
            "The selected milestone is authorized; an implementer records READY and begins the attempt.",
            eligibility,
            ["Record the AUTHORIZED to READY transition and commit the updated owning issue."],
            [_transition_command(milestone_id, "--to", "READY")],
            milestone, status,
        )
    if status == "READY":
        return _decision(
            "implementer",
            "The selected milestone is ready; an implementer begins attempt {} from the current immutable base.".format(state["attempt"] + 1),
            eligibility,
            ["Record the READY to IN_PROGRESS transition and commit the updated owning issue."],
            [_transition_command(milestone_id, "--to", "IN_PROGRESS")],
            milestone, status,
        )
    if status == "IN_PROGRESS":
        return _decision(
            "implementer",
            "Attempt {} is in progress under implementor label {}; the implementer finishes the allowed-paths work and submits a verified immutable target.".format(state["attempt"], state["implementor"]),
            [
                "Attempt {} is bound to implementor label {}; that participant continues it.".format(state["attempt"], state["implementor"]),
                "The implementer may not review or record acceptance of the same attempt.",
            ],
            [
                "Implement only within the milestone allowed paths.",
                "Commit the immutable target and record the IN_PROGRESS to AWAITING_PEER_REVIEW transition with passing verification evidence.",
                "Reconcile HANDOFF.md so it exposes exactly one next action for the independent reviewer.",
            ],
            [_transition_command(milestone_id, "--to", "AWAITING_PEER_REVIEW", "--target", "<full-immutable-target-revision>")],
            milestone, status,
        )
    return _decision(
        "implementer",
        "The latest independent review recorded open material findings; an implementer begins fix attempt {} within the authorized scope.".format(state["attempt"] + 1),
        eligibility,
        [
            "Record the CHANGES_REQUIRED to IN_PROGRESS transition for the new attempt.",
            "Resolve each open material finding of the latest review round within the authorized scope.",
            "Commit a new immutable target and resubmit to AWAITING_PEER_REVIEW.",
        ],
        [_transition_command(milestone_id, "--to", "IN_PROGRESS")],
        milestone, status,
    )


def _reviewer_round_work(milestone: Milestone, state: Dict[str, Any], reason: str) -> Dict[str, Any]:
    return _decision(
        "independent-reviewer",
        reason,
        [
            "The reviewer label must differ from the attempt implementor label {}.".format(state["implementor"]),
            "The reviewer must be independent of the authorship of the change under review.",
        ],
        [
            "Persist exactly one independent review round in the owning issue naming reviewed target {}, the open material findings count, and the disposition.".format(state["target_revision"]),
            "Reconcile HANDOFF.md so it exposes exactly one next action.",
        ],
        [],
        milestone, state["state"],
    )


def _awaiting_review(milestone: Milestone, issue_text: str, state: Dict[str, Any]) -> Dict[str, Any]:
    milestone_id = milestone.milestone_id
    try:
        latest: Optional[ReviewRound] = _parse_latest_review(issue_text, milestone.issue)
    except PipelineError:
        latest = None
    if latest is None:
        return _reviewer_round_work(
            milestone, state,
            "The verified target awaits independent review and no durable review round is recorded.",
        )
    if latest.target != state["target_revision"]:
        return _reviewer_round_work(
            milestone, state,
            "The latest review round covers a different revision than the verified target {}; a fresh independent round is required.".format(state["target_revision"]),
        )
    if latest.disposition == "APPROVED" and latest.material_findings == 0:
        return _decision(
            "recorder",
            "The latest independent review approved the verified target with zero open material findings; a recorder validates the acceptance gates and records ACCEPTED.",
            [
                "The recorder label must differ from the attempt implementor label {} and the approving reviewer label {}.".format(state["implementor"], latest.reviewer),
                "The recorder confirms acceptance preconditions from durable records and does not re-review or modify implementation.",
            ],
            [
                "Complete evidence-supported closure-checklist items in the owning issue.",
                "Record the AWAITING_PEER_REVIEW to ACCEPTED transition and reconcile the owning issue, HANDOFF.md, and HUMAN_CHECKPOINT.md.",
                "Publish with a normal non-force push and verify local, cached, and direct remote references are equal.",
            ],
            [_transition_command(milestone_id, "--to", "ACCEPTED")],
            milestone, state["state"],
        )
    if latest.disposition == "CHANGES_REQUIRED" and latest.material_findings >= 1:
        return _decision(
            "independent-reviewer",
            "The latest independent review recorded CHANGES_REQUIRED with open material findings; the reviewer completes the role by recording the matching transition.",
            [
                "The reviewer label must differ from the attempt implementor label {}.".format(state["implementor"]),
                "The reviewer must be independent of the authorship of the change under review.",
            ],
            [
                "Record the AWAITING_PEER_REVIEW to CHANGES_REQUIRED transition matching the persisted round.",
                "Reconcile HANDOFF.md so it exposes exactly one next action for the implementer's fix attempt.",
            ],
            [_transition_command(milestone_id, "--to", "CHANGES_REQUIRED")],
            milestone, state["state"],
        )
    if latest.disposition == "BLOCKED":
        return _decision(
            "human-escalation",
            "The latest independent review recorded disposition BLOCKED; existing repository authority is insufficient and human escalation is required.",
            [
                "Any participant may record the blocker issue and the BLOCKED_HUMAN_AUTHORITY transition.",
                "Only the human technical owner can supply the missing authority.",
            ],
            [
                "Persist a linked BLOCKED issue stating the blocker, unblock owner, and unblock condition.",
                "Record the BLOCKED_HUMAN_AUTHORITY transition with --blocker-issue.",
                "The human technical owner records the unblock decision through specification evolution or explicit owner direction.",
            ],
            [_transition_command(milestone_id, "--to", "BLOCKED_HUMAN_AUTHORITY", "--blocker-issue", "<linked-blocker-issue-path>")],
            milestone, state["state"],
        )
    return _reviewer_round_work(
        milestone, state,
        "The latest review round is not a terminal disposition the pipeline can consume; a fresh independent round is required.",
    )


def decide(context: Context) -> Dict[str, Any]:
    selected = _selected(context)
    if selected is None:
        return _decision(
            "none",
            "No authorized milestone with satisfied dependencies awaits work; the repository is in its terminal wait state.",
            [],
            ["No participant action; new work requires an explicit owner direction recorded through specification evolution."],
            [],
        )
    milestone = next(item for item in context.milestones if item.milestone_id == selected)
    state = context.states[selected]
    status = state["state"]
    if status in IMPLEMENTER_STATES:
        return _implementer(milestone, state)
    if status == "AWAITING_PEER_REVIEW":
        return _awaiting_review(milestone, context.issue_texts[selected], state)
    return _decision(
        "human-escalation",
        "The selected milestone is blocked on human authority; the linked blocker issue defines the unblock condition.",
        [
            "Any participant may record the blocker issue and the BLOCKED_HUMAN_AUTHORITY transition.",
            "Only the human technical owner can supply the missing authority.",
        ],
        ["The human technical owner records the unblock decision through specification evolution or explicit owner direction."],
        [],
        milestone, status,
    )


def render_human(decision: Dict[str, Any]) -> str:
    lines = [
        "ROLE {}".format(decision["role"]),
        "MILESTONE {}".format(decision["selected_milestone"] or "NONE"),
        "STATE {}".format(decision["state"] or "NONE"),
        "ISSUE {}".format(decision["issue"] or "NONE"),
        "ROLE_CONTRACT {}".format(decision["role_contract"] or "NONE"),
        "HOST_ADAPTER {}".format(decision["host_adapter"]),
        "REASON {}".format(decision["reason"]),
        "ELIGIBILITY",
    ]
    lines.extend("- {}".format(item) for item in decision["eligibility"] or ["NONE"])
    lines.append("EXPECTED_RECORDS")
    lines.extend("- {}".format(item) for item in decision["expected_records"] or ["NONE"])
    lines.append("EXPECTED_COMMANDS")
    lines.extend(
        "- {}".format(shlex.join(command)) for command in decision["expected_commands"] or [["NONE"]]
    )
    return "\n".join(lines) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit the deterministic next-role decision for already-authorized milestone work (read-only).",
    )
    parser.add_argument("--root", default=None, help="repository root (default: parent of this script)")
    parser.add_argument("--json", action="store_true", help="emit canonical JSON")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _build_parser().parse_args(argv)
    root = Path(arguments.root) if arguments.root is not None else Path(__file__).resolve().parent.parent
    try:
        context = _load_context(root)
        decision = decide(context)
    except PipelineError as error:
        print(error.render(), file=sys.stderr)
        print("SUMMARY dispatched=0 errors=1", file=sys.stderr)
        return error.exit_code
    except Exception as error:  # Defensive boundary: do not expose an unstable traceback as API.
        print("ERROR AEP-DISPATCH-INTERNAL command: {}: {}".format(type(error).__name__, error), file=sys.stderr)
        print("SUMMARY dispatched=0 errors=1", file=sys.stderr)
        return 2
    if arguments.json:
        sys.stdout.write(json.dumps(decision, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        sys.stdout.write(render_human(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
