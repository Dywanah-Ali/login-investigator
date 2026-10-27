"""Check a delivered own corpus against its brief, the organisation tables and the answer key.

Facts in the corpus are checked by code; people read the documents only for feel. No networking.
"""

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from login_investigator.attack_corpus import MITIGATIONS, TECHNIQUES

FIELDS = ("id", "title", "kind", "owner", "department", "date", "version", "status", "supersedes")
WORD = re.compile(r"[A-Za-z0-9]+(?:[.'-][A-Za-z0-9]+)*")
# A username is first.last; the look-arounds skip email domains, device IDs and dotted names.
USERNAME = re.compile(r"(?<![\w.@/-])[a-z]{2,}\.[a-z]{2,}(?![\w-]|\.[a-z])")
DEVICE_ID = re.compile(r"\bdev-[a-z0-9]+(?:[.-][a-z0-9]+)*")
ASSET_ID = re.compile(r"\basset-[a-z0-9]+(?:-[a-z0-9]+)*")
ADDRESS = re.compile(r"(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.]*\d)")
ATTACK_ID = re.compile(r"\b(?:T\d{4}(?:\.\d{3})?|M\d{4})\b")
OWN_KINDS = ("policy", "runbook", "register", "record", "meeting", "email", "guidance")
INCIDENT_WRITEUP_TERMS =("incident report", "incident write-up", "post-incident", "post-mortem")


@dataclass(frozen=True)
class PlannedDocument:
    id: str
    title: str
    kind: str
    owner: str
    department: str
    date: str
    version: str
    status: str
    supersedes: str | None


@dataclass(frozen=True)
class Brief:
    teams: tuple[str, ...]
    documents: tuple[PlannedDocument, ...]
    forbidden_terms: tuple[str, ...]


@dataclass(frozen=True)
class DocumentLength:
    id: str
    kind: str
    words: int
    sections: int
    longest_section_words: int


@dataclass(frozen=True)
class CorpusReport:
    errors: tuple[str, ...]
    lengths: tuple[DocumentLength, ...]


def section_lines(text: str, heading: str) -> list[str]:
    """The lines under one `## heading` of the brief, up to the next heading of that level."""
    lines = text.splitlines()
    try:
        start = lines.index(f"## {heading}") + 1
    except ValueError as exc:
        raise ValueError(f"Brief has no '## {heading}' section") from exc
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def table_rows(lines: list[str]) -> list[list[str]]:
    """Cells of a Markdown table's body rows, with code ticks stripped."""
    rows = [line for line in lines if line.startswith("|")]
    return [[cell.strip().strip("`") for cell in row.strip("|").split("|")] for row in rows[2:]]


def read_brief(text: str) -> Brief:
    teams = tuple(row[0] for row in table_rows(section_lines(text, "Owner teams")))
    documents = []
    for row in table_rows(section_lines(text, "Document list")):
        if len(row) != len(FIELDS):
            raise ValueError(f"Brief document row needs {len(FIELDS)} cells: {row}")
        values = dict(zip(FIELDS, row))
        documents.append(PlannedDocument(**{
            **values, "supersedes": None if values["supersedes"] == "none" else values["supersedes"],
        }))
    forbidden = tuple(
        line.removeprefix("- ").strip("`") for line in section_lines(text, "Forbidden terms")
        if line.startswith("- ")
    )
    return Brief(teams, tuple(documents), forbidden)


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    """Front matter is `key: <JSON value>` lines between two `---` lines, as the ATT&CK pages use."""
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("no front matter between '---' lines")
    end = lines.index("---", 1)
    header: dict[str, object] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(": ")
        if not separator:
            raise ValueError(f"front matter line is not 'key: value': {line!r}")
        try:
            header[key] = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"front matter value for {key} is not quoted text or null") from exc
    return header, "\n".join(lines[end + 1:])


def measure(identifier: str, kind: str, body: str) -> DocumentLength:
    sections = re.split(r"^## .*$", body, flags=re.MULTILINE)
    return DocumentLength(
        id=identifier, kind=kind, words=len(WORD.findall(body)), sections=len(sections) - 1,
        longest_section_words=max(len(WORD.findall(section)) for section in sections[1:] or [""]),
    )


