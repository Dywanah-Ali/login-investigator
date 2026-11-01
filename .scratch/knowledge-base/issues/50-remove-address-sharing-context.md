# 50: Remove address-sharing context

Type: build
Status: ready-for-agent
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

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] Before build work, the author rules whether network nodes and their `used_address` edges
      stay in the graph once nothing reads them. Ruled 1 November 2026: keep nodes, drop edges
      (see Comments and the spec's decision log).
- [ ] The graph build draws no `used_address` edges, and the peer query offers only
      `used_device`. Network nodes and their `mentions` links are unchanged. The integrity
      check asserts that no `used_address` edge exists, and a corruption test proves it refuses
      a graph that has one. Organisation inspection counts are recomputed and recorded.
- [ ] The generator no longer writes `address_reuse_context` into `truth.json`; every other part
      of the answer key is byte-identical. A test proves it.
- [ ] The radius in `knowledge_base/radius.py` returns no address-sharing context, and its walk
      and neighbourhood carry no address paths. S6 still recomputes exactly against the answer
      key: two groups, seven assets, no device peers.
- [ ] Tests that asserted address-reuse context are updated or removed, not skipped. Native
      inspection's S6 counts are recomputed from the new neighbourhood and recorded.
- [ ] Retrieval evaluation gold is unchanged; a test or the existing door 6 test proves K04 still
      equals S6's planted radius. The frozen question file is not edited.
- [ ] A new paired build from the changed dataset is made and activated by restart, following
      `docs/admin-manual.md`; the current pair stays retained for rollback. All saved
      investigations reopen identically through the normal API.
- [ ] Historical evidence (`.graph-versions/` contexts, the legacy recovery bundle, earlier
      research files) is left unchanged.
- [ ] `GLOSSARY.md` and the admin manual are checked for address-sharing wording and updated if
      present.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are
      clean under the type checker, and the two-axis code review (`mp-code-review`) has run with
      its findings triaged. The Port's eval is not required: no agent behaviour changes.

## Comments

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
