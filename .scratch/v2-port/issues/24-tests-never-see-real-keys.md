# 24: Tests never see the real keys

**Status:** ready-for-human (build done 2026-10-17, waiting for the author's review)
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

One automatic guard for every test, in a new `backend/conftest.py` beside the copied v1
`tests/conftest.py`: `.env` loading is switched off and both key names are removed before each
test. A test that needs a key sets a fake one itself, as the existing tests already do.

## Acceptance

- [x] Reproduced before the fix: after one app start in a test, both key names were set
  - Evidence: `tests/test_no_real_keys.py` failed with `(True, True) == (False, False)`. Only
    whether each name is set was checked; no value was printed
- [x] After the fix, starting the app puts no key into the test environment. Test
  - Evidence: the same test passes
- [x] Every existing test passes unchanged; the copied v1 files are untouched
  - Evidence: full backend suite 352 passed (351 on `main` plus the new test); `tests/conftest.py`
    and `login_investigator/agent.py` unchanged in the diff
- [x] The new file is type-checked
  - Evidence: `conftest.py` added to Pyright's `include`; Pyright checks 47 files instead of 46,
    0 errors

Notes: the AbuseIPDB-key removals inside individual tests stay; they now repeat the guard, which
is harmless. Bug log B-036, prompt P-029.
