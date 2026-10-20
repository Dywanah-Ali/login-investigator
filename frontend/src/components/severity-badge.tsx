import { Badge } from '@/components/ui/badge'
import type { SeverityLevel } from '@/lib/api'
import { SEVERITY_COLOUR, SEVERITY_WORD } from '@/lib/severity'

/** A rule's default severity as a coloured badge carrying its word. */
export function SeverityBadge({ level }: { level: SeverityLevel }) {
  return <Badge className={SEVERITY_COLOUR[level]}>{SEVERITY_WORD[level]}</Badge>
}
