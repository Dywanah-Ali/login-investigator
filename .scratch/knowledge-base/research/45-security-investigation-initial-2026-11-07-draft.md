# T45: initial defensive security-investigation retrieval research

Date: 2026-11-07. Status: Perplexity discovery complete; selected claims await parent verification. No architecture adopted. No implementation, ingestion, gold change, threshold change, application tests or paid model-comparison calls.

## Scope and evidence provenance

The question is reliable read-only login investigation in phases 0/1. Combine authentication activity, bounded account-impact and involved-device context, applicable threat guidance and internal exceptions. Preserve competing explanations and uncertainty. The analyst retains the verdict. Full asset inventory, reverse exposure and response automation remain out of scope.

Read locally: `PRINCIPLES.md`, T45, current initiative map, relevant AUD-062/AUD-064 entries, T52 evidence mappings and the spec's uncertainty section. P-01 assigns facts to code, judgment to the model and verdict to the analyst. P-02 prohibits categorical compromise verdicts. P-03 prohibits designing around one weak model's limits.

The requested engine is `mcp__perplexity__perplexity_research`. Its first call failed while streaming without returning sources. A malformed retry was stopped; a corrected concise request then returned a report. Raw results and operational limitations are recorded in the adjacent Perplexity raw files. Keenable is absent from the available tool inventory. The ticket's combined Perplexity/Keenable research criterion is therefore not fully satisfied by this pass. The author-confirmed model gate was supplied by the parent; this worker did not alter the ticket to record it because writes were restricted to these research files.

## Eight-source discovery shortlist

All eight entries below are attributed to the returned Perplexity report. This worker has not independently opened these primary pages. Titles, dates, methods and quantitative claims remain discovery leads until the parent verifies them. The raw report's much larger trailing bibliography is not an endorsed source set. Publication dates are not independently established; arXiv identifiers are not used as a substitute for verified publication metadata.

