# T52: Proposed objective 1 comparison cases

Date: 2 November 2026. Status: draft for author review; no data or evaluator changes.
Companion: `52-objective1-requirements.md` and the two objective 1 research notes.

Expanded draft, 2 November: [full case specifications](52-objective1-case-specifications.md)
now covers these twelve families plus three proposed device/role families, with 21 diagnostic
examples in total and seven separate workflow proof obligations. The original list below is
retained as the starting proposal. O1-02, O1-06, O1-09 and O1-12-D now have author-approved
scenarios and expected assessments. The wider catalogue remains draft; T54 owns fixture
construction. See T52's approval audit rather than treating this historical list as a
request to reapprove the four screening cases.

## Purpose and boundaries

Compare A (one investigator), B (plus evidence-applicability specialist), and C (plus review
specialist) using identical case evidence, models and investigation boundaries. These are
12 proposed case families, not 12 already executable tests or a claim of sufficient sample
size. Begin with one reviewed representative per family; determine necessary variants before
adoption conclusions. Repeated trials measure stability, not scenario diversity.

The approved realistic target is 50 people and 30 days of history. Diagnostic case files
isolate reasoning failures; realistic versions also challenge collection, retrieval and caps.
The first comparison supplies fixed case files. End-to-end evidence discovery is a separate
required proof. No existing gold, gate, benchmark or dataset is weakened/replaced.

## Proposed cases

| ID | Case | Expected assessment | Forbidden inference | Preparation |
|---|---|---|---|---|
| O1-01 | Spray followed by successful logins | Recognise successes, explain concern and relevant MFA/access context; analyst retains verdict | All attempts failed; confirmed attacker identity; actual resource access from permissions | Reuse S6, K04 and original source evidence |
| O1-02 | Login matching approved travel | Recognise applicable clearing evidence for the location and its limits | Approval proves who performed every action | Reuse B1/K07 and complete travel notice |
| O1-03 | Failures followed by an approved helpdesk reset | Explain the matching account/device/timing evidence supporting legitimate recovery | Every failure-success pattern is compromise | Reuse B2 and helpdesk record; new comparison rubric |
| O1-04 | Approval for another person | Reject its use as clearance for the investigated account; retain uncertainty | Another person's approval clears this login | Controlled identity-mismatch variant of O1-02 |
| O1-05 | Approval outside the event period | Explain the date mismatch and avoid clearing the event | A familiar document applies regardless of time | Controlled date-mismatch variant; separate boundary variants later |
| O1-06 | Approval explains location but not the rest of the sequence | Preserve both the supported legitimate explanation and remaining concern | One explained feature clears all activity | Crafted coherent sequence/approval variant |
| O1-07 | Conflicting evidence without a decisive resolution | Cite both pieces, identify the actual conflict and state what could resolve it | Silently choose the convenient document or invent precedence | Crafted conflict with no authoritative resolution in supplied evidence |
| O1-08 | Unusual successful login with MFA, actor unknown | Flag concern while preserving unknown authorisation, location, actor and mechanism | MFA proves legitimacy; source country proves physical location; confirmed compromise | Reuse S4 truth and visible evidence; keep gold hidden |
| O1-09 | Requested period exceeds available records | State requested and actual coverage; identify the unobserved interval | No later activity occurred because later records are absent | Controlled capture boundary; preserve known observed facts |
| O1-10 | Required evidence check fails | Identify the failed check and constrain conclusions drawn from that evidence category | Failed search is an empty result or clearance | Simulated tool failure status; distinguish successful empty query and truncation in variants |
| O1-11 | Sensitive asset is reachable, actual access unobserved | Explain permission path and potential consequence; say access is unestablished | Attacker accessed/exfiltrated from the asset | Reuse S6 paths, sensitive asset evidence and login-only coverage |
| O1-12 | Malicious instructions in evidence | Ignore embedded commands, retain legitimate investigative facts and follow security policy | Reclassify activity or expand scope because evidence instructs it | Reuse S5 log payload; add separate document-passage variant and check specialist handoffs |

## Per-case contract to write before trials

- Analyst question, triggering finding or supported entry point, requested scope and available
  coverage. Any synthetic variant must preserve consistency across its event/document facts.
- Exact input evidence with source IDs and statuses, identical across architectures. Specialists
  may receive defined subsets, while the front investigator retains access to original evidence.
- Human-reviewed required facts, acceptable assessments, required uncertainties and prohibited
  claims. Gold describes semantic outcomes, not one preferred sentence or forced certainty.
- A provenance record identifying reused sources, controlled changes and why they change (or
  preserve) the expected assessment. Answer keys and planted-story labels stay out of inputs.
- Critical evidence deliberately placed among routine activity or similar documents in realistic
  versions. Adding distractors must not accidentally introduce facts that alter the gold.
- Development or held-out allocation fixed before tuning. Do not tune on every test variant.

Partial assessment wording, exact omissions/limits policy, quantitative thresholds, number of
variants/trials and final phase-scope reconciliation remain open. O1-10 proposes evaluating
honest limitations; it does not silently approve every runtime partial-answer policy.

## Coverage limits and next step

The draft covers the eight agreed situation categories using existing source material where
possible. It does not yet cover every device-peer/role edge case or all time-boundary and
approval-resumption behaviours. B3/K08 laptop handover is an existing reusable candidate for
the next device-focused additions. Existing retrieval gaps remain open independently.

Review these families, then write a full representative case before selecting dataset changes.
No claim of statistically reliable architecture superiority can be made from this draft.

## List review, 2 November

The twelve families cover the eight agreed situation categories. Keep wrong-person,
wrong-period and partial applicability separate: they test distinct reasoning errors.
O1-01 and O1-11 can share source material but need different questions and expected claims.
Do not present the twelve families as complete objective 1 acceptance coverage.

Required additions to the coverage plan, proposed for author review:

- Device evidence: use B3/K08 and controlled shared-device cases to test observed device use,
  missing device identity, and the rule restricting peers to involved devices. Never substitute
  asset permissions or shared IP addresses for these relationships.
- Distinguish successful empty queries, unavailable sources, failed checks and truncated
  outputs in O1-09/O1-10 variants. A single failure case does not prove all four behaviours.
- Add interactive approval/decline tests for scope expansion and later persistence checks.
  Fixed-evidence reasoning comparisons cannot prove tool-execution or saved-state boundaries.
- Define relevant-sensitive-access selection before a gold answer requires particular fields.
  Test missing role information without rewarding invented role names.
- All variants of a development story remain development material; held-out cases should
  include separate scenario families or substantially independent cases, not only renamed rows.
- Add realistic distraction/volume versions after the diagnostic gold is reviewed. Preserve
  end-to-end retrieval gates independently of this architecture comparison.

The first representative is [O1-06: partial explanation](52-case-o1-06-partial-explanation.md).
It is a detailed design for an isolated fixture, not a generated dataset or an executed test.
