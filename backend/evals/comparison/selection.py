"""The provisional-model selection report for the screen (T52, approved 2 November 2026).

A configuration is eligible only when all twelve of its scheduled trials completed, every
applicable criterion of every answer has a human label, every designated critical error has been
assessed and none is flagged present, and no applicable criterion scored 0. An unassessed critical
error is unscored, not absent. A score of 1 is allowed; "n/a" is not a zero; "unscored" is
not a pass. Partial answers from incomplete trials stay as evidence, but those trials are not
complete. While any scheduled trial has not run, nothing is decided: the first-24 checkpoint
never eliminates a candidate.

The report shows per-case profiles, failures and resources side by side. It does not rank, weight
or pick: the author compares eligible profiles case by case, then cost, then speed, and the
rationale is recorded with `record_rationale`.
"""

from __future__ import annotations

from statistics import median

from evals.comparison import assessment, records, review
from evals.comparison.records import RunBundle


def _eligible_versions(bundle: RunBundle) -> dict[str, str]:
    """Scheduled trial ID -> the trial that counts for it: the latest linked rerun, if any."""
    current = {s["trial_id"]: s["trial_id"] for s in bundle.manifest["schedule"]}
    for event in bundle.events():
        if event["type"] == "rerun_scheduled":
            original = event["original_trial_id"]
            root = next((k for k, v in current.items() if v == original), original)
            current[root] = event["trial_id"]
    return current


def report(bundle: RunBundle) -> dict:
    if bundle.manifest["stage"] != "screening":
        raise ValueError("the selection report applies to the screening stage")
    states = records.trial_states(bundle)
    versions = _eligible_versions(bundle)
    slots = {s["trial_id"]: s for s in bundle.manifest["schedule"]}
    by_trial = {trial: review_id for review_id, trial in review.identity_map(bundle).items()}
    finished = {e["trial_id"]: e for e in bundle.events() if e["type"] == "trial_finished"}
    resources = records.resources(bundle)["requests"]
    run_complete = all(states.get(v) not in (None, "started") for v in versions.values())
    rationale = [e for e in bundle.events() if e["type"] == "selection_rationale"]

    configs = {}
    for config in bundle.manifest["configs"]:
        cid = config["config_id"]
        cells = [(scheduled, versions[scheduled]) for scheduled, slot in slots.items()
                 if slot["config_id"] == cid]
        reasons, cases = [], {}
        incomplete = unscored = 0
        for scheduled, trial in cells:
            slot, status = slots[scheduled], states.get(trial, "not_run")
            review_id = by_trial.get(trial)
            prof = (assessment.profile(bundle, review_id, slot["case_id"]) if review_id
                    else {"scores": None, "critical_errors": [], "critical_unassessed": None})
            entry = {"pass": slot["pass"], "trial_id": trial, "status": status,
                     "rerun_of": None if trial == scheduled else scheduled,
                     "review_id": review_id, **prof}
            cases.setdefault(slot["case_id"], []).append(entry)
            if status != "completed":
                incomplete += 1
                reasons.append(f"{trial}: trial {status}")
            if prof["critical_errors"]:
                reasons.append(f"{trial}: critical error {', '.join(prof['critical_errors'])}")
            scores = prof["scores"]
            if status == "completed" and (scores is None or assessment.UNSCORED in scores.values()
                                          or prof["critical_unassessed"]):
                unscored += 1
            if scores:
                reasons += [f"{trial}: {c} scored 0" for c, s in scores.items() if s == 0]
        trial_ids = {t for _, t in cells}
        own = [r for r in resources.values() if r.get("trial_id") in trial_ids]
        durations = [finished[t]["elapsed_s"] for t in trial_ids
                     if t in finished and finished[t]["status"] == "completed"]
        if not run_complete:
            status = "pending_run"
        elif reasons:
            status = "not_eligible"
        elif unscored:
            status = "pending_scoring"
        else:
            status = "eligible"
        configs[cid] = {
            "label": config["label"], "status": status, "scheduled": len(cells),
            "completed": len(cells) - incomplete, "unscored_answers": unscored,
            "reasons": reasons, "cases": cases,
            "resources": {**records.summarise(own),
                          "median_trial_s": median(durations) if durations else None},
        }
    return {"run_complete": run_complete,
            "note": "no ranking or weighted score; compare eligible profiles case by case, then "
                    "cost, then speed; if none is eligible, diagnose rather than promote",
            "configs": configs, "rationale": rationale}


def record_rationale(bundle: RunBundle, *, chosen: str | None, rationale: str, author: str) -> dict:
    """The author's evidence-based choice, or `chosen=None` with the diagnosis when none qualifies."""
    return bundle.append("selection_rationale", chosen=chosen, rationale=rationale, author=author)
