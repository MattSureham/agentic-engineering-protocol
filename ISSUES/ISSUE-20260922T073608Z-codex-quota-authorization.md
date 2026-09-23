# Issue — Owner authorization for the minimal remaining Codex live run set

## Metadata

- **ID:** `ISSUE-20260922T073608Z-codex-quota-authorization`
- **Title:** Owner authorization gate for the minimal remaining Codex live conformance runs (attempt 3)
- **Status:** `OPEN`
- **Severity:** `HIGH`
- **Owner:** `human:MattSureham`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-09-22T07:36:08Z`
- **Updated UTC:** `2026-09-23T01:32:06Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `DISCOVERY-001`–`DISCOVERY-006`, discovery acceptance criteria 4–5
- **ADRs:** [ADR-20260918T064510Z](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md)
- **Evidence:** [attempt-3 live conformance](../EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md), [`attempt-3-quota-aborted/`](../EVIDENCE/discovery-conformance/attempt-3-quota-aborted/NOTE.md)
- **Milestone:** `milestone-20260918t064510z-prompt-independent-discovery-v1`

## Problem

The discovery milestone's accepted scope requires both harnesses, and acceptance criterion 5 prevents a support claim while a required case lacks passing coverage. After the second Codex account-quota exhaustion, two required Codex cases remain without an evaluated PASS (`UNVERIFIED`, single run each). On 2026-09-22 the human technical owner directed: cancel all scheduled Codex live-probe/rerun launches; do not auto-start new Codex CLI sessions after quota recovery; preserve every existing record (completed, `UNVERIFIED`, `FAIL`, quota-aborted) without deletion or overwriting reruns; document the minimal missing run set, per-run purpose, and estimated session count in durable records; and wait for explicit owner authorization before executing further Codex live runs.

## Evidence or reproduction

- Attempt-3 final matrix (uniform frozen-oracle re-evaluation, [`attempt-3-final/`](../EVIDENCE/discovery-conformance/attempt-3-final/)):
  - `codex negative_collision run1` — `UNVERIFIED`; sole gap: no recorded post-mutation verification read of `RESULT.txt`; otherwise conforming (result bytes exact, `KEEP.txt` intact, records updated, recovery reads established).
  - `codex adapter_removed_manual run1` — `UNVERIFIED`; sole gap: no recorded post-mutation verification read; otherwise conforming.
- Quota-aborted launches (fast exit-1 with the account usage-limit error, excluded from all claims): [`attempt-3-quota-aborted/`](../EVIDENCE/discovery-conformance/attempt-3-quota-aborted/) — 11 records across two exhaustion windows (resets observed at 14:50 and 19:50 local).

## Expected behavior

Both required cases produce at least one evaluated `PASS` under the frozen v3 oracle, completing Codex root-scope acceptance coverage — or the owner decides an alternative disposition (for example accepting UNVERIFIED coverage with a bounded claim amendment through specification evolution, which is a separate owner decision and is not proposed here).

## Assumptions

- **CONFIRMED:** The two cases lack only the recorded verification read; all other oracle obligations were met in run 1 of each (per-record `evaluation` fields).
- **CONFIRMED:** The owner's 2026-09-22 directive prohibits further Codex live launches without explicit authorization (recorded from the session instruction; this issue persists it durably).
- **INFERRED:** Observed Codex verification-discipline rate on completed positive-shape sessions is 3 PASS of 7 (`positive_root`); the same rate is a reasonable planning basis for the two outstanding cases.

## Investigation and decision

### Owner decision recorded 2026-09-23T01:32:06Z

