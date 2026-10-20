import { useLocation, useSearchParams } from 'react-router'

import {
  type FilterKey,
  clearFilters,
  filterQuery,
  otherScreensFilters,
  readFilters,
  withFilter,
} from '@/lib/filters'

/** The shared filters, read from and written to the address bar. */
export function useFilters() {
  const [search, setSearch] = useSearchParams()
  const filters = readFilters(search)
  const { pathname } = useLocation()
  for (const key of otherScreensFilters(pathname)) delete filters[key]

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
