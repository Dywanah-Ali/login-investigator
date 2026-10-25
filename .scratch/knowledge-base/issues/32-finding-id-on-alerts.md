# 32: Finding ID on the Alerts screen

Type: build
Status: ready-for-agent
Blocked by: 13, 29
Phase: 1

## What to build

The analyst sees each alert's stable finding ID as the first column of the Alerts table, and the
Investigate button puts a question carrying that ID into the chat, so the agent investigates exactly
that alert.

## Decisions implemented

- T07 d7 (the finding ID as the first column; the details panel gains no context section), T05 d16
  (the Alerts reply gains the finding ID and nothing else), API contract change 1 (the field and the
  Investigate question's exact text).
- [review ruling 5] the Alerts field ships in phase 1.
- User stories 1, 3.

## Acceptance criteria

- [ ] The Alerts reply gains `finding_id` and nothing else; the API contract is updated first.
- [ ] Door 4 test: `finding_id` appears on every alert.
- [ ] The Alerts table shows the finding ID as its first column, as plain text.
- [ ] The Investigate button builds the question in the contract's exact form, in the frontend.
- [ ] Door 5 tests with the fake API cover the column and the question.
- [ ] The author looks at the screen in light and dark mode; a dated line records it.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
