# Default dataset

Synthetic authentication data generated with seed `20261008`.

- `logins.csv` holds the Port's existing sign-ins and five planted stories.
- `ground_truth.json` is the Port's existing answer key, with its original shape and contents.

Regenerate both files from `backend/` with:

```bash
uv run python -m login_investigator.generator
```

Later knowledge-base tickets add organisation tables, `truth.json` and the document corpus here.
Ticket 14 records the ATT&CK version when those pages are added.
