import { BotIcon, TableIcon } from 'lucide-react'
import { useId } from 'react'
import { Link } from 'react-router'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { alertKey, evidenceCaption, explorerLink, investigateLink } from '@/lib/alerts'
import type { Alert, LogRow } from '@/lib/api'
import { formatLogTime } from '@/lib/format'

// The log fields in the order the log holds them. Each value shows as plain text in a cell, raw
// unless its column says how to format it.
const EVIDENCE_COLUMNS: { key: keyof LogRow; label: string; format?: (value: string) => string }[] = [
  { key: 'timestamp_utc', label: 'Time (UTC)', format: formatLogTime },
  { key: 'username', label: 'User' },
  { key: 'source_ip', label: 'Source IP' },
  { key: 'country', label: 'Country' },
  { key: 'outcome', label: 'Outcome' },
  { key: 'failure_reason', label: 'Failure reason' },
  { key: 'user_agent', label: 'User agent' },
]

/** The details panel beside the table: the selected alert's evidence and the two ways onward.
 * Its content fades in each time another alert is shown; no motion when the system asks for
 * reduced motion (author's ruling, ticket 14). */
export function AlertDetails({ alert, title }: { alert: Alert; title: string }) {
  const titleId = useId()

  return (
    // A quieter surface than the alerts table: the list is where the analyst works, the panel
    // supports it (author, 15 Oct).
    <Card role="region" aria-labelledby={titleId} className="min-w-0 gap-0 bg-muted/40 py-0 ring-foreground/5">
      {/* A new key per alert remounts the content, which replays the entry animation. */}
      <div
        key={alertKey(alert)}
        className="flex min-h-0 flex-col gap-4 py-4 duration-300 ease-out animate-in fade-in-0 slide-in-from-bottom-1 motion-reduce:animate-none"
      >
        <CardHeader className="px-4">
          <CardTitle id={titleId}>{title}</CardTitle>
          <CardDescription>{evidenceCaption(alert)}</CardDescription>
        </CardHeader>
        <CardContent className="px-4">
          <div className="overflow-hidden rounded-lg border border-foreground/5">
            <Table aria-label="Evidence" className="text-xs">
              <TableHeader>
                <TableRow className="hover:bg-transparent">
                  {EVIDENCE_COLUMNS.map((column) => (
                    <TableHead key={column.key} className="h-8 text-muted-foreground">
                      {column.label}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {alert.evidence.map((row, index) => (
                  <TableRow key={index} className="border-foreground/5">
                    {EVIDENCE_COLUMNS.map((column) => (
                      <TableCell key={column.key} className="py-1.5 text-muted-foreground tabular-nums">
                        {column.format ? column.format(row[column.key]) : row[column.key]}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
        <CardFooter className="flex-wrap gap-2 px-4">
          <Button variant="outline" asChild>
            <Link to={explorerLink(alert)}>
              <TableIcon aria-hidden />
              Open in Log explorer
            </Link>
          </Button>
          <Button asChild>
            <Link to={investigateLink(alert, title)}>
              <BotIcon aria-hidden />
              Investigate
            </Link>
          </Button>
        </CardFooter>
      </div>
    </Card>
  )
}
