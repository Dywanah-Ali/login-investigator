# 05: How the knowledge base reaches the agent

Type: grilling
Status: open
Blocked by: 02, 04

## Question

Which new read-only tools does the investigator agent get, what does each return, and how do
they fit the Port's seams (tool list from one place, model and agent created in one function,
data access in the core)?

## Scope

- Candidate tools: look up an account's context (owner, privilege, groups, reachable assets with
  criticality and owners); find who shares a device or source network; search the corpus with
  citations; expand a spray alert into its targets. Decide how many tools, and whether graph
  traversal and text search are separate tools or one.
- Return shapes: what the agent sees, what it must cite, and the rule that an ATT&CK mapping is
  "consistent with" until evidence supports more.
- Whether the four detection rules change at all (expected: no), and whether the Alerts API
  gains a context field or the agent alone carries the explanation.
- Injection stance: graph and corpus content is untrusted data, like log fields. How the system
  prompt and the tool outputs say so.

## Acceptance

- [ ] Tool list, inputs and return shapes decided.
- [ ] Seam placement decided: where tools live, how they get the store.
- [ ] Untrusted-data rule written for graph and corpus content.
- [ ] Decision recorded here under `## Answer`.

## Comments
