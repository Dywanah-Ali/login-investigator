"""The shared filter parameters of the dashboard endpoints, checked at the boundary before the core
is called. All optional; missing means "all". The core resolves the dates into a window.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Literal

import pandas as pd
from fastapi import Query

from api.errors import FILTER_MESSAGES, ApiError
from login_investigator.dashboard import date_window
from login_investigator.search import filter_logins

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass(frozen=True)
class Filters:
    start: datetime | None
    end: datetime | None
    outcome: str | None
    country: str | None
    user: str | None

    def rows(self, frame: pd.DataFrame) -> pd.DataFrame:
        """The log rows these filters keep, in time order, from the core's one search."""
        return filter_logins(frame, user=self.user, start=self.start, end=self.end,
                             outcome=self.outcome, country=self.country)


def _given(value: str | None) -> str | None:
    """An empty box in the toolbar means "all", as a missing parameter does."""
    if value is None or not value.strip():
        return None
    return value


def _date(value: str | None, name: str) -> date | None:
    """A plain YYYY-MM-DD date, and nothing a lenient parser would also take: a number read as a
    Unix time, or a date with a time, would quietly filter the wrong days (bug log B-002)."""
    if value is None:
        return None
    try:
        if not _DATE.fullmatch(value):
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        raise ApiError(422, "invalid_filter", FILTER_MESSAGES[name]) from None


def filters(
    from_: Annotated[str | None, Query(alias="from")] = None,
    to: str | None = None,
    outcome: Literal["success", "failure"] | None = None,
    country: str | None = None,
    user: str | None = None,
) -> Filters:
    """A route's dependency: the shared filters, read from the query string."""
    first, last = _date(from_, "from"), _date(to, "to")
    if first is not None and last is not None and first > last:
        raise ApiError(422, "invalid_filter", "from is after to.")
    start, end = date_window(first, last)
    return Filters(start=start, end=end, outcome=outcome, country=_given(country),
                   user=_given(user))
