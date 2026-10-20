"""The dashboard endpoints: dataset facts, the rules guide, the Overview, Alerts and Explorer. Each validates input,
calls the core and shapes the reply with only the fields the contract lists.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.filters import Filters, alerts_rule, explorer_ip, filters
from api.services import Dataset, dataset
from login_investigator.dashboard import alerts_for_view
from login_investigator.loader import TIMESTAMP_FORMAT, to_records
from login_investigator.rules import GENERAL_ASSUMPTIONS, RULE_GUIDE, RuleGuide
from login_investigator.severity import RULE_SEVERITY, SEVERITY_NOTE
from login_investigator.search import export_csv, summarize
from login_investigator.stats import hourly_counts, top_failed_ips

router = APIRouter()

# What a route declares to receive the loaded dataset, or the filters read from the query string.
LoadedDataset = Annotated[Dataset, Depends(dataset)]
QueryFilters = Annotated[Filters, Depends(filters)]

# The three figures the Overview's tiles show. The search summary holds more, but only what the
# screen needs leaves the server (author's ruling, ticket 13).
SUMMARY_FIELDS = ("total", "failures", "distinct_users")
EXPLORER_SUMMARY_FIELDS = ("total", "successes", "failures", "distinct_users", "distinct_ips")


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
def get_alerts(data: LoadedDataset, chosen: QueryFilters,
               rule: Annotated[str | None, Depends(alerts_rule)]) -> dict:
    # The core's finding dictionary unchanged, evidence included, so the side panel makes no
    # second request. The core sorts it newest first.
    rows = chosen.rows(data.frame)
    found = alerts_for_view(data.findings, rows, rule=rule)
    return {"alerts": [finding.to_dict() for finding in found]}


@router.get("/rules")
def get_rules() -> dict:
    return {
        "rules": [_rule_entry(guide) for guide in RULE_GUIDE],
        "general_assumptions": list(GENERAL_ASSUMPTIONS),
        "severity_note": SEVERITY_NOTE,
    }


def _rule_entry(guide: RuleGuide) -> dict:
    # Each rule travels with its default severity, so the screen looks both up by rule key.
    policy = RULE_SEVERITY[guide.rule]
    return {**asdict(guide), "severity": policy.level, "severity_reason": policy.reason}


# Explorer and CSV share this dependency so filters and row order cannot drift apart.
def explorer_rows(data: LoadedDataset, chosen: QueryFilters,
                  ip: Annotated[str | None, Depends(explorer_ip)]) -> pd.DataFrame:
    return chosen.rows(data.frame, ip=ip).iloc[::-1]


ExplorerRows = Annotated[pd.DataFrame, Depends(explorer_rows)]


@router.get("/explorer")
def get_explorer(rows: ExplorerRows) -> dict:
    summary = summarize(rows.iloc[::-1]).to_dict()
    return {"summary": {field: summary[field] for field in EXPLORER_SUMMARY_FIELDS},
            "rows": to_records(rows)}


@router.get("/explorer.csv")
def get_explorer_csv(rows: ExplorerRows) -> Response:
    return Response(export_csv(rows), media_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="login-investigator-rows.csv"'})
