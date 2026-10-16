import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  useReactTable,
} from '@tanstack/react-table'

import { TablePager } from '@/components/table-pager'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import type { LogRow } from '@/lib/api'
import { formatLogTime } from '@/lib/format'

const columns: ColumnDef<LogRow>[] = [
  {
    accessorKey: 'timestamp_utc',
    header: 'Time (UTC)',
    cell: ({ row }) => formatLogTime(row.original.timestamp_utc),
  },
  { accessorKey: 'username', header: 'User' },
  { accessorKey: 'source_ip', header: 'Source IP' },
  { accessorKey: 'country', header: 'Country' },
  { accessorKey: 'outcome', header: 'Outcome' },
  { accessorKey: 'failure_reason', header: 'Failure reason' },
  { accessorKey: 'user_agent', header: 'User agent' },
]

/** All matching rows arrive newest first. Only log fields rendered as text reach these cells. */
export function ExplorerTable({ rows }: { rows: LogRow[] }) {
  const table = useReactTable({
    data: rows,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageIndex: 0, pageSize: 20 } },
  })

  return (
    <div className="min-w-0 space-y-3">
      <div className="overflow-hidden rounded-lg border">
        <Table aria-label="Login events">
          <TableHeader className="bg-muted">
            {table.getHeaderGroups().map((group) => (
              <TableRow key={group.id}>
                {group.headers.map((header) => (
                  <TableHead key={header.id}>
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
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
