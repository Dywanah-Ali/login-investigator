"""Operator commands for the comparison runner. See docs/admin-manual.md.

    uv run python -m evals.comparison new screening RUN_DIR --adapter dry-run
    uv run python -m evals.comparison run RUN_DIR [--until-slot 24]
    uv run python -m evals.comparison status RUN_DIR
    uv run python -m evals.comparison checks RUN_DIR
    uv run python -m evals.comparison review RUN_DIR --size 6
    uv run python -m evals.comparison labels RUN_DIR SHEET.json
    uv run python -m evals.comparison revise RUN_DIR --review-id R-… --criterion facts --score 1 …
    uv run python -m evals.comparison note RUN_DIR --review-id R-… --text … --assistant …
    uv run python -m evals.comparison effort RUN_DIR --batch 1 --reviewer … --minutes 20 --answers 6
    uv run python -m evals.comparison trace RUN_DIR TRIAL_ID      # process view, not blinded
    uv run python -m evals.comparison rerun RUN_DIR TRIAL_ID --reason … --repair-version …
    uv run python -m evals.comparison select RUN_DIR --chosen CONFIG_ID --rationale … --author …
    uv run python -m evals.comparison export-labels RUN_DIR
    uv run python -m evals.comparison report RUN_DIR
    uv run python -m evals.comparison mirror RUN_DIR      # only with LI_LANGFUSE=on

`dry-run` answers with a fixed text and costs nothing. `openrouter` dispatch requires
`run --execute-paid`, used only after the author's explicit execution go and readiness checks.
Creating a run never loads model keys or sends a request.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from evals.comparison import (
    assessment,
    mirror,
    plans,
    records,
    review,
    runner,
    selection,
)
from evals.comparison.adapters import Adapter, ModelRequest, ModelResponse
from evals.comparison.openrouter import OpenRouterAdapter

RUNS = Path(__file__).parent / "runs"
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
REVIEW_AT_USD = 15.0


class DryRunAdapter(Adapter):
    """No network and no cost: a fixed answer, and a tool call in compatibility sessions."""

    name = "dry-run"
    version = "1"

    def complete(self, request: ModelRequest) -> ModelResponse:
        if request.tools and request.messages[-1]["role"] != "tool":
            return ModelResponse(text="", tool_calls=[{"id": "dry-1", "name": "get_record",
                                                       "arguments": '{"ref": "CMP-1"}'}],
                                 usage={"input": 0, "output": 0}, cost_usd=0.0)
        text = ("Dry run: the colour code is 7 [CMP-1]." if request.tools
                else "Dry run answer: no model was called [C1].")
        return ModelResponse(text=text, usage={"input": 0, "output": 0}, cost_usd=0.0,
                             model_reported="dry-run", provider_reported="dry-run")


ADAPTERS = {"dry-run": DryRunAdapter, "openrouter": OpenRouterAdapter}


def _adapter(name: str) -> Adapter:
    if name not in ADAPTERS:
        raise SystemExit(f"unknown adapter {name!r}; available: {', '.join(ADAPTERS)}")
    return ADAPTERS[name]()


def _open(path: str) -> records.RunBundle:
    root = Path(path)
    if not (root / "manifest.json").is_file():
        raise SystemExit(f"{root} holds no run (no manifest.json)")
    return records.RunBundle.open(root)


def cmd_new(args) -> int:
    adapter = _adapter(args.adapter)
    configs = plans.SCREENING_CONFIGS
    if args.stage == "compatibility":
        cases, passes, designs = [], 1, ["compat"]
    elif args.stage == "screening":
        cases, passes, designs = plans.SCREENING_CASES, plans.SCREENING_PASSES, ["A"]
    else:
        raise SystemExit("architecture calibration waits for the provisional-model selection")
    bundle = runner.new_run(Path(args.run_dir), stage=args.stage, configs=configs,
                            case_ids=cases, passes=passes, designs=designs, adapter=adapter,
                            experiment_id=args.experiment)
    print(f"Created {bundle.root} with {len(bundle.manifest['schedule'])} scheduled trials; "
          f"adapter {adapter.name}; fixtures {bundle.manifest['fixture_version']}; "
          f"prompts {bundle.manifest['prompt_version']}")
    return 0


def cmd_run(args) -> int:
    bundle = _open(args.run_dir)
    adapter = _adapter(bundle.manifest["adapter"]["name"])
    prior_cost = 0.0
    if isinstance(adapter, OpenRouterAdapter):
        if not args.execute_paid:
            raise ValueError("OpenRouter dispatch requires --execute-paid after explicit execution go")
        if args.until_slot is None:
            raise ValueError("paid runs require --until-slot; review cost between bounded batches")
        maximum_slot = max([s["slot"] for s in bundle.manifest["schedule"]] + [
            e["slot"]["slot"] for e in bundle.events() if e["type"] == "rerun_scheduled"])
        if args.until_slot < 1 or args.until_slot > maximum_slot:
            raise ValueError("paid --until-slot must name a slot in the frozen schedule")
        if (bundle.manifest["stage"] == "screening" and args.until_slot > 24
                and not args.after_setup_review):
            raise ValueError("later screening passes await the first-24 setup review")
        if bundle.manifest["stage"] == "screening" and args.until_slot > 24:
            closed = {e["trial_id"] for e in bundle.events()
                      if e["type"] in ("trial_finished", "trial_interrupted")}
            if any(s["trial_id"] not in closed for s in bundle.manifest["schedule"][:24]):
                raise ValueError("finish the first 24 results before recording their setup review")
        related = [_open(path) for path in args.cost_run]
        roots = [bundle.root.resolve(), *(b.root.resolve() for b in related)]
        if len(roots) != len(set(roots)):
            raise ValueError("cost bundles must be distinct; do not count a run twice")
        if any(b.manifest["adapter"]["name"] != "openrouter" for b in related):
            raise ValueError("paid cost context cannot contain a dry run")
        if (bundle.manifest["stage"] == "screening"
                and not any(b.manifest["stage"] == "compatibility" for b in related)):
            raise ValueError("paid screening requires its compatibility bundle via --cost-run")
        prior_cost = sum(records.resources(b)["total"]["known_cost_usd"] for b in related)
        unknown = sum(records.resources(b)["total"]["unknown_cost_requests"] for b in related)
        print(f"Related runs: known cost US${prior_cost:.4f}; {unknown} unknown-cost request(s).")
        from dotenv import dotenv_values

        env = {**{k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None}, **os.environ}
        key = env.get("OPENROUTER_API_KEY", "")
        if not key.strip():
            raise ValueError("OPENROUTER_API_KEY is missing or empty")
        adapter = OpenRouterAdapter(key)
        bundle.append("spending_context", related_runs=[b.manifest["run_id"] for b in related],
                      known_cost_usd=prior_cost, unknown_cost_requests=unknown,
                      spending_review_confirmed=args.after_spending_review,
                      setup_review_confirmed=args.after_setup_review)
    result = runner.Runner(bundle, adapter).run(
        until_slot=args.until_slot,
        stop_cost_usd=(REVIEW_AT_USD if isinstance(adapter, OpenRouterAdapter)
                       and not args.after_spending_review else None), prior_cost_usd=prior_cost,
        reruns_only=args.reruns_only)
    if result["stop_reason"]:
        print(f"REVIEW POINT: {result['stop_reason']}.")
    recovery = result["recovery"]
    if recovery["unresolved_requests"] or recovery["interrupted_trials"]:
        print(f"Recovered after an interruption: {len(recovery['interrupted_trials'])} trial(s) "
              f"marked interrupted, {len(recovery['unresolved_requests'])} request(s) marked "
              "unresolved with unknown cost. None was sent again.")
    print(f"Ran {len(result['ran'])} trial(s).")
    return cmd_status(args)


def cmd_status(args) -> int:
    bundle = _open(args.run_dir)
    states = records.trial_states(bundle)
    total = records.resources(bundle)["total"]
    counts: dict[str, int] = {}
    for state in states.values():
        counts[state] = counts.get(state, 0) + 1
    scheduled = {s["trial_id"] for s in bundle.manifest["schedule"]}
    reruns = len(set(states) - scheduled)
    print(f"Stage {bundle.manifest['stage']}: {len(scheduled & set(states))} of {len(scheduled)} "
          f"scheduled trials started, plus {reruns} linked rerun(s); "
          f"{json.dumps(counts, sort_keys=True)}")
    unknown = total["unknown_cost_requests"]
    print(f"Known cost US${total['known_cost_usd']:.4f} over {total['request_count']} requests; "
          f"{unknown} request(s) with unknown cost; {total['retry_count']} retries.")
    if total["known_cost_usd"] >= REVIEW_AT_USD:
        print(f"REVIEW POINT: known spending has reached US${REVIEW_AT_USD:.0f}.")
    if bundle.manifest["stage"] == "screening" and len(states) >= 24:
        print("REVIEW POINT: the first 24 results exist; inspect the setup before continuing.")
    return 0


def cmd_checks(args) -> int:
    bundle = _open(args.run_dir)
    results = assessment.run_deterministic_checks(bundle)
    unresolved = [r for r in results if r["unresolved"]]
    unsupported = [r for r in results if r.get("unsupported_citations")]
    print(f"Reference checks on {len(results)} answers; {len(unresolved)} cite references that "
          f"do not exist in their case file; {len(unsupported)} contain unsupported citation "
          "syntax requiring inspection. No model was called.")
    for result in unresolved:
        print(f"- {result['trial_id']}: {', '.join(result['unresolved'])}")
    for result in unsupported:
        print(f"- {result['trial_id']}: unsupported citation syntax: "
              f"{result['unsupported_citations']!r}")
    return 0


def cmd_review(args) -> int:
    bundle = _open(args.run_dir)
    batch = review.prepare_batch(bundle, size=args.size, seed=args.seed)
    print(f"Blinded batch {batch['batch']}: {len(batch['items'])} answer(s) in "
          f"{bundle.root / 'artifacts' / 'review' / f'batch-{batch['batch']}.json'}")
    if batch["blinding_limitations"]:
        print(f"Blinding limitations recorded for {len(batch['blinding_limitations'])} answer(s).")
    return 0


def cmd_labels(args) -> int:
    bundle = _open(args.run_dir)
    result = review.import_label_sheet(bundle, json.loads(Path(args.sheet).read_text()))
    print(f"Recorded {result['labels']} initial label(s) and {result['critical_flags']} "
          "critical-error flag(s). Blank entries stay unscored.")
    return 0


def _parse_score(value: str):
    return "n/a" if value == "n/a" else int(value)


def cmd_revise(args) -> int:
    bundle = _open(args.run_dir)
    case_id = _case_of(bundle, args.review_id)
    if args.criterion:
        earlier = assessment.existing_labels(bundle, args.review_id, args.criterion)
        if not earlier:
            raise assessment.AssessmentError(f"no {args.criterion} label to revise; use `labels`")
        event = assessment.record_label(
            bundle, review_id=args.review_id, case_id=case_id, criterion=args.criterion,
            score=_parse_score(args.score), excerpt=args.excerpt, evidence_ref=args.evidence_ref,
            reason=args.reason, assessor=args.assessor, revises=earlier[-1]["seq"])
    else:
        earlier = assessment.existing_flags(bundle, args.review_id, args.error_id)
        if not earlier:
            raise assessment.AssessmentError(f"no {args.error_id} flag to revise; use `labels`")
        event = assessment.record_critical(
            bundle, review_id=args.review_id, case_id=case_id, error_id=args.error_id,
            present=args.present == "true", excerpt=args.excerpt, reason=args.reason,
            assessor=args.assessor, revises=earlier[-1]["seq"])
    print(f"Recorded revision {event['seq']}, revising {event['revises']}. History kept.")
    return 0


def _case_of(bundle: records.RunBundle, review_id: str) -> str:
    trial = review.identity_map(bundle).get(review_id)
    if trial is None:
        raise assessment.AssessmentError(f"unknown review ID {review_id}")
    return next(e["case_id"] for e in bundle.events()
                if e["type"] == "trial_started" and e["trial_id"] == trial)


def cmd_note(args) -> int:
    bundle = _open(args.run_dir)
    assessment.record_assistant_note(bundle, review_id=args.review_id,
                                     case_id=_case_of(bundle, args.review_id), text=args.text,
                                     assistant=args.assistant)
    print("Recorded the assistant note. It is assistance, not an independent human assessment.")
    return 0


def cmd_effort(args) -> int:
    bundle = _open(args.run_dir)
    review.record_effort(bundle, batch=args.batch, reviewer=args.reviewer, minutes=args.minutes,
                         answers=args.answers)
    print(f"Recorded {args.minutes} minute(s) for {args.answers} answer(s) in batch {args.batch}.")
    return 0


def cmd_trace(args) -> int:
    print(json.dumps(review.process_view(_open(args.run_dir), args.trial_id), indent=2))
    return 0


def cmd_rerun(args) -> int:
    bundle = _open(args.run_dir)
    new_id = runner.schedule_rerun(bundle, args.trial_id, reason=args.reason,
                                   repair_version=args.repair_version)
    print(f"Scheduled {new_id}, linked to {args.trial_id}. The original stays in the record. "
          "The next `run` executes it.")
    return 0


def cmd_select(args) -> int:
    bundle = _open(args.run_dir)
    chosen = None if args.none else args.chosen
    if chosen is not None and chosen not in {c["config_id"] for c in bundle.manifest["configs"]}:
        raise assessment.AssessmentError(f"unknown configuration {chosen}")
    selection.record_rationale(bundle, chosen=chosen, rationale=args.rationale, author=args.author)
    print("Recorded the selection rationale." if chosen else
          "Recorded that no configuration was selected, with the diagnosis.")
    return 0


def cmd_export_labels(args) -> int:
    bundle = _open(args.run_dir)
    export = review.export_labels(bundle)
    problems = review.verify_exports(bundle)
    print(f"Labels version {export['version']}: {export['count']} assessment event(s) in "
          f"{bundle.root / export['file']['path']}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


def cmd_mirror(args) -> int:
    from dotenv import dotenv_values

    bundle = _open(args.run_dir)
    env = {**{k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None}, **os.environ}
    try:
        settings = mirror.MirrorSettings.from_env(env)
    except mirror.MirrorDisabled as off:
        print(off)
        return 0
    result = mirror.mirror(bundle, mirror.LangfuseHttp(settings),
                           resend_unresolved=args.resend_unresolved)
    print(f"Mirror: {result['sent']} sent, {result['skipped']} already sent or waiting, "
          f"{result['failed']} failed, {result['unresolved']} unresolved. Local records unchanged.")
    for key in result["failures"]:
        print(f"NOT MIRRORED: {key}")
    return 1 if result["failures"] else 0


def cmd_report(args) -> int:
    bundle = _open(args.run_dir)
    print(json.dumps(selection.report(bundle), indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m evals.comparison",
                                     description="T54 comparison runner (dry-run or explicitly paid)")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="freeze a new run")
    new.add_argument("stage", choices=["compatibility", "screening"])
    new.add_argument("run_dir")
    new.add_argument("--adapter", required=True)
    new.add_argument("--experiment", default=f"t54-{time.strftime('%Y%m%d')}")
    new.set_defaults(func=cmd_new)
    run = sub.add_parser("run", help="run every trial not yet started")
    run.add_argument("run_dir")
    run.add_argument("--until-slot", type=int)
    run.add_argument("--execute-paid", action="store_true",
                     help="allow OpenRouter calls only after explicit execution authorisation")
    run.add_argument("--after-setup-review", action="store_true",
                     help="continue beyond 24 screening slots after the setup review")
    run.add_argument("--after-spending-review", action="store_true",
                     help="continue after the US$15 spending review")
    run.add_argument("--cost-run", action="append", default=[],
                     help="related paid bundle whose costs share this budget; repeat as needed")
    run.add_argument("--reruns-only", action="store_true",
                     help="run only explicitly linked repairs, leaving pending original slots alone")
    run.set_defaults(func=cmd_run)
    for name, func, text in (("status", cmd_status, "trial states and actual cost"),
                             ("checks", cmd_checks, "offline reference checks"),
                             ("report", cmd_report, "the selection report")):
        command = sub.add_parser(name, help=text)
        command.add_argument("run_dir")
        command.set_defaults(func=func)
    rev = sub.add_parser("review", help="prepare the next blinded review batch")
    rev.add_argument("run_dir")
    rev.add_argument("--size", type=int, default=6)
    rev.add_argument("--seed", type=int)
    rev.set_defaults(func=cmd_review)
    labels = sub.add_parser("labels", help="record a filled label sheet as initial human labels")
    labels.add_argument("run_dir")
    labels.add_argument("sheet")
    labels.set_defaults(func=cmd_labels)
    revise = sub.add_parser("revise", help="revise one human label or critical flag, with a reason")
    revise.add_argument("run_dir")
    revise.add_argument("--review-id", required=True)
    target = revise.add_mutually_exclusive_group(required=True)
    target.add_argument("--criterion")
    target.add_argument("--error-id")
    revise.add_argument("--score", help="0, 1, 2 or n/a (with --criterion)")
    revise.add_argument("--present", choices=["true", "false"], help="with --error-id")
    revise.add_argument("--reason", required=True)
    revise.add_argument("--assessor", required=True)
    revise.add_argument("--excerpt", default="")
    revise.add_argument("--evidence-ref", default="")
    revise.set_defaults(func=cmd_revise)
    note = sub.add_parser("note", help="assistant note, only after the author's initial labels")
    note.add_argument("run_dir")
    note.add_argument("--review-id", required=True)
    note.add_argument("--text", required=True)
    note.add_argument("--assistant", required=True)
    note.set_defaults(func=cmd_note)
    effort = sub.add_parser("effort", help="record the time a review batch took")
    effort.add_argument("run_dir")
    effort.add_argument("--batch", type=int, required=True)
    effort.add_argument("--reviewer", required=True)
    effort.add_argument("--minutes", type=float, required=True)
    effort.add_argument("--answers", type=int, required=True)
    effort.set_defaults(func=cmd_effort)
    trace = sub.add_parser("trace", help="the full, unblinded trace of one trial")
    trace.add_argument("run_dir")
    trace.add_argument("trial_id")
    trace.set_defaults(func=cmd_trace)
    rerun = sub.add_parser("rerun", help="schedule an explicit, versioned rerun after a setup fix")
    rerun.add_argument("run_dir")
    rerun.add_argument("trial_id")
    rerun.add_argument("--reason", required=True)
    rerun.add_argument("--repair-version", required=True)
    rerun.set_defaults(func=cmd_rerun)
    select = sub.add_parser("select", help="record the author's selection and rationale")
    select.add_argument("run_dir")
    choice = select.add_mutually_exclusive_group(required=True)
    choice.add_argument("--chosen")
    choice.add_argument("--none", action="store_true", help="no configuration qualifies")
    select.add_argument("--rationale", required=True)
    select.add_argument("--author", required=True)
    select.set_defaults(func=cmd_select)
    export = sub.add_parser("export-labels", help="write a new numbered label export")
    export.add_argument("run_dir")
    export.set_defaults(func=cmd_export_labels)
    mirror_cmd = sub.add_parser("mirror", help="copy saved records to Langfuse (LI_LANGFUSE=on)")
    mirror_cmd.add_argument("run_dir")
    mirror_cmd.add_argument("--resend-unresolved", action="store_true",
                            help="after checking Langfuse, resend traces whose upload got no answer")
    mirror_cmd.set_defaults(func=cmd_mirror)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (assessment.AssessmentError, FileExistsError, KeyError, ValueError) as refused:
        print(f"REFUSED: {refused}. Nothing was recorded.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
