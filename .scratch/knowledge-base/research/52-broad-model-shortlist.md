# T52: Broad model shortlist, including open-weight challengers

Checked: 2 November 2026. Status: six-model screening pool approved; execution and winner undecided.
Researcher: delegated Codex research agent. No inference, credential access or service changes.
Companion: `52-model-screening-evidence.md` for independent measurement and screening design.

## Selection principle

Missing published success in security investigation is not evidence of inability. Research
selects plausible candidates on general reasoning, instruction following, tool support,
structured outputs, price, hosting and lifecycle. Our cases then test investigation quality,
evidence discipline and security boundaries. A smaller, older or inexpensive model is not
excluded merely because it lacks a security paper or sits lower on a broad benchmark.

The former Sol/Sonnet-only recommendation is too narrow. Retain those as reference candidates,
not presumed winners. Open-weight and proprietary candidates face the same required outcomes.
We should deliberately try lower-cost challengers before deciding that this workload needs
a high-price model. This is consistent with P-03; it does not weaken any required outcome.

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

## Earlier research pool, retained as evidence

Earlier proposed screening pool: eight candidates, six open-weight and two inexpensive proprietary
models. The subsequent nine-model proposal added Sol as its reference. Both proposals are
superseded by the approved six above. This is a proposal to bound work, not authorisation to run eight/nine models.
The open-weight candidates span different architectures and vendors; no claim of equal quality
or speed is made. Prices are USD per million input/output tokens, as displayed by the named
provider on the check date. No cache, batch or free-route savings are assumed.

