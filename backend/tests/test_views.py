"""The logic v1 kept in its Streamlit screens, now in the core so the API and the screens can
never disagree (decided in ticket 01, moved in ticket 11). Adapted from v1's tests/test_app.py. Expected values
come from evals/ground_truth.json or are written out by hand, never recomputed the way the code does.
"""

from datetime import date

import pandas as pd
import pytest

from login_investigator.search import filter_logins
from login_investigator.rules import detect_all
from login_investigator.views import alerts_for_view, dataset_facts, date_window

UTC = "UTC"


# --- Date resolution -----------------------------------------------------------------------------

def test_a_date_range_becomes_a_half_open_window_ending_the_day_after():
    assert date_window(date(2026, 10, 3), date(2026, 10, 5)) == (
        pd.Timestamp("2026-10-03T00:00:00", tz=UTC),
        pd.Timestamp("2026-10-06T00:00:00", tz=UTC),
    )


def test_a_single_date_is_that_one_day():
    one_day = (pd.Timestamp("2026-10-04", tz=UTC), pd.Timestamp("2026-10-05", tz=UTC))
    assert date_window(date(2026, 10, 4), None) == one_day
    assert date_window(date(2026, 10, 4), date(2026, 10, 4)) == one_day


def test_an_end_date_alone_runs_from_the_start_of_the_log():
    assert date_window(None, date(2026, 10, 4)) == (None, pd.Timestamp("2026-10-05", tz=UTC))


def test_no_dates_means_the_whole_log(log, truth):
    """Adapted from v1's "reset restores the whole log"."""
    start, end = date_window(None, None)
    assert len(filter_logins(log, start=start, end=end)) == truth["row_count"]


# --- Dataset facts -------------------------------------------------------------------------------

def test_dataset_facts_match_the_ground_truth(log, truth):
    """Adapted from v1's "every screen loads with the synthetic label and capture date"."""
    facts = dataset_facts(log)
    assert facts.captured_at == pd.Timestamp(truth["captured_at"])
    assert facts.label == "Synthetic data"
    assert facts.first_date == date(2026, 10, 1)
    assert facts.last_date == date(2026, 10, 8)
    assert facts.row_count == truth["row_count"]


def test_the_pickers_get_every_country_and_user_once_in_order(log, s):
    """The country list and the user count are pinned from the seeded log (seed 20261008)."""
    facts = dataset_facts(log)
    assert facts.countries == ("GB", "NL", "RO", "RU", "US")
    assert list(facts.users) == sorted(facts.users)
    assert len(facts.users) == len(set(facts.users)) == 57
    assert {s["S1"]["target_user"], s["S4"]["user"], *s["S2"]["unknown_usernames"]} <= set(
        facts.users)


# --- Alerts for a view ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def findings(log):
    """The rules run once on the whole log, as the API does at startup."""
    return detect_all(log)


def rule_and_ip(alerts):
    return [(a.rule, a.ips[0]) for a in alerts]


def test_the_whole_log_lists_every_alert_newest_first(log, s, findings):
    """Adapted from v1's "overview counts match the core", "S1 to S4 appear on the alerts screen"
    and "alerts are listed newest first". Order written out from the ground-truth times. S3 and
    the second new-country alert share a last-seen time; the rule breaks the tie, newest first."""
    attacker = s["S1"]["attacker_ip"]
    # Reversed, so the order cannot come from the order the rules happen to return.
    assert rule_and_ip(alerts_for_view(findings[::-1], log)) == [
        ("success_after_failures", s["S3"]["attacker_ip"]),  # S3, 8 Oct 02:32:20
        ("new_country", attacker),                           # same sign-in, 8 Oct 02:32:20
        ("brute_force", attacker),                           # S1, 8 Oct 02:31:44
        ("new_country", s["S4"]["ip"]),                      # S4, 6 Oct 13:47:12
        ("password_spraying", s["S2"]["attacker_ip"]),       # S2, 6 Oct 03:17:29
    ]


def test_a_user_filter_keeps_only_that_users_alerts(log, s, findings):
    """Adapted from v1's "a filter change updates every screen consistently"."""
    rows = filter_logins(log, user=s["S4"]["user"])
    assert rule_and_ip(alerts_for_view(findings, rows)) == [("new_country", s["S4"]["ip"])]


def test_a_date_filter_keeps_alerts_with_an_event_on_those_days(log, s, findings):
    start, end = date_window(date(2026, 10, 6), None)
    rows = filter_logins(log, start=start, end=end)
    assert rule_and_ip(alerts_for_view(findings, rows)) == [
        ("new_country", s["S4"]["ip"]),
        ("password_spraying", s["S2"]["attacker_ip"]),
    ]


def test_an_empty_view_has_no_alerts(log, s, findings):
    """Adapted from v1's "an empty filter shows a clear message": an unknown username the
    spraying attacker tried never succeeded."""
    rows = filter_logins(log, user=s["S2"]["unknown_usernames"][0], outcome="success")
    assert rows.empty
    assert alerts_for_view(findings, rows) == []
