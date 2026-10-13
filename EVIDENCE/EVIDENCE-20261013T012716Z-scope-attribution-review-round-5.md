# Evidence — Scope-attribution amendment independent review round 5

## Metadata, recovered authority and disposition

- **ID:** `EVIDENCE-20261013T012716Z-scope-attribution-review-round-5`
- **Recorded by:** `agent:Codex-scope-review-20261013`, fresh reviewer with no authorship of the implementation; distinct from `agent:ClaudeCode-discovery-fix-3`. Recorded labels are not authenticated identity.
- **Disposition UTC:** `2026-10-13T01:28:02Z`.
- **Immutable target:** `5bf73a0ab33bc851678c6adee30c45780d2bdb03`. Its parent `0089f8e` is part of the rework under review. The complete round-4 rework comparison starts at recovered review commit `301bc45f1f881554054d14e67edec099e209a267`; reviewing only `5bf73a0^..5bf73a0` would miss the substantive changes.
- **Recovered repository:** clean `main`, HEAD and cached `origin/main` at `46f63599bf329ecbf58d6d6c395e995cd9bd57d4`. The post-target commit changes only HANDOFF/checkpoint/owning-issue reconciliation and is not the implementation target. Direct remote equality was NOT CHECKED; no publication performed.
- **Authority:** complete root [BOOTSTRAP](../BOOTSTRAP.md), accepted [PROJECT_SPEC](../PROJECT_SPEC.md) PIPELINE-001–010 and unchanged ten owner invariants, accepted [pipeline ADR decision 7](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md), [root adoption ADR](../ADR/ADR-20260806T013907Z-root-protocol-adoption.md), [owning issue](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) owner/rework records, and [role contracts](../ROLE_CONTRACTS.md). Authority and history were recovered from Git and repository records only; no implementer chat or memory was used.
- **Disposition:** **CHANGES_REQUIRED**, **3 open material findings: R2 HIGH, R3 HIGH, R5 MEDIUM**. R1/R4 remain resolved within bounded regression evidence. No implementation repair was performed.

The amendment is ordinary issue-level contract evolution, with no pipeline machine state. Discovery remains IN_PROGRESS attempt 3, target null, original base/digest/events, exactly two registry entries. The read-only dispatcher still selects discovery implementer; it does not dispatch this review and its emitted submission command was not executed.

## Recovered review history

| Round | Immutable target | Disposition and material findings |
|---|---|---|
| [1](EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md) | `6e39cea8ac46d909709ddaeeda1aa8d2df59ce08` | CHANGES_REQUIRED: R1 merge/touch blind spots; R2 unbound ranges/scope/self-reference/overlap; R3 ambiguous approval/count/target/status; R4 invalid registry skipped; R5 absent or pending SELF authority |
| [2](EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md) | `4f5e38744340fb7597222bf31483eb67187e2bbf` | CHANGES_REQUIRED: R2/R3/R5 persist; R1/R4 independently closed within recorded bounds |
| [3](EVIDENCE-20261009T015211Z-scope-attribution-review-round-3.md) | `4dda31e9945000b51e950f4ac01ec7f82ffb15bf` | CHANGES_REQUIRED: R2 file introduction substitutes for effective authority, including mixed merges; R3 example/malformed latest approvals; R5 contracted negation and contradictory satisfaction |
| [4](EVIDENCE-20261012T015542Z-scope-attribution-review-round-4.md) | `d9bd6d806e0f1160df4b6893154017e9d287cc4e` | CHANGES_REQUIRED: R2/R3/R5 persist under structured records; 13 false advances plus two non-material schema gaps |

All Round-4 material variants were recovered and replayed: R2 historical scope widening and pending authority, native decision scope/pending conflicts, INDEPENDENT pending/duplicate unblock; R3 historical review scope widening, open findings and negated approval, native review scope conflict; R5 historical pending SELF, declined decision and denied satisfaction. All 13 now refuse. O5 repeated same-line end marker and O6 impossible UTC also now refuse. This confirms those particular corrections; the original general findings are not closed by that result.

