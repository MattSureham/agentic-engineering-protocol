# Live Participant Invocation Capability

## Metadata

- **ID:** `ISSUE-20260817T021218Z-live-invocation`
- **Title:** Implement the authorized live participant invocation capability milestone
- **Status:** `REVIEW`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-17T02:12:18Z`
- **Updated UTC:** `2026-08-17T03:27:54Z`
- **Requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Product-level autonomy objective, Live invocation and autonomy demonstration phase (`LIVE-001`–`LIVE-004`), and `MILESTONE-20260817T021218Z-live-invocation-v1`
- **ADRs:** [`ADR-20260817T021218Z-autonomy-end-state`](../ADR/ADR-20260817T021218Z-autonomy-end-state.md); [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md)
- **Evidence:** [`EVIDENCE-20260814T092504Z-host-capability-probe`](../EVIDENCE/EVIDENCE-20260814T092504Z-host-capability-probe.md) (original launch-interface probes); [`EVIDENCE-20260817T023721Z-live-profile-probe`](../EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md) (minimal tool-enabled profile and headless permission behavior)
- **Milestone:** `MILESTONE-20260817T021218Z-live-invocation-v1`

Primary states are `OPEN`, `INVESTIGATING`, `IMPLEMENTING`, `VERIFYING`, `REVIEW`, and `CLOSED`. `BLOCKED` records a temporary side state. Code written is not closure.

## Problem

The accepted rotation runner has never launched a real participant: the committed registry pins `tools` to the originally probed empty value, which cannot perform file-editing roles, and headless permission behavior with a widened tool set is unprobed. The product-level autonomy objective requires real unattended operation, so the minimal tool-enabled launch profile must be established by evidence and the adapter conformed to it before the autonomy demonstration can run.

## Evidence or reproduction

- **CONFIRMED:** [`ROTATION_PARTICIPANTS.json`](../ROTATION_PARTICIPANTS.json) at rotation target `d6471f54b7e75f255b308d44885146762642b261` declares `tools: ""` for all participants; the original probe evidence probed only that profile.
- **CONFIRMED:** The rotation review round 1 (`2026-08-17T01:40:05Z`, `APPROVED`) recorded that live runner invocation was deliberately unexercised and that prompt-wording adequacy for real work is unverified.
- **CONFIRMED:** The owner direction of `2026-08-17T02:12:18Z` authorizes this milestone as the capability predecessor of the gated autonomy demonstration.

## Expected behavior

Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `LIVE-001`–`LIVE-004` define the expected result: recorded probe evidence for the minimal tool-enabled headless profile (including permission behavior), runner/registry/role-contract conformance to that verified profile, stub-only tests preserved, and fail-closed classification of anything outside the verified profile. Compatible architecture is recorded in [`ADR-20260817T021218Z-autonomy-end-state`](../ADR/ADR-20260817T021218Z-autonomy-end-state.md).

## Assumptions

- **CONFIRMED:** The accepted runner's launcher is stub-injectable and flag-driven; conforming it to a verified widened profile is a bounded change within the allowed paths.
- **CONFIRMED:** The reusable ten-file package is out of scope; all changes are root-only.
- **INFERRED:** The minimal profile includes file read/edit, shell execution for checks and Git, and no network tools beyond what the host session itself manages. Facts: role contracts require reading, editing within allowed paths, running checks, committing, and recording transitions; the demonstration milestone needs exactly those.
- **CONFIRMED:** Headless permission behavior with tools enabled is probed and machine-readable: denial arrives as a success-shaped envelope with a non-empty `permission_denials` array and absent work product ([`EVIDENCE-20260817T023721Z-live-profile-probe`](../EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md)).
- **UNKNOWN:** Long-running session stability, rate limits, envelope stability across CLI versions, and any tool outside the four probed. Resolution path: anything unprobed stays prohibited and fails closed.

## Investigation and decision

The owner direction is recorded through specification evolution and summarized in [`HUMAN_CHECKPOINT.md`](../HUMAN_CHECKPOINT.md). The execution architecture is decided in the accepted ADR: probe before reliance, minimal verified profile, adapter conformance, fail-closed continuity. No further product or architecture question is open.

## Change

- **Files or components:** New probe evidence under `EVIDENCE/`; `scripts/run_rotation.py`; `tests/test_run_rotation.py`; `ROTATION_PARTICIPANTS.json`; `ROLE_CONTRACTS.md`; `README.md`; this issue; `HANDOFF.md`; `HUMAN_CHECKPOINT.md`.
- **Behavior changed:** Real launches use the minimal probe-verified tool-enabled profile (`--tools "Read,Edit,Write,Bash"` with the matching `--allowedTools` grant, registry schema `rotation-participants/v2`); the failure taxonomy gains the probed `permission_denied` participant-failure class; the stub-only test suite is preserved and extended to the profile handling and denial shapes.
- **Out-of-scope work deliberately excluded:** The autonomy demonstration itself (milestone 5); changes to the accepted pipeline or dispatcher tools; the reusable package; any unprobed capability; the four still-`BLOCKED` capability deferrals.
- **Rollback or recovery:** Revert the immutable target while preserving the owner direction, accepted specification/ADR records, and probe evidence.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Widened probed launch surface | Real roles require file and shell capability | New probe evidence plus stub-suite conformance tests | Cross-version envelope stability and rate limits remain `UNKNOWN` |
| Live-profile conformance edits to the accepted runner | Real launches must use the verified profile | Stub-launcher tests covering the profile handling | Semantic adequacy of any prompt changes remains reviewer judgment |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-17T02:12:18Z` | `ClaudeCode/root` | Authority-boundary recording only: parsed the updated five-milestone contract with the accepted pipeline parser; verified milestones 1–3 digests unchanged and milestone 4 digest computed | Contract parses; milestone-1 `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4`, milestone-2 `afe725805d919f850e7d44017a2b4b63ba6b0f3453ec6bea84ece1ee265b638c`, milestone-3 `a38bb7bfd1511045e8e09b4a0dc6af7893f24a8a833e9a3faa444660cc3b977b` unchanged; milestone-4 digest `36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea` | This issue and the accepted specification/ADR | No implementation exists yet; deterministic verification begins with the first attempt |
| `2026-08-17T02:37:21Z` | `agent:ClaudeCode-live` | Five live headless probes in `/tmp/aep-live-probe` (read without grant; edit+shell without grant; edit+shell with grant; write with grant; budget exhaustion under the widened profile), all with `--max-budget-usd` caps, zero-byte stderr, and on-disk side-effect checks | Read without grant: exit `0`, `subtype: success`, `permission_denials: []`; edit+shell without grant: exit `0`, `subtype: success`, **`permission_denials` non-empty, fixture unchanged** (silent denial, machine-readable only via the field); edit+shell with grant: exit `0`, denials empty, fixture edited and `wc` output returned; write with grant: exit `0`, `created.txt` created; budget probe: exit `1`, `subtype: error_max_budget_usd`, `is_error: true` | [`EVIDENCE-20260817T023721Z-live-profile-probe`](../EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md) | Single host, single CLI version `2.1.118`; long-running stability, `--resume` under the widened profile, and rate limits unprobed; total probe spend under $0.15 |
| `2026-08-17T02:45:09Z` | `agent:ClaudeCode-live` | `python3 -m unittest discover -s tests -v` | 97 tests `OK` (89 retained pipeline/structural/dispatch/rotation tests plus 8 new live-profile conformance tests), exit `0` | `tests/test_run_rotation.py` and this row | Stub launcher only; no real session launched by the suite; recorded Darwin/Python 3.9 environment |
| `2026-08-17T02:45:09Z` | `agent:ClaudeCode-live` | `python3 scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)`, exit `0` | Inline | Structural invariants only |
| `2026-08-17T02:45:09Z` | `agent:ClaudeCode-live` | `LIVE-001`–`LIVE-004` conformance: probe-before-reliance evidence recorded for every relied-upon behavior; minimal profile (`Read,Edit,Write,Bash` + matching grant, no network tool, no permission-mode flags) pinned in registry v2; launcher emits `--allowedTools` only when non-empty (stub-captured argv tests); classifier maps non-empty `permission_denials` to the new `permission_denied` participant failure and malformed denial fields to `session_error`; budget class re-probed unchanged; suite remains stub-only (ROTATE-008 unchanged); no live runner invocation against this repository | Each requirement maps to probe evidence or stub-suite tests; denial shapes never produce a `BLOCKED_HUMAN_AUTHORITY` transition; v1 registries and unrecognized envelope fields fail closed | `tests/test_run_rotation.py` (8 new tests), [`EVIDENCE-20260817T023721Z-live-profile-probe`](../EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md) | Live runner operation begins only with milestone 5's demonstration; semantic adequacy of the profile for real role work is demonstrated there, not here |

