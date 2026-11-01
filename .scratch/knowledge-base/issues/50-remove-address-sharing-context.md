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

- Author's T25 gate rulings, 1 November 2026: sharing an address answers no investigation
  question in this app; no allocation evidence is added (AUD-073); remove everywhere. See
  [T25 Comments](25-peers-and-corpus-search-tools.md),
  [research note 25](../research/25-shared-address-value.md) and the spec's decision-log row of
  that date.
- Supersedes T19 decisions 3 and 5 (address-reuse context retained and grouped by address).
  T19 decision 2 (VPN address meaning) and decision 4 (relationship dates) stay.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Before build work, the author rules whether network nodes and their `used_address` edges
      stay in the graph once nothing reads them. Record the ruling here.
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

- 2026-11-01 — Opened by the author's approval of the T25 gate edits. Changing `truth.json`
  makes the live build stale under the T18 fingerprint, so this ticket includes a new paired
  build and activation. Flagged, not decided: whether the spec's phase 1 phrase "spread and
  shared ground" refers to addresses; check research note 01 before changing it.
