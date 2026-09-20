# Fixture Repository Bootstrap

This is the normative entry point for every participant in this repository. Read it completely before changing files. Repository records, not prior chat or the session prompt, must be sufficient to continue safely.

## Project truth

Resolve claims about intended behavior in this order:

1. `PROJECT_SPEC.md` (requirements and authorized tasks)
2. `HANDOFF.md` (current operational snapshot)
3. Participant inference

Only tasks explicitly authorized in `PROJECT_SPEC.md` may be implemented. An ordinary task request does not create scope.

## Start procedure

Before any implementation:

1. Read this file completely.
2. Read `PROJECT_SPEC.md` and `HANDOFF.md`.
3. Implement only an explicitly authorized task, then verify the result against the specification's acceptance text.
4. Record the outcome in `HANDOFF.md`: the completed task and the remaining next action.

If `PROJECT_SPEC.md` and `HANDOFF.md` conflict, stop and report the contradiction instead of choosing one. If no task is authorized, change nothing and report that state.
