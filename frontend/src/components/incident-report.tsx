import { useEffect, useState, useSyncExternalStore } from 'react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { investigationPath, type IncidentReport as Report } from '@/lib/investigations'

const SEVERITY = {
  none: { accent: 'border-l-green-400', label: 'No incident', colour: 'bg-green-100 text-green-900 dark:bg-green-950 dark:text-green-200' },
  low: { accent: 'border-l-blue-400', label: 'Low severity', colour: 'bg-blue-100 text-blue-900 dark:bg-blue-950 dark:text-blue-200' },
  medium: { accent: 'border-l-orange-400', label: 'Medium severity', colour: 'bg-orange-100 text-orange-900 dark:bg-orange-950 dark:text-orange-200' },
  high: { accent: 'border-l-red-400', label: 'High severity', colour: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200' },
  critical: { accent: 'border-l-red-400', label: 'Critical severity', colour: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200' },
}

const MOTION_QUERY = '(prefers-reduced-motion: reduce)'
function subscribeMotion(change: () => void) {
  const media = window.matchMedia(MOTION_QUERY)
  media.addEventListener('change', change)
  return () => media.removeEventListener('change', change)
}
const reducedMotion = () => window.matchMedia(MOTION_QUERY).matches

type ReportSection = { title: string; kind: 'paragraph' | 'list' | 'timeline'; values: string[] }
function reportSections(report: Report): ReportSection[] {
  return [
    { title: 'Summary', kind: 'paragraph', values: [report.summary] },
    { title: 'Attacker IPs', kind: 'list', values: report.attacker_ips },
    { title: 'Affected users', kind: 'list', values: report.affected_users },
    { title: 'Timeline (UTC)', kind: 'timeline', values: report.timeline.map((entry) => `${entry.time_utc}: ${entry.event}`) },
    { title: 'Evidence', kind: 'list', values: report.evidence },
    { title: 'Recommended next steps', kind: 'list', values: report.recommended_next_steps },
  ]
}
const valuesOrNone = (section: ReportSection) => section.values.length ? section.values : ['None']
const characters = (text: string) => Array.from(text)

// A local budget produces a new plain-text view without mutating the saved report.
function reportPreview(reportTitle: string, sections: ReportSection[], budget: number) {
  let remaining = budget
  function take(text: string): string | null {
    if (remaining < 0 || (remaining === 0 && text.length > 0)) return null
    const letters = characters(text)
    const visible = letters.slice(0, remaining).join('')
    remaining -= letters.length
    return visible
  }
  const title = take(reportTitle)
  const visibleSections = sections.map((section) => ({
    ...section,
    empty: !section.values.length,
    visible: valuesOrNone(section).map(take).filter((value): value is string => value !== null),
  })).filter((section) => section.visible.length > 0)
  return { title, visibleSections }
}

type ReportProps = {
  id: string
  report: Report
  revealCharactersPerSecond?: number
  onRevealComplete?: (id: string, reportNumber: number) => void
}

/** Fixed fields only. Reveal clips plain text; it never changes or re-parses the saved report. */
export function IncidentReport({ id, report, revealCharactersPerSecond, onRevealComplete }: ReportProps) {
  const severity = SEVERITY[report.severity]
  const sections = reportSections(report)
  const total = [report.title, ...sections.flatMap(valuesOrNone)]
    .reduce((sum, text) => sum + characters(text).length, 0)
  const motionDisabled = useSyncExternalStore(subscribeMotion, reducedMotion, () => false)
  const [shown, setShown] = useState(1)
  const [skipped, setSkipped] = useState(false)
  const animate = (revealCharactersPerSecond ?? 0) > 0 && !motionDisabled && !skipped
  const budget = animate ? Math.min(shown, total) : total
  const revealing = budget < total

  useEffect(() => {
    const rate = revealCharactersPerSecond ?? 0
    if (rate <= 0) return
    if (motionDisabled || skipped) { onRevealComplete?.(id, report.number); return }
    const started = performance.now()
    let frame: number
    function advance(now: number) {
      const next = Math.min(total, 1 + Math.floor((now - started) * rate / 1000))
      setShown(next)
      if (next < total) frame = requestAnimationFrame(advance)
      else onRevealComplete?.(id, report.number)
    }
    frame = requestAnimationFrame(advance)
    return () => cancelAnimationFrame(frame)
  }, [id, report.number, total, revealCharactersPerSecond, motionDisabled, skipped, onRevealComplete])

  const { title, visibleSections } = reportPreview(report.title, sections, budget)

  return (
    <Card role="region" aria-label="Incident report" aria-busy={revealing} className={`min-w-0 gap-3 rounded-lg border-l-4 py-3 shadow-none ${severity.accent}`}>
      <CardHeader className="gap-2 px-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-medium text-muted-foreground">Incident report</span>
          <Badge className={severity.colour}>{severity.label}</Badge>
          {revealing && <Button size="xs" variant="ghost" className="ml-auto" onClick={() => setSkipped(true)}>Show full report</Button>}
        </div>
        {title !== null && <CardTitle className="text-sm leading-relaxed">{title}</CardTitle>}
      </CardHeader>
      <CardContent className="space-y-3 px-3 text-xs leading-relaxed">
        {visibleSections.map((section) => {
          const List = section.kind === 'timeline' ? 'ol' : 'ul'
          return <section key={section.title} className="space-y-2">
            <h4 className="font-medium">{section.title}</h4>
            {section.empty || section.kind === 'paragraph'
              ? <p className={`whitespace-pre-wrap break-words ${section.empty ? 'text-muted-foreground' : ''}`}>{section.visible[0]}</p>
              : <List className={`space-y-1 pl-5 ${section.kind === 'timeline' ? 'list-decimal' : 'list-disc'}`}>
                {section.visible.map((value, index) => <li className="whitespace-pre-wrap break-words" key={index}>{value}</li>)}
              </List>}
          </section>
        })}
        <a className="inline-block font-medium underline underline-offset-4" href={`${investigationPath(id)}/reports/${report.number}.pdf`} download>Download PDF</a>
      </CardContent>
    </Card>
  )
}
