# 35: The evidence download

Type: build
Status: ready-for-agent
Blocked by: 33
Phase: 1
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

The analyst downloads the investigation's evidence as a JSON file from a button in the Evidence tab,
to hand the case to a colleague. The file holds exactly what the panel shows and nothing internal.

## Decisions implemented

- T07 d5 (downloadable as JSON), API contract change 3
  (`GET /api/investigations/{id}/artifact.json`, served as an attachment, the same evidence and
  graph payload for the whole investigation, nothing from the prompt or the memory file).
- T05 d16 (only what the screen needs crosses the trust boundary).
- User stories 34, 35.

## Acceptance criteria

- [ ] The endpoint serves the file as an attachment; the API contract is updated first.
- [ ] Door 4 test: the file's keys are exactly the contract's, and nothing from the prompt or the
      memory file appears in it.
- [ ] The `graph` payload is included once ticket 37 adds it; until then the file carries
      `evidence` only, and the contract says so.
- [ ] A download button sits in the Evidence tab; a door 5 test covers it.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
