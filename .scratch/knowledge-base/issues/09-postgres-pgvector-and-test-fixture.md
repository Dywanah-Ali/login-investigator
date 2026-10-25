# 09: PostgreSQL with pgvector, and the loud test fixture

Type: build
Status: claimed
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

- [x] pgvector is installed for the Homebrew PostgreSQL 18.6 and `CREATE EXTENSION vector` succeeds;
      the install steps, versions and architecture are recorded under this ticket's Answer.
- [x] The PostgreSQL driver is pinned, with its x86_64 build checked.
- [x] Connection details live only in `.env`; their names are added to `env.example`; the no-real-keys
      test covers the new settings.
- [x] The shared fixture creates a uniquely named fresh database per test session and drops it at the
      end, including after a failing test.
- [x] With the service stopped, a test that needs the database fails (never skips) with a message
      carrying the exact start command. Proven by a recorded run.
- [x] The existing tests still run with the service stopped.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged. *Type checker, code review, backend and frontend tests done; the Port's eval
      outstanding, see Answer. Codex's review was dropped by the author's ruling of 25 October 2026.*

## Answer

Built on 25 October 2026. Evidence for each criterion:

| Criterion | Evidence |
|---|---|
| pgvector installed, `CREATE EXTENSION vector` works | `brew install pgvector` (about 33 minutes; see Comments for what it compiled and rebuilt). pgvector **0.8.7**; `vector.dylib` is a Mach-O 64-bit bundle **x86_64**; macOS 15.7.8, Intel. The extension files link into `/usr/local/share/postgresql@18/extension/` and `/usr/local/lib/postgresql@18/`. The author ran `backend/setup/postgres-setup.sql` as superuser `postgres`: `CREATE EXTENSION` succeeded in `li_template`. Server `18.6 (Homebrew)`, rebuild `18.6_1`, now running that build. |
| Driver pinned, x86_64 build checked | `psycopg[binary]==3.3.6` in `pyproject.toml`, the driver `langchain-postgres` 0.0.19 requires (`psycopg[binary]<4,>=3`). `uv.lock` holds `psycopg_binary-3.3.6-cp312-cp312-macosx_10_13_x86_64.whl`; the installed `_psycopg` and `pq` modules are Mach-O 64-bit x86_64. |
| Connection details only in `.env`; names in `env.example`; no-real-keys covers them | Five names, `LI_PG_PASSWORD` required, the rest optional with defaults in the core. Read with `dotenv_values`, never `load_dotenv`. `test_no_real_keys.py` proves the password stays out of `os.environ` and out of the settings' `repr`; the test was seen to fail with `load_dotenv` put back on purpose. |
| Fresh, uniquely named database per session, dropped even after a failing test | `test_database_fixture.py`: a fresh empty `li_test_<12 hex>` database with pgvector working; an inner pytest session whose test fails, after which its database is absent from `pg_database` and differs from the outer session's. After the sessions, `pg_database` held only `fastapi`, `li_template`, `postgres`, `template0`, `template1`. |
| Service stopped: fails, never skips, with the start command; recorded run | Recorded run 16:41:46Z to 16:43:18Z, after `pg_ctl ... stop -m fast`, with no PostgreSQL process before or after: **418 passed, 2 errors, 0 skipped**, each error `PostgreSQL is not answering at localhost:5432. Start it with: brew services start postgresql@18`. That command then failed (B-072), so the fixture now prints `brew services restart postgresql@18`; the service-free test against port 1 checks that literal on every run. In pytest terms the test errors at setup rather than failing in its body: both are a non-pass with exit code 1, and nothing skips. |
| Existing tests run with the service stopped | The same run: every test except the two database ones passed. |
| Safety net, types | With the service up: backend 420 passed before the review fixes, 15 of the ticket's tests and the boundary test after them; frontend 149 passed; `pyright` 0 errors. Full suite rerun before commit: see the last Comment. |

Design, by the author's ruling (Comments): a limited role `li_admin` (login and `CREATEDB`, not a
superuser) and a template `li_template` with pgvector, marked `IS_TEMPLATE` and closed to
connections. The core module is `login_investigator/postgres.py` (settings, server check,
create and drop); the fixture is `tests/postgres_fixture.py`, imported by `tests/conftest.py`.
The template's pgvector version is pinned by a test at 0.8.7.

Outstanding before `resolved`:
- The Port's eval, if the author wants it run: the change touches no agent code, but the safety
  net names it.

Review findings not fixed, by choice: the ping treats every non-OK answer alike, so a server that is
shutting down or a mistyped host also gets the start command (the message names host and port);
`drop_database` raises a plain driver error if the server dies mid-session (loud, not silent);
leftover databases after a killed run are AUD-044.

## Comments

