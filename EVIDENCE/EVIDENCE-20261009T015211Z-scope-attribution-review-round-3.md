# Evidence — Scope-attribution amendment independent review round 3

## Metadata and authority

- **ID:** `EVIDENCE-20261009T015211Z-scope-attribution-review-round-3`
- **Recorded by:** `agent:Codex-scope-review-20261009`, independent of target implementor `agent:ClaudeCode-discovery-fix-3`; no implementation authorship. Label inequality is not authentication.
- **Disposition UTC:** `2026-10-09T01:54:25Z`; exact run capture UTC/platform/Git version in [raw results](scope-attribution-review-round-3/results.json).
- **Immutable target:** `4dda31e9945000b51e950f4ac01ec7f82ffb15bf`, parent `0cb370f525c51e30f67020ccc9208e08abda45a4`.
- **Recovered repository:** clean `main`; local and cached `origin/main` both `b0ea36f51123d77d7d0293b8be5d65c4a6188b8f`. Its changes after the target are HANDOFF/checkpoint/issue reconciliation only, not implementation. Direct remote equality/publication was not checked or performed.
- **Normative sources:** complete root [BOOTSTRAP](../BOOTSTRAP.md); accepted [PROJECT_SPEC](../PROJECT_SPEC.md) PIPELINE-010 including the 2026-10-08 strengthening and unchanged ten invariants; [accepted pipeline ADR](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md) decision 7; [owning issue](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) owner approval/rework directives; [role contracts](../ROLE_CONTRACTS.md).
- **Recovered review history:** [round 1](EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md), target `6e39cea`, CHANGES_REQUIRED R1–R5; [round 2](EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md), target `4f5e387`, CHANGES_REQUIRED R2 HIGH/R3 HIGH/R5 MEDIUM, with bounded R1/R4 resolution. Those histories and reproductions were read directly, not inherited as conclusions.
- **Current scope:** ordinary issue-level contract amendment review, not a milestone attempt. Discovery remains IN_PROGRESS attempt 3, target null, original base/digest/events and exactly two entries. Dispatcher selects discovery implementer; it does not route this amendment's review and its generic submission command is not executed.
- **Disposition:** `CHANGES_REQUIRED`, **3 open material findings**: R2 HIGH, R3 HIGH, R5 MEDIUM. No R1/R4 regression observed within the checks below.

## Exact procedure and observations

