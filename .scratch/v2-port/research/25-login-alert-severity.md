# Research: severity for the existing four login alerts

Researched 18 October 2026. Decision support only. No application, API contract, spec, detection threshold, or report policy changed. The author must approve any future implementation. This is an enhancement after Parity.

## Recommendation

Use a fixed, documented **default severity for each rule** first. Define it as the urgency of reviewing this suspicious pattern. It is not a calculated probability of compromise, confirmed incident impact, or a verdict that an account was taken over.

| Existing rule | Proposed default | Explanation shown to the analyst |
| --- | --- | --- |
| Brute force | Medium | Repeated failures on one account need review. This finding alone does not establish whether related sign-ins succeeded. |
| Password spraying | Medium | Failures across many accounts suggest an attempt against several accounts. The log cannot verify that the same password was tried. |
| Success after repeated failures | High | A successful sign-in follows many failures on the same account and IP address. Check urgently whether it was authorized. |
| Sign-in from a new country | Low | An unfamiliar country is a useful lead. Travel, network routing, or an incomplete history may explain it. |

These exact ratings are our recommendation for this project's available evidence. No source below prescribes them as universal ratings. Low still requires review. High does not mean confirmed compromise. The three-level scheme need not populate all three levels equally.

### How Perplexity informed the recommendation

Exactly one authorized paid `perplexity_research` call completed successfully. No additional paid calls were made. It received only generic rule descriptions and evidence limitations. Its main factual claims were checked against the primary sources linked below; its generated narrative is not treated as an authority.

Perplexity also recommended fixed defaults, but proposed Low for brute force, Medium for spraying, High for success after failures, and Medium for new country. This disagreement concerns policy judgments, not conflicting source facts. Low for repeated failures prioritizes observed effect; Medium for a new-country success prioritizes the presence of a successful authentication. Our alternative gives concentrated suspected attack behavior Medium and a standalone, weakly contextualized country anomaly Low. Both need an explicit project policy. No official universal mapping resolves the choice.

Perplexity proposed replacing the report prompt and aggregating incident severity from the highest alert. Those proposals are not adopted. They would change current report behavior and need separate author approval after Parity. An Investigation can include evidence beyond its table findings, so maximum default severity cannot automatically substitute for its assessment.

## Scope and local evidence

`Finding` and screen/API `Alert` are the same object, as defined in [GLOSSARY.md](../../../GLOSSARY.md). The current Alerts table has no severity. The rule filter needs only the existing four categories and an All rules option. It does not require an attack catalog or more detections.

The local source is [rules.py](../../../backend/login_investigator/rules.py). The existing rules are:

| Rule | Existing condition | Important limitation |
| --- | --- | --- |
| `brute_force` | At least 20 failures on one account from one IP within 60 minutes | Its finding contains failed rows only. |
| `password_spraying` | One IP fails against at least 10 accounts within 60 minutes | Its finding contains failed rows only. Neither passwords nor password equality are logged. |
| `success_after_failures` | A success follows at least 10 failures from the same IP on the same account within the previous 60 minutes | The success is observed. The identity and intent of the person using the account are not. |
| `new_country` | A successful sign-in from an unseen country after at least five earlier successful sign-ins | Five events establish only this dataset's baseline, not a validated production learning period. |

The log provides timestamps, account names, source IPs, country, outcome, failure reason, and user agent. It lacks multifactor authentication outcomes, account privileges, asset importance, device trust, and activity after sign-in. Existing saved IP reputation can inform an Investigation but is not part of these four rule triggers or a calibrated severity policy.

For the first two rules, `success_count == 0` means no successful rows were included in that finding. It does **not** mean no related successful sign-in occurred elsewhere. The same activity can trigger several findings. Counts are findings, not separate confirmed attacks.

## What the primary sources establish

### Severity, risk, confidence, and confirmation answer different questions

