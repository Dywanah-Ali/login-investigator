# 31: Langfuse behind its switch

Type: build
Status: ready-for-agent
Blocked by: 29
Phase: 0

## What to build

Langfuse mirrors dev investigations and eval runs behind one switch that is off by default. The repo
stays the source of truth: the JSON result file is written first, an upload failure is shown loudly,
and the author's labels come back only through an export script into a repo file.

## Decisions implemented

- T06 d10 (Langfuse adopted to the full as a mirror), AUD-036.
- [review ruling 4] proven with the switch on against a fake destination, plus one real eval run
  seen in Langfuse.
- API contract change 5 (the Langfuse switch setting).
- User stories 83 to 85. Spec doors 3 and 6.

## Acceptance criteria

- [ ] One callback handler is added in the agent-building function.
- [ ] Off by default; one environment variable turns it on; the key is loaded only when on and never
      written to a result.
- [ ] The two question files are uploaded as datasets; each eval run is an experiment run stamped with
      the same fingerprint and commit as the JSON file; every check verdict is a boolean score; the
      judge's verdict and reason are a score with a comment.
- [ ] A masking hook is applied to everything sent.
- [ ] Tests with the switch off, and with it on against a fake destination: the JSON is written
      before any upload; an upload failure is reported loudly in the summary and the JSON survives;
      the masking hook is applied; labels return only through the export script.
- [ ] Nothing at runtime reads from Langfuse.
- [ ] One real eval run is visible in Langfuse; a dated line records the author's look, and AUD-036 is
      closed with that evidence.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review has run with its findings triaged
      (`mp-code-review` in Claude Code, `code-review` in Codex).

## Comments
