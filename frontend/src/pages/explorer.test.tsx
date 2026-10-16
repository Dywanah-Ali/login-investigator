import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, test, vi } from 'vitest'
import { AppRoutes } from '@/App'
import { DATASET, fakeApi } from '@/test/fake-api'

const API = { '/api/dataset': { body: DATASET } }
function open(address = '/explorer') {
  render(<MemoryRouter initialEntries={[address]}><AppRoutes /></MemoryRouter>)
}
afterEach(() => vi.unstubAllGlobals())

test('an invalid IP in the address is refused before a request and never echoed', async () => {
  const hostile = '<script>alert(1)</script>'
  const api = fakeApi(API)
  open(`/explorer?ip=${encodeURIComponent(hostile)}`)
  expect(await screen.findByText('That is not a valid IP address. Clear the box or enter one like 203.0.113.10.')).toBeInTheDocument()
  expect(document.body).not.toHaveTextContent(hostile)
  expect(screen.getByRole('textbox', { name: 'IP address' })).toHaveValue('')
  expect(api.requests().some((request) => request.startsWith('/api/explorer'))).toBe(false)
  expect(screen.queryByRole('link', { name: 'Download these rows (CSV)' })).not.toBeInTheDocument()
})


const rows = Array.from({ length: 21 }, (_, index) => ({
  timestamp_utc: `2026-10-08T00:00:${String(59 - index).padStart(2, '0')}Z`,
  username: `user-${index + 1}`, source_ip: '203.0.113.10', country: 'GB',
  outcome: 'failure', failure_reason: 'bad_password', user_agent: 'test-agent',
}))
const EXPLORER = { summary: { total: 21, successes: 0, failures: 21, distinct_users: 21, distinct_ips: 1 }, rows }

test('shows the five counts, pages every row locally and downloads the same filters', async () => {
  const api = fakeApi({ ...API, '/api/explorer': { body: EXPLORER } })
  open('/explorer?from=2026-10-08&outcome=failure&ip=203.0.113.10')
  const table = await screen.findByRole('table', { name: 'Login events' })
  expect(within(table).getAllByRole('columnheader').map((cell) => cell.textContent)).toEqual([
    'Time (UTC)', 'User', 'Source IP', 'Country', 'Outcome', 'Failure reason', 'User agent',
  ])
  const counts = screen.getByRole('group', { name: 'Matching event counts' })
  expect(within(counts).getAllByRole('term').map((node) => node.textContent)).toEqual([
    'Matching events', 'Successful events', 'Failed events', 'Usernames seen', 'Distinct IPs',
  ])
  expect(within(counts).getAllByRole('definition').map((node) => node.textContent)).toEqual(['21', '0', '21', '21', '1'])
  expect(within(table).getAllByRole('row')).toHaveLength(21)
  expect(within(table).getByText('user-1')).toBeInTheDocument()
  expect(within(table).queryByText('user-21')).not.toBeInTheDocument()
  const pager = screen.getByRole('navigation', { name: 'Table pages' })
  expect(within(pager).getByRole('button', { name: 'Previous page' })).toBeDisabled()
  await userEvent.click(within(pager).getByRole('button', { name: 'Next page' }))
  expect(within(table).getAllByRole('row')).toHaveLength(2)
  expect(within(table).getByText('user-21')).toBeInTheDocument()
  expect(within(pager).getByRole('button', { name: 'Next page' })).toBeDisabled()
  await userEvent.click(within(pager).getByRole('button', { name: 'Previous page' }))
  expect(within(table).getByText('user-1')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Download these rows (CSV)' })).toHaveAttribute(
    'href', '/api/explorer.csv?from=2026-10-08&outcome=failure&ip=203.0.113.10',
  )
  expect(api.requests().filter((request) => request.startsWith('/api/explorer'))).toEqual([
    '/api/explorer?from=2026-10-08&outcome=failure&ip=203.0.113.10',
  ])
})