| Source | Evidence class reported by Perplexity | Relevant reported finding | Transfer limit and parent verification target |
| --- | --- | --- | --- |
| [Alert-Bench / AIDA](https://arxiv.org/abs/2610.10608) | Measured study, preprint | Replayed security alerts expose missed attacks and empty-retrieval dismissal; AIDA reportedly improves attack detection. | Verify paper identity, dataset, baseline fairness and attack-phase concentration. Alert triage is not proof of complete login evidence retrieval. |
| [CORTEX](https://arxiv.org/abs/2510.00311) | Measured study, preprint | Workflow-routed agents reportedly improve actionable F1 relative to a tool-using single agent, with latency cost and a shared tool library. | Verify identity and experimental controls. A bundled workflow comparison does not isolate document retrievers or agent-facing tool count. |
| [DiagChain](https://arxiv.org/abs/2608.03591) | Measured benchmark, preprint | Reportedly separates discovery from grouping, ordering, grounding and attribution in reconstructed attack chains. | Verify title, task, sample and metric denominator. Chain reconstruction differs from bounded login investigation. |
| [SIR-Bench](https://arxiv.org/abs/2604.12040) | Measured benchmark, preprint | Reportedly distinguishes incident detection from discovery of expected new findings in simulated AWS/CloudTrail investigations. | Verify identity, synthetic scenarios, scoring and denominator. Correct incident detection does not establish evidence completeness. |
| [Microsoft Security Alert Triage Agent](https://learn.microsoft.com/en-us/defender-xdr/security-alert-triage-agent) | First-party vendor product description | Describes contextual identity-alert triage and inspectable reasoning. | Verify supported alerts, preview status and permissions. Reported alert resolution/management actions are outside this read-only investigator. Product claims are not independent accuracy measurements. |
| [Google Triage and Investigation Agent](https://docs.cloud.google.com/chronicle/docs/secops/triage-investigation-agent) | First-party vendor product description | Describes iterative searching, threat-intelligence/context gathering and an investigation timeline. | Verify actual workflow and evidence visibility. This demonstrates a product design, not superiority over the local shared-tool baseline. |
| [Microsoft identity-risk investigation](https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk) | First-party operational guidance | Suggests investigating sign-in history, device, location/IP and legitimate explanations such as travel or VPN context. | Verify exact passage and applicability. Real Entra telemetry exceeds the synthetic application's available fields; remediation steps remain excluded. |
| [Microsoft MFA sign-in details](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-reporting) | First-party technical guidance | Explains authentication details, policy results and reused MFA claims; initial details may be incomplete. | Verify precise field semantics. Do not assume the local MFA field has Entra's semantics. Useful as an applicability warning, not authority to reinterpret local facts. |

### Quantitative claims quarantined for verification

These numbers are reproduced solely to tell the parent what to check. They are not accepted findings and must not be used to justify architecture or an acceptance threshold before verification.

- Alert-Bench/AIDA: Perplexity reports 1,247 replayed alerts, five baselines missing at least 40.4% of attack-related alerts, and AIDA missing 3.1%. Verify denominators, attack distribution and dataset dependence. [Candidate paper](https://arxiv.org/abs/2610.10608).
- CORTEX: Perplexity reports actionable F1 of 0.66 versus 0.78, greater latency and the same tool library. Verify configuration, models, budgets and whether the comparator is actually controlled. [Candidate paper](https://arxiv.org/abs/2510.00311).
- DiagChain: Perplexity reports 69 reconstructed cases and 39.6% of reference steps reconstructed by its strongest configuration. Verify metric definition and whether this is recall, exact reconstruction or another measure. [Candidate paper](https://arxiv.org/abs/2608.03591).
- SIR-Bench: Perplexity reports 97.1% incident detection but 41.9% coverage of expected novel findings for true positives. Verify task, scorer, denominators and model setup. [Candidate paper](https://arxiv.org/abs/2604.12040).

No discovered source, as represented in this report, supplies a controlled answer to shared versus subject-specific retrieval behind an otherwise identical tool interface. Neither specialized agents nor a shared tool library settle that question.

### Synthesis of the discovery, pending verification

The useful distinction is between finding evidence, retaining it and using it correctly. Perplexity's descriptions of DiagChain and SIR-Bench offer potentially relevant security-specific evaluation examples; the local K04 diagnostics already establish why this distinction matters here. The vendor pages offer workflow examples for iterative investigation and inspectable evidence. They do not establish that this app needs autonomous triage, multiple agents or separate subject tools. The identity/MFA guidance may help frame applicability checks, but internal exception records must still establish the actual person's applicable exception. A general threat or authentication passage cannot establish that an event occurred.

The report proposes coverage-aware selection and a controlled comparison of internal retrieval boundaries and tool interfaces. Those are proposed designs, not measured findings from the cited papers. Its suggested hard five-passage final pack is not adopted as a new universal package rule; the parent reports a current default reranked five, and exact budget policy remains a T45 decision. Likewise, its suggestion to return insufficient evidence on exhaustion should preserve known supported findings alongside gaps; a missing peripheral fact must not erase valid evidence or force a categorical verdict.

## Verified guidance supplied by the parent

NIST SP 800-61r3 supports correlating sources (DE.AE-03), integrating threat intelligence and context (DE.AE-07), and considering false positives (DE.AE-08), printed pages 25–26. Its incident-analysis guidance addresses establishing what occurred (RS.AN-03) and preserving investigation records and evidence provenance (RS.AN-06/07), printed pages 28–29. This is normative incident-response guidance, not an agent benchmark or a mandate for multiagent architecture. Verification was performed by the parent and supplied in this session; this worker did not duplicate it. [NIST SP 800-61r3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf).

Local implication, proposed rather than adopted: evaluate whether each material explanation has supporting and competing evidence, with recoverable provenance. The guidance does not choose a retriever, decomposition method, tool count or top-k value.

## Local failure that the research must explain

AUD-062 records that K04 needs a runbook and MFA exception register. The compound all-terms keyword search produces no candidates; the register sits at dense rank 115. Human-written focused queries recover it at rank 7 or 2. Those probes establish recoverability, not automatic decomposition quality. Equal cross-query fusion can push an already retrieved register to rank 25. Fair route allocation fails in two of six tested route orders, and the five-passage stress cap can discard the required passage. T23 reranking promotes the runbook but never scores the missing register. Source: local T45 and AUD-062.

The parent reports current code uses one search query, fused 20 candidates and a default reranked five. A nonempty verdict remains weak/not_calibrated pending T39. This is parent-reported code inspection, not an independent runtime measurement by this worker. AUD-064 separately records why relevance scores require calibration.

**Ranking and coverage are different questions.** Ranking asks which available result is more relevant. Coverage asks whether every material evidence need is represented. A well-ranked runbook cannot replace a missing exception. A nonempty result cannot establish sufficient evidence, nor can a relevance score establish confidence that an account was compromised.

## Candidate investigation needs mapped to the approved scope

These are synthesis proposals for review, not adopted retrieval templates.

| Evidence need | Proposed question | Boundary or failure to preserve |
| --- | --- | --- |
| E01 activity | What failed and succeeded, for which accounts, sources and devices, in the approved window? | Code computes counts, joins and sequence. Clipped or missing time coverage remains explicit. |
| E02 significance | What relevant role, privilege and sensitive-access context is actually recorded? | Structured account lookup is distinct from document retrieval. Role is not proof of normal behaviour. |
| E03 competing evidence | Which records support suspicious activity, and which explain some or all of it? | Travel can explain location without explaining a separate spray. An MFA exception may explain policy applicability without proving a login benign. |
| E04 bounded impact | What potential account impact and involved-device context matter to this login investigation? | Permission is potential impact, not observed resource access or event-time permission proof. No full inventory. |
| E05 connected activity | What directly connected activity is evidenced? | Do not expand to independent spread investigation or claim unseen activity did not occur. |
| E06 uncertainty | What remains unresolved, why, and which case-specific analyst check could resolve it? | Distinguish empty, unavailable, failed and omitted evidence. A recommended external check has not been performed. |

## Six open T45 decisions

| Decision | Evidence needed for a ruling | Status in this initial pass |
| --- | --- | --- |
| Gate paths | Separate raw analyst-question retrieval and protected code-built package searches; retain original K04 gold and fused-20 obligation. | No gate change proposed as a ruling. |
| Chat decomposition | Does automatic splitting find required needs without human knowledge of gold, omit fewer needs and preserve scope? | Human-focused probes do not answer this. |
| Package coverage | Can searches built from finding records cover relevant supporting and competing evidence for each approved step? | Untrusted chat must not steer protected package searches. |
| Evidence preservation | Track candidates, reranked results, retained results and actual model-visible evidence separately. | A retrieval success can become a merge/cap failure. |
| Keyword strategy | Compare the relevant lexical alternatives on the unchanged compound questions and regression set. | Security-agent descriptions alone cannot settle AND versus BM25. T41 owns its comparison. |
| Retrieval boundaries | Compare shared baseline with subject-specific internals, then separately assess the agent-facing interface. | A shared tool can dispatch internally. Separate tools add routing choices; neither shape establishes access control. |

## Evaluation proposals, not new acceptance gates

- Keep retrieval, assembly and interpretation checks distinct. Supplying ideal evidence to a model tests interpretation, not live retrieval.
- Record evidence-need coverage at candidate, reranked, retained and model-visible stages. Attribute missing evidence to the stage that lost it.
- Use cross-subject cases requiring both ATT&CK guidance and an applicable internal exception. Include single-subject controls and wrong-subject routing.
- Test expired exceptions, wrong-person exceptions, partial travel explanations, contradictory documents, unavailable logs and failed lookups. Separate no matching record from a failed or omitted search.
- Preserve exact code-built activity facts and test whether the model contradicts them. Judge applicability and hedged assessment separately from counting.
- Compare alternatives under matched search/result/context budgets. Record route order and cap effects. Do not credit more calls or a larger context as a demonstrated architecture advantage.
- For bounded stopping, distinguish resolved needs from unresolved needs at a budget limit. Preserve gaps and relevant analyst checks instead of forcing a verdict. An exact retry budget remains undecided.
- Include untrusted instructions inside logs and documents. Tool names and subject filters are not backend authorization boundaries.

## Existing corpus before new guidance

The file inventory already includes ATT&CK T1078, T1110 and T1110.003; password-spray, new-country and compromised-account runbooks; MFA policy and exception register; approved travel; and shared-device records. This worker inspected their presence, not their full content or adequacy. First map existing approved passages to E06 uncertainties. External sources below are candidates for review, not approved ingestion. Response-oriented documents require passage-level scope checks before recommending read-only investigation guidance.

## Limitations and parent handoff

The eight-source external shortlist is discovery only. NIST is the only external guidance with primary verification supplied in this worker's context. The raw Perplexity report contains many secondary and tangential URLs beyond the selected eight; they are preserved for provenance, not promoted as evidence. Local design proposals are not measured findings. All six decisions remain open. Parent will verify selected source identities, claims, dates, samples, comparators and applicability before integration. If any paper URL or reported metric does not match its claim, exclude the claim rather than repairing it by inference.

Verification priority: first confirm the four paper identities and the reported task/metric definitions; then verify CORTEX's shared-tool comparator and the detection-versus-discovery distinction in SIR-Bench/DiagChain. Verify one vendor workflow only to substantiate a concrete capability claim, and the identity guidance for case-specific E06 applicability. Do not duplicate the parent's completed NIST check. No paid experiment or application test is needed for this discovery artifact.

Artifacts: `45-security-investigation-initial-2026-11-07-perplexity-raw.md` records the failed first call and malformed retry. `45-security-investigation-initial-2026-11-07-perplexity-corrected-raw.md` preserves the successful complete tool response, including its response text, citation tokens and URL bibliography. This draft separates those engine claims from local evidence and parent-verified guidance.
