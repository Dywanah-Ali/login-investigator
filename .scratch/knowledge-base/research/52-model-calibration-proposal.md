# T52: Model baseline for the twelve-answer calibration

Date checked: 2 November 2026. Status: research-backed proposal, not a selected app model.
Companion: `52-model-selection-industry-evidence.md` for security-system precedents and
Google/Anthropic documentation. Research does not establish a universal industry standard.

## Current status after author correction

The earlier Sol recommendations below are historical proposals, now superseded pending
[broad model research](52-broad-model-shortlist.md). The author requested cheaper/faster
open-weight and proprietary candidates without requiring published success on our exact
use case. See [research method and proposed screening](52-model-screening-evidence.md).
No model is selected; additional screening execution remains unapproved.

## Approved screening pool, 2 November 2026

The author approved six candidates: Qwen3.8-27B, gpt-oss-120b, DeepSeek V4.1 Flash,
GPT-6 Luna, Claude Haiku 5.5 and GPT-6.1 Sol. Sol is a higher-capability reference,
not the selected winner. The exact DeepSeek served version and all provider routes
must be verified before execution.

GLM-5.3-Flash, MiniMax-M3.1-Flash and Mistral Small 4 move to reserve to limit review
workload while retaining smaller open weights, inexpensive hosted options, proprietary
challengers and a higher-capability reference. This is not evidence of inferior performance.

Screen models using the same single-investigator setup before freezing a baseline for
A/B/C. Four cases per model would produce 24 final answers, but that case count, repeat
policy, settings, budget and execution remain to be agreed. Approval of this pool does
not authorise inference calls or select a permanent production model.

## Production-selection clarification

Author ruling, 2 November: use a balanced production-selection approach, weighing investigation
quality, response time and sustainable cost. Start with capable mid-priced candidates rather
than automatically choosing either the cheapest or the flagship. Sol 6.1 and Claude Sonnet 5.5
remain candidates; exact model, effort and route are undecided. All candidates face the same
quality requirements. No additional runs are authorised by this preference.

After the initial proposal, the author asked to use a realistic production candidate as the
comparison baseline. Sol was proposed as the tested app model, not the model authoring or
grading evaluations. The initial recommendation did not establish production fitness; treat
it as one candidate pending workload, quality, cost and latency requirements.

