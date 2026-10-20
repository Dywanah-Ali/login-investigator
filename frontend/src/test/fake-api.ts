import { vi } from 'vitest'

// A stand-in for the API at the HTTP boundary: each path answers with a fixed status and body.
// Tests read what the screen shows and which requests it sent, never how it got there.

type Reply = { status?: number; body: unknown } | 'network-down'

export const DATASET = {
  captured_at: '2026-10-08T09:00:00Z',
  label: 'Synthetic data',
  first_date: '2026-10-01',
  last_date: '2026-10-08',
  countries: ['DE', 'GB', 'RU'],
  users: ['alice.k', 'bob.m'],
}

export const OVERVIEW = {
  summary: { total: 1856, failures: 156, distinct_users: 41 },
  alert_count: 5,
  hourly: [
    { hour: '2026-10-07T23:00:00Z', outcome: 'failure', events: 88 },
    { hour: '2026-10-07T23:00:00Z', outcome: 'success', events: 3 },
  ],
  top_failed_ips: [{ source_ip: '198.51.100.7', failures: 150, accounts: 1 }],
}

export const EMPTY_OVERVIEW = {
  summary: { total: 0, failures: 0, distinct_users: 0 },
  alert_count: 0,
  hourly: [],
  top_failed_ips: [],
}

const row = (timestamp_utc: string, username: string, source_ip: string, country: string,
  outcome: 'success' | 'failure', failure_reason = '') => ({
  timestamp_utc, username, source_ip, country, outcome, failure_reason, user_agent: 'curl/8.4.0',
})

// Two alerts, newest first as the core sorts them. The spraying alert is cut: 2 of 23 events.
export const ALERTS = {
  alerts: [
    {
      rule: 'new_country',
      summary: 'olivia.bennett signed in from RU for the first time.',
      ips: ['91.142.73.116'],
      users: ['olivia.bennett'],
      event_count: 1, failure_count: 0, success_count: 1,
      first_seen: '2026-10-06T13:47:12Z', last_seen: '2026-10-06T13:47:12Z',
      evidence: [row('2026-10-06T13:47:12Z', 'olivia.bennett', '91.142.73.116', 'RU', 'success')],
      evidence_shown: 1,
    },
    {
      rule: 'password_spraying',
      summary: '2.57.122.53 failed on 4 accounts within an hour.',
      ips: ['2.57.122.53'],
      users: ['admin', 'backup', 'helpdesk', 'test'],
      event_count: 23, failure_count: 23, success_count: 0,
      first_seen: '2026-10-05T23:04:00Z', last_seen: '2026-10-06T00:17:29Z',
      evidence: [
        row('2026-10-05T23:04:00Z', 'admin', '2.57.122.53', 'RO', 'failure', 'unknown_user'),
        row('2026-10-06T00:17:29Z', 'test', '2.57.122.53', 'RO', 'failure', 'unknown_user'),
      ],
      evidence_shown: 2,
    },
  ],
}

export const RULES = {
  rules: [
    { rule: 'brute_force', title: 'Brute force', fires_when: 'Twenty failures.', assumption: 'Staff mistype less.', severity: 'medium', severity_reason: 'Failures on one account need review.' },
    { rule: 'password_spraying', title: 'Password spraying', fires_when: 'Ten accounts.', assumption: 'A list is worked through.', severity: 'medium', severity_reason: 'Failures across many accounts.' },
    { rule: 'success_after_failures', title: 'Success after repeated failures', fires_when: 'A success after ten failures.', assumption: 'Staff succeed within two tries.', severity: 'high', severity_reason: 'Check urgently whether it was authorized.' },
    { rule: 'new_country', title: 'Sign-in from a new country', fires_when: 'A new country.', assumption: 'Five sign-ins are enough.', severity: 'low', severity_reason: 'An unfamiliar country is a lead.' },
  ],
  general_assumptions: ['Thresholds fit this dataset.', 'Usernames ignore case.'],
  severity_note: 'Rule default. A report can rate the case higher or lower.',
}

export function fakeApi(replies: Record<string, Reply>) {
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = new URL(String(input), 'http://localhost')
    const reply = replies[url.pathname]
    if (reply === 'network-down') throw new TypeError('Failed to fetch: connection refused')
    if (!reply) return new Response('{}', { status: 404 })
    return new Response(JSON.stringify(reply.body), {
      status: reply.status ?? 200,
      headers: { 'Content-Type': 'application/json' },
    })
  })
  vi.stubGlobal('fetch', fetchMock)

  return {
    /** The paths and query strings the screen asked for, in order. */
    requests: () =>
      fetchMock.mock.calls.map(([input]) => {
        const url = new URL(String(input), 'http://localhost')
        return url.pathname + url.search
      }),
  }
}
