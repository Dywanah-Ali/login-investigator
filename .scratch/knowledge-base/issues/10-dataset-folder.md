# 10: The dataset folder

Type: build (prefactor)
Status: ready-for-agent
Blocked by: none
Phase: 0

## What to build

The app's setting names a dataset folder instead of a single log file. The regenerated world will
live in the folder called `default`; this ticket moves the Port's current log into it and makes
everything that reads the log read it from there. Nothing the analyst sees changes. This prepares
the ground so tickets 11 and 12 only add to the folder.

## Decisions implemented

- T04 d13 (one folder per dataset); [spec ruling] the regenerated world is the dataset folder
  `default`, the setting names a folder and replaces the log-path setting, the old log file is
  retired; API contract change 5 (the setting part).
- [spec ruling] the Port's ground-truth file stays, in its current shape, beside `truth.json`.
- User story 56.

## Acceptance criteria

- [ ] The dataset setting names a folder; the old log-path setting is removed; `env.example` and the
      API contract's configuration section are updated.
- [ ] The generator writes the log into `default`; the log file at its old place is removed.
- [ ] The folder has a README naming the seed. The ATT&CK version is added to it in ticket 14.
- [ ] The Port's ground-truth file is written beside the log in `default` and the Port's scorer reads
      it from there. If moving it would change the frozen Port exam, it stays where it is and the
      reason is recorded here.
- [ ] A missing or invalid dataset folder behaves as today's invalid log does; the startup tests
      prove it.
- [ ] The eval runner's isolation works the same way with a folder.
- [ ] The backend tests, the frontend tests and the Port's eval pass unchanged.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review has run with its findings triaged
      (`mp-code-review` in Claude Code, `code-review` in Codex).

## Comments
