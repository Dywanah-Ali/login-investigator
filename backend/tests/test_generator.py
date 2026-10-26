"""The generator must be repeatable and must plant every scenario exactly as documented."""

import csv
import hashlib
import io
import ipaddress
from collections import Counter

import pytest

from login_investigator import generator as g

ATTACKER_IPS = {g.S1_IP, g.S2_IP, g.S4_IP}
DECOY_IPS = set(g.DECOY_IPS)

# SHA-256 of logins.csv as committed before knowledge-base ticket 11 (commit e57d11d), when the log
# had only the Port's seven columns.
PORT_LOG_SHA256 = "920f501fc32b12ffb94286425909a920aa790926f8186316a78c943a58d389ea"
PORT_COLUMNS = ["timestamp_utc", "username", "source_ip", "country", "outcome",
                "failure_reason", "user_agent"]


@pytest.fixture(scope="module")
def world():
    return g.generate()


@pytest.fixture(scope="module")
def generated(world):
    return world.rows, world.ground_truth


def _written_files(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def test_same_seed_gives_identical_files(tmp_path):
    for run in ("a", "b"):
        g.write(g.generate(), tmp_path / run)
    assert _written_files(tmp_path / "a") == _written_files(tmp_path / "b")


def test_committed_files_match_the_generator(tmp_path, world):
    """Catches a file that was edited by hand or a generator change without regenerating."""
    g.write(world, tmp_path)
    written = _written_files(tmp_path)
    assert "logins.csv" in written and "ground_truth.json" in written
    for name, content in written.items():
        assert (g.DATASET_DIR / name).read_bytes() == content, name


def test_port_rows_keep_their_old_values(world):
    """The Port's columns are byte for byte what they were before the organisation was added."""
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=PORT_COLUMNS, extrasaction="ignore",
                            lineterminator="\n")
    writer.writeheader()
    writer.writerows(world.rows)
    assert hashlib.sha256(out.getvalue().encode("utf-8")).hexdigest() == PORT_LOG_SHA256


def test_rows_are_sorted_and_inside_the_window(generated):
    rows, _ = generated
    times = [r["timestamp_utc"] for r in rows]
    assert times == sorted(times)
    assert times[0] >= g._ts(g.WINDOW_START)
    assert times[-1] < g._ts(g.CAPTURED_AT)


def test_size_is_in_the_planned_range(generated):
    rows, _ = generated
    assert 1500 <= len(rows) <= 2500
    assert len({r["username"] for r in rows if r["source_ip"] not in ATTACKER_IPS}) == 50


def test_s1_brute_force_then_s3_success(generated):
    rows, truth = generated
    s1 = [r for r in rows if r["source_ip"] == g.S1_IP]
    failures = [r for r in s1 if r["outcome"] == "failure"]
    successes = [r for r in s1 if r["outcome"] == "success"]
    assert len(failures) == g.S1_FAILURES
    assert {r["username"] for r in s1} == {g.S1_TARGET}
    assert len(successes) == 1
    assert successes[0]["timestamp_utc"] > failures[-1]["timestamp_utc"]
    # "Last night" relative to the capture date: the night of 7 to 8 October.
    assert failures[0]["timestamp_utc"].startswith("2026-10-08T0")
    assert truth["scenarios"]["S3"]["time"] == successes[0]["timestamp_utc"]


def test_s2_password_spraying(generated):
    rows, truth = generated
    s2 = [r for r in rows if r["source_ip"] == g.S2_IP]
    per_account = Counter(r["username"] for r in s2)
    assert len(per_account) == 35
    assert set(per_account.values()) <= {2, 3}
    assert all(r["outcome"] == "failure" for r in s2)
    unknown = {r["username"] for r in s2 if r["failure_reason"] == "unknown_user"}
    assert unknown == set(g.S2_UNKNOWN_USERNAMES)
    assert truth["scenarios"]["S2"]["accounts_tried"] == 35


def test_s4_new_country(generated):
    rows, _ = generated
    user_rows = [r for r in rows if r["username"] == g.S4_TARGET]
    countries = Counter(r["country"] for r in user_rows)
    assert countries["RU"] == 1
    before = [r for r in user_rows if r["timestamp_utc"] < g._ts(g.S4_TIME)]
    assert before and all(r["country"] == "GB" for r in before)


def test_s5_injection_sits_in_s1_rows(generated):
    rows, truth = generated
    injected = [r for r in rows if "ignore all previous instructions" in r["user_agent"]]
    assert len(injected) == len(g.S5_ROW_POSITIONS)
    assert {r["source_ip"] for r in injected} == {g.S1_IP}
    assert truth["scenarios"]["S5"]["rows"] == len(injected)


def test_normal_users_only_use_reserved_or_decoy_addresses(generated):
    rows, _ = generated
    for r in rows:
        ip = r["source_ip"]
        if ip in ATTACKER_IPS:
            continue
        assert ip in DECOY_IPS or not ipaddress.ip_address(ip).is_global, ip