Prior R1/R4 resolution and earlier R2/R3/R5 subcase fixes were rechecked through retained reviewer scenarios, not inferred from implementer test results. Prior rounds and evidence remain unchanged.

## Exact procedure and results

Run from a clone retaining this target and the earlier reviewer artifacts:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-5/replay_checks.py . --baseline
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-5/replay_checks.py . --hostile
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-5/adversarial_checks.py .
```

All three procedures exited `0`: reproduction completed, **not conformance**. The [replay wrapper](scope-attribution-review-round-5/replay_checks.py) changes only target-selection constants of retained reviewer harnesses. Those harnesses use `git archive` to extract the exact target, import that target's implementation/fixture helpers and retained reviewer scenario code, and execute real pipeline CLI submissions only in disposable local repositories. Production code and milestone allowlists are not patched. [New cases](scope-attribution-review-round-5/adversarial_checks.py) preserve original anchor snapshots, current issue text, registry, commit graphs, exits/stdout/stderr, exclusions and no-mutation results in [adversarial-results.json](scope-attribution-review-round-5/adversarial-results.json). Synthetic SHAs and durations vary; constructions and predicates are reproducible.

Environment: Darwin arm64, Python 3.9.6; exact platform/Git/capture details and frozen check argv are in [baseline-results.json](scope-attribution-review-round-5/baseline-results.json).

| Frozen-target check, after `python3` | Output | Exit |
|---|---|---:|
| `-m unittest discover -s tests -p test_run_pipeline.py -v` | `Ran 57 tests in 90.789s` / `OK` | 0 |
| `-m unittest discover -s tests -v` | `Ran 202 tests in 99.359s` / `OK` | 0 |
| `scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)` | 0 |

| Independent scenario group | Cases | Advances | Refusals | Interpretation |
|---|---:|---:|---:|---|
| Round-1 original v2 adapter | 22 | 1 | 21 | Its decision-less legacy positive refuses as required by the structured-record contract |
| Round-1 explicit fixture migration | 22 | 2 | 20 | All expected outcomes; missing-decision SELF adversary preserved |
| Round-2 unchanged variants | 20 | 1 | 19 | One conservative positive-fixture mismatch: `octopus_record_only` |
| Round-3 unchanged variants | 15 | 2 | 13 | All expected outcomes |
| [Round-4 unchanged hostile/control cases](scope-attribution-review-round-5/round4-results.json) | 50 | 4 | 46 | All expected outcomes, including all 13 previously unsafe cases and both schema gaps |
| Round-2 octopus fixture calibration | 1 | 1 | 0 | Record-only merge passes after removing one ambiguous parenthetical from fixture prose only |
| New Round-5 adversarial/control cases | 16 | 13 | 3 | 2 compatibility controls, **11 unsafe advances**, 3 expected refusals |

The unchanged octopus fixture says earlier attempt changes “including any to OTHER/amendment.md” are NOT authorized, so v5's path/negative-clause check refuses before reaching the merge gate. In this positive control no earlier attempt change exists. The separate calibration removes only that parenthetical before committing the fixture, preserves the exclusion of earlier attempt work and other paths, and preserves its octopus graph, expectations and production code. Both observations are retained. It is not counted as an unchanged pass or hidden by changing the old evidence. New `legacy_positive` is the inherited generic-prose compatibility shape, not independent proof of substantive scope; the explicit native control carries the scope at its decision anchor.

Every observed refusal preserves all non-Git fixture files and machine state. Every case preserves the attempt base. All 11 new false advances exit `0`, write verification evidence and reach AWAITING_PEER_REVIEW; they are not parser-only anomalies. Once these findings were established, no fix or additional role action was attempted.

## R2 — HIGH — Claimed scope and effective authority still exceed committed facts

**Still open.** At target `scripts/run_pipeline.py:1134`, `_verify_scope_consistent_prose` rejects only when a claimed path and a negative keyword occur in the same clause. It does not bind a projection to the positively authorized scope. A statement authorizing ONLY one file does not establish authority over a second file merely because the second file is not named in a negative clause.

- `legacy_only_scope_widening`: the decision anchor says `human:fixture-owner approved ONLY OTHER/amendment.md.` A later machine block claims both that file and AGENTS.md; both paths are committed after the narrow decision. The historical prose is preserved, yet AGENTS.md is excluded and submission advances. This is the Round-4 widening case with the redundant explicit AGENTS denial removed, not new authority.
- `legacy_only_scope_merge`: the same unsupported broad projection covers foreign AGENTS work merged from a side branch after the narrow authority. Explicit per-parent diffs agree with implementation touch enumeration. Ancestry/touch discovery is correct; attribution is wrong.
- `native_only_scope_conflict`: a native two-path block contradicts its own decision body saying ONLY the one file. It also advances. Structured data does not resolve contradictory authority by outranking its required narrative.
- `native_anchor_pending_rewritten`: a native EFFECTIVE block was committed beside `has NOT approved ... authorization is pending`; substantive work follows. Later only the current prose becomes positive. `_verify_anchor_content` at lines 1184–1191 returns after machine identity equality without checking the original anchor's contradiction, so that non-effective anchor retrospectively authorizes the intervening work.
- `native_revocation_erased`: after the first EFFECTIVE block, the same identity is committed with state REJECTED, then restored to the old EFFECTIVE fields without a new decision identity, owner timestamp or approval record. The verifier selects the original anchor and ignores the intervening rejection. It compares endpoints, not an unambiguous effective historical decision.
- `same_path_foreign_effect`: the owner authorizes only an alpha spelling correction; a later unrelated beta behavior expansion changes the same exact file. The review explicitly excludes the beta commit by full hash. File scopes and ancestry still match, so both substantive effects are exempted. A file allowlist is necessary, not proof that every later change to that file belongs to the separate authorization.

**Required follow-up:** establish actual authorized scope/effect and applicability to every excluded substantive change from authoritative committed records, with no retrospective repair of an invalid anchor and no resurrection of rejected authority. Preserve exact-file coverage, all-parent enumeration, original base/history/allowlist/digest and HEAD semantics. Unsupported or contradictory historical facts must refuse; do not patch more permissive prose guesses or reinterpret the contract as “anything not explicitly denied is authorized.” A new migration/trust representation requires owner approval; this review adopts none.

## R3 — HIGH — Current review projection still overrides historical scope and conflicts

**Still open.** The historical prose branch now correctly checks exact disposition and bare finding count (lines 1239–1248), and the old count/NOT APPROVED cases refuse. The native branch at lines 1213–1221 nevertheless returns after identity equality without establishing consistent historical acceptance. Scope uses the same insufficient negative-clause check as R2.

- `legacy_only_review_widening`: the owner legitimately authorizes both files, but the historical review's Scope field says ONLY OTHER/amendment.md. A later review block claims both, with the same old target/UTC/reviewer/APPROVED/0 and anchor. The original narrow review remains in both historical and current prose. AGENTS.md is incorrectly treated as reviewed and submission advances.
- `native_review_anchor_conflict_rewritten`: at the review anchor, the native block says APPROVED/0 while its own round fields say CHANGES_REQUIRED/1. Later only the current prose is rewritten to APPROVED/0. Identity equality passes against the unchanged old block, and current consistency passes against the rewritten fields; the historical contradictory round is credited as an unambiguous approval.
- `same_path_foreign_effect` also demonstrates that the exact target hash and path membership do not establish review of a commit expressly excluded by the review's scope narrative. The no-smuggling invariant is not satisfied by a snapshot containing unreviewed work.

**Required follow-up:** bind target, approval, zero findings, review scope and applicable historical anchor as one unique, consistent acceptance record. Refuse both native and migrated contradictory anchors and unsupported broad projections. Retain exact scalar/type/identity/ancestry gates and historical records; current edits must not manufacture old acceptance. No expansion to authenticated reviewer identity is requested.

## R5 — MEDIUM — Historical owner decision and satisfaction can be rewritten after the fact

**Still open.** Native decision-anchor validation checks block equality only. Both historical branches omit validation of the anchor's unblock field; `_verify_unblock_condition` is called only on the current issue (line 1408).

- `self_native_anchor_pending_rewritten`: the historical native block claims EFFECTIVE while its decision body expressly says NOT approved/pending. Replacing only current prose with a positive body makes the old anchor pass and excludes the SELF issue.
- `self_legacy_unblock_rewritten`: historical positive decision prose is accompanied by `PENDING - awaiting owner approval`. A later migration claims SATISFIED at that anchor and rewrites the current field. The anchor's contrary satisfaction record is never checked; submission advances.
- `self_native_unblock_rewritten`: the same pending-to-satisfied rewrite succeeds with an unchanged native block, so the gap is not confined to legacy migration.

The current `has NOT authorized` control refuses, as do retained declined/denied/duplicate/pending variants. A newly appended contradictory second structured block refuses. These lexical/schema improvements cannot close a historical-effectiveness gap. SELF remains empty-scope/own-file-only, limiting impact but not proving effective owner authority.

**Required follow-up:** establish a unique effective decision and satisfied condition at the claimed historical point, and reject contradictory, pending, duplicate, revoked or retrospectively rewritten evidence for both classes. Keep SELF's own-file boundary. Rework remains governed by accepted invariants; any new authority or architecture must be approved before implementation.

## Machine-fact provenance and architectural/scope audit

**CONFIRMED:** Native block identities, scalar schemas and Git ancestry are checked against committed content. Missing/duplicate blocks, pending/rejected current state, invalid datetime/marker counts, mismatched native fields, wrong target/identity, current duplicate satisfaction and earlier merge/coverage controls refuse. The gate reads current issue blocks but submission requires a clean HEAD target, so these reproductions commit their forged projections before invoking the real CLI; none depends on dirty files or bypassing HEAD equality.

**CONFIRMED:** Historical scope still comes from the current projection under a negative-word veto, rather than from facts positively established at the historical anchor. Native anchors lend a block's identical fields without checking their then-existing contradiction; current-only checks let later edits erase the conflict operationally while Git retains it. The restored REJECTED record also demonstrates missing authority continuity between anchor and work. The declared set and derived Git set matching does not cure these authority defects.

**INFERRED architecture classification:** strict blocks/root-local verification remain ALIGNED with accepted architecture, but the exercised historical binding and contradiction behavior is UNJUSTIFIED_DRIFT from fail-closed/no-smuggling and the owner's prohibition on permissive prose heuristics. The checkpoint's statement that binding is enforced “rather than by adding prose heuristics” is not supported by the new clause/keyword verifier. This evidence records the contradiction without rewriting the implementer's authored claim.

The complete rework changes five files: specification, pipeline ADR, code, pipeline tests and owning issue. The follow-up reconciliation changes three record files only. Specification/ADR additions correspond to the recorded 2026-10-12 owner directive and strengthen PIPELINE-010; they do not change the milestone JSON, ten invariants, schemas, state edges, target==HEAD rule, package, live tooling, dependency or external interface. No separate unauthorized specification or architecture expansion was found. The added “no express exclusion” wording is a necessary consistency check under the still-binding requirement to project only facts actually carried by the historical record; it is not authority to treat absence of a denial as scope approval. New permissive behavior remains a defect, not an accepted exception.

## R1/R4 and real A/B verification

Retained hidden-touch, post-review merge, asymmetric-parent, octopus substantive, uncovered-touch, overlap, same-issue, range widening, rename, delete/re-add, null/malformed/in-scope registry checks were replayed. The new sibling-authority control refuses because substantive work lacks the authority ancestor. The new mixed-authority merge has complete parent-touch discovery but false attribution (R2). The separate positive octopus calibration passes. `_commit_paths`, `_verify_target_scope` and `_parse_intervening_registry` ASTs remain unchanged from pre-rework `301bc45` to target. No R1/R4 regression observed in these bounds; all refusal paths tested preserve files/state.

Actual A/B verification is read-only component characterization against historical candidate `9f72d3de57085525a8ddf8a3b14bf1a3161e26e8`, base `88fa8359ec3a62f200096d0d96bd04a88ebd118a`, not discovery submission or a target==HEAD exception. The harness uses target code and confirms A/B issue bytes equal their target versions; independent explicit-parent diffs agree for every touching commit. [Raw results](scope-attribution-review-round-5/baseline-results.json) retain both entries, all six outside paths and their covering commits, metadata and machine state.

- A: decision anchor `47a0cb40684ad8edc1d574eba28ded610ea2ba93` contains the bounded positive blocked-exit approval and its four substantive file changes. Review anchor `79063cb2201517567c3a8fe9702fd59ca41e9e5d` records APPROVED/0 on `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3`, with scope covering that amendment and resume. Direct `git show <anchor>:<issue>` inspection confirms the migration's actual scope and facts; post-review work is record-only.
- B: decision anchor `610c672082a44e591a13822ffc12a9aa58babadb` records the bounded owner authorization and satisfied authority gate, preserving the separate execute-now gate. Empty decision scope and own-issue-only exclusion are consistent. No new execution/resource authorization follows from this characterization.
- Both entries pass v5; all six paths are covered exactly once, removing A exposes five and removing B one, existing entries cannot cover hypothetical AGENTS work. Discovery contract/digest/state/registry bytes remain unchanged. A/B migration records themselves are unchanged by this rework and reviewer.

Honest actual A/B support does not validate the general verifier against the retained counterexamples.

## Limitations, records and stopping boundary

Darwin/Python 3.9, deterministic local fixtures and bounded Git graphs only; no exhaustive Markdown/Unicode/history space, authenticated identity or concurrent-writer guarantee. Dedicated `markdownlint`, `markdownlint-cli2` and `pymarkdown` are unavailable; structural validation plus local link/fence/newline/whitespace checks are not a full Markdown linter. No live-agent probe, discovery conformance/oracle rerun or network operation was run. Fixture Git objects are temporary; clone-resident scripts/results reconstruct them. Artifact identity is supplied by the reviewer commit tree (`git log --` this evidence), not an external retention claim.

Inherited non-material O2 indirect exclusion provenance, O3 role-contract direct-parent wording and O4 strict milestone-parser prose collision remain outside this repair scope. O5/O6 are resolved within the original-case checks. The ordinary amendment parser reads this appended review; no milestone transition is appropriate. The conservative octopus fixture mismatch is disclosed above and does not reopen the independently verified merge enumeration mechanism.

Persisted outputs are reviewer evidence, an appended owning-issue Round 5, reconciled HANDOFF and an attributable checkpoint update. CHANGES_REQUIRED keeps the ordinary amendment IMPLEMENTING; findings are not accepted debt. No implementation/specification/ADR/test/package/A/B/discovery record changes, registry addition, milestone acceptance/closure, discovery implementer, recorder/coordinator or later-role work is performed. Reviewer records are committed locally, with no push.

Separate post-write reads and governance outputs are retained in [governance-readback.json](scope-attribution-review-round-5/governance-readback.json). Reproduce record checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-5/check_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
```

Governance validation checks record integrity and scope, not implementation approval. Stop after recording this disposition and validation; the next bounded work is resolution of R2/R3/R5 within owner authority by a separate implementer, followed by fresh independent review.
