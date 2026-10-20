"""The dashboard endpoints, called from outside through FastAPI's test client (ticket 12). Shapes come
from docs/api-contract.md. Expected values come from evals/ground_truth.json or are written out by
hand, never recomputed the way the code does.
"""

import csv
import io

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
    # Only what the screens show leaves the server (author's ruling, ticket 13): no row count.
    assert set(body) == {"captured_at", "label", "first_date", "last_date", "countries", "users"}
    assert body["captured_at"] == truth["captured_at"]
    assert body["label"] == "Synthetic data"
    assert body["first_date"] == "2026-10-01"
    assert body["last_date"] == "2026-10-08"
    assert body["countries"] == ["GB", "NL", "RO", "RU", "US"]
    assert len(body["users"]) == 57
    assert body["users"] == sorted(body["users"])
    assert {s["S1"]["target_user"], s["S4"]["user"]} <= set(body["users"])


# --- Rules guide ---------------------------------------------------------------------------------

def test_the_rules_guide_names_every_rule_with_its_title_and_reasons(client, s):
    """The rule keys are the ground truth's scenario types; the titles are v1's, written out."""
    reply = client.get("/api/rules")
    assert reply.status_code == 200
    body = reply.json()
    assert set(body) == {"rules", "general_assumptions", "severity_note"}
    # The default severities are the author's approved policy (P-044, ticket 26).
    assert [(r["rule"], r["title"], r["severity"]) for r in body["rules"]] == [
        (s["S1"]["type"], "Brute force", "medium"),
        (s["S2"]["type"], "Password spraying", "medium"),
        (s["S3"]["type"], "Success after repeated failures", "high"),
        (s["S4"]["type"], "Sign-in from a new country", "low"),
    ]
    for rule in body["rules"]:
        assert set(rule) == {"rule", "title", "fires_when", "assumption", "severity",
                             "severity_reason"}
        assert rule["fires_when"] and rule["assumption"] and rule["severity_reason"]
    assert len(body["general_assumptions"]) == 4
    assert all(body["general_assumptions"])
    assert body["severity_note"].startswith("Rule default.")


# --- Overview ------------------------------------------------------------------------------------

# The three figures the Overview's tiles show (author's ruling, ticket 13).
SUMMARY_FIELDS = {"total", "failures", "distinct_users"}


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
    assert 0 < body["summary"]["failures"] < truth["row_count"]
    assert body["summary"]["distinct_users"] == 57
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
    assert body["summary"]["failures"] == s["S2"]["attempts"] - s["S2"]["successes"]
    assert sum(h["events"] for h in body["hourly"]) == s["S2"]["attempts"]
    hours = [h["hour"] for h in body["hourly"]]
    # The view's first and last hours are the hours of S2's first and last attempts.
    assert min(hours) == s["S2"]["first_seen"][:13] + ":00:00Z"
    assert max(hours) == s["S2"]["last_seen"][:13] + ":00:00Z"
    assert [ip["source_ip"] for ip in body["top_failed_ips"]] == [s["S2"]["attacker_ip"]]
    assert body["alert_count"] == 1


def test_a_reset_restores_the_whole_log(client, truth):
    """Adapted from v1's "reset restores the whole log": the server keeps no filter between calls."""
    assert overview(client, country="ro", outcome="failure")["summary"]["total"] < truth["row_count"]
    assert overview(client)["summary"]["total"] == truth["row_count"]


def test_an_empty_box_means_all_as_a_missing_one_does(client):
    """The author's ruling, 14 Oct (ticket 12): one rule for every filter, dates included."""
    empty = {"from": "", "to": " ", "outcome": "", "country": "", "user": ""}
    assert overview(client, **empty) == overview(client)


def test_the_date_and_user_filters_reach_the_alert_count(client, s):
    """Pinned in test_dashboard.py: S4's user has one alert; 6 October holds S2 and S4."""
    assert overview(client, user=s["S4"]["user"])["alert_count"] == 1
    assert overview(client, **{"from": "2026-10-06"})["alert_count"] == 2
    assert overview(client, **{"from": "2026-10-06", "to": "2026-10-06"})["alert_count"] == 2


def test_an_outcome_filter_keeps_only_that_outcome(client):
    body = overview(client, outcome="failure")
    assert body["summary"]["failures"] == body["summary"]["total"] > 0
    assert {h["outcome"] for h in body["hourly"]} == {"failure"}


def test_an_empty_view_is_not_an_error(client, s):
    """Adapted from v1's "an empty filter shows a clear message": the spraying attacker's unknown
    usernames never signed in."""
    body = overview(client, user=s["S2"]["unknown_usernames"][0], outcome="success")
    assert body == {
        "summary": {"total": 0, "failures": 0, "distinct_users": 0},
        "alert_count": 0,
        "hourly": [],
        "top_failed_ips": [],
    }