A subsequent official lifecycle check found GPT-4.1 is deprecated with OpenAI API shutdown
scheduled for 14 January 2027, alongside GPT-4o mini. See the
[official notice](https://developers.openai.com/api/docs/deprecations) and
[GPT-4.1 model page](https://developers.openai.com/api/docs/models/gpt-4.1).
The older security-system examples remain valid research evidence, but GPT-4.1 is not
recommended as this phase's new long-lived production baseline. This establishes OpenAI's
schedule; separate provider routing/availability must not be presumed identical without checks.
The model-page standard rates were $2 input/$8 output per million tokens at inspection.
Per-token rates alone do not determine investigation cost; call count and reasoning usage matter.

## Recommended comparison design

Use one capable reasoning model, one provider route and one explicit reasoning setting for
every generative role in A/B/C for the first calibration. Role prompts/context differ as
required by the architecture, while model capability does not. The current app's gpt-4o-mini
is not automatically the baseline for the expanded objective. P-03 requires evaluating model
fitness rather than shaping the new investigation around its limitations.

Proposed initial choice: **GPT-6.1 Sol, high reasoning**, for the investigator and any added
specialist. This is an engineering starting hypothesis: documented complex-work capability
at a lower listed price than Astra, not a claim of measured security-investigation superiority.
Use GPT-6 Astra as a higher-capability alternative/reference if the author prioritises that
for calibration or common failures warrant a separate comparison. Do not add those extra
model runs silently or switch model halfway through A/B/C.

| Design | Front investigator | Applicability specialist | Review specialist |
|---|---|---|---|
| A | Same selected model/settings | None | None |
| B | Same selected model/settings | Same selected model/settings | None |
| C | Same selected model/settings | None | Same selected model/settings |

The orchestrator performs synthesis and evidence interpretation; it is not merely a routing
classifier. The applicability specialist makes contextual judgments and the reviewer tests
claims. None should be presumed suitable for a tiny/fast model merely because its task is
narrow. Exact counts, query execution and permission traversal remain in core code.

Same-model roles can still have correlated errors. Separate context does not create a fully
independent judge. Mixed-family reviewing is a later candidate, distinct from the separately
agreed advisory evaluation judge under T30. Keep that judge out of the scored app architecture.

## Verified OpenAI capability and price references

[OpenAI's model selection guidance](https://developers.openai.com/api/docs/guides/model-selection)
recommends representative-input comparisons and varying reasoning effort while holding model
and inputs fixed. This supports controlled experimentation, not a security-specific choice.

| Candidate | Officially documented properties relevant here | Published standard text rate per million tokens |
|---|---|---|
| [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Complex professional work; low/medium/high/xhigh/max effort; structured output and function calling | $2 input, $10 output |
| [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | Flagship for demanding reasoning; low/medium/high/xhigh/max effort; structured output and function calling | $10 input, $50 output |

These are dated published rates for standard text usage, not the price of the calibration.
Caching, long-context rates, service tiers, reasoning/output usage and actual provider routing
can change total cost. No token estimate or spending cap is established yet. Vendor capability
descriptions are not evidence that either model passes our cases.

Both model listings were also opened on OpenRouter:
[Sol](https://openrouter.ai/openai/gpt-6.1-sol),
[Astra](https://openrouter.ai/openai/gpt-6-astra).
Listings establish advertised availability, not access through this account or correctness
of the current adapter. No credentials were read and no inference requests were made.

## Compatibility and reproducibility work before execution

The current `backend/login_investigator/agent.py::make_model` uses `init_chat_model` with
OpenRouter's OpenAI-compatible URL and temperature 0. It must not be assumed that a model-name
substitution preserves reasoning controls, tool behaviour or structured output. The official
Sol page specifically says tool calling requires Responses API. Check the chosen OpenRouter
route/adapter explicitly; public model capability does not prove route-level compatibility.
The fixed-evidence calibration can use supplied case files, but any tool-free simplification
must be stated and cannot count as proof of later tool-using integration.

Before a run, record the exact model identifier/version where exposed, provider route and
fallback policy, requested/accepted reasoning setting, sampling settings supported by that
model, prompts, schemas, output/token limits, timeouts, retry policy and usage accounting.
Do not silently force an unsupported temperature or let routing fall back to a different model.
Pin a snapshot when offered; otherwise disclose alias/version uncertainty and record returned
metadata. Verify supported settings without pretending that temperature zero is deterministic.

## After calibration

First inspect whether failures arise in missing evidence, prompts, model reasoning or handoffs.
If all A/B/C fail for the same reasoning reason, a stronger-model comparison may be useful;
a stronger model cannot recover unavailable facts. If a specialist helps, test a cheaper
model for that role later using the same required outcomes and cost/latency measurements.

Using different models for each architecture initially would compare complete systems, not
isolate architecture. That can be a valid later product experiment if labelled accordingly.
The first 12 answers are scoring/runner calibration, not proof of model superiority or final
architecture selection. Model choice, effort and cost limit await the author's ruling.

## Selection resumed, 2 November 2026

Official model pages rechecked: both Sol 6.1 and Sonnet 5.5 list standard text prices of
$2 input/$10 output per million tokens. These do not establish equal investigation cost.
Sol documents medium as default and Responses API as required for tool calling. Sonnet
lists high as default, rejects temperature/top_p/top_k and lists retirement no sooner than
28 September 2027. OpenRouter lists both models, but account/adapter support remains untested.
Sources: [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[Sonnet](https://platform.claude.com/docs/en/models/sonnet-5-5/overview),
[OpenRouter Sol](https://openrouter.ai/openai/gpt-6.1-sol),
[OpenRouter Sonnet](https://openrouter.ai/anthropic/claude-sonnet-5.5).

Revised recommendation awaiting author choice: Sol 6.1 at medium reasoning for the provisional
calibration baseline, superseding the earlier high-effort recommendation. Rationale: a
capable professional-work candidate at its documented default, aligned with the author's
balanced preference. This is a starting hypothesis, not evidence of superiority over Sonnet
or production fitness. Keep the selected model/settings fixed across A/B/C; measured quality,
latency and cost decide later changes. Sonnet 5.5 remains a credible alternative. No inference
call, provider choice, adapter migration or permanent production adoption has occurred.
