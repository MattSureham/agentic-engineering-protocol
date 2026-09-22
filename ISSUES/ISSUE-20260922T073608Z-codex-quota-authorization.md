# Issue — Owner authorization for the minimal remaining Codex live run set

## Metadata

- **ID:** `ISSUE-20260922T073608Z-codex-quota-authorization`
- **Title:** Owner authorization gate for the minimal remaining Codex live conformance runs (attempt 3)
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `human:MattSureham`
- **Authority:** `HUMAN`
- **Review:** `SELF`
- **Created UTC:** `2026-09-22T07:36:08Z`
- **Updated UTC:** `2026-09-22T07:36:08Z`
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

Decision needed from the human technical owner: authorize the minimal run set below, or direct an alternative. No Codex live session will be launched until authorization is durably recorded here (owner reply persisted by the recorder into this issue's decision section and activity history).

### Minimal missing run set (awaiting authorization)

| Run | Purpose | Estimated sessions |
|---|---|---|
| `codex negative_collision` reruns | Obtain 1 evaluated PASS for the required collision case (bridges merged over pre-existing host instructions; `KEEP.txt` byte preservation; task completion with recorded verification) | 1–3 (cap 3; observed verification rate ≈ 3/7) |
| `codex adapter_removed_manual` reruns | Obtain 1 evaluated PASS for the required manual-fallback case (PROMPTS.md onboarding path; never counts as automatic activation) | 1–3 (cap 3) |

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

- **Blocked from:** `IMPLEMENTING` (milestone attempt 3)
- **Blocker:** Owner authorization for the minimal Codex run set above is not yet recorded.
- **Unblock owner:** `human:MattSureham`
- **Unblock condition:** The owner records an explicit decision here — authorize the minimal run set (or an amended bounded set), or direct an alternative disposition. On authorization, the recorder persists the decision in this section and the activity history before any launch.

## Residual uncertainty

- Quota window behavior is host-account-controlled; the next window's capacity is UNKNOWN until observed. The bounded batch is sized to fit one window based on the observed ~18-session capacity.
- Whether the owner prefers a different disposition (e.g., specification evolution for a bounded claim) is UNKNOWN until the decision is recorded.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-09-22T07:36:08Z` | `agent:ClaudeCode-discovery-fix-3` | `NONE` | `BLOCKED` | Recorded the owner's Codex quota directive, cancelled the scheduled 19:55 relaunch (no session launched from it), preserved all records, and documented the minimal remaining run set with per-run purpose and estimates. Milestone attempt 3 cannot reach review until Codex `negative_collision` and `adapter_removed_manual` have an evaluated PASS or the owner directs otherwise. |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is recorded (`NOT_APPLICABLE`) and no independent-review risk category applies to this record-keeping issue.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: the owner decision is pending and is the purpose of this issue.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue (NONE added).
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
