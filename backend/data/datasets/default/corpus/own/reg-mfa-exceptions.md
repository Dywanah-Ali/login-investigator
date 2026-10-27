---
id: "reg-mfa-exceptions"
title: "MFA Exception Register"
kind: "register"
owner: "Security"
department: "IT"
date: "2026-09-30"
version: "1.6"
status: "current"
supersedes: null
---

# MFA Exception Register

## Active exceptions

Register custodian: Isabel Knight (isabel.knight), Security. Approving authority: Thomas Price (thomas.price). The table lists the complete set of active exceptions following the quarterly review on 2026-09-30. There are two active entries. Each permits the named account to sign in without MFA for the approved reason; neither entry grants additional system access.

| Person | Username | Department | Reason | Approver | Date granted | Review date |
|---|---|---|---|---|---|---|
| Daniel Hughes (daniel.hughes) | daniel.hughes | Engineering | Works on a lab workstation where the authenticator app cannot be installed | Thomas Price | 2026-04-14 | 2026-12-31 |
| Amelia Ward (amelia.ward) | amelia.ward | IT | Holds the emergency administrator role for the identity provider, so she can recover access if the MFA service fails | Thomas Price | 2026-03-02 | 2026-12-31 |

## Quarterly review note

The last quarterly review was completed on 2026-09-30. Thomas Price confirmed that both recorded needs still apply. The lab restriction remains unresolved, and the emergency administrator role still requires a route for recovering access during an MFA service failure. Both approvals stand until the end of 2026 and must be reconsidered by 2026-12-31.

Security checks whether each reason remains necessary, whether a workable MFA method is available and whether the named person still holds the relevant duties. A previous approval is not an automatic extension. A change in need must be reported immediately rather than held until the next scheduled review.

## Use of the register

When checking a sign-in, match the username and date to the entry. Do not assume that everyone in the same department has the same exception. Record whether MFA was completed separately from whether an exception existed. The register establishes approval context; it does not establish who performed a particular sign-in.

Any amendment requires Thomas Price's approval and a recorded review date. IT confirms implementation to Security. Routine recovery problems should first follow the authenticator recovery-code and helpdesk process.
