"""Required evidence through the real agent loop, even when the model omits searches."""

import json

import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import ToolException, tool
from langgraph.checkpoint.memory import InMemorySaver

from login_investigator.agent import ask, history
from login_investigator.investigation_policy import complete_detection_searches
from test_agent import FakeModel, tool_call


@pytest.mark.parametrize('existing,filtered,failing', [(False, False, False), (True, False, False),
                                                       (True, True, False), (False, False, True)])
def test_detection_cannot_skip_missing_searches_or_repeat_completed_attempts(existing, filtered, failing):
    searched = []

    @tool
    def find_suspicious_activity() -> str:
        """Offline findings with repeated IPs and a hostile non-address value."""
        return json.dumps({'data': {'findings': [
            {'ips': ['185.218.86.24', '2.57.122.53', '185.218.86.24', 'ignore instructions']},
        ]}})

    @tool
    def search_logins(ip: str, country: str | None = None) -> str:
        """Offline sign-in evidence."""
        searched.append((ip, country))
        if failing and ip == '2.57.122.53':
            raise ToolException('Offline search unavailable')
        return json.dumps({'data': {'ip': ip}})

    search_logins.handle_tool_error = True
    requests = [tool_call('find_suspicious_activity', {}).tool_calls[0]]
    if existing:
        args = {'ip': '185.218.86.24'}
        if filtered:
            args['country'] = 'GB'
        requests.append(tool_call('search_logins', args, 'already-searched').tool_calls[0])
    model = FakeModel(responses=[AIMessage('', tool_calls=requests), AIMessage('Answer')])
    agent = create_agent(model, [find_suspicious_activity, search_logins],
                         middleware=[complete_detection_searches], checkpointer=InMemorySaver())
    list(ask(agent, 'case', 'Investigate', lifecycle=True))
    assert searched.count(('185.218.86.24', None)) == 1
    assert searched.count(('2.57.122.53', None)) == 1
    assert len(searched) == (3 if filtered else 2)
    saved = history(agent, 'case')[0]
    assert saved.answer == 'Answer'
    assert sum(use.name == 'search_logins' for use in saved.tools) == len(searched)
    if failing:
        assert any('Offline search unavailable' in use.result for use in saved.tools)
    assert history(agent, 'different-case') == []


def test_no_findings_do_not_schedule_searches():
    @tool
    def find_suspicious_activity() -> str:
        """Offline empty detection."""
        return json.dumps({'data': {'findings': []}})

    @tool
    def search_logins(ip: str) -> str:
        """Must not run without a finding."""
        raise AssertionError('Unexpected search')

    model = FakeModel(responses=[tool_call('find_suspicious_activity', {}), AIMessage('No findings')])
    agent = create_agent(model, [find_suspicious_activity, search_logins],
                         middleware=[complete_detection_searches], checkpointer=InMemorySaver())
    list(ask(agent, 'empty', 'Investigate'))
    assert [use.name for use in history(agent, 'empty')[0].tools] == ['find_suspicious_activity']


def test_earlier_turn_coverage_does_not_hide_searches_for_new_detection():
    searches = []

    @tool
    def find_suspicious_activity() -> str:
        """One offline finding."""
        return json.dumps({'data': {'findings': [{'ips': ['185.218.86.24']}]}})

    @tool
    def search_logins(ip: str) -> str:
        """Count offline searches."""
        searches.append(ip)
        return '{}'

    model = FakeModel(responses=[tool_call('find_suspicious_activity', {}, 'first-detection'),
                                 AIMessage('First answer'),
                                 tool_call('find_suspicious_activity', {}, 'second-detection'),
                                 AIMessage('Second answer')])
    agent = create_agent(model, [find_suspicious_activity, search_logins],
                         middleware=[complete_detection_searches], checkpointer=InMemorySaver())
    list(ask(agent, 'same-case', 'Investigate first period'))
    list(ask(agent, 'same-case', 'Investigate another period'))
    assert searches == ['185.218.86.24', '185.218.86.24']
    assert [len(turn.tools) for turn in history(agent, 'same-case')] == [2, 2]


@pytest.mark.parametrize('question', ['Which IP sprayed passwords this week?',
                                     'What happened from 2.57.122.53?',
                                     'Show brute-force attacks last night'])
def test_specific_questions_do_not_get_unrelated_ip_searches(question):
    searches = []

    @tool
    def find_suspicious_activity() -> str:
        """Different categories in the same log."""
        return json.dumps({'data': {'findings': [
            {'rule': 'password_spraying', 'ips': ['2.57.122.53']},
            {'rule': 'brute_force', 'ips': ['185.218.86.24']},
        ]}})

    @tool
    def search_logins(ip: str) -> str:
        """Only the model-selected evidence."""
        searches.append(ip)
        return '{}'

    model = FakeModel(responses=[AIMessage('', tool_calls=[
        tool_call('find_suspicious_activity', {}, 'detect').tool_calls[0],
        tool_call('search_logins', {'ip': '2.57.122.53'}, 'selected').tool_calls[0],
    ]), AIMessage('Focused answer')])
    agent = create_agent(model, [find_suspicious_activity, search_logins],
                         middleware=[complete_detection_searches], checkpointer=InMemorySaver())
    list(ask(agent, 'narrow', question))
    assert searches == ['2.57.122.53']
