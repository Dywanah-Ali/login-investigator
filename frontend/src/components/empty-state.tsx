import { SearchXIcon } from 'lucide-react'

// One empty state for the three dashboard screens.
export const NO_MATCH = 'No sign-ins match these filters. Widen the date range or reset the filters.'

export function EmptyState({ message = NO_MATCH }: { message?: string }) {
  return (
    <div className="flex flex-col items-center gap-2 rounded-lg border border-dashed px-6 py-12 text-center text-muted-foreground">
      <SearchXIcon className="size-6" aria-hidden />
      <p className="text-sm">{message}</p>
    </div>
  )
}