| Candidate | Weight availability/licence | Published hosted input/output price | Why it belongs in a screen; important limit |
|---|---|---|---|
| Qwen3.8-27B | Open weights; Apache 2.0 | OpenRouter headline $0.006 / $0.328 | A genuinely smaller dense candidate with configurable thinking. Headline router price is a discovery floor, not a pinned endpoint quote. [Model card](https://huggingface.co/Qwen/Qwen3.8-27B), [route listing](https://openrouter.ai/qwen/qwen3.8-27b). |
| gpt-oss-120b | Open weights; Apache 2.0 | OpenRouter headline $0.03 / $0.15 | Older inexpensive challenger with documented function calling, structured outputs and three reasoning levels. Age alone does not disqualify it. [OpenAI model page](https://developers.openai.com/api/docs/models/gpt-oss-120b), [route listing](https://openrouter.ai/openai/gpt-oss-120b). |
| GLM-5.3-Flash | Open weights; MIT | Z.ai $0.15 / $0.50 | Low-priced current agent/document-work candidate. Thinking is always enabled; provider recommends max effort, so low token price is not low total cost by itself. [Model card](https://huggingface.co/zai-org/GLM-5.3-Flash), [capabilities](https://docs.z.ai/guides/vlm/glm-5.3-flash), [pricing](https://docs.z.ai/guides/overview/pricing). |
| DeepSeek-V4.1-Flash-1017 hosted alias | V4.1-Flash family weights under MIT; exact 1017 checkpoint parity not established | DeepSeek $0.15 / $0.60 off-peak; $0.30 / $1.20 peak | Reasoning/non-reasoning, tools and JSON output documented. Test the actual served version, not the family name. [API table](https://api-docs.deepseek.com/quick_start/pricing/), [family weights](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash). |
| MiniMax-M3.1-Flash | Open weights; custom MiniMax Community licence | MiniMax $0.15 / $0.60 | Agentic-reasoning challenger with tunable effort. Default max effort makes an explicit setting essential. [Weights](https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash), [API capabilities](https://platform.minimax.io/docs/guides/text-generation), [pricing](https://platform.minimax.io/docs/pricing/overview). |
| Mistral Small 4, `mistral-small-2603` | Open weights; Apache 2.0 | Mistral $0.15 / $0.60 | Alternative vendor with documented function calling, structured outputs, reasoning and instruct capability. It has 256k context; sufficient context must be checked against actual evidence size. [Official model page](https://docs.mistral.ai/models/mistral-small-4-0-26-03). |
| GPT-6 Luna | Proprietary hosted | OpenAI $0.10 / $0.50 at standard short-context tier | Cheap proprietary control. Tools with reasoning require Responses; Chat Completions function calls require effort none. Parent verified the <=272k price tier and medium default. [Official model page](https://developers.openai.com/api/docs/models/gpt-6-luna). |
| Claude Haiku 5.5 | Proprietary hosted | Anthropic $0.10 / $0.50 for prompts <=100k; $0.50 / $2.50 above | Another cheap proprietary control. Parent verified adaptive thinking, medium default and 1M context. Long-context price makes evidence size consequential. [Official model page](https://platform.claude.com/docs/en/models/haiku-5-5/overview). |

“Six open-weight” describes the families, not proof that a hosted version exactly reproduces
released weights. DeepSeek's hosted 1017 variant is an explicit unresolved mapping. Router
headline prices may combine changing provider offerings; they must not be used as a budget
without selecting an endpoint and confirming its input/output pair, quantisation and features.

## Wider candidates retained

| Candidate | Evidence and disposition |
|---|---|
| Qwen3.5-9B | An even smaller Apache-2.0 challenger. [Official model card](https://huggingface.co/Qwen/Qwen3.5-9B) is available. The fetched [OpenRouter page](https://openrouter.ai/qwen/qwen3.5-9b) exposed no price or working-provider evidence; do not invent a rate or assume availability. Keep as a candidate for an explicitly verified hosted/local route. No cybersecurity publication is required. |
| Kimi K3 | Open weights under the custom Kimi K3 licence. Its API documents tools and strict schema output. OpenRouter displayed $0.1495 / $7.15, illustrating that open weights need not mean cheap output. Keep as a stronger open-weight reference if the inexpensive pool fails or benchmark diversity warrants it. [Weights](https://huggingface.co/moonshotai/Kimi-K3), [API guide](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart), [router listing](https://openrouter.ai/moonshotai/kimi-k3). |
| Kimi K3.1 Pro | Current [official API guide](https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart) exists. Exact weight release/licence and a readable direct rate were not established in this bounded check. Do not label it open-weight based on K3's licence. Keep in wider reference pool pending those details. |
| Gemini 3.8 Flash | Parent verified function calling and structured outputs. $0.75 / $3.75 introductory rate until 31 December 2026, then $1.50 / $7.50 from 1 January 2027. Retain as a mid-price proprietary alternative; use the future rate when discussing sustainable cost. [Pricing](https://ai.google.dev/gemini-api/docs/pricing), [model](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash). |
| Gemini 3.5 Flash-Lite | Parent verified stable availability, tools, structured outputs and thinking; $0.30 / $2.50 standard. Keep as a reserve low-cost proprietary alternative without enlarging the initial pool indefinitely. [Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite), [pricing](https://ai.google.dev/gemini-api/docs/pricing). |
| GPT-6.1 Sol and Claude Sonnet 5.5 | Retain the earlier candidates as higher-price references: $2 / $10 standard text rates. They are not automatically better for this app. The prior notes contain compatibility findings; Sol needs Responses for tools, Sonnet rejects temperature. [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [Sonnet](https://platform.claude.com/docs/en/models/sonnet-5-5/overview). |
| GLM-5.3 | Z.ai lists $1.40 / $4.40, versus $0.15 / $0.50 for Flash. Retain as an upgrade comparison if needed; a larger variant is not inherently the efficient starting point. [Pricing](https://docs.z.ai/guides/overview/pricing). |
| Kimi K2 family | Do not begin a new direct-provider baseline: official pricing documentation says new users lose access from 31 October and all K2 models are planned to retire by end December 2026. Third-party weights/hosting have separate lifecycles. [Kimi pricing/lifecycle notice](https://platform.kimi.ai/docs/pricing/chat). |

This is broad coverage, not an exhaustive market census. Families without a row have not been
proved inferior. Additional candidates can enter when they offer a meaningful price, deployment
or capability difference. Do not expand the first paid run without a bounded plan.

## What the capability evidence actually establishes

- Mistral's model page explicitly lists both function calling and structured outputs. Kimi's
  API guide demonstrates `json_schema` with strict mode and tool calls. These are documented
  interfaces, not proof of reliable selections or factually correct schema contents.
- DeepSeek's table lists tools, JSON output, Chat-compatible and Responses interfaces. A JSON
  checkbox does not establish strict schema adherence on our chosen route.
- GLM's guide documents tools in professional workflows and always-on thinking. Strict schema
  behaviour still needs route documentation and a small compatibility test.
- Qwen's card documents default thinking, optional non-thinking mode and sampling guidance.
  The exact hosted tool parser, structured-output support and thinking preservation policy
  must be checked. Do not carry the app's temperature zero blindly into every model.
- MiniMax offers OpenAI-compatible and Anthropic-compatible routes, recommends the latter,
  and supports low/medium/high/xhigh/max effort with max default. Compatibility at the HTTP
  format level does not prove our LangChain adapter preserves tool and thinking messages.
- gpt-oss has native tool/structured-output capabilities, but the hosting provider supplies
  the serving stack. Provider, quantisation, parser and limits are part of the tested system.

These are research entry reasons. The first three user criteria remain local acceptance
criteria: investigation quality, evidence discipline, and security/scope boundaries.

## Cost, speed and hosting interpretation

A token price is not an investigation price. Measure input, output/reasoning usage, retries,
number of calls and failures for each completed case. Then report cost per successful case,
with failed attempts included in total spend. Use each model's tokenizer and actual usage,
not one assumed token count for every candidate.

None of this child research establishes an end-to-end speed ranking. Vendor claims such as
“Flash” or “200 tokens/s” are not our investigation latency. The parent companion note covers
benchmark-owner measurements and their limitations. Record time to first useful response,
completion time and variation on the chosen endpoint. A short answer at modest token speed
may finish before a fast model that generates a long reasoning trace.

Open-weight means downloadable parameters under stated licence terms. It does not guarantee
all training data/code are open, unlimited commercial rights, free inference or easy local
hosting. MIT/Apache-labelled cards and custom community licences are distinct. Kimi and
MiniMax custom terms need deployment-specific review before adoption, not automatic exclusion
from read-only research. No legal conclusion is made here.

Hosted open-weight inference can be compared through an API without buying GPUs. Self-hosting
is a separate deployment decision: memory, context cache, quantisation, concurrency, idle
capacity and maintenance affect total cost. An “active parameters” figure does not tell you
the memory needed to store all weights. No local-hardware recommendation or estimate is made.

## Proposed screening before A/B/C

1. Agree the pool, provider endpoints and limits. Require supported tools/output format and
   sufficient context; inspect exact version and fallback settings. Failures here are route
   failures, not automatic proof of model incapability.
2. Use one simple common investigation configuration and reviewed diagnostic cases to screen
   quality, critical errors, cost and time. Include cheap candidates without a domain-paper gate.
   This is development evidence, not held-out reliability certification.
3. Keep a feasible cheaper challenger if results are close. Repeat consequential or unstable
   cases before eliminating a candidate. Do not select on one aggregate benchmark or one answer.
4. Freeze one model/endpoint/settings for the already agreed twelve-answer A/B/C calibration.
   Later mixed-model specialist work is a separate optimisation comparison.

Exact number of screening cases/repeats, assessor workload, maximum spend and latency targets
remain for the author. Screening adds work before the existing calibration and has not been
approved as an executable run. Langfuse can capture screening as well, subject to the same
local-first contract, but this note does not modify T54 or authorise additional implementation.

## Method and known gaps

The child used official model cards, provider documentation and provider pricing pages through
web search/open. Perplexity was absent from the child's available tools; the parent performed
Perplexity discovery and independent benchmark research separately. Secondary snippets were
used only to find primary pages, not as factual support. Parent-verified proprietary rows are
explicitly marked above; see the companion note for its independent source evidence.

A source conflict was resolved: DeepSeek's September launch page says V4-Pro would redirect
to Flash, but its [current changelog](https://api-docs.deepseek.com/updates/) says continued
V4-Pro service was retained after user demand, matching today's pricing table. Use current
API metadata at execution; a launch announcement is not a live routing guarantee.

No candidate has been tested on our data. Exact account access, endpoint privacy terms,
regional availability, provider quantisation, full licence terms, strict schema support where
not documented, hosted-to-weight parity and sustainable per-investigation cost remain unproved.
No model is selected, no full trial is authorised and no application behaviour changed.