# --- Alerts --------------------------------------------------------------------------------------

# The fields of the core's finding dictionary, which the contract sends unchanged.
ALERT_FIELDS = {"rule", "summary", "ips", "users", "event_count", "failure_count", "success_count",
                "first_seen", "last_seen", "evidence", "evidence_shown"}
LOG_FIELDS = {"timestamp_utc", "username", "source_ip", "country", "outcome", "failure_reason",
              "user_agent"}


def alerts(client, **filters):
    reply = client.get("/api/alerts", params=filters)
    assert reply.status_code == 200, reply.text
    body = reply.json()
    assert set(body) == {"alerts"}
    return body["alerts"]


def test_s1_to_s4_appear_in_alerts_newest_first(client, s):
    """Adapted from v1's "S1 to S4 appear in alerts" and "alerts newest first". The order is
    written out by hand from the ground truth's times: S3's success and its sign-in from a new
    country share the last second, and the core breaks that tie by rule, newest first."""
    found = alerts(client)
    assert [(a["rule"], a["last_seen"]) for a in found] == [
        (s["S3"]["type"], s["S3"]["time"]),
        (s["S4"]["type"], s["S3"]["time"]),  # S3's sign-in is also the user's first from NL
        (s["S1"]["type"], s["S1"]["last_seen"]),
        (s["S4"]["type"], s["S4"]["time"]),
        (s["S2"]["type"], s["S2"]["last_seen"]),
    ]
    brute = found[2]
    assert brute["ips"] == [s["S1"]["attacker_ip"]]
    assert brute["users"] == [s["S1"]["target_user"]]
    assert brute["first_seen"] == s["S1"]["first_seen"]
    assert brute["event_count"] == brute["failure_count"] == s["S1"]["failures"]
    assert found[3]["users"] == [s["S4"]["user"]] and found[3]["ips"] == [s["S4"]["ip"]]
    assert found[4]["ips"] == [s["S2"]["attacker_ip"]]
    assert len(found[4]["users"]) == s["S2"]["accounts_tried"]


def test_every_alert_has_the_contract_shape_with_its_evidence(client):
    """The side panel makes no second request, so the evidence travels with the list: at most 20
    log rows, each with the seven log fields, and the count of rows shown."""
    for alert in alerts(client):
        assert set(alert) == ALERT_FIELDS
        assert 0 < alert["evidence_shown"] == len(alert["evidence"]) <= 20
        assert alert["evidence_shown"] <= alert["event_count"]
        assert all(set(row) == LOG_FIELDS for row in alert["evidence"])
        assert alert["evidence"][0]["timestamp_utc"] == alert["first_seen"]
        assert alert["evidence"][-1]["timestamp_utc"] == alert["last_seen"]


def test_a_cut_alert_shows_its_first_and_last_events(client, s):
    """S1 has 150 events, so its evidence is cut to 20: the first ten and the last ten."""
    brute = next(a for a in alerts(client) if a["rule"] == s["S1"]["type"])
    assert brute["evidence_shown"] == 20 < brute["event_count"]


@pytest.mark.parametrize(("filters", "expected"), [
    # Pinned in test_dashboard.py and by hand from the ground truth, as for the alert count.
    ({"country": "ro"}, ["S2"]),
    ({"from": "2026-10-06", "to": "2026-10-06"}, ["S4", "S2"]),
    ({"user": "OLIVIA.BENNETT"}, ["S4"]),  # usernames match without regard to case
    ({"outcome": "success", "from": "2026-10-08"}, ["S3", "S3-new-country"]),
])
def test_filters_narrow_the_alerts(client, s, filters, expected):
    """Adapted from v1's "a filter change updates every screen consistently": an alert stays when
    at least one of its events is in the view. The success filter keeps S3, whose last event is
    the success, and drops S1, which has none."""
    rules = {"S1": s["S1"]["type"], "S2": s["S2"]["type"], "S3": s["S3"]["type"],
             "S4": s["S4"]["type"], "S3-new-country": s["S4"]["type"]}
    assert [a["rule"] for a in alerts(client, **filters)] == [rules[key] for key in expected]


