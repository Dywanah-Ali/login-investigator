# T52: Broad model research and proposed local screening

Date: 2 November 2026. Status: research method and six-model pool agreed; execution details proposed only.
Companion: [broad shortlist](52-broad-model-shortlist.md).

## Author's correction and the decision it changes

The author rejected narrowing candidates to models with published security-investigation
results. Lack of task-specific published evidence is not evidence of inability. Research
must admit credible cheaper/faster candidates, including open-weight models. General
reasoning, instruction following, tools, structured outputs and practical deployment
facts justify entry. Investigation quality, evidence discipline and security boundaries
remain local acceptance requirements, not prerequisites for appearing in a paper.

The earlier Sol-only recommendation is superseded pending this broader comparison.
No model or provider is selected. No inference calls, paid runs, self-hosting, fixture
implementation or permanent architecture adoption are approved by this research.

## Approved screening pool, 2 November 2026

The author approved six candidates: Qwen3.8-27B, gpt-oss-120b, DeepSeek V4.1 Flash,
GPT-6 Luna, Claude Haiku 5.5 and GPT-6.1 Sol. Sol is a higher-capability reference,
not the selected winner. The exact DeepSeek served version and all provider routes
must be verified before execution.

GLM-5.3-Flash, MiniMax-M3.1-Flash and Mistral Small 4 move to reserve to limit review
workload while retaining smaller open weights, inexpensive hosted options, proprietary
challengers and a higher-capability reference. This is not evidence of inferior performance.

Screen models using the same single-investigator setup before freezing a baseline for
A/B/C. Four cases per model would produce 24 final answers, and this four-case set plus three attempts are now approved. Settings, budget and
execution remain to be agreed. Approval of this pool does
not authorise inference calls or select a permanent production model.

## Four-case screening set approved, 2 November 2026

The author clarified that all four cases are approved: O1-02 matching travel, O1-06 partial
explanation, O1-09 missing later history and O1-12-D document injection, including their
plain-language expected assessments. The O1-09 discussion resolved a concern; it was not
approval of only that case. No further case-set approval is needed.

Use these four cases across the six approved model candidates. One pass produces
24 final answers; three passes are now approved. Exact fixtures, detailed scoring readiness,
provider routes, settings, limits and execution authorisation still need settlement.
The already agreed 12-answer A/B/C architecture calibration remains a separate stage.

## Case review checkpoint, 2 November 2026

The author accepted the missing-later-history case O1-09 after comparing it with O1-06:
identical suspicious sequence and travel approval, but capture stops immediately after
success. Explicit coverage metadata must distinguish an unobserved later interval from
no later login events in a fully covered interval. Neither permits an account-safety claim.
O1-06 was already accepted. The subsequent clarification above confirms approval of all
four cases. Repetition policy and execution remain open.

## Screening repetitions approved, 2 November 2026

Author approved three attempts per model per case: six models × four cases × three
attempts = 72 final answers. Run a first pass of 24 answers, then inspect the setup for
fixture, prompt, scoring, adapter or recording problems before completing the other two
passes. This checkpoint is for setup diagnosis, not early winner selection or eliminating
candidates on one answer. Each attempt uses fresh memory and frozen evidence/instructions/
settings; preserve every result, failure and retry.

If the checkpoint exposes a problem requiring a change, preserve the original records and
version the correction. Do not pool changed-condition answers with the original comparison;
rerun affected comparisons fairly, with any extra calls covered by the eventual execution
limits. Additional reruns are not silently included in the approved 72-answer plan.

Provider routes, settings, detailed fixture/scoring readiness, spending/call limits and
execution authorisation remain open. The separate 12-answer A/B/C architecture calibration
is unchanged. These repeats measure variability on four development cases, not broad
production reliability.

## Configuration approved, 2 November 2026

The author confirmed OpenRouter as the gateway, fixed providers and these starting settings:

| Model | Serving provider through OpenRouter | Reasoning |
|---|---|---|
| Qwen3.8-27B | DeepInfra | Medium |
| gpt-oss-120b | DeepInfra | Medium |
| DeepSeek V4.1 Flash 1017 | DeepInfra | High |
| GPT-6 Luna | OpenAI | Medium |
| Claude Haiku 5.5 | Anthropic | Adaptive, medium |
| GPT-6.1 Sol | OpenAI | Medium |

Use standard service, disable automatic provider/model fallback and require support for
requested settings. This approves the starting configuration subject to compatibility checks;
it does not establish runtime support. DeepSeek's exact provider variant remains to be verified.
Record effective mappings, sampling and model revisions before execution; changes to approved
providers or reasoning levels need an explicit disposition, not silent substitution.

Time, output, retry/call and spending limits remain open. No paid inference or application
migration is authorised by this configuration confirmation. The six-model/four-case/three-pass
plan remains 72 answers with a setup checkpoint after the first 24.

## Evidence hierarchy and practical limits

| Evidence | Appropriate use | Limit |
|---|---|---|
| Provider documentation and model-owner cards | IDs, interfaces, published rates, released weights and licence text | Capability and speed descriptions remain provider claims |
| Independent benchmark-owner results | General capabilities, settings tradeoffs and measured service performance | Different tasks, evaluation harnesses and dates; not our acceptance evidence |
| Source-available evaluations and independent audits | Inspect grading and reproducibility | Tests and scorers may contain errors |
| Our future saved runs | Compare observed quality, total cost and time on representative inputs | Development examples do not establish held-out reliability |

