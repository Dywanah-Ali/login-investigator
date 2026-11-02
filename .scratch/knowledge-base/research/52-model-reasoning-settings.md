# T52: Proposed reasoning settings for the six-model screen

Checked: 2 November 2026. Status: provider/reasoning configuration approved subject to compatibility; execution pending.
Scope: the six approved candidates, four cases and three passes. No inference, keys, account
inspection, dependency changes or application code. The author confirmed OpenRouter access;
use it as the preferred gateway, with provider pinning settled separately.

## Configuration approved, 2 November 2026

Later public-metadata check on the same date identifies DeepSeek's standard route as
`deepinfra/fp8`, with reasoning/tools/structured-output parameters advertised. This resolves
the catalogue lookup marked pending below, not runtime compatibility. All six selected
standard-route prices and native limits are saved in the
[price report](52-screening-price-and-reservation-check.md). Explicit standard service
remains necessary; do not select its flex/priority siblings. Earlier pending statements
are retained as research history.

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

## Principle

Compare usable model configurations under a balanced quality/time/cost objective. A shared
label such as medium does not allocate equal computation across vendors. Set each model's
native controls explicitly and preserve that configuration for all twelve answers from it.
The result compares those configurations; it does not establish each model's best possible
performance. Do not silently tune a failing model between passes.

## Detailed settings and remaining compatibility checks

| Candidate and intended OpenRouter identifier | Requested reasoning | Sampling proposal | Reason and qualification |
|---|---|---|---|
| Qwen3.8-27B: `qwen/qwen3.8-27b` | Enabled, medium | Temperature 1.0, top_p 0.95, top_k 20; remaining documented neutral defaults where supported | Owner describes medium as accuracy/speed balance. This deliberately differs from its xhigh default. Verify the selected provider forwards native effort rather than only imposing a token budget. |
| gpt-oss-120b: `openai/gpt-oss-120b` | Medium | Keep selected endpoint's documented default sampling; record it | Native low/medium/high support makes medium a defensible middle starting point. The provider's serving template/parser must actually apply it. |
| DeepSeek V4.1 Flash 1017: `deepseek/deepseek-v4.1-flash-1017` | Enabled, high | Omit temperature and penalties; leave top_p at documented default | High is its native default and middle of low/high/max. Native medium maps to high; use high explicitly rather than imply an independent medium setting. |
| GPT-6 Luna: `openai/gpt-6-luna` | Medium, standard mode | Omit sampling overrides pending endpoint validation | Medium is the documented default. Reasoning with tool calls needs Responses; native Chat Completions permits function calls only at effort none. Do not turn reasoning off just to fit the old adapter. |
| Claude Haiku 5.5: `anthropic/claude-haiku-5.5` | Adaptive enabled, medium | Omit temperature, top_p and top_k | Medium is the documented default. Ensure the gateway selects native adaptive thinking, not a legacy fixed-budget emulation. |
| GPT-6.1 Sol: `openai/gpt-6.1-sol` | Medium, standard mode | Omit sampling overrides pending endpoint validation | Medium is the documented default. Tool calling requires Responses. Standard mode avoids silently introducing pro execution into this balanced baseline. |

These model identifiers are gateway targets, not provider endpoint pins. DeepSeek's generic
`deepseek/deepseek-v4.1-flash` listing represents a separately listed September release;
use the explicit 1017 target for the October snapshot already researched. No immutable
version guarantee is inferred for identifiers without a date.

## Primary evidence

