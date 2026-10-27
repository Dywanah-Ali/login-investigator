---
id: "run-compromised-account-response"
title: "Compromised Account Response"
kind: "runbook"
owner: "Security"
department: "IT"
date: "2026-07-14"
version: "1.3"
status: "current"
supersedes: null
---

# Compromised Account Response

## Purpose and responsibility

Use this procedure when an account is believed to be in the wrong hands. It applies to ordinary staff accounts and privileged accounts. Security coordinates the work. IT applies the account changes, and affected system owners help assess what the account could reach. Reference T1078 where an investigation needs a classification; T1078.002 may apply to domain account use when the evidence supports it.

Open a working record with an SD- reference. Record the account, the reason for concern, the assigned analyst and action times in UTC. Distinguish what has been observed from what is still being checked. Do not wait for every detail before taking necessary containment action.

## Response steps

1. **Disable sign-in.** Ask an authorised IT Admins member to disable sign-in for the account. Record the person making the change and the completion time. Confirm that the action applied to the intended account. Tell the account holder through a known contact route that access is being handled by Security. Avoid relying on the account under investigation to establish who is responding.

2. **Revoke sessions.** End active sessions and check the outcome. Disabling a new sign-in does not by itself demonstrate that an existing session has ended. Record any session that cannot be revoked and contact the affected system owner for further action. Make the remaining exposure clear to the security lead.

3. **Reset the password.** Arrange a password reset using the helpdesk's identity verification process. The new password must follow the current Password Policy. Do not send it through the account being investigated or include it in the working record. Completing a reset does not authorise re-enabling sign-in. Keep that decision separate until the investigation and recovery checks are complete.

4. **Review sign-ins, devices and addresses.** Set a time window and examine recent activity, including successes and failures. Compare device names with the person's issued company laptop and any handover record. Check approved travel before treating a country change as unexplained. Record addresses in the investigation evidence where available, together with their session times. The VPN gateway reuses a small address pool, so an address without its time is insufficient attribution.

5. **List groups and reachable systems.** Establish membership during the period under review. All Staff reaches email, intranet and file share. IT Admins permits administration of the identity provider, VPN gateway and domain controller. Finance Approvers reaches the payments system and ERP. HR Data Owners reaches the HR system. Ask the owners of reachable systems to check relevant activity. Do not assume a person's department tells you which privileges they hold.

6. **Check related accounts.** Identify other accounts that used the same device or address in the same period. For shared machines, consult the Shared Device Register and confirm whether its entries are still accurate. For the VPN gateway, compare session allocation times before drawing a connection. Investigate a related account on its own evidence. Shared equipment or an address match is a reason to check, not proof that another account was misused.

7. **Review any MFA exception.** Check the MFA Exception Register for the account, approval, reason and review date. Establish whether sign-in occurred under that exception or with completed MFA. Ask whether the approved need still applies. Escalate any proposed exception change to Thomas Price (thomas.price). Do not leave an exception in place simply because it predates the concern.

8. **Prepare restoration and obtain sign-off.** Confirm that the account holder's identity has been verified, the password has changed, sessions have been revoked and the device is suitable for use. Confirm group memberships and the required MFA setup or approved exception. Summarise outstanding uncertainty for Thomas Price. Restore access only after his explicit sign-off, then record who restored it and when.

## Follow-through

After restoration, ask the person to complete a normal sign-in and confirm that the required access works. Check for unexpected activity during the agreed observation period. Keep staff instructions practical and avoid sharing speculative conclusions. Use the Incident Communication Template when a wider message is needed. Record open tasks with an owner and a due date so that restored access does not cause unfinished checks to be overlooked.
