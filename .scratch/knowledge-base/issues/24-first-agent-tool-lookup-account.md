# 24: The first agent tool end to end

Type: build
Status: resolved
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

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] `lookup_account(account_id)` sits in the one tool tuple and connects through the read-only
      role.
- [x] When a build exists, app startup opens the core knowledge base and builds/checks its graph
      once per backend process before requests are accepted. The first and subsequent tool calls,
      across investigations, reuse that instance. Door-4 lifecycle tests prove this and prove
      integrity failure prevents startup; retain the existing no-build startup behaviour.
- [x] Shutdown closes the knowledge-base context and engine/pool, including startup-failure
      cleanup. Connections are borrowed for database queries, never held per conversation.
      Record measured graph preparation time. A rebuilt dataset is adopted on restart and
      checked again; no file watcher or automatic hot replacement.
- [x] It returns short labelled content for the model and a full artifact; a test proves the artifact
      never reaches the model.
- [x] One wrap-tool-call middleware fences every tool result, the Port's three included, labelled
      with source and trust level; one test proves it.
- [x] The untrusted-data rule of T05 d8 is in the system prompt as written.
- [x] A test proves the artifact survives the SQLite checkpointer round trip.
- [x] Document the lookup artifact's fields and persistence path, including what goes to the
      model and what stays in saved evidence.
- [x] With a fake model and disposable SQLite memory, record storage at baseline and after
      1, 10 and 50 repeated lookups in one conversation. Include checkpoint/intermediate-write
      counts and stored bytes as well as database file size; state the measurement method.
      This is a baseline for AUD-065, not a new performance threshold.
- [x] Close and reopen memory and prove the original lookup artifact is preserved without
      querying the knowledge base again. This strengthens the existing round-trip criterion.
- [x] Run the existing report restart/download test to confirm saved reports remain
      downloadable without a model. No new PDF-storage mechanism is introduced.
- [x] Agent tests use the fake model.
- [x] Browser accepts `lookup_account` progress in the existing status line and displays its
      saved tool result with a readable label; a fake-API screen test proves stream completion.
- [x] The system prompt changed, so the Port's eval is run and passes.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-28, author ruling after the T19 walkthrough: prepare and integrity-check the graph at
  backend startup, then reuse it. The author raised first-question latency from lazy loading.
  This ticket owns app/agent integration; T19 remains closed and its core opening is reused.
  Lifecycle tests extend this ticket's coverage to the already agreed door 4 as well as door 3.

- 2026-10-29: author confirmed Astra is set. Discussion and read-only persistence inspection
  only; no build go yet. Registered the author's deferred storage-scaling concern as AUD-065.
  Proposed addition awaiting approval: document artifact fields/storage path, measure repeated
  lookups in disposable SQLite memory, and prove close/reopen preserves original evidence
  without querying the source again. Preserve existing report-download behaviour. No retention,
  pruning, migration or separate artifact store is authorised by this proposal.

- 2026-10-29: author approved the four persistence checks above in chat after the approval
  popup failed to remain visible. Spec Testing Decisions and its decisions log updated.
  AUD-065's broader storage work stays deferred. This approval adds acceptance criteria;
  application build has not started.

- 2026-10-29: author invoked implement T24 with Astra confirmed. Build authorised on current
  branch. TDD at pre-agreed doors 3 and 4, with the existing core door reused. Review baseline:
  `3993679` plus this session's approved specification changes. No push authorised.

