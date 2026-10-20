# 06: The eval set for a graph-plus-text system

Type: grilling
Status: open
Blocked by: 04, 05

## Question

What does the eval set look like, so that retrieval and answer quality are measured separately,
every question has a gold answer in the ground truth, and the whole set re-runs on every change
without Claude?

## Scope

- Two layers: retrieval (did the gold node or chunk appear in the top results, at what rank) and
  answer (is every claim backed by the retrieved context; faithfulness).
- Question types: graph lookups, multi-hop traversals, text lookups, mixed, and "not in the
  knowledge base" questions that must be refused.
- How it fits the existing eval runner and its API mode; whether it is a new set or an extension;
  thresholds (the existing 90% overall and 100% security stay as the floor; what the retrieval
  floor is).
- Grader: deterministic where possible (retrieval), model-graded where needed (faithfulness),
  with the grader's prompt versioned.
- Size for phase 1 and how it grows per later phase.

## Acceptance

- [ ] Layers, question types, thresholds and grader decided.
- [ ] Runner integration decided.
- [ ] Decision recorded here under `## Answer`.

## Comments
