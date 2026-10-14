"""What the server builds once at startup, and how a route gets it.

`start` is the one place each of v1's seams is called: the log is loaded once, the rules run once on
the whole log, the memory is opened once and the agent built once. Every request then reads the
same `Services`. The seams are called through their modules, so each has one name everywhere.

A failure stays inside the part it belongs to: a log that fails validation stops the dataset
endpoints only, and a missing model key stops the Investigation endpoints only.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import pandas as pd
from fastapi import Request
from langgraph.checkpoint.sqlite import SqliteSaver

from api.errors import ApiError
from api.settings import Settings
from login_investigator import agent, investigations, loader, rules
from login_investigator.dashboard import DatasetFacts, dataset_facts

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Dataset:
    """The one loaded log, the rules' findings on the whole of it, and the facts about it."""
    frame: pd.DataFrame
    findings: list[rules.Finding]
    facts: DatasetFacts


@dataclass(frozen=True)
class Services:
    """Everything a request needs, built once at startup."""
    settings: Settings  # the Investigation endpoints need the memory path (ticket 16)
    dataset: Dataset | None  # None when the log failed validation
    dataset_error: str | None  # the loader's message, which names row problems, not secrets
    memory: SqliteSaver
    model: Any | None  # None when the model key is missing; the report writer needs it (ticket 16)
    agent: Any | None  # None when the model key is missing


def start(settings: Settings) -> Services:
    dataset, dataset_error = None, None
    try:
        frame = loader.load_log(settings.log_path)
        # The rules need each user's whole history, so they run once on the whole log.
        dataset = Dataset(frame=frame, findings=rules.detect_all(frame),
                          facts=dataset_facts(frame))
    except loader.LogValidationError as error:
        log.error("The log failed validation: %s", error)
        # The client gets fixed text; the loader's own message stays in the server log. Its
        # missing-file message holds the full path, which can name the machine's user (bug log
        # B-003), and its row messages quote the bad rows' raw log values (B-008).
        dataset_error = ("The log failed validation. The server log lists the problems."
                         if settings.log_path.is_file()
                         else "The configured log file was not found.")

    memory = investigations.open_memory(settings.memory_path)
    model, built = None, None
    try:
        model = agent.make_model()
    except RuntimeError as error:  # the model key is not set; the message names the setting
        log.warning("The agent is unavailable: %s", error)
    if model is not None:
        built = agent.build_agent(model, memory)

    return Services(settings=settings, dataset=dataset, dataset_error=dataset_error,
                    memory=memory, model=model, agent=built)


def services(request: Request) -> Services:
    """A route's dependency: the Services built at startup."""
    return request.app.state.services


def dataset(request: Request) -> Dataset:
    """A dataset endpoint's dependency: the loaded log, or 500 `log_invalid` when it failed."""
    svc = services(request)
    if svc.dataset is None:
        raise ApiError(500, "log_invalid", svc.dataset_error or "The log failed validation.")
    return svc.dataset
