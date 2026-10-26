# Default dataset

Synthetic authentication data generated with seed `20261008`. The capture window ends at
`2026-10-08T09:00:00Z`.

- `logins.csv` holds 1,948 sign-ins, S1 to S6, the three benign look-alikes and 44 UK employee
  VPN sign-ins. The four unchanged rules produce 10 findings. Maya Patel's ordinary activity
  during 2–4 October is located in Germany to agree with her approved travel. The original
  S1 to S5 event fields are preserved. The laptop replacement keeps both devices in the register
  so earlier events still resolve correctly.
- The last two log columns are `device_id` (empty for unregistered attacker machines and personal
  phones) and `mfa_result` (`pass`, `fail`, `none` for not prompted, `denied` reserved and unused).
  The API and the agent's existing tools return only the original seven fields.
- `ground_truth.json` is the Port's answer key in its original shape. Its row count reflects the
  additional activity; its original story entries are unchanged.
- `truth.json` is the knowledge-base answer key. It holds the stories, the benign verdicts and
  planned clearing-document IDs, the planted S6 groups/assets/paths and VPN peers, the exception
  list and four deliberately absent topics. It is evaluation data, never investigator context.
  S4 remains suspicious but unresolved: the source country and an authentication pass establish
  neither Olivia's physical location nor authorisation, compromise or an attack mechanism.
- `org/` holds one CSV per table: `people`, `groups`, `memberships`, `assets`, `grants`, `devices`,
  `device_assignments` and `networks`. IDs are made from content and remain stable across rebuilds.
  There are 50 people, 51 laptops (one historical replacement) and two shared machines.
- S6's saved IP reputation response lives at `backend/data/ip_reputation/45.148.10.80.json`.
  It is a real AbuseIPDB response saved during T12, used offline by the existing reputation tool.

Regenerate every generated file from `backend/` with:

```bash
uv run python -m login_investigator.generator
```

Planned own-document IDs already referenced by the key are `reg-mfa-exceptions`,
`run-password-spray-response`, `run-compromised-account-response`, `rec-approved-travel`,
`rec-helpdesk-reset` and `rec-laptop-handover`. Ticket 15 must use these IDs when specifying the
27-document corpus; the documents are delivered in ticket 16. These are document IDs, not chunk
IDs, which will be derived during ingestion. No document governs the backup server; membership
and grants remain structured organisation facts.

The independent recomputation of S6's radius belongs to ticket 19. The `used address` row filter
is fixed in ticket 18 and recorded beside the radius then. The planted VPN rows are all successful,
so either all-sign-in or success-only construction agrees on their peers.
Ticket 14 records the ATT&CK version when those pages are added.
