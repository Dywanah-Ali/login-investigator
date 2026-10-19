import { type CSSProperties, useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { QuietCard } from '@/components/quiet-card'
import { CardContent } from '@/components/ui/card'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useRevealInChat } from '@/hooks/use-reveal-in-chat'
import type { ToolView } from '@/lib/investigations'

function ToolResult({ tool }: { tool: ToolView }) {
  const [raw, setRaw] = useState(false)
  return (
    <section className="space-y-2 border-t border-foreground/5 pt-2">
      <h3 className="font-medium">{tool.title}</h3>
      <div><p className="text-xs font-medium">Asked</p><p className="whitespace-pre-wrap">{tool.asked}</p></div>
      <div><p className="text-xs font-medium">Found</p><p className="whitespace-pre-wrap">{tool.found}</p></div>
      {tool.rows && <Table aria-label={tool.title}>
        <TableHeader><TableRow>{tool.columns.map((column) => <TableHead className="text-xs text-muted-foreground" key={column}>{column}</TableHead>)}</TableRow></TableHeader>
        <TableBody>{tool.rows.map((row, index) => <TableRow key={index}>{tool.columns.map((column) => <TableCell key={column}>{typeof row[column] === 'object' ? JSON.stringify(row[column]) : String(row[column] ?? '')}</TableCell>)}</TableRow>)}</TableBody>
      </Table>}
      <label className="flex items-center gap-2 text-xs"><input type="checkbox" role="switch" checked={raw} onChange={(event) => setRaw(event.target.checked)} />Show raw JSON</label>
      {raw && <pre className="max-h-96 overflow-auto whitespace-pre-wrap rounded-md bg-muted p-3 text-xs">{tool.raw}</pre>}
    </section>
  )
}

export function ToolsUsed({ tools, charactersPerSecond = 200 }: { tools: ToolView[]; charactersPerSecond?: number }) {
  const [open, setOpen] = useState(false)
  const [revealDuration, setRevealDuration] = useState(800)
  const contentRef = useRevealInChat(open, revealDuration)
  if (!tools.length) return null
  // A short passage at the same pace as report reveal sets the expansion's rhythm. Keep a
  // large evidence table from making the user wait through its entire reading time.
  const rate = Number.isFinite(charactersPerSecond) && charactersPerSecond > 0 ? charactersPerSecond : 200
  const duration = Math.round(Math.max(400, Math.min(1200, 160_000 / rate)))
  return (
    <QuietCard className="gap-0 rounded-none border-l-2 border-border/60 bg-transparent py-1 text-xs text-muted-foreground ring-0"><CardContent className="px-3">
      <Collapsible
        open={open}
        onOpenChange={(next) => { if (next) setRevealDuration(duration); setOpen(next) }}
        style={{ '--tools-open-duration': `${revealDuration}ms` } as CSSProperties}
      >
        <CollapsibleTrigger className="tools-used-trigger flex w-full items-center justify-between text-left text-xs font-medium">Tools used ({tools.length})<ChevronDown className="tools-used-chevron size-4" aria-hidden="true" /></CollapsibleTrigger>
        <CollapsibleContent ref={contentRef} className="tools-used-content overflow-hidden">
          <div className="space-y-4 pt-3 pb-1">{tools.map((tool, index) => <ToolResult key={index} tool={tool} />)}</div>
        </CollapsibleContent>
      </Collapsible>
    </CardContent></QuietCard>
  )
}
