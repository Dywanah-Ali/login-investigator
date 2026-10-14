"""The dashboard endpoints, called from outside through FastAPI's test client (ticket 12). Shapes come
from docs/api-contract.md. Expected values come from evals/ground_truth.json or are written out by
hand, never recomputed the way the code does.
"""

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    """One server for the module, on the real log, with its memory in a temporary folder."""
    settings = Settings.from_env({"LI_MEMORY_PATH": str(tmp_path_factory.mktemp("memory") / "m.sqlite")})
    with TestClient(create_app(settings)) as client:
        yield client


# --- Dataset facts -------------------------------------------------------------------------------

def test_dataset_facts_match_the_ground_truth(client, truth, s):
    """Adapted from v1's "every screen loads with the synthetic label and capture date". The
    dates, countries and user count are pinned from the seeded log, as in test_dashboard.py."""
    reply = client.get("/api/dataset")
    assert reply.status_code == 200
    body = reply.json()
    assert set(body) == {"captured_at", "label", "first_date", "last_date", "countries", "users",
                         "row_count"}
    assert body["captured_at"] == truth["captured_at"]
    assert body["label"] == "Synthetic data"
    assert body["first_date"] == "2026-10-01"
    assert body["last_date"] == "2026-10-08"
    assert body["countries"] == ["GB", "NL", "RO", "RU", "US"]
    assert len(body["users"]) == 57
    assert body["users"] == sorted(body["users"])
    assert {s["S1"]["target_user"], s["S4"]["user"]} <= set(body["users"])
    assert body["row_count"] == truth["row_count"]


# --- Rules guide ---------------------------------------------------------------------------------

def test_the_rules_guide_names_every_rule_with_its_title_and_reasons(client, s):
    """The rule keys are the ground truth's scenario types; the titles are v1's, written out."""
    reply = client.get("/api/rules")
    assert reply.status_code == 200
    body = reply.json()
    assert set(body) == {"rules", "general_assumptions"}
    assert [(r["rule"], r["title"]) for r in body["rules"]] == [
        (s["S1"]["type"], "Brute force"),
        (s["S2"]["type"], "Password spraying"),
        (s["S3"]["type"], "Success after repeated failures"),
        (s["S4"]["type"], "Sign-in from a new country"),
    ]
    for rule in body["rules"]:
        assert set(rule) == {"rule", "title", "fires_when", "assumption"}
        assert rule["fires_when"] and rule["assumption"]
    assert len(body["general_assumptions"]) == 4
    assert all(body["general_assumptions"])


# --- Overview ------------------------------------------------------------------------------------

SUMMARY_FIELDS = {"total", "successes", "failures", "distinct_users", "distinct_ips",
                  "distinct_countries", "first_seen", "last_seen"}


def overview(client, **filters):
    reply = client.get("/api/overview", params=filters)
    assert reply.status_code == 200, reply.text
    return reply.json()


def test_the_overview_of_the_whole_log_has_the_contract_shape_and_nothing_more(client, truth, s):
    """Adapted from v1's "overview counts match the core". No `sample` and no `truncated`: those
    are for the agent only."""
    body = overview(client)
    assert set(body) == {"summary", "alert_count", "hourly", "top_failed_ips"}
    assert set(body["summary"]) == SUMMARY_FIELDS
    assert body["summary"]["total"] == truth["row_count"]
    assert body["summary"]["successes"] + body["summary"]["failures"] == truth["row_count"]
    assert body["alert_count"] == 5  # S1 to S4, plus the new-country alert of S3's sign-in
    assert body["top_failed_ips"][:2] == [
        {"source_ip": s["S1"]["attacker_ip"], "failures": s["S1"]["failures"], "accounts": 1},
        {"source_ip": s["S2"]["attacker_ip"], "failures": s["S2"]["attempts"],
         "accounts": s["S2"]["accounts_tried"]},
    ]
    assert len(body["top_failed_ips"]) == 10


