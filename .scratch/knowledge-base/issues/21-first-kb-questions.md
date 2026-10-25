# 21: The first knowledge-base questions

Type: build
Status: ready-for-agent
Blocked by: 16, 17, 19
Phase: 0

## What to build

The knowledge base's own question file, beside the frozen Port file, starts with a first handful of
questions, each carrying its gold IDs or its expected verdict. They are written and committed before
any search runs, so the exam cannot be fitted to the results.

## Decisions implemented

- Map, evaluation stance (the eval set exists before the first retrieval runs); spec build order
  item 8 (review finding R5).
- T06 d3 (question fields: `type`, `gold`, `split`, a provenance line), T06 d8 (two files, kept
  separate).
- [review ruling 2] the gold items choose the checks; a say-no question may carry no gold IDs but
  states its expected verdict.
- User story 71.

## Acceptance criteria

- [ ] The question file sits beside the Port's file, which stays unchanged.
- [ ] Six to ten questions, covering at least one document lookup, one graph lookup, one mixed
      question on S6, one absent topic (verdict `none`, no gold IDs) and one twin.
- [ ] Every question carries `type`, `split`, a provenance line, and gold IDs or an expected verdict.
- [ ] A test proves every gold chunk ID exists in a fresh build, every gold record ID exists in the
      world's files, and every question has gold IDs or a verdict.
- [ ] The file is committed before ticket 22's first search run; the commit order is the evidence.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