- 2026-10-29 — Codex: langchain-core 1.4.0 and LangChain 1.3.1; Context Hub
  `langchain/core` and [official tools](https://docs.langchain.com/oss/python/langchain/tools)
  / [custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom);
  checked typed tools, content/artifact separation and wrap-tool/model-call hooks, supplemented
  by installed source for `content_and_artifact` and request overrides. FastAPI installed version
  0.143.1: Context Hub `fastapi/package` covers 0.136.3, so supplemented with the
  [official lifespan documentation](https://fastapi.tiangolo.com/advanced/events/).
  Checked resource lifetime before/after yield; existing application lifespan is retained.
  Runtime behaviour is separately verified by the startup/restart/cleanup tests.

- 2026-10-29: author approved moving the minimal `lookup_account` progress-name support and
  saved tool label forward from T36 after inspection found the old parser would abort its stream.
  Existing single status line only; no step stack or evidence panel.

- 2026-10-29: implementation complete with the evidence below. The full backend command
  passed all 677 test assertions but exited 1 on two known B-094/AUD-061 fixture teardowns.
  Both exact temporary databases were verified idle and dropped without FORCE; both affected
  tests reran clean (2 passed, exit 0). No fixture or privileges changed. This qualification is
  retained with the standing safety-net evidence, following the T22 cleanup treatment.

## Answer

Follow-up, 30 October 2026: the author tested account lookup in the GUI and liked the result.
Requested two-space JSON indentation in both Found and the raw-JSON view. This is a display-only
formatting change to the saved briefing; model input, artifacts and original saved messages stay
unchanged. Existing saved investigations receive the formatting when reopened. B-106 records
the compact display that prompted the request.

Second GUI ruling, 30 October 2026: the author accepted indented JSON behind the raw switch,
but found JSON under Found visually inappropriate. Approved a plain summary there: Owner,
Department, then Groups with standard/privileged access labels. This supersedes only the Found
format from the first iteration. Saved messages, artifacts and model input remain unchanged.

Polish verification, 30 October: full backend safety-net run passed 677 tests (415.65 seconds,
exit 0; no teardown errors this run), frontend 150 passed. After the second Found-format ruling,
the affected tool-view/API tests passed again (13), and live reads verified the plain summary
plus indented raw JSON on two existing saved lookups. Pyright clean. Both independent reviewers
rechecked the final formatter with zero findings. No agent eval rerun: model inputs, tool output
and prompts are unchanged. The backend was restarted so the approved display is available live.

`lookup_account(account_id)` is the first knowledge-base tool in the central tuple, bound at
agent construction to the checked core instance. It accepts a username or stable person ID,
returns copied owner/department/group evidence and membership paths, and never writes the graph.
The app opens the core with the separate reader role, prepares/checks once before serving,
reuses across investigations, closes the context/pool on shutdown or failed startup, and adopts
a rebuild only on restart. No build retains the existing startup behaviour.

One wrap-tool-call hook fences all four registered tools with source and trust labels. The
existing policy and tool views read the original payload through one decoder, so log/reputation
behaviour remains intact. The exact graph/corpus untrusted-data rule is in the system prompt.
Model calls receive message copies without artifacts; saved state retains full evidence,
including across close/reopen and follow-up turns. Report generation uses text only, and saved
report downloads remain independent of the model.

The author-approved compatibility change adds account-lookup progress to the existing status
line and labels its saved result. T36 retains the remaining new tool names and step stack.

### Evidence

- `uv run pytest -q`: **677 passed, 2 teardown errors**, 353.17 seconds, exit 1. Both errors
  were unchanged tests with the known permission-to-terminate failure (B-094/AUD-061).
  Exact idle-database cleanup succeeded; affected rerun: **2 passed**, 2.76 seconds, exit 0.
- Door 3/4: `tests/test_kb_agent.py`, **11 passed**. Covers model-input separation, all-tool
  fences, readonly identity/write refusal, once-only preparation, shutdown/failure cleanup,
  corruption refusal, evidence reopening without a source query, and rebuild adoption on restart.
  Earlier combined agent/policy run: **40 passed**; startup/report/tools run: **48 passed**.
- `uv run pyright`: **0 errors**. Explicit Pyright run on the research probe: **0 errors**.
- Frontend: **150 passed**; typecheck clean; lint retains only the six existing AUD-009 warnings.
  The lookup stream test failed before the allowlist fix, then both old/new progress cases passed.
- Port API eval: **62/63 overall, 15/15 security**, targets met, fingerprint `fa8f3e8f`.
  `backend/evals/results/2026-10-29-204751-654728-fa8f3e8f.json`. Q04 run 1 stays failed;
  attribution-check concern recorded as B-105/AUD-066, no grader change or cleaner-score rerun.
- Live isolated API lookup selected the tool and correctly returned Amelia Ward, IT, All Staff
  (baseline), IT Admins (privileged): [saved evidence](../research/24-live-lookup.json).
- [Persistence evidence](../research/24-persistence-evidence.md) documents artifact contents,
  storage and the tested command. One artifact: **601 bytes**. File after 1/10/50 lookups:
  **40,960 / 811,008 / 16,404,480 bytes**. Graph preparation **4.9589 seconds**; reopening
  **0.0181 seconds**. Single observations, not performance gates. AUD-065 stays deferred.
- [Two-axis review](../reviews/24-code-review-2026-10-29.md): Standards had one documentation
  finding, fixed and independently confirmed; Spec had zero findings. No unresolved review item.
- Admin manual section 3 documents the measured probe and restart behaviour. Probe command
  tested as written. Bugs B-102 to B-104 fixed; B-105 and existing AUD-061 remain recorded.

Model: author-confirmed Astra. Local commit only; no push. T25 is next; T45 still blocks T26.
