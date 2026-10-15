// How an alert is shown and where it leads. Presentation only: the API sends the full lists and
// raw timestamps, and the core decides which alerts a view holds.

import type { Alert, RuleGuide } from '@/lib/api'
import { countOf, formatCount, formatLogTime } from '@/lib/format'

/** Looks up a rule key's title, such as "brute_force" to "Brute force". */
export type TitleOf = (rule: string) => string

/** Each rule key's title, from the rules endpoint. A key the guide lacks shows as itself. */
export function ruleTitles(rules: RuleGuide[]): TitleOf {
  const titles = new Map(rules.map((guide) => [guide.rule, guide.title]))
  return (rule) => titles.get(rule) ?? rule
}

/** The line above the table: "5 alerts in the selected period", then a count per rule title,
 * in title order, as v1 wrote it. */
export function countsLine(alerts: Alert[], titleOf: TitleOf) {
  const perTitle = new Map<string, number>()
  for (const alert of alerts) {
    const title = titleOf(alert.rule)
    perTitle.set(title, (perTitle.get(title) ?? 0) + 1)
  }
  return {
    total: `${countOf(alerts.length, 'alert')} in the selected period`,
    perRule: [...perTitle]
      .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
      .map(([title, count]) => `${title}: ${formatCount(count)}`),
  }
}

/** The caption above the evidence: every event, or the first and last ones when it was cut. */
export function evidenceCaption(alert: Alert): string {
  const shown = `Showing ${formatCount(alert.evidence_shown)} of ${countOf(alert.event_count, 'event')}`
  return alert.evidence_shown < alert.event_count ? `${shown}: the first and the last ones.` : `${shown}.`
}

const MAX_NAMES = 3

/** A list of IPs or users cut to three, then "and N more", as v1's Alerts table did. */
export function cutNames(names: string[]): string {
  if (names.length <= MAX_NAMES) return names.join(', ')
  return `${names.slice(0, MAX_NAMES).join(', ')} and ${formatCount(names.length - MAX_NAMES)} more`
}

/** The day of a log timestamp (UTC), as the filters take it: "2026-10-08". */
const dayOf = (timestamp: string) => timestamp.slice(0, 10)

/** The Log explorer showing every row from the alert's first IP on the alert's dates. The other
 * filters are left out, so they read "all", as v1's button set them. */
export function explorerLink(alert: Alert): string {
  const query = new URLSearchParams({
    ip: alert.ips[0],
    from: dayOf(alert.first_seen),
    to: dayOf(alert.last_seen),
  })
  return `/explorer?${query}`
}

/** The prepared question for the Investigator, in the contract's wording. The times keep their
 * seconds, so the agent's search window holds the alert's first and last events. */
export function investigateQuestion(alert: Alert, ruleTitle: string): string {
  return (
    `Investigate the ${ruleTitle} alert: ${alert.ips[0]} against ${alert.users[0]} ` +
    `from ${formatLogTime(alert.first_seen)} to ${formatLogTime(alert.last_seen)} UTC.`
  )
}

/** The Investigator with the prepared question in the address. The analyst presses send. */
export function investigateLink(alert: Alert, ruleTitle: string): string {
  return `/investigator?${new URLSearchParams({ ask: investigateQuestion(alert, ruleTitle) })}`
}
