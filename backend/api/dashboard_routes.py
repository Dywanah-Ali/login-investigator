"""The dashboard endpoints: dataset facts, the rules guide and the Overview. Each validates input,
calls the core and shapes the reply with only the fields the contract lists.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends

from api.filters import Filters, filters
from api.services import Dataset, dataset
from login_investigator.dashboard import alerts_for_view
from login_investigator.loader import TIMESTAMP_FORMAT
from login_investigator.rules import GENERAL_ASSUMPTIONS, RULE_GUIDE
from login_investigator.search import summarize
from login_investigator.stats import hourly_counts, top_failed_ips

router = APIRouter()

# What a route declares to receive the loaded dataset, or the filters read from the query string.
LoadedDataset = Annotated[Dataset, Depends(dataset)]
QueryFilters = Annotated[Filters, Depends(filters)]

# The search summary's counts. Its `sample`, `sample_shown` and `truncated` are for the agent only.
SUMMARY_FIELDS = ("total", "successes", "failures", "distinct_users", "distinct_ips",
                  "distinct_countries", "first_seen", "last_seen")


@router.get("/dataset")
def get_dataset(data: LoadedDataset) -> dict:
    facts = data.facts
    return {
        "captured_at": facts.captured_at.strftime(TIMESTAMP_FORMAT),
        "label": facts.label,
        "first_date": facts.first_date.isoformat(),
        "last_date": facts.last_date.isoformat(),
        "countries": list(facts.countries),
        "users": list(facts.users),
        "row_count": facts.row_count,
    }


@router.get("/overview")
def get_overview(data: LoadedDataset, chosen: QueryFilters) -> dict:
    rows = chosen.rows(data.frame)
    summary = summarize(rows).to_dict()
    return {
        "summary": {field: summary[field] for field in SUMMARY_FIELDS},
        "alert_count": len(alerts_for_view(data.findings, rows)),
        "hourly": [
            {"hour": row["hour"].strftime(TIMESTAMP_FORMAT), "outcome": row["outcome"],
             "events": int(row["events"])}
            for row in hourly_counts(rows).to_dict("records")
        ],
        "top_failed_ips": [
            {"source_ip": row["source_ip"], "failures": int(row["failures"]),
             "accounts": int(row["accounts"])}
            for row in top_failed_ips(rows).to_dict("records")
        ],
    }


@router.get("/rules")
def get_rules() -> dict:
    return {
        "rules": [asdict(guide) for guide in RULE_GUIDE],
        "general_assumptions": list(GENERAL_ASSUMPTIONS),
    }