- **Pipeline verification `2026-08-17T02:51:24Z`:** [`EVIDENCE/EVIDENCE-20260817T025124Z-milestone-20260817t021218z-live-invocation-v1-attempt-1.json`](../EVIDENCE/EVIDENCE-20260817T025124Z-milestone-20260817t021218z-live-invocation-v1-attempt-1.json) — deterministic structural and accepted-command gates passed for `83838e0b1a579f13706b4728da3c3219ed73a8e9`.

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260817T021218Z-live-invocation-v1",
  "authority_digest": "36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea",
  "state": "AWAITING_PEER_REVIEW",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-live",
  "base_revision": "8b1c13269f12df583a98f09c74bcc185143999a8",
  "target_revision": "83838e0b1a579f13706b4728da3c3219ed73a8e9",
  "verification_evidence": [
    "EVIDENCE/EVIDENCE-20260817T025124Z-milestone-20260817t021218z-live-invocation-v1-attempt-1.json"
  ],
  "review_references": [],
  "events": [
    {
      "sequence": 1,
      "utc": "2026-08-17T02:12:18Z",
      "actor": "human:MattSureham",
      "from": null,
      "to": "AUTHORIZED",
      "reason": "Explicit product-level autonomy owner direction accepted through specification evolution with a compatible accepted ADR."
    },
    {
      "sequence": 2,
      "utc": "2026-08-17T02:31:39Z",
      "actor": "agent:ClaudeCode-live",
      "from": "AUTHORIZED",
      "to": "READY",
      "reason": "Validated transition AUTHORIZED to READY."
    },
    {
      "sequence": 3,
      "utc": "2026-08-17T02:31:47Z",
      "actor": "agent:ClaudeCode-live",
      "from": "READY",
      "to": "IN_PROGRESS",
      "reason": "Implementation attempt 1 began from immutable base 8b1c13269f12df583a98f09c74bcc185143999a8."
    },
    {
      "sequence": 4,
      "utc": "2026-08-17T02:51:24Z",
      "actor": "agent:ClaudeCode-live",
      "from": "IN_PROGRESS",
      "to": "AWAITING_PEER_REVIEW",
      "reason": "Immutable target 83838e0b1a579f13706b4728da3c3219ed73a8e9 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260817T025124Z-milestone-20260817t021218z-live-invocation-v1-attempt-1.json."
    }
  ]
}
```
<!-- AEP-PIPELINE-STATE-V1:END -->

## Self-review

- **Participant:** `ClaudeCode/root`
- **Reviewed UTC:** `2026-08-17T02:12:18Z`
- **Reviewed repository state:** Authority-boundary records only; synchronized baseline `ffdd275e70798318cdbfb74f13f1cb864ea65924` plus the records created by this phase
- **Scope and authority references:** Root `PROJECT_SPEC.md` autonomy objective and live-invocation requirements, accepted ADR; no implementation exists
- **Checks and evidence reviewed:** Contract digest parse (row above)
- **Findings and corrections:** NONE
- **Limitations:** No implementation to review; this self-review covers authority-recording consistency only
- **Residual risks:** NONE beyond the declared UNKNOWNs
- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES` — the milestone widens the probed launch surface that acts on authority-bound state.

