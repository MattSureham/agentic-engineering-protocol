# Live Participant Invocation Capability

## Metadata

- **ID:** `ISSUE-20260817T021218Z-live-invocation`
- **Title:** Implement the authorized live participant invocation capability milestone
- **Status:** `IMPLEMENTING`
- **Severity:** `MEDIUM`
- **Owner:** `ClaudeCode/root`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-17T02:12:18Z`
- **Updated UTC:** `2026-08-17T02:45:09Z`
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

## Pipeline state

The JSON block is operational state bound to the accepted milestone contract. It does not contain or override scope.

<!-- AEP-PIPELINE-STATE-V1:BEGIN -->
```json
{
  "schema": "aep-pipeline-state/v1",
  "milestone_id": "MILESTONE-20260817T021218Z-live-invocation-v1",
  "authority_digest": "36f862db0345ff9667b7a3469fbc6a25750c8ef9e300324de181dc1f57659cea",
  "state": "IN_PROGRESS",
  "attempt": 1,
  "implementor": "agent:ClaudeCode-live",
  "base_revision": "8b1c13269f12df583a98f09c74bcc185143999a8",
  "target_revision": null,
  "verification_evidence": [],
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

No independent review round has been recorded. Review begins after the first immutable implementation target is submitted through the pipeline.

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
