import { useMemo, useState } from 'react'

import { AlertDetails } from '@/components/alert-details'
import { AlertsTable } from '@/components/alerts-table'
import { EmptyState } from '@/components/empty-state'
import { FailureMessage } from '@/components/failure-message'
import { FilterSelect, FilterToolbar } from '@/components/filter-toolbar'
import { RulesGuide } from '@/components/rules-guide'
import { Skeleton } from '@/components/ui/skeleton'
import { useApi } from '@/hooks/use-api'
import { useFilters } from '@/hooks/use-filters'
import { type SeverityOf, type TitleOf, alertKey, ruleSeverities, ruleTitles } from '@/lib/alerts'
import type { Alert, AlertsReply, RulesReply } from '@/lib/api'
import { countOf } from '@/lib/format'

const NO_ALERTS = 'No alerts match these filters. Widen the date range or reset the filters.'

export function AlertsPage() {
  const { query, filters, setFilters } = useFilters()
  const alerts = useApi<AlertsReply>('/api/alerts', query)
  const guide = useApi<RulesReply>('/api/rules', '')
  // The analyst's choice belongs to the view it was made in. Until they choose, and after any
  // filter change, the newest alert is shown, so a stale choice never lingers (bug log B-009).
  const [picked, setPicked] = useState<{ query: string; key: string } | null>(null)
  const rules = useMemo(() => (guide.state === 'ready' ? guide.data.rules : []), [guide])
  const titleOf = useMemo(() => ruleTitles(rules), [rules])
  const severityOf = useMemo(() => ruleSeverities(rules), [rules])

  // The table needs the rule titles, so it waits for both replies. The first failure is told.
  const failure = alerts.state === 'failed' ? alerts : guide.state === 'failed' ? guide : null

  return (
    <>
      <FilterToolbar>
        {/* The rule filter belongs to Alerts (ticket 26). Its choices are the rules the endpoint
            sent, so the screen never hard-codes them. */}
        {guide.state === 'ready' && (
          <FilterSelect
            label="Rule"
            value={filters.rule}
            options={rules.map((rule) => ({ value: rule.rule, label: rule.title }))}
            onChange={(value) => setFilters({ rule: value })}
          />
        )}
      </FilterToolbar>
      {failure ? (
        <FailureMessage kind={failure.kind} />
      ) : alerts.state !== 'ready' || guide.state !== 'ready' ? (
        <Skeleton className="h-32 w-full" />
      ) : alerts.data.alerts.length === 0 ? (
        <EmptyState message={NO_ALERTS} />
      ) : (
        <AlertsView
          key={query}
          alerts={alerts.data.alerts}
          titleOf={titleOf}
          severityOf={severityOf}
          severityNote={guide.data.severity_note}
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
  severityOf,
  severityNote,
  chosenKey,
  onChoose,
}: {
  alerts: Alert[]
  titleOf: TitleOf
  severityOf: SeverityOf
  severityNote: string
  chosenKey: string | null
  onChoose: (alert: Alert) => void
}) {
  const selected = alerts.find((alert) => alertKey(alert) === chosenKey) ?? alerts[0]

  return (
    <>
      <p className="text-sm"><strong>{countOf(alerts.length, 'alert')} in the selected period</strong></p>
      {/* The panel takes 28% of the content width, the table 72% (author, 15 Oct). */}
      <div className="grid items-start gap-4 @5xl/main:grid-cols-[minmax(0,18fr)_minmax(0,7fr)]">
        <AlertsTable
          alerts={alerts}
          titleOf={titleOf}
          severityOf={severityOf}
          selected={selected}
          onSelect={onChoose}
        />
        <AlertDetails
          alert={selected}
          title={titleOf(selected.rule)}
          severity={severityOf(selected.rule)}
          severityNote={severityNote}
        />
      </div>
    </>
  )
}
