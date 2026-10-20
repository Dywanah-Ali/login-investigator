// One colour per severity level, shared by the Alerts screen and the report card, so a colour
// always means the same level (ticket 26). Each pair measured at 8.2:1 or better in both themes.
// The level's word is always shown too, so the meaning never rests on colour alone.

import type { RuleSeverity } from '@/lib/api'

export const SEVERITY_COLOUR = {
  none: 'bg-green-100 text-green-900 dark:bg-green-950 dark:text-green-200',
  low: 'bg-blue-100 text-blue-900 dark:bg-blue-950 dark:text-blue-200',
  medium: 'bg-orange-100 text-orange-900 dark:bg-orange-950 dark:text-orange-200',
  high: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200',
  critical: 'bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-200',
}

/** The word shown for a rule's default severity. */
export const SEVERITY_WORD: Record<RuleSeverity, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
}
