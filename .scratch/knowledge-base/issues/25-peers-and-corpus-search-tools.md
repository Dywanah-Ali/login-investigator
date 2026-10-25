# 25: Peers and corpus search as tools

Type: build
Status: ready-for-agent
Blocked by: 22, 24
Phase: 0

## What to build

The analyst asks "who else uses this laptop?" or "what does our policy say about MFA exceptions?",
and the agent answers through `find_peers` or `search_corpus`. Both follow the tracer bullet of
ticket 24: typed, read-only, fenced, short content for the model and a full artifact.

## Decisions implemented

- T05 d1 (`find_peers(account_id | device_id | network)` and
  `search_corpus(question, doc_type, technique_id)`), T05 d4 (content plus artifact), T05 d12
  (package caps: five chunks per search, peers paged with a `truncated` flag, full lists in the
  artifact), T03 d6 (the model picks typed options; code builds the filter; the model never writes
  one), T03 d1 (the verdict travels with the chunks).
- User stories 8, 17, 28. Spec door 3.

## Acceptance criteria

- [ ] `find_peers` returns the users sharing a device or a network address that week, from the graph,
      paged with a `truncated` flag; the full list is in the artifact.
- [ ] `search_corpus` takes typed options, builds the filter in code, and returns the verdict with up
      to five chunks; the artifact records every score.
- [ ] Both are in the one tool tuple and their results are fenced.
- [ ] Agent tests use the fake model.
- [ ] The Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
