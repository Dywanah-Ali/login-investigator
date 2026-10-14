import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from 'recharts'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  type ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart'
import type { OverviewReply } from '@/lib/api'
import { formatHour } from '@/lib/format'

const chartConfig = {
  success: { label: 'Successful', color: 'var(--chart-2)' },
  failure: { label: 'Failed', color: 'var(--destructive)' },
} satisfies ChartConfig

const HOUR = 60 * 60 * 1000

type HourBar = { hour: string; success: number; failure: number }

// The API leaves out hours with no events. They are put back as zero bars between the first and
// last hour, so a quiet night shows as a gap in time rather than vanishing from the axis.
function hourBars(hourly: OverviewReply['hourly']): HourBar[] {
  if (hourly.length === 0) return []
  const counts = new Map<number, HourBar>()
  for (const { hour, outcome, events } of hourly) {
    const at = Date.parse(hour)
    const bar = counts.get(at) ?? { hour, success: 0, failure: 0 }
    bar[outcome] += events
    counts.set(at, bar)
  }
  const times = [...counts.keys()]
  const bars: HourBar[] = []
  for (let at = Math.min(...times); at <= Math.max(...times); at += HOUR) {
    bars.push(counts.get(at) ?? { hour: new Date(at).toISOString(), success: 0, failure: 0 })
  }
  return bars
}

export function HourlyChart({ hourly }: { hourly: OverviewReply['hourly'] }) {
  const data = hourBars(hourly)

  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Sign-in attempts per hour</CardTitle>
        <CardDescription>Successful and failed, by hour (UTC)</CardDescription>
      </CardHeader>
      <CardContent className="px-2 sm:px-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-64 w-full">
          <BarChart data={data}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="hour"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={48}
              tickFormatter={formatHour}
            />
            <YAxis tickLine={false} axisLine={false} width={40} allowDecimals={false} />
            <ChartTooltip
              content={<ChartTooltipContent labelFormatter={(hour) => formatHour(String(hour))} />}
            />
            <ChartLegend content={<ChartLegendContent />} />
            <Bar dataKey="success" stackId="outcome" fill="var(--color-success)" />
            <Bar dataKey="failure" stackId="outcome" fill="var(--color-failure)" />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
