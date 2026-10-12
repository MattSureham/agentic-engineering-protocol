"""Offline frozen-target review; only disposable fixture repositories mutate.

PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-4/reviewer_checks.py . --baseline
Exit zero means reproduction completed, not conformance. No live probes.
"""
import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import importlib.util

TARGET = "d9bd6d806e0f1160df4b6893154017e9d287cc4e"
SHARED = "OTHER/amendment.md"


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def adapted_replay(old, prior, module, case):
    """Preserve the scenario, add only the required explicit authority record.

    The prior adapter suppressed ALL INDEPENDENT owner decisions. For this
    architecture, supply the fixture's strict scoped decision except in the
    scenario explicitly about an absent SELF decision. No production patch.
    """
    original_entry = old.entry
    original_write = module.PipelineRepository.write_intervening_issue
    if case == "null_registry_in_scope":
        return prior.replay(old, module, case, True)

    def entry(m, base, tip, issue=None):
        value = original_entry(m, base, tip, issue)
        value["paths"] = ([] if case in {"positive_self", "self_awaiting_decision", "self_substantive"}
                          else ["AGENTS.md"] if case == "same_issue_registry"
                          else ["OTHER/second.md"] if issue and issue != m.INTERVENING_ISSUE
                          else [SHARED])
        return value

    def write(self, *args, **kwargs):
        kwargs["decision"] = case != "self_awaiting_decision"
        kwargs["decision_scope"] = [] if kwargs.get("review") == "SELF" else [SHARED]
        return original_write(self, *args, **kwargs)

    old.entry = entry
    module.PipelineRepository.write_intervening_issue = write
    try:
        return old.reproduction(module, case)
    finally:
        old.entry = original_entry
        module.PipelineRepository.write_intervening_issue = original_write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    root = args.repository.resolve()
    prior = module_at("round4_prior", root / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
    output = {"target": TARGET, "captured_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "environment": {"platform": platform.platform(), "python": platform.python_version(),
                              "git": prior.git(root, "--version")}, "checks": []}
    with tempfile.TemporaryDirectory(prefix="aep round4 independent review ") as temporary:
        extracted = Path(temporary)
        module = prior.extract(root, TARGET, extracted)
        old = module_at("round4_old", extracted / "EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py")
        prior = module_at("round4_frozen_prior", extracted / "EVIDENCE/scope-attribution-review-round-2/reviewer_checks.py")
        third = module_at("round4_third", extracted / "EVIDENCE/scope-attribution-review-round-3/reviewer_checks.py")
        prior.TARGET = TARGET
        if args.baseline:
            for argv in [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_run_pipeline.py", "-v"],
                         [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                         [sys.executable, "scripts/validate_protocol.py"]]:
                result = subprocess.run(argv, cwd=extracted, text=True, capture_output=True, timeout=300,
                                        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                output["checks"].append({"argv": argv, "exit": result.returncode, "stdout": result.stdout,
                                         "stderr_tail": result.stderr.splitlines()[-8:]})
                print("completed: " + " ".join(argv[1:]) + "; exit=" + str(result.returncode), file=sys.stderr, flush=True)
            output["round1_unadapted"] = [prior.replay(old, module, case, True) for case in prior.OLD_CASES]
            output["round1_migrated"] = [adapted_replay(old, prior, module, case) for case in prior.OLD_CASES]
            output["round2_replays"] = [prior.new_case(old, module, case) for case in prior.NEW_CASES]
            output["round3_replays"] = [third.hostile(old, prior, module, case) for case in third.CASES]
            output["real_case"] = prior.real_case(root, module)
    output["summary"] = {
        group: {"cases": len(rows), "advances": sum(row["actual"] == "ADVANCED" for row in rows),
                "requirement_mismatches": [row["case"] for row in rows if not row["requirement_met"]],
                "all_refusals_no_mutation": all(row["refusal_no_mutation"] for row in rows if row["actual"] == "REFUSED"),
                "all_bases_preserved": all(row["base_preserved"] for row in rows)}
        for group, rows in output.items() if group.startswith("round")
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
