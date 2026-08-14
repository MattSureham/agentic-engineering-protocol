# Authorized Milestone Pipeline v1 Verification

## Metadata

- **ID:** `EVIDENCE-20260814T023224Z-authorized-pipeline-verification`
- **Title:** Immutable-target verification and review-boundary evidence for the root-local pipeline
- **Captured UTC:** `2026-08-14T02:32:24Z`
- **Recorded by:** `Codex/root`
- **Claim supported or challenged:** Target `6c0a3bda06686635023e334a4e644fb176372b04` implements the bounded root pipeline contract and passed the specified deterministic verification; this evidence does not establish independent approval or broader protocol maturity.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), `PIPELINE-001` through `PIPELINE-008` and pipeline acceptance criteria
- **Related ADRs/issues:** [`ADR-20260814T015817Z-authorized-milestone-pipeline`](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md); [`ISSUE-20260806T013907Z-runtime-automation`](../ISSUES/ISSUE-20260806T013907Z-runtime-automation.md); [`ISSUE-20260807T022523Z-pilot-onboarding-authority-friction`](../ISSUES/ISSUE-20260807T022523Z-pilot-onboarding-authority-friction.md); [`ISSUE-20260811T030136Z-review-disposition-vocabulary`](../ISSUES/ISSUE-20260811T030136Z-review-disposition-vocabulary.md)
- **Repository revision/state:** Immutable target `6c0a3bda06686635023e334a4e644fb176372b04`, tree `d999df04d656551a8c64704a39abdf3891855677`, parent/authority boundary `a6f2699a4bed2e1a08c9a506bad62204bd2d0086`; target is published at public `origin/main`; this evidence and the generated state-transition record are post-target review records.
- **Environment:** Darwin `25.3.0` arm64; Apple Git `2.50.1`; Python `3.9.6`; standard library only; dedicated `markdownlint` and `markdownlint-cli2` executables `NOT AVAILABLE`.

## Method