@pytest.mark.parametrize(("filters", "expected"), [
    # Ticket 26. Pinned by hand from the ground truth, as above.
    ({"rule": "new_country"}, ["S3-new-country", "S4"]),
    ({"rule": "brute_force"}, ["S1"]),
    ({"rule": "new_country", "from": "2026-10-06", "to": "2026-10-06"}, ["S4"]),
    ({"rule": "password_spraying", "country": "ro"}, ["S2"]),
    ({"rule": "brute_force", "outcome": "success"}, []),  # S1 has no success
    ({"rule": "success_after_failures", "user": "OLIVIA.BENNETT"}, []),
    ({"rule": ""}, ["S3", "S3-new-country", "S1", "S4", "S2"]),  # an empty box means all
    ({"rule": "  "}, ["S3", "S3-new-country", "S1", "S4", "S2"]),
])
def test_a_rule_filter_composes_with_the_other_filters(client, s, filters, expected):
    rules = {"S1": s["S1"]["type"], "S2": s["S2"]["type"], "S3": s["S3"]["type"],
             "S4": s["S4"]["type"], "S3-new-country": s["S4"]["type"]}
    assert [a["rule"] for a in alerts(client, **filters)] == [rules[key] for key in expected]


@pytest.mark.parametrize("rule", ["<script>alert(1)</script>", "Brute force", "BRUTE_FORCE",
                                  "brute_force,new_country"])
def test_an_unknown_rule_is_refused_without_echoing_it(client, rule):
    reply = client.get("/api/alerts", params={"rule": rule})
    assert reply.status_code == 422
    assert reply.json() == {"error": {"code": "invalid_filter",
                                      "message": "rule is not a known rule."}}
    assert rule not in reply.text


def test_the_rule_filter_belongs_to_alerts_only(client, s):
    """The Overview ignores it, as it ignores ip, so its alert count stays the view's."""
    whole = client.get("/api/overview").json()
    assert client.get("/api/overview", params={"rule": "brute_force"}).json() == whole


def test_the_alerts_of_an_empty_view_are_an_empty_list(client, s):
    assert alerts(client, user=s["S2"]["unknown_usernames"][0], outcome="success") == []


def test_the_alerts_endpoint_refuses_a_bad_filter_without_echoing_it(client):
    reply = client.get("/api/alerts", params={"outcome": HOSTILE})
    assert reply.status_code == 422
    assert reply.json() == {"error": {"code": "invalid_filter",
                                      "message": "outcome must be success or failure."}}
    assert HOSTILE not in reply.text


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

# --- Explorer ------------------------------------------------------------------------------------

def test_explorer_returns_every_matching_row_newest_first(client, s):
    attack = s["S1"]
    reply = client.get("/api/explorer", params={"ip": attack["attacker_ip"],
                                             "user": attack["target_user"], "outcome": "failure"})
    assert reply.status_code == 200
    body = reply.json()
    assert set(body) == {"summary", "rows"}
    assert len(body["rows"]) == attack["failures"] == 150
    assert all(set(row) == LOG_FIELDS for row in body["rows"])
    assert {row["source_ip"] for row in body["rows"]} == {attack["attacker_ip"]}
    assert {row["username"] for row in body["rows"]} == {attack["target_user"]}
    assert {row["outcome"] for row in body["rows"]} == {"failure"}
    times = [row["timestamp_utc"] for row in body["rows"]]
    assert times == sorted(times, reverse=True)
    assert times[0] == attack["last_seen"]
    assert times[-1] == attack["first_seen"]


def test_explorer_summary_and_empty_view(client, s):
    body = client.get('/api/explorer', params={'ip': s['S1']['attacker_ip']}).json()
    assert body['summary'] == {'total': 151, 'successes': 1, 'failures': 150,
                               'distinct_users': 1, 'distinct_ips': 1}
    assert client.get('/api/explorer', params={'user': 'no-such-user'}).json() == {
        'summary': {'total': 0, 'successes': 0, 'failures': 0, 'distinct_users': 0, 'distinct_ips': 0},
        'rows': [],
    }


@pytest.mark.parametrize('path', ['/api/explorer', '/api/explorer.csv'])
@pytest.mark.parametrize('ip', [HOSTILE, '999.1.2.3', '01.2.3.4', '1', '::1%eth0'])
def test_explorer_refuses_bad_ips_without_echoing(client, path, ip):
    reply = client.get(path, params={'ip': ip})
    assert reply.status_code == 422
    assert reply.json() == {'error': {'code': 'invalid_filter', 'message': 'ip is not a valid IP address.'}}
    assert ip not in reply.text


def test_csv_contains_the_same_filtered_rows_in_the_same_order(client):
    params = {'from': '2026-10-06', 'to': '2026-10-06', 'country': 'ro', 'outcome': 'failure'}
    rows = client.get('/api/explorer', params=params).json()['rows']
    reply = client.get('/api/explorer.csv', params=params)
    assert reply.status_code == 200
    assert reply.headers['content-type'] == 'text/csv; charset=utf-8'
    assert reply.headers['content-disposition'] == 'attachment; filename="login-investigator-rows.csv"'
    assert len(rows) > 0
    assert list(csv.DictReader(io.StringIO(reply.text))) == rows
    empty = client.get('/api/explorer.csv', params={'user': 'no-such-user'})
    assert empty.text == 'timestamp_utc,username,source_ip,country,outcome,failure_reason,user_agent\n'


