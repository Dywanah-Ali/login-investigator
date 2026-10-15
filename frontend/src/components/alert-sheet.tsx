import { BotIcon, TableIcon } from 'lucide-react'
import { Link } from 'react-router'

import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { evidenceCaption, explorerLink, investigateLink } from '@/lib/alerts'
import type { Alert, LogRow } from '@/lib/api'
import { formatLogTime } from '@/lib/format'

// The log fields in the order the log holds them. Each value shows as plain text in a cell.
const EVIDENCE_COLUMNS: { key: keyof LogRow; label: string }[] = [
  { key: 'timestamp_utc', label: 'Time (UTC)' },
  { key: 'username', label: 'User' },
  { key: 'source_ip', label: 'Source IP' },
  { key: 'country', label: 'Country' },
  { key: 'outcome', label: 'Outcome' },
  { key: 'failure_reason', label: 'Failure reason' },
  { key: 'user_agent', label: 'User agent' },
]

/** The side panel for the alert clicked in the table: its evidence and the two ways onward. */
export function AlertSheet({
  alert,
  title,
  onClose,
}: {
  alert: Alert | null
  title: string
  onClose: () => void
}) {
  return (
    <Sheet open={alert !== null} onOpenChange={(open) => !open && onClose()}>
      <SheetContent className="w-full data-[side=right]:sm:max-w-3xl">
        {alert && (
          <>
            <SheetHeader>
              <SheetTitle>{title}</SheetTitle>
              <SheetDescription>{evidenceCaption(alert)}</SheetDescription>
            </SheetHeader>
            <div className="min-h-0 flex-1 overflow-auto px-4">
              <Table aria-label="Evidence">
                <TableHeader className="bg-muted">
                  <TableRow>
                    {EVIDENCE_COLUMNS.map((column) => (
                      <TableHead key={column.key}>{column.label}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {alert.evidence.map((row, index) => (
                    <TableRow key={index}>
                      {EVIDENCE_COLUMNS.map((column) => (
                        <TableCell key={column.key} className="tabular-nums">
                          {column.key === 'timestamp_utc' ? formatLogTime(row[column.key]) : row[column.key]}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <SheetFooter className="flex-row justify-end">
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
            </SheetFooter>
          </>
        )}
      </SheetContent>
    </Sheet>
  )
}
