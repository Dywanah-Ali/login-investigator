"""What the dashboard screens show, decided here so the API and the screens can never disagree.
v1 kept this logic in its Streamlit layer. Ticket 01 decided to move it into the core; ticket 11
moved it. The agent's tools do not call this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

import pandas as pd

from login_investigator.generator import CAPTURED_AT
from login_investigator.rules import Finding, findings_matching

DATA_LABEL = "Synthetic data"


@dataclass(frozen=True)
class DatasetFacts:
    """What the shell and the filter pickers need to know about the loaded log."""
    captured_at: datetime  # UTC; the app treats this as "today"
    label: str
    first_date: date
    last_date: date
    countries: tuple[str, ...]  # sorted, distinct
    users: tuple[str, ...]  # sorted, distinct, as they appear in the log
    row_count: int


def dataset_facts(df: pd.DataFrame) -> DatasetFacts:
    """The facts the frontend must never hard-code: capture time, label, date bounds, the
    pickers' values and the row count. `df` is the whole loaded log."""
    times = df["timestamp_utc"]
    return DatasetFacts(
        captured_at=CAPTURED_AT,
        label=DATA_LABEL,
        first_date=times.min().date(),
        last_date=times.max().date(),
        countries=tuple(sorted(df["country"].unique())),
        users=tuple(sorted(df["username"].unique())),
        row_count=len(df),
    )


def alerts_for_view(
    findings: list[Finding], rows: pd.DataFrame, rule: str | None = None
) -> list[Finding]:
    """The alerts a dashboard view shows, newest first by last seen, then by rule.

    `findings` come from the rules run once on the whole log, since the rules need each user's full
    history. A finding is kept when at least one of its events is among `rows`, so every filter
    counts. This is not the agent's matching, which keeps findings overlapping a time window.
    `rule`, when given, keeps only that rule's findings (ticket 26).
    """
    kept = findings_matching(findings, rows)
    if rule is not None:
        kept = [finding for finding in kept if finding.rule == rule]
    return sorted(kept, key=lambda f: (f.last_seen, f.rule), reverse=True)


def date_window(first: date | None, last: date | None) -> tuple[datetime | None, datetime | None]:
    """Turn the filter's plain dates into the half-open UTC window [start, end) the search takes.

    Both days are included, so the end is the day after `last`. `first` alone is that one day, as
    v1's picker did. `last` alone runs from the start of the log. No dates means the whole log.
    """
    if first is not None and last is None:
        last = first
    start = None if first is None else _midnight_utc(first)
    end = None if last is None else _midnight_utc(last) + timedelta(days=1)
    return start, end


def _midnight_utc(day: date) -> datetime:
    return datetime.combine(day, time(), tzinfo=timezone.utc)