def test_decoys_appear_as_normal_us_sign_ins(generated):
    rows, _ = generated
    for decoy in DECOY_IPS:
        hits = [r for r in rows if r["source_ip"] == decoy]
        assert hits, f"decoy {decoy} never appears"
        assert {r["country"] for r in hits} == {"US"}
        # Decoys are judged on reputation alone, so they carry no failed sign-ins at all.
        assert all(r["outcome"] == "success" for r in hits)


def test_normal_noise_stays_far_below_attack_patterns(generated):
    """No benign user or address should look like brute force or spraying by accident."""
    rows, _ = generated
    benign_failures = [r for r in rows
                       if r["outcome"] == "failure" and r["source_ip"] not in ATTACKER_IPS]
    per_user_day = Counter((r["username"], r["timestamp_utc"][:10]) for r in benign_failures)
    assert max(per_user_day.values()) <= 4
    users_per_ip_failing = Counter()
    for ip in {r["source_ip"] for r in benign_failures}:
        users_per_ip_failing[ip] = len({r["username"] for r in benign_failures
                                        if r["source_ip"] == ip})
    # The shared offices see typos from many staff, but spread over a whole week.
    home_ips = {ip for ip in users_per_ip_failing if ip.startswith(g.UK_HOME_PREFIX)}
    assert all(users_per_ip_failing[ip] == 1 for ip in home_ips)


# The organisation (knowledge-base ticket 04, decisions 2 to 5). Expected names are T04's.

TABLES = ("people", "groups", "memberships", "assets", "grants", "devices",
          "device_assignments", "networks")
DEPARTMENTS = {"Engineering", "Finance", "HR", "Sales", "Operations", "IT"}
PRIVILEGED = {"IT Admins": "IT", "Finance Approvers": "Finance", "HR Data Owners": "HR"}
# Cross-cutting (T04 d2; author's ruling at ticket 11): each group has one member from outside its
# home department.
OUTSIDER_DEPARTMENT = {"IT Admins": "Engineering", "Finance Approvers": "Operations",
                       "HR Data Owners": "Finance"}
ASSETS_BY_GROUP = {
    "All Staff": {"email", "intranet", "file share"},
    "IT Admins": {"identity provider", "VPN gateway", "domain controller", "backup server"},
    "Finance Approvers": {"payments system", "ERP"},
    "HR Data Owners": {"HR system"},
}


@pytest.fixture(scope="module")
def org(world):
    return world.tables


def _by(table, key):
    return {row[key]: row for row in table}


def test_the_generator_writes_the_eight_tables(tmp_path, world):
    assert set(world.tables) == set(TABLES)
    g.write(world, tmp_path)
    for name in TABLES:
        with open(tmp_path / "org" / f"{name}.csv", encoding="utf-8", newline="") as f:
            assert list(csv.DictReader(f)) == world.tables[name], name


def test_every_record_has_an_id_unique_in_its_table(org):
    for name in TABLES:
        id_column = next(iter(org[name][0]))
        assert id_column.endswith("_id"), name
        ids = [row[id_column] for row in org[name]]
        assert all(ids) and len(ids) == len(set(ids)), name


def test_people_are_the_ports_fifty_users_in_six_departments(org):
    people = org["people"]
    us_users = {name for name, _ in g.US_USERS}
    assert {p["username"] for p in people} == set(g.UK_USERS) | us_users
    assert len(people) == 50
    assert {p["department"] for p in people} == DEPARTMENTS
    # The six US users are spread across the six departments.
    assert len({p["department"] for p in people if p["username"] in us_users}) == 6


def test_three_cross_cutting_privileged_groups_of_three_to_five(org):
    people = _by(org["people"], "person_id")
    groups = _by(org["groups"], "group_id")
    members = {}
    for m in org["memberships"]:
        members.setdefault(groups[m["group_id"]]["name"], []).append(people[m["person_id"]])
    for name, department in PRIVILEGED.items():
        assert 3 <= len(members[name]) <= 5, name
        departments = Counter(p["department"] for p in members[name])
        assert departments == {department: len(members[name]) - 1,
                               OUTSIDER_DEPARTMENT[name]: 1}, name
        assert {group["kind"] for group in groups.values() if group["name"] == name} == {
            "privileged"}
    # Everyone holds baseline access through one group.
    assert len(members["All Staff"]) == 50


def test_ten_assets_granted_as_t04_lists_with_an_owner(org):
    people = _by(org["people"], "person_id")
    groups = _by(org["groups"], "group_id")
    assets = _by(org["assets"], "asset_id")
    assert len(assets) == 10
    assert all(a["sensitivity"] in {"internal", "confidential", "restricted"}
               for a in assets.values())
    assert all(a["owner_id"] in people for a in assets.values())
    reached = {}
    for grant in org["grants"]:
        reached.setdefault(groups[grant["group_id"]]["name"], set()).add(
            assets[grant["asset_id"]]["name"])
    assert reached == ASSETS_BY_GROUP
    # Every privileged group reaches at least one restricted asset.
    restricted = {a["name"] for a in assets.values() if a["sensitivity"] == "restricted"}
    assert all(reached[name] & restricted for name in PRIVILEGED)


