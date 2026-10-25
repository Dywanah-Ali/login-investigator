# 18: The staleness guard

Type: build
Status: ready-for-agent
Blocked by: 17
Phase: 0

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

- [ ] Each build records a fingerprint of the dataset folder's files with the embedding model, the
      vector length and the chunking settings.
- [ ] At startup the app recomputes the fingerprint from the folder.
- [ ] On a mismatch the server does not start; the failure carries fixed text naming the build
      command and no path. No endpoint answers.
- [ ] On a match the server starts as before.
- [ ] What happens when no database has been built yet is decided, consistent with the guard, and
      recorded under this ticket's Answer.
- [ ] Door 2 test: the guard refuses a database built from a changed file. Door 4 test: the startup
      test proves the server refuses to start.
- [ ] The API contract records the startup failure.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review has run with its findings triaged
      (`mp-code-review` in Claude Code, `code-review` in Codex).

## Comments
