# Evidence — Scope-attribution amendment independent review round 4

## Metadata and recovered authority

- **ID:** `EVIDENCE-20261012T015542Z-scope-attribution-review-round-4`
- **Recorded by:** `agent:Codex-scope-review-20261012`; no authorship of this implementation, independent of `agent:ClaudeCode-discovery-fix-3`. Recorded-label inequality is not authentication.
- **Disposition UTC:** `2026-10-12T01:57:58Z`.
- **Immutable target:** `d9bd6d806e0f1160df4b6893154017e9d287cc4e`, parent `b80ccda21826073ae214f960877536c0e0348b98`.
- **Recovered state:** clean `main`; local and cached `origin/main` at `500df768721aa751d3826715429e9b56bf6dab39`. Its post-target diff is only HANDOFF/checkpoint/owning-issue reconciliation, not the implementation. No direct-remote check or publication performed by this reviewer.
- **Authority:** complete [BOOTSTRAP](../BOOTSTRAP.md); accepted [PROJECT_SPEC](../PROJECT_SPEC.md) PIPELINE-001–010, especially the 2026-10-10 structured-record amendment and unchanged ten owner invariants; [accepted pipeline ADR decision 7](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md), [root adoption ADR](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md), [owning issue](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) owner decision/rework directives, and [role contracts](../ROLE_CONTRACTS.md).
- **Recovered history:** [round 1](EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md) CHANGES_REQUIRED R1–R5; [round 2](EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md) and [round 3](EVIDENCE-20261009T015211Z-scope-attribution-review-round-3.md) CHANGES_REQUIRED R2 HIGH/R3 HIGH/R5 MEDIUM, R1/R4 resolved within bounded evidence. Records and retained reproduction code were inspected directly, not accepted as conclusions.
- **Scope:** only the ordinary issue-level amendment and A/B migration. No amendment machine state exists. Dispatcher selects discovery implementer, IN_PROGRESS attempt 3, target null; it does not dispatch this ordinary review. Its generic discovery submission command was not executed.
- **Disposition:** `CHANGES_REQUIRED`, **3 open material findings: R2 HIGH, R3 HIGH, R5 MEDIUM**. R1/R4 have no observed regression in the checks below. The new representation improves native-record binding, but does not yet establish general fail-closed authority.

## Method, commands and raw observations

