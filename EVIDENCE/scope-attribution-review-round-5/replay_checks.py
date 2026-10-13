"""Replay retained reviewer scenarios against the immutable Round 5 target.

Only target-selection constants change; production and scenario code do not.
Run with . --baseline or . --hostile. Exit zero means completed, not approved.
"""
import importlib.util
import sys
from pathlib import Path

TARGET = "5bf73a0ab33bc851678c6adee30c45780d2bdb03"


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve()
    baseline = module_at("reviewer_checks", root / "EVIDENCE/scope-attribution-review-round-4/reviewer_checks.py")
    baseline.TARGET = TARGET
    sys.modules["reviewer_checks"] = baseline
    if sys.argv[2] == "--baseline":
        baseline.main()
    elif sys.argv[2] == "--hostile":
        hostile = module_at("round5_retained_hostile", root / "EVIDENCE/scope-attribution-review-round-4/hostile_checks.py")
        hostile.main()
    else:
        raise SystemExit("use --baseline or --hostile")
