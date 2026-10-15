import { useMemo, useState } from 'react'

import { AlertDetails } from '@/components/alert-details'
import { AlertsTable } from '@/components/alerts-table'
import { EmptyState } from '@/components/empty-state'
import { FailureMessage } from '@/components/failure-message'
import { FilterToolbar } from '@/components/filter-toolbar'
import { RulesGuide } from '@/components/rules-guide'
import { Skeleton } from '@/components/ui/skeleton'
import { useApi } from '@/hooks/use-api'
import { useFilters } from '@/hooks/use-filters'
import { type TitleOf, alertKey, countsLine, ruleTitles } from '@/lib/alerts'
import type { Alert, AlertsReply, RulesReply } from '@/lib/api'

const NO_ALERTS = 'No alerts match these filters. Widen the date range or reset the filters.'

export function AlertsPage() {
  const { query } = useFilters()
  const alerts = useApi<AlertsReply>('/api/alerts', query)
  const guide = useApi<RulesReply>('/api/rules', '')
  // The analyst's choice belongs to the view it was made in. Until they choose, and after any
  // filter change, the newest alert is shown, so a stale choice never lingers (bug log B-009).
  const [picked, setPicked] = useState<{ query: string; key: string } | null>(null)
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
        <AlertsView
          alerts={alerts.data.alerts}
          titleOf={titleOf}
          chosenKey={picked?.query === query ? picked.key : null}
          onChoose={(alert) => setPicked({ query, key: alertKey(alert) })}
        />
      )}
      {guide.state === 'ready' && <RulesGuide guide={guide.data} />}
    </>
  )
}

/** The counts line, then the table with the details panel beside it, or below it when narrow. */
function AlertsView({
  alerts,
  titleOf,
  chosenKey,
  onChoose,
}: {
  alerts: Alert[]
  titleOf: TitleOf
  chosenKey: string | null
  onChoose: (alert: Alert) => void
}) {
  const selected = alerts.find((alert) => alertKey(alert) === chosenKey) ?? alerts[0]

  return (
    <>
      <AlertsCounts alerts={alerts} titleOf={titleOf} />
      {/* The panel takes 28% of the content width, the table 72% (author, 15 Oct). */}
      <div className="grid items-start gap-4 @5xl/main:grid-cols-[minmax(0,18fr)_minmax(0,7fr)]">
        <AlertsTable alerts={alerts} titleOf={titleOf} selected={selected} onSelect={onChoose} />
        <AlertDetails alert={selected} title={titleOf(selected.rule)} />
      </div>
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
