export const TOOL_NAMES = ['find_suspicious_activity', 'search_logins', 'lookup_ip_reputation'] as const
export type ToolName = typeof TOOL_NAMES[number]

export function isToolName(value: unknown): value is ToolName {
  return typeof value === 'string' && TOOL_NAMES.some((name) => name === value)
}

const PHRASES: Record<ToolName, string> = {
  find_suspicious_activity: 'checking the detection rules',
  search_logins: 'searching the sign-in log',
  lookup_ip_reputation: 'looking up IP reputation',
}

/** Only active calls contribute. Repeated invocations of one tool share a phrase. */
export function toolProgress(active: ReadonlyMap<string, ToolName>, hasText: boolean): string {
  const names = new Set(active.values())
  const phrases = TOOL_NAMES.filter((name) => names.has(name)).map((name) => PHRASES[name])
  if (!phrases.length) return hasText ? 'Writing the answer…' : 'Thinking…'
  const last = phrases.pop()!
  const text = phrases.length ? `${phrases.join(', ')} and ${last}` : last
  return `${text[0].toUpperCase()}${text.slice(1)}…`
}
