# Investigation retrieval: decomposition, coverage and bounded recovery

Date: 29 October 2026. Tier 3 research. Status: evidence and proposals only.

This note follows the [T22 query probe](22-query-decomposition-probe.json) and
[AUD-062](../../../docs/audit/improvement-register.md#aud-062-compound-retrieval-question-loses-the-mfa-exception-register).
It does not approve implementation, change the spec or gold, or close the retrieval gap.
Perplexity was used for research discovery and targeted search. Material conclusions below
are checked against primary papers or official documentation. External prompts used a generic
investigation scenario, not private repository contents.

## Plain-English conclusion

The useful principle is **search separately for the evidence needed to answer each part,
then check what is still missing**. A librarian given a compound question should have a
checklist, rather than return twenty books about its most prominent topic.

Our probe supports that direction. The whole K04 question finds the response runbook but
misses the MFA exception register. A neutral MFA-focused query finds the register at rank 7;
a procedure-focused query finds the runbook at rank 1. These were human-written queries after
we saw the failure. They establish that the passages are recoverable. They do not establish
that an automatic planner will choose those queries or retain both passages inside one final
twenty-candidate budget. [Local probe](22-query-decomposition-probe.json)

The proposed safety net has two distinct jobs:

1. Search again when a known evidence need remains unanswered.
2. Keep a separate broad route because the initial checklist itself might omit a need.

The second matters. A fallback activated only when the planner says something is missing
cannot reliably catch a need that the planner never listed. Keeping an original-question
route alongside focused routes is a reasonable mitigation to test. It is not a guarantee
that all relevant evidence will be found. Existing systems retain original queries, but
their existence does not prove the policy will solve this application's failures.
[IRCoT](https://aclanthology.org/2023.acl-long.557/),
[LlamaIndex example](https://developers.llamaindex.ai/python/framework/integrations/retrievers/simple_fusion/)

For this application, start by evaluating a checklist derived from the finding's structured
facts. T26 already requires that boundary. A future model could propose additional searches,
but code would still enforce permissions, scope and spending limits. Changing ownership of
the investigation plan requires an author-approved spec decision. Production growth does
not itself require unlimited retries, autonomous agents, or moving to a cloud search platform.
This is our architectural proposal, informed by the research below and the existing
[T26 contract](../issues/26-investigate-alert-package.md).

## What the research actually supports

The table distinguishes experimental papers from documented implementations and engineering
advice. None demonstrates complete retrieval for this security investigation domain.

| Source and date | Supported finding | Limit and relevance here |
| --- | --- | --- |
| [IRCoT, ACL 2023](https://aclanthology.org/2023.acl-long.557/), [paper](https://aclanthology.org/2023.acl-long.557.pdf) | Interleaves retrieval with reasoning because later searches can depend on earlier evidence. Its procedure begins with the original question and has stopping and passage limits. Its retrieval comparison uses a matched maximum passage budget. | Multi-step question-answering benchmarks, not enterprise investigations. Supports testing iterative retrieval and fair budgets; does not establish our planner or thresholds. |
| [Adaptive-RAG, NAACL 2024](https://aclanthology.org/2024.naacl-long.389/) | Learns to select between no retrieval, single retrieval and iterative retrieval according to question complexity. | The paper acknowledges imperfect complexity labels. Routing is another fallible component. A small task need not pay for the most expensive route, but the router itself needs evaluation. |
| [Google Research, sufficient context, 14 May 2025](https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/) | Distinguishes relevant context from context containing enough information to answer. Investigates an automatic sufficiency evaluator against human judgments and selective answering. | A sufficiency judgment is not proof that the corpus was exhaustively searched. It can be wrong. Use it as an evaluated signal, never a completeness oracle. |
| [CRAG, 2024](https://arxiv.org/abs/2401.15884) | Uses a retrieval evaluator to select corrective actions. Includes external web retrieval and filtering/recomposition of retrieved content. | Its document decomposition is not the same as splitting an investigation question. Web recovery cannot establish private account configuration facts; that restriction is our domain inference, not a CRAG result. |
| [LlamaIndex Simple Fusion Retriever, current documentation](https://developers.llamaindex.ai/python/framework/integrations/retrievers/simple_fusion/) | The documented example searches the original query plus generated related queries, aggregates and deduplicates results. | Related paraphrases are not necessarily distinct evidence needs. This is an implementation example, not evidence that query expansion improves our recall under a fixed budget. No framework adoption is proposed. |
| [Azure retrieval reasoning effort, current documentation](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort), [maturity overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview) | Medium effort evaluates initial results and permits one revised-plan follow-up. It can focus or broaden the search and change sources. Generated queries appear in activity logs. | A useful bounded-recovery example, not an independent efficacy study. As checked on this date, minimal extractive retrieval is generally available; model planning and nonminimal effort are preview features. Do not treat preview planning as a production recommendation. |
| [Anthropic, Building effective agents, December 2024, current page](https://www.anthropic.com/research/building-effective-agents) | Separates predefined workflows from model-directed agents and advises increasing complexity only when measured benefits justify it. | First-party engineering guidance, not a controlled comparison for this app. A deterministic workflow can be a deliberate architecture choice while leaving room for future adaptive planning. |

### Upfront planning and iterative planning solve different problems

An upfront plan separates known independent needs before any retrieval. In our example,
account reach and the explanation for MFA behavior belong to different evidence routes.
Independent lookups can run together. An iterative plan is useful when a retrieved fact
reveals the next question, such as a policy reference whose conditions must then be checked.
IRCoT provides experimental support for the latter dependency pattern. Adaptive-RAG shows
one approach to varying retrieval effort. Neither establishes that every question needs an
iterative model planner. [IRCoT](https://aclanthology.org/2023.acl-long.557/),
[Adaptive-RAG](https://aclanthology.org/2024.naacl-long.389/)

Our proposed combination is an explicit initial checklist plus bounded recovery for unresolved
needs. This is a synthesis to test, not a universally established best practice.

### Coverage is more demanding than relevance

A highly relevant paragraph about MFA can still fail to explain the account's sign-ins.
The distinction between relevance and sufficiency is supported by Google's work. For this
application we also need to ask whether evidence applies to the right entity, period and
source authority. Those are domain requirements, not properties implied by a similarity score.
[Sufficient context](https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/)

Offline evaluation can use known gold passages to measure whether all required evidence was
retrieved. At runtime, that answer key is unavailable. A coverage checker can record what it
thinks is supported, identify explicit gaps and flag conflicts. It cannot prove that neither
the plan nor the corpus omitted a relevant fact. We should measure its false assurances as
well as its useful recovery requests. This is our evaluation proposal.

## Proposed design within the application's boundaries

These are proposed behaviors, not new acceptance criteria. The approved
[spec, T05 tool/playbook section](../spec.md#the-agent-its-tools-and-its-playbook-t05)
and [T26](../issues/26-investigate-alert-package.md) remain authoritative.

| Part | Proposed responsibility |
| --- | --- |
| Evidence checklist | Code derives required investigation sections and query inputs from the finding record. The model does not decide whether mandatory sections exist. |
| Focused retrieval | Separate the evidence needs. Use graph functions for relationships and corpus search for documentary context. Preserve both clearing and aggravating evidence. |
| Independent broad route | Test a broad finding-derived query alongside focused routes. For direct free-form `search_corpus`, test retaining the original question. T26 must not receive raw chat to build its internal searches. |
| Coverage record | Record which need each passage supports, its source/version and applicability. Distinguish no retrieved support, conflicting evidence, source failure and budget exhaustion. These are diagnostic concepts, not replacements for existing verdict enums. |
| Recovery | Retry a specific unresolved need with alternative wording or a suitable authorized source. Broader retrieval means broader topical wording, not relaxed access controls or silently changed identity/time scope. |
| Stop | Code enforces a finite plan, retry limit and resource budget. Stop with a visible gap when no permitted useful action remains or the budget is spent. Do not translate a failed search into proof of absence. |

This preserves [P-01 and P-02](../../../PRINCIPLES.md): code assembles facts and enforces required
steps; the model weighs the evidence; the analyst decides. A document that describes a possible
exception must not become proof that an exception caused these sign-ins.

The scope distinction matters:

- A deterministic, finding-derived query plan is compatible with T26's chosen ownership.
  The exact recovery, merging and stopping policy still needs a concrete design and review.
- A model that decides the investigation's evidence needs or generates its internal queries
  changes the present T05/T26 arrangement. That is a proposal for the author, even if code
  subsequently validates the plan.
- Improving direct `search_corpus` and designing T26 are related but separate. A successful
  T26 package does not automatically repair K04's existing direct retrieval gate.

### Failure modes the safety net must include

These are risks to test locally, not measured failure rates:

| Risk | Proposed protection or test |
| --- | --- |
| Omitted need | Preserve an independent broad route; test compound questions whose required evidence is easy to omit. An internal checklist cannot certify its own completeness. |
| False premise | Prefer neutral searches such as why MFA was not required over assuming an approved exception exists. Include questions where the expected exception does not exist. |
| Query drift | Retain the original intent and source scope in the trace. Reject changes to account identity or investigation boundaries that are not explicitly justified. |
| Evidence crowding | Deduplicate candidates and evaluate whether repeated queries about one topic push another required passage out of the final budget. Test route weighting or per-need allocation before adopting either. |
| Conflicting or stale evidence | Keep source versions and applicability visible. Search hits from different periods must not be silently combined into one current fact. |
| Mistaken sufficiency | Measure false positive coverage judgments and unsupported answers. Similarity, reranker scores and the coverage judgment are different signals. |
| Endless recovery | Enforce limits outside the model and record the actual stopping reason. An insufficient result must not authorize unlimited searches. |

### Production scale means bounded work and inspectable results

Our proposed resource contract should cover total query count, retries, candidates examined,
final context tokens, elapsed time and model cost. Concurrency needs its own cap because
parallel searches can reduce latency while still increasing load. Source permissions and
entity boundaries must apply on every route. Cached results, if later introduced, must retain
the same authorization and source-version boundaries. These are proposed engineering controls,
not features demonstrated by the K04 probe.

Record the planned needs, actual queries, candidate provenance, deduplication, final selections,
unresolved needs and stopping reason. This is an observable decision record, not a request to
store private model reasoning. Azure's documented bounded retry and activity log provide one
concrete example of this pattern. Its chosen retry count is not an application default.
[Azure retrieval effort](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort)

## Next experiments before deciding the build

1. **Freeze the current baseline and gold.** K04 remains a diagnostic case, not a newly held-out
   success. Preserve the existing requirement that both gold passages reach the fused top 20
   and that other questions do not regress. [AUD-062](../../../docs/audit/improvement-register.md#aud-062-compound-retrieval-question-loses-the-mfa-exception-register)
2. Compare the full-question baseline with fixed focused queries, then focused queries plus an
   independent broad route, then bounded recovery. Add a model-proposed plan only after a scope
   ruling. This separates the contribution of each mechanism.
3. Keep the final candidate and model-context budgets fixed when comparing coverage. Also run
   a comparison with matched total retrieval work. More queries can improve final-top-20 recall
   while consuming more total candidates, tokens and latency. Report that tradeoff explicitly.
   IRCoT's matched passage comparison is a precedent for budget-aware evaluation, not a reason
   to adopt its numerical budget. [IRCoT paper](https://aclanthology.org/2023.acl-long.557.pdf)
4. Add held-out compound, ambiguous, absent-evidence, false-premise and wrong-period cases.
   Include a trap where the proposed checklist omits a required need, and one where relevant
   passages exist but do not answer the question. Keep these separate from K04 tuning.
5. Measure all-required-evidence recall before reranking and in the model-visible context.
   Measure unsupported assertions, citations, correct handling of gaps, query count, latency,
   tokens and cost. Count retrieval errors separately from answer errors and source outages.
6. Evaluate any runtime sufficiency checker against human-labelled needs. Test whether it
   catches omissions and whether its recovery actually adds useful evidence. Do not borrow a
   universal similarity threshold. T39's calibration remains separate; this note does not
   enable the currently disabled `none` rule.

The unresolved design choices are the breadth of the deterministic checklist, the independent
broad route's allocation, the recovery triggers, and the total resource budget. Research
supports testing this bounded workflow. It does not yet establish which version passes our
retrieval gate or justify closing AUD-062.
