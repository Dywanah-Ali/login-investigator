import { useMemo, useState } from 'react'

import { AlertSheet } from '@/components/alert-sheet'
import { AlertsTable } from '@/components/alerts-table'
import { EmptyState } from '@/components/empty-state'
import { FailureMessage } from '@/components/failure-message'
import { FilterToolbar } from '@/components/filter-toolbar'
import { RulesGuide } from '@/components/rules-guide'
import { Skeleton } from '@/components/ui/skeleton'
import { useApi } from '@/hooks/use-api'
import { useFilters } from '@/hooks/use-filters'
import { countsLine, ruleTitles } from '@/lib/alerts'
import type { Alert, AlertsReply, RulesReply } from '@/lib/api'

export const NO_ALERTS = 'No alerts match these filters. Widen the date range or reset the filters.'

export function AlertsPage() {
  const { query } = useFilters()
  const alerts = useApi<AlertsReply>('/api/alerts', query)
  const guide = useApi<RulesReply>('/api/rules', '')
  const [selected, setSelected] = useState<Alert | null>(null)
  const titleOf = useMemo(
    () => ruleTitles(guide.state === 'ready' ? guide.data.rules : []),
    [guide],
  )

  // The table needs the rule titles, so it waits for both replies. The first failure is told.
  const failure = alerts.state === 'failed' ? alerts : guide.state === 'failed' ? guide : null

  return (
    <>
      <FilterToolbar />
      {failure ? (
        <FailureMessage kind={failure.kind} />
      ) : alerts.state !== 'ready' || guide.state !== 'ready' ? (
        <Skeleton className="h-32 w-full" />
      ) : alerts.data.alerts.length === 0 ? (
        <EmptyState message={NO_ALERTS} />
      ) : (
        <>
          <AlertsCounts alerts={alerts.data.alerts} titleOf={titleOf} />
          <AlertsTable
            alerts={alerts.data.alerts}
            titleOf={titleOf}
            selected={selected}
            onSelect={setSelected}
          />
          <AlertSheet
            alert={selected}
            title={selected ? titleOf(selected.rule) : ''}
            onClose={() => setSelected(null)}
          />
        </>
      )}
      {guide.state === 'ready' && <RulesGuide guide={guide.data} />}
    </>
  )
}

function AlertsCounts({ alerts, titleOf }: { alerts: Alert[]; titleOf: (rule: string) => string }) {
  const line = countsLine(alerts, titleOf)
  return (
    <p className="text-sm">
      <strong>{line.total}</strong>
      {line.perRule.map((part) => ` · ${part}`).join('')}
    </p>
  )
}
