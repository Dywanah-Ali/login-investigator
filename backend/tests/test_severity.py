"""The default severity of each rule (ticket 26). Expected values are the author's approved policy
(P-044) written out by hand, never read back from the module under test.
"""

from login_investigator.rules import RULE_GUIDE
from login_investigator.severity import RULE_SEVERITY, SEVERITY_NOTE


def test_each_rule_has_its_approved_default():
    assert {rule: policy.level for rule, policy in RULE_SEVERITY.items()} == {
        "brute_force": "medium",
        "password_spraying": "medium",
        "success_after_failures": "high",
        "new_country": "low",
    }


def test_the_policy_covers_exactly_the_rules_that_exist():
    assert set(RULE_SEVERITY) == {guide.rule for guide in RULE_GUIDE}


def test_a_failure_only_rule_never_claims_that_nothing_succeeded():
    for rule in ("brute_force", "password_spraying"):
        reason = RULE_SEVERITY[rule].reason.lower()
        assert "no sign-in succeeded" not in reason and "failed attack" not in reason
    assert "does not establish whether related sign-ins succeeded" in (
        RULE_SEVERITY["brute_force"].reason)


def test_high_asks_for_an_urgent_check_and_never_claims_a_compromise():
    reason = RULE_SEVERITY["success_after_failures"].reason
    assert "Check urgently whether it was authorized." in reason
    for policy in RULE_SEVERITY.values():
        assert "compromise" not in policy.reason.lower()
        assert "confirmed" not in policy.reason.lower()


def test_the_note_says_a_report_can_rate_the_case_differently():
    """Option A, P-114: the table's level is the rule's default, not the Investigation's."""
    assert SEVERITY_NOTE.startswith("Rule default.")
    assert "can rate the case higher or lower" in SEVERITY_NOTE
