"""Investigation transport: validate requests, call the core, shape the contract's replies."""

import json
import logging
from collections.abc import AsyncIterator, Generator, Iterator
from datetime import datetime, timezone
from typing import Annotated, cast

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel, field_validator
from starlette.concurrency import run_in_threadpool

from api.errors import ApiError
from api.services import Services, services
from api.sse_disconnect import DisconnectSafeRoute
from login_investigator import agent, investigations, report_pdf, tool_views
from login_investigator.loader import TIMESTAMP_FORMAT

router = APIRouter()
log = logging.getLogger(__name__)
Server = Annotated[Services, Depends(services)]


class Question(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def valid_question(cls, value: str) -> str:
        value = value.strip()
        if not 1 <= len(value) <= 2000:
            raise ApiError(422, "invalid_question", "question must be 1 to 2,000 characters after trimming.")
        return value


def available(svc: Server) -> Services:
    if svc.agent is None:
        raise ApiError(503, "agent_unavailable",
                       "OPENROUTER_API_KEY is not set. Copy env.example to .env and add the key.")
    return svc


Available = Annotated[Services, Depends(available)]


def case_summary(case: investigations.Investigation) -> dict:
    return {"id": case.thread_id, "started_at": case.started_at.strftime(TIMESTAMP_FORMAT),
            "first_question": case.first_question}


def known_case(id: str, svc: Server) -> investigations.Investigation:
    for case in investigations.list_all(svc.settings.memory_path):
        if case.thread_id == id:
            return case
    raise ApiError(404, "not_found", "Not found.")


KnownCase = Annotated[investigations.Investigation, Depends(known_case)]


def turn_views(turns: list[agent.Turn]) -> list[dict]:
    result = []
    number = 0
    for turn in turns:
        tools = []
        for use in turn.tools:
            view = tool_views.describe(use.name, use.args, use.result)
            tools.append({"title": view.title, "asked": view.asked, "found": view.found,
                          "columns": list(view.rows.columns) if view.rows is not None else [],
                          "rows": json.loads(cast(str, view.rows.to_json(orient="records")))
                          if view.rows is not None else None,
                          "raw": view.raw})
        report = None
        if turn.report is not None:
            number += 1
            report = {**turn.report.model_dump(), "number": number}
        result.append({"question": turn.question, "answer": turn.answer,
                       "tools": tools, "report": report})
    return result


@router.get("/investigations")
def list_cases(svc: Available) -> dict:
    return {"investigations": [case_summary(case)
                              for case in investigations.list_all(svc.settings.memory_path)]}


@router.post("/investigations", status_code=201)
def start_case(body: Question, svc: Available) -> dict:
    return case_summary(investigations.start(body.question, svc.settings.memory_path))


@router.get("/investigations/{id}")
def reopen_case(case: KnownCase, svc: Available) -> dict:
    turns = agent.history(svc.agent, case.thread_id)
    return {**case_summary(case), "turns": turn_views(turns),
            "report_offer": agent.report_request(turns)}


def writing(case: KnownCase, svc: Available) -> Iterator[None]:
    """Reserve one Investigation through the response, including stream cancellation.

    Reports use the same reservation so a stale report cannot race an answer or another report.
    The lock protects only the set, never a model call or another Investigation.
    """
    with svc.activity_lock:
        if case.thread_id in svc.active_investigations:
            raise ApiError(409, "busy", "The investigation is busy. Wait for it to finish.")
        svc.active_investigations.add(case.thread_id)
    try:
        yield
    finally:
        with svc.activity_lock:
            svc.active_investigations.remove(case.thread_id)


Writing = Annotated[None, Depends(writing)]


class ReportRequest(BaseModel):
    request: str

    @field_validator("request")
    @classmethod
    def valid_request(cls, value: str) -> str:
        if value not in agent.REPORT_REQUESTS:
            raise ApiError(422, "invalid_request", "request is not valid.")
        return value


@router.post("/investigations/{id}/report")
def write_report(body: ReportRequest, case: KnownCase, svc: Available,
                 reserved: Writing) -> dict:
    turns = agent.history(svc.agent, case.thread_id)
    if body.request != agent.report_request(turns):
        raise ApiError(409, "not_offered", "The requested report is not currently offered.")
    report = agent.write_report(svc.agent, svc.model, case.thread_id, body.request)
    number = sum(turn.report is not None for turn in turns) + 1
    return {**report.model_dump(), "number": number}


@router.get("/investigations/{id}/reports/{number}.pdf")
def download_report(number: int, case: KnownCase, svc: Server) -> Response:
    # Reading saved reports needs the checkpointer, never a model or another agent instance.
    reports = [turn.report for turn in agent.saved_history(svc.memory, case.thread_id)
               if turn.report is not None]
    if number < 1 or number > len(reports):
        raise ApiError(404, "not_found", "Not found.")
    content = report_pdf.build(reports[number - 1], case.thread_id, datetime.now(timezone.utc))
    name = report_pdf.file_name(case.thread_id, number)
    return Response(content, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


def question_stream(body: Question, case: KnownCase, svc: Available,
                    reserved: Writing) -> Iterator[Generator[agent.Stream, None, None]]:
    """Close the core before releasing the writer, even when delivery is cancelled at a yield."""
    stream = agent.ask(svc.agent, case.thread_id, body.question)
    try:
        yield stream
    finally:
        stream.close()


QuestionStream = Annotated[Generator[agent.Stream, None, None], Depends(question_stream)]


async def ask_question(stream: QuestionStream) -> AsyncIterator[ServerSentEvent]:
    try:
        while True:
            # The synchronous core runs in a worker. Cancellation waits for this step, then
            # closes the generator without advancing it again. None marks the end safely.
            item = await run_in_threadpool(next, stream, None)
            if item is None:
                break
            yield ServerSentEvent(event=item.kind,
                                  data={"name" if item.kind == "tool" else "text": item.value})
        yield ServerSentEvent(event="done", data={})
    except Exception:
        log.exception("The agent stream failed")
        yield ServerSentEvent(event="error", data={
            "code": "agent_failed", "message": "The agent stopped before it finished.",
        })


# Opt in only this route; the guard must include ASGI delivery and request cleanup.
router.add_api_route("/investigations/{id}/ask", ask_question, methods=["POST"],
                     response_class=EventSourceResponse, route_class_override=DisconnectSafeRoute)
