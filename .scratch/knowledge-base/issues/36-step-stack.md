# 36: The step stack

Type: research, then build
Status: ready-for-agent
Blocked by: 26, 29
Phase: 1
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

While the investigation tool runs, its five steps stack in the chat so the analyst sees how far the
playbook has got. Once the answer arrives, the stack folds into the Tools used drawer. The Port's
quick tools keep their single status line.

## Decisions implemented

- T07 d4 (the step stack, an exception to the Port's single status line, collapsing into Tools used),
  with its build condition: a short research step into how Anthropic and OpenAI document streaming
  progress for multi-step agents, recording the patterns borrowed.
- API contract change 4 (a `step` stream event emitted only by the investigation tool; the `tool`
  event's name list widens from three to seven tools).
- User stories 10 to 12.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Research first: Anthropic's and OpenAI's documentation on streaming progress for multi-step
      agents is read, and a short research note records the patterns borrowed and why. Nothing is
      built before it.
- [ ] The `step` event and the widened `tool` names are added to the API contract first.
- [ ] Door 4 test: `step` events come only from the investigation tool, in order, with start, end
      and error phases.
- [ ] The five steps stack while running, show an error state on a failed step, and fold into Tools
      used when the answer arrives.
- [ ] The Port's tools keep one status line.
- [ ] Door 5 tests with the fake API cover the stack, the error state and the fold.
- [ ] The author's screenshot review in light and dark mode is recorded as a dated line.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-29: author approved bringing `lookup_account` name support forward into T24 to keep
  its chat stream working. It uses the existing single status line. This ticket still owns
  the remaining new tool names and the investigation step stack.
