# T45 initial research brief: security investigation retrieval

Date: 7 November 2026. Tier 3. Decision research, not implementation.
Author authorised research through Perplexity and confirmed the selected model gate.

## Question

How should a read-only login investigator gather and preserve evidence across event records,
account/device context, threat guidance and internal policies or exceptions, while considering
competing explanations and leaving the verdict to the analyst?

## Bounded initial pass

- Use Perplexity research for discovery and initial synthesis. Check material claims against
  their primary sources. Identify unavailable or unverified evidence explicitly.
- Prioritise defensive SOC triage and investigation systems, relevant research evaluations,
  and authoritative investigation guidance. Generic customer-support retrieval and offensive
  agents are not direct evidence for this design.
- Compare shared versus specialised retrieval, model versus code query planning, preservation
  across merging/caps, applicability checks, uncertainty/stopping, and evaluation of missing
  or competing evidence. Do not assume multiple agents or tools are necessary.
- Cover both free-form analyst chat and code-built searches from an alert's facts.
- Use a concrete mixed question: does suspicious login activity match attack guidance, and
  does an approved authentication exception explain any of it? An exception cannot erase
  separate unexplained activity. General guidance cannot establish that an event occurred.
- Seek a small set of strong primary sources. Label measured results, vendor descriptions,
  proposals, and our own inferences separately. Explain differences from our synthetic,
  bounded login-investigation setting.

## Existing evidence to reuse

AUD-062 and T22/T23 show a missing MFA register in broad retrieval, recovery by human-written
focused searches, and loss after merging or a five-passage cap. These are local diagnostic
results, not proof of autonomous decomposition or coverage checking. Preserve original gates.
Read PRINCIPLES.md: code owns facts, model owns judgment, analyst owns verdict; avoid designing
around one small model. T45's six decisions and E06 guidance-source approval remain open.

## Output and limits

A cited initial research note, source-quality/applicability table, implications for T45's
decisions, unresolved questions, and a small set of options for author discussion. Save the
Perplexity response separately for provenance. No implementation, ingestion, paid model
comparison, new proof suite, or architecture adoption. Later expansion informs boundaries,
not additional phase 0/1 features. Research completion does not resolve T45.

## Local baseline checked during research

Read-only inspection of `backend/login_investigator/knowledge_base/retrieval.py` and
`reranking.py`: the core receives one query and optional metadata filters, combines semantic
and keyword candidates, sends the fused top 20 to the optional reranker, and normally retains
five after reranking. The recorded candidates retain ranking information. This is not a
cross-question coverage check. Nonempty results default to `weak` / `not_calibrated` until
the separate calibration work; an empty result is `none` / `empty_result`.

These existing mechanisms are reusable. Research must distinguish candidate discovery,
retention, applicability to the case, and whether the resulting answer is supported.

Tool availability: Perplexity research is available and explicitly requested. The legacy
T45 criterion also names Keenable, but no Keenable tool is available in this session.
Primary-source checking remains required; no Keenable execution is claimed.
