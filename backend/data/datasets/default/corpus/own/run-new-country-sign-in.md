---
id: "run-new-country-sign-in"
title: "New-Country Sign-In Triage"
kind: "runbook"
owner: "Security"
department: "IT"
date: "2026-08-03"
version: "1.0"
status: "current"
supersedes: null
---

# New-Country Sign-In Triage

## Purpose

Use this procedure for a successful sign-in from a country the account has not used before. A new country is a reason to establish context. It does not by itself show that the account has been misused. Security owns the decision and may ask IT Support to confirm device details or help contact the person.

Record the account, country, successful sign-in time in UTC and device name. Note whether the country comes from a sign-in record or another source. Do not describe the country estimate as proof of a person's physical location. T1078 may be relevant if subsequent checks support possible use of valid credentials by someone else.

## Triage steps

1. **Check travel notices.** Look for an approved notice covering the person, country and dates. Read the acknowledgement as well as the request. Confirm that the period includes the sign-in time. A notice for a neighbouring country or an earlier trip is not a match. If a notice is missing or incomplete, record the gap and continue the checks rather than assuming travel was approved.

2. **Check the company laptop.** Compare the sign-in device with the person's own issued laptop. Consult the current device record and any replacement handover. A replacement may legitimately have a different name from the original laptop. Confirm the effective handover time before deciding that an unfamiliar name is unexplained. A shared machine is not the person's own laptop. A personal phone is not registered company equipment, although reading email on it is permitted.

3. **Contact the person through a known channel.** Use contact details already established by the company. Do not rely on a reply from the session being checked or on new contact details offered during the enquiry. Ask whether they are in the country, whether they made the sign-in at the recorded time and which device they used. Never ask for their password, authenticator code or recovery code. Record the response and the time of contact in UTC.

4. **Compare all the evidence.** Check that the notice, device and person's confirmation agree. An approved journey explains the country only within its dates. It does not explain a device the traveller denies using. Also consider whether the sign-in route matches the Remote Access and VPN Policy. For VPN activity, match the session time because the gateway assigns addresses from a shared pool. Do not attach a different person's session to the traveller solely because an address matches.

5. **Decide and record the outcome.** Treat the sign-in as expected travel when the checks support that conclusion. State which notice, device evidence and contact confirmation support it. If travel is not confirmed, or the person denies the activity, treat the account as possibly misused and hand it over to the Compromised Account Response procedure. An unanswered call is not confirmation of travel. Escalate promptly rather than leaving the case indefinitely waiting for a reply.

6. **Complete the handover where required.** Provide the account, time, country, device, travel check and contact attempts. Identify which facts are confirmed and which remain uncertain. Include any containment already applied so that the next analyst knows the current access state. The receiving analyst should acknowledge responsibility for further action.

## Recording an expected journey

A conclusion of expected travel applies to the assessed activity. It must not suppress later checks for different dates, devices or countries. If the traveller extends or changes the trip, ask them to update Security through the normal travel notice process. Security records the outcome in plain language and closes the enquiry only when the relevant checks are complete.