Human technical owner `MattSureham` **authorized** the minimal run set with strict bounds (persisted from the owner's explicit direction; this entry is the durable record):

- **Scope:** only `codex negative_collision` and `codex adapter_removed_manual`.
- **Acceptance target:** one evaluated PASS per case under the current frozen oracle, then stop — no further repeats for a case once it passes.
- **Resource cap:** at most 6 new Codex live sessions total across both cases; on reaching the cap, stop immediately regardless of outcome and return to the human/review boundary.
- Quota exhaustion, infrastructure failure, timeout, or any run without a valid evaluated result must be preserved as evidence and must not trigger unbounded automatic retry.
- No increasing run counts for prettier pass rates, 3/3 repetition, or statistics.
- No scheduled wakeups, background auto-relaunch, or self-started Codex sessions after quota recovery.
- This decision does not change the two-harness requirement, acceptance criteria, support boundary, or any accepted specification.

**Second gate:** the owner explicitly deferred execution — no Codex live runs until the owner issues a distinct "execute the authorized Codex supplementary verification now" instruction. The budget above is armed, not consumed.

### Contract gap discovered at unblock (2026-09-23T01:32:06Z, agent:ClaudeCode-discovery-fix-3)

The accepted pipeline contract (ADR-20260814T015817Z decision 5, PROJECT_SPEC PIPELINE-003) defines entry into `BLOCKED_HUMAN_AUTHORITY` but no exit edge; `run_pipeline.py` refuses every transition out of it. Additionally, self-correction: the 2026-09-22 entry transition misapplied ROTATE-004 — quota exhaustion is a participant-failure class that MUST NOT produce `BLOCKED_HUMAN_AUTHORITY`; the human gate came from the owner's resource directive, which is now satisfied by the recorded decision above. The milestone's machine state remains `BLOCKED_HUMAN_AUTHORITY` because no contract-conformant exit exists; the state block is never hand-edited. Resolution is tracked in [ISSUE-20260923T013206Z-pipeline-blocked-exit](ISSUE-20260923T013206Z-pipeline-blocked-exit.md) and requires owner-approved contract evolution.

Total estimate: 2–6 Codex sessions in one bounded batch. Each rerun is a fresh isolated fixture copy launched by `tests/probe_discovery.py` with the frozen v3 oracle; every record, pass or fail, is retained. No other Codex runs are needed: `positive_root` has 3 evaluated PASS, `positive_subdir` remains unclaimed (writable-scope boundary, unchanged from attempt 2), and all other negatives and `adapter_removed_auto` (OBSERVE) are complete.

## Change

- **Files or components:** None yet — this issue records the gate. Authorized reruns would append records under `EVIDENCE/discovery-conformance/attempt-3-final/` only.
- **Behavior changed:** None.
- **Out-of-scope work deliberately excluded:** Any Codex launch beyond the two cases above; any change to acceptance criteria or support scope.
- **Rollback or recovery:** NOT APPLICABLE (no mutation performed).

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| NONE | — | — | — |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-09-22T07:36:08Z` | `agent:ClaudeCode-discovery-fix-3` | Uniform frozen-oracle re-evaluation of all 42 attempt-3 records (deterministic; no live sessions) | Both outstanding cases confirmed `UNVERIFIED` with the single verification-read gap; exit 0 | [attempt-3 evidence](../EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md) | Re-evaluation cannot substitute for the missing live PASS coverage |

## Pipeline state (optional)

NOT APPLICABLE.

## Self-review

- **Outcome:** `NOT_APPLICABLE` (this issue gates a human decision; it is not an implementation change).

## Independent review rounds

- **Required:** NO — this issue records an owner decision gate and launches no change. The milestone's own review requirements are unchanged and handled in ISSUE-20260918T064510Z.

## Blocker

- **Blocked from:** `IMPLEMENTING` (milestone attempt 3) — Codex live execution only; all non-Codex-quota work may proceed.
- **Blocker:** RESOLVED at the authority layer — the owner decision is recorded above (2026-09-23T01:32:06Z). Two gates remain before any launch: (1) the owner's distinct explicit "execute the authorized Codex supplementary verification now" instruction; (2) a contract-conformant machine exit from `BLOCKED_HUMAN_AUTHORITY`, tracked in [ISSUE-20260923T013206Z-pipeline-blocked-exit](ISSUE-20260923T013206Z-pipeline-blocked-exit.md).
- **Unblock owner:** `human:MattSureham`
- **Unblock condition:** SATISFIED for the authorization gate by the recorded owner decision. Execution unblocks only when the owner issues the explicit execution instruction; the machine-state gate unblocks per the contract-amendment decision in the linked issue.

## Residual uncertainty

- Quota window behavior is host-account-controlled; the next window's capacity is UNKNOWN until observed. The bounded batch is sized to fit one window based on the observed ~18-session capacity.
- When the owner will issue the explicit execution trigger is UNKNOWN by design — the decision defers execution.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-22T07:36:08Z` | `agent:ClaudeCode-discovery-fix-3` | `NONE` | `BLOCKED` | Recorded the owner's Codex quota directive, cancelled the scheduled 19:55 relaunch (no session launched from it), preserved all records, and documented the minimal remaining run set with per-run purpose and estimates. Milestone attempt 3 cannot reach review until Codex `negative_collision` and `adapter_removed_manual` have an evaluated PASS or the owner directs otherwise. |
| `2026-09-23T01:32:06Z` | `human:MattSureham` (recorded by `agent:ClaudeCode-discovery-fix-3`) | `BLOCKED` | `OPEN` | Owner granted the bounded authorization recorded in "Investigation and decision": the two named cases only, one evaluated PASS each then stop, at most 6 new Codex live sessions total, failures preserved without unbounded retry, no repetition inflation, no wakeups or auto-relaunch, no specification change. The owner explicitly deferred execution pending a distinct "execute now" instruction. Status moves `BLOCKED`→`OPEN` at the authority layer; the milestone's machine state remains `BLOCKED_HUMAN_AUTHORITY` pending the contract-conformant exit tracked in ISSUE-20260923T013206Z. No Codex session was launched and none is scheduled. |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is recorded (`NOT_APPLICABLE`) and no independent-review risk category applies to this record-keeping issue.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: the owner decision is recorded in "Investigation and decision" (2026-09-23T01:32:06Z); execution awaits the owner's explicit trigger.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (NONE added).
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
