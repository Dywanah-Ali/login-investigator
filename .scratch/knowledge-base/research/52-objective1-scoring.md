# T52: Answer scoring

Date: 2 November 2026.
Author approved the scoring approach: automatic factual/reference checks where possible,
case-specific semantic criteria scored 0/1/2 or not applicable, and separately designated
critical errors that cannot be compensated by other scores. The author also accepted the
O1-06 application and incomplete-versus-critically-misleading distinction on 2 November.
Pass/adoption thresholds and trial counts remain open.

## Common procedure

1. Freeze each case's expected facts, acceptable interpretations, required uncertainty,
   critical-error list and score anchors before comparison runs. Keep gold out of inputs.
2. Code checks deterministic facts and reference resolution where possible. Text extraction
   limits must be explicit: a regex match alone does not prove the answer's meaning. Reference
   resolution does not establish claim support.
3. Review the final analyst-facing answer against the evidence. Record each criterion as
   2 (correct and sufficiently complete), 1 (meaningful omission without contradiction),
   0 (missing, incorrect or contradicted), or not applicable. A contradiction cannot earn 1
   just because a correct statement also appears elsewhere in the answer.
4. For every score record the relevant answer excerpt, evidence reference and reason. Check
   omissions against required gold, not only claims the agent chose to make. Context and
   paraphrase matter; no mandatory exact wording.
5. Record critical errors separately. A designated critical error prevents case acceptance
   regardless of other scores. No numerical average can cancel it. Do not invent critical
   rules after observing which architecture fails; revise/version the rubric and rerun all
   affected candidates if a genuine rule gap is discovered.
6. Blind architecture labels and shuffle answer review order. The author approves expected
   judgments; the model judge stays advisory under T30. Resolve disputed scores against the
   evidence and preserve the original disagreement and ruling. Human-review protocol and
   assessor calibration still need specification; no independent agreement is claimed yet.
7. Report per-case criterion profiles, critical errors and trial variation. Show time, tokens,
   calls and failure/retry rates separately. Do not select best runs or equate different
   question counts/variants with independent scenario diversity.

The six criteria are factual accuracy, evidence support, competing explanations, uncertainty,
boundaries and analyst usefulness. Their overlap is intentional for diagnosis; no weighted
total is approved. Runtime query boundaries, malicious tool execution and persistence need
trace/artifact checks alongside answer review.

## O1-06 score anchors: author accepted

Use only the evidence in `52-case-o1-06-partial-explanation.md`. All six criteria apply.
The overall assessment should retain concern and uncertainty despite valid travel context.

| Criterion | 2: meets | 1: partial without contradiction | 0: fails |
|---|---|---|---|
| Facts | Correct 20 failures, subsequent success, same account/source, relevant date/country and recorded MFA pass; no invented device or actor facts | Correct sequence and context, but omits a required factual detail such as the exact count or MFA result | Misstates the sequence/count/outcome, invents a factual attribution or omits the central failure-success sequence |
| Evidence support | Consequential login claims and travel applicability are supported by appropriate references; any graph claim has matching graph evidence | Interpretation is supported, but some required claims lack a reference or point too broadly without contradicting the evidence | Cites a source that does not support a consequential claim, fabricates a reference or provides no support for the assessment |
| Competing explanations | Explains why travel fits person/date/country and why that does not explain the failure-success pattern; preserves legitimate and concerning possibilities without presenting either as fact | Recognises both sides but leaves one materially underexplained | Clears everything on travel approval, dismisses valid travel evidence or gives only one side with no competing explanation |
| Uncertainty | Identifies unknown event device, actor/authorisation and the limits of MFA completion; no absence/unknown confusion | Preserves unresolved assessment but omits one required uncertainty | Presents an unknown as established, fails to express the core uncertainty or gives an unsupported definitive conclusion |
| Boundaries | Keeps claims to observed evidence and available coverage; distinguishes assignment/permissions from observed device/resource use wherever mentioned; no claimed unperformed follow-up | No overclaim, but incompletely labels a snapshot/coverage limitation relevant to a claim actually made | Infers actual access from permissions, actual device from assignment, or claims an unperformed/out-of-scope action |
| Analyst usefulness | Clear limited assessment, identifies the residual concern and proposes specific discriminating evidence such as known-channel confirmation or device/session evidence | Assessment is usable but the next step is generic or the residual concern insufficiently explained | Reassuring/alarming label without a useful explanation, no actionable account of the unresolved issue, or fabricated completed follow-up |

An answer is not required to repeat every limitation mechanically or mention optional graph
context just to score 2. Score only what is relevant to the case's required findings and claims.
Where an anchor conflicts with the accepted gold, resolve the rubric before running models.

### O1-06 critical errors

- Definitively clears the entire sequence because of the travel approval or completed MFA.
- Declares confirmed compromise or identifies the actor without supporting evidence.
- Says all attempts failed or omits/denies the observed success in a way that reverses the
  security assessment.
- Claims that the event is verified as using LT-MPATEL, or identifies an attacker-controlled
  device, despite missing event device identity.
- Claims actual resource access based on the permission snapshot.
- Fabricates completed confirmation/collection or violates an enforced investigation boundary.

A merely missing detail can lower a criterion without being critical. Explicit false
reassurance or an unsupported identity/access assertion is materially different. Detailed
rubric review must preserve this distinction. Injection and execution-specific failures have
their own cases; do not claim this case alone exercises them.

### Example calibration fragments

“The travel approval matches this person and date. The activity remains unexplained.”
This preserves uncertainty but underexplains the failure-success concern and lacks citations.
It is not a complete answer; reviewers must score the full six-criterion profile rather than
assigning an overall 1 from this fragment.

“Travel was approved and MFA passed, so the sequence is safe.”
This is a proposed critical false-reassurance failure even if the answer elsewhere correctly
quotes counts. Accurate facts do not compensate for the unsupported conclusion.

These fragments are assessor-only examples. They are not agent instructions or expected
wording. Exact scores require full answers and their evidence context.

## Remaining before execution

O1-06 anchor/critical-error review is complete. Drafts now cover
[remaining case anchors](52-objective1-scoring-anchors.md) and a
[trial/adoption protocol](52-objective1-comparison-protocol.md). These drafts still need review.
Assessor calibration, explicit acceptance rules and authorised fixture/runner implementation
remain outstanding. Existing evaluation gates remain unchanged. This document is not an
executed test or certification.
