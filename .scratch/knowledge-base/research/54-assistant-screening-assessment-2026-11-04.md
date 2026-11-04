# T54: assistant assessment of the completed screen

Date: 4 November 2026. Status: all 71 saved answers assessed; T54 remains claimed.

## Author ruling and scope

The author declined 70+ individual human assessments and explicitly instructed Codex to assess them. This supersedes initial human scoring for this screening run only. The frozen questions, evidence, expected findings, six criteria, critical-error rules, candidate prompts and original outcomes are unchanged. This report is a single assistant assessment, not independent human validation or application acceptance.

## Results

Scores were saved while candidate identities, configurations, costs, timing and revealing traces were hidden. Only after all 71 complete profiles and a hashed blind checkpoint were saved were identities joined for this table. No answer declared a candidate identity in the prepared batches. The assessor had historical experiment context; this is not a double-blind study.

| Configuration | Answers assessed | Answers with no zero | Answers with a zero | All six criteria scored 2 | No answer |
|---|---:|---:|---:|---:|---:|
| Qwen3.8-27B | 12 | 6 | 6 | 2 | 0 |
| gpt-oss-120b | 11 | 3 | 8 | 1 | 1 |
| DeepSeek V4.1 Flash 1017 | 12 | 8 | 4 | 4 | 0 |
| GPT-6 Luna | 12 | 10 | 2 | 2 | 0 |
| Claude Haiku 5.5 | 12 | 8 | 4 | 4 | 0 |
| GPT-6.1 Sol | 12 | 12 | 0 | 6 | 0 |

All 426 criterion scores and 602 designated critical-error decisions are saved. No designated critical error was found in these answer texts. 24 answers have at least one criterion scored 0; 47 have no zero. 19 answers received 2 on all six criteria. These counts describe answers, not a weighted quality score or independent case diversity.

Under these assistant scores, GPT-6.1 Sol alone meets the existing numerical screening rule: twelve completed answers, no applicable zero and no designated critical error. This is a provisional screening observation, not a model-adoption decision. Other configurations retain their complete profiles and failures. No model is automatically promoted or permanently eliminated.

## Findings and grading application

- Coverage reasoning: several answers confuse the 3 October event with the 4 October capture end, invent a gap before a burst despite preceding-day coverage, or mix a rule lookback with its observed alert span. These are incorrect claims, so the affected criteria receive 0 rather than 1.
- Clipped-history case: correct identification of missing later activity with omitted exact interval details receives 1 for facts, following the frozen allowance. No answer is labelled as claiming later inactivity solely because it omits interval dates.
- Matching travel: a single corrected password entry does not require an invented attack story. Broad collection or refusal to give a bounded travel explanation can lose usefulness/alternatives credit; optional proportionate assurance checks remain acceptable.
- Authentication: recorded MFA pass is not proof of actor, factor possession or a particular mechanism. Conditional hypotheses are distinguished from asserted facts. Borderline wording and the reasoning for its disposition are retained in the individual assessments.
- Injection: nine answers omit reporting D1’s malicious instruction. They receive partial usefulness under the frozen injection-reporting anchor, without being falsely classified as obeying the instruction. The runner prompt does not explicitly command reporting, although the frozen gold invokes the existing reporting policy. This limits attribution of the omission to model capability; no prompt or gold change was made.
- References: support is judged semantically, not by reference existence alone. Non-ASCII reference brackets and explanatory bracket text remain lexical-contract limitations. A readable citation is not automatically a fabricated reference, and zero unresolved references does not prove support.

## Saved evidence

- `backend/evals/comparison/runs/screen-live/artifacts/assistant-assessment/01-*.json` through `71-*.json`: per-answer profiles, complete answer excerpts, evidence references, reasons, critical flags, review IDs, source hashes and event sequences. Full-answer excerpts preserve the complete context rather than extracting an isolated phrase for full-credit labels.
- `artifacts/assistant-assessment/blind-checkpoint.json`: 71 file hashes and the event boundary before identity grouping.
- `artifacts/assistant-assessment/summary.json`: model/case profiles, explicit assistant provenance and numerical-rule observation.
- `artifacts/exports/labels-v1.json`: all 1,028 assistant scoring events. Original human label sheets remain blank and unchanged.
- `artifacts/assistant-assessment/verification.json`: preservation, provenance and completeness checks. Original run manifest and request/answer artifacts remain frozen.

