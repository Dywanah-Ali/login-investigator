import { useEffect, useState } from 'react'

import { ApiFailure, type FailureKind, getJson } from '@/lib/api'

export type Loaded<T> =
  | { state: 'loading' }
  | { state: 'ready'; data: T }
  | { state: 'failed'; kind: FailureKind }

/** Load an endpoint for the given query string; load again whenever the query changes. */
export function useApi<T>(path: string, query: string): Loaded<T> {
  const key = `${path}?${query}`
  const [result, setResult] = useState<{ key: string; loaded: Loaded<T> }>({
    key,
    loaded: { state: 'loading' },
  })

  useEffect(() => {
    const controller = new AbortController()
    getJson<T>(path, query, controller.signal)
      .then((data) => setResult({ key, loaded: { state: 'ready', data } }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        const kind = error instanceof ApiFailure ? error.kind : 'failed'
        setResult({ key, loaded: { state: 'failed', kind } })
      })
    return () => controller.abort()
  }, [key, path, query])

  // A result for an older query is not shown while the new one loads.
  return result.key === key ? result.loaded : { state: 'loading' }
}
