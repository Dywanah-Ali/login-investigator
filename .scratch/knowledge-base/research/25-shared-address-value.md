# Research note 25: what "other accounts on this address" is worth to an investigation

Ticket: [25-peers-and-corpus-search-tools](../issues/25-peers-and-corpus-search-tools.md), required
pre-build gate (author ruling, 1 November 2026)
Date: 1 November 2026
Method: Keenable search (about 25 queries, mostly restricted to vendor documentation sites) and
three Keenable page extractions (NIST SP 800-86, Microsoft's password spray playbook, Microsoft
Defender XDR's password-spray IP alert guide). Keenable worked throughout, so Perplexity was not
needed and was not called. Neither tool was down. No secrets or customer data were sent.
Repository files were read for the dataset facts in section 7; nothing was changed.

`[P]` marks a claim checked against the owning first-party page (official documentation, MITRE,
IETF, NIST, ASD/CISA, Europol). `[S]` marks a claim read only in a search snippet of that
first-party page, not in the full page. `[V]` marks a claim resting on a secondary or
non-authoritative source, used only as a lead. Sources are listed at the end.

## 1. The question

T25 plans `find_peers(network)`: the users who share a network address with an account. In our
dataset the shared addresses are the company's two office addresses and a four-address VPN pool
that hands out addresses per session and reuses them. The author doubts that this sharing helps an
investigation. This note asks:

1. Which concrete investigation questions do analysts answer with "other accounts seen from this
   address"? Does it matter whether the address belongs to an attacker or to the company?
2. When do vendors and guidance treat a shared address as noise?
3. What extra evidence turns a shared address into a meaningful signal?
4. How do security tools present "related accounts on this address"?

## 2. Summary in plain language

- **The pivot is real, but it starts from a suspicious address.** Every first-party playbook found
  uses "which accounts signed in from this address" when the address is the attacker's. The aim is
  to find other victims of a spray, stuffing or token-theft campaign, and to rank them by success.
  No source was found that starts from a company office or VPN address to find victims.
- **Company addresses are documented as noise.** Microsoft, Okta and Google all tell you to
  declare office and VPN ranges so that detections ignore or down-weight them. Microsoft's UEBA
  even treats "my peers use this place too" as evidence of a false positive.
- **An address alone does not name a person.** The IETF, Europol and NIST all say a shared or
  reassigned address needs a time and an allocation record (DHCP, VPN or NAT log) before it points
  at one user or device. Our dataset has no allocation record.
- **The signal comes from other evidence.** Analysts use time overlap with an allocation log, the
  same device or user agent, how rare the address is, whether it is external, and success versus
  failure. Lateral movement is traced through device sessions and admin rights, not shared
  addresses.
- **Tools show it as an exploration, not a finding.** Sentinel's investigation graph adds IP
  pivots only when the analyst asks. Defender's IP page lists the devices that talked to a
  suspected address. Splunk uses a separate Session Center to turn an address into a user.
  No vendor counts co-users of a corporate address as affected accounts.
- **For our data:** the attacker's address in S6 is already covered by `search_logins(ip=...)`
  and the spray finding's address sentence. The S6 shared-address context (43 office, 10 VPN) is
  Amelia's ordinary neighbours on her own legitimate addresses. The attacker never used them.
  Without VPN allocation records, those matches can answer "is this address normal here?" but not
  "who else was on it at that moment?".

## 3. Question 1: which investigation questions use "other accounts on this address"

### 3.1 Documented uses

| Investigation question | Whose address | What the analyst does | Source |
|---|---|---|---|
| **Find other victims of a spray or stuffing campaign** | Attacker-controlled, external | Filter successful sign-ins from the attack address over the attack period. These are "your accounts of interest". | [P] Microsoft password spray playbook; [P] Defender XDR spray-IP alert guide ("review the accounts that signed in from that IP. It's possible that a group of accounts were compromised") |
| **Rank the victims** | Attacker-controlled | Prioritise successful sign-ins by the attacker address, then interrupted ones (password right, MFA failed), then unsuccessful ones, then other unknown addresses' successes. | [P] Microsoft password spray playbook |
| **Check whether others were targeted** | Attacker-controlled | "Validate that no other users in your directory are targets of the same attack", and look for the same atypical user agent, application, protocol, ASN ranges and timing. | [S] Microsoft Entra ID Protection, investigate risk |
| **Pivot across attacker infrastructure** | Attacker-controlled | Check other addresses in the same subnet or ISP; spray often comes from many addresses in one range. ATT&CK's credential-stuffing analytics key on one source address authenticating as many identities. | [P] Defender XDR spray-IP guide; [S] ATT&CK DET0460, DET0487 |
| **Scope a token-theft incident** | Attacker-controlled | "Use sign-in logs to get users with same IP address" as the attacker, then check for persistence. | [S] Microsoft token theft playbook |
| **Scope contact with a malicious host** | External (C2) | Defender's IP entity page lists devices in the organisation that communicated with the address, to "determine the potential scope of breach". | [S] Defender XDR IP entity page |
| **Decide the address is benign** | Any | If several users sign in successfully with MFA from the address, that "might indicate that the IP isn't malicious". | [P] Defender XDR spray-IP guide |

In every row, the address is the thing under suspicion. The question is "who else did this bad
address touch?". Our spray rule and the agent's log tools already answer it (section 7.1).

### 3.2 Questions that look related but use other evidence

| Question | What vendors actually pivot on | Source |
|---|---|---|
| **Session hijack or token replay** | One account's session changing address or device mid-session, or one session ID seen from two locations. It is within one account, not across accounts. | [S] Okta ITP session protection; [S] Defender session cookie theft guide; [S] Entra linkable identifiers (session ID) |
| **Credential sharing or a second person using one login** | One account seen from distant places too fast. Microsoft describes impossible travel as "indicating that a different user is using the same credentials". | [S] Defender for Cloud Apps anomaly policies |
| **Lateral movement** | Where a sensitive account's credentials were left on a computer ("logged into by") and who has admin rights there. It is device and session evidence, not a shared address. | [S] Defender for Identity lateral movement paths; BloodHound `HasSession`, see note 01 |
| **Password hygiene around the victim** | "Check accounts of anyone working in the same office/delegated access". In context this is a people check on colleagues and delegates for password reuse. It does not mention addresses. Reading it as "same office network address" would be our interpretation. | [P] Microsoft password spray playbook |

No first-party source was found that uses "other accounts that shared a company VPN or office
address" as a credential-sharing, lateral-movement or spread signal.

## 4. Question 2: when a shared address is documented as noise

### 4.1 How vendors treat known company addresses

| Vendor | What the documentation says | Effect on detection | Source |
|---|---|---|---|
| **Microsoft Entra ID Protection** | Configure named locations and add VPN ranges to Defender for Cloud Apps. Sign-ins from trusted or known locations "lower a user's risk" and reduce false positives. | Corporate and VPN addresses are down-weighted | [S] Plan an ID Protection deployment |
| **Microsoft Entra (Zero Trust guidance)** | Without named locations, ID Protection "can't assess location-based risk signals", which raises false positives and alert fatigue. | Declaring company addresses is the baseline | [S] Protect networks guidance |
| **Defender for Cloud Apps** | Categories: Corporate (office, branch and Wi-Fi egress) and VPN (remote workers). The VPN category exists "to avoid raising impossible travel alerts". When both sides of a journey are tagged corporate, the journey is trusted. The impossible-travel model ignores "VPNs and locations regularly used by other users in the organization". | Corporate and VPN addresses are suppressed in travel detections | [S] IP ranges and tags; [S] Anomaly detection policies |
| **Defender for Cloud Apps** | The suspicious-IP and anonymous-IP models reduce false positives from "mis-tagged IP addresses that are widely used by users in the organization". It warns that "IPs that serve malicious actors are also being in use by legitimate employees", so examine each case. | Wide use inside the organisation lowers suspicion | [S] Anomaly detection policies; [S] IP ranges and tags |
| **Okta** | The exempt zone lets traffic through "irrespective of" ThreatInsight, blocked zones or IP-change events. A VPN concentrator should be a trusted proxy so Okta evaluates the real client address. Session protection lets admins exclude HQ/VPN zones from re-evaluation. Session context changes "don't imply action or risk on their own". | Corporate and VPN gateways are excluded or looked through | [S] Okta trusted proxies; [S] IP zones; [S] Configure session protection; [S] Session protection |
| **Google Workspace** | The logged IP "might reflect your physical location, but it can be something else like a proxy server or a Virtual Private Network (VPN) address". | The address is a hint, not an identity | [S] Login audit log; [S] User log events |
| **Microsoft Sentinel UEBA** | Insights include `ISPUncommonlyUsedAmongPeers` and `ISPUncommonlyUsedInTenant`. Its tip: if the user's peers usually connect from the same locations, "this knowledge would make an even stronger case for a false positive". | Shared use among peers argues for benign | [S] Investigate incidents with UEBA |

**Pattern:** vendors use "many of our own users share this address" to suppress or down-weight
alerts. They do not use it to find exposed accounts.

### 4.2 Address-sharing technologies and attribution limits

| Kind of sharing | What the source says | Source |
|---|---|---|
| **Carrier-grade NAT** | One public address is shared by many subscribers at once. Without the source port and an accurate timestamp, operators "will not be able to identify unambiguously customers". | [P] IETF RFC 6302 |
| **Carrier-grade NAT** | Thousands can share one address, so innocent people may be "wrongly investigated" because they share an address with criminals. | [S] Europol, 2017 |
| **DHCP and session-assigned pools** | DHCP servers can log each assignment with MAC address and timestamp. This "can be helpful to analysts in identifying which host performed an activity using a particular IP address". Spoofing remains possible. | [P] NIST SP 800-86 §6.4.2.1 |
| **VPN and DHCP sessions** | Splunk's Network Sessions model records the address "leased to the client" and the user of a VPN session. The Session Center uses DHCP or VPN data to "identify the user or machine associated with an IP address used during a session". | [S] Splunk CIM Network Sessions; [S] Splunk ES 8 asset and identity dashboards |
| **Cloud proxy or security edge** | The sign-in log records the proxy egress address, which "prevents security operations teams from correlating sign-in events to user locations during incident response". | [S] Microsoft Entra Protect networks guidance |
| **Logging baseline** | Logs should carry accurate timestamps, device identifier, session or transaction ID, ASN, source address and user ID. | [S] ASD/CISA and partners, Best practices for event logging (citing OMB M-21-31) |

Our VPN pool is a session-assigned pool (T19 decision 2). By these sources, a pool address names
one user only when combined with the gateway's allocation record for that moment.

## 5. Question 3: what turns a shared address into a meaningful signal

| Added evidence | Why it matters | Source | In our dataset? |
|---|---|---|---|
| **Allocation record for the moment** (VPN session, DHCP lease, NAT port) | Ties an address at a time to one user or device. Without it a pool address is ambiguous. | [P] RFC 6302; [P] NIST SP 800-86; [S] Splunk Network Sessions | **No.** The log has `source_ip` only; no allocation telemetry is approved (T19 d2/d3) |
| **Time overlap** | Our own runbook and policy say a VPN address "without its time is insufficient attribution" and to "compare session allocation times". Login timestamps alone do not give session start and end. | Dataset corpus: `run-compromised-account-response.md` step 4 and 6, `pol-remote-access.md` | Partly. Sign-in times exist; session spans do not |
| **Same device or user agent** | Entra's unfamiliar-sign-in-properties detection weighs IP, ASN, location, device, browser and tenant subnet together. Spray victims share atypical user agent, app, protocol and ASN ranges. | [S] Entra risk detections; [S] Entra investigate risk | **Yes.** `device_id` and user agent are logged. `device_id` is empty for attacker rows and phones |
| **Rarity of the address** | UEBA flags values "rarely observed across the tenant population". Wide use lowers suspicion. | [S] Sentinel UEBA anomalies; [S] Defender for Cloud Apps | Computable. 43 of 50 accounts on the UK office address is the opposite of rare |
| **External versus company address, plus reputation** | Vendors split addresses into corporate, VPN, cloud, risky and anonymous. A malicious-IP verdict comes from high failure rates or reputation. | [S] Defender for Cloud Apps IP tags; [S] Entra risk detections | **Yes.** The networks table gives the kind; `lookup_ip_reputation` covers external addresses |
| **Success versus failure** | Playbooks rank successes first. Elastic's entity store will not treat a failed login as identity evidence. Defender for Cloud Apps' location detections skip failed logins. | [P] Microsoft spray playbook; [V] Elastic Security Labs blog; [S] Defender for Cloud Apps | **Yes.** Address edges are already success-only (T19 d1) |
| **MFA outcome** | Several users succeeding with MFA from one address suggests it is not malicious. | [P] Defender XDR spray-IP guide | **Yes.** `mfa_result` is logged |
| **Session identifier** | Entra's session ID links every token from one interactive sign-in, so a session can be followed across services. | [S] Entra linkable identifiers | **No** |
| **Activity after sign-in** | Search the accounts that signed in from the address for unusual activity afterwards. | [P] Defender XDR spray-IP guide | **No.** No application or audit log |

## 6. Question 4: how tools present "related accounts on this address"

| Tool | Presentation | Labelled, ranked or suppressed? | Source |
|---|---|---|---|
| **Microsoft Sentinel investigation graph** | Hover an entity to see "exploration queries" written per entity type, for example Related alerts. Results join the graph, linked by dotted lines. Each query can open its raw events. | Analyst-driven exploration. Nothing is added until asked | [S] Investigate incidents with Sentinel (legacy and Azure portal) |
| **Sentinel entity pages and incident insights** | An IP entity page (preview) with geolocation. Insights such as "IP address remote connections" and "...with TI match", run over a window from 24 hours before the earliest alert. | Shown as insights, scoped to the incident window | [S] Sentinel entity pages; [S] Investigate incidents in depth |
| **Defender XDR IP entity page** | "Observed in organization" lists devices that connected to the address, up to 100, with threat-intelligence tabs beside it. Its stated purpose is scoping contact with a suspected malicious address. | Context for a suspect address, capped | [S] Defender XDR IP entity page |
| **Defender XDR incident** | "Scope" lists impacted devices, users and mailboxes "in order of risk level and investigation priority". Entities enter because alerts tie them in, not by address sharing. | Ranked by risk | [S] Defender XDR investigate incidents |
| **Splunk Enterprise Security** | Asset and identity correlation enriches events by matching addresses to assets, preferring an exact address over a subnet. A separate Session Center turns an address into the user or machine for a session, from DHCP/VPN data. | Address-to-user mapping is a distinct, time-bound step | [S] Splunk ES asset and identity correlation (ES 4.x docs); [S] Splunk ES 8 dashboards |
| **Elastic entity analytics** | Entities are users, hosts and services, plus generic resources. Relationship jobs such as `accesses_frequently` count successful accesses over 30 days. Failed logins are not identity evidence. A graph view shows an entity's connections over 30 days. No address-sharing relationship is documented. | Built from successful access only; address is not an entity type | [V] Elastic Security Labs engineering blog (first-party, but a blog); [S] Elastic entity analytics docs |
| **Okta** | IP and device changes in a session are logged as `user.session.context.change`. Only those failing policy re-evaluation become session violations. | Context events by default; risk only on policy failure | [S] Okta session protection |

**Pattern:** tools offer the address pivot as an analyst-triggered exploration around a suspect
address, rank what they show by risk, and suppress known company ranges. No tool was found that
lists co-users of a corporate address as affected or exposed accounts.

## 7. What this means for our data

### 7.1 Dataset facts that decide the answer

| Fact | Where it comes from |
|---|---|
| The log has time, user, source IP, country, device, outcome, user agent, plus `device_id` and `mfa_result`. No VPN session or allocation records. | Spec, synthetic world (T04); AUD-060 |
| `used address` edges exist only for **successful** sign-ins to addresses **in the networks table**. | T19 decision 1; `truth.json` `used_address_filter` |
| The networks table holds two offices, a corporate proxy, a cloud egress, a public resolver, 47 per-person home addresses and four VPN pool addresses. | `backend/data/datasets/default/org/networks.csv` |
| S6's attacker address (45.148.10.80) is **not** in the networks table. It therefore creates no graph edge, and its 20 failures would not anyway. | `truth.json` S6; T19 decision 1 |
| S6's address context comes from **Amelia's own legitimate addresses**: the UK office (43 other accounts) and VPN pool address 4 (10 other accounts). | `truth.json` S6 `address_reuse_context` |
| The agent already has `search_logins(ip=...)`, which returns exact counts and sample rows for everything one address did, with optional outcome and time filters. | `backend/login_investigator/tools.py` |
| The spray finding already carries a code-built sentence naming the accounts its address signed in to. | Spec decision log, T43 rulings 4, 8 and 9 |
| The dataset's own runbooks ask for related accounts on "the same device or address in the same period", and say a VPN match needs session allocation times. | `run-compromised-account-response.md` step 6; `run-new-country-sign-in.md` step 4 |

### 7.2 Case (a): the attacker's external address touching many accounts

- **Question it answers:** "Which other accounts did this address sign in to, and which did it
  only try?" This is the documented core of spray and stuffing scoping (section 3.1).
- **Evidence we have:** the log rows from that address, with outcome, time, user agent, empty
  `device_id` and `mfa_result`; the reputation file; the spray rule's finding and its T43
  address sentence.
- **Who answers it today:** the spray rule plus `search_logins(ip=45.148.10.80)`. `find_peers` by
  network would **not** answer it, because the attacker address has no graph edge.
- **Evidence missing:** activity after sign-in, session identifiers, and sibling addresses in the
  same subnet or ASN beyond what the reputation file states.

### 7.3 Case (b): employees reusing the VPN pool or office address near a compromised account

| Possible question | Can our data answer it? | Why |
|---|---|---|
| "Was someone else on this VPN address at the moment of the suspicious sign-in?" | **No** | It needs the gateway's allocation log (RFC 6302, NIST SP 800-86, Splunk Session Center). Sign-in timestamps do not give session spans. Our runbook says the same. |
| "Did the attacker use our VPN or office to reach other accounts?" | **Not applicable to S6** | The attacker never signed in from a company address in S6. The matches are Amelia's ordinary neighbours. |
| "Is this address normal for this person and their colleagues?" | **Yes** | Rarity and baseline can be computed from the log. Vendors use this to argue *for* a false positive (Sentinel UEBA, Defender for Cloud Apps). |
| "Could the compromise spread to these accounts?" | **No, not from address reuse** | Vendors trace spread through device sessions, admin rights and group reach. T19 d3 already rules that reuse is not exposure or spread. |
| "Do colleagues reuse the victim's password?" | **Not from addresses** | Microsoft's "same office" check is about people and delegates. Department and group data in the graph fit it better than addresses. |
| "Is the account shared, or was the session hijacked?" | **Not from cross-account matches** | Vendors look at one account across places, devices and session IDs. |

## 8. The three options for the author

No option is recommended. The author decides.

### 8.1 Retain

Keep `find_peers(network)` as specified: all organisation-address co-users, grouped by address,
date-filtered, labelled as context and outside exposure counts (T19 d3 to d5).

| For | Against |
|---|---|
| The dataset's own runbooks ask the analyst to identify accounts on the same address in the same period, so the tool matches a written procedure. | No first-party source uses co-users of a corporate or VPN address to find victims, spread or credential sharing. |
| Sentinel and Defender both offer an address pivot, so analysts expect one. | Vendors suppress or down-weight exactly these addresses (section 4.1). |
| The core calculation is already built and tested at T19, with dates, coverage statements and grouping. | Without allocation records the VPN matches cannot be tied to a moment. The runbook itself says so. |
| Labels and the exposure-count exclusion are already agreed. | 43 of 50 accounts share the UK office address. The list adds volume, not discrimination. |
| | The author's gate notes that labels do not establish usefulness. T43 showed the model repeating numbers it is given, so a list of 53 names risks being narrated as spread. |

### 8.2 Narrow

Keep a network form of the tool, but limit what it returns. These variants are not exclusive.

| Variant | For | Against |
|---|---|---|
| **Return a baseline summary instead of names**: address kind, how many accounts use it in the period, and whether it is usual for this account. | Mirrors UEBA's "uncommon value" insight; answers the one question our data supports; small, hard to misread. | Drops the names the runbook step asks for; needs a new output shape and spec change. |
| **Exclude shared company kinds** (office, VPN, proxy, cloud) from network peers, keeping only rarer addresses. | Matches vendor practice of trusting company ranges. | Home addresses are one person each, so the result would almost always be empty. The tool may then add little. |
| **Require a tight window around the alert** by default, rather than the full log period. | Fewer, closer matches; aligns with "in the same period" in the runbook. | Still no allocation data, so overlap stays unproven; it changes T19 decision 4's default. |
| **Point the network pivot at external addresses**, including failures. | That is the documented use (section 3.1). | Duplicates `search_logins(ip=...)` and the spray finding; needs reopening T19 decision 1 (success-only, networks table only). |
| **Keep names but rank them** by evidence beyond the address (same device, close time, same user agent). | Follows the "added evidence" pattern of section 5. | More design and eval work; device evidence already lives in device peers. |

### 8.3 Remove

Drop the network form from `find_peers`. Keep account and device peers. Address questions go
through the existing log tools.

| For | Against |
|---|---|
| The documented question (case a) is already answered by `search_logins(ip=...)` and the spray finding. | Removes the tool form of a step the dataset's runbooks describe; the agent would need to reach it another way. |
| Matches how vendors treat company addresses: trusted, suppressed or looked through. | Loses an easy way to show that an address is ordinary, unless provided elsewhere. |
| Removes the risk of the model reading 53 names as affected accounts. | T19's radius already returns the address context. T26's `investigate_alert` would still need its own ruling on whether to keep it. |
| Simpler tool, smaller artifact, fewer eval checks. | Needs spec, T25 and decision-log changes, and possibly answer-key changes if the radius drops the context too. |

## 9. Open questions and limits

- **No vendor measures value.** Vendor documents describe product behaviour, not how often a pivot
  helps. "No source found" for corporate-address victim finding is absence of evidence, not proof.
- **Coverage gaps.** CrowdStrike Falcon Identity documentation sits behind a customer portal and
  was not consulted. Google Workspace was checked only for its log fields. Splunk's asset and
  identity correlation rules were read in older ES 4.x pages; the Session Center was confirmed in
  ES 8 pages.
- **Snippet reading.** Most first-party claims (`[S]`) come from Keenable's extracts of the
  official pages, not full reads. Three pages were extracted in full (`[P]` items from NIST
  SP 800-86, the Microsoft password spray playbook and the Defender XDR spray-IP guide). RFC 6302
  was read in its text form through the search results.
- **The Microsoft "same office" line** is short. The reading that it means colleagues, not a
  network address, is ours.
- **Elastic** claims rest on a first-party engineering blog, not product documentation.
- **Europol** statements date from 2017. Their figures for CGN use may have changed.
- **Not checked:** whether any of S6's ten VPN-4 matches fall close in time to the attack. Even if
  they did, the log could not show session overlap.
- **For the author to decide:** whether a narrowed or removed network form also changes T26's
  radius output, the answer key or the Graph tab. This note does not cover those.

## Sources

All accessed 1 November 2026 through Keenable.

**Standards and government**
- IETF RFC 6302, Logging Recommendations for Internet-Facing Servers: https://www.rfc-editor.org/rfc/rfc6302
- NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-86.pdf
- ASD's ACSC, CISA and partners, Best practices for event logging and threat detection: https://www.cyber.gov.au/business-government/detecting-responding-to-threats/event-logging/best-practices-for-event-logging-and-threat-detection
- Europol, "Are you sharing the same IP address as a criminal?" (2017): https://www.europol.europa.eu/newsroom/news/are-you-sharing-same-ip-address-criminal-law-enforcement-call-for-end-of-carrier-grade-nat-cgn-to-increase-accountability-online
- MITRE ATT&CK T1110.003 Password Spraying: https://attack.mitre.org/techniques/T1110/003/
- MITRE ATT&CK T1110.004 Credential Stuffing (DET0460 analytics): https://attack.mitre.org/techniques/T1110/004/
- MITRE ATT&CK DET0487, Distributed Password Spraying: https://attack.mitre.org/detectionstrategies/DET0487
- MITRE D3FEND D3-UGLPA, User Geolocation Logon Pattern Analysis: https://d3fend.mitre.org/technique/d3f:UserGeolocationLogonPatternAnalysis
- MITRE D3FEND D3-ANET, Authentication Event Thresholding: https://d3fend.mitre.org/technique/d3f:AuthenticationEventThresholding

**Microsoft**
- Password spray investigation playbook: https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-password-spray
- Token theft playbook: https://learn.microsoft.com/en-us/security/operations/token-theft-playbook
- Defender XDR, alert classification for suspicious IP related to password spray: https://learn.microsoft.com/en-us/defender-xdr/alert-classification-suspicious-ip-password-spray
- Defender XDR, session cookie theft alert grading: https://learn.microsoft.com/en-us/microsoft-365/security/defender/session-cookie-theft-alert
- Defender XDR, IP address entity page: https://learn.microsoft.com/en-us/defender-xdr/entity-page-ip
- Defender XDR, investigate incidents: https://learn.microsoft.com/en-us/defender-xdr/investigate-incidents
- Entra ID Protection, risk detections: https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks
- Entra ID Protection, investigate risk: https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk
- Entra ID Protection, plan a deployment (known network locations): https://learn.microsoft.com/en-us/entra/id-protection/how-to-deploy-identity-protection
- Entra security guidance, protect networks: https://learn.microsoft.com/en-us/entra/fundamentals/zero-trust-protect-networks
- Entra, linkable identifiers: https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-authentication-track-linkable-identifiers
- Defender for Cloud Apps, IP ranges and tags: https://learn.microsoft.com/en-us/defender-cloud-apps/ip-tags
- Defender for Cloud Apps, anomaly detection policies: https://learn.microsoft.com/en-us/defender-cloud-apps/anomaly-detection-policy
- Defender for Cloud Apps, detect suspicious activity using UEBA: https://learn.microsoft.com/en-us/defender-cloud-apps/tutorial-suspicious-activity
- Defender for Identity, lateral movement paths: https://learn.microsoft.com/en-us/defender-for-identity/classic-use-case-lateral-movement-path
- Sentinel, entity pages: https://learn.microsoft.com/en-us/azure/sentinel/entity-pages
- Sentinel, investigate incidents in depth: https://learn.microsoft.com/en-us/azure/sentinel/investigate-incidents
- Sentinel, investigate incidents (legacy, investigation graph): https://learn.microsoft.com/en-us/azure/sentinel/investigate-cases
- Sentinel, investigate incidents with UEBA data: https://learn.microsoft.com/en-us/azure/sentinel/investigate-with-ueba
- Sentinel, UEBA anomalies on behaviours: https://learn.microsoft.com/en-us/azure/sentinel/ueba-anomalies-on-behaviors

**Okta**
- Trusted proxies: https://help.okta.com/en-us/content/topics/security/network/about-trusted-proxies.htm
- IP zones: https://help.okta.com/en-us/Content/topics/security/network/about-ip-zones.htm
- Session protection: https://help.okta.com/oie/en-us/content/topics/itp/continuous-access-evaluation.htm
- Configure session protection: https://help.okta.com/oie/en-us/content/topics/itp/configure-session-protection.htm
- About Behavior Detection: https://help.okta.com/en-us/Content/Topics/Security/behavior-detection/about-behavior-detection.htm

**Google**
- Login audit log: https://support.google.com/a/answer/4580120
- SAML log events: https://support.google.com/a/answer/7007375

**Splunk**
- ES 8 asset and identity dashboards (Session Center): https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.4/analytics/asset-and-identity-dashboards
- CIM Network Sessions data model: https://help.splunk.com/en/splunk-enterprise-security-8/common-information-model/8.5/data-models/network-sessions
- ES asset and identity correlation (ES 4.2 docs): https://docs.splunk.com/Documentation/ES/4.2.0/User/AssetandIdentityCorrelation

**Elastic**
- Entity analytics documentation: https://www.elastic.co/docs/solutions/security/explore
- Elastic Security Labs, entity definition, identity resolution and entity risk scoring (first-party blog, `[V]`): https://www.elastic.co/security-labs/blog/entity-resolution-identity-scoring-elastic-security

**Repository files read (not changed)**
- `.scratch/knowledge-base/issues/25-peers-and-corpus-search-tools.md` (the gate)
- `.scratch/knowledge-base/issues/19-graph-integrity-and-radius.md` (Answer decisions 1 to 5)
- `docs/audit/improvement-register.md` (AUD-060)
- `.scratch/knowledge-base/spec.md` (VPN address meaning, address grouping, relationship dates, used-address edges, S6)
- `backend/data/datasets/default/org/networks.csv`, `backend/data/datasets/default/truth.json` (S6)
- `backend/data/datasets/default/corpus/own/` runbooks and policies that mention the VPN pool
- `backend/login_investigator/tools.py` (`search_logins`)