def test_csv_keeps_formula_protection_at_the_http_boundary(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text('timestamp_utc,username,source_ip,country,outcome,failure_reason,user_agent\n'
                    '2026-10-01T00:00:00Z,=1+1,203.0.113.10,GB,failure,bad_password,+cmd\n')
    settings = Settings.from_env({'LI_LOG_PATH': str(path), 'LI_MEMORY_PATH': str(tmp_path / 'm.sqlite')})
    with TestClient(create_app(settings)) as api:
        raw = api.get('/api/explorer').json()['rows'][0]
        downloaded = list(csv.DictReader(io.StringIO(api.get('/api/explorer.csv').text)))[0]
    assert raw['username'] == '=1+1'
    assert downloaded['username'] == "'=1+1"
    assert downloaded['user_agent'] == "'+cmd"


@pytest.mark.parametrize('ip', ['2001:db8::1', '::1', '::ffff:192.0.2.1', '', '  '])
def test_explorer_accepts_ipv6_and_empty_ip_filters(client, ip):
    assert client.get('/api/explorer', params={'ip': ip}).status_code == 200


# --- Cross-screen Parity (ticket 19) --------------------------------------------------------------

@pytest.mark.parametrize('filters', [
    {'country': 'ro'},
    {'from': '2026-10-06', 'to': '2026-10-06', 'country': 'ro', 'outcome': 'failure'},
])
def test_a_filter_change_updates_every_screen_consistently(client, s, filters):
    """Replay v1's cross-screen case through all three HTTP endpoints on the same server.
    Romania holds only S2; its ground truth pins the counts independently of the API."""
    attack = s['S2']
    expected = attack['attempts'] - (attack['successes'] if filters.get('outcome') else 0)
    summary = overview(client, **filters)
    found = alerts(client, **filters)
    reply = client.get('/api/explorer', params=filters)
    assert reply.status_code == 200
    rows = reply.json()
    assert summary['summary']['total'] == rows['summary']['total'] == len(rows['rows']) == expected
    assert summary['summary']['failures'] == rows['summary']['failures'] == (
        attack['attempts'] - attack['successes'])
    assert sum(hour['events'] for hour in summary['hourly']) == expected
    assert summary['alert_count'] == len(found) == 1
    assert found[0]['rule'] == attack['type']
    assert found[0]['ips'] == [attack['attacker_ip']]
    assert {row['country'] for row in rows['rows']} == {'RO'}
    assert {row['source_ip'] for row in rows['rows']} == {attack['attacker_ip']}
    if filters.get('outcome'):
        assert {row['outcome'] for row in rows['rows']} == {'failure'}


def test_an_empty_filter_returns_clear_empty_data_on_all_three_screens(client, s):
    """The browser supplies the message; the API supplies unambiguous successful empty data."""
    filters = {'user': s['S2']['unknown_usernames'][0], 'outcome': 'success'}
    assert overview(client, **filters) == {
        'summary': {'total': 0, 'failures': 0, 'distinct_users': 0},
        'alert_count': 0, 'hourly': [], 'top_failed_ips': [],
    }
    assert alerts(client, **filters) == []
    reply = client.get('/api/explorer', params=filters)
    assert reply.status_code == 200
    assert reply.json() == {
        'summary': {'total': 0, 'successes': 0, 'failures': 0,
                    'distinct_users': 0, 'distinct_ips': 0},
        'rows': [],
    }


def test_reset_restores_the_whole_log_on_all_three_screens(client, truth):
    """Removing the query restores every screen, including after an empty view.
    Neither another screen nor an earlier request can leave hidden server filter state."""
    paths = ['/api/overview', '/api/alerts', '/api/explorer']
    initial = {}
    for path in paths:
        reply = client.get(path)
        assert reply.status_code == 200
        initial[path] = reply.json()
    for filters in [{'country': 'ro', 'outcome': 'failure'}, {'user': 'no-such-user'}]:
        for path in paths:
            filtered = client.get(path, params=filters)
            assert filtered.status_code == 200
            assert filtered.json() != initial[path]
        for path in paths:
            reset = client.get(path)
            assert reset.status_code == 200
            assert reset.json() == initial[path]
    assert initial['/api/overview']['summary']['total'] == truth['row_count']
    assert initial['/api/explorer']['summary']['total'] == truth['row_count']
    assert len(initial['/api/explorer']['rows']) == truth['row_count']
    assert len(initial['/api/alerts']['alerts']) == 5
