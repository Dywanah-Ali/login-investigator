# 51: Reword the S6 answer key's leftover address sentences

Type: build
Status: ready-for-agent
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

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `generator.py` writes the reworded `basis` and no `used_address_filter`; the key-set
      assertion in `test_generator.py` is updated; every other part of `truth.json` is
      byte-identical to the T50 key, shown by the same normalised comparison T50 used.
- [ ] The S6 radius still recomputes exactly against the key (existing tests).
- [ ] A new paired build from the changed dataset is made, reusing the T50 pair's passage
      vectors with no provider calls (follow `research/50-prepare.py`), selected and activated
      by restart per the admin manual; the T50 pair `f937ea59…` stays retained for rollback;
      all saved investigations reopen identically through the normal API.
- [ ] The eval question file is not edited; the door 6 tests pass.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, Pyright and Ruff are
      clean, and `mp-code-review` has run with its findings triaged. The Port's eval is not
      required: no agent behaviour changes.

## Comments

- 2026-11-01 — Opened at T50's close from the two-axis review's finding (Standards: Mysterious
  Name on `used_address_filter`; Spec: conflict with spec line "the answer key ... carry no
  address-sharing context"). See [T50 Comments](50-remove-address-sharing-context.md).

- 2026-11-01 — Author prioritised completing this ticket before T52, so the objectives and
  reliability review starts from the cleaned answer key and verified active pair. Scope and
  acceptance criteria are unchanged; this priority ruling does not start implementation.

- 2026-11-01 — Model: Claude Opus 5.5, matching the ticket's standard line. The builder named the
  line; the author set the model with `/model` and confirmed before build work started.