def test_the_hourly_counts_are_whole_hours_that_add_up_to_the_total(client, truth):
    hourly = overview(client)["hourly"]
    assert all(set(h) == {"hour", "outcome", "events"} for h in hourly)
    assert all(h["hour"].endswith(":00:00Z") for h in hourly)
    assert {h["outcome"] for h in hourly} == {"success", "failure"}
    assert sum(h["events"] for h in hourly) == truth["row_count"]


def test_a_filter_changes_every_part_of_the_overview_consistently(client, s):
    """Adapted from v1's "a filter change updates every screen consistently". S2 is the only
    activity from Romania, and its country matches without regard to case, as the core does."""
    body = overview(client, country="ro")
    assert body["summary"]["total"] == s["S2"]["attempts"]
    assert body["summary"]["successes"] == s["S2"]["successes"]
    assert body["summary"]["first_seen"] == s["S2"]["first_seen"]
    assert body["summary"]["last_seen"] == s["S2"]["last_seen"]
    assert sum(h["events"] for h in body["hourly"]) == s["S2"]["attempts"]
    assert [ip["source_ip"] for ip in body["top_failed_ips"]] == [s["S2"]["attacker_ip"]]
    assert body["alert_count"] == 1


def test_a_reset_restores_the_whole_log(client, truth):
    """Adapted from v1's "reset restores the whole log": the server keeps no filter between calls."""
    assert overview(client, country="ro", outcome="failure")["summary"]["total"] < truth["row_count"]
    assert overview(client)["summary"]["total"] == truth["row_count"]


def test_the_date_and_user_filters_reach_the_alert_count(client, s):
    """Pinned in test_dashboard.py: S4's user has one alert; 6 October holds S2 and S4."""
    assert overview(client, user=s["S4"]["user"])["alert_count"] == 1
    assert overview(client, **{"from": "2026-10-06"})["alert_count"] == 2
    assert overview(client, **{"from": "2026-10-06", "to": "2026-10-06"})["alert_count"] == 2


def test_an_outcome_filter_keeps_only_that_outcome(client):
    summary = overview(client, outcome="failure")["summary"]
    assert summary["successes"] == 0
    assert summary["failures"] == summary["total"] > 0


def test_an_empty_view_is_not_an_error(client, s):
    """Adapted from v1's "an empty filter shows a clear message": the spraying attacker's unknown
    usernames never signed in."""
    body = overview(client, user=s["S2"]["unknown_usernames"][0], outcome="success")
    assert body == {
        "summary": {"total": 0, "successes": 0, "failures": 0, "distinct_users": 0,
                    "distinct_ips": 0, "distinct_countries": 0,
                    "first_seen": None, "last_seen": None},
        "alert_count": 0,
        "hourly": [],
        "top_failed_ips": [],
    }


# --- Filter validation ---------------------------------------------------------------------------

# Looks like an attack, so an echo of it would be easy to spot and harmful if it happened.
HOSTILE = "<script>alert(1)</script>"


@pytest.mark.parametrize(("params", "message"), [
    ({"from": HOSTILE}, "from is not a date (YYYY-MM-DD)."),
    ({"to": HOSTILE}, "to is not a date (YYYY-MM-DD)."),
    ({"from": "2026-02-30"}, "from is not a date (YYYY-MM-DD)."),  # the right form, no such day
    # Forms a lenient parser accepts. A number read as a Unix time would give a confident empty
    # view of 2025 (bug log B-002).
    ({"from": "1759708800"}, "from is not a date (YYYY-MM-DD)."),
    ({"to": "2026-10-06T00:00:00"}, "to is not a date (YYYY-MM-DD)."),
    ({"to": "20261006"}, "to is not a date (YYYY-MM-DD)."),
    ({"from": "2026-10-07", "to": "2026-10-05"}, "from is after to."),
    ({"outcome": HOSTILE}, "outcome must be success or failure."),
])
def test_a_bad_filter_is_refused_naming_the_field_never_the_value(client, params, message):
    reply = client.get("/api/overview", params=params)
    assert reply.status_code == 422
    assert reply.json() == {"error": {"code": "invalid_filter", "message": message}}
    for value in params.values():
        assert value not in reply.text