From a retained clone containing the target:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-3/reviewer_checks.py . --suite
```

The [reviewer-owned harness](scope-attribution-review-round-3/reviewer_checks.py) extracts **that exact Git target**, imports its fixture helpers and the retained earlier reviewer harnesses, and runs actual pipeline CLI submissions only in disposable local repositories. The original 22 scenarios use the same explicit v2 fixture adapters documented in round 2; its 20 new variants are replayed unchanged. Only the old harness's source-record lookup constant is retargeted, not production code or accepted fixture scope. Fifteen new variants independently challenge the strengthened rules. No Codex/Claude/live-agent session or discovery conformance/oracle rerun occurs.

The command exited `0`: reproduction completed, **not conformance**. Raw records preserve exact input issue text/registry, synthetic commit graph and introduction selection, exit/stdout/stderr, state, exclusions and no-mutation checks. Fixture hashes and durations vary on rerun; relationships, inputs and outcomes are reproducible. Disposable Git objects are not retained, but their construction is.

Inside the frozen extraction, the harness ran:

| Exact argv after `python3` | Captured concise output | Exit |
|---|---|---:|
| `-m unittest discover -s tests -p test_run_pipeline.py -v` | `Ran 49 tests in 54.216s` / `OK` | 0 |
| `-m unittest discover -s tests -v` | `Ran 194 tests in 64.917s` / `OK` | 0 |
| `scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)` | 0 |

| Reviewer scenarios at `4dda31e` | Cases | Valid advances | Expected refusals observed | Unsafe advances |
|---|---:|---:|---:|---:|
| Prior round-1 scenarios | 22 | 2 | 20 | 0 |
| Prior round-2 variants | 20 | 2 | 18 | 0 |
| New hostile variants and controls | 15 | 2 | 4 | 9 |

Every refusal preserves all non-Git fixture files and pipeline state; all cases preserve the original attempt base. Unsafe cases actually advance to AWAITING_PEER_REVIEW, emit evidence and exit 0. They are not helper-only parser anomalies. The prior 42 scenarios' success is independently confirmed, but is not sufficient to close the general findings.

## Material findings and required follow-up

### R2 — HIGH — File introduction and Git touches still substitute for separate scope authority

**Still open.** At target `scripts/run_pipeline.py:832`, `_issue_introduction` selects the oldest file-add commit with path-limited `git log --diff-filter=A --reverse`. It does not inspect that historical record's authority or effective decision. At lines 936–979, exact declaration equality proves only what paths a caller-selected range touched; it does not prove that those paths/commits were authorized by the separate issue or included in its actual review scope.

Four new cases advance with AGENTS.md explicitly excluded by separate owner/reviewer records:

- `post_introduction_foreign`: introduce a legitimate narrowly authorized issue first, then commit current-attempt-owned AGENTS.md, then the legitimate amendment. Declaring both touched paths launders the foreign work. Moving the unrelated commit after issue creation defeats the new guard without supplying authority.
- `draft_introduction`: the file initially says Authority AGENT and proposal only/no owner authority. Unauthorized AGENTS work lands next; a later HUMAN decision authorizes only the amendment. The old draft's introduction is nevertheless used as the authority start, so genuinely pre-approval work is absorbed.
- `deleted_readded_authority`: delete that unauthoritative draft before the unauthorized work, then re-add the issue with a later, narrow HUMAN decision. The oldest, deleted draft still supplies the purported authority ancestor; the actual authority did not exist at the foreign commit.
- `mixed_authority_merge`: after introducing the narrow issue, merge a foreign AGENTS branch into the legitimate amendment before a review explicitly scoped only to the latter. Declared paths equal the derived union and all commits descend from introduction, so the mixed-authority range passes. All-parent touch enumeration correctly sees the foreign change; its attribution, not touch discovery, is wrong.

The `side_work_before_introduction` control refuses when a side-branch substantive commit is not descended from the introduction; a legitimate merged introduction before work passes. An authorized exact-file rename also passes. Thus the ancestry/equality checks are real improvements, but they do not establish the unchanged no-smuggling/separate-authority invariant.

**Required follow-up:** bind the effective historical authorization and independently accepted scope/range to each exempted path/commit, not merely file existence and a caller-selected Git set. Refuse drafts, deleted/reintroduced records, foreign work after introduction, and mixed ranges lacking that binding. Keep exact-file, no-prefix, coverage/disjointness checks, original base/history and HEAD semantics. The new mechanical clauses are necessary checks, not permission to discard the governing invariant. Any new authority/trust representation requires owner approval; this review neither implements nor adopts one.

### R3 — HIGH — Example-only approval and malformed latest rounds still pass

**Still open.** At lines 719–732, fence stripping tracks only delimiter character, not delimiter length or valid closing syntax. At lines 747–768, review selection considers only headings that already match the expected regex; an unrecognized latest round can disappear from consideration.

- `review_long_fence_example`: the only review is inside a four-backtick fenced example containing a shorter three-backtick line with `example` text. That shorter line does not close the outer Markdown fence, but the parser treats it as a close, exposes the example APPROVED/0 fields, and advances without a real review. The issue explicitly introduces it as an example and says no actual review exists.
- `review_malformed_latest`: after an earlier valid approval, a later review heading uses a hyphen instead of the required em dash and states BLOCKED/unresolved authority/do not use the earlier approval. The parser ignores the malformed heading and reuses the favorable earlier fields. The contract says malformed or contradictory review evidence refuses, not that it may be silently skipped.

Duplicate sections, same-timestamp rounds, unknown/negated counts, elongated 41-hex tokens, missing/BLOCKED/unrecognized statuses and label-equality controls now refuse. Those improvements do not cure the two new false approvals.

**Required follow-up:** prove that credited records are outside examples with correct fence boundaries (or refuse unsupported/ambiguous constructs); reject malformed/conflicting round candidates rather than choosing the last recognized favorable one. Keep uniquely applicable section/round, exact target, bare count and independence gates. Add both counterexamples and clean historical-prose controls. Do not rewrite old review records to hide ambiguity.

### R5 — MEDIUM — Lexical positivity and SATISFIED prefix still accept unresolved authority

**Still open.** `_verify_owner_decision` (lines 840–865) requires a positive word but uses an incomplete negation filter. The SELF unblock gate (lines 984–993) takes the first matching field and tests only its prefix.

- `self_contracted_negation`: `human:fixture-owner hasn't approved this authority record.` passes because `approved` is present but the contraction is not rejected.
- `self_satisfied_pending`: a positive recorded body plus `SATISFIED is false; awaiting owner authorization` in Unblock condition passes.
- `self_duplicate_unblock`: the first SATISFIED field is credited despite a second field explicitly recording PENDING/unresolved authorization.

The control mixing positive and explicit `pending` in the decision body refuses. Old empty/pending/fenced-heading cases refuse. SELF still declares no paths and excludes only its own issue file, limiting impact; it nevertheless does not establish effective authority.

**Required follow-up:** require a unique, effective, unambiguous positive attributable decision and a consistent satisfied condition; contracted/other negation, contradictory/pending fields and duplicates must refuse. A positive-word/prefix heuristic cannot substitute for that evidence. Preserve SELF's own-file-only boundary. Escalate any new trust/architecture decision rather than weakening the invariant.

## R1/R4 regression checks, scope and history

The retained merge-post-review, simplified-history hidden-touch, asymmetric-parent and octopus cases were independently replayed. Record-only octopus passes; hidden/substantive/asymmetric/uncovered changes refuse. New post-review deletion followed by re-addition of identical final bytes also refuses. Explicit parent-diff unions agree with implementation touches in new merge variants and the real case. Registry absent/null/malformed cases still behave correctly on in-scope as well as outside-path scenarios. No refusal mutates fixture files/state.

