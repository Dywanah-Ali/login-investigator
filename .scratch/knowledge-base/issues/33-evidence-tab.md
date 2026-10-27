# 33: The Evidence tab

Type: build
Status: ready-for-agent
Blocked by: 27, 29
Phase: 1
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

A third column beside the Investigator chat lists every cited record and passage for the
investigation, across turns. A click on a citation tag in the answer highlights its row. A citation
that could not be verified shows an amber warning. The column holds two tabs, Evidence and Graph;
the Graph tab shows its quiet empty-state line until ticket 37 draws in it. On a narrow screen the
column folds under the chat.

## Decisions implemented

- T07 d1 (the evidence panel as a third column, built from the saved artifact), T07 d5 (the panel's
  content), T07 d6 (citation letters L, G, D), T07 d9 point 2 (unverified citations amber, never
  hidden), T08 d2 (Evidence and Graph tabs in the third column), T08 d7 (the Graph tab always
  present, with an empty state).
- API contract change 2 (`evidence` and `unresolved` on reopen, projected from the saved artifacts
  through the one resolver, never from the model's text, never from a fresh walk).
- Project security rules: data fields render as plain text only.
- User stories 25, 27, 31 to 33, 36, 46.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Reopen turns gain `evidence` and `unresolved`, projected through ticket 27's resolver; the API
      contract is updated first.
- [ ] Door 4 test: the fields come from the saved artifact; a test proves they do not change when
      the model's text does.
- [ ] The third column sits right of the chat, with Evidence and Graph tabs, built from the Port's
      shell and shadcn/ui pieces.
- [ ] Evidence lists every cited record and passage for the investigation, across turns.
- [ ] A click on a citation tag highlights its row.
- [ ] An unresolved citation shows an amber warning, never hidden.
- [ ] Every data field renders as plain text; the repository-rules test covers the new components.
- [ ] The column folds under the chat on a narrow screen.
- [ ] Door 5 tests with the fake API cover the list, the highlight, the warning and the fold.
- [ ] The author's screenshot review in light and dark mode is recorded as a dated line.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
