# T54 model screening: retained summary

Retention ruling: 4 November 2026, T56. This compact summary replaces the detailed local
experiment results. Counts were checked against saved assessments and the event log before
removal. Historical ticket/spec/audit decisions remain; hosted Langfuse records are untouched.

## Decision

The author shortlisted GPT-6 Luna and GPT-6.1 Sol as two different cost/capability tiers.
Sol alone met the original numeric screen rule under assistant scoring. Luna remains a
lower-cost candidate despite two zero-bearing answers; its shortlist inclusion is not a
passed-screen claim. No permanent model or A/B/C agent design was selected.

After tools exist, the possible final comparison will consider one direct Anthropic and
one direct open-source challenger per tier. Exact models, cases, scoring and model roles
remain undecided. A two-model design must be evaluated as a combined investigation system.

## Results

Six configurations, four fixed-evidence cases, three repetitions: 72 outcomes, 71 answers
and one no-answer from gpt-oss-120b. One assistant assessed all answers with identities
hidden until initial scoring was saved. No independent human validation was performed.

| Configuration | Answers | No zero scores | At least one zero | All six scores full credit |
| --- | ---: | ---: | ---: | ---: |
| Qwen3.8-27B | 12 | 6 | 6 | 2 |
| gpt-oss-120b | 11 | 3 | 8 | 1 |
| DeepSeek V4.1 Flash 1017 | 12 | 8 | 4 | 4 |
| GPT-6 Luna | 12 | 10 | 2 | 2 |
| Claude Haiku 5.5 | 12 | 8 | 4 | 4 |
| GPT-6.1 Sol | 12 | 12 | 0 | 6 |

426 criterion labels and 602 critical-error decisions were recorded. No designated critical
error was observed in the saved answer text. This does not establish production safety.

## Limits and costs

- Fixed evidence tests interpretation, not retrieval, tool execution or full-agent reliability.
- Nine injection-case answers lost usefulness credit for omitting an injection report;
  that reporting requirement was in the gold but not explicit in the runner prompt.
- Eight answers retained citation-syntax warnings. The original no-answer cause remains unknown.
- Known screening cost: US$0.278057; combined compatibility/screen cost: US$0.281197.
  Some charges were unknown. These are recorded totals, not a complete invoice.
- Mean recorded screening cost per answer: Sol US$0.012048825; Luna US$0.000769418333.
  The roughly 15.66x difference is specific to this exercise, not a production estimate.
- T54 Langfuse familiarisation was accepted by the author: 72 trial traces and 1,099 scores
  accepted in local POST receipts, followed by visual inspection. It was not operational
  integration acceptance. Combined experiment grouping and US$0.004366 of unmirrored later
  billing settlements were accepted limitations. No repair/re-upload is required.

## Retired evidence

T56 removes the five local run bundles (`compat-dry`, `compat-live`, `compat-readiness-1`,
`screen-dry`, `screen-live`) and temporary comparison fixtures/workflows. Individual answers,
labels and receipt files will no longer be available locally after cleanup. Existing audit
entries retain historical failures and their dispositions; their old artifact links are
historical provenance, not promises that those files remain available.
