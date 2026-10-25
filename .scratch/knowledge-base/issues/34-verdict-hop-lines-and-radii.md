# 34: The verdict, hop lines and radii tiles

Type: build
Status: ready-for-agent
Blocked by: 26, 33
Phase: 1

## What to build

The answer to a full investigation reads at a glance. The verdict sits on the one coloured surface,
with a "Cleared by" line when a document cleared it. The graph path is an indented list, one hop per
line with its tag. Three tiles show the radii as counts with the worst item named, and a "See list"
link opens the full list in the evidence panel.

## Decisions implemented

- T07 d2 (one hop per line), T07 d3 (radii as counts first, lists in the panel), T07 d9 (the
  five-level visual hierarchy: the verdict and "Cleared by" as the one coloured surface, red, green
  or amber; amber for "Not checked" and unverified; bordered boxes without colour for tiles and
  path; citation tags small, monospace, calm link blue; plain prose; no new colours).
- API contract change 2 (`radii` on reopen, present only where the investigation tool ran).
- User stories 18 to 22, 24, 26, 29.

## Acceptance criteria

- [ ] Reopen turns gain `radii` where the investigation tool ran, projected from the artifact; the
      API contract is updated first.
- [ ] Where the verdict shown comes from is fixed under this ticket's Answer, following ticket 27's
      answer-shape decision.
- [ ] The verdict and the "Cleared by" line sit on one coloured surface: red for threat, green for
      benign, amber for cannot tell.
- [ ] The path renders one hop per line, each with its tag.
- [ ] Three tiles show number and worst item; "See list" opens the list in the evidence panel.
- [ ] Tags are small, monospace, in the app's link blue; no new colours are added.
- [ ] The answer still renders with links and images switched off.
- [ ] Door 5 tests with the fake API cover each element.
- [ ] The author's screenshot review in light and dark mode settles the exact colours and is recorded
      as a dated line.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
