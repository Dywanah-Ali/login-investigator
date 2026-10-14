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
  row_count: 1856,
}

export const OVERVIEW = {
  summary: {
    total: 1856,
    successes: 1700,
    failures: 156,
    distinct_users: 41,
    distinct_ips: 37,
    distinct_countries: 6,
    first_seen: '2026-10-01T09:02:57Z',
    last_seen: '2026-10-08T08:59:40Z',
  },
  alert_count: 5,
  hourly: [
    { hour: '2026-10-07T23:00:00Z', outcome: 'failure', events: 88 },
    { hour: '2026-10-07T23:00:00Z', outcome: 'success', events: 3 },
  ],
  top_failed_ips: [{ source_ip: '198.51.100.7', failures: 150, accounts: 1 }],
}

export const EMPTY_OVERVIEW = {
  summary: {
    total: 0,
    successes: 0,
    failures: 0,
    distinct_users: 0,
    distinct_ips: 0,
    distinct_countries: 0,
    first_seen: null,
    last_seen: null,
  },
  alert_count: 0,
  hourly: [],
  top_failed_ips: [],
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
