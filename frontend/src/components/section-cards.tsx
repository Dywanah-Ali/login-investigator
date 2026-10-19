import { BellIcon, CircleCheckIcon } from 'lucide-react'

import { Card, CardAction, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import type { OverviewReply } from '@/lib/api'
import { failedShare, formatCount, noun } from '@/lib/format'

// dashboard-01's KPI cards, holding v1's four Overview figures. The trend badges are dropped:
// v1 has no period-on-period figures.
export function SectionCards({ overview }: { overview: OverviewReply }) {
  const { summary, alert_count } = overview
  const AlertIcon = alert_count === 0 ? CircleCheckIcon : BellIcon
  const alertColour = alert_count === 0
    ? 'text-green-700 dark:text-green-400'
    : 'text-amber-700 dark:text-amber-400'
  const tiles = [
    { label: 'Sign-in attempts', value: summary.total, note: noun(summary.total, 'event') },
    {
      label: 'Failed attempts',
      value: summary.failures,
      note: `${failedShare(summary.failures, summary.total) ?? 'No share'} of attempts`,
    },
    { label: 'Usernames seen', value: summary.distinct_users, note: 'includes guessed names' },
    {
      label: 'Alerts', value: alert_count, note: `${noun(alert_count, 'finding')} in this view`,
      colour: alertColour,
      icon: <AlertIcon aria-hidden="true" className="size-4" />,
      iconBackground: alert_count === 0 ? 'bg-green-500/10' : 'bg-amber-500/10',
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:shadow-xs @xl/main:grid-cols-2 @5xl/main:grid-cols-4 dark:*:data-[slot=card]:bg-card">
      {tiles.map((tile) => (
        <Card key={tile.label} className="@container/card">
          <CardHeader>
            <CardDescription>{tile.label}</CardDescription>
            <CardTitle className={`text-2xl font-semibold tabular-nums @[250px]/card:text-3xl ${tile.colour ?? ''}`}>
              {formatCount(tile.value)}
            </CardTitle>
            {tile.icon && (
              <CardAction>
                <span className={`flex rounded-full p-2 ${tile.colour} ${tile.iconBackground}`}>
                  {tile.icon}
                </span>
              </CardAction>
            )}
          </CardHeader>
          <CardFooter className="text-sm text-muted-foreground">{tile.note}</CardFooter>
        </Card>
      ))}
    </div>
  )
}
