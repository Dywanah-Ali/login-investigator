import { EmptyState } from '@/components/empty-state'
import { FailureMessage } from '@/components/failure-message'
import { FilterToolbar } from '@/components/filter-toolbar'
import { HourlyChart } from '@/components/hourly-chart'
import { SectionCards } from '@/components/section-cards'
import { TopIpsChart } from '@/components/top-ips-chart'
import { Skeleton } from '@/components/ui/skeleton'
import { useApi } from '@/hooks/use-api'
import { useFilters } from '@/hooks/use-filters'
import type { OverviewReply } from '@/lib/api'

export function OverviewPage() {
  const { query } = useFilters()
  const overview = useApi<OverviewReply>('/api/overview', query)

  return (
    <>
      <FilterToolbar />
      {overview.state === 'loading' && <Skeleton className="h-32 w-full" />}
      {overview.state === 'failed' && <FailureMessage kind={overview.kind} />}
      {overview.state === 'ready' &&
        (overview.data.summary.total === 0 ? (
          <EmptyState />
        ) : (
          <>
            <SectionCards overview={overview.data} />
            <div className="grid gap-4 @5xl/main:grid-cols-2">
              <HourlyChart hourly={overview.data.hourly} />
              <TopIpsChart ips={overview.data.top_failed_ips} />
            </div>
          </>
        ))}
    </>
  )
}
