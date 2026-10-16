import type { Table } from '@tanstack/react-table'

import { Button } from '@/components/ui/button'
import { formatCount } from '@/lib/format'

/** Both dashboard tables page locally. The server still returns every matching row. */
export function TablePager<T>({ table }: { table: Table<T> }) {
  return (
    <nav aria-label="Table pages" className="flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground">
      <span>{formatCount(table.getPrePaginationRowModel().rows.length)} rows, newest first. {table.getState().pagination.pageSize} per page.</span>
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          aria-label="Previous page"
          disabled={!table.getCanPreviousPage()}
          onClick={() => table.previousPage()}
        >
          Previous
        </Button>
        <span aria-live="polite">
          Page {table.getState().pagination.pageIndex + 1} of {Math.max(1, table.getPageCount())}
        </span>
        <Button
          variant="outline"
          size="sm"
          aria-label="Next page"
          disabled={!table.getCanNextPage()}
          onClick={() => table.nextPage()}
        >
          Next
        </Button>
      </div>
    </nav>
  )
}
