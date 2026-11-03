"""Assessment records (record group 8): human labels, critical-error flags, assistant notes and
deterministic checks, all appended to the run bundle and never overwritten.

Scores follow the approved common method: 2, 1 or 0 per criterion, or "n/a" where the case's
gold marks the criterion not applicable. A criterion with no label is "unscored": it is neither
a zero nor a pass. Critical errors are separate flags and are never averaged away. The author's
initial labels for an answer must all be saved before an assistant note on that answer can be
recorded, so suggestions cannot shape the first human judgement.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from evals.comparison import fixtures
from evals.comparison.records import RunBundle

SCORES = (0, 1, 2, "n/a")
UNSCORED = "unscored"
BRACKETS = re.compile(r"\[([^\[\]]*)\]")
REF = r"[A-Z]{1,3}-?[0-9]+"
REFERENCE = re.compile(rf"(?<![\w]){REF}(?![\w])")
CITATION_ITEM = re.compile(rf"({REF})(?:\s*[-‐‑–−]\s*({REF}))?")
REF_PARTS = re.compile(r"([A-Z]{1,3}-?)([0-9]+)")
MAX_RANGE_REFS = 1000
CHECK_VERSION = "reference-resolution/2"


def load_gold(case_id: str, root: Path = fixtures.FROZEN) -> dict:
    return json.loads((root / "gold" / f"{case_id}.json").read_text())


class AssessmentError(ValueError):
    pass


def _labels(bundle: RunBundle, review_id: str) -> list[dict]:
    return [e for e in bundle.events() if e["type"] == "label" and e["review_id"] == review_id]


def validate_label(gold: dict, case_id: str, criterion: str, score, reason: str) -> None:
    if criterion not in gold["criteria"]:
        raise AssessmentError(f"unknown criterion {criterion!r}")
    if score not in SCORES or isinstance(score, bool):
        raise AssessmentError(f"score must be one of 0, 1, 2 or 'n/a', not {score!r}")
    if score == "n/a" and gold["criteria"][criterion]["applicable"]:
        raise AssessmentError(f"{criterion} applies to {case_id}; n/a cannot excuse it")
    if not reason.strip():
        raise AssessmentError("every label records its reason")


def existing_labels(bundle: RunBundle, review_id: str, criterion: str,
                    assessor_type: str = "human") -> list[dict]:
    return [e for e in _labels(bundle, review_id) if e["criterion"] == criterion
            and e["assessor_type"] == assessor_type]


def record_label(bundle: RunBundle, *, review_id: str, case_id: str, criterion: str, score,
                 excerpt: str, evidence_ref: str, reason: str, assessor: str,
                 assessor_type: str = "human", revises: int | None = None) -> dict:
    """Save one criterion label. A revision names the label it revises and keeps it in history."""
    validate_label(load_gold(case_id), case_id, criterion, score, reason)
    if assessor_type not in ("human", "assistant"):
        raise AssessmentError("assessor_type is 'human' or 'assistant'")
    earlier = existing_labels(bundle, review_id, criterion, assessor_type)
    if revises is None and earlier:
        raise AssessmentError(f"{criterion} already has an initial label; record a revision")
    if revises is not None and revises not in {e["seq"] for e in earlier}:
        raise AssessmentError(f"label {revises} is not an earlier {criterion} label for {review_id}")
    return bundle.append("label", review_id=review_id, case_id=case_id, criterion=criterion,
                         score=score, excerpt=excerpt, evidence_ref=evidence_ref, reason=reason,
                         assessor=assessor, assessor_type=assessor_type,
                         phase="revision" if revises is not None else "initial", revises=revises,
                         rubric_version=bundle.manifest.get("rubric_version"))


def validate_flag(gold: dict, case_id: str, error_id: str, reason: str) -> None:
    if error_id not in {c["id"] for c in gold["critical_errors"]}:
        raise AssessmentError(f"{error_id} is not a designated critical error for {case_id}")
    if not reason.strip():
        raise AssessmentError("every flag records its reason")


def existing_flags(bundle: RunBundle, review_id: str, error_id: str,
                   assessor_type: str = "human") -> list[dict]:
    return [e for e in bundle.events() if e["type"] == "critical_flag"
            and e["review_id"] == review_id and e["error_id"] == error_id
            and e["assessor_type"] == assessor_type]


def record_critical(bundle: RunBundle, *, review_id: str, case_id: str, error_id: str,
                    present: bool, excerpt: str, reason: str, assessor: str,
                    assessor_type: str = "human", revises: int | None = None) -> dict:
    validate_flag(load_gold(case_id), case_id, error_id, reason)
    if assessor_type not in ("human", "assistant"):
        raise AssessmentError("assessor_type is 'human' or 'assistant'")
    earlier = existing_flags(bundle, review_id, error_id, assessor_type)
    if revises is None and earlier:
        raise AssessmentError(f"{error_id} already has an initial flag; record a revision")
    if revises is not None and revises not in {e["seq"] for e in earlier}:
        raise AssessmentError(f"flag {revises} is not an earlier {error_id} flag for {review_id}")
    return bundle.append("critical_flag", review_id=review_id, case_id=case_id, error_id=error_id,
                         present=present, excerpt=excerpt, reason=reason, assessor=assessor,
                         assessor_type=assessor_type,
                         phase="revision" if revises is not None else "initial", revises=revises)


def initial_labels_complete(bundle: RunBundle, review_id: str, case_id: str) -> bool:
    """Every criterion labelled and every designated critical error assessed by a human."""
    gold = load_gold(case_id)
    initial = [e for e in bundle.events() if e.get("review_id") == review_id
               and e.get("assessor_type") == "human" and e.get("phase") == "initial"]
    labelled = {e["criterion"] for e in initial if e["type"] == "label"}
    flagged = {e["error_id"] for e in initial if e["type"] == "critical_flag"}
    return set(gold["criteria"]) <= labelled and {c["id"] for c in gold["critical_errors"]} <= flagged


def record_assistant_note(bundle: RunBundle, *, review_id: str, case_id: str, text: str,
                          assistant: str) -> dict:
    """Assistant discussion or a suggested score: only after the author's initial labels."""
    if not initial_labels_complete(bundle, review_id, case_id):
        raise AssessmentError("save the author's initial labels for every criterion and "
                              "critical error first")
    return bundle.append("assistant_note", review_id=review_id, case_id=case_id, text=text,
                         assistant=assistant,
                         note="assistant assistance; not an independent human assessment")


