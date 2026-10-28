# 24: The first agent tool end to end

Type: build
Status: ready-for-agent
Blocked by: 19
Phase: 0
Model: strongest (Fable 5.1 or Astra)

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

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `lookup_account(account_id)` sits in the one tool tuple and connects through the read-only
      role.
- [ ] When a build exists, app startup opens the core knowledge base and builds/checks its graph
      once per backend process before requests are accepted. The first and subsequent tool calls,
      across investigations, reuse that instance. Door-4 lifecycle tests prove this and prove
      integrity failure prevents startup; retain the existing no-build startup behaviour.
- [ ] Shutdown closes the knowledge-base context and engine/pool, including startup-failure
      cleanup. Connections are borrowed for database queries, never held per conversation.
      Record measured graph preparation time. A rebuilt dataset is adopted on restart and
      checked again; no file watcher or automatic hot replacement.
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

- 2026-10-28, author ruling after the T19 walkthrough: prepare and integrity-check the graph at
  backend startup, then reuse it. The author raised first-question latency from lazy loading.
  This ticket owns app/agent integration; T19 remains closed and its core opening is reused.
  Lifecycle tests extend this ticket's coverage to the already agreed door 4 as well as door 3.
