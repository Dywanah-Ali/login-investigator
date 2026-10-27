"""The T15 consistency script: a delivered own corpus checked against its brief and the world."""

import json
import re
import shutil
from collections import Counter
from pathlib import Path

import pytest

from login_investigator.corpus_check import (
    World, absent_topic_terms, brief_errors, check_corpus, contains_term, mention_errors, read_brief,
)
from scripts.check_corpus import main

SAMPLE = Path(__file__).parent / "fixtures" / "corpus"


def sample_brief():
    return read_brief((SAMPLE / "brief.md").read_text())


def copy_of_sample(tmp_path: Path) -> Path:
    dataset = tmp_path / "dataset"
    shutil.copytree(SAMPLE / "dataset", dataset)
    return dataset


def edit(dataset: Path, document: str, old: str, new: str) -> None:
    path = dataset / "corpus" / "own" / f"{document}.md"
    text = path.read_text()
    assert old in text
    path.write_text(text.replace(old, new))


def test_good_sample_passes_and_reports_lengths():
    report = check_corpus(SAMPLE / "dataset", sample_brief())

    assert report.errors == ()
    lengths = {length.id: length for length in report.lengths}
    assert set(lengths) == {"pol-sample", "pol-sample-old", "reg-sample", "rec-sample"}
    assert lengths["pol-sample"].kind == "policy"
    assert lengths["pol-sample"].sections == 2
    assert lengths["pol-sample-old"].words == 15  # 3 heading words and a 12-word sentence


def test_missing_front_matter_field_fails(tmp_path):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "rec-sample", 'department: "Sales"\n', "")

    report = check_corpus(dataset, sample_brief())

    assert report.errors == ("rec-sample: front matter is missing department",)


def test_owner_outside_the_allowed_teams_fails(tmp_path):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "pol-sample", 'owner: "Security"', 'owner: "ann.lee"')

    report = check_corpus(dataset, sample_brief())

    assert report.errors == ("pol-sample: owner ann.lee is not an allowed team",)


def test_header_that_differs_from_the_brief_fails(tmp_path):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "reg-sample", 'owner: "IT Support"', 'owner: "Security"')
    edit(dataset, "reg-sample", 'version: "1.1"', 'version: "1.2"')

    report = check_corpus(dataset, sample_brief())

    assert report.errors == (
        "reg-sample: owner is Security, the brief plans IT Support",
        "reg-sample: version is 1.2, the brief plans 1.1",
    )


def test_missing_and_unplanned_documents_fail(tmp_path):
    dataset = copy_of_sample(tmp_path)
    own = dataset / "corpus" / "own"
    (own / "rec-sample.md").unlink()
    (own / "pol-extra.md").write_text((own / "pol-sample-old.md").read_text())

    report = check_corpus(dataset, sample_brief())

    assert report.errors == (
        "pol-extra: id is pol-sample-old, which does not match its file name",
        "pol-extra: not planned in the brief",
        "rec-sample: planned in the brief but not delivered",
    )


def test_brief_that_omits_a_document_the_answer_key_expects_fails(tmp_path):
    dataset = copy_of_sample(tmp_path)
    (dataset / "corpus" / "own" / "rec-sample.md").unlink()
    text = (SAMPLE / "brief.md").read_text()
    row = next(line for line in text.splitlines() if line.startswith("| `rec-sample`"))

    report = check_corpus(dataset, read_brief(text.replace(row + "\n", "")))

    assert report.errors == ("brief: the answer key expects rec-sample, which the brief does not plan",)


@pytest.mark.parametrize(("mention", "error"), [
    ("zed.marlow", "mentions unknown username zed.marlow"),
    ("LT-ZMARLOW", "mentions unknown device LT-ZMARLOW"),
    ("dev-laptop-zed.marlow", "mentions unknown device dev-laptop-zed.marlow"),
    ("asset-crm", "mentions unknown asset asset-crm"),
    ("10.20.30.40", "mentions address 10.20.30.40, which is not in the networks table"),
    ("T1566.001", "mentions technique T1566.001, which is not in the ATT&CK corpus"),
])
def test_unknown_mention_fails(tmp_path, mention, error):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "rec-sample", "Bob Kerr received", f"Bob Kerr ({mention}) received")

    report = check_corpus(dataset, sample_brief())

    assert report.errors == (f"rec-sample: {error}",)


@pytest.mark.parametrize(("text", "term"), [
    ("Cara Voss", "Cara Voss"),
    ("cara.voss", "cara.voss"),
    ("LT-CVOSS", "LT-CVOSS"),
    ("the backup server", "backup server"),
    ("asset-backup-server", "asset-backup-server"),
    ("a data\nretention schedule", "data retention"),
    ("an Incident Report", "incident report"),
    ("nightly backups", "backup"),
])
def test_absent_topic_or_forbidden_term_present_fails(tmp_path, text, term):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "rec-sample", "after a hardware fault", f"after a hardware fault, see {text}")

    report = check_corpus(dataset, sample_brief())

    assert f"rec-sample: contains forbidden term {term}" in report.errors