## Limits and next step

This screen tests interpretation of supplied fixed evidence. It does not test retrieval, tool use, graph execution or production reliability. One assistant assessed all answers without independent human agreement or a calibrated second judge. Numeric labels retain judgment uncertainty and possible model/style bias; no confidence interval or statistically reliable superiority is claimed. The scorer model identity was not independently verified in this session.

The official selection profile and Langfuse score builder currently read human assessment events only. They will continue to show human scoring pending and will not upload these assistant criterion/critical scores. Do not relabel them as human to bypass this. B-156/AUD-082 records the integration gap. The explicit label export already includes assistant provenance correctly.

No new inference, replacement answer, paid judging, Langfuse upload, model-selection rationale, architecture calibration, application code or full application test run occurred. The original empty response and unresolved cost/cause remain under B-155/AUD-081.

Next: review this compact comparison, then scope assistant-score support in selection/mirroring before any separately authorised live upload.

## Subsequent author decision — 4 November 2026

The author shortlisted **GPT-6 Luna and GPT-6.1 Sol** after discussing quality and cost.
These define two comparison tiers. After tools are built, select and assess one direct
Anthropic challenger and one direct open-source challenger in each tier, four future
challengers total. Exact models are not chosen. The original assessment above is preserved:
Luna's two zero-bearing answers remain; shortlist inclusion does not certify a screen pass.
No single architecture baseline or permanent model selected. See the
[protocol ruling](52-objective1-comparison-protocol.md#author-shortlist-ruling--4-november-2026).

## Subsequent familiarisation scope correction — 4 November 2026

**Author scope correction, 4 November 2026:** pre-live model comparison is temporary,
ad hoc model-selection work, possibly repeated once after tools are built. It is not a
routine operational task. The current comparison upload is solely for the author to learn
Langfuse. Use the existing connector with only the minimum changes needed to display it
truthfully. Do not build automated remote read-back/reconciliation, a permanent comparison
operations workflow, or a staged pilot/control framework for this exercise. Simple author
inspection in Langfuse is sufficient for the learning objective. Formal comparison-upload
reconciliation requirements are superseded for this exercise. Real operational Langfuse
tracing/evaluations come later with the fully implemented running v2 app under T29/T30/T31;
their acceptance is neither designed nor satisfied by this familiarisation upload. Preserve
existing evidence, truthful assistant provenance and secret filtering. Luna/Sol shortlist
and deferred tier-matched challengers remain. Historical findings stay recorded without
becoming mandatory engineering work for this learning step.

## Familiarisation upload completed — 4 November 2026

Minimal connector changes now export the saved assistant scores explicitly. Local HTTP
receipts record one dataset, four cases, 72 trial records and 1,099 scores accepted in the
configured Japan-region Langfuse project, with zero failed/unresolved latest transfer
statuses. This includes 426 criterion scores, 602 critical decisions and 71 reference
checks. No new inference or automated remote read-back. Original human-only selection
report behaviour remains deliberately unchanged. Author screen inspection is pending;
this learning exercise is not operational integration acceptance. The local receipt is
`screen-live/artifacts/assistant-assessment/familiarisation-upload-receipt.json`.

## Familiarisation accepted — 4 November 2026

Author completed the visual walkthrough and accepted this upload subject as done. T54 is
resolved for that reduced purpose. Combined-experiment grouping does not provide distinct
per-model columns or mean all six models share each displayed score. Billing difference
B-158/AUD-084 remains recorded without repair. Historical evidence is preserved. Agreed
retirement/minimal foundation is a separate T56 follow-up; operational evaluations remain
later work. No automatic model adoption or full operational-integration acceptance.
