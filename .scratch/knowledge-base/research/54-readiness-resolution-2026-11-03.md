# T54: compatibility readiness repair and disposition

Date: 3 November 2026. Author asked to resolve the initial compatibility gaps.

## Outcome

All six configurations pass the tool round trip and the unchanged literal citation check
under one repaired compatibility setup. The requested native control fields are now visible
in twelve transformed upstream requests and match the approved settings. Screening is ready
for the author's separate execution go. No screened answer, label, model selection or live
Langfuse upload occurred.

The original failed gpt-oss answer remains in `compat-live`. The repair is one shared prompt
clarification, not a relaxed check: the connection prompt now explicitly says to use ordinary
ASCII square brackets. The investigator, specialist and reviewer prompts, cases, gold, rubric,
model providers, sampling and requested reasoning levels are unchanged.

## Versioned evidence

The separate bundle `backend/evals/comparison/runs/compat-readiness-1/` has a `repair_context`
event linking all six originals and their manifest hash. Each paid command included the
original bundle through `--cost-run`. All six slots were dispatched separately and inspected.
New prompt version: `28b2667c34b4`; adapter version: `2`; fixture version: `f903b7f47620`.
All six configurations received the same setup change. Neither bundle is overwritten.

Adapter version 2 requests `debug.echo_upstream_body` on tool-bearing compatibility requests.
It saves the transformed provider request under `continuation.debug_events`, with secrets
removed. Only `continuation.output` is replayed into model history. The existing mirror
removes the entire continuation field recursively, so diagnostic inputs stay local.
Failure and malformed-response paths retain any available diagnostic body too.

Machine-readable [evidence summary](54-readiness-repair-evidence.json) links every inspected
diagnostic to its original hashed artifact. The relevant public
[OpenAPI diagnostic schema](54-upstream-debug-contract.json) is saved separately.

| Configuration | Tool and citation checks | Native fields observed | Upstream output limit observed |
|---|---|---|---:|
| Qwen3.8-27B | Pass | reasoning enabled, medium; temperature 1, top_p 0.95, top_k 20 | 131072 |
| gpt-oss-120b | Pass | reasoning enabled, medium; sampling omitted | 117806 then 117775 |
| DeepSeek V4.1 Flash 1017 | Pass | reasoning enabled, high; sampling omitted | 131072 |
| GPT-6 Luna | Pass | medium, standard, all_turns; store false; default service | 65536 |
| Claude Haiku 5.5 | Pass | thinking adaptive; output_config effort medium; sampling omitted | 65536 |
| GPT-6.1 Sol | Pass | medium, standard, all_turns; store false; default service | 65536 |

DeepInfra's omitted service tier means standard service under its documented contract.
Luna/Sol also receive the encrypted-reasoning include field. All returned output items were
replayed in exact order for the tool return. The upstream DeepInfra assistant messages retain
`reasoning_content` where returned. Haiku did not return a thinking block on its tool-call
turn in this repeat, so there was no such block to replay on that turn.

The output limits above were supplied downstream by the gateway/provider. Our wire requests
still omit output caps. They differ from the advertised endpoint ceilings and are hidden by
the normalized response's `max_output_tokens: null`. B-151 records this discovery. Record these
as observed defaults, not new evaluation-imposed limits or guaranteed future defaults.

Verification reaches the observable API boundary: OpenRouter exposes the body it says it
sends, the provider documents those fields, and the request completes. We cannot independently
inspect the provider's inference engine. No equal-compute, hidden-setting attestation,
comparative performance or investigation-quality claim follows from this connection check.

## Billing disposition

| Bundle | Requests | Rate-limit retries | Known charge US dollars | Missing-charge responses |
|---|---:|---:|---:|---:|
| Original compat-live | 14 | 2 | 0.001584 | 2 |
| Shared repair compat-readiness-1 | 13 | 1 | 0.001556 | 1 |
| Combined | 27 | 3 | 0.003140 | 3 |

All three errors are definite HTTP 429 upstream capacity rejections with `engine_overloaded`,
no selected endpoint, no generation ID and no usage. There were no paid auxiliary services.
OpenRouter's [published pricing policy](https://openrouter.ai/pricing) says failed attempts
have no model-token charge. DeepInfra's
[capacity-rejection documentation](https://docs.deepinfra.com/chat/overview) says a rejected
request never reaches the model and is not billed.

Each bundle now contains an append-only `billing_disposition` note classifying those errors
as nonbillable rejections under the published policy. This resolves their operational billing
treatment. The absence of a returned charge or per-request account record remains explicit:
no `cost_settled` event or invented numeric zero was written. Resource summaries correctly
retain `cost_complete: false`. The known total is not a verified account-invoice total.
No US$15 checkpoint was reached on known charges.

## Verification

- Focused adapter and runner tests: **75 passed in 39.79 seconds**. They cover diagnostics
  on success/failure/malformed output, secret removal, exclusion from replay/mirror, and
  keeping a correct fact with non-ASCII citation as a failed contract.
- Focused Pyright: zero errors/warnings. Focused Ruff: clean after fixing a test import layout.
- Live repaired run: six completed trials, twelve successful requests, one recovered HTTP 429.
- All 62 event artifact references match their recorded hashes; all thirteen started requests
  have terminal records; six fresh memory IDs; six exact ordered output replays verified.
- All twelve successful upstream bodies match their requested provider-native control fields.
- Configured OpenRouter and Langfuse credential values are absent from the repaired bundle.
- Original frozen fixtures remain unchanged. No application suite rerun was needed.
- Sandbox blocked a public schema fetch's DNS; the authorised public read succeeded outside
  the sandbox. No new account, key, dependency or provider was introduced.

## Sources and checked contract

Context Hub had no OpenRouter entry. The official [OpenAPI schema](https://openrouter.ai/openapi.json)
defines ResponsesRequest.debug and the initial response.debug event's upstream body.
The two generated reference pages returned 404 when opened; the schema supplied the contract.
Transport remains Requests 2.34.2 under the already checked documentation.

DeepInfra's [reasoning guide](https://docs.deepinfra.com/chat/reasoning) documents the
`reasoning` object as an alternative to `reasoning_effort`. Its
[API reference](https://docs.deepinfra.com/api-reference/chat-completions/openai-chat-completions)
confirms the field. The observed Haiku body uses the native controls described in the
[model documentation](https://platform.claude.com/docs/en/models/haiku-5-5/overview).
OpenAI's [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning) and the
[Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)/
[Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) pages establish the matching
native reasoning and Responses tool interfaces. These sources support the API-contract
interpretation; the saved upstream bodies supply this run's observations.

## Concrete next execution

`screen-live` has been created with 72 frozen slots and no request events. Creating it loaded
no credentials and spent nothing. Start with slot 1, inspect setup and advance only through
slot 24 under the bounded first-pass approval. Both paid compatibility bundles must be in the
cost context. Later passes require the existing setup-review gate.

```sh
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-live --execute-paid --until-slot 1 --cost-run evals/comparison/runs/compat-live --cost-run evals/comparison/runs/compat-readiness-1
```

This command is prepared, not executed. T54 remains claimed and its live scored-mirror
acceptance criteria remain unticked. B-150's setup remedy and AUD-079's readiness evidence are
ready for author review; original failures and billing disclosure limits remain visible.