- 2026-10-25, author's ruling (pop-up): the tests log in as a **limited role** that can only create
  and drop its own databases, never as a superuser. pgvector is not a trusted extension (its
  `vector.control` has no `trusted = true`), so only a superuser can run `CREATE EXTENSION vector`.
  The author therefore runs a one-time setup once with their own superuser: it creates the limited
  role and a template database with pgvector already enabled, and every fresh test database is
  copied from that template. The author's superuser password never enters `.env`; the author sets
  the limited role's password themselves. Options B (the author's own superuser) and C (a new
  superuser for the app) were rejected on least privilege. Ticket 17's build role can reuse the
  template.
- 2026-10-25, Claude: `brew install pgvector` on this Intel Mac (macOS 15.7.8) found no ready-made
  builds, so Homebrew compiles its build dependencies from source, including `openssl@4` and
  `postgresql@17`. Flagged to the author; the install was left to finish.
- 2026-10-25, Claude: the install finished after about 33 minutes (pgvector 0.8.7, `vector.dylib`
  a Mach-O x86_64 bundle, Homebrew calling the setup "Tier 3"). It also **rebuilt `postgresql@18`
  as `18.6_1`** against `openssl@4` and `icu4c@79`, which Claude had told the author it would not
  do. Same PostgreSQL 18.6; the data folder untouched; the running server (old build, up since
  23 October) not restarted; `psql` and `pg_config` on the PATH link to 18.6_1; `postgresql@17`
  not linked and not running. The server moves to the new build at its next restart, planned to
  coincide with the service-stopped recorded run, with the author's approval.
- 2026-10-25, author (pop-up): approved one stop of the service of about 3 minutes for the
  service-stopped recorded run, with a start afterwards onto the rebuilt server.
- 2026-10-25, Claude: **the stop was not clean.** `brew services stop postgresql@18` sends a
  *smart* shutdown, which waits for every client to leave; pgAdmin held three connections (to
  `fastapi` and `postgres`), so the server sat in "shutting down" from 19:34:00, brew reported
  "Unable to stop", and at 19:36:00 the server process ended abruptly: the service file
  (`sh.brew.postgresql@18.plist`) gives the process `ExitTimeOut` 120 seconds before macOS kills
  it, which matches the two minutes in the log. Its `KeepAlive` restarts it only after a crash, so a
  clean fast stop stays stopped. The start at 19:36:29 ran
  PostgreSQL's automatic crash recovery from its write-ahead log ("redo done", ready at 19:36:30).
  Recovery replayed a test database's drop whose folder was already gone (two harmless warnings
  about `base/16890`). The recorded run (16:35:03Z) therefore met a server **rejecting
  connections while shutting down**, not one with no process; the fully stopped case is the
  automated test against port 1. Lesson: stop the service with a *fast* shutdown
  (`pg_ctl -D /usr/local/var/postgresql@18 stop -m fast`), which disconnects clients and shuts
  down cleanly, or close pgAdmin first.
- 2026-10-25, author: remove the build-only packages (`postgresql@17` and the rest) once pgvector
  works. Claude runs `brew autoremove --dry-run` first and shows the list before removing anything,
  because `autoremove` also removes leftovers from earlier, unrelated installs.
- 2026-10-25, Claude: two-axis review (standards and spec, parallel agents). Fixed: `env.example`
  held default values where the rule allows names only; the template's pgvector version is now
  pinned by a test; duplicated defaults and an unused `prefix` parameter removed; bug citations use
  B-072; README gained the PostgreSQL requirement, the one-time setup and the fixture's behaviour.
  Not fixed, recorded in the Answer, and AUD-044 added. Final run before commit, service up:
  backend **421 passed**, `pyright` 0 errors.
- 2026-10-25, Claude: `brew autoremove --dry-run` lists only `icu4c@78`; it does **not** list
  `postgresql@17`, which Homebrew keeps as a build dependency of the source-built pgvector. Removing
  it needs an explicit `brew uninstall postgresql@17`; the old `postgresql@18` 18.6 build (no longer
  running) needs `brew cleanup postgresql@18`. Awaiting the author's approval of that list.
- 2026-10-25, author's ruling (pop-up): from ticket 17, our table access uses SQLAlchemy Core on
  the psycopg driver, sharing one engine with LangChain's store. This ticket's server-level work
  (ping, create and drop a database) stays on psycopg directly. Spec decisions log has the row.
- 2026-10-25, author approved; Claude ran it. `brew uninstall postgresql@17` also autoremoved
  `icu4c@78` (86.7 MB); `brew cleanup postgresql@18` removed the old 18.6 build and its download
  (96.9 MB). Left: `postgresql@18` 18.6_1, `pgvector` 0.8.7, `icu4c@79`; `brew autoremove
  --dry-run` lists nothing. Server accepting connections; the four database fixture tests pass.
