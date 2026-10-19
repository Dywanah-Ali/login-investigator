"""Real LangChain execution signals, using offline tools and fake models."""

from threading import Barrier, Event

import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import ToolException, tool
from langgraph.checkpoint.memory import InMemorySaver

from login_investigator.agent import ask, history
from test_agent import FakeModel, tool_call


def graph(tools, requests):
    model = FakeModel(responses=[AIMessage('', tool_calls=requests), AIMessage('Answer'),
                                 AIMessage('Follow-up')])
    return create_agent(model, tools, checkpointer=InMemorySaver())


@pytest.mark.parametrize('duplicate_name', [False, True])
def test_parallel_calls_keep_distinct_lifecycles_and_saved_followup(duplicate_name):
    barrier, release = Barrier(2), Event()

    @tool
    def search_logins(number: int) -> str:
        """Controlled offline search."""
        barrier.wait(timeout=5)
        assert release.wait(5)
        return f'PRIVATE output {number}'

    @tool
    def lookup_ip_reputation(number: int) -> str:
        """Controlled offline reputation lookup."""
        barrier.wait(timeout=5)
        assert release.wait(5)
        return f'PRIVATE output {number}'

    other = 'search_logins' if duplicate_name else 'lookup_ip_reputation'
    requests = [tool_call('search_logins', {'number': 1}, 'one').tool_calls[0],
                tool_call(other, {'number': 2}, 'two').tool_calls[0]]
    agent = graph([search_logins, lookup_ip_reputation], requests)
    stream = ask(agent, 'parallel-case', 'Investigate', lifecycle=True)
    try:
        starts = [next(stream), next(stream)]
        assert [event.phase for event in starts] == ['start', 'start']
        assert len({event.call_id for event in starts}) == 2
        assert {event.value for event in starts} == {'search_logins', other}
        release.set()
        remaining = list(stream)
    finally:
        release.set()
        stream.close()
    ends = [event for event in remaining if event.kind == 'tool']
    assert {event.call_id for event in ends} == {event.call_id for event in starts}
    assert [event.phase for event in ends] == ['end', 'end']
    assert all('PRIVATE' not in event.value for event in [*starts, *ends])
    assert ''.join(event.value for event in remaining if event.kind == 'text') == 'Answer'
    assert len(history(agent, 'parallel-case')[0].tools) == 2
    list(ask(agent, 'parallel-case', 'Continue', lifecycle=True))
    assert [turn.answer for turn in history(agent, 'parallel-case')] == ['Answer', 'Follow-up']
    assert history(agent, 'unrelated-case') == []


def test_unexecuted_model_request_does_not_emit_tool_progress():
    @tool
    def lookup_ip_reputation() -> str:
        """Offline unused lookup."""
        return 'unused'

    request = tool_call('search_logins', {}, 'missing-tool').tool_calls[0]
    agent = graph([lookup_ip_reputation], [request])
    events = list(ask(agent, 'invalid-request', 'Investigate', lifecycle=True))
    assert all(event.kind != 'tool' for event in events)
    assert ''.join(event.value for event in events) == 'Answer'


@pytest.mark.parametrize('handled', [False, True])
def test_tool_failure_emits_terminal_signal_without_private_details(handled):
    @tool
    def search_logins() -> str:
        """Controlled failing offline tool."""
        raise ToolException('PRIVATE error')

    search_logins.handle_tool_error = handled
    agent = graph([search_logins], [tool_call('search_logins', {}, 'failure').tool_calls[0]])
    stream = ask(agent, 'failure-case', 'Investigate', lifecycle=True)
    started = next(stream)
    ended = next(stream)
    assert started.phase == 'start'
    assert ended.phase == ('end' if handled else 'error')
    assert ended.call_id == started.call_id
    assert started.value == ended.value == 'search_logins'
    if handled:
        assert ''.join(event.value for event in stream if event.kind == 'text') == 'Answer'
    else:
        with pytest.raises(ToolException, match='PRIVATE error'):
            list(stream)
