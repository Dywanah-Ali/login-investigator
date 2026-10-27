# 26: The investigation tool and its package

Type: build
Status: ready-for-agent
Blocked by: 13, 25
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The analyst asks the agent to investigate a finding by its ID, and `investigate_alert` runs playbook
steps 2 to 6 in code and returns one package: account context, reachable assets, peers, clearing
documents and aggravating documents, each section with its own verdict and citations. It reports
progress per internal step, so the screen can later stack the steps while they run.

## Decisions implemented

- T05 d1 (`investigate_alert(finding_id)`), T05 d2 and d3 (one package with a named section per step,
  computed and ordered in code; spray and brute-force targets as a section, empty for other rules),
  T05 R5 (clearing and aggravating searches built in code from the finding's record, never from the
  chat; the radius from the one radius function of ticket 19), T05 d12 (package caps), T05 d13
  (parallel tool calls stay on).
- T05 d2 and T07 d4 (progress per internal step through the Port's custom stream).
- User stories 9, 15 to 19, 22, 23. Spec doors 2 and 3.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `investigate_alert` finds the finding by its ID; an unknown ID returns plain content saying so.
- [ ] The package has the five named sections, each with its own verdict and citations, computed and
      ordered in code. A targets section is filled for spray and brute force and empty otherwise.
- [ ] The clearing and aggravating searches are built from the finding's record; a test proves the
      chat text does not reach them.
- [ ] The radius comes from ticket 19's radius function; a door 2 test proves S6's package radius
      equals `truth.json`.
- [ ] Caps hold: five chunks per search, assets and peers paged with `truncated` flags, full lists in
      the artifact.
- [ ] Each internal step emits start, end or error through the Port's custom stream; a test proves
      the order. The API event itself ships in ticket 36.
- [ ] Parallel tool calls stay on.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
