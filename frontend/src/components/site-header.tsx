import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { useDataset } from '@/hooks/use-dataset'
import { formatTimestamp } from '@/lib/format'

export function SiteHeader({ title }: { title: string }) {
  const dataset = useDataset()

  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
        <h1 className="text-base font-medium">{title}</h1>
        {/* The label and capture time come from the dataset endpoint; nothing is hard-coded. */}
        {dataset.state === 'ready' && (
          <div className="ml-auto flex items-center gap-3 text-sm text-muted-foreground">
            <Badge variant="outline">{dataset.data.label}</Badge>
            <span>Log captured {formatTimestamp(dataset.data.captured_at)}</span>
          </div>
        )}
      </div>
    </header>
  )
}
