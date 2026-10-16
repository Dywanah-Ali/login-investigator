import { type ColumnDef, flexRender, getCoreRowModel, getPaginationRowModel, useReactTable } from '@tanstack/react-table'
import { useMemo } from 'react'

import { TablePager } from '@/components/table-pager'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { type TitleOf, cutNames } from '@/lib/alerts'
import type { Alert } from '@/lib/api'
import { formatCount, formatLogMinute } from '@/lib/format'

/** The tasks example's table (TanStack Table) with v1's seven columns. The rows come sorted
 * newest first by the core. Log fields appear only as plain text in these cells. */
export function AlertsTable({
  alerts,
  titleOf,
  selected,
  onSelect,
}: {
  alerts: Alert[]
  titleOf: TitleOf
  selected: Alert
  onSelect: (alert: Alert) => void
}) {
  const columns = useMemo<ColumnDef<Alert>[]>(
    () => [
      { id: 'rule', header: 'Rule', cell: ({ row }) => titleOf(row.original.rule) },
      {
        accessorKey: 'summary',
        header: 'Summary',
        meta: { className: 'min-w-72 whitespace-normal' },
      },
      { id: 'ips', header: 'IP addresses', cell: ({ row }) => cutNames(row.original.ips) },
      {
        id: 'users',
        header: 'Users',
        cell: ({ row }) => cutNames(row.original.users),
        meta: { className: 'whitespace-normal' },
      },
      {
        id: 'events',
        header: 'Events',
        cell: ({ row }) => formatCount(row.original.event_count),
        meta: { className: 'text-right tabular-nums' },
      },
      {
        id: 'first_seen',
        header: 'First seen (UTC)',
        cell: ({ row }) => formatLogMinute(row.original.first_seen),
        meta: { className: 'tabular-nums' },
      },
      {
        id: 'last_seen',
        header: 'Last seen (UTC)',
        cell: ({ row }) => formatLogMinute(row.original.last_seen),
        meta: { className: 'tabular-nums' },
      },
    ],
    [titleOf],
  )

  const table = useReactTable({
    data: alerts,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageIndex: 0, pageSize: 20 } },
  })

  return (
    <div className="min-w-0 space-y-3">
      <div className="overflow-hidden rounded-lg border">
        <Table aria-label="Alerts">
          <TableHeader className="bg-muted">
            {table.getHeaderGroups().map((group) => (
              <TableRow key={group.id}>
                {group.headers.map((header) => (
                  <TableHead key={header.id} className={cellClass(header.column.columnDef)}>
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.original === selected ? 'selected' : undefined}
                aria-selected={row.original === selected}
                tabIndex={0}
                // The chosen row carries an accent bar on its left edge, tying it to the panel.
                className="cursor-pointer data-[state=selected]:shadow-[inset_3px_0_0_var(--primary)]"
                onClick={() => onSelect(row.original)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault()
                    onSelect(row.original)
                  }
                }}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id} className={cellClass(cell.column.columnDef)}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <TablePager table={table} />
    </div>
  )
}

function cellClass(column: ColumnDef<Alert>): string | undefined {
  return (column.meta as { className?: string } | undefined)?.className
}
