import { useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { QuietCard } from '@/components/quiet-card'
import { CardContent } from '@/components/ui/card'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import type { ToolView } from '@/lib/investigations'

function ToolResult({ tool }: { tool: ToolView }) {
  const [raw, setRaw] = useState(false)
  return (
    <section className="space-y-3 border-t border-foreground/5 pt-3">
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

export function ToolsUsed({ tools }: { tools: ToolView[] }) {
  if (!tools.length) return null
  return (
    <QuietCard className="text-sm text-muted-foreground"><CardContent>
      <Collapsible>
        <CollapsibleTrigger className="flex w-full items-center justify-between text-left text-xs font-medium">Tools used<ChevronDown className="size-4" aria-hidden="true" /></CollapsibleTrigger>
        <CollapsibleContent className="mt-3 space-y-4">{tools.map((tool, index) => <ToolResult key={index} tool={tool} />)}</CollapsibleContent>
      </Collapsible>
    </CardContent></QuietCard>
  )
}
