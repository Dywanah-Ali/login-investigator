# T52: Screening prices and request reservations

Author ruling, 2 November 2026: reservation proposal rejected. Keep the public price evidence;
the accounting contract below is historical, not required work. Track actual spending against
a US$25 planning budget, with reviews at US$15 and after 24 results. No hard final-charge
guarantee, request reservations or worst-case billing gate. See T52 and the comparison protocol.

Checked: 2 November 2026. Status: public price verification complete; accounting design
proposed, not implemented or runtime-proven. No credentials read, account changes or inference.

## Finding

Keep the approved US$25 allowance as a starting budget, not a completion guarantee. Current
published prices permit inexpensive trials, but no token/call caps means total usage is
unknown. A request reservation can protect the remaining allowance without constraining
model output: hold its conservative possible cost before dispatch, then reconcile actual
charges. This is a design inference, conditional on verified billing bounds and accounting.

## Selected standard-service prices

USD per million tokens, as returned by the public endpoint catalogue. Input is uncached;
output includes billable generated tokens under the endpoint's accounting. Listed prices
are used directly, without applying the separately reported discount a second time.
The [raw snapshot](52-provider-price-snapshot.json) preserves all returned fields for each
selected route, including tier overrides and native output ceilings.

| Candidate | Selected route | Base input | Base output | Native output ceiling |
|---|---|---:|---:|---:|
| [Qwen3.8-27B](https://openrouter.ai/api/v1/models/qwen/qwen3.8-27b/endpoints) | DeepInfra `deepinfra/bf16` | $0.15 | $1.875 | 235,929 |
| [gpt-oss-120b](https://openrouter.ai/api/v1/models/openai/gpt-oss-120b/endpoints) | DeepInfra `deepinfra/bf16` | $0.037 | $0.17 | 117,964 |
| [DeepSeek V4.1 Flash 1017](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash-1017/endpoints) | DeepInfra `deepinfra/fp8` | $0.098 | $0.294 | 393,216 |
| [GPT-6 Luna](https://openrouter.ai/api/v1/models/openai/gpt-6-luna/endpoints) | OpenAI `openai` | $0.10 | $0.50 | 128,000 |
| [Claude Haiku 5.5](https://openrouter.ai/api/v1/models/anthropic/claude-haiku-5.5/endpoints) | Anthropic `anthropic` | $0.10 | $0.50 | 128,000 |
| [GPT-6.1 Sol](https://openrouter.ai/api/v1/models/openai/gpt-6.1-sol/endpoints) | OpenAI `openai` | $2 | $10 | 128,000 |

These ceilings are catalogue metadata, not proposed evaluation caps or evidence that a
request with omitted output controls actually receives the full ceiling. Verify combined
reasoning/output accounting and effective defaults during compatibility work.

DeepSeek's previously unresolved standard route is now identified in public metadata.
Its flex and priority siblings exist but are not the approved standard configuration.
gpt-oss also has a more expensive DeepInfra fp8 route; using only the provider's base name
would not adequately specify the intended variant.

Higher input tiers matter. Luna's catalogue override at 272,000 prompt tokens changes
input/output to $0.20/$0.75 per million; Sol's at the same threshold changes to $4/$15.
Haiku's override at 100,000 prompt tokens changes to $0.50/$2.50. Cache-write prices also
exist for these routes and must be included if applicable. Cache savings are not assumed.
Threshold values are catalogue fields; verify boundary semantics before relying on a
cheaper tier. Sources: the corresponding endpoint records linked above.

Pin standard service explicitly, not merely the provider name. OpenRouter documents
`service_tier: "default"`, exact endpoint variants, disabled fallbacks and parameter-support
filtering. Its `provider.max_price` filters unit prices; it is not a total dollar budget.
Sources: [service tiers](https://openrouter.ai/docs/guides/features/service-tiers),
[provider selection](https://openrouter.ai/docs/guides/routing/provider-selection).

## Cost illustrations, not forecasts

For all 72 scored trials, twelve per model, the arithmetic is:

`sum over six models: 12 × (aggregate trial input × input rate + aggregate trial output × output rate)`

| Aggregate tokens per trial across all its requests | Cost of 72 trials |
|---|---:|
| 10,000 input + 5,000 output | $1.09854 |
| 50,000 input + 20,000 output | $4.69236 |
| 100,000 input + 100,000 output | $18.98880 |

These are hypothetical usage scenarios calculated from the snapshot, not expected usage.
Every individual request is assumed below its higher-price threshold; aggregate trial input
can span multiple requests. Include repeated conversation history in aggregate input and
reasoning in output without double counting. No cache savings, setup sessions, repair reruns,
extra retry usage beyond the assumed totals, paid judges or architecture trials are included.
The US$25 allowance covers inference charges from existing credits in this proposal; no
credit purchase, payment fee, tax or account modification is proposed or authorised.

## Proposed accounting contract

1. Before each billable dispatch, including retries, save the request identity, selected
   route, price snapshot and a conservative dollar reservation. Calculate it from a verified
   input bound and the provider's native combined generated-token bound, at applicable upper
   unit prices, plus any applicable fees. If exact input counting is unavailable, the verified
   context maximum is a conservative fallback. This over-reserves; it does not shorten output.
2. Admit only when settled charges + outstanding reservations + new reservation fit $25.
   Check before every dispatch, not only at case boundaries. Do not let hidden SDK retries
   bypass admission. This adds no retry-count cap. If the bound cannot be established, pause
   before dispatch and record the gap; do not invent a token cap or assume average usage.
3. Save the generation ID as soon as available. On completion, replace that request's
   reservation with its reported charge exactly once. Reconcile a missing terminal usage
   record by generation ID. Missing usage is unknown, never zero; retain the reservation.
4. Prefer streaming to enforce the agreed timeouts. If cancelled, keep the reservation until
   charges settle. Never use elapsed time or observed tokens/second as a billing upper bound.
   Unresolved requests can still consume the budget after the client has stopped waiting.
5. Review at $15 and after 24 scored attempts as approved. If admitting the next request
   could cross $15, review first. This preserves the checkpoint without interrupting a model
   for a new token rule. If insufficient funds remain for a reservation, pause the run,
   preserve incomplete coverage and report it separately from a model-quality failure.
6. A dedicated evaluation key with a non-resetting $25 limit is a useful optional second
   barrier and simplifies attribution. It is not created or required by this research.
   Existing application credentials/settings remain unchanged. Key-limit semantics alone
   are not proof of a strict final-charge ceiling; see the independent check below.

The proposed upper-bound method needs verification for native reasoning accounting,
provider limits, price changes, prompt/cache tiers and all automatic retries before it can
be described as a tested guarantee. Freeze or reject unit-price changes where supported;
the exact price-filter interaction with tier overrides is still a compatibility check.
Paid provider plugins are outside the intended synthetic task; include their costs if a
later approved runner adds any. A finite budget cannot guarantee all uncapped trials finish.

## Documentation evidence and limits

OpenRouter's usage documentation exposes charged cost and native token breakdowns. Its
generation endpoint supplies historical cost and provider metadata for reconciliation.
Sources: [usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting),
[generation metadata](https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation).

OpenRouter documents streaming cancellation for OpenAI, Anthropic and DeepInfra, but
non-streaming cancellation does not stop billed completion. Capture the generation ID
from the response header when available. This is documentation evidence, not tested
behaviour of our adapters. Source: [streaming](https://openrouter.ai/docs/api_reference/streaming).

Its account in-flight holds use estimates with a fixed cap, cover only some accounts and
do not include every charge type. Do not equate those holds to this experiment's $25
ledger. Source: [limits](https://openrouter.ai/docs/api_reference/limits).

The [independent spending check](52-budget-enforcement-check.md) examines key-limit and
settlement limitations separately. Context Hub search returned no OpenRouter entry;
official documentation and unauthenticated `/api/v1/models/.../endpoints` metadata were used.
The sandboxed public fetch failed DNS; an approved network fetch succeeded without credentials.
No account access, inference, application implementation or runtime tests occurred.
