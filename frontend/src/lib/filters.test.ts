import { describe, expect, test } from 'vitest'

import { clearFilters, filterQuery, readFilters, withFilter } from '@/lib/filters'

describe('the filters in the address bar', () => {
  test('reading the address keeps the five filters and ignores anything else', () => {
    const search = new URLSearchParams(
      'from=2026-10-01&to=2026-10-03&outcome=failure&country=RU&user=alice.k&page=2',
    )
    expect(readFilters(search)).toEqual({
      from: '2026-10-01',
      to: '2026-10-03',
      outcome: 'failure',
      country: 'RU',
      user: 'alice.k',
    })
  })

  test('an empty box in the address means "all", so it is not a filter', () => {
    expect(readFilters(new URLSearchParams('from=&outcome=  &user=bob.m'))).toEqual({ user: 'bob.m' })
  })

  test('the request carries the filters in a fixed order and leaves empty ones out', () => {
    expect(filterQuery({ user: 'alice.k', outcome: '', from: '2026-10-01' })).toBe(
      'from=2026-10-01&user=alice.k',
    )
  })

  test('no filters means the whole log: the request carries nothing', () => {
    expect(filterQuery({})).toBe('')
  })

  test('a value with URL characters survives the trip to the address and back', () => {
    const query = filterQuery({ user: 'a&b=c d' })
    expect(query).toBe('user=a%26b%3Dc+d')
    expect(readFilters(new URLSearchParams(query))).toEqual({ user: 'a&b=c d' })
  })

  test('setting one filter replaces its value and keeps the others', () => {
    const search = new URLSearchParams('from=2026-10-01&user=alice.k')
    expect(withFilter(search, 'user', 'bob.m').toString()).toBe('from=2026-10-01&user=bob.m')
  })

  test('setting a filter to "all" removes it from the address', () => {
    const search = new URLSearchParams('from=2026-10-01&user=alice.k')
    expect(withFilter(search, 'user', undefined).toString()).toBe('from=2026-10-01')
  })

  test('reset clears every filter', () => {
    const search = new URLSearchParams(
      'from=2026-10-01&to=2026-10-03&outcome=failure&country=RU&user=alice.k',
    )
    expect(clearFilters(search).toString()).toBe('')
  })

  test('setting and resetting leave the address they were given unchanged', () => {
    const search = new URLSearchParams('user=alice.k')
    withFilter(search, 'user', 'bob.m')
    clearFilters(search)
    expect(search.toString()).toBe('user=alice.k')
  })
})
