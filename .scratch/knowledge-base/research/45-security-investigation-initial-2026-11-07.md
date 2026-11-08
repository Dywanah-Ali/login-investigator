# T45: initial research on retrieval for security investigations

Date: 7 November 2026. Initial research complete; design rulings remain open.
Tier 3 decision research. Perplexity discovery, followed by direct primary-source checks.

## Main finding

**Prior-decision reconciliation, 7 November 2026:** the author correctly challenged the
subsequent briefing's presentation of these practices as new proposals. T52 already approved
E01/E03/E06–E10 and reconciled them into downstream tickets on 2 November. Supporting and
competing evidence, person/time/activity applicability, preservation through ranking/caps,
distinct incomplete states, analyst-controlled expansion, provenance and separate evaluation
are inherited requirements, not approvals to seek again. P-01/P-02 already assign facts,
judgment and verdict. T54's fixed-evidence screening does not prove retrieval; T56 retains
minimal evaluation mechanisms without reopening those decisions. Research supports and
informs implementation of this baseline. Only the unresolved retrieval mechanisms below
need T45 rulings. See [T52 accepted mapping and handoffs](../issues/52-agent-objectives-and-reliability-review.md#mapping-review-e03-accepted--2-november-2026).

Design around the evidence an investigation needs, not only the documents a query ranks highly.
Security-specific work supports distinguishing evidence gathering, preservation and interpretation.
It does not settle whether our app needs one search tool, specialised internal retrievers,
multiple tools or multiple agents. Those are separate choices to discuss and test proportionately.

This is a synthesis, not an adopted architecture. Phases 0/1 remain a read-only login investigator:
code establishes facts, the model assesses them, and the analyst retains the verdict.

## Sources checked and what they establish

Primary pages were opened directly. Paper findings below are authors' reported results, not
independently reproduced results. Preprint publication is not independent validation.

| Source | Evidence and relevance | Limits for our decision |
| --- | --- | --- |
| [AIDA / ALERT-BENCH, October 2026](https://arxiv.org/html/2610.10608v1), abstract and sections V–VII | Security-alert experiments; separates successful, empty and failed retrievals and retains an investigation ledger. Its cross-scenario example shows all reasoning roles agreeing on incomplete retrieved context. | A triage protocol, not a controlled comparison of policy and threat-document retrievers. Its final classification differs from our analyst-owned verdict. |
| [CORTEX, September 2025](https://arxiv.org/html/2510.00311v1), sections 3–4 | Includes anomalous-login and authentication workflows. Reports a shared typed-tool library for the multi-agent system and single-agent tool baseline, with matched call/turn caps. | Workflow, role and synthesis changes are bundled. Same maximum budgets do not mean equal actual work. It does not isolate tool count or retrieval boundaries. |
| [DiagChain, August 2026](https://arxiv.org/abs/2608.03591), abstract | A 69-scenario attack-chain benchmark explicitly separates intermediate failures from final accuracy. Reports that even its strongest configuration reconstructs only 39.6% of 849 reference steps. | Attack-chain reconstruction is broader than our login task. Identity, date, task and headline denominator checked; detailed scorer and artifacts not audited in this initial pass. |
| [SIR-Bench, April 2026](https://arxiv.org/html/2604.12040v1), sections 3–4 | Distinguishes alert classification from discovery of evidence beyond the original alert. Uses simulated cloud activity and expert-reviewed expected findings. | Metric/reporting inconsistencies below prevent treating headline numbers as a dependable target. This is not a reproduction or proof of performance on our data. |
| [Microsoft Security Alert Triage Agent](https://learn.microsoft.com/en-us/defender-xdr/security-alert-triage-agent), overview | First-party description of supported identity/cloud triage and visible evidence/rationale; expanded capabilities are labelled preview. | Product capability description, not independent accuracy evidence. Autonomous verdicts and incident actions are outside our scope. |
| [Microsoft identity-risk investigation](https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk), investigation framework | Directly relevant sign-in guidance: examine history, device, location, application and related alerts; investigate legitimate explanations. | Entra has telemetry our synthetic app may lack. Remediation instructions are excluded. VPN guidance does not reverse our decision to remove address-sharing peers. |
| [Microsoft MFA event interpretation](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-reporting), interpretation note | A sign-in's apparent single-factor status can coexist with a previously satisfied MFA claim; detailed authentication context matters. | Do not import Entra semantics into our synthetic fields. This illustrates why evidence must match the system and event being investigated. |
| [NIST SP 800-61r3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf), printed pp. 25–29 | DE.AE-03/07/08 cover source correlation, threat/context integration and false positives. RS.AN-03/06/07 address event analysis and provenance. | Normative investigation guidance, not a retriever prescription, agent benchmark or approval to ingest the document. |

### Findings that limit strong architecture claims

AIDA's full-text ablation reports no statistically isolated contribution from its adversary
role on the 300-alert subset: relevant intervals include zero. Its wardbeck example misses
an attack because retrieval returns too little context despite agreement among roles.
The lesson is to examine evidence sufficiency; the paper does not justify copying its team.
[AIDA sections VI-C/D](https://arxiv.org/html/2610.10608v1).

CORTEX reports actionable F1 increasing from 0.66 to 0.78, but median latency rises from
44.6 to 152.4 seconds, with more actual calls and tokens. This is a bundled workflow result,
not proof that separate subject tools are better. Exact model identity and a reproducible
dataset split were not established by the inspected experimental summary.
[CORTEX tables 4–5](https://arxiv.org/html/2510.00311v1).

SIR-Bench's abstract describes an adversarial model judge, whereas section 4.2 describes
ROUGE-L finding matching. Table 6 reports overall 5+ finding frequency greater than 3+
frequency, which cannot hold for the same population under those definitions. Its reported
97.1% detection and 41.9% novel-finding coverage illustrate different measures, but are
not accepted as reliable comparative targets without resolving reporting details.
[SIR-Bench abstract and section 4](https://arxiv.org/html/2604.12040v1).

Google's investigation-agent page was a Perplexity discovery lead. Its detailed workflow was
not independently verified in this pass and is not used to support the conclusions.

## What this means for our mixed policy/threat question

Example: does suspicious login activity fit an attack, and could an approved MFA exception
explain it? The following is our proposed reasoning frame, not a new implementation contract.

| Need | Evidence to seek | Mistake to avoid |
| --- | --- | --- |
| Establish activity | Login facts and bounded account/device context | Letting a policy passage substitute for event evidence |
| Explain suspicious features | Applicable threat guidance | Treating a known technique as proof that it happened |
| Check a competing explanation | Relevant policy plus the actual exception record | Treating a general policy as proof this account had an exception |
| Check applicability | Person, date, system and activity covered | Letting an exception explain unrelated failed-login activity |
| Preserve uncertainty | Missing, failed or out-of-scope checks | Treating an empty search as proof of innocence |

Our existing K04 evidence already shows two distinct problems: broad retrieval misses a
required register, and merging/capping can discard it after focused retrieval finds it.
Human-selected focused queries demonstrate recoverability, not autonomous need discovery.
See [AUD-062](../../../docs/audit/improvement-register.md#aud-062-compound-retrieval-question-loses-the-mfa-exception-register)
and the [local experiment](22-retrieval-experiment-results.md).

## Implications for T45's decisions

1. **Gate paths:** keep ordinary chat and protected code-built investigation searches visible
   as different paths. No original question, expected evidence or threshold is waived.
2. **Chat planning:** decide whether the model or a shared component identifies separate
   evidence needs. Published security-agent results do not establish the right choice here.
3. **Package searches:** define which supporting and competing evidence each investigation
   step needs. Keep searches built from finding facts, not untrusted chat instructions.
4. **Preservation:** distinguish evidence found, retained and actually given to the model.
   A relevant top-five list is not itself a coverage guarantee.
5. **Keyword strategy:** the research does not settle all-terms matching versus BM25. Keep
   T41 ownership and the existing retrieval gate intact.
6. **Boundaries:** separate the decision about internal search methods from the decision
   about the tools the agent sees. One shared interface can contain different methods;
   multiple interfaces add routing choices that need evidence to justify them.

Future expansion strengthens the case for clear responsibilities and inspectable evidence.
It does not justify building an autonomous SOC, extra agent roles or future data sources now.

## Proposed next discussion

Start from T52's approved evidence and uncertainty requirements; do not repeat their approval.
Use the mixed question to compare three options: model-directed focused calls
to the shared tool; one shared tool with internal planning/routing; separate subject tools.
Do not choose by name or diagram. Examine coverage, misrouting, lost evidence, applicability
and inspectability using existing local evidence first. Any new experiment needs its bounded
purpose agreed; this report does not authorise a comparison run.

Guidance-source selection remains open. Existing approved corpus passages should be mapped
to E06 uncertainties before proposing additions. Reading a source here does not approve ingestion.

## Provenance, checks and limits

- [Research brief](45-security-investigation-brief-2026-11-07.md).
- [Successful Perplexity output](45-security-investigation-initial-2026-11-07-perplexity-corrected-raw.md).
- [Discovery draft](45-security-investigation-initial-2026-11-07-draft.md) preserves unverified
  leads; this note supersedes its verification-pending status for the claims checked above.
- [Failed-call/retry record](45-security-investigation-initial-2026-11-07-perplexity-raw.md).
  Initial network failure and an assistant malformed retry delayed research; the corrected
  request returned the report. Stopping a local request does not establish remote billing.
- Keenable is unavailable. Perplexity preference was honoured; the legacy criterion naming
  both engines is not fully satisfied. This initial pass does not close T45.
- Direct source inspection establishes what sources report, not that their systems work as
  claimed. No benchmarks reproduced, application tests run or model comparisons executed.
- T45 now blocks T25 by author approval. No retrieval architecture has been adopted.
