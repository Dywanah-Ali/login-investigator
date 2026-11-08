# T45: handling oversized reranking inputs

Date: 8 November 2026. Tier 3 focused decision research. Findings for discussion, not an
approved overflow policy or implementation release.

## Finding and correction

The earlier proposal to stop ranking and try a narrower search was local reasoning, not an
established best practice. More importantly, it treated a candidate pool too much like one
chat prompt. Cohere describes its context limit as the query plus **one document**, separately
for each document. Forty passages do not collectively have to fit its 4,096-token model
window. A request can still face separate document-count, payload, runtime or provider limits.
[Cohere model documentation](https://docs.cohere.com/docs/rerank).

The focused sources support distinguishing these limits and controlling document chunking.
They do not establish narrower retrieval as the preferred first response to a size problem.
No evidence found here warrants dropping already admitted candidates simply because their
combined tokens exceed one model context window.

## Scope and method

Checked official Cohere model, best-practice, API and release documentation; official
Sentence Transformers documentation for batching; and Voyage documentation to distinguish
provider-specific limits. Web search supported discovery and primary pages were opened.
The parent session independently inspected OpenRouter guidance and the local adapter.
No inference, tokenizer download, dependency change, application test or live endpoint probe ran.
This does not choose another model, change the approved 20 plus 20 candidate allowances,
change five final passages, or close AUD-062.

## What the primary sources establish

| Source | Documented behaviour | Limit of this evidence |
| --- | --- | --- |
| [Cohere Rerank](https://docs.cohere.com/docs/rerank) | Rerank v3.5 has a roughly 4k context. Each query/document pair counts separately; the overview describes internal chunk processing for longer documents. | Does not establish OpenRouter's exact forwarding, truncation or aggregate payload rules. |
| [Cohere best practices](https://docs.cohere.com/docs/reranking-best-practices) | For v3.5, its worked example splits document text into model-sized pieces after allowing for query and reserved tokens, then uses the maximum piece score. It recommends doing chunking yourself when more control is needed. Queries beyond 2,048 tokens are described as truncated. | Its earlier-model `max_chunks_per_doc` discussion must not be conflated with the v2 API contract below. Maximum-piece relevance does not prove all conditions were understood together. |
| [Cohere v3.5 release, 2 December 2024](https://docs.cohere.com/changelog/rerank-v3.5) | The v2 API replaces `max_chunks_per_doc` with `max_tokens_per_doc`, default 4,096, and truncates documents beyond that setting. | Model context and the maximum document text accepted for processing are different controls. |
| [Cohere v2 API](https://docs.cohere.com/reference/rerank) | Documents are automatically truncated to `max_tokens_per_doc`; default 4,096. The API recommends no more than 1,000 documents for optimal performance. `top_n` controls returned results. | The 1,000 recommendation is not a verified OpenRouter hard limit. Returning all scores does not prove all text was processed. |
| [Sentence Transformers CrossEncoder](https://www.sbert.net/docs/package_reference/cross_encoder/model.html) | Scores input pairs; `rank` has a separate batch-size parameter and returns ranked document indices/scores. Input sequence length is a different control. | Establishes batching as a normal cross-encoder execution mechanism, not a contractual guarantee that separate OpenRouter calls produce interchangeable scores. |
| [Voyage rerankers](https://docs.voyageai.com/docs/reranker) | Separates query size, each query/document pair, document count and total request tokens. Offers truncation or an error when truncation is disabled. | Comparison only. Its numeric limits and switches do not apply to Cohere/OpenRouter. |

The Cohere pages mix general model processing descriptions and API-version-specific controls.
Read together, they are sufficient to reject the single-window-for-all-candidates assumption,
but insufficient to promise that arbitrary long text survives our routed endpoint intact.

## Comparison of the proposed responses

The assessments below are local design inferences from those sources and IC-06/07, not
externally prescribed policy.

| Response | Appropriate problem | Assessment for T45 |
| --- | --- | --- |
| Keep the existing short passages and score all admitted candidates | Each query/passage fits, and the request meets actual endpoint limits | Preferred ordinary path. No additional candidate cut is justified by summing passage tokens against one context window. |
| Cut the tail of a passage | One passage exceeds its permitted size | Providers may do this automatically. It risks losing a condition; successful scoring must not be mistaken for full-text review. |
| Split an oversized passage into source-linked pieces | One passage exceeds its permitted size | Better-supported direction than automatic narrowing. Preserve original identity and necessary context. Piece aggregation and restoration of conditions need an explicit local design. Splitting is not proof of semantic completeness. |
| Batch the same admitted candidates with the same query | An actual count/payload limit prevents one request | Candidate-preserving option to investigate if needed. Keep model/settings fixed, preserve global identity, validate every score and merge globally. Confirm cross-call comparability before adoption; never merely interleave batch ranks. |
| Remove whole candidates | A deliberate admission/cost bound | Trades coverage for resources. The approved admission bounds already do this. A new overflow reduction policy would introduce another evidence-loss point. |
| Search again with a narrower question | A missing evidence need or poor relevance warrants refinement | A semantic recovery action, not a general repair for request packaging. It changes the candidate population and may omit evidence already found. No reviewed source establishes it as the default size-overflow remedy. |
| Return an explicit limitation | No approved safe handling remains within execution limits | Honest final fallback. Preserve earlier evidence and distinguish incomplete ranking from no matches. |

## Local relevance and unresolved endpoint details

The saved [source profile](45-candidate-volume-profile-2026-11-08.json) contains 320 prepared
passages, with maximum length 2,134 characters. This is not a provider-token measurement and
does not certify query-plus-passage fit. It also does not demonstrate an existing size failure.

Read-only inspection of `backend/login_investigator/knowledge_base/reranking.py` found that
the adapter sends model, query, document strings and `top_n` equal to candidate count. It
checks that every input has a returned score, then sorts globally. It does not explicitly
set truncation, token or provider controls. This is an implementation observation, not a
reproduced defect or authority to change the old tools before planned design is complete.

The indexed [OpenRouter endpoint reference](https://openrouter.ai/docs/api/api-reference/rerank/create-rerank)
returned 404 on direct opening. The parent checked the readable
[OpenRouter RAG guide](https://openrouter.ai/docs/cookbook/evaluate-and-optimize/rag), which
describes comparing documents to a query and paragraph/section/semantic chunking. Neither
establishes the exact routed v3.5 input limits or truncation controls. Keep these unknown;
do not copy another provider's limits or assume every Cohere v2 parameter is forwarded.

## Recommended next design step

### Follow-up: official OpenRouter schema inspected

After the author's acceptance of the revised direction, read the official Python SDK
[rerank schema at commit f0ceb9b](https://github.com/OpenRouterTeam/python-sdk/blob/f0ceb9be02fd9c78a4898382b74b36db11b41610/src/openrouter/operations/creatererank.py)
through the read-only GitHub API. The first sandbox network request failed; the approved
network retry succeeded. No SDK was installed and no inference request was submitted.

The request declares documents, model, query, provider preferences, top_n and observability
fields. It does not declare max_tokens_per_doc, max_chunks_per_doc or a truncation switch.
The response declares scores, input indices, echoed documents, model, optional provider
and usage; it does not declare per-passage truncation or processed-token coverage. Echoed
input text is not a receipt proving that all text was scored. These are observations about
this published schema, not proof that undocumented server parameters are rejected.

This resolves the earlier inability to inspect the public request contract. It does not
resolve runtime truncation, tokenizer compatibility, aggregate request limits or cross-call
score comparability. Do not borrow Cohere-native controls without forwarding evidence.

### Direction retained

Withdraw the earlier stop-and-narrow recommendation as the default. Keep normal scoring of
the admitted short passages. Design separate checks for query length, individual passage
length and actual request limits. Treat final research/chat context allocation as a separate
boundary again. If an oversized individual passage needs handling, discuss source-preserving
splitting; if a genuine request-level limit occurs, discuss bounded batching after compatibility
is established. Explicit failure remains the fallback when those mechanisms are unavailable.

This is a research-backed direction, not approval of numeric limits, splitting, batching or
new evaluation work. The eventual implementation must demonstrate that important supporting
and competing evidence survives. Existing gates and the analyst-owned verdict remain intact.