test('an invalid typed IP sends no request; Reset clears its error and restores the view', async () => {
  const api = fakeApi({ ...API, '/api/explorer': { body: EXPLORER } })
  open('/explorer?country=GB')
  await screen.findByRole('table', { name: 'Login events' })
  const box = screen.getByRole('textbox', { name: 'IP address' })
  await userEvent.type(box, '999.1.2.3')
  await userEvent.click(screen.getByRole('button', { name: 'Apply IP' }))
  expect(screen.getByRole('alert')).toHaveTextContent('That is not a valid IP address.')
  expect(screen.getByRole('alert')).not.toHaveTextContent('999.1.2.3')
  expect(api.requests().some((request) => request.includes('999'))).toBe(false)
  await userEvent.click(screen.getByRole('button', { name: 'Reset' }))
  expect(await screen.findByRole('table', { name: 'Login events' })).toBeInTheDocument()
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'IP address' })).toHaveValue('')
})

test('a valid IP is applied on submission and Reset also works for an unsubmitted invalid draft', async () => {
  const api = fakeApi({ ...API, '/api/explorer': { body: EXPLORER } })
  open()
  await screen.findByRole('table', { name: 'Login events' })
  await userEvent.type(screen.getByRole('textbox', { name: 'IP address' }), '203.0.113.10')
  expect(api.requests()).not.toContain('/api/explorer?ip=203.0.113.10')
  await userEvent.click(screen.getByRole('button', { name: 'Apply IP' }))
  await vi.waitFor(() => expect(api.requests()).toContain('/api/explorer?ip=203.0.113.10'))
  await userEvent.click(screen.getByRole('button', { name: 'Reset' }))
  await screen.findByRole('table', { name: 'Login events' })
  await userEvent.type(screen.getByRole('textbox', { name: 'IP address' }), 'bad')
  await userEvent.click(screen.getByRole('button', { name: 'Apply IP' }))
  await userEvent.click(screen.getByRole('button', { name: 'Reset' }))
  expect(await screen.findByRole('table', { name: 'Login events' })).toBeInTheDocument()
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
})

test('no matching logins shows the shared empty state and zero counts', async () => {
  fakeApi({ ...API, '/api/explorer': { body: {
    summary: { total: 0, successes: 0, failures: 0, distinct_users: 0, distinct_ips: 0 }, rows: [],
  } } })
  open('/explorer?user=nobody')
  expect(await screen.findByText('No logins match these filters. Widen the date range or reset the filters.')).toBeInTheDocument()
  expect(screen.queryByRole('table')).not.toBeInTheDocument()
  expect(screen.getAllByRole('definition').map((node) => node.textContent)).toEqual(['0', '0', '0', '0', '0'])
})

test('hostile log fields stay plain cell text', async () => {
  const hostile = '<img src=x onerror=alert(1)>**bold** [link](javascript:alert(1))'
  fakeApi({ ...API, '/api/explorer': { body: { ...EXPLORER, rows: [{ ...rows[0], username: hostile, user_agent: hostile }] } } })
  open()
  const table = await screen.findByRole('table', { name: 'Login events' })
  expect(within(table).getAllByText(hostile).every((node) => node.tagName === 'TD')).toBe(true)
  expect(table.querySelector('img, a, script, iframe, strong')).toBeNull()
})

test('IP is confined to Explorer and shared filters travel to the other dashboard screens', async () => {
  fakeApi({ ...API, '/api/explorer': { body: EXPLORER } })
  open('/explorer?country=GB&ip=203.0.113.10')
  await screen.findByRole('table', { name: 'Login events' })
  const nav = screen.getByRole('navigation', { name: 'Screens' })
  expect(within(nav).getByRole('link', { name: 'Overview' })).toHaveAttribute('href', '/?country=GB')
  expect(within(nav).getByRole('link', { name: 'Alerts' })).toHaveAttribute('href', '/alerts?country=GB')
})

test('an API failure shows fixed text and hides the CSV link', async () => {
  fakeApi({ ...API, '/api/explorer': { status: 500, body: { error: { code: 'internal_error', message: 'SECRET TRACE' } } } })
  open()
  expect(await screen.findByText('The server could not answer. Try again in a moment.')).toBeInTheDocument()
  expect(document.body).not.toHaveTextContent('SECRET TRACE')
  expect(screen.queryByRole('link', { name: 'Download these rows (CSV)' })).not.toBeInTheDocument()
})
