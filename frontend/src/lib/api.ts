// The one door to the API. Reply shapes follow docs/api-contract.md. The frontend never reaches
// past these endpoints.

export type DatasetFacts = {
  captured_at: string
  label: string
  first_date: string
  last_date: string
  countries: string[]
  users: string[]
  row_count: number
}

export type Outcome = 'success' | 'failure'

export type OverviewReply = {
  summary: {
    total: number
    successes: number
    failures: number
    distinct_users: number
    distinct_ips: number
    distinct_countries: number
    first_seen: string | null
    last_seen: string | null
  }
  alert_count: number
  hourly: { hour: string; outcome: Outcome; events: number }[]
  top_failed_ips: { source_ip: string; failures: number; accounts: number }[]
}

/** What went wrong, in the few kinds the screen tells apart. */
export type FailureKind = 'invalid_filter' | 'log_invalid' | 'unreachable' | 'failed'

// Fixed text written here. The server's own message is never shown: it is read only for its code.
export const FAILURE_TEXT: Record<FailureKind, string> = {
  invalid_filter: 'A filter in the address is not valid. Reset the filters to continue.',
  log_invalid: 'The log could not be loaded. The server log says why.',
  unreachable: 'The API cannot be reached. Check that it is running.',
  failed: 'The server could not answer. Try again in a moment.',
}

export class ApiFailure extends Error {
  readonly kind: FailureKind

  constructor(kind: FailureKind) {
    super(FAILURE_TEXT[kind])
    this.name = 'ApiFailure'
    this.kind = kind
  }
}

/** GET an endpoint and return its JSON, or throw an ApiFailure. */
export async function getJson<T>(path: string, query: string, signal?: AbortSignal): Promise<T> {
  let response: Response
  try {
    response = await fetch(query ? `${path}?${query}` : path, { signal })
  } catch (error) {
    if (signal?.aborted) throw error
    throw new ApiFailure('unreachable')
  }
  if (response.ok) return (await response.json()) as T
  throw new ApiFailure(await failureKind(response))
}

async function failureKind(response: Response): Promise<FailureKind> {
  const code = await errorCode(response)
  // Every reply from our API carries the one error shape. A reply without it came from something
  // in between, such as the dev proxy when the API is not running.
  if (code === null) return 'unreachable'
  if (code === 'invalid_filter' || code === 'log_invalid') return code
  return 'failed'
}

async function errorCode(response: Response): Promise<string | null> {
  try {
    const body: unknown = await response.json()
    const code = (body as { error?: { code?: unknown } }).error?.code
    return typeof code === 'string' ? code : null
  } catch {
    return null
  }
}
