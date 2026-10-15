"""The dashboard endpoints: dataset facts, the rules guide, the Overview and Alerts. Each validates input,
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

# The three figures the Overview's tiles show. The search summary holds more, but only what the
# screen needs leaves the server (author's ruling, ticket 13).
SUMMARY_FIELDS = ("total", "failures", "distinct_users")


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


@router.get("/alerts")
def get_alerts(data: LoadedDataset, chosen: QueryFilters) -> dict:
    # The core's finding dictionary unchanged, evidence included, so the side panel makes no
    # second request. The core sorts it newest first.
    rows = chosen.rows(data.frame)
    return {"alerts": [finding.to_dict() for finding in alerts_for_view(data.findings, rows)]}


@router.get("/rules")
def get_rules() -> dict:
    return {
        "rules": [asdict(guide) for guide in RULE_GUIDE],
        "general_assumptions": list(GENERAL_ASSUMPTIONS),
    }
