import { describe, expect, test } from 'vitest'

import { countOf, failedShare, noun } from '@/lib/format'

describe('singular or plural counts', () => {
  test.each([
    [0, 'finding', '0 findings'],
    [1, 'finding', '1 finding'],
    [2, 'finding', '2 findings'],
    [4812, 'event', '4,812 events'],
  ])('%i with %s reads %s', (count, singular, expected) => {
    expect(countOf(count, singular)).toBe(expected)
  })

  test('a word with an irregular plural takes the plural it is given', () => {
    expect(countOf(1, 'IP address', 'IP addresses')).toBe('1 IP address')
    expect(countOf(3, 'IP address', 'IP addresses')).toBe('3 IP addresses')
  })

  test('the word alone follows the count, for labels that show the number elsewhere', () => {
    expect(noun(1, 'finding')).toBe('finding')
    expect(noun(7, 'finding')).toBe('findings')
  })
})

describe('failed share', () => {
  test.each([
    [1207, 4812, '25.1%'],
    [156, 1856, '8.4%'],
    [0, 40, '0.0%'],
    [40, 40, '100.0%'],
    [1, 3, '33.3%'],
  ])('%i failures out of %i attempts is %s', (failures, total, expected) => {
    expect(failedShare(failures, total)).toBe(expected)
  })

  test('an empty view has no failed share rather than a made-up one', () => {
    expect(failedShare(0, 0)).toBeNull()
  })
})
