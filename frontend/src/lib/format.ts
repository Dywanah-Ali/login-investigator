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

/** Failed sign-ins as a share of all sign-ins, one decimal place. Null when there are none. */
export function failedShare(failures: number, total: number): string | null {
  if (total === 0) return null
  return `${((failures / total) * 100).toFixed(1)}%`
}
