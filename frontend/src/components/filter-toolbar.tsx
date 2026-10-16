import { CalendarIcon } from 'lucide-react'
import type { ReactNode } from 'react'
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
import { formatDate, parseDate, toPlainDate } from '@/lib/format'

// Radix Select cannot hold an empty value, so "all" has a stand-in that never reaches the address.
const ALL = '__all__'

const OUTCOMES = [
  { value: 'success', label: 'Success' },
  { value: 'failure', label: 'Failure' },
]

/** The shared filters, under the page title on the three dashboard screens. */
export function FilterToolbar({ children, dirty = false, onReset }: {
  children?: ReactNode
  dirty?: boolean
  onReset?: () => void
}) {
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
      {children}
      <Button
        variant="ghost"
        size="sm"
        onClick={() => { reset(); onReset?.() }}
        disabled={Object.keys(filters).length === 0 && !dirty}
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
  // A value in the address that the dataset does not hold still shows in the box, so the analyst
  // can see what is filtering the view. It matches nothing, so the screen shows its empty state.
  const choices =
    value && !options.some((option) => option.value === value)
      ? [...options, { value, label: value }]
      : options

  return (
    <Select value={value ?? ALL} onValueChange={(next) => onChange(next === ALL ? undefined : next)}>
      <SelectTrigger size="sm" aria-label={label} className="min-w-36">
        <span className="text-muted-foreground">{label}:</span>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value={ALL}>All</SelectItem>
        {choices.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
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
  const first = parseDate(firstDate)
  const last = parseDate(lastDate)
  const selected: DateRange = { from: parseDate(from), to: parseDate(to) }

  // Only a real date is shown back. With none, the label shows the whole log, as the agreed
  // screen does.
  const shown = [selected.from && from, selected.to && to].filter(Boolean) as string[]
  const label = (shown.length ? shown : [firstDate, lastDate]).map(formatDate).join(' – ')

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
          // The app treats the log's last day as "today" (contract, dataset facts), not the
          // reader's clock.
          today={last}
          startMonth={first}
          endMonth={last}
          disabled={[...(first ? [{ before: first }] : []), ...(last ? [{ after: last }] : [])]}
          onSelect={(range) =>
            onChange(
              range?.from && toPlainDate(range.from),
              range?.to && toPlainDate(range.to),
            )
          }
        />
      </PopoverContent>
    </Popover>
  )
}
