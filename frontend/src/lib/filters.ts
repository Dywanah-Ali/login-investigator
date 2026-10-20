// The shared filters live in the address bar as search parameters (ticket 07). The same
// parameters travel on every API request, so the address describes the screen and a reload shows
// the same view. Names and meanings follow the API contract's "Shared filter parameters".

export const FILTER_KEYS = ['from', 'to', 'outcome', 'country', 'user', 'ip', 'rule'] as const

/** Filters that belong to one screen, as the IP box belongs to the Log explorer. Elsewhere they
 * are neither sent nor carried onward. */
export const SCREEN_ONLY_FILTERS: Partial<Record<FilterKey, string>> = {
  ip: '/explorer',
  rule: '/alerts',
}

export type FilterKey = (typeof FILTER_KEYS)[number]

export type Filters = Partial<Record<FilterKey, string>>

/** The filters in an address. An empty box means "all", as the API reads it. */
export function readFilters(search: URLSearchParams): Filters {
  const filters: Filters = {}
  for (const key of FILTER_KEYS) {
    const value = search.get(key)?.trim()
    if (value) filters[key] = value
  }
  return filters
}

/** The query string for an API request: the filters in a fixed order, empty ones left out. */
export function filterQuery(filters: Filters): string {
  const query = new URLSearchParams()
  for (const key of FILTER_KEYS) {
    const value = filters[key]?.trim()
    if (value) query.set(key, value)
  }
  return query.toString()
}

/** A copy of the address with one filter set, or removed when the value is "all". */
export function withFilter(search: URLSearchParams, key: FilterKey, value: string | undefined) {
  const next = new URLSearchParams(search)
  if (value?.trim()) next.set(key, value.trim())
  else next.delete(key)
  return next
}

/** A copy of the address with every filter removed: the whole log. */
export function clearFilters(search: URLSearchParams) {
  const next = new URLSearchParams(search)
  for (const key of FILTER_KEYS) next.delete(key)
  return next
}
