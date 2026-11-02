# T52: Patterns for a bounded login investigation

Date: 2 November 2026. Researcher: Codex, Astra.
Scope: small primary-source comparison for objective 1. No integration, new data source,
agent framework, autonomy or evaluation-policy change is approved by this note.

## Finding

The useful common pattern is a case built from bounded evidence, followed by an assessment
the analyst can inspect. Existing products provide implementation ideas, but their access to
endpoint, identity and cloud telemetry cannot be assumed for this app. Objective 1 can remain
a substantial standalone investigation capability without becoming a general incident-response
system. That is this review's assessment, not a measured result for Login Investigator.

## Evidence inspected

Web discovery and direct primary-page inspection were used. Perplexity was unavailable in this
child's tools, so the parent completed Perplexity discovery and independently located the same
Microsoft paper and Defender documentation. This note inspects the paper's linked v1, not v2
returned by the parent's discovery. No product tenant was connected and no vendor implementation
was executed. Six primary pages were read:

| Source | What the source establishes | Evidence limit |
|---|---|---|
| [Sentinel data exploration tools](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-data-exploration-tool) | User analysis takes explicit start/end times, has a seven-day maximum, and requires identity plus authentication, alert and cloud-activity tables. | This is a service contract. It does not disclose its reasoning implementation or establish sufficiency of login data alone. |
| [Defender agent deployment documentation](https://learn.microsoft.com/en-us/defender-xdr/security-copilot-agents-defender) | Security Alert Triage extends phishing triage to supported identity/cloud alerts in preview, with rationale and analyst feedback. | Product capability documentation, not an independent accuracy evaluation. Its autonomous classification is not our agreed policy. |
| [Microsoft Security Research: Dynamic Threat Detection Agent](https://arxiv.org/html/2605.20896v1) | Sections 3–5 describe structured input/output contracts, validation, bounded expansion, timeline construction and investigation tasks seeking supporting and refuting evidence. | First-party architecture paper. Broad incident telemetry and autonomous detection differ from our bounded login objective. Its reported results do not transfer to our app. |
| [Google SecOps Triage and Investigation Agent](https://docs.cloud.google.com/chronicle/docs/secops/triage-investigation-agent) | Documents staged enrichment, entity-context analysis, adaptive searches, visible investigation steps and suggested follow-up evidence. | Product workflow documentation. Its process reconstruction needs endpoint data. Automated verdicts and early benign closure differ from our analyst-owned verdict. |
| [Elastic: identify, investigate and document threats](https://www.elastic.co/docs/solutions/security/ai/identify-investigate-document-threats) | Documents filtering related alerts by entity/time, passing discoveries into a follow-up conversation and attaching summaries with associated alerts to a case. | An analyst workflow, not a disclosed autonomous investigation algorithm or proof of claim support. |
| [Microsoft: randomized trials for Phishing Triage Agent](https://arxiv.org/html/2511.13860v1) | Studies analyst productivity and accuracy against expert-reviewed ground truth. Its behavioural results also examine agreement with incorrect agent suggestions. | First-party phishing study with a specific corpus/protocol and counterfactual analyses. It provides evaluation ideas, not login-investigation benchmarks. |

## Five transferable patterns

The following are local recommendations derived from the comparison. They are not descriptions
of existing Login Investigator behaviour or additional author-approved requirements.

1. **Make the investigation boundary part of the evidence.** Sentinel's explicit window and
   Elastic's entity/time filtering support making scope visible. For this app, record the
   triggering finding, subject accounts/devices, requested interval, actual available interval
   and any truncation. Keep the author's 24-hour-before/after default and analyst-approved
   expansion. Neither source validates that exact default. Test events at both boundaries and
   ensure missing future records are reported as unavailable rather than as no later activity.

2. **Gather a stable case file before interpreting it.** Microsoft's architecture separates
   evidence construction from subsequent reasoning over a fixed timeline. For this app, code
   should assemble the triggering records, related login sequence and selected graph context,
   preserving record identities and source timestamps. The model explains that material.
   Each displayed fact should remain traceable after saving/reopening the case. Sensitive
   access is potential consequence; it must not become a claim that the resource was accessed.

3. **Test an explanation against competing evidence.** Microsoft's planner tasks explicitly
   ask what supports or weakens an interpretation. For this app, seek documents that aggravate
   and explain away the observed login, and check applicability to its account, device and time.
   A travel approval can explain geography without explaining every event in the sequence.
   Evaluation should include a plausible but inapplicable clearing document, contradictory
   evidence and a correct unresolved assessment. This does not require adopting a planner agent
   or changing the agreed fixed playbook.

4. **Make incomplete evidence an investigation result.** Google's suggested next steps are a
   useful presentation pattern. For this app, distinguish a successful query with no matches,
   unavailable data, tool failure and omitted results. Explain what missing evidence would
   discriminate between explanations. Propose additional history with a reason and await the
   analyst's decision. A source address or shared device is an investigative connection, not
   proof of common control or compromise. Existing login records cannot establish endpoint
   execution or resource access that they never recorded.

5. **Evaluate the analyst decision, not just fluent output.** The phishing trial's separation
   of productivity, correctness and analyst behaviour is useful. For this app, proposed checks
   should cover correct factual assembly, critical evidence retained in the package, supported
   assessment, competing explanation coverage and honest uncertainty. Include misleading
   premises and cases where the safest supported answer remains unresolved. A valid citation
   identifier alone does not show that its passage supports the claim. No new score, threshold
   or authoritative judge is selected here; these need T52 rulings and later measured proof.

## Scope implications and limits

- Treat these as improvements to one bounded investigation contract. Do not add tools merely
  because a vendor exposes them. This research gives no basis for adding endpoint telemetry,
  autonomous response, dynamic table discovery or a multi-agent architecture now.
- The selected sources do not establish a universal login-investigation time window, privileged
  access taxonomy, evidence-completeness guarantee or calibrated confidence score.
- Account role, privilege and sensitivity must come from explicit evidence. If the current
  schema lacks a field, the model cannot reconstruct it safely from a suggestive name. The
  parent review is inspecting local schema and implementation separately.
- Keeping objective 1 as the sole phase goal is still a scope decision. Existing blast-radius
  requirements must be reconciled explicitly before they can be deferred.
- Suggested ownership for review: T26 for the evidence package and coverage; T28 for execution
  and expansion control; T45 for competing document retrieval; T29/T40/T42 for measured proof.
  Confirm actual ticket fit before editing requirements. T52 remains open.

## Recommended next step

Map each agreed objective 1 outcome to existing data and functions, then label it usable,
needs adaptation, or unsupported by present evidence. Resolve missing role/privilege semantics
before estimating implementation scope. No additional vendor survey is needed for that step.
