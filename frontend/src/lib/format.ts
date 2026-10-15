// How numbers and times are shown. Presentation only: the API sends raw numbers and timestamps.

/** A whole number with thousands separators: 4,812. */
export function formatCount(count: number): string {
  return count.toLocaleString('en-GB')
}

/** The word that goes with a count: "finding" for one, "findings" otherwise. */
export function noun(count: number, singular: string, plural = `${singular}s`): string {
  return count === 1 ? singular : plural
}

/** A count and its word: "1 finding", "4,812 events". */
export function countOf(count: number, singular: string, plural?: string): string {
  return `${formatCount(count)} ${noun(count, singular, plural)}`
}

// Month names written out, so the wording does not shift with the browser's locale data.
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const twoDigits = (n: number) => String(n).padStart(2, '0')

/** A log timestamp (UTC) as "8 Oct 2026, 09:00 UTC". */
export function formatTimestamp(timestamp: string): string {
  const t = new Date(timestamp)
  return (
    `${t.getUTCDate()} ${MONTHS[t.getUTCMonth()]} ${t.getUTCFullYear()}, ` +
    `${twoDigits(t.getUTCHours())}:${twoDigits(t.getUTCMinutes())} UTC`
  )
}

/** A log timestamp (UTC) to the second, as tables show it: "2026-10-07 23:10:05". */
export function formatLogTime(timestamp: string): string {
  return timestamp.slice(0, 19).replace('T', ' ')
}

/** A log timestamp (UTC) to the minute, as v1's Alerts table showed it: "2026-10-07 23:10". */
export function formatLogMinute(timestamp: string): string {
  return formatLogTime(timestamp).slice(0, 16)
}

/** An hour bucket (UTC) as "7 Oct 23:00", for chart axes. */
export function formatHour(timestamp: string): string {
  const t = new Date(timestamp)
  return `${t.getUTCDate()} ${MONTHS[t.getUTCMonth()]} ${twoDigits(t.getUTCHours())}:00`
}

/** A plain date (YYYY-MM-DD) as "1 Oct 2026". */
export function formatDate(date: string): string {
  const [year, month, day] = date.split('-').map(Number)
  return `${day} ${MONTHS[month - 1]} ${year}`
}

// The date picker works in the browser's local calendar days; the filters are plain dates. A date
// moves between the two by its year, month and day, never through a time of day.

/** A plain date (YYYY-MM-DD) as a local calendar day, or undefined when it is not a real date. */
export function parseDate(date: string | undefined): Date | undefined {
  if (!date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) return undefined
  const [year, month, day] = date.split('-').map(Number)
  const parsed = new Date(year, month - 1, day)
  // new Date rolls 45 October over into November; a real date reads back unchanged.
  return toPlainDate(parsed) === date ? parsed : undefined
}

/** A local calendar day as a plain date (YYYY-MM-DD). */
export function toPlainDate(day: Date): string {
  return `${day.getFullYear()}-${twoDigits(day.getMonth() + 1)}-${twoDigits(day.getDate())}`
}

/** Failed sign-ins as a share of all sign-ins, one decimal place. Null when there are none. */
export function failedShare(failures: number, total: number): string | null {
  if (total === 0) return null
  return `${((failures / total) * 100).toFixed(1)}%`
}
