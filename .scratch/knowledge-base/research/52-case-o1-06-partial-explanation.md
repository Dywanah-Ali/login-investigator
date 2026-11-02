# O1-06: An approved trip explains only part of the activity

Date: 2 November 2026. Status: author accepted the representative scenario, expected
assessment and specification format on 2 November. Implementation remains unapproved.
No fixture, application code, model call or dataset rebuild has been executed.
Split: development/example, because the scenario and gold are being openly designed here.

## Purpose

Test whether a valid clearing document is applied only to the facts it explains. Compare
the final answers from A (one investigator), B (plus applicability specialist), and C (plus
review specialist). This diagnostic isolates reasoning over supplied evidence. It does not
prove retrieval, detection, full 30-day operation, permission enforcement or runtime stability.

## Analyst request

“Investigate Maya's successful sign-in at 14:00 UTC on 3 October, following repeated failures.
What does the available evidence suggest, and what remains unknown?”

Use the same wording for every architecture. Do not tell the model that this is a partial
explanation test or name the expected conclusion. Bind the event to the fixture finding when
materialised; derive its actual finding ID using the core, never invent a production ID.

## Fixture provenance and scope

- Reuse `rec-approved-travel` v1.0, unchanged and in full: Maya Patel, Germany, 2–4 October
  2026 inclusive, expected laptop LT-MPATEL. The notice explicitly limits what it establishes.
- Reuse the actual base event identified by account `maya.patel`, timestamp
  `2026-10-03T14:00:00Z`, address `203.0.113.70`, outcome success. The original event has
  device `dev-laptop-maya.patel` and MFA pass; it is currently B1 benign source material.
- In an isolated fixture only, replace that event's device field with empty and add the
  failure sequence below. Do not relabel the original B1 truth, modify its source event, or
  supply its original benign verdict to the model.
- Reuse Maya's organisation records: person `user-maya.patel`, Sales, country GB;
  membership in `group-all-staff`; registered laptop LT-MPATEL. Keep person country distinct
  from actual physical location. No structured job title is provided.
- Pattern anchor: 3 October 2026, 13:50–14:00 UTC. Proposed default requested and available
  diagnostic coverage: 2 October 13:50 through 4 October 14:00 UTC. Express exact inclusive/
  exclusive bounds using the core's existing time convention in the eventual fixture.
- This diagnostic snapshot contains only the 21 login events specified below in that
  coverage. It is deliberately small, not a claim about the full original dataset. Its
  realistic extension will require separate surrounding activity and the agreed 30-day world.
- No expansion is authorised in this case. No endpoint/resource-access events or confirmation
  from Maya are available. Source reputation is unavailable in this diagnostic package.

## Model-visible evidence manifest

Use neutral evidence references such as L1, G1 and D1 in the eventual package. Do not expose
test-family labels, expected assessments or this specification as model context.

| Evidence | Exact content or source |
|---|---|
| Login sequence | 20 failures at 30-second intervals from 13:50:00 through 13:59:30 UTC on 3 October; then one success at 14:00:00. All use account maya.patel, source 203.0.113.70 and country DE. Device field empty in all 21 rows. |
| Remaining event fields | Failures have failure_reason `bad_password`, MFA `none`; success has empty failure_reason, MFA `pass`. Use the original successful event's ordinary browser user-agent consistently. These are synthetic fixture choices, not observations from the current dataset. |
| Code-built facts | 20 failures and one success in the specified sequence; same account and source; source country DE; event device identity absent. Raw event evidence accompanies the counts. |
| Travel document | Full unchanged `rec-approved-travel` v1.0, including approval and the limits stated in its last paragraph. |
| Account/device records | Maya's identity and department, assigned laptop and all-staff membership. The assigned laptop does not identify the device behind the event. |
| Access context | Existing all-staff grants to email/internal, intranet/internal and file-share/confidential, with exact membership/grant paths. This is an organisation snapshot, not event-time access evidence. |
| Device peer result | `unavailable`: no event device can be resolved. Do not turn this into an empty peer list implying no peers. |
| Coverage/status | The stated diagnostic login coverage is available and contains the listed events. No truncation; source reputation, endpoint/resource telemetry and user confirmation unavailable. No material is silently omitted. |

Source inspection confirms `bad_password` is an allowed failure reason in the loader and
generator. Before generating, validate derived finding boundaries and the complete fixture
against the loader/generator. No runtime validation has passed yet. Freeze source bytes/hashes and variant provenance when
creating the fixture, and keep the reviewer-only gold separate from model-visible data.

## Gold assessment, reviewer-only

Required semantic findings:

1. State that a success followed 20 failures on this account from the same source in ten
   minutes. This remains concerning and warrants follow-up.
2. Recognise that the travel approval matches the person, country and date. It supports a
   legitimate explanation for the German source-country observation.
3. Explain that travel approval does not account for the failure-success pattern or establish
   the identity of the person using the account.
4. State that the event device is unknown. The registered/expected laptop cannot fill that gap.
5. Recognise recorded MFA completion without treating it as proof of authorisation or actor.
6. Keep the overall assessment unresolved, with concern explicitly retained. Both possible
   misuse and a legitimate recovery/credential-entry explanation may be discussed as
   hypotheses; neither is established by the available evidence.
7. Name useful follow-up evidence, such as known-channel confirmation of the activity and
   device/session evidence. Do not claim contact was made or new records were fetched.
8. Cite the log facts and travel document for their respective claims. Any access-context
   statement must cite its graph records and describe potential permission only.

Forbidden claims include: confirmed compromise; confirmed benign activity for the entire
sequence; verified use of LT-MPATEL; identification of an attacker-controlled device; Maya's
physical presence established by IP country; resource access inferred from permissions;
no peers inferred from unresolved device identity; or a completed follow-up that never ran.

Gold should reward meaning and supported reasoning, not require exact wording or hidden
ground-truth labels. One acceptable explanation is: the approval makes the location plausible,
but the repeated failures followed by success and missing device evidence leave the activity
unresolved and worth checking. This example stays out of agent inputs.

## Architecture execution and observations

- A receives the complete model-visible case file and makes the assessment.
- B's applicability specialist receives the same source evidence needed to test applicability;
  its findings go to the front investigator alongside the unchanged original case file.
- C first produces its own draft from the same case file. The reviewer receives that draft
  and source evidence; the front investigator receives the challenges and finalises its answer.
  Do not inject a deliberately faulty draft only into C for this end-to-end comparison.
- A separate reviewer unit test may use a fixed faulty draft, but its score cannot be pooled
  with final-answer architecture results.
- Record each required/forbidden semantic finding individually, source-reference validity,
  actual claim support, intermediate findings lost or corrected at handoff, final answer,
  calls/tokens, latency and errors. Preserve every trial; do not select the best run.
- Use the same model version and settings, reset case memory between trials, and record
  model-call budgets. Additional compute remains a confound until explicitly controlled.

Exact trial counts, scorer protocol, independent gold review and adoption thresholds remain
to be agreed. A passing diagnostic example is not architecture acceptance.

## Approval checklist before implementation

Author review of the representative scenario/expected assessment is complete. Remaining:
verify source/fixture consistency; agree scoring and
trial procedure; assign implementation owner and record approved spec changes. Keep original
B1/K07 and the existing dataset/evaluation gold unchanged. No paid evaluation or dataset
generation is authorised by drafting this representative case.
