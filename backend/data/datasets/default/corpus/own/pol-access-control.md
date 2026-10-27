---
id: "pol-access-control"
title: "Access Control Policy"
kind: "policy"
owner: "Security"
department: "IT"
date: "2026-05-12"
version: "2.1"
status: "current"
supersedes: null
---

# Access Control Policy

## Purpose and scope

Access follows the work a person needs to do. Being employed by the company does not give someone permission to administer systems or approve payments. This policy covers accounts and access to company information in the UK office, the US office and remote working locations. It applies to employees, system owners and anyone handling an access request.

Use the smallest set of permissions that allows the work to be completed. A useful permission is not automatically a necessary permission. Access for a temporary assignment must have an end date. The requester must describe the work, the systems involved and the duration before approval is sought.

## Baseline and privileged access

Every member of staff belongs to All Staff. This provides access to email, intranet and file share. Permission to use the file share does not permit unrestricted distribution of confidential material. Staff must still follow the handling instructions for the information they use.

Privileged access is provided only through IT Admins, Finance Approvers and HR Data Owners. Do not create individual grants as a shortcut around group approval. The system owner must approve access to the relevant system before group membership is changed. Where one group reaches several systems, obtain approval from each affected system owner. A manager's request alone is not sufficient authority to make the change.

The approved memberships are:

| Group | Members |
|---|---|
| IT Admins | Amelia Ward (amelia.ward), Joseph Burton (joseph.burton), Leah Gibbons (leah.gibbons), Ruby Stevens (ruby.stevens) |
| Finance Approvers | Hannah Porter (hannah.porter), Mark Sullivan (mark.sullivan), Max Thornton (max.thornton), William Ellis (william.ellis) |
| HR Data Owners | Benjamin Cole (benjamin.cole), Chloe Barker (chloe.barker), Grace Mitchell (grace.mitchell) |

Department membership does not replace these rules. Someone in Finance does not automatically become a Finance Approver. Someone outside Finance may have approved membership when their duties require it.

## Systems and accountable owners

| System | Sensitivity | System owner | Access group |
|---|---|---|---|
| email | internal | Joseph Burton | All Staff |
| intranet | internal | Amelia Ward | All Staff |
| file share | confidential | Amelia Ward | All Staff |
| identity provider | restricted | Amelia Ward | IT Admins |
| VPN gateway | confidential | Leah Gibbons | IT Admins |
| domain controller | restricted | Ruby Stevens | IT Admins |
| payments system | restricted | Hannah Porter | Finance Approvers |
| ERP | confidential | Max Thornton | Finance Approvers |
| HR system | restricted | Chloe Barker | HR Data Owners |

For the identity provider, VPN gateway and domain controller, the group shown controls administrative access. All staff sign in through the identity provider. All staff may connect through the VPN gateway. These ordinary activities do not make the person an administrator. Owners must explain this distinction when approving requests so that support does not grant administrative permissions for routine sign-in or remote work.

## Joiners

People confirms a new starter's identity, department, office and starting date. IT Support issues an individual account and company laptop against that instruction. All Staff membership is the starting position. Any request for privileged membership follows the owner approval process separately.

The helpdesk records what was requested, who approved it, who applied it and when it was checked. Dates and times in the record use UTC. Before closing the request, confirm that the person can reach the required systems and that no unrelated group was added. First sign-in includes the password and MFA setup required by the current policies.

## Movers and temporary duties

A change of role is a new access decision. The receiving manager describes the new duties; the previous manager identifies permissions that are no longer needed. IT Support removes unnecessary memberships as part of the move, rather than allowing permissions to accumulate across roles.

Temporary membership must identify a person responsible for confirming its removal. If work continues beyond the agreed end date, obtain a fresh owner approval. Do not extend access merely because nobody has complained. Record both the new permission and any permission removed in the same request where practical.

## Leavers

People supplies the last working day and informs IT Support of any changes to it. Access must be removed on the last working day. Coordinate the timing with People so that an account does not remain usable after the agreed departure point. Disable sign-in, end active sessions and remove group memberships. Company equipment is returned through IT Support.

The analyst records completion and checks that all listed systems have been covered. A returned laptop is not evidence that account access has ended. Escalate an incomplete removal to Security and the affected system owner immediately.

## Quarterly review and exceptions

Each quarter, system owners review membership against actual duties. IT Support provides the membership list and approval records. Owners confirm continuing need or instruct removal; silence is not approval. Security follows up missing responses and unresolved permissions.

Thomas Price (thomas.price), who leads security, resolves disputes about unnecessary privilege with the owner. No one may approve their own access request. Changes must remain traceable to the person who requested, approved and implemented them. Access review supports M1018; the working requirement is the owner review and removal process described here.
