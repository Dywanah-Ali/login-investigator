import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { investigationPath, type IncidentReport as Report } from '@/lib/investigations'

const SEVERITY = {
  none: { label: 'No incident', colour: 'bg-green-100 text-green-900 dark:bg-green-950 dark:text-green-200' },
  low: { label: 'Low severity', colour: 'bg-blue-100 text-blue-900 dark:bg-blue-950 dark:text-blue-200' },
  medium: { label: 'Medium severity', colour: 'bg-orange-100 text-orange-900 dark:bg-orange-950 dark:text-orange-200' },
  high: { label: 'High severity', colour: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200' },
  critical: { label: 'Critical severity', colour: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200' },
}

function ReportList({ title, items }: { title: string; items: string[] }) {
  return <section className="space-y-2"><h4 className="font-medium">{title}</h4>{items.length ? <ul className="list-disc space-y-1 pl-5">{items.map((item, index) => <li className="whitespace-pre-wrap break-words" key={index}>{item}</li>)}</ul> : <p className="text-muted-foreground">None</p>}</section>
}

/** Fixed fields only. Report content never passes through the answer renderer. */
export function IncidentReport({ id, report }: { id: string; report: Report }) {
  const severity = SEVERITY[report.severity]
  return (
    <Card className="min-w-0">
      <CardHeader><CardTitle>{report.title}</CardTitle><Badge className={severity.colour}>{severity.label}</Badge></CardHeader>
      <CardContent className="space-y-4">
        <section><h4 className="font-medium">Summary</h4><p className="whitespace-pre-wrap break-words">{report.summary}</p></section>
        <ReportList title="Attacker IPs" items={report.attacker_ips} />
        <ReportList title="Affected users" items={report.affected_users} />
        <section><h4 className="font-medium">Timeline (UTC)</h4>{report.timeline.length ? <ol className="list-decimal space-y-1 pl-5">{report.timeline.map((entry, index) => <li className="whitespace-pre-wrap break-words" key={index}>{entry.time_utc}: {entry.event}</li>)}</ol> : <p className="text-muted-foreground">None</p>}</section>
        <ReportList title="Evidence" items={report.evidence} />
        <ReportList title="Recommended next steps" items={report.recommended_next_steps} />
        <a className="inline-block font-medium underline underline-offset-4" href={`${investigationPath(id)}/reports/${report.number}.pdf`} download>Download PDF</a>
      </CardContent>
    </Card>
  )
}