### 2026-08-17T03:27:54Z — ClaudeCode/live-review

- **Reviewed repository state:** Clean synchronized `9e7bb9aaab1d7003e25e087e4e5d7a3710f3b122` (local HEAD, cached `origin/main`, and direct remote `refs/heads/main` equal); dispatcher routing to `independent-reviewer` for `AWAITING_PEER_REVIEW` milestone 4 with implementor-exclusion eligibility; read-only `git archive` extraction of the target at `/tmp/aep-review-live`.
- **Reviewed target:** `83838e0b1a579f13706b4728da3c3219ed73a8e9`
- **Open material findings:** `0`
- **Scope:** Accepted Live invocation and autonomy demonstration phase (`LIVE-001`–`LIVE-004`, milestone-4 contract) in root `PROJECT_SPEC.md`; accepted [`ADR-20260817T021218Z-autonomy-end-state`](../ADR/ADR-20260817T021218Z-autonomy-end-state.md) and [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md); the new probe record [`EVIDENCE-20260817T023721Z-live-profile-probe`](../EVIDENCE/EVIDENCE-20260817T023721Z-live-profile-probe.md); the original probe record and its surviving raw envelopes at `/tmp/aep-host-probe`; the complete base→target diff (`EVIDENCE/`, `scripts/run_rotation.py`, `tests/test_run_rotation.py`, `ROTATION_PARTICIPANTS.json`, `ROLE_CONTRACTS.md`, `README.md`, this issue, `HANDOFF.md`); the generated submission evidence; the post-target record range.
- **Commands or procedures:** `git log/diff/diff --check/merge-base/ls-tree` over `8b1c13269f12df583a98f09c74bcc185143999a8..83838e0b1a579f13706b4728da3c3219ed73a8e9` and the post-target range; `git archive` extraction then `python3 -m unittest discover -s tests` (97 tests `OK`) and `python3 scripts/validate_protocol.py` (`PASS`) at the extraction; all five milestone digests recomputed at the target with the accepted pipeline parser (milestone 4 `36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea`, milestones 1–3 and 5 unchanged); an independent eight-scenario adverse harness (`/tmp/aep_live_adverse.py`, run against the extraction, `TOTAL 8 FAILED 0`): A1 every real dispatcher decision across `AUTHORIZED`/`READY`/`IN_PROGRESS`/`AWAITING_PEER_REVIEW` fed through the target's `parse_constraints`/`select_participant` with the committed v2 registry, including a fixture whose bound implementor is registry participant `agent:rotation-alpha` (bound-decision selection is exactly that participant; reviewer selection excludes it, leaving beta/gamma); A2 the three surviving raw captured envelopes from the original probe (`/tmp/aep-host-probe/*.json`) classified by the target code — `success`, `quota_exhausted`, `success`, identical to the accepted rotation behavior; A3 the five envelope shapes recorded by the new probe evidence reconstructed and classified — empty `permission_denials` success, non-empty denials → `permission_denied`, widened-profile budget exhaustion → `quota_exhausted`; A4 deceptive and malformed denial shapes — `permission_denials` as object or string fails closed to `session_error`, non-empty denials with exit `1` classify `permission_denied` (never success), unrecognized subtype with empty denials fails closed to `session_error`; A5 real `default_launch` argv captured through monkeypatched `subprocess.run` — the committed profile yields exactly `claude -p <prompt> --output-format json --tools Read,Edit,Write,Bash --max-budget-usd 1.0 --allowedTools Read,Edit,Write,Bash` with the registry timeout, a participant-level `allowed_tools` override wins, and an empty `allowed_tools` omits the flag entirely (the originally probed `tools ""` profile preserved); A6 registry validation — committed v2 loads; v1 schema, an extra default key, a missing or non-string `allowed_tools`, a participant unknown key, and a non-string participant `allowed_tools` all raise `AEP-ROTATE-SCHEMA`; A7 end-to-end on a real fixture repository (ledger path added to its contract) with the real dispatcher binary and a stub participant whose first envelope is the probed denial shape and whose second performs the real emitted transitions — outcomes `permission_denied` then `success_advancing` with rotation from p1 to p2, no `BLOCKED` anywhere in the ledger, bounded `steps_exhausted` stop; A8 crash after the participant's transition landed but before the outcome append recovers as `success_advancing` with no duplicate transition.
- **Specification compliance:** `LIVE-001` (probe before reliance — the widened profile is relied upon only after the recorded five-probe evidence with exact commands, exit codes, envelope fields, and on-disk side-effect checks; the runner's only new reliance, `--allowedTools` plus the denial field, is exactly what was probed), `LIVE-002` (minimal verified profile — `Read,Edit,Write,Bash` with the matching grant covers the role contracts' read/edit/write/checks/Git/transition needs; no network tool; no `--permission-mode` or `--dangerously-skip-permissions`; ambient-permission dependence explicitly rejected by the evidence), `LIVE-003` (adapter conformance — launcher emits exactly the probed flags with `--allowedTools` only when non-empty (A5); registry v2 pins the verified profile; role contracts and README conformed; the suite remains stub-only — the launcher tests monkeypatch `subprocess.run` and the CLI test launches nothing, ROTATE-008 unchanged), `LIVE-004` (fail-closed continuity — malformed denial fields and unrecognized subtypes classify `session_error` (A4); denial shapes are participant failures with bounded retry/rotation and never approach `BLOCKED_HUMAN_AUTHORITY` (A7); v1 registries and unknown keys are rejected (A6); no new escalation path exists). The milestone-4 contract's allowed-paths scope holds: the base→target diff touches exactly the eight recorded paths, all inside the contract; the reusable package, pipeline, and dispatcher are untouched.
- **Correctness and regression findings:** None. The extracted-target suite passes 97 tests (89 retained plus 8 new); the structural validator passes; digests, base ancestry (target parent `62bc403` is the `IN_PROGRESS` record, base `8b1c132` an ancestor, matching the accepted pattern), and record-only post-target drift (generated evidence JSON, HANDOFF, owning issue) all reproduce; the originally probed envelope classes classify byte-identically under the new code (A2); `git diff --check` is clean and the target tree contains no `.DS_Store`.
- **Architecture and complexity findings:** None material. The runner adds no state machine, no second authority source, and no new launch-surface reliance beyond the probe record; the classifier's denial precedence (denials checked before the success shape) is the fail-safe direction; the registry schema bump to v2 with exact-key validation preserves the fail-closed boundary.
- **Material findings and resolution conditions:** `NONE`.
- **Limitations:** Review ran on Darwin/Python 3.9.6 only; the new probe's raw envelope bytes were session-scoped and are not preserved (the record quotes exact commands, exit codes, and the salient fields — the salient classification behavior is independently reproduced in A3, and the original probe's surviving raw envelopes reproduce in A2); live runner invocation against this repository remains deliberately unexercised (operational use, milestone 5); long-running stability, rate limits, cross-version envelope stability, other authentication modes, and `--resume` under the widened profile remain unprobed as recorded.
- **Residual risks:** (1) Classification-preference observation (non-material): an unrecognized error subtype carrying a non-empty `permission_denials` array classifies `permission_denied` rather than `session_error` (A4 observed); both are non-escalating participant failures with bounded retry, so the direction is safe. (2) Denial-list elements are not individually shape-validated (a non-empty list of arbitrary values classifies `permission_denied`); the failure direction is again safe. (3) Ledger appends dirty the worktree between launches, so launched participants must commit the ledger before pipeline transitions (documented in `ROLE_CONTRACTS.md`); the pipeline gate fails closed otherwise, and milestone 5's contract correctly includes the ledger in its allowed paths while milestone 4's correctly does not. (4) Semantic sufficiency of the minimal profile for real role work is demonstrated by milestone 5's gated run, not here, as the issue records.
- **Evidence:** Implementor verification rows and generated submission evidence above; independent reproduction outputs quoted under Commands or procedures (extraction suite/validator, digest recomputation, eight-scenario harness `TOTAL 8 FAILED 0`).
- **Disposition:** `APPROVED`
- **Prior-round resolution:** `FIRST ROUND`

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NOT APPLICABLE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Long-running session stability, host rate limits, envelope stability across CLI versions, and behavior under other authentication modes remain `UNKNOWN` and are owned by this issue's fail-closed requirement; the owner accepts this residual risk within the authorized slice.
- `--resume` under the widened profile was not re-probed; the runner's current launch path does not use `--resume`, so this gap is inert but recorded.
- Ambient host settings participated in the no-grant probes (Read permitted ambiently, Edit denied); only the explicit-grant profile is relied upon, and behavior under different host settings may differ.
- Whether the minimal profile is semantically sufficient for real role work (prompt adequacy, multi-turn task completion) is demonstrated by milestone 5's gated dogfood run, not by this milestone's probes; the dependency ordering in the accepted ADR keeps that demonstration's evidence clean if this profile proves insufficient.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-17T02:12:18Z` | `human:MattSureham` | `NONE` | `INVESTIGATING` | Owner direction authorized the product-level autonomy objective and this capability milestone; specification evolution, accepted ADR, and this owning issue recorded; pipeline state `AUTHORIZED` |
| `2026-08-17T02:31:39Z` | `agent:ClaudeCode-live` | `INVESTIGATING` | `INVESTIGATING` | Pipeline AUTHORIZED -> READY. Validated transition AUTHORIZED to READY. |
| `2026-08-17T02:31:47Z` | `agent:ClaudeCode-live` | `INVESTIGATING` | `IMPLEMENTING` | Pipeline READY -> IN_PROGRESS. Implementation attempt 1 began from immutable base 8b1c13269f12df583a98f09c74bcc185143999a8. |
| `2026-08-17T02:45:09Z` | `agent:ClaudeCode-live` | `IMPLEMENTING` | `IMPLEMENTING` | Implemented attempt 1 within the contract allowed paths: five live probes recorded in `EVIDENCE-20260817T023721Z-live-profile-probe.md` (minimal profile `Read,Edit,Write,Bash` + matching grant; silent success-shaped permission denial machine-readable via `permission_denials`; budget class unchanged); registry evolved to schema `rotation-participants/v2` with `allowed_tools`; launcher emits `--allowedTools` only when non-empty; classifier gains the `permission_denied` participant-failure class with fail-closed malformed-field handling; 8 new stub-launcher tests (97 total `OK`); `ROLE_CONTRACTS.md` and `README.md` conformed; verification rows recorded above |
| `2026-08-17T02:51:24Z` | `agent:ClaudeCode-live` | `IMPLEMENTING` | `REVIEW` | Pipeline IN_PROGRESS -> AWAITING_PEER_REVIEW. Immutable target 83838e0b1a579f13706b4728da3c3219ed73a8e9 passed structural and accepted deterministic checks; evidence EVIDENCE/EVIDENCE-20260817T025124Z-milestone-20260817t021218z-live-invocation-v1-attempt-1.json. |
| `2026-08-17T03:27:54Z` | `ClaudeCode/live-review` | `REVIEW` | `REVIEW` | Independent review round 1 persisted: extracted-target verification (97 tests `OK`, validator `PASS`, five digests recomputed and matching), base ancestry and eight-path allowed scope confirmed, record-only post-target drift confirmed, and an eight-scenario adverse harness (`TOTAL 8 FAILED 0`) covering real-decision constraint parsing with registry-participant independence filtering, original raw-envelope classification, probed denial/budget shapes, malformed-denial fail-closed behavior, exact launcher argv for the committed profile, registry v2 validation boundaries, denial-then-advance end-to-end without escalation, and crash recovery without duplicate transition. Disposition `APPROVED`, zero open material findings; no pipeline transition (approval leaves `AWAITING_PEER_REVIEW` for the recorder) |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies. — `NOT_APPLICABLE`: review is `INDEPENDENT`.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
