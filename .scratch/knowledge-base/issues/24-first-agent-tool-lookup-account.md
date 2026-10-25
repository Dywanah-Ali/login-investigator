# 24: The first agent tool end to end

Type: build
Status: ready-for-agent
Blocked by: 19
Phase: 0

## What to build

The analyst asks "whose account is this?" in chat, and the agent answers through `lookup_account`:
the account's owner, department and privilege groups from the graph. This is the tracer bullet for
every knowledge-base tool: typed and read-only, it returns short content for the model and a full
artifact for the eval and the screen, its result is fenced, and the artifact survives the memory
round trip.

## Decisions implemented

- T05 d1 (seven typed tools in one tuple; `lookup_account(account_id)` first), T05 d4 (content plus
  artifact, the artifact never sent to the model), T05 d8 (the fence in one wrap-tool-call
  middleware; the untrusted-data rule added to the system prompt as written), T02 d8 (the agent's
  read-only role), T05 conditions (the artifact survives the SQLite round trip).
- Project rules: the tool list comes from one place; the model and agent are created in exactly one
  function each.
- User stories 8, 15, 30, 68. Spec door 3.

## Acceptance criteria

- [ ] `lookup_account(account_id)` sits in the one tool tuple and connects through the read-only
      role.
- [ ] It returns short labelled content for the model and a full artifact; a test proves the artifact
      never reaches the model.
- [ ] One wrap-tool-call middleware fences every tool result, the Port's three included, labelled
      with source and trust level; one test proves it.
- [ ] The untrusted-data rule of T05 d8 is in the system prompt as written.
- [ ] A test proves the artifact survives the SQLite checkpointer round trip.
- [ ] Agent tests use the fake model.
- [ ] The system prompt changed, so the Port's eval is run and passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