def read_table(dataset: Path, name: str) -> list[dict[str, str]]:
    with (dataset / "org" / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@dataclass(frozen=True)
class World:
    """The organisation facts a mention is checked against."""
    usernames: frozenset[str]
    device_ids: frozenset[str]
    device_names: frozenset[str]
    asset_ids: frozenset[str]
    addresses: frozenset[str]
    display_names: dict[str, str]
    devices_by_user: dict[str, tuple[str, ...]]
    asset_names: dict[str, str]
    departments: frozenset[str]

    @classmethod
    def read(cls, dataset: Path) -> "World":
        people = read_table(dataset, "people")
        devices = read_table(dataset, "devices")
        assets = read_table(dataset, "assets")
        device_names = {row["device_id"]: row["name"] for row in devices}
        usernames = {row["person_id"]: row["username"] for row in people}
        devices_by_user: dict[str, tuple[str, ...]] = {}
        for row in read_table(dataset, "device_assignments"):
            user = usernames[row["person_id"]]
            device = row["device_id"]
            devices_by_user[user] = (*devices_by_user.get(user, ()), device, device_names[device])
        return cls(
            usernames=frozenset(usernames.values()),
            device_ids=frozenset(device_names),
            device_names=frozenset(device_names.values()),
            asset_ids=frozenset(row["asset_id"] for row in assets),
            addresses=frozenset(row["address"] for row in read_table(dataset, "networks")),
            display_names={row["username"]: row["display_name"] for row in people},
            devices_by_user=devices_by_user,
            asset_names={row["asset_id"]: row["name"] for row in assets},
            departments=frozenset(row["department"] for row in people),
        )

    def device_name_pattern(self) -> re.Pattern[str]:
        """Device names share a few prefixes, such as LT-; any token with one is a device."""
        prefixes = sorted({name.split("-", 1)[0] for name in self.device_names})
        return re.compile(rf"\b(?:{'|'.join(prefixes)})-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")


def mention_errors(body: str, world: World, leaver: str) -> list[str]:
    # `.example` is a reserved domain (RFC 2606), used for the company's email addresses.
    errors = [f"mentions unknown username {name}" for name in USERNAME.findall(body)
              if name not in world.usernames and name != leaver and not name.endswith(".example")]
    errors += [f"mentions unknown device {device}"
               for device in world.device_name_pattern().findall(body) + DEVICE_ID.findall(body)
               if device not in world.device_names | world.device_ids]
    errors += [f"mentions unknown asset {asset}" for asset in ASSET_ID.findall(body)
               if asset not in world.asset_ids]
    errors += [f"mentions address {address}, which is not in the networks table"
               for address in ADDRESS.findall(body) if address not in world.addresses]
    errors += [f"mentions technique {identifier}, which is not in the ATT&CK corpus"
               for identifier in ATTACK_ID.findall(body)
               if identifier not in (*TECHNIQUES, *MITIGATIONS)]
    return list(dict.fromkeys(errors))


def brief_errors(brief: Brief, world: World) -> list[str]:
    """The brief's plan must itself be valid before documents are compared with it."""
    errors: list[str] = []
    planned = [document.id for document in brief.documents]
    errors += [f"brief: {identifier} is planned more than once"
               for identifier in dict.fromkeys(planned) if planned.count(identifier) > 1]
    for document in brief.documents:
        name = document.id
        if document.kind not in OWN_KINDS:
            errors.append(f"brief: {name} kind {document.kind} is not an own-document kind")
        if document.owner not in brief.teams:
            errors.append(f"brief: {name} owner {document.owner} is not an allowed team")
        if document.department not in world.departments:
            errors.append(f"brief: {name} department {document.department} "
                          "is not a department in the people table")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", document.date):
            errors.append(f"brief: {name} date {document.date} is not YYYY-MM-DD")
        if document.status not in ("current", "superseded"):
            errors.append(f"brief: {name} status {document.status} is not current or superseded")
        if document.supersedes is not None and document.supersedes not in planned:
            errors.append(f"brief: {name} supersedes {document.supersedes}, "
                          "which the brief does not plan")
    return errors


def absent_topic_terms(truth: dict, world: World) -> tuple[str, ...]:
    """Words that would bring one of the answer key's absent topics into the corpus."""
    terms: list[str] = []
    for topic in truth["absent_topics"]:
        kind = topic["kind"]
        if kind == "incident_writeups":
            terms += INCIDENT_WRITEUP_TERMS
        elif kind == "asset_governance":
            terms += [topic["asset_id"], world.asset_names[topic["asset_id"]]]
        elif kind == "policy":
            terms.append(topic["topic"])
        elif kind == "users":
            for user in topic["usernames"]:
                terms += [user, world.display_names[user], *world.devices_by_user.get(user, ())]
        else:
            raise ValueError(f"No check is defined for absent topic kind {kind}")
    return tuple(dict.fromkeys(terms))


def contains_term(text: str, term: str) -> bool:
    """Case-insensitive, from a word start, across line breaks: 'backup' also finds 'backups'."""
    words = r"\s+".join(re.escape(word) for word in term.split())
    return re.search(rf"(?<!\w){words}", text, flags=re.IGNORECASE) is not None


def check_corpus(dataset: Path, brief: Brief) -> CorpusReport:
    errors: list[str] = []
    lengths: list[DocumentLength] = []
    plan = {document.id: document for document in brief.documents}
    truth = json.loads((dataset / "truth.json").read_text(encoding="utf-8"))
    world = World.read(dataset)
    errors.extend(brief_errors(brief, world))
    errors.extend(f"brief: the answer key expects {identifier}, which the brief does not plan"
                  for identifier in sorted(expected_document_ids(truth)) if identifier not in plan)
    leaver = truth["leaver"]
    leaver_documents: list[tuple[str, object]] = []
    unreadable: list[str] = []
    forbidden = tuple(dict.fromkeys((*absent_topic_terms(truth, world), *brief.forbidden_terms)))
    for path in sorted((dataset / "corpus" / "own").glob("*.md")):
        name = path.stem
        text = path.read_text(encoding="utf-8")
        errors.extend(f"{name}: contains forbidden term {term}"
                      for term in forbidden if contains_term(text, term))
        try:
            header, body = split_front_matter(text)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            unreadable.append(name)
            continue
        errors.extend(f"{name}: front matter is missing {field}"
                      for field in FIELDS if field not in header)
        errors.extend(f"{name}: front matter has unexpected field {field}"
                      for field in header if field not in FIELDS)
        errors.extend(f"{name}: front matter {field} must be quoted text"
                      for field, value in header.items()
                      if not isinstance(value, str) and not (field == "supersedes" and value is None))
        if "id" in header and header["id"] != name:
            errors.append(f"{name}: id is {header['id']}, which does not match its file name")
        if name not in plan:
            errors.append(f"{name}: not planned in the brief")
        if header.get("owner") not in brief.teams:
            errors.append(f"{name}: owner {header.get('owner')} is not an allowed team")
        planned = plan.get(name)
        if planned:
            errors.extend(
                f"{name}: {field} is {header[field]}, the brief plans {getattr(planned, field)}"
                for field in FIELDS if field in header and header[field] != getattr(planned, field)
                and not (field == "owner" and header[field] not in brief.teams)
            )
        errors.extend(f"{name}: {error}" for error in mention_errors(body, world, leaver))
        if re.search(rf"\b{re.escape(leaver)}\b", body):
            leaver_documents.append((name, header.get("kind")))
        lengths.append(measure(name, str(header.get("kind")), body))
    delivered = {length.id for length in lengths} | set(unreadable)
    errors.extend(f"{identifier}: planned in the brief but not delivered"
                  for identifier in plan if identifier not in delivered)
    if [kind for _, kind in leaver_documents] != ["register"]:
        found = ", ".join(name for name, _ in leaver_documents) or "none"
        errors.append(f"leaver {leaver} must appear in exactly one register, found in {found}")
    return CorpusReport(tuple(errors), tuple(lengths))


def expected_document_ids(truth: object) -> set[str]:
    """Every document ID the answer key points at, wherever it sits in the key."""
    found: set[str] = set()
    if isinstance(truth, dict):
        for key, value in truth.items():
            if key == "expected_document_ids":
                found.update(value)
            elif key == "clearing_document_id":
                found.add(value)
            else:
                found |= expected_document_ids(value)
    elif isinstance(truth, list):
        for item in truth:
            found |= expected_document_ids(item)
    return found
