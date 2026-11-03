"""Blinded answer review and the separate process/security view (record group 9).

A blinded batch shows the reviewer the question, the case file, the answer and the assessor-only
anchors. It never shows the configuration, model, design, settings, cost, timing, trial ID or
trace. Review IDs map back to trials only through `review/identity-map.json`, kept apart from the
batches. An answer that names its own model can still reveal it: that is recorded as a blinding
limitation and the answer is kept unchanged.

The process view keeps the full trace for security and process review. It is not blinded, and
says so.
"""

from __future__ import annotations

import json
import random
import re
import secrets

from evals.comparison import assessment, fixtures
from evals.comparison.records import RunBundle

IDENTITY_MAP = "review/identity-map.json"
VENDOR_WORDS = ("openai", "anthropic", "claude", "gpt", "qwen", "deepseek", "google", "gemini",
                "mistral", "meta", "llama", "deepinfra", "openrouter")


def _write_json(bundle: RunBundle, relative: str, data) -> dict:
    return bundle.write_artifact(relative, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def identity_map(bundle: RunBundle) -> dict[str, str]:
    """Review ID -> trial ID, from the event log, which is authoritative. The JSON file of the
    same name is a convenience copy for the operator."""
    mapping: dict[str, str] = {}
    for event in bundle.events():
        if event["type"] == "review_batch":
            mapping.update(event["identity"])
    return mapping


def _next_batch_number(bundle: RunBundle) -> int:
    """Never reuse a number, even one whose files were written before a crash lost its event."""
    recorded = sum(1 for e in bundle.events() if e["type"] == "review_batch")
    on_disk = [int(m.group(1)) for p in (bundle.root / "artifacts" / "review").glob("batch-*.json")
               if (m := re.fullmatch(r"batch-(\d+)\.json", p.name))]
    return 1 + max([recorded, *on_disk])


def _identity_words(bundle: RunBundle) -> list[str]:
    words = set(VENDOR_WORDS)
    for config in bundle.manifest["configs"]:
        words.update({config["label"].lower(), config["model"].lower(),
                      config["model"].split("/")[-1].lower(), config["config_id"].lower()})
    return sorted(w for w in words if len(w) >= 3)


def _limitations(answer: str, words: list[str]) -> list[str]:
    text = answer.lower()
    found = [w for w in words if re.search(rf"(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])", text)]
    return [f"answer text mentions {w!r}, which may reveal the candidate" for w in found]


def _anchors(gold: dict) -> dict:
    return {key: gold[key] for key in ("criteria", "required_findings", "forbidden_claims",
                                       "critical_errors", "unknowns", "grading_note")}


def prepare_batch(bundle: RunBundle, *, size: int, seed: int | None = None) -> dict:
    """Blind the next `size` answers not yet in a batch, in a shuffled, recorded order. Trials
    without any answer are listed as no-answer outcomes, never as scoreable items."""
    finished = [e for e in bundle.events() if e["type"] == "trial_finished"]
    started = {e["trial_id"]: e for e in bundle.events() if e["type"] == "trial_started"}
    mapping = identity_map(bundle)
    queued = set(mapping.values())
    candidates = [e for e in finished if e["trial_id"] not in queued
                  and started[e["trial_id"]]["case_id"] in fixtures.CASE_IDS]
    no_answer = [e["trial_id"] for e in candidates
                 if not e.get("final_answer") and not e.get("partial_answer")]
    scorable = [e for e in candidates if e.get("final_answer") or e.get("partial_answer")]
    seed = secrets.randbits(32) if seed is None else seed
    rng = random.Random(seed)
    rng.shuffle(scorable)
    chosen = scorable[:size]
    words = _identity_words(bundle)
    batch_number = _next_batch_number(bundle)
    items, limitations, identity = [], {}, {}
    for event in chosen:
        review_id = f"R-{rng.getrandbits(40):010x}"
        trial = started[event["trial_id"]]
        case = fixtures.load_case(trial["case_id"])
        is_final = bool(event.get("final_answer"))
        answer = bundle.read_artifact(event["final_answer"] if is_final else event["partial_answer"])
        identity[review_id] = event["trial_id"]
        found = _limitations(answer, words)
        if found:
            limitations[review_id] = found
        items.append({"review_id": review_id, "case_id": trial["case_id"],
                      "answer_kind": "final" if is_final else "partial (trial did not complete)",
                      "question": case["question"], "case_file": fixtures.render_case(case),
                      "answer": answer, "anchors": _anchors(assessment.load_gold(trial["case_id"]))})
    batch = {"batch": batch_number, "blinded": True, "items": items,
             "hidden": ["model", "provider", "configuration", "design", "settings", "cost",
                        "timing", "trial identity", "trace"],
             "blinding_limitations": limitations}
    ref = _write_json(bundle, f"review/batch-{batch_number}.json", batch)
    sheet = _write_json(bundle, f"review/labels-batch-{batch_number}.json", label_sheet(batch))
    bundle.append("review_batch", batch=batch_number, file=ref, label_sheet=sheet,
                  identity=identity, seed=seed, blinding_limitations=limitations,
                  no_answer_trials=no_answer)
    _write_json(bundle, IDENTITY_MAP, {**mapping, **identity})
    return batch


def label_sheet(batch: dict) -> dict:
    """A blank sheet for the author's initial labels: one entry per criterion and per designated
    critical error. Blank stays unscored; nothing is pre-filled."""
    return {"batch": batch["batch"], "assessor": "", "items": [
        {"review_id": item["review_id"], "case_id": item["case_id"],
         "labels": {c: {"score": None, "excerpt": "", "evidence_ref": "", "reason": ""}
                    for c in item["anchors"]["criteria"]},
         "critical_errors": {e["id"]: {"present": None, "excerpt": "", "reason": ""}
                             for e in item["anchors"]["critical_errors"]}}
        for item in batch["items"]]}


def import_label_sheet(bundle: RunBundle, sheet: dict) -> dict:
    """Record a filled sheet as initial human labels. Every entry is validated before anything is
    written, so a bad sheet records nothing. Blank entries stay unscored."""
    assessor = sheet.get("assessor", "").strip()
    if not assessor:
        raise assessment.AssessmentError("the sheet names its assessor")
    known = identity_map(bundle)
    labels, flags = [], []
    for item in sheet["items"]:
        if item["review_id"] not in known:
            raise assessment.AssessmentError(f"unknown review ID {item['review_id']}")
        gold = assessment.load_gold(item["case_id"])
        for criterion, entry in item["labels"].items():
            if entry["score"] is None:
                continue
            assessment.validate_label(gold, item["case_id"], criterion, entry["score"],
                                      entry["reason"])
            if assessment.existing_labels(bundle, item["review_id"], criterion):
                raise assessment.AssessmentError(
                    f"{item['review_id']} already has a {criterion} label; revise it explicitly")
            labels.append((item, criterion, entry))
        for error_id, entry in item["critical_errors"].items():
            if entry["present"] is None:
                continue
            assessment.validate_flag(gold, item["case_id"], error_id, entry["reason"])
            if assessment.existing_flags(bundle, item["review_id"], error_id):
                raise assessment.AssessmentError(
                    f"{item['review_id']} already has a {error_id} flag; revise it explicitly")
            flags.append((item, error_id, entry))
    for item, criterion, entry in labels:
        assessment.record_label(bundle, review_id=item["review_id"], case_id=item["case_id"],
                                criterion=criterion, score=entry["score"], excerpt=entry["excerpt"],
                                evidence_ref=entry["evidence_ref"], reason=entry["reason"],
                                assessor=assessor)
    for item, error_id, entry in flags:
        assessment.record_critical(bundle, review_id=item["review_id"], case_id=item["case_id"],
                                   error_id=error_id, present=bool(entry["present"]),
                                   excerpt=entry["excerpt"], reason=entry["reason"],
                                   assessor=assessor)
    return {"labels": len(labels), "critical_flags": len(flags)}


LABEL_EVENTS = ("label", "critical_flag", "assistant_note")


def export_labels(bundle: RunBundle) -> dict:
    """Write every assessment event so far, full history included, to a new numbered file. An
    export with nothing new returns the latest version instead of writing a duplicate."""
    events = [e for e in bundle.events() if e["type"] in LABEL_EVENTS]
    exports = [e for e in bundle.events() if e["type"] == "labels_exported"]
    last_seq = events[-1]["seq"] if events else 0
    if exports and exports[-1]["last_seq"] == last_seq:
        return exports[-1]
    version = len(exports) + 1
    data = {"schema": "comparison-labels/1", "version": version, "run_id": bundle.manifest["run_id"],
            "rubric_version": bundle.manifest.get("rubric_version"), "last_seq": last_seq,
            "events": events}  # review IDs only; the identity map stays in its own file
    ref = _write_json(bundle, f"exports/labels-v{version}.json", data)
    return bundle.append("labels_exported", version=version, file=ref, count=len(events),
                         last_seq=last_seq)


def verify_exports(bundle: RunBundle) -> list[str]:
    """Problems with earlier exports: a changed file, or contents that no longer match the log."""
    problems = []
    log = {e["seq"]: e for e in bundle.events() if e["type"] in LABEL_EVENTS}
    for export in [e for e in bundle.events() if e["type"] == "labels_exported"]:
        try:
            data = json.loads(bundle.read_artifact(export["file"]))
        except (OSError, ValueError) as error:
            problems.append(f"labels-v{export['version']}: {error}")
            continue
        expected = [e for seq, e in sorted(log.items()) if seq <= export["last_seq"]]
        if data["events"] != expected:
            problems.append(f"labels-v{export['version']}: contents differ from the log")
    return problems


def record_effort(bundle: RunBundle, *, batch: int, reviewer: str, minutes: float,
                  answers: int) -> dict:
    return bundle.append("review_effort", batch=batch, reviewer=reviewer, minutes=minutes,
                         answers=answers)


def process_view(bundle: RunBundle, trial_id: str) -> dict:
    """Everything recorded for one trial, for process and security review. Not blinded."""
    events = [e for e in bundle.events() if e.get("trial_id") == trial_id]
    request_ids = {e["request_id"] for e in events if e["type"] == "request_started"}
    events += [e for e in bundle.events() if e["type"] in ("request_finished", "cost_settled",
                                                          "request_unresolved")
               and e.get("request_id") in request_ids]
    return {"trial_id": trial_id, "blinded": False,
            "blinding_note": "process/security review sees the full trace, including identity "
                             "and settings; it is not equivalently blinded",
            "events": sorted(events, key=lambda e: e["seq"])}
