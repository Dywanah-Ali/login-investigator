"""The default severity of each rule: how urgently to review its pattern (ticket 26).

A fixed project policy approved by the author (P-044), not an industry score, a confidence, or a
verdict that an account was taken over. It never rises because findings overlap, and no language
model assigns it. The agent never sees it, so the Investigation report keeps its own assessment.
"""

from dataclasses import dataclass
from typing import Literal

from login_investigator.rules import (
    BRUTE_FORCE,
    NEW_COUNTRY,
    PASSWORD_SPRAYING,
    SUCCESS_AFTER_FAILURES,
)

Level = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class RuleSeverity:
    level: Level
    reason: str  # one sentence shown with the badge


RULE_SEVERITY: dict[str, RuleSeverity] = {
    BRUTE_FORCE: RuleSeverity(
        "medium",
        "Repeated failures on one account need review. This finding alone does not establish "
        "whether related sign-ins succeeded.",
    ),
    PASSWORD_SPRAYING: RuleSeverity(
        "medium",
        "Failures across many accounts suggest an attempt against several accounts. The log "
        "cannot verify that the same password was tried.",
    ),
    SUCCESS_AFTER_FAILURES: RuleSeverity(
        "high",
        "A successful sign-in follows many failures on the same account and IP address. Check "
        "urgently whether it was authorized.",
    ),
    NEW_COUNTRY: RuleSeverity(
        "low",
        "An unfamiliar country is a useful lead. Travel, network routing, or an incomplete "
        "history may explain it.",
    ),
}

# How the table's level differs from an Investigation report's (Option A, P-114).
SEVERITY_NOTE = (
    "Rule default. This is how urgently to review this pattern. An investigation report weighs "
    "all the evidence and can rate the case higher or lower."
)
