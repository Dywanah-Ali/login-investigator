import { describe, expect, test } from 'vitest'

import { cutNames, explorerLink, investigateLink, investigateQuestion } from '@/lib/alerts'
import type { Alert } from '@/lib/api'

// The contract's example alert: one IP, two users, a window that crosses midnight.
const ALERT: Alert = {
  rule: 'brute_force',
  summary: 'written by the core',
  ips: ['198.51.100.7', '203.0.113.9'],
  users: ['alice.k', 'bob.m'],
  event_count: 23,
  failure_count: 22,
  success_count: 1,
  first_seen: '2026-10-07T23:10:00Z',
  last_seen: '2026-10-08T00:05:00Z',
  evidence: [],
  evidence_shown: 0,
}

describe('names are cut to three, then "and N more"', () => {
  test('three names or fewer are all shown', () => {
    expect(cutNames([])).toBe('')
    expect(cutNames(['alice.k'])).toBe('alice.k')
    expect(cutNames(['alice.k', 'bob.m', 'carol.p'])).toBe('alice.k, bob.m, carol.p')
  })

  test('a fourth name becomes "and 1 more"', () => {
    expect(cutNames(['alice.k', 'bob.m', 'carol.p', 'dan.r'])).toBe(
      'alice.k, bob.m, carol.p and 1 more',
    )
  })

  test('S2 sprayed 35 accounts: three shown and 32 more', () => {
    const accounts = Array.from({ length: 35 }, (_, i) => `user${i + 1}`)
    expect(cutNames(accounts)).toBe('user1, user2, user3 and 32 more')
  })
})

describe('"Open in Log explorer"', () => {
  test('is the explorer with the first IP and the first and last dates, and nothing else', () => {
    expect(explorerLink(ALERT)).toBe('/explorer?ip=198.51.100.7&from=2026-10-07&to=2026-10-08')
  })

  test('an alert within one day opens that one day', () => {
    const oneDay = { ...ALERT, first_seen: '2026-10-08T01:12:07Z', last_seen: '2026-10-08T02:31:44Z' }
    expect(explorerLink(oneDay)).toBe('/explorer?ip=198.51.100.7&from=2026-10-08&to=2026-10-08')
  })
})

describe('"Investigate"', () => {
  test('asks about the rule, the first IP, the first user and the window, in the contract wording', () => {
    expect(investigateQuestion(ALERT, 'Brute force')).toBe(
      'Investigate the Brute force alert: 198.51.100.7 against alice.k ' +
        'from 2026-10-07 23:10:00 to 2026-10-08 00:05:00 UTC.',
    )
  })

  test('links to the Investigator with the question in the address', () => {
    const link = new URL(investigateLink(ALERT, 'Brute force'), 'http://localhost')
    expect(link.pathname).toBe('/investigator')
    expect([...link.searchParams.keys()]).toEqual(['ask'])
    expect(link.searchParams.get('ask')).toBe(
      'Investigate the Brute force alert: 198.51.100.7 against alice.k ' +
        'from 2026-10-07 23:10:00 to 2026-10-08 00:05:00 UTC.',
    )
  })
})
