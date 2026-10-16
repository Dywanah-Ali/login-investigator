import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { IncidentReport } from '@/components/incident-report'
import type { IncidentReport as Report } from '@/lib/investigations'

const REPORT: Report = {
  title: 'Unusual sign-ins from a suspicious address', severity: 'high',
  summary: 'Many failures were followed by a successful sign-in.',
  attacker_ips: ['203.0.113.2'], affected_users: ['alice'],
  timeline: [{ time_utc: '2026-10-16T08:00:00Z', event: 'Successful sign-in' }],
  evidence: ['Search found ten failures'], recommended_next_steps: ['Review the account'], number: 1,
}

afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks() })

test('a new report reveals plain text progressively at the supplied pace and finishes with its exact fields', () => {
  vi.useFakeTimers()
  render(<IncidentReport id="case-0" report={REPORT} revealCharactersPerSecond={100} />)
  expect(screen.queryByText(REPORT.title)).not.toBeInTheDocument()
  expect(screen.queryByText(REPORT.summary)).not.toBeInTheDocument()
  expect(screen.getByText('High severity')).toBeInTheDocument()
  act(() => vi.advanceTimersByTime(160))
  expect(screen.getByText(/^Unusual sign/)).toBeInTheDocument()
  expect(screen.queryByText(REPORT.summary)).not.toBeInTheDocument()
  act(() => vi.advanceTimersByTime(5000))
  expect(screen.getByText(REPORT.title)).toBeInTheDocument()
  expect(screen.getByText(REPORT.summary)).toBeInTheDocument()
  expect(screen.getByText('Review the account')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Download PDF' })).toHaveAttribute('href', '/api/investigations/case-0/reports/1.pdf')
  expect(screen.queryByRole('button', { name: 'Show full report' })).not.toBeInTheDocument()
})

test('past reports open in full and the new-report reveal can be skipped', () => {
  const view = render(<IncidentReport id="case-0" report={REPORT} />)
  expect(screen.getByText(REPORT.summary)).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Show full report' })).not.toBeInTheDocument()
  view.unmount()
  render(<IncidentReport id="case-0" report={REPORT} revealCharactersPerSecond={100} />)
  fireEvent.click(screen.getByRole('button', { name: 'Show full report' }))
  expect(screen.getByText(REPORT.summary)).toBeInTheDocument()
  expect(screen.getByText('Review the account')).toBeInTheDocument()
})

test('reduced motion shows the full saved text immediately, including hostile text and empty fields', () => {
  vi.spyOn(window, 'matchMedia').mockImplementation((query) => ({
    matches: query === '(prefers-reduced-motion: reduce)', media: query,
    onchange: null, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {}, dispatchEvent: () => false,
  }))
  const { container } = render(<IncidentReport id="case-0" report={{ ...REPORT, summary: '<img src=x> [link](javascript:alert(1))', attacker_ips: [], affected_users: [], timeline: [] }} revealCharactersPerSecond={100} />)
  expect(screen.getByText('<img src=x> [link](javascript:alert(1))')).toBeInTheDocument()
  expect(screen.getAllByText('None')).toHaveLength(3)
  expect(screen.queryByRole('button', { name: 'Show full report' })).not.toBeInTheDocument()
  expect(container.querySelector('img,script,iframe')).toBeNull()
  expect(container.querySelectorAll('a')).toHaveLength(1) // trusted PDF link only
})

test('leaving during a reveal cancels its remaining animation', () => {
  vi.useFakeTimers()
  const complete = vi.fn()
  const view = render(<IncidentReport id="case-0" report={REPORT} revealCharactersPerSecond={100} onRevealComplete={complete} />)
  act(() => vi.advanceTimersByTime(160))
  view.unmount()
  act(() => vi.advanceTimersByTime(10000))
  expect(complete).not.toHaveBeenCalled()
})