- **Procedure:** Validate the candidate, commit it as an immutable target, invoke the pipeline's own `IN_PROGRESS → AWAITING_PEER_REVIEW` gate against that exact commit, inspect generated evidence/state, publish only after fetch/ancestry/no-divergence checks, then rerun structural and record-integrity checks at the review boundary.
- **Exact command/input:** Primary commands were `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; `python3 scripts/validate_protocol.py`; `python3 -m py_compile scripts/validate_protocol.py scripts/run_pipeline.py tests/test_validate_protocol.py tests/test_run_pipeline.py`; `python3 scripts/run_pipeline.py status --json`; `python3 scripts/run_pipeline.py --root . status --json`; `python3 scripts/run_pipeline.py transition --milestone MILESTONE-20260814T015817Z-authorized-pipeline-v1 --actor agent:Codex-root --to AWAITING_PEER_REVIEW --target 6c0a3bda06686635023e334a4e644fb176372b04`; isolated-copy validation through a standard-library `tempfile.TemporaryDirectory`; a fence-aware repository Markdown/link scan using the existing validator parser; `git diff --check`; exact manifest/symlink, allowlist, source-identity, credential-pattern, commit ancestry, fetch, push, and direct/cached remote-ref checks.
- **Exit status:** All claimed checks exited `0`. The pipeline transition exited `0` and recorded `AWAITING_PEER_REVIEW`. The dedicated Markdown linter was not run because neither executable exists.
- **Repeatability:** Check out target `6c0a3bda06686635023e334a4e644fb176372b04`, run the commands above with bytecode disabled, and compare the pipeline-generated JSON record linked below. Review-state checks additionally require this post-target evidence/issue/HANDOFF record commit.

## Raw observation

| Check | Concise result |
|---|---|
| Accepted command at immutable target | `Ran 39 tests in 12.463s` / `OK` during final pre-target run; the pipeline rerun also exited `0` with untruncated `4,475`-byte stderr and zero stdout |
| Existing structural validator | `PASS structural protocol validation (package_files=10 handoffs=2)` |
| Live pipeline status before submission | Schema `aep-pipeline-status/v1`; one selected `IN_PROGRESS` milestone; authority digest `36fba5d84569105f11c8a6c2052c54dfdd4efe8f3ad63279be4b051c263ca7d4` |
| Pipeline submission | `PASS MILESTONE-20260814T015817Z-authorized-pipeline-v1 IN_PROGRESS -> AWAITING_PEER_REVIEW issue=ISSUES/ISSUE-20260806T013907Z-runtime-automation.md` |
| Generated verification | [`EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json`](EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json): schema `aep-pipeline-verification/v1`, result `PASS`, structural finding count `0`, test exit `0`, no timeout/truncation |
| Pipeline tests | 18 scenarios: accepted/draft and malformed/duplicate authority; dependency/order/path/digest refusal; deterministic read-only status; structural-validator reuse; scoped target; success/failure/unavailable/timeout evidence; atomic conflict; target/reviewer/disposition/material gates; fix/re-review; acceptance; second authorized milestone selection; post-target drift; and human escalation |
| Retained structural tests | 21 scenarios remain passing |
| Reusable package | Exact ten-file manifest, regular files only, zero symlinks; target protocol tree `70cf91821a3ae7651b2eea2644aea2a62d29aaf6`; isolated copy is byte-identical and validates independently |
| Repository Markdown/link scan | 42 UTF-8 Markdown files; final newlines, trailing whitespace, and fences pass; 195 supported relative links resolve inside the repository |
| Scope and governed sources | Target range changes exactly 15 accepted allowlist paths; `git diff --check` passes; root `PROJECT_SPEC.md`, pipeline ADR, and authority analysis are unchanged from `a6f2699` |
| Static boundary checks | Python compilation passes; no package executable, symlink, credential-pattern match, network client, daemon, database, web UI, external tracker, agent invocation, commit, or push path is implemented by the tool |
| Publication | Fetch required remote `a6f2699` to equal the target's parent; normal non-force push succeeded; local/cached/direct remote then equaled `6c0a3bda06686635023e334a4e644fb176372b04` |

Three discarded harness attempts are not claimed as checks: one combined validation command was rejected before execution because its temporary-directory cleanup used a command blocked by the execution safety layer; a later repository search used unescaped backticks in its shell argument, causing a harmless `AUTHORIZED: command not found` diagnostic; and the first post-handoff issue counter assumed an extra bracket in HANDOFF link labels and exited `1` with an empty-match assertion. All changed no repository state. The intended observations were rerun with safe, corrected procedures and are the passing results reported above.

### Post-target implementor findings

At `2026-08-14T02:39:53Z`, an additional source audit identified and reproduced cases missing from the accepted suite. Both temporary repositories were deleted by their `TemporaryDirectory` owners after the observation.

| Finding | Exact safe procedure | Observation | Implementor assessment and resolution condition |
|---|---|---|---|
| `F1` — verification-command mutation is not rechecked | Configure the fixture's accepted argv as `python -c` writing `work/check-side-effect.txt`, begin/commit a target, and submit it | `MUTATING_CHECK exit=0 state=AWAITING_PEER_REVIEW side_effect_exists=True`; Git showed the issue/evidence plus the unexpected work file dirty | `MEDIUM`, material: after accepted commands, recheck HEAD, clean state, current authority/issue source, and record a failed result without advancement when any check mutates the repository; add a regression test |
| `F2` — baseline evidence-directory symlink is not rejected | Replace the empty fixture `EVIDENCE` directory with a committed symlink to a sibling temporary directory before readiness, then run status/begin/submit | `EVIDENCE_SYMLINK status_exit=0 submit_exit=0 state=AWAITING_PEER_REVIEW`; generated JSON appeared in the sibling directory outside the repository | `MEDIUM`, material: orientation and output creation must reject a missing ownership boundary or any symlinked/escaping evidence directory before executing checks or writing; add baseline and transition regression tests |
| `F3` — generated activity row is separated from its Markdown table | Inspect the exact post-transition owning issue produced at `2026-08-14T02:31:16Z` | A blank line precedes the appended row, so its bytes remain readable but renderer table continuity is not guaranteed; the verification bullet is also immediately adjacent to the next heading | `LOW`: specialize section/table insertion and test rendered structural continuity, or explicitly accept the plain-text rendering limitation with rationale |

## Interpretation

- **CONFIRMED:** The immutable target preserves specification authority and the ten-file Markdown-only package while adding a root-only Python/Git state-and-gate tool.
- **CONFIRMED:** The tool rejects unsupported authority/state, out-of-scope targets, failed/unavailable/timed-out verification, self-review labels, target mismatch, informal dispositions, approval with material findings, post-target implementation drift, and unlinked human escalation in the tested fixtures.
- **CONFIRMED:** Successful deterministic verification produces bounded durable JSON before atomically advancing the owning issue; failed commands produce failure evidence without state advancement.
- **CONFIRMED:** The accepted target is not yet accepted by the protocol: operational state is `AWAITING_PEER_REVIEW`, the issue is `REVIEW`, and no independent round exists.
- **CONFIRMED:** The configured target checks passed, but `F1` and `F2` demonstrate that the target's gate boundary is incomplete. Passing output therefore does not establish acceptance readiness.
- **INFERRED:** This is the smallest useful lifecycle proof consistent with the accepted requirements because it automates gates and record transitions but neither performs engineering work nor schedules/invokes participants.
- **UNKNOWN:** Independent semantic correctness, behavior outside Darwin/Python `3.9.6`/Apple Git, CommonMark conformance, non-cooperating concurrent writes, authenticated identity, and usefulness in a second real repository.

## Limitations and residual uncertainty

- The 18 pipeline scenarios use isolated temporary local Git repositories. They demonstrate lifecycle mechanics, not production-grade, distributed, or multi-host coordination.
- The only real accepted contract contains one milestone. Automatic selection of a second milestone is demonstrated in an isolated fixture; no second real milestone was invented.
- Reviewer/implementor separation is exact recorded-label inequality, not identity authentication. The existing authenticated-identity issue remains blocked.
- Same-directory temporary replacement plus source-byte recheck is cooperative conflict detection, not a concurrent-writer guarantee. The existing concurrency issue remains blocked.
- Acceptance commands are trusted because they are owner-authorized specification content. They run without a shell and with common credential-bearing environment variables removed, but the tool cannot prove that arbitrary accepted commands are semantically safe or never emit sensitive data.
- The tool invokes only fixed local Git inspection commands itself. It does not use the network; publication commands in this evidence were manual release actions outside the tool.
- No dedicated Markdown linter is installed, so structural/fence/link checks are not claimed as full CommonMark validation.
- Independent review is mandatory and pending. This evidence cannot supply its own disposition.
- Implementor findings `F1` and `F2` are assessed as material and remain unresolved at target `6c0a3bd`. The implementation must not be accepted unless an independent reviewer rejects that assessment with evidence or a later target satisfies both resolution conditions.
- Finding `F3` preserves all data but may render outside the intended table. It requires reviewer disposition as a correction or explicit residual limitation.

## Integrity and provenance

- **Artifact location:** This file plus generated [`EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json`](EVIDENCE-20260814T023116Z-milestone-20260814t015817z-authorized-pipeline-v1-attempt-1.json)
- **Artifact digest:** Generated JSON SHA-256 `04823c3030ac9baa32a7d797048def838bbf75e91cef1053bcbd7f1d57156a32`; target source SHA-256: `scripts/run_pipeline.py` `7f8de45c9501e68fc390c8936ffd67bc481cba30a6ddb3a2f4a2f0906729484f`; `tests/test_run_pipeline.py` `e938313ccb8f5512bf13a5771ea70f105079ee63ce664fbb7770a4a66567cd3b`; authoritative `PROJECT_SPEC.md` `efafb0a257d3507f375e2ce08125aaee899615d5a6f205d631ceaaaa15b12ecf`; pipeline ADR `f24c15f28dd3ed9e3926ae3fec103560d257abd21102170b1d804149746e136a`.
- **External retention risk:** Public GitHub remote is useful provenance but not a higher truth tier; all claimed target and evidence content is repository-resident.
- **Supersedes / superseded by:** Supersedes candidate-only inline verification in the runtime issue; superseded by a later fix-attempt evidence record if independent review returns `CHANGES_REQUIRED`.

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-14T02:40:06Z` | `Codex/root` | Qualified the initial passing-gate interpretation with reproduced findings `F1`–`F3`; passing configured checks is retained as an observation but is not closure-ready evidence | Safe temporary-fixture observations under Post-target implementor findings; repository target remains immutable |
