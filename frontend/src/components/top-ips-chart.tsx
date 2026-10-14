import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from 'recharts'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart'
import type { OverviewReply } from '@/lib/api'
import { countOf } from '@/lib/format'

const chartConfig = {
  failures: { label: 'Failed sign-ins', color: 'var(--destructive)' },
} satisfies ChartConfig

type TopIp = OverviewReply['top_failed_ips'][number]

export function TopIpsChart({ ips }: { ips: OverviewReply['top_failed_ips'] }) {
  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Top source IPs by failed sign-ins</CardTitle>
        <CardDescription>The ten IPs with the most failed sign-ins in this view</CardDescription>
      </CardHeader>
      <CardContent className="px-2 sm:px-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-64 w-full">
          <BarChart data={ips} layout="vertical" margin={{ left: 8 }}>
            <CartesianGrid horizontal={false} />
            <XAxis type="number" tickLine={false} axisLine={false} allowDecimals={false} />
            <YAxis
              type="category"
              dataKey="source_ip"
              tickLine={false}
              axisLine={false}
              width={110}
              // Every bar keeps its IP. By default Recharts drops labels it finds crowded, which
              // hid the top IP of all (bug log B-007).
              interval={0}
            />
            <ChartTooltip
              content={
                <ChartTooltipContent
                  formatter={(_value, _name, item) => {
                    const ip = item.payload as TopIp
                    return `${countOf(ip.failures, 'failed sign-in')} against ${countOf(ip.accounts, 'account')}`
                  }}
                />
              }
            />
            <Bar dataKey="failures" fill="var(--color-failures)" radius={4} />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