def profile(bundle: RunBundle, review_id: str, case_id: str) -> dict:
    """The latest human label per criterion (`unscored` where none exists), the critical errors
    whose latest human flag is present, and those nobody has assessed yet. An unassessed
    critical error is unscored, not absent."""
    gold = load_gold(case_id)
    scores = {c: UNSCORED for c in gold["criteria"]}
    flags: dict[str, bool] = {}
    for event in bundle.events():
        if event.get("review_id") != review_id or event.get("assessor_type") != "human":
            continue
        if event["type"] == "label":
            scores[event["criterion"]] = event["score"]
        elif event["type"] == "critical_flag":
            flags[event["error_id"]] = event["present"]
    return {"scores": scores,
            "critical_errors": sorted(e for e, present in flags.items() if present),
            "critical_unassessed": sorted(c["id"] for c in gold["critical_errors"]
                                          if c["id"] not in flags)}


def reference_check(answer: str, case: dict) -> dict:
    """Do the answer's bracketed citations exist in the case file? Resolution only: a resolving
    citation is not proof that the source supports the claim.

    Accept whitespace, comma/semicolon groups and ascending same-prefix ranges with full
    endpoints. Unsupported reference-like groups retain explicit references and a warning;
    they must not silently become a clean result. Other bracketed prose is ignored.
    """
    occurrences: list[str] = []
    unsupported: list[str] = []
    for bracket in BRACKETS.finditer(answer):
        body = bracket.group(1).strip()
        if not REFERENCE.search(body):
            continue
        complete = True
        for item in re.split(r"[,;]", body):
            item = item.strip()
            match = CITATION_ITEM.fullmatch(item)
            if match is None:
                occurrences.extend(REFERENCE.findall(item))
                complete = False
                continue
            first, last = match.groups()
            if last is None:
                occurrences.append(first)
                continue
            start, end = REF_PARTS.fullmatch(first), REF_PARTS.fullmatch(last)
            assert start is not None and end is not None
            prefix, low_text = start.groups()
            end_prefix, high_text = end.groups()
            if len(low_text) > 9 or len(high_text) > 9:
                occurrences.extend((first, last))
                complete = False
                continue
            low, high = int(low_text), int(high_text)
            if (prefix != end_prefix or not 0 <= high - low < MAX_RANGE_REFS
                    or str(low) != low_text or str(high) != high_text):
                occurrences.extend((first, last))
                complete = False
            else:
                occurrences.extend(f"{prefix}{number}" for number in range(low, high + 1))
        if not complete:
            unsupported.append(bracket.group(0))
    cited = sorted(set(occurrences))
    known = set(fixtures.evidence_refs(case))
    return {"check": "reference_resolution", "cited": cited,
            "unresolved": [ref for ref in cited if ref not in known],
            "citation_count": len(occurrences), "unsupported_citations": unsupported,
            "limit": "resolution does not establish that the source supports the claim; "
                     "only reference-like square-bracket groups are inspected"}


def run_deterministic_checks(bundle: RunBundle) -> list[dict]:
    """Rescore saved answers offline. No model is called. An answer already checked by this
    version of the check is not recorded again."""
    events = bundle.events()
    started = {e["trial_id"]: e for e in events if e["type"] == "trial_started"}
    done = {(e["trial_id"], e.get("answer_sha256")) for e in events
            if e["type"] == "deterministic_check" and e.get("check_version") == CHECK_VERSION}
    results = []
    for event in [e for e in events if e["type"] == "trial_finished"]:
        trial = started[event["trial_id"]]
        ref = event.get("final_answer") or event.get("partial_answer")
        if ref is None or trial["case_id"] not in fixtures.CASE_IDS:
            continue
        if (event["trial_id"], ref["sha256"]) in done:
            continue
        outcome = reference_check(bundle.read_artifact(ref), fixtures.load_case(trial["case_id"]))
        results.append(bundle.append("deterministic_check", trial_id=event["trial_id"],
                                     answer_sha256=ref["sha256"], check_version=CHECK_VERSION,
                                     **outcome))
    return results
