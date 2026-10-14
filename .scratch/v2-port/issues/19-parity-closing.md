# 19: Parity closing

**What to build:** the proof that the Port is done. Every row of the acceptance gate in the spec is
ticked with named evidence, the cross-screen checks pass through the API, a fresh clone starts from
the README, and the author closes the manual checklist and the eight-step scenario with a dated ruling.

**Blocked by:** 14 (Alerts), 15 (Log explorer), 17 (Investigator screen), 18 (Eval set in API mode).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "Testing Decisions" (the gate table and the eight-step scenario).
Decisions: ticket 08.

- [ ] API replay tests that need every screen: a filter change updates every screen consistently; an empty filter gives a clear message on all three; reset restores the whole log
- [ ] Full automated set green: pytest (copied, adapted, boundary, API), Vitest, the eval API mode run from ticket 18
- [ ] Fresh clone: both servers start from the README's two commands in a clean folder
- [ ] A scan of every git object finds no key value and no key pattern; no personal name or email in any file
- [ ] The manual presence checklist ticked by the author with a dated ruling: synthetic label, metric labels, empty-state messages, scope note, AI note, progress words per tool, locked input, severity labels and colours, charts per theme, error messages hide exception text
  - Reference for the Overview (author's ruling 2026-10-14, ticket 13, point 4; spec decisions log): its metric labels, chart titles and empty-state text are checked against the agreed screens prototype (`research/07-screens-prototype.html`), not v1's code. A wording that differs from v1 but matches the prototype passes. The failed share rounds a half up, and the sidebar links keep the filters, both as decided. Every other item is checked against v1, as the gate says
- [ ] The eight-step scenario run end to end in the live app by the author, closed with a dated ruling
- [ ] The gate table in the spec rewritten as a ticked list with the evidence named beside each box, in v1's style
- [ ] Bug log and prompt log complete for the whole Port
- [ ] The author's review before anything is pushed