Artificial Analysis distinguishes models from hosting endpoints. Its methodology explains
that tokenizers differ, cost per task includes consumed tokens, and its estimated time per
Intelligence Index task is derived from token counts and measured output speed rather than
timed during those evaluations. Treat those metrics as screening evidence, not a forecast
of our investigation duration. Measure our complete workflow separately, including time to
first useful answer, tool waits, retries and specialist calls.
Source: [Artificial Analysis methodology](https://artificialanalysis.ai/methodology).

Its Endpoint Accuracy Index reruns tools, reasoning and long-context tests by provider,
using a reference deployment and reporting uncertainty. Quantization, parsing and settings
can affect results even when the model name matches. Therefore the local experimental unit
should be model plus exact route plus settings; a changed route requires a compatibility
check and may require rescoring. Published endpoint snapshots are not availability promises.
Source: [endpoint methodology](https://artificialanalysis.ai/methodology/endpoint-accuracy-index).

Berkeley's BFCL distinguishes native function calls from prompt-based workarounds and links
responses/code for reproduction. The inspected leaderboard says it was updated 12 April 2026,
so absence of a newer candidate cannot justify exclusion. It cannot prove our tool-loop
behaviour or injection resistance.
Source: [BFCL owner](https://gorilla.cs.berkeley.edu/leaderboard.html).

Epoch's September 2026 audit found potentially accuracy-affecting defects in 24 of 50 sampled
BFCL v4 tasks. This is evidence to qualify that benchmark, not a new defect found in our
project. It supports inspecting graders instead of treating a leaderboard score as a gate.
Source: [Epoch's own audit](https://epoch.ai/benchmarks/berkeley-function-calling-leaderboard/review).

## Independent general-capability observations

Snapshot from the [Artificial Analysis leaderboard](https://artificialanalysis.ai/leaderboards/models),
2 November 2026. Index v5 values are general benchmark observations, not pass percentages.
Speed is the displayed median output tokens/second, not completed investigations/second.
These model-table observations are not measurements of the endpoints we will select.

| Displayed model/setting | Intelligence Index | Output tokens/second |
|---|---|---|
| DeepSeek V4.1 Flash 1017, max | 32 | 170 |
| MiniMax-M3.1-Flash | 29 | 136 |
| GLM-5.3-Flash | 28 | 76 |
| Claude Haiku 5.5, medium | 25 | 172 |
| Qwen3.8 27B, xhigh | 20 | 41 |
| GPT-6 Luna, medium | 18 | Not shown |
| Mistral Small 4 | 4 | 158 |
| gpt-oss-120b, high | Not shown | 217 |
| GPT-6.1 Sol, medium | 46 | 63 |

Inference: these observations justify a varied screen, not ranking our app's suitability.
Keep Mistral and gpt-oss eligible despite low/missing index results. Settings differ; no
identical-compute comparison is implied. Model-page defaults and benchmark effort are separate.

## Proposed screening before the architecture comparison

This is an engineering proposal, not an authorised additional run schedule.

1. Select a small, diverse set from the broad shortlist: compact open weights, efficient
   larger open weights, cheap proprietary models and a more capable reference. Do not
   remove a model solely because its general benchmark score is below the reference.
2. Freeze evidence, instructions, review anchors and output contract. Keep answer keys out
   of model input. Use the same single-investigator workflow for the first model screen.
   The four existing calibration cases could be reused as development diagnostics, subject
   to completing their review. They cannot become unseen confirmation evidence afterwards.
3. Check each route's actual tool calls, structured outputs, supported reasoning controls
   and failure handling separately. Fixed evidence alone does not demonstrate live retrieval
   or tool integration. Separate unsupported transport from weak model judgments.
4. Preserve every attempt. Apply the existing semantic rubric and critical-error flags.
   Record total billable usage, cost, elapsed time, no-answers and retries. Compare the same
   input text, not assumed identical token counts. Do not equate vendor effort labels.
5. A first pass identifies promising candidates and failures; repeat close or inconsistent
   results before choosing a provisional baseline. Do not use a single failure to declare a
   model generally incapable. Any tuning must be versioned and the comparison rerun fairly.
6. Freeze one model/route/settings combination for the agreed 12-answer A/B/C architecture
   calibration. Record the limitation: architecture findings are conditional on that model.
   A specialist may interact differently with a different model; later model-role allocation
   or model-by-architecture checks need a separately bounded proposal.

T52 must settle candidate count, repetition policy, review workload, latency/cost targets,
spending and call limits, runner owner and execution authorisation. No universal winning
model follows from this research. A full grid of every model across all architectures is
not proposed as the first step.

## Delivery and preservation

The approved order remains T52, then T54's Langfuse foundation, then instrumented calibration.
If the proposed model screen is adopted, plan its recording through that same foundation
before A/B/C. Its additional outputs and costs are separate from the agreed twelve answers.
T31 retains full application/exam integration. Local evidence stays authoritative; hosted
records mirror it. There is no approval here to change the phase gate or weaken the rubric.

## Method

Parent used Perplexity discovery for benchmark sources and verified primary pages with web
browsing. The research-skill background agent independently investigates model families and
writes the companion shortlist. No paid model inference or account inspection occurred.
Prices and benchmark observations are dated; provider/account compatibility is untested.
