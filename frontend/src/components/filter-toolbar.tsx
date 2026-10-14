import { CalendarIcon } from 'lucide-react'
import type { DateRange } from 'react-day-picker'

import { FailureMessage } from '@/components/failure-message'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useDataset } from '@/hooks/use-dataset'
import { useFilters } from '@/hooks/use-filters'
import { formatDate } from '@/lib/format'

// Radix Select cannot hold an empty value, so "all" has a stand-in that never reaches the address.
const ALL = '__all__'

const OUTCOMES = [
  { value: 'success', label: 'Success' },
  { value: 'failure', label: 'Failure' },
]

/** The shared filters, under the page title on the three dashboard screens. */
export function FilterToolbar() {
  const dataset = useDataset()
  const { filters, setFilters, reset } = useFilters()

  if (dataset.state === 'failed') return <FailureMessage kind={dataset.kind} />
  if (dataset.state === 'loading') return <div className="h-9" aria-hidden />

  const { first_date, last_date, countries, users } = dataset.data

  return (
    <div role="toolbar" aria-label="Filters" className="flex flex-wrap items-center gap-2">
      <DateRangePicker
        from={filters.from}
        to={filters.to}
        firstDate={first_date}
        lastDate={last_date}
        onChange={(from, to) => setFilters({ from, to })}
      />
      <FilterSelect
        label="Outcome"
        value={filters.outcome}
        options={OUTCOMES}
        onChange={(value) => setFilters({ outcome: value })}
      />
      <FilterSelect
        label="Country"
        value={filters.country}
        options={countries.map((country) => ({ value: country, label: country }))}
        onChange={(value) => setFilters({ country: value })}
      />
      <FilterSelect
        label="User"
        value={filters.user}
        options={users.map((user) => ({ value: user, label: user }))}
        onChange={(value) => setFilters({ user: value })}
      />
      <Button
        variant="ghost"
        size="sm"
        onClick={reset}
        disabled={Object.keys(filters).length === 0}
      >
        Reset
      </Button>
    </div>
  )
}

function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string
  value: string | undefined
  options: { value: string; label: string }[]
  onChange: (value: string | undefined) => void
}) {
  return (
    <Select value={value ?? ALL} onValueChange={(next) => onChange(next === ALL ? undefined : next)}>
      <SelectTrigger size="sm" aria-label={label} className="min-w-36">
        <span className="text-muted-foreground">{label}:</span>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value={ALL}>All</SelectItem>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/

// The picker works in the browser's local calendar days; the filters are plain UTC dates. A date
// is moved between the two by its year, month and day, never through a time of day.
function toDay(date: string | undefined): Date | undefined {
  if (!date || !ISO_DATE.test(date)) return undefined
  const [year, month, day] = date.split('-').map(Number)
  return new Date(year, month - 1, day)
}

function fromDay(day: Date | undefined): string | undefined {
  if (!day) return undefined
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${day.getFullYear()}-${pad(day.getMonth() + 1)}-${pad(day.getDate())}`
}

function DateRangePicker({
  from,
  to,
  firstDate,
  lastDate,
  onChange,
}: {
  from: string | undefined
  to: string | undefined
  firstDate: string
  lastDate: string
  onChange: (from: string | undefined, to: string | undefined) => void
}) {
  const first = toDay(firstDate)
  const last = toDay(lastDate)
  const selected: DateRange = { from: toDay(from), to: toDay(to) }

  // Only a date that reads as one is shown back; anything else in the address shows as "all".
  const shown = [selected.from && from, selected.to && to].filter(Boolean) as string[]
  const label = shown.length ? shown.map(formatDate).join(' – ') : 'All dates'

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" aria-label="Date range (UTC)">
          <CalendarIcon />
          <span className="text-muted-foreground">Date range (UTC):</span>
          {label}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <Calendar
          mode="range"
          selected={selected}
          defaultMonth={selected.from ?? last}
          startMonth={first}
          endMonth={last}
          disabled={[...(first ? [{ before: first }] : []), ...(last ? [{ after: last }] : [])]}
          onSelect={(range) => onChange(fromDay(range?.from), fromDay(range?.to))}
        />
      </PopoverContent>
    </Popover>
  )
}