def test_one_laptop_each_and_two_shared_machines_used_by_three(org):
    people = _by(org["people"], "person_id")
    devices = _by(org["devices"], "device_id")
    users_of = {}
    for a in org["device_assignments"]:
        users_of.setdefault(a["device_id"], []).append(people[a["person_id"]])
    laptops = [d for d in devices.values() if d["kind"] == "laptop"]
    shared = [d for d in devices.values() if d["kind"] == "shared"]
    assert len(laptops) == 50 and len(shared) == 2 and len(devices) == 52
    assert sorted(len(users_of[d["device_id"]]) for d in laptops) == [1] * 50
    assert {users_of[d["device_id"]][0]["username"] for d in laptops} == {
        p["username"] for p in people.values()}
    for d in shared:
        assert len(users_of[d["device_id"]]) == 3, d["name"]
    # The shared-device case crosses a department (T04 d4).
    assert any(len({p["department"] for p in users_of[d["device_id"]]}) > 1 for d in shared)


def test_networks_hold_the_offices_homes_decoys_and_a_four_address_vpn_pool(org):
    networks = org["networks"]
    by_kind = Counter(n["kind"] for n in networks)
    assert by_kind["vpn"] == 4
    assert by_kind["home"] == len(g.UK_USERS)
    addresses = {n["address"] for n in networks}
    assert {g.UK_OFFICE_IP, g.US_OFFICE_IP, *g.DECOY_IPS} <= addresses
    assert len(addresses) == len(networks)
    # Attackers' addresses are not the organisation's networks.
    assert not addresses & ATTACKER_IPS
    vpn = [n["address"] for n in networks if n["kind"] == "vpn"]
    assert all(not ipaddress.ip_address(ip).is_global for ip in vpn)


# The two new log columns (T04 d4 and d7, with the author's device rulings of 26 October 2026).

def _is_phone(row):
    return "iPhone" in row["user_agent"] or "Android" in row["user_agent"]


def test_the_log_gains_device_id_and_mfa_result(generated):
    rows, _ = generated
    assert g.COLUMNS == PORT_COLUMNS + ["device_id", "mfa_result"]
    assert all(list(r) == g.COLUMNS for r in rows)


def test_mfa_result_follows_the_outcome_and_the_exception_list(generated):
    rows, _ = generated
    assert set(g.MFA_RESULTS) == {"pass", "fail", "none", "denied"}
    # Failed passwords never reach MFA.
    assert {r["mfa_result"] for r in rows if r["outcome"] == "failure"} == {"none"}
    # S3's target is on the MFA exception list, so it is never prompted.
    assert {r["mfa_result"] for r in rows
            if r["username"] == g.S1_TARGET and r["outcome"] == "success"} == {"none"}
    others = {r["mfa_result"] for r in rows
              if r["username"] != g.S1_TARGET and r["outcome"] == "success"}
    assert others == {"pass"}
    # `denied` is reserved for MFA fatigue and unused.
    assert "denied" not in {r["mfa_result"] for r in rows}


def test_device_id_is_empty_exactly_on_attacker_and_phone_rows(generated):
    rows, _ = generated
    for r in rows:
        unregistered = r["source_ip"] in ATTACKER_IPS or _is_phone(r)
        assert (r["device_id"] == "") == unregistered, r
    phone_rows = [r for r in rows if r["source_ip"] not in ATTACKER_IPS and _is_phone(r)]
    assert len(phone_rows) == 124  # measured in the Port's log at ticket 11


def test_the_tables_and_the_log_agree(generated, org):
    rows, _ = generated
    people = _by(org["people"], "person_id")
    usernames = {p["username"]: pid for pid, p in people.items()}
    devices = _by(org["devices"], "device_id")
    uses = {(a["device_id"], a["person_id"]) for a in org["device_assignments"]}
    for r in rows:
        if r["failure_reason"] == "unknown_user":
            continue  # the sprayer guessed names that are no account
        assert r["username"] in usernames, r
        if r["device_id"]:
            assert r["device_id"] in devices, r
            assert (r["device_id"], usernames[r["username"]]) in uses, r


def test_each_shared_machine_is_used_in_the_log_by_all_three_of_its_users(generated, org):
    rows, _ = generated
    people = _by(org["people"], "person_id")
    for device in (g.MEETING_ROOM_PC, g.WAREHOUSE_TERMINAL):
        expected = {people[a["person_id"]]["username"] for a in org["device_assignments"]
                    if a["device_id"] == device}
        on_it = [r for r in rows if r["device_id"] == device]
        assert {r["username"] for r in on_it} == expected, device
        assert {r["source_ip"] for r in on_it} == {g.UK_OFFICE_IP}, device
