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
import { type TitleOf, countsLine, ruleTitles } from '@/lib/alerts'
import type { Alert, AlertsReply, RulesReply } from '@/lib/api'

const NO_ALERTS = 'No alerts match these filters. Widen the date range or reset the filters.'

export function AlertsPage() {
  const { query } = useFilters()
  const alerts = useApi<AlertsReply>('/api/alerts', query)
  const guide = useApi<RulesReply>('/api/rules', '')
  // A selection belongs to the view it was made in. When the address changes under an open panel
  // (Back or Forward), the list is reloaded and the old selection no longer applies (bug log B-009).
  const [picked, setPicked] = useState<{ query: string; alert: Alert } | null>(null)
  const selected = picked?.query === query ? picked.alert : null
  const setSelected = (alert: Alert | null) => setPicked(alert && { query, alert })
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
          <p className="-mt-2 text-sm text-muted-foreground">Select an alert to see its evidence.</p>
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

function AlertsCounts({ alerts, titleOf }: { alerts: Alert[]; titleOf: TitleOf }) {
  const line = countsLine(alerts, titleOf)
  return (
    <p className="text-sm">
      <strong>{line.total}</strong>
      {line.perRule.map((part) => ` · ${part}`).join('')}
    </p>
  )
}