def test_invalid_rows_in_the_brief_fail():
    text = (SAMPLE / "brief.md").read_text().replace(
        "| `reg-sample` | Sample Register | register | IT Support | IT | 2026-09-01 | 1.1 | current | none |",
        "| `reg-sample` | Sample Register | memo | Legal | Legal | 1 Sept | 1.1 | draft | `pol-gone` |",
    )

    report = check_corpus(SAMPLE / "dataset", read_brief(text))

    brief_errors = [error for error in report.errors if error.startswith("brief:")]
    assert brief_errors == [
        "brief: reg-sample kind memo is not an own-document kind",
        "brief: reg-sample owner Legal is not an allowed team",
        "brief: reg-sample department Legal is not a department in the people table",
        "brief: reg-sample date 1 Sept is not YYYY-MM-DD",
        "brief: reg-sample status draft is not current or superseded",
        "brief: reg-sample supersedes pol-gone, which the brief does not plan",
    ]


def test_command_passes_a_good_corpus_and_prints_lengths(capsys):
    code = main(["--dataset-dir", str(SAMPLE / "dataset"), "--brief", str(SAMPLE / "brief.md")])

    output = capsys.readouterr().out
    assert code == 0
    assert "Passed: 4 documents, 0 errors" in output
    assert "pol-sample-old" in output


def test_command_fails_a_bad_corpus_and_lists_the_errors(tmp_path, capsys):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "rec-sample", 'department: "Sales"\n', "")

    code = main(["--dataset-dir", str(dataset), "--brief", str(SAMPLE / "brief.md")])

    output = capsys.readouterr().out
    assert code == 1
    assert "Failed: 4 documents, 1 error\n" in output
    assert "- rec-sample: front matter is missing department" in output


REAL_BRIEF = Path(__file__).resolve().parents[2] / ".scratch" / "knowledge-base" / "codex-brief.md"
DEFAULT_DATASET = Path(__file__).resolve().parents[1] / "data" / "datasets" / "default"
# Words that would tell the writer about the exam, the planted events or why a document exists.
EXAM_WORDS = (
    "eval", "evals", "evaluation", "test", "tests", "testing", "exam", "exams", "planted",
    "story", "stories", "scenario", "scenarios", "twin", "twins", "benign", "decoy", "gold",
    "answer key", "ground truth", "truth.json", "retrieval", "RAG", "canary", "injection",
    "prompt", "prompts", "investigator", "agent", "agents", "model", "chunk", "chunks",
    "embedding", "graph", "blast radius", "S1", "S2", "S3", "S4", "S5", "S6", "B1", "B2", "B3",
)


def whole_word(text: str, word: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text, flags=re.IGNORECASE) is not None
REAL_NAMES = ("Microsoft", "Okta", "Google", "Cisco", "Duo", "Azure", "Amazon", "AWS", "Apple",
              "Zoom", "Slack", "MITRE")


def test_real_brief_plans_the_27_documents_with_the_answer_keys_ids():
    brief = read_brief(REAL_BRIEF.read_text())
    world = World.read(DEFAULT_DATASET)
    truth = json.loads((DEFAULT_DATASET / "truth.json").read_text())

    kinds = Counter(document.kind for document in brief.documents)
    # T04 d10 and d11: 15 core documents (6 policies with the superseded one, 4 runbooks,
    # 2 registers, 3 records) and 12 others (5 meetings, 5 emails, 2 guidance documents).
    assert kinds == {"policy": 6, "runbook": 4, "register": 2, "record": 3,
                     "meeting": 5, "email": 5, "guidance": 2}
    assert {"reg-mfa-exceptions", "run-password-spray-response",
            "run-compromised-account-response", "rec-approved-travel", "rec-helpdesk-reset",
            "rec-laptop-handover"} <= {document.id for document in brief.documents}
    assert brief_errors(brief, world) == []
    assert not set(brief.teams) & world.usernames
    assert [document.id for document in brief.documents if document.status == "superseded"] == [
        "pol-password-2024"]
    assert mention_errors(REAL_BRIEF.read_text(), world, truth["leaver"]) == []


def test_real_brief_never_names_the_exam_or_a_real_company():
    text = REAL_BRIEF.read_text()

    assert [word for word in EXAM_WORDS if whole_word(text, word)] == []
    assert [name for name in REAL_NAMES if whole_word(text, name)] == []


def test_real_brief_keeps_absent_topics_out_or_forbids_them():
    text = REAL_BRIEF.read_text()
    brief = read_brief(text)
    world = World.read(DEFAULT_DATASET)
    truth = json.loads((DEFAULT_DATASET / "truth.json").read_text())
    hidden = [term for topic in truth["absent_topics"] if topic["kind"] == "users"
              for user in topic["usernames"]
              for term in (user, world.display_names[user], *world.devices_by_user[user])]

    assert [term for term in hidden if contains_term(text, term)] == []
    uncovered = [term for term in absent_topic_terms(truth, world) if term not in hidden
                 and not any(contains_term(term, listed) for listed in brief.forbidden_terms)]
    assert uncovered == []


def test_leaver_outside_one_register_fails(tmp_path):
    dataset = copy_of_sample(tmp_path)
    edit(dataset, "rec-sample", "Bob Kerr received", "Finn Archer (finn.archer) received")

    report = check_corpus(dataset, sample_brief())

    assert report.errors == (
        "leaver finn.archer must appear in exactly one register, found in rec-sample, reg-sample",
    )
