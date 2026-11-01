# 50: Remove address-sharing context

Type: build
Status: resolved
Blocked by: none
Blocks: 25, 26
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)
Rigour: Tier 3

## What to build

Remove address-sharing context from the system, by the author's T25 gate ruling of
1 November 2026. The radius no longer returns the office and VPN co-users of an account's
addresses, the answer key no longer records them, and nothing downstream can pass them to the
model. Account context, assets, device peers and the shared date handling are unchanged.

## Decisions implemented

- Author's T25 gate rulings, 1 November 2026: the office/VPN co-user list adds no useful
  evidence to the current investigation; no allocation evidence is added (AUD-073); remove
  address-sharing context everywhere. Suspicious-address investigation remains supported by
  `search_logins(ip=...)` and the spray finding. See
  [T25 Comments](25-peers-and-corpus-search-tools.md),
  [research note 25](../research/25-shared-address-value.md) and the spec's decision-log row of
  that date.
- Supersedes T19 decisions 3 and 5 (address-reuse context retained and grouped by address).
  T19 decision 2 (VPN address meaning) and decision 4 (relationship dates) stay.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used. Done 1 November 2026: the author ruled
      to build on Claude Fable 5.1, above the standard line (see Comments).
- [x] Before build work, the author rules whether network nodes and their `used_address` edges
      stay in the graph once nothing reads them. Ruled 1 November 2026: keep nodes, drop edges
      (see Comments and the spec's decision log).
- [x] The graph build draws no `used_address` edges, and the peer query offers only
      `used_device`. Network nodes and their `mentions` links are unchanged. The integrity
      check asserts that no `used_address` edge exists, and a corruption test proves it refuses
      a graph that has one. Organisation inspection counts are recomputed and recorded.
      Evidence: `graph_ingestion.py` draws device edges only; `neo4j_graph._device_peers` is the
      one peer query; `graph_verification.py` refuses by name; `test_graph_verification` plants a
      `used_address` edge and is refused. Counts: 141 such edges before, 0 after; organisation
      170 nodes, 185 relationships (was 326); mentions unchanged at 257.
- [x] The generator no longer writes `address_reuse_context` into `truth.json`; every other part
      of the answer key is byte-identical. A test proves it. Evidence: the committed file
      normalised with the key removed equals the regenerated file; `test_committed_files_match_
      the_generator` and the key-set assertion in `test_vpn_pool_is_shared_and_answer_key…`.
- [x] The radius in `knowledge_base/radius.py` returns no address-sharing context, and its walk
      and neighbourhood carry no address paths. S6 still recomputes exactly against the answer
      key: two groups, seven assets, no device peers. Evidence: `test_s6_radius_matches_the_
      planted_answer_key`, and the 50-prepare parity run (10 findings, 40 dated radii equal).
- [x] Tests that asserted address-reuse context are updated or removed, not skipped. Native
      inspection's S6 counts are recomputed from the new neighbourhood and recorded. Evidence:
      five test files updated, none skipped; S6 is 10 nodes and 9 relationships (was 55 and 64).
- [x] Retrieval evaluation gold is unchanged; a test or the existing door 6 test proves K04 still
      equals S6's planted radius. The frozen question file is not edited. Evidence:
      `test_eval_retrieval` door 6 tests passed on the new code; the question file is untouched
      in the diff.
- [x] A new paired build from the changed dataset is made and activated by restart, following
      `docs/admin-manual.md`; the current pair stays retained for rollback. All saved
      investigations reopen identically through the normal API. Evidence: build
      `f937ea5949f44cfb97f0f9e62920a4ee` ([50-preparation.json](../research/50-preparation.json)),
      0 provider calls; selected with `select_graph_version`, previous `3d58516c…` retained;
      backend restarted; overview, listing and all 25 saved investigations byte-identical.
- [x] Historical evidence (`.graph-versions/` contexts, the legacy recovery bundle, earlier
      research files) is left unchanged. Evidence: `git status` shows only the two new T50
      research files as untracked; no earlier research file or retained version is modified.
- [x] `GLOSSARY.md` and the admin manual are checked for address-sharing wording and updated if
      present. Evidence: the glossary has no such entry (only T43's "Address activity", which
      stays); the manual's section 6 and section 5 rollback note updated.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are
      clean under the type checker, and the two-axis code review (`mp-code-review`) has run with
      its findings triaged. The Port's eval is not required: no agent behaviour changes.
      Evidence: full backend run 661 passed, 2 failed in 17 min 13 s, both failures outside
      T50's files and both passed in the isolated rerun with the edited verification test
      (3 passed in 5 min 26 s); logged as B-135 and B-136 (AUD-075). Frontend 150 passed.
      Ruff and Pyright clean. Review triaged in Comments. See
      [50-verification.json](../research/50-verification.json).

## Comments

- 2026-11-01 — Build evidence. Code: `radius.py` (dataclasses and neighbourhood), `neo4j_graph.py`
  (`_device_peers`), `graph_ingestion.py`, `graph_verification.py` (named refusal),
  `inspection.py` (style), `generator.py`; dataset regenerated (only `truth.json` changed).
  Affected tests: 23 passed in 6 min 19 s outside the sandbox, since the Docker socket is denied
  inside it; `test_generator` 32 passed. Ruff and Pyright clean. Frontend: 150 passed. The new
  pair was prepared by [50-prepare.py](../research/50-prepare.py), which reads the previous pair
  directly because the new integrity check refuses it by design, and reuses its 320 passage
  vectors. Consequence recorded in the admin manual: pairs built before T50 cannot be opened by
  the current code, so rollback to `3d58516c…` or `eb6c7d59…` also needs the earlier code.
  Noticed, not changed (byte-identical criterion): `truth.json` keeps `basis` and
  `used_address_filter` strings that describe the removed edges; a follow-up may reword them.
  Open flags for the author: spec phase 1 "spread and shared ground" (research note 01 defines
  shared ground as device or source network; now device only); the draft Graph tab schema still
  lists node type `network`.

- 2026-11-01 — `mp-code-review` against `012de46`, findings triaged. Standards axis: README
  line 108 still described shared-address context (fixed); the manual's rollback note named a
  commit that did not exist yet (reworded: two-step rollback, retained pair plus earlier code);
  `used_address_filter` and `basis` in the answer key now name a filter nothing applies
  (judgement; held by the byte-identical criterion, author's ruling requested); the named
  `used_address` refusal duplicates the exact comparison (kept: the criterion asks for it);
  `test_dates_filter…` lost its positive dated-window witness (fixed: a positive dated device
  witness added to `test_graph_verification`, window 11:00 to 11:02 keeps emily.foster);
  `hasattr` assertions are structural only (kept beside the JSON scan and key-set assertions).
  Spec axis: same answer-key wording conflict (criterion versus spec line 540, author to rule);
  rollback wording (fixed as above); K04 proof is indirect through the walk gate (accepted, the
  door 6 test is what the criterion names); counts now recorded here; the two new research
  files are the build evidence and are kept.

- 2026-11-01 — Model used: Claude Fable 5.1 (Claude Code). The builder reported the ticket's
  standard `Model:` line; the author ruled to build on Fable 5.1 instead, and to commit the
  rationale clarification first (commit `012de46`). Build started after that ruling.
  Process gap, noticed by the author mid-build: the `implement` skill was not used; the builder
  read the ticket and built directly, and the skill was absent from this session's skill list.
  The author ruled to continue and close with the same gates: full safety net, type checker,
  `mp-code-review` with findings triaged.

- 2026-11-01 — Author-approved rationale clarification: the removal concerns the office/VPN
  co-user list, not address correlation in general. Suspicious-address investigation remains
  supported by the existing log tool and spray finding. Scope and acceptance criteria unchanged.

- 2026-11-01 — Opened by the author's approval of the T25 gate edits. Changing `truth.json`
  makes the live build stale under the T18 fingerprint, so this ticket includes a new paired
  build and activation. Flagged, not decided: whether the spec's phase 1 phrase "spread and
  shared ground" refers to addresses; check research note 01 before changing it.

- 2026-11-01 — Author's pre-build ruling: keep network nodes, drop `used_address` edges.
  Reason: after the T25 removal the radius was the edges' only reader; keep facts about the
  world and remove derived links nobody reads. The graph is rebuilt from source and the log
  keeps every sign-in, so a later phase can redraw the edges. Network nodes stay as
  organisation facts with their `mentions` links (17 documents name the UK or US office).
  Spec updated: the edge rule, the integrity table row, door 7 and a decision-log row. The
  admin manual's Browser section still describes the purple `used_address` relationship; this
  ticket updates it with the tested commands. Mislinking risk from name matching is AUD-074.
