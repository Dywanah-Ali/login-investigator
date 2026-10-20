import { ChevronRightIcon } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { SeverityBadge } from '@/components/severity-badge'
import type { RulesReply } from '@/lib/api'

/** "How these rules work": each rule's title, when it fires, its assumption and its default
 * severity (ticket 26), then the general assumptions. Collapsed by default. The text comes from
 * the rules endpoint, the same source as the core's rules. */
export function RulesGuide({ guide }: { guide: RulesReply }) {
  return (
    <Collapsible className="rounded-lg border">
      <CollapsibleTrigger asChild>
        <Button variant="ghost" className="group w-full justify-start rounded-lg">
          <ChevronRightIcon
            className="transition-transform group-data-[state=open]:rotate-90"
            aria-hidden
          />
          How these rules work
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent className="grid gap-3 px-4 pt-1 pb-4 text-sm">
        {guide.rules.map((rule) => (
          <div key={rule.rule}>
            <p>
              <strong>{rule.title}.</strong> Fires when: {rule.fires_when}
            </p>
            <p className="text-muted-foreground">
              <em>Assumption:</em> {rule.assumption}
            </p>
            <p className="text-muted-foreground">
              <em>Default severity:</em> <SeverityBadge level={rule.severity} />{' '}
              {rule.severity_reason}
            </p>
          </div>
        ))}
        <ul className="list-disc space-y-1 pl-5 text-muted-foreground">
          {guide.general_assumptions.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </CollapsibleContent>
    </Collapsible>
  )
}
