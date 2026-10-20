import { useLocation, useSearchParams } from 'react-router'

import {
  type FilterKey,
  SCREEN_ONLY_FILTERS,
  clearFilters,
  filterQuery,
  readFilters,
  withFilter,
} from '@/lib/filters'

/** The shared filters, read from and written to the address bar. */
export function useFilters() {
  const [search, setSearch] = useSearchParams()
  const filters = readFilters(search)
  const { pathname } = useLocation()
  for (const [key, screen] of Object.entries(SCREEN_ONLY_FILTERS)) {
    if (pathname !== screen) delete filters[key as FilterKey]
  }

  return {
    filters,
    /** The query string every request on this screen carries. */
    query: filterQuery(filters),
    setFilters(changes: Partial<Record<FilterKey, string | undefined>>) {
      let next = search
      for (const [key, value] of Object.entries(changes)) {
        next = withFilter(next, key as FilterKey, value)
      }
      setSearch(next)
    },
    reset() {
      setSearch(clearFilters(search))
    },
  }
}
