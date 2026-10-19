import type { Table } from '@tanstack/react-table'

import { Button } from '@/components/ui/button'
import { countOf } from '@/lib/format'

/** Both dashboard tables page locally. The server still returns every matching row. */
export function TablePager<T>({ table, showSummary = true }: { table: Table<T>; showSummary?: boolean }) {
  return (
    <nav aria-label="Table pages" className={`flex flex-wrap items-center gap-2 text-xs text-muted-foreground ${showSummary ? 'justify-between' : 'justify-end'}`}>
      {showSummary && <span>{countOf(table.getPrePaginationRowModel().rows.length, 'row')}.</span>}
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
