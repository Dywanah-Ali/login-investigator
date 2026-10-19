import { useState } from 'react'

import { EmptyState } from '@/components/empty-state'
import { ExplorerTable } from '@/components/explorer-table'
import { FailureMessage } from '@/components/failure-message'
import { FilterToolbar } from '@/components/filter-toolbar'
import { QuietCard } from '@/components/quiet-card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { useApi } from '@/hooks/use-api'
import { useFilters } from '@/hooks/use-filters'
import type { ExplorerReply } from '@/lib/api'
import { formatCount } from '@/lib/format'
import { IP_ERROR, validIp } from '@/lib/ip'

export function ExplorerPage() {
  const { query } = useFilters()
  // Draft input and its error belong to one view. Back, Forward or Reset starts a fresh draft.
  return <ExplorerView key={query} />
}

function ExplorerView() {
  const { filters, setFilters, query } = useFilters()
  const invalid = !validIp(filters.ip)
  const [draft, setDraft] = useState(invalid ? '' : filters.ip ?? '')
  const [badDraft, setBadDraft] = useState(false)
  const showError = invalid || badDraft

  return (
    <>
      <FilterToolbar
        dirty={draft !== (filters.ip ?? '') || badDraft}
        onReset={() => { setDraft(''); setBadDraft(false) }}
      >
        <form
          className="flex items-center gap-2"
          onSubmit={(event) => {
            event.preventDefault()
            if (!validIp(draft)) { setBadDraft(true); return }
            setBadDraft(false)
            setFilters({ ip: draft })
          }}
        >
          <Input
            aria-label="IP address"
            aria-invalid={showError}
            aria-describedby={showError ? 'ip-error' : undefined}
            placeholder="IP address"
            className="h-8 w-48"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
          />
          <Button type="submit" variant="outline" size="sm">Apply IP</Button>
        </form>
      </FilterToolbar>
      {showError ? (
        <p id="ip-error" role="alert" className="text-sm text-destructive">{IP_ERROR}</p>
      ) : (
        <ExplorerResults query={query} />
      )}
    </>
  )
}

const COUNTS = [
  ['total', 'Matching events'],
  ['successes', 'Successful events'],
  ['failures', 'Failed events'],
  ['distinct_users', 'Usernames seen'],
  ['distinct_ips', 'Distinct IPs'],
] as const

function ExplorerResults({ query }: { query: string }) {
  const result = useApi<ExplorerReply>('/api/explorer', query)
  if (result.state === 'loading') return <Skeleton className="h-32 w-full" />
  if (result.state === 'failed') return <FailureMessage kind={result.kind} />
  const { summary, rows } = result.data

  return (
    <>
      <dl role="group" aria-label="Matching event counts" className="grid grid-cols-2 gap-3 @xl/main:grid-cols-5">
        {COUNTS.map(([field, label]) => (
          <QuietCard key={field} className="gap-1 rounded-lg px-4 py-3">
            <dt className="text-xs text-muted-foreground">{label}</dt>
            <dd className="text-xl font-medium tabular-nums">{formatCount(summary[field])}</dd>
          </QuietCard>
        ))}
      </dl>
      {summary.total === 0 ? (
        <EmptyState message="No logins match these filters. Widen the date range or reset the filters." />
      ) : (
        <ExplorerTable rows={rows} />
      )}
      <div className="flex justify-end">
        <Button variant="outline" size="sm" asChild>
          <a href={`/api/explorer.csv${query ? `?${query}` : ''}`}>Download these rows (CSV)</a>
        </Button>
      </div>
    </>
  )
}
