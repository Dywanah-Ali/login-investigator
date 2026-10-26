# Default dataset

Synthetic authentication data generated with seed `20261008`.

- `logins.csv` holds the Port's existing sign-ins and five planted stories. Its last two columns
  come from the knowledge base: `device_id` (empty for a machine the register does not hold: the
  attackers' machines and personal phones) and `mfa_result` (`pass`, `fail`, `none` for not
  prompted, `denied` reserved and unused). The API and the agent's tools never return these two.
- `ground_truth.json` is the Port's existing answer key, with its original shape and contents.
- `org/` holds the organisation drawn around the 50 users, one CSV per table: `people`, `groups`,
  `memberships`, `assets`, `grants`, `devices`, `device_assignments` and `networks`. Every record's
  first column is its ID, made from its content, so it is the same on every run.

Regenerate every file from `backend/` with:

```bash
uv run python -m login_investigator.generator
```

Later knowledge-base tickets add `truth.json` and the document corpus here.
Ticket 14 records the ATT&CK version when those pages are added.