Run from a clone retaining the immutable target and prior review records:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-4/reviewer_checks.py . --baseline
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-4/hostile_checks.py .
```

Both procedures exited `0`, meaning reproduction completed, **not conformance**. The [baseline harness](scope-attribution-review-round-4/reviewer_checks.py) and [new hostile harness](scope-attribution-review-round-4/hostile_checks.py) extract the exact target with Git, import only its implementation/fixture helpers and retained earlier scenario code, and exercise actual pipeline CLI transitions solely in disposable local repositories. Production code, source repository state and accepted fixture allowlists are never patched. Environment: Darwin arm64 / Python 3.9.6; exact platform/Git versions and capture times in [baseline-results.json](scope-attribution-review-round-4/baseline-results.json). New inputs, anchor snapshots for mismatches, commit graphs, exact exits/stdout/stderr, exclusions and no-mutation results are in [hostile-results.json](scope-attribution-review-round-4/hostile-results.json). Scripts reconstruct ephemeral Git objects; synthetic SHAs/durations vary on rerun.

Frozen-target commands after `python3`:

| Command | Captured output | Exit |
|---|---|---:|
| `-m unittest discover -s tests -p test_run_pipeline.py -v` | `Ran 56 tests in 74.335s` / `OK` | 0 |
| `-m unittest discover -s tests -v` | `Ran 201 tests in 85.972s` / `OK` | 0 |
| `scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)` | 0 |

| Reviewer group | Cases | Valid advances | Expected refusals | Other result |
|---|---:|---:|---:|---|
| Round-1 unchanged v2 adapter | 22 | 1 | 20 | Legacy `positive_independent` refuses for missing machine decision |
| Round-1 fixture-only structured migration | 22 | 2 | 20 | All conform |
| Round-2 variants | 20 | 2 | 18 | All conform |
| Round-3 variants | 15 | 2 | 13 | All conform |
| New structured/migration variants | 50 | 4 | 31 | 13 material false advances, 2 non-material parser strictness gaps |

The old adapter suppresses owner decisions for **all** INDEPENDENT fixtures, not only its positive. Thus its refusals alone would provide weak regression evidence. The explicit second replay supplies the required scoped structured decision for those scenarios, preserving the absent-decision SELF adversary and every original path/range/review mutation. This is a fixture migration, not a production workaround or weaker expectation. Missing blocks are explicitly unsupported by the accepted migration contract, so the old positive's refusal is reasonable legacy incompatibility, not a product regression. All 57 migrated/current prior scenarios conform.

Every refusal preserves all non-Git fixture files and pipeline state; every scenario preserves the original attempt base. Each new false advance actually exits 0, writes evidence and reaches AWAITING_PEER_REVIEW, not just a permissive parser return. Four new positive controls cover native INDEPENDENT, honest legacy migration, SELF, and authority established before the attempt/range. No live-agent probe or discovery conformance/oracle rerun occurs.

## R2 — HIGH — Historical authority scope/effect is not bound; contradictions still pass

**Still open.** At target `scripts/run_pipeline.py:1065`, `_verify_anchor_content`'s native branch compares machine identity fields. Its historical-decision branch checks only HUMAN metadata, a matching UTC heading and attribution. It does **not** establish historical authorized scope, EFFECTIVE/positive approval or satisfied condition. At lines 1361–1374, subset tests consequently compare the declaration against a later migration's unsupported claims. The authorized prose-migration exception is not itself wrong; its claimed proof is incomplete.

- `legacy_scope_widening`: historical owner and review explicitly authorize/review only `OTHER/amendment.md`, excluding AGENTS.md. A later block declares both and cites the old anchors; all prose is retained. Submission excludes the foreign AGENTS change and advances.
- `legacy_pending_authority`: the historical HUMAN heading expressly says NOT approved / pending. Work follows that non-decision. A later block claims EFFECTIVE at the same old UTC/anchor, and current prose is changed to positive. The anchor attribution check passes, laundering pre-authority work. Git history still contains the contradiction; no history rewrite occurs.
- `native_decision_prose_scope_conflict`: even an unchanged native block passes when its own decision body expressly excludes the substantive path named by the block.
- `native_independent_pending`: a native EFFECTIVE block with `human:fixture-owner has NOT approved; substantive authorization is pending.` advances. The current decision check deliberately applies its negation filter only to SELF (`strict_negation=review_class == "SELF"`).
- `native_independent_unblock_pending` and `native_independent_unblock_duplicate`: INDEPENDENT advances with PENDING/unresolved satisfaction, or a second contradictory Unblock field. `_verify_unblock_condition` is called only in the SELF branch, although PIPELINE-010/ADR decision 7 require one consistent unblock field for the owning issue generally.

**Required follow-up:** prove the historical/effective decision actually authorizes every exempted substantive path and precedes the work; later machine projection cannot manufacture past scope/effect. Reject conflicting native decision scope/effect and unblock records for both classes. Preserve original allowlist/base/history/HEAD semantics, exact paths, range coverage and no-mutation behavior. A new migration/trust representation must receive owner approval; this review does not prescribe or adopt one. Do not cure the problem by rewriting historical prose or relabeling attempt work.

## R3 — HIGH — Migration can manufacture reviewed scope, approval and zero findings

**Still open.** In `_verify_anchor_content`'s historical-review branch (target lines 1115–1139), a matching reviewer/UTC heading plus substring membership of the target and disposition is accepted. Historical material count and reviewed scope are never compared; `APPROVED` inside `NOT APPROVED` satisfies the membership test. The current consistency check (lines 1219–1234) checks selected scalar fields but not scope.

- `legacy_review_scope_widening`: separate decision legitimately names both paths, but the historical review expressly excludes AGENTS.md. Migration widens only the claimed review scope; current/historical scope prose remains narrow. The unreviewed path is excluded and submission advances.
- `legacy_review_open_findings`: historical review records APPROVED with **1** material finding. The later block and current narrative say zero and cite that old review anchor. Submission advances although Git proves the claimed zero was never recorded there.
- `legacy_review_negated_approval`: the anchor says `CHANGES_REQUIRED. NOT APPROVED.`. A later block/current narrative says APPROVED/0 with the same target, UTC and reviewer. The substring check credits that adverse historical round and advances.
- `native_review_prose_scope_conflict`: a native block naming the substantive file passes despite its review body explicitly saying record-only and that the substantive file was NOT reviewed.

**Required follow-up:** bind the migrated approval, exact count, target, identity and scope to the actual applicable historical acceptance; refuse unsupported/contradictory projections. Do not infer positive disposition from substring presence. Current review prose/block scope conflicts must refuse, not silently favor the block. Retain correct native identity-change, duplicate, exact-type, target/anchor ancestry and independent-label protections. Any new architectural decision requires owner authority; no fix is implemented here.

## R5 — MEDIUM — SELF can still assert effective authority that was denied or pending

**Still open.** SELF's boundary remains own-issue-only, but effectiveness is not established generally.

- `legacy_self_pending_anchor`: its historical attributed heading says NOT approved / pending. A later EFFECTIVE/SATISFIED block and positive current body cite that same historical anchor. The issue is excluded and submission advances, although the anchor records no positive decision.
- `self_decision_declined`: native EFFECTIVE block plus `human:fixture-owner declined the request to mark this record approved.` advances. The lexical check sees `approved` and misses the rejection.
- `self_unblock_denied`: native SATISFIED block with `SATISFIED - approval was denied` advances. The negative-word heuristic misses that explicit denial.

**Required follow-up:** require a unique, effective positive owner decision with an anchor that actually records it, and fail closed on conflicting/denied satisfaction. Adding structured fields must not turn a contradictory narrative into valid authority. Keep empty SELF scope and own-file-only exclusion. Repair within accepted authority or escalate a new migration/trust design; do not weaken the invariant. No authenticated-identity requirement is being added.

## Machine-authority separation and confirmed strengths

Native JSON blocks now provide decision/round identities, owner/reviewer labels, state, exact scopes, target, disposition/count and anchor input; no absent-block fallback exists. Exact keys, duplicate JSON keys, scalar count types, state enums, missing commits and native identity drift are rejected. Explicit valid records before the range work; a replacement decision after work refuses. Duplicate/conflicting blocks, repeated keys, unknown/missing fields, PENDING/REJECTED/SUPERSEDED, booleans/string counts, missing anchors, post-anchor scope/target changes, reviewer equality, post-review substantive changes, unauthorized rename, path traversal/dot aliases/directory scopes, fenced-only blocks, lookalike-only markers, NBSP marker changes and CRLF records refuse in the new checks. CRLF refusal is conservative, not a portability success.

However, historical fallback still reconstructs critical approval/effect from partial prose signals, and current contradiction checks do not cover all binding fields/classes. The trusted fact is then a later assertion, not verified separate authority. Therefore the representation is **ALIGNED** with the accepted architecture, but the exercised migration/consistency behavior is **UNJUSTIFIED_DRIFT** from its unchanged fail-closed requirements. Passing tests cannot resolve that difference. This is not a request for arbitrary natural-language understanding: the retained fixtures show explicit inspectable contrary scope, counts, disposition and decision records that must cause refusal rather than claimed proof.

## R1/R4, implementation scope and append-only history

Independently replayed original hidden-touch/post-review merges, asymmetric-parent and octopus cases. Hidden/substantive cases refuse; record-only octopus and merged introduction controls pass. Explicit per-parent enumeration agrees in the retained merge scenarios and real-case window. Unauthorized rename, post-review substantive changes and uncovered same-path touches refuse in new cases; prior delete/re-add and range/overlap cases re-pass. Absent registry remains allowed; malformed/null registries refuse even on in-scope targets. All refusals preserve files/state.

The governance check compares `_commit_paths`, `_verify_target_scope` and `_parse_intervening_registry` ASTs between parent and target: unchanged. R1/R4 show no regression within these bounds, not exhaustive Git/path-space proof.

The target changes exactly seven expected files: specification, pipeline ADR, pipeline implementation/tests, owning amendment issue and the two A/B migration issues. The later reconciliation changes three records only. No package/bridge/dependency/live-runner/discovery-issue/registry/contract-state/allowed_paths change. SPEC PIPELINE-010 and ADR decision 7 consistently state the new block/anchor/consistency requirements and retain the state machine, digest, attempt base and target==HEAD semantics. Earlier targets, reviews and accepted intervening work remain ancestors; no rewrite/rebase/revert was used in the inspected chain. Identifier/path/commit handling is generic, not hard-coded to A/B or six paths.

## Real A/B migration — read-only characterization

Read the blocks and original Git content directly; useful exact commands:

```sh
git diff d9bd6d8^ d9bd6d8 -- ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md
git show 47a0cb40684ad8edc1d574eba28ded610ea2ba93:ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md
git show 79063cb2201517567c3a8fe9702fd59ca41e9e5d:ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md
git show 610c672082a44e591a13822ffc12a9aa58babadb:ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md
```

- A decision anchor `47a0cb4` records MattSureham's positive bounded blocked-exit amendment approval, lists its four substantive files, and contains their implementation. Equality of decision anchor and substantive commit is permitted by the accepted contract. Review anchor `79063cb` records the independent APPROVED/0 round on `9e8f6b2`, explicitly including that amendment and resume. Its four machine scope files match that historical work/review. No authority expansion observed in this actual migration.
- B decision anchor `610c672` records MattSureham's bounded quota authorization with a separate execute-now gate. Empty scope and own-record-only accounting preserve that distinction; EFFECTIVE here does not renew consumed budget or authorize any live launch. The historical decision and satisfaction are real, unlike the hostile pending-anchor fixture.
- Migration inserts projections/attributable activity and refreshes Updated UTC; no other old lines are removed, independently checked. Prior prose/review history remains preserved. The new blocks postdate the historical ranges by the explicitly approved migration design; they cite historical decisions rather than being newly executed authority.
- Frozen code verifies both entries against historical candidate `9f72d3d`, original base `88fa835`. All six original outside paths have exactly one covering entry and complete touching-commit coverage. Removing A exposes five, removing B one; existing entries cannot cover a hypothetical AGENTS path. Raw JSON retains full hashes/ranges/touches and unchanged machine state/contract. This is not submission of the old candidate or approval of discovery conformance.

Honest A/B success and manual migration verification do not establish generic migration safety; R2/R3/R5 show why.

## Non-material observations and limitations

- **O1 LOW — evidence precision:** implementer summaries correctly leave resolution open; the old round-1 adapter's missing-block effect is now quantified for all cases, with a migrated replay retained separately. No historical result is overwritten.
- **O2 LOW — inherited provenance convenience:** exclusion output still carries issue/range/class/touching commits, not structured decision/round IDs and resolved anchors. Immutable target issue reconstruction makes real A/B auditable, but a future evidence improvement should carry that provenance directly. This does not rescue false verification.
- **O3 LOW — inherited role wording:** ROLE_CONTRACTS still says target parent equals attempt base; higher-authority ancestor/base-preservation rules govern. Authorized documentation follow-up remains needed, not a target fix by this reviewer.
- **O4 LOW — inherited strict milestone-parser prose collision:** ordinary amendment uses the anchored amendment parser, not the strict milestone parser. The round-3 observation remains; no unrelated parser change made.
- **O5 LOW — malformed marker suffix:** `duplicate_end_marker` advances with the end marker twice on the same line. `_structured_block_region` records at most one occurrence per line. No competing machine facts are introduced in this fixture, so it is a strictness defect but not an additional material authority bypass. Require explicit marker grammar/occurrence validation in authorized follow-up.
- **O6 LOW — timestamp validity:** `invalid_utc` advances with matching block/heading `2026-99-99T99:99:99Z`. UTC regex validates shape, not a real UTC datetime. This fixture does not change scope/approval, so recorded as non-material validation debt, not a fourth material finding.
- Darwin/Python 3.9, bounded synthetic histories and standard-library checks only. Dedicated Markdown linters unavailable (`command -v markdownlint markdownlint-cli2 pymarkdown` returned no paths); local link/fence/newline checks are not a full linter. No cross-host/concurrency/authenticated-identity guarantee. Global uniqueness across every unrelated record and every Unicode/Markdown construct is not exhaustively established.

## Durable disposition, governance and stopping boundary

CHANGES_REQUIRED with R2 HIGH/R3 HIGH/R5 MEDIUM still open, not accepted debt. The ordinary amendment remains IMPLEMENTING for bounded rework and fresh review. Discovery remains IN_PROGRESS attempt 3, target null, original digest/base/events, exactly two entries. No amendment pipeline transition exists; no discovery transition is appropriate.

Only reviewer evidence, appended owning-issue round, HANDOFF and checkpoint are changed. No implementation/specification/ADR/test/package/A/B migration/discovery record edits, no third registry entry, live probe, discovery submission, acceptance/closure, recorder/coordinator action or push. Reviewer records are committed locally only; resolve their containing commit with `git log --` this evidence.

Separate post-write content reads and exact governance outputs are retained in [governance-readback.json](scope-attribution-review-round-4/governance-readback.json). Reproduce:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-4/check_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
```

The [governance check](scope-attribution-review-round-4/check_governance.py) binds this target/disposition/count, preserved prior rounds/activity, five HANDOFF sections/one Next Action, exact reviewer-only diff, unchanged discovery/A/B bytes, raw results, migration append-only bounds and ancestry. These checks verify the records, not implementation approval. Clone-resident scripts/results plus the reviewer commit tree supply artifact identity; no external retention or aggregate-digest claim is made.
