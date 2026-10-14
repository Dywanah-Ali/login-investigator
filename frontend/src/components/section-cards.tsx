import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import type { OverviewReply } from '@/lib/api'
import { failedShare, formatCount, noun } from '@/lib/format'

// dashboard-01's KPI cards, holding v1's four Overview figures. The trend badges are dropped:
// v1 has no period-on-period figures.
export function SectionCards({ overview }: { overview: OverviewReply }) {
  const { summary, alert_count } = overview
  const tiles = [
    { label: 'Sign-in attempts', value: summary.total, note: noun(summary.total, 'event') },
    {
      label: 'Failed attempts',
      value: summary.failures,
      note: `${failedShare(summary.failures, summary.total) ?? 'No share'} of attempts`,
    },
    { label: 'Usernames seen', value: summary.distinct_users, note: 'includes guessed names' },
    { label: 'Alerts', value: alert_count, note: `${noun(alert_count, 'finding')} in this view` },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:shadow-xs @xl/main:grid-cols-2 @5xl/main:grid-cols-4 dark:*:data-[slot=card]:bg-card">
      {tiles.map((tile) => (
        <Card key={tile.label} className="@container/card">
          <CardHeader>
            <CardDescription>{tile.label}</CardDescription>
            <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
              {formatCount(tile.value)}
            </CardTitle>
          </CardHeader>
          <CardFooter className="text-sm text-muted-foreground">{tile.note}</CardFooter>
        </Card>
      ))}
    </div>
  )
}
