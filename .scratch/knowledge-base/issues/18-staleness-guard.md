# 18: The staleness guard

Type: build
Status: resolved (28 October 2026)
Blocked by: 17
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

The app never answers from an old world. Every build records a fingerprint of the dataset folder's
files and the embedding and chunking settings. At startup the app recomputes the fingerprint; when
it does not match the database, the server does not start, and its message names the build command.

## Decisions implemented

- [spec ruling] the staleness guard; [review ruling 6] a stale database stops the server from
  starting, with fixed text naming the build command and never echoing a path.
- API contract change 5 (the error part).
- User story 66.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] Each build records a fingerprint of the dataset folder's files with the embedding model, the
      vector length and the chunking settings.
- [x] At startup the app recomputes the fingerprint from the folder.
- [x] On a mismatch the server does not start; the failure carries fixed text naming the build
      command and no path. No endpoint answers.
- [x] On a match the server starts as before.
- [x] What happens when no database has been built yet is decided, consistent with the guard, and
      recorded under this ticket's Answer.
- [x] Door 2 test: the guard refuses a database built from a changed file. Door 4 test: the startup
      test proves the server refuses to start.
- [x] The API contract records the startup failure.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Answer

**Decision 1 (author, 28 October 2026): no build yet means the server starts without the
knowledge base.** When the build pointer file is absent, startup marks the knowledge base "not
built" and continues. The startup log says so in fixed text and names the build command. The
dashboards and the Port's agent work as before. Knowledge-base tools from later tickets answer a
fixed "not built" error. Reason: the guard exists to stop confident answers from an old world, and
a missing knowledge base gives no answers, so it cannot mislead. This follows the Port's ruling
that a failure stays inside the part it belongs to, and keeps the spec's rule that today's tests
stay free of PostgreSQL. Rejected: refusing to start, which would block every API test, the eval
runner and the dev server on a part the app does not read yet.

**Decision 2 (author, 28 October 2026): a build that cannot be checked stops the server.** When
the pointer file names a database but PostgreSQL is down, or that database or its fingerprint is
missing, the server does not start. The fixed text names the fix: the PostgreSQL start command
when the service is down, the build command otherwise. Reason: a guard that cannot check must not
let things through (fail closed). Unlike decision 1, a database may exist here and the app cannot
tell what is in it. Rejected: starting without the knowledge base, which would let a later
reconnect read a database that was never checked.

**Decision 3 (author, 28 October 2026, on review finding B1): the fingerprint skips hidden
entries.** A file or folder whose name starts with a dot, at any depth of the dataset folder, is
left out. Reason: hidden entries hold tooling state, such as the `.claude/.cc-writes` folder found
in `default/` during T18 or Finder's `.DS_Store`, never the world. Counting them would let any tool
mark the knowledge base stale. Rejected: counting every file.

**Decision 4 (author, 28 October 2026, on review finding B3): `LI_KNOWLEDGE_BASE_STATE` joins
the contract.** It names the build pointer file for the app and the build command alike, read from
the environment only, default `backend/.knowledge-base.json`. Reason: the test run and any eval
server a test starts point it at a file that does not exist, so they never check the real build.
Rejected: a fixed location only. *Superseded in part on 28 October 2026, after closure:* the
author's settings rule (spec, API contract change 5) reads every `LI_` setting from the
environment first, then `.env`. The pointer setting follows it when the phase 0 cleanup ticket
aligns the existing settings; until then it is read from the environment only, as built.

**Decision 5 (author, 28 October 2026, on review finding C2): the "cannot be checked" text names
both fixes.** It reads: "The knowledge base named by the last build cannot be checked. Check the
reader's login in .env, or rebuild it from backend/ with: uv run python -m
scripts.build_knowledge_base". Reason: PostgreSQL gives no error code at connection time that
separates a refused login from a missing database (checked during T18), so a rebuild-only text
would send a wrong password to the wrong fix. This refines decision 2's wording; its fail-closed
rule is unchanged. Rejected: the rebuild-only text.

## Comments

- 2026-10-28: Model check. The builder stated the `Model:` line (standard: Opus 5.5 or Sol 6.1)
  before any build work. The author confirmed with "go". Model used: Claude Opus 5.5.
- 2026-10-28: Built and closed. Evidence:
  - What shipped: `knowledge_base/staleness.py` (fingerprint and fixed texts), a one-row
    `build_record` table written last by every build, `check_knowledge_base` run as the read-only
    role at the start of the app's lifespan, `app.state.knowledge_base` as the marker (None when
    nothing is built), one `ChunkSettings` object read by the chunker and the fingerprint, the
    `LI_KNOWLEDGE_BASE_STATE` setting, and a run-wide test guard that hides the real build.
  - Door 2: 10 new tests (match, hidden entries ignored, edited/added/removed/renamed files,
    changed model, vector length and each chunking setting, nothing built, unreadable pointer,
    missing database, unrecorded database, PostgreSQL down, incomplete settings). Door 4: 4 new
    startup tests (stale refuses with no services started, uncheckable refuses, match starts,
    nothing built starts and logs). A deliberate break of the stale comparison failed both the
    door 2 and the door 4 stale tests.
  - Real server: on the pre-guard T17 build it refused with exit code 3 (B-090). After the
    author-approved rebuild (`li_kb_f9d6bcf6f8c5`; 40 documents, 320 chunks, 257 links, 18.362
    seconds, $0.00111362; `li_kb_0af9160cc4ed` retained; evidence `evidence/18-rebuild-2026-10-28.json`)
    it started and answered `/api/dataset` and `/api/overview` with 200. Pointed at a copy of the
    dataset with one changed file, it refused with the stale text and exit code 3; the copy's path
    never appeared in its output.
  - Safety net: 585 backend tests passed; pyright 0 errors; 149 frontend tests passed; frontend
    typecheck exit 0; lint exit 0 with the six existing warnings (AUD-009). Port API eval, approved
    by the author: 63/63 overall and 15/15 security, every question 3/3, prompt version unchanged
    (b70d0745), saved as `backend/evals/results/2026-10-27-224010-b70d0745.json`.
  - Review: two-axis `mp-code-review`, triaged in `reviews/18-code-review-2026-10-28.md`. Author
    rulings on findings became decisions 3 to 5. AUD-058 and AUD-059 registered. B-089 and B-090
    logged.
  - Left for the author: Python's traceback on a refusal shows source-file paths in the console;
    the fixed message has none.
