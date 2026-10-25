# 09: PostgreSQL with pgvector, and the loud test fixture

Type: build
Status: ready-for-agent
Blocked by: none
Phase: 0

## What to build

The author's installed PostgreSQL runs pgvector on the Intel Mac, and the backend test suite gains a
shared database fixture. A test that needs the database gets a fresh one for its test session,
built from pinned inputs and dropped afterwards. When the service is down, such a test fails at once
with the exact start command, never skips. Every test that does not need the database keeps running
without the service.

## Decisions implemented

- T02 d1 (one store: Homebrew PostgreSQL 18.6 with pgvector), T02 d4 (always-on service, tests only
  connect), T02 d5 (fresh database per test session, loud failures), T02 conditions (prove pgvector
  compiles on the Intel Mac and loads first).
- Spec: "The store and the build"; build order item 1. User stories 63, 64, 67.

## Acceptance criteria

- [ ] pgvector is installed for the Homebrew PostgreSQL 18.6 and `CREATE EXTENSION vector` succeeds;
      the install steps, versions and architecture are recorded under this ticket's Answer.
- [ ] The PostgreSQL driver is pinned, with its x86_64 build checked.
- [ ] Connection details live only in `.env`; their names are added to `env.example`; the no-real-keys
      test covers the new settings.
- [ ] The shared fixture creates a uniquely named fresh database per test session and drops it at the
      end, including after a failing test.
- [ ] With the service stopped, a test that needs the database fails (never skips) with a message
      carrying the exact start command. Proven by a recorded run.
- [ ] The existing tests still run with the service stopped.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
