# 07: What the screen shows for an explained alert

Type: prototype
Status: open
Blocked by: 05

## Question

Where and how does the explanation appear: in the Alerts details panel, in the Investigator
answer, or both? What does the analyst see for blast radius, spread and shared ground, and how
are citations shown?

## Scope

- A rough prototype in the style of `.scratch/v2-port/research/07-screens-prototype.html`, using
  the Port's shell and shadcn/ui pieces.
- Candidates: a "Context" section in the Alerts details panel fed by a new API field; an
  "Investigate" handover that pre-asks the agent the blast-radius question; both.
- Citations: how a graph path and a document passage are shown as plain text, with the Port's
  rule that log, graph and corpus fields never pass through a markup renderer.
- The API contract change, if any, written before the build.

## Acceptance

- [ ] Prototype reviewed with the author and the placement chosen.
- [ ] API contract addition drafted, if the Alerts panel gains context.
- [ ] Decision recorded here under `## Answer`.

## Comments