Microsoft Sentinel describes severity in terms of potential effect and response urgency. It supports rule defaults and overrides based on query results, and warns that defaults do not guarantee actual environmental impact. That supports either fixed or contextual approaches, but does not prescribe our four ratings. [Microsoft Sentinel analytics rule guidance](https://learn.microsoft.com/en-us/azure/sentinel/isv/sentinel-analytic-rules-creation).

Sentinel's alert schema separately represents severity and confidence. Confidence describes how sure the provider is that an alert is not a false positive. We should not present an invented percentage or call a severity badge a confidence score. [Microsoft Sentinel security alert schema](https://learn.microsoft.com/en-us/azure/sentinel/security-alert-schema).

Microsoft Entra sign-in risk expresses the likelihood that the request was not made by the account owner. Its levels can vary with evidence and confidence. The same unfamiliar-properties detection can have different risk levels. These are product-specific risk assessments, not portable severity assignments for our rule names. [Entra risk detection types and levels](https://learn.microsoft.com/en-us/entra/id-protection/concept-risk-detection-types).

Defender treats incident severity and incident classification as different fields. An incident gathers related alerts, and its severity can change when alerts change. This supports separating a finding's default from an Investigation report's assessment. [Defender XDR incident resource](https://learn.microsoft.com/en-us/defender-xdr/api-incident).

NIST recommends prioritizing incidents using risk evaluation factors such as asset criticality, functional and data impact, observed activity stage, threat actor characteristics, and recoverability. Our log cannot measure most of those factors. A deterministic default is more honest than claiming a comprehensive incident risk calculation. This last sentence is our inference. [NIST SP 800-61 Revision 3, April 2025, RS.MA-02 and RS.MA-03, printed pages 26–28](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf).

### Technique mappings describe behavior, not severity

| Existing rule | Defensible relationship to ATT&CK | Qualification |
| --- | --- | --- |
| Brute force | T1110.001 Password Guessing | Repeated failures are consistent with guessing. They do not establish which passwords were used or attacker intent. |
| Password spraying | T1110.003 Password Spraying | Suspected relationship only. The technique involves a small password set across many accounts; our evidence measures account fan-out. |
| Success after repeated failures | T1110.001; possible T1078 Valid Accounts if malicious use is established | Failure then success fits investigation of guessing. Successful authentication alone does not prove abuse of valid credentials. |
| New country | Possible lead for T1078 Valid Accounts | Geographic novelty is not a standalone ATT&CK attack technique or proof of account abuse. |

MITRE describes password guessing as repeated attempts to obtain credentials, spraying as trying one or a small set of common passwords across many accounts, and Valid Accounts as adversary use of existing credentials. The table's relationship and qualification judgments are ours. These technique pages supply taxonomy and detection guidance, not Low/Medium/High ratings. [T1110.001](https://attack.mitre.org/techniques/T1110/001/), [T1110.003](https://attack.mitre.org/techniques/T1110/003/), [T1078](https://attack.mitre.org/techniques/T1078/).

### Vendor detections with similar names are not equivalent

Entra's password-spray risk detection requires successful password validation. Its documentation explicitly distinguishes knowing the password from accessing resources. Unsuccessful sprays do not trigger that specific detection. Our rule is a failure-based heuristic. Importing a vendor risk label because the names match would give our finding stronger meaning than its evidence supports. [Entra risk detection definitions](https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks), [Entra risk investigation guide](https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk).

Our country rule also uses a much smaller baseline than Entra's unfamiliar-properties assessment, which considers several properties and a learning period. We are not reproducing that product's model. Legitimate explanations must remain open during review. [Entra risk detection definitions](https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks).

IP location is approximate. Microsoft warns that mobile networks and VPNs can associate a client with a distant IP pool. This supports investigating geographic novelty without treating the country as proof of physical travel or malicious use. [Entra sign-in activity details](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details).

## Why fixed defaults first

| Approach | Benefit | Limitation |
| --- | --- | --- |
| Fixed rule defaults | Predictable. Every badge has a short explanation. Easy to check across API and screen. | Does not capture account importance or linked evidence. |
| Contextual assessment for each finding | Can prioritize related success, identity importance, and corroboration when available. | Requires correlation definitions and more trustworthy context. Current data cannot support many factors. |

Recommendation: start with the first approach because it makes the promise match the evidence. Future contextual scoring must specify the exact evidence and explain every change. Do not add arbitrary points for country names, IP reputation scores, raw volume, or overlapping findings without validation. Do not lower severity because a failure-only finding has zero successes.

If approved later, the core should own one rule-to-default mapping. The API and screen consume it. A language model should not assign table badges. Name the column Severity and explain nearby that it is the rule's default review priority. Use text with color so the meaning survives color-vision differences. Proposed colors are blue for Low, amber for Medium, and red for High. Green remains appropriate for the Overview's zero-alert state, not a detected Low finding. These are design recommendations for author review, not already approved screen changes.

## Relationship to the existing report policy

The existing report prompt in [agent.py](../../../backend/login_investigator/agent.py) assesses the whole Investigation. It allows None, Low, Medium, High, and Critical. The table below compares indicative report criteria with proposed defaults, not a claim that every finding automatically determines a report rating.

| Evidence category | Existing report policy | Proposed rule default |
| --- | --- | --- |
| Brute force consistent with an active attack | High when attack with no sign-in is established | Medium |
| Suspected password spraying consistent with an active attack | High when attack with no sign-in is established | Medium |
| Success after repeated failures from an attacker IP | Critical when evidence shows an attacker signed in | High |
| A single new-country anomaly | Medium | Low |

Do not silently harmonize the report prompt during the Port. Its current behavior belongs to Parity. Also do not blindly compute report severity as the maximum table default: reports assess a different scope and can include additional evidence.

There is a real user-facing consistency decision before shipping the column. An isolated country finding could display Low while its report says Medium. Merely saying the scopes differ does not fully explain that case. Proposed future acceptance requires either:

1. Retain the current report policy and explicitly distinguish Rule default severity from Investigation severity, with a short evidence-based reason for any difference. Keep both policy meanings documented and test the isolated-anomaly example.
2. After Parity and explicit author approval, adopt a coordinated report policy. Record the behavior change, update expectations, and rerun report evaluations. Preserve the distinction between observed success and confirmed attacker access.

Prefer resolving this decision in the severity enhancement ticket before implementation. Do not promise a shared numeric scale or a Critical badge in the three-level table.

## Suggested future acceptance criteria

These are proposals only. They do not amend the spec.

1. The author approves the meaning, four defaults, visual treatment, and report consistency option.
2. Existing rule conditions, findings, evidence counts, and Parity results remain unchanged.
3. A rule filter contains All rules and the four existing categories. It composes with existing filters, resets paging, and handles an empty result clearly. Decide its API contract before coding.
4. Severity comes from one deterministic core policy. Each supported rule has exactly one default and explanation. Screen and API agree.
5. Badges include visible severity words and accessible contrast. The filter and table work by keyboard.
6. A brute-force finding with zero successes remains Medium even when another finding shows a related success. No explanation claims the attack failed based solely on that zero.
7. Overlapping findings keep their own defaults. Their count does not silently escalate severity or represent incident count.
8. The High explanation says success was observed and authorization needs checking. It does not assert confirmed compromise.
9. An isolated country finding and its report have the approved, documented treatment. The report's policy does not change without an author-approved decision and relevant evaluation evidence.
10. Targeted tests cover policy mapping, filter composition, paging, unknown rule handling, accessible labels, and these evidence limitations. No new paid model evaluation is needed for a pure table default unless the report behavior is changed.

## Future coverage, explicitly outside this change

MITRE documents distributed and deliberately slow password spraying that can avoid single-IP, short-window thresholds. That is one useful future coverage study. Credential stuffing and valid-account abuse are separate areas; neither can be confirmed merely from our current country field or generic failure counts. Additional telemetry and representative validation would be needed. This is not a recommendation to add them during Parity. [MITRE T1110.003](https://attack.mitre.org/techniques/T1110/003/), [MITRE T1078](https://attack.mitre.org/techniques/T1078/).

## Source dates and uncertainty

All linked primary sources were accessed on 18 October 2026. The dates below are the pages' displayed modification dates, not independently verified publication histories. Documentation can change.

| Source | Displayed date |
| --- | --- |
| MITRE T1110.001, version 1.7 | 12 May 2026 |
| MITRE T1110.003, version 1.8 | 24 October 2025 |
| MITRE T1078, version 3.0 | 12 May 2026 |
| Entra risk detection types and levels | 10 June 2026 |
| Entra risk detection definitions | 22 April 2026 |
| Sentinel security alert schema | 22 April 2026 |
| Sentinel analytics rule guidance | 25 June 2026 |
| Defender XDR incident resource | 7 August 2026 |
| Entra sign-in activity details | 4 March 2026 |
| NIST SP 800-61 Revision 3 | April 2025 |

This research does not validate production thresholds, measure false positives, calibrate a confidence score, or establish real business impact. `docs/adr/` was absent when checked. No course solution kits, secrets, log rows, real identities, or real IPs were used in external research prompts.


## Author decision, 18 October 2026

The author accepted the recommended Medium/Medium/High/Low defaults (P-044). Implementation
is queued in [ticket 26](../issues/26-alert-rule-filter-default-severity.md), blocked by Parity
closing in ticket 19. The existing report policy stays unchanged. Exact column explanation,
report distinction, visual treatment and API contract remain implementation prerequisites.
The preceding research narrative is retained as the record of alternatives considered.
