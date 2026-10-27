---
id: "run-password-spray-response"
title: "Password Spray Response"
kind: "runbook"
owner: "Security"
department: "IT"
date: "2026-07-14"
version: "1.1"
status: "current"
supersedes: null
---

# Password Spray Response

## When to use this procedure

Use this procedure when one source appears to be trying one or a few common passwords against many accounts. Repeated failures against one account are not enough to establish this pattern. Security leads the assessment, with IT helping to apply access changes and obtain the relevant sign-in records.

Record observations and action times in UTC. Separate confirmed facts from assumptions. A source address can be shared, particularly through the VPN gateway, so do not assume that it identifies one employee. Keep the scope focused on the observed activity and expand it when evidence supports doing so.

## Response steps

1. **Confirm the pattern across accounts.** Compare attempts from the source over a defined time window. Count distinct accounts, note the timing and compare the failure reasons. Establish whether the behaviour is consistent with one or a few common passwords being tried broadly. Do not collect or reproduce attempted password values. If the records do not establish the pattern, record the uncertainty and investigate other explanations, including an ordinary password problem.

2. **Block the source.** Ask the responsible administrator to block the observed source at the relevant access boundary. Record who applied the block, when it took effect and how it was checked. Consider whether it is a shared company connection so that the impact on legitimate staff is understood. If a precise block cannot be applied, escalate immediately to Thomas Price (thomas.price) for a containment decision. Do not treat a requested block as completed until it has been verified.

3. **Check for successful attempts.** Search the same source and time window for successes, not just failures. Include activity immediately before and after the visible failure pattern where useful. List each account with a successful result and the corresponding time and device. A successful sign-in is a priority for investigation even if the account had many earlier failures. A source block does not end a session already created.

4. **Check MFA for each success.** Establish whether the sign-in included completed MFA. Check the MFA Exception Register for the named account and the approval period. Distinguish a completed challenge from a prompt merely being issued. If the account had an exception, identify its scope and justification. Neither an exception nor a completed challenge proves that the person using the account was authorised.

5. **Reset passwords and revoke sessions.** For accounts with a success in the suspected pattern, arrange password resets and revoke active sessions. Use the verified helpdesk process when contacting staff. Record the completion of both actions separately. Do not ask a person to supply their existing password, app code or recovery code. Accounts without a success still need assessment; decide any additional action from the evidence rather than assuming all have been used.

6. **Check reachable systems.** List each affected account's actual group memberships. All Staff reaches email, intranet and file share. IT Admins provides administration of the identity provider, VPN gateway and domain controller. Finance Approvers reaches the payments system and ERP. HR Data Owners reaches the HR system. Use the membership at the relevant time where available and identify gaps in that evidence.

7. **Escalate account misuse.** Hand any account with a suspected unauthorised success to the Compromised Account Response procedure. Pass the source, time window, accounts, devices, MFA findings, group memberships and completed containment actions. Identify the person taking responsibility for the next steps. Do not close the assessment simply because the source has stopped trying.

## Completion checks

Security confirms that the block outcome, success search and account handovers are documented. If no success was found, state the records and time window examined. Describe any missing evidence plainly. Thomas Price decides whether further investigation or staff communication is needed. Use the Incident Communication Template if staff action is required.