The governance check independently compares ASTs of `_commit_paths`, `_verify_target_scope` and `_parse_intervening_registry` between `4f5e387` and `4dda31e`; all remain unchanged. No R1/R4 regression observed in these bounds; no exhaustive Git graph/path-space claim.

The target modifies only five expected files: root specification, pipeline ADR, pipeline code/tests and owning issue. Later `b0ea36f` changes only HANDOFF/checkpoint/issue reconciliation. No bridge/package/dependency/discovery issue/registry/live implementation or accidental artifact drift. PIPELINE-010 and ADR decision 7 express the same strengthening, with no new state edge, allowed_paths/digest change, base rewrite or target==HEAD change. Their general fail-closed/no-smuggling requirements remain unmet by the implementation; test success cannot supply missing architectural proof. Prior implementation/review commits and accepted intervening work remain ancestors, with no rewrite/rebase/revert in the inspected chain.

## Real A/B characterization — read-only

The harness retargets only source-record lookup to `4dda31e`, checks current A/B authority-record bytes equal that target, then uses frozen code to verify both entries against historical candidate `9f72d3de57085525a8ddf8a3b14bf1a3161e26e8`, original base `88fa8359ec3a62f200096d0d96bd04a88ebd118a`. Independent enumeration diffs every reachable window commit against each explicit parent; no path-limited simplification is used for the audit.

A's dated owner decision and latest APPROVED/0 round on `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3` cover the actual blocked-exit amendment; post-review work is record-only and reviewer label differs. Its four exact declared substantive files plus its issue cover five paths. B's actual attributed positive owner decision and satisfied historical authority record, empty paths and own-file-only exclusion cover one. Both still pass the strengthened verifier. All six paths have exactly one covering entry with complete touch coverage; dropping A exposes five paths, dropping B one. Existing A/B cannot cover a hypothetical AGENTS change. Full hashes/provenance and touching commits are in `real_case` in the raw JSON.

This is component characterization, not submission of an old target, not a bypass of target==HEAD, and not discovery conformance approval. Honest A/B success does not remedy the general hostile variants. Discovery contract block, digest, machine state, attempt base and event history remain unchanged.

## Non-material findings, limitations and stopping boundary

- **O1 LOW — continuity/evidence precision:** issue Updated UTC remained at the previous review despite subsequent rework. HANDOFF's 42-scenario summary says only two positive controls advance, while the two groups contain two each (four total). Current snapshot/counts are reconciled with attribution; authored summaries remain historical. The implementer now correctly leaves resolution to independent review.
- **O2 LOW — audit convenience, inherited:** exclusions carry path, touching commits and covering issue/range/review class; exact decision/round/target still requires reconstruction from the immutable issue. Reconstructable for real A/B, not an additional blocker; it cannot rescue falsely verified provenance.
- **O3 LOW — inherited role wording:** ROLE_CONTRACTS still says target parent equals attempt base, subordinate to accepted ancestor/base-preservation semantics. Not introduced by this target. Reconcile through authorized documentation work; no change by this reviewer.
- **O4 LOW — parser integration friction:** the initial reviewer governance check called the strict milestone `_parse_latest_review` on this non-milestone amendment issue and failed with `no durable independent review round is recorded`. Its unanchored section search matches the inline heading name in the target's rework narrative before the actual section. The amendment-specific `_tolerant_latest_review` anchors the section correctly; the reviewer-only check now uses that applicable parser. The failed command is retained, historical issue text and implementation are unchanged. No current amendment machine transition depends on the strict parser, so this is not another material scope-attribution finding. Authorized follow-up should cover heading-name prose consistently across parsers.
- Darwin/Python 3.9 only; standard-library deterministic checks and bounded fixture graphs. Dedicated Markdown linters unavailable (`command -v markdownlint markdownlint-cli2 pymarkdown` returned no paths); bounded local link/fence/newline/whitespace checks are not a full linter. No cross-host/concurrency/authenticated-identity guarantee.
- No live-agent probe, discovery conformance/oracle rerun, implementation/specification/ADR/test/package/bridge/discovery-issue change, third registry entry, discovery submission, acceptance/closure, recorder/coordinator work or push. Only reviewer evidence/issue/HANDOFF/checkpoint records are persisted and committed locally.
- **Disposition:** CHANGES_REQUIRED, R2 HIGH/R3 HIGH/R5 MEDIUM remain open, not accepted debt. The amendment has no machine state, so there is no applicable amendment pipeline transition; discovery stays IN_PROGRESS attempt 3. Next safe work is bounded amendment rework, not the dispatcher's generic discovery submission.

## Governance verification and artifact integrity

Exact separate post-write reads and governance command outputs are retained in [governance-readback.json](scope-attribution-review-round-3/governance-readback.json). Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-3/check_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
```

The check binds the exact disposition/target/count, preserved earlier rounds/activity, one Next Action/five HANDOFF sections, reviewer-only diff, unchanged discovery bytes/state/two entries, raw scenario outcomes, real-case coverage, ancestry and R1/R4 code preservation. The eventual reviewer commit tree identifies these clone-resident artifacts (`git log --` this file); no aggregate digest or external retention claim is needed. Historical evidence remains immutable; these results add a new round rather than reclassifying prior observations.
