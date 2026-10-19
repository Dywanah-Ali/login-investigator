"""Validate timeline sort keys for new reports without rewriting historical reports."""

from datetime import datetime, timezone


def timeline_instant(value: str) -> datetime:
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("Report timeline timestamps must include a timezone")
    return instant.astimezone(timezone.utc)
