# 51: Reword the S6 answer key's leftover address sentences

Type: build
Status: resolved
Blocked by: 50
Blocks: none
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)
Rigour: Tier 3

## What to build

T50 removed address-sharing context from the graph, the radius and the answer key, but its
byte-identical criterion left two sentences in `truth.json` under `scenarios.S6.blast_radius`
that were written for the removed feature:

- `basis` ends with "shared address is context, not proof of compromise."
- `used_address_filter` describes the row filter for `used_address` edges, which the build no
  longer draws.

Reword `basis` so it describes only what the key still records (planted memberships, the grant
plan, the VPN hand-out order, the unregistered attacker device) and drop `used_address_filter`.
Keep `network_id` and `network_address`: the VPN address meaning (T19 decision 2) still stands.
Everything else in the key stays byte-identical. Then build and activate a new pair, because the
changed key changes the source fingerprint (T18).

## Decisions implemented

- Author's ruling, 1 November 2026, at T50's close: reword in a small follow-up rather than
  leave the strings or fold them into T25. Reason: the spec says the answer key carries no
  address-sharing context (spec, "Address-sharing context removed"); T50's byte-identical
  criterion and that rule conflicted, and the author chose the spec's side with a clean record.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used. Evidence: Comments, 1 November 2026,
      Claude Opus 5.5.
- [x] `generator.py` writes the reworded `basis` and no `used_address_filter`; the key-set
      assertion in `test_generator.py` is updated; every other part of `truth.json` is
      byte-identical to the T50 key, shown by the same normalised comparison T50 used.
      Evidence: the T50 key and the regenerated key, each with `basis` and
      `used_address_filter` deleted and keys sorted by `jq -S`, compare identical with `cmp`;
      the `truth.json` diff is those two lines only. The test now pins the key set and the full
      `basis` text. `test_generator` 32 passed.
- [x] The S6 radius still recomputes exactly against the key (existing tests). Evidence:
      `test_s6_radius_matches_the_planted_answer_key` in the full run, and 51-prepare's check of
      groups, assets, paths and device peers against the new key.
- [x] A new paired build from the changed dataset is made, reusing the T50 pair's passage
      vectors with no provider calls (follow `research/50-prepare.py`), selected and activated
      by restart per the admin manual; the T50 pair `f937ea59…` stays retained for rollback;
      all saved investigations reopen identically through the normal API. Evidence: build
      `2d1bf85ead1944709f5ab8cbd6ed4ad1` ([51-preparation.json](../research/51-preparation.json)),
      0 provider calls, parity on 320 passages, graph counts, 50 accounts, 10 findings and 40
      dated radii; selected with `select_graph_version`, previous `f937ea59…`; backend restarted;
      overview, alerts, listing and all 25 saved investigations byte-identical through the API.
- [x] The eval question file is not edited; the door 6 tests pass. Evidence: the question file
      is absent from the diff; `test_eval_retrieval` passed in the full run.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, Pyright and Ruff are
      clean, and `mp-code-review` has run with its findings triaged. The Port's eval is not
      required: no agent behaviour changes. Evidence: backend 663 passed, 0 failed in 14 min
      9 s; frontend 150 passed; Pyright and Ruff clean over the backend. Review triaged in
      Comments. See [51-verification.json](../research/51-verification.json).

## Comments

- 2026-11-01 — Opened at T50's close from the two-axis review's finding (Standards: Mysterious
  Name on `used_address_filter`; Spec: conflict with spec line "the answer key ... carry no
  address-sharing context"). See [T50 Comments](50-remove-address-sharing-context.md).

- 2026-11-01 — Author prioritised completing this ticket before T52, so the objectives and
  reliability review starts from the cleaned answer key and verified active pair. Scope and
  acceptance criteria are unchanged; this priority ruling does not start implementation.

- 2026-11-01 — Model: Claude Opus 5.5, matching the ticket's standard line. The builder named the
  line; the author set the model with `/model` and confirmed before build work started.

- 2026-11-01 — Build evidence. `basis` now reads "Planted memberships, grant plan and VPN
  hand-out order. The attacker device is unregistered and supplies no device peer edge."
  `used_address_filter` is gone; `network_id` and `network_address` stay. The new pair was
  prepared by [51-prepare.py](../research/51-prepare.py). Unlike T50's script, it opens the
  previous pair through the normal checked path, because the T50 pair has no address edges.
  Rollback to `f937ea59…` therefore needs no earlier code.

- 2026-11-01 — `mp-code-review` against `676c593`, findings triaged. Spec axis: no missing
  requirement, no scope creep, no wrong implementation. Standards axis, no hard violation;
  five judgement calls. Fixed: the substring check on `basis` became an exact-text assertion;
  the parity helper was renamed `parity_snapshot`. Kept: the script duplicates 50-prepare's
  blocks (each one-time script stays self-contained as evidence); the S6 spray is picked by
  its address, as in 50-prepare; ticket-tagged test comments follow the file's style. Noticed,
  not changed: Ruff reports unused `noqa` and a blocking `open` in the research script, the
  same kind it reports in 50-prepare; research scripts sit outside the backend's lint scope.