Qwen's owner card lists low, medium and xhigh, with xhigh default; it describes medium as the
balance setting. Thinking and preserved historical thinking default on. Its thinking sampling
recipe is temperature 1, top_p .95, top_k 20, min_p 0, presence penalty 0 and repetition penalty
1. Sampling support depends on the server. Its examples use `reasoning_effort` and, depending
on framework, `chat_template_kwargs`. This is native behaviour, not proof of the gateway's
selected endpoint mapping. Lower per-turn effort can also increase retries and total cost.
Sources: [owner card](https://huggingface.co/Qwen/Qwen3.8-27B),
[OpenRouter listing](https://openrouter.ai/qwen/qwen3.8-27b).

DeepSeek's thinking guide supports low/high/max, default high. Medium and xhigh map to high;
minimal maps to low. Temperature and presence/frequency penalties are ignored in thinking
mode rather than rejected. Flash top_p is effective only in thinking mode, clamped to
.95–1.0. Tool-bearing conversations require preserving returned reasoning content across
turns according to the documented protocol. A gateway/adapter that discards it can change
behaviour. These mappings must be checked on the actual pinned endpoint.
Sources: [thinking guide](https://api-docs.deepseek.com/guides/thinking_mode/),
[exact OpenRouter snapshot](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017).

OpenAI documents gpt-oss low/medium/high effort and native tool/structured-output capability.
Its listed context is 131,072 tokens. This does not establish a direct OpenAI inference route;
gpt-oss will use a third-party hosting endpoint through OpenRouter.
Source: [gpt-oss model page](https://developers.openai.com/api/docs/models/gpt-oss-120b).

Sol's native effort choices are low/medium/high/xhigh/max, default medium, with Responses
required for tools. Luna adds none and permits Chat Completions tool calls only with none.
Standard/pro execution is a separate control; explicitly retain standard for the proposal.
Sources: [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
[reasoning guide](https://developers.openai.com/api/docs/guides/reasoning).

Haiku 5.5 uses adaptive thinking, medium by default. Its model page instructs callers to omit
temperature, top_p and top_k. The effort guide supports low, medium, high, xhigh and max for
this model. The provider's native fields are `thinking` and `output_config.effort`.
Sources: [Haiku model page](https://platform.claude.com/docs/en/models/haiku-5-5/overview),
[effort guide](https://platform.claude.com/docs/en/build-with-claude/effort).

## OpenRouter contract and unresolved mappings

OpenRouter documents unified `reasoning.effort`, `enabled` and token-budget controls. Its
model catalogue can report `supported_efforts`, `default_effort`, `default_enabled` and
`mandatory`. The selected endpoint's supported parameters still need inspection. Do not
assume every accepted gateway string reaches the native model unchanged. Native Anthropic
Messages requests can preserve adaptive thinking plus explicit effort; the gateway docs
explain this mapping. The selected request protocol/adapter needs verification before calls.
Most providers count reasoning and visible answer against the same output cap; exhausting
it can produce no visible answer while still incurring charges. This is a truncation outcome,
not permission to discard the attempt. Source:
[OpenRouter reasoning documentation](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens).

## Setup checks before the first scored pass

- Record requested settings, supported endpoint settings and any documented mapping separately.
  Do not claim accepted/effective settings were runtime-verified before a compatibility probe.
- Confirm native tool arguments/results, structured output and returned reasoning-block
  continuity where the model protocol requires it. Fixed-evidence outputs alone prove none
  of these tool-loop behaviours.
- Freeze provider endpoint, model ID, revision metadata where exposed, quantisation, context
  limits, sampling and reasoning modes before scored calls. Record missing disclosures.
- Choose total output caps, timeouts and retry limits with explicit budgets. Do not claim equal
  token caps imply equal reasoning work or equal time. Surface incomplete/no-answer outcomes.
- Retain provider-emitted protocol artifacts where required, without assuming every model
  exposes internal reasoning. Review final answers using the same evidence rubric.
- No automatic effort escalation, downgrade, model substitution or provider fallback within
  the scored comparison. Changes create a separately versioned condition and fair reruns.

## Method and limits

Official owner/model documentation and OpenRouter pages were opened through web browsing.
No SDK integration is implemented here; installed-adapter behaviour and public catalogue
pinning are parent work. Recommendations are engineering starting points, not measured
optimal settings or equal-compute controls. Exact pins and provider mapping remain unresolved.

## Routing evidence and local inspection

Author confirmed existing OpenRouter access during this discussion. Prefer that gateway for
all six; no new direct-provider account is required by this proposal. Pin one serving endpoint
per model, disable provider/model fallbacks and require support for requested parameters.
Use standard service rather than dynamically changing price/latency tiers. Base provider
slugs can cover multiple variants, so use the exact endpoint slug where one is exposed.
Source: [OpenRouter routing](https://openrouter.ai/docs/guides/routing/provider-selection).

| Model | Proposed provider behind OpenRouter | Public evidence and remaining checks |
|---|---|---|
| Qwen3.8-27B | DeepInfra, `deepinfra/bf16` | Endpoint catalogue lists reasoning, tools and structured outputs, 262144 context and $0.15/$1.875 per million input/output tokens at inspection; discounted price can change. |
| gpt-oss-120b | DeepInfra, `deepinfra/bf16` | Catalogue lists reasoning, tools and structured outputs, 131072 context and $0.037/$0.17. The precision label is provider metadata, not proof of original-weight fidelity. |
| DeepSeek V4.1 Flash 1017 | DeepInfra standard, exact variant slug pending | Model page lists this provider and snapshot. Endpoint JSON did not expose a readable complete entry through the browsing tool; exact slug, features and effort mapping remain a pre-run check. Do not silently substitute the September target. |
| GPT-6 Luna | OpenAI standard, `openai` | Catalogue lists tools/reasoning/structured outputs and $0.10/$0.50 short-context pricing. Do not opt into flex/priority. |
| Claude Haiku 5.5 | Anthropic standard, `anthropic` | Catalogue lists reasoning/tools/structured outputs and $0.10/$0.50 up to 100k prompt tokens. Forced tool choice is not advertised; automatic tool choice is. |
| GPT-6.1 Sol | OpenAI standard, `openai` | Catalogue lists tools/reasoning/structured outputs and $2/$10 short-context pricing. Do not opt into flex/priority. |

Sources: [Qwen endpoints](https://openrouter.ai/api/v1/models/qwen/qwen3.8-27b/endpoints),
[gpt-oss endpoints](https://openrouter.ai/api/v1/models/openai/gpt-oss-120b/endpoints),
[DeepSeek provider listing](https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017),
[Luna endpoints](https://openrouter.ai/api/v1/models/openai/gpt-6-luna/endpoints),
[Haiku endpoints](https://openrouter.ai/api/v1/models/anthropic/claude-haiku-5.5/endpoints),
[Sol endpoints](https://openrouter.ai/api/v1/models/openai/gpt-6.1-sol/endpoints).

Rationale is a reproducible route with documented necessary interfaces and known precision
metadata where available, rather than a changing cheapest-provider choice. DeepInfra can
serve all three open-weight-family candidates, but it is not proved fastest or highest quality.
Their results will describe these deployments, not every possible host of each model. Provider
selection is now approved subject to the checks above; pricing is a snapshot, not a budget
or an account-access guarantee.

Public metadata fetch from the local shell failed at DNS resolution. Browser access supplied
the public sources instead. No key was read or authenticated model call made. The exact
DeepSeek endpoint check remains incomplete; no user account connectivity has been established.

The repo pins LangChain 1.3.1 and langchain-openai 1.2.2. Current make_model unconditionally
passes temperature zero. Installed adapter source exposes use_responses_api and
use_previous_response_id, but source inspection is not end-to-end compatibility proof.
OpenRouter's Responses API is stateless and rejects store:true/non-null previous_response_id;
full required history must be supplied explicitly. Plan a compatibility check through the
isolated runner; do not silently migrate the working application.
Source: [Responses contract](https://openrouter.ai/docs/api_reference/responses/overview).
Context Hub/installed-version documentation must be checked under get-api-docs before coding;
this turn performs planning and read-only source inspection only.
