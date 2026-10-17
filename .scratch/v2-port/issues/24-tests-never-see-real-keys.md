# 24: Tests never see the real keys

**Status:** resolved
**Blocked by:** none

## Scope

Noticed during ticket 22 and raised by the author the same day ("fix it pls"). Building the model
calls `load_dotenv(REPO_ROOT / ".env")` in `login_investigator/agent.py`, which copies the real
OpenRouter and AbuseIPDB keys into the process environment. Every API test starts the app, which
builds the model, so from the first such test onwards every later test in the run held both real
keys. A test without a network guard could then spend real quota, or send log IPs to AbuseIPDB.
The ticket-22 reputation test showed it: it removed the AbuseIPDB key, yet startup put it back and
only the test's guard stopped a live call.

The running app and the eval runner keep loading `.env`; only test runs change. The copied v1
core and `tests/conftest.py` stay unchanged.

## Approach

One guard for the whole test run, in a new `backend/conftest.py` beside the copied v1
`tests/conftest.py`. It starts when pytest starts, before any fixture of any scope and before any
test module is imported: `.env` loading is switched off and both key names are removed. It is
undone when pytest ends. A test that needs a key sets a fake one itself, as the existing tests
already do.

The first version guarded each test only. The spec review found that apps shared by a whole test
module start before such a guard, so they still built a model with the real OpenRouter key
(B-036). The guard moved to pytest's start.

## Acceptance

- [x] Reproduced before the fix: after one app start in a test, both key names were set
  - Evidence: `tests/test_no_real_keys.py` failed with `(True, True) == (False, False)`. Only
    whether each name is set was checked; no value was printed
- [x] After the fix, no app started by the tests gets a key, including apps shared by a module,
  and building the model finds no key. Test
  - Evidence: `test_an_app_shared_by_a_module_gets_no_model_key` failed against the per-test
    guard (the shared app had a model) and passes with the run-wide guard. The other two tests in
    the file pass. With fake keys set in the terminal before pytest starts, all three still pass
- [x] Every existing test passes unchanged; the copied v1 files are untouched
  - Evidence: full backend suite 354 passed (351 on `main` before ticket 22, plus three new
    tests); `tests/conftest.py` and `login_investigator/agent.py` unchanged in the diff
- [x] The new file is type-checked
  - Evidence: `conftest.py` added to Pyright's `include`; Pyright checks 47 files instead of 46,
    0 errors

Notes: the AbuseIPDB-key removals inside individual tests stay; they now repeat the guard, which
is harmless. On a machine without `.env`, as in a fresh clone, the tests pass either way: there is
no key there to leak. Bug log B-036, prompt P-029.

2026-10-17: two-axis review. Standards: no rule broken; it asked that the boolean-only assertions
be explained, now in the test file's docstring. Spec: the module-scope hole above, fixed and
re-tested. The author chose to review and merge the ticket ("1").

2026-10-17: status set to `resolved` on that choice. Replayed on top of ticket 22 and merged into
`main` locally. With both tickets together: 359 backend tests pass, Pyright 0 errors, eval prompt
fingerprint `35d4d98f`. Nothing pushed.
