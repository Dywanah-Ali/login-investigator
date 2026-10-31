# Tooling 01: Apply the reviewed Ruff policy

Type: task
Status: resolved
Rigour: Tier 1
Source: AUD-013; author's approval on 31 October 2026 after reviewing the remaining 115 warnings.

## Agreed scope

Relax the twelve reviewed style rules accounting for 46 diagnostics. Preserve correctness
checks and the previously approved BLE001 exceptions. Clarify imported pytest fixtures,
intentional joined strings and callback/validation patterns. Remove unused imports/binding,
make subprocess defaults explicit, and dispatch the native-inspection test's HTTP probe off
the event loop. No agent behaviour, API contract, application selection or T49 scope changes.

## Implementation and evidence

- Ruff 0.17.3 pinned in the backend development dependencies and lockfile; no existing package
  version changed. Configuration lives in `backend/pyproject.toml`, targets Python 3.12 and
  uses the pinned default checks plus import ordering, excluding the agreed twelve style rules.
- Fixture imports explicitly expose their names. Parenthesized joined strings have identical
  syntax trees. The hostile control character uses an escape with the same runtime value.
  Specific comments retain validation contracts and immediately awaited callbacks.
- Source comparison confirms that, after accounting for import organisation, redundant fixture
  aliases, two unused imports, one unused local name and explicit default `check=False`, the
  only executable change is the test-only HTTP worker dispatch. No application logic change.
- Full-policy lint passes. In-memory probes still detect F821, BLE001 and B023; UP017's approved
  style is allowed. Backend Pyright: zero errors/warnings. Frontend: 150 passed in 19.60 seconds.
- Admin manual section 7 added. Both commands tested exactly as written:
  `uv sync --locked --directory backend` and `uv run --locked --directory backend ruff check .`.
- Full backend suite passed: 701 tests in 993.52 seconds, no failures or teardown errors.
- B-125 records the suppression-cleanup mistake and restoration. The untracked VS Code settings
  created during interpreter selection were preserved. No push or paid evaluation.

## Documentation lookup

31 October 2026: Ruff 0.17.3; Context Hub `ruff/package` covers 0.15.15, so current official
[configuration](https://docs.astral.sh/ruff/configuration/),
[settings](https://docs.astral.sh/ruff/settings/) and
[suppression](https://docs.astral.sh/ruff/linter/#error-suppression) documentation checked for
version requirements, pinned defaults, ignores and line exceptions; confirmed with installed CLI.
Pytest 9.1.1: core fixture guidance was not returned by Context Hub search; official
[fixture documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html) checked for imported
fixture discovery. Python 3.12 official
[asyncio.to_thread](https://docs.python.org/3.12/library/asyncio-task.html#asyncio.to_thread)
and [subprocess.run](https://docs.python.org/3.12/library/subprocess.html#subprocess.run)
documentation checked for worker dispatch and the default false subprocess check policy.

## Answer

The author-approved policy is implemented and verified. Full backend 701 passed in 993.52 seconds;
frontend 150 passed; backend Pyright clean; full-policy Ruff clean; documented commands tested.
All existing dependency versions are retained; Ruff 0.17.3 is the sole addition. Syntax-tree
comparison and diagnostic probes confirm the intended scope and retained detection. Diff
whitespace check passes. AUD-013 closes on this evidence; AUD-072 remains a separate intermittent
service observation and did not recur. No agent behaviour changed, so no paid eval was run.
Final resource inspection found no active test processes and only the pre-existing retained
inspection graph container; disposable test graph resources were cleaned up.

The Python 3.12 target exposed one existing TypeVar-style warning, documented locally with
UP047. Explicit fixture aliases exposed PLC0414, likewise documented at the imports. These
specific exceptions preserve existing semantics and do not broaden the twelve ignored rules.
