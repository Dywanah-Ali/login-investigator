import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, describe, expect, test, vi } from 'vitest'

import { AppRoutes } from '@/App'
import { ALERTS, DATASET, RULES, fakeApi } from '@/test/fake-api'

function openApp(address: string) {
  return render(
    <MemoryRouter initialEntries={[address]}>
      <AppRoutes />
    </MemoryRouter>,
  )
}

/** A paragraph whose whole text is this, even when part of it is bold. */
const paragraph = (text: string) => (_: string, element: Element | null) =>
  element?.tagName === 'P' && element.textContent === text

const API = { '/api/dataset': { body: DATASET }, '/api/rules': { body: RULES } }

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('the Alerts table', () => {
  test("shows v1's seven columns, rule titles from the rules endpoint, names cut to three", async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts')

    const table = await screen.findByRole('table', { name: 'Alerts' })
    expect(within(table).getAllByRole('columnheader').map((th) => th.textContent)).toEqual([
      'Rule',
      'Summary',
      'IP addresses',
      'Users',
      'Events',
      'First seen (UTC)',
      'Last seen (UTC)',
    ])
    const rows = within(table).getAllByRole('row').slice(1)
    expect(rows.map((tr) => within(tr).getAllByRole('cell').map((td) => td.textContent))).toEqual([
      [
        'Sign-in from a new country',
        'olivia.bennett signed in from RU for the first time.',
        '91.142.73.116',
        'olivia.bennett',
        '1',
        '2026-10-06 13:47',
        '2026-10-06 13:47',
      ],
      [
        'Password spraying',
        '2.57.122.53 failed on 4 accounts within an hour.',
        '2.57.122.53',
        'admin, backup, helpdesk and 1 more',
        '23',
        '2026-10-05 23:04',
        '2026-10-06 00:17',
      ],
    ])
  })

  test('the counts line gives the total and a count per rule title, in title order', async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts')

    expect(
      await screen.findByText(
        paragraph(
          '2 alerts in the selected period · Password spraying: 1 · Sign-in from a new country: 1',
        ),
      ),
    ).toBeInTheDocument()
  })
})

describe('the side panel', () => {
  test('a row click opens its evidence, the explorer link and the Investigate link', async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts?country=RO')

    await userEvent.click(await screen.findByText('2.57.122.53 failed on 4 accounts within an hour.'))

    const panel = await screen.findByRole('dialog', { name: 'Password spraying' })
    expect(
      within(panel).getByText('Showing 2 of 23 events: the first and the last ones.'),
    ).toBeInTheDocument()
    const evidence = within(panel).getByRole('table', { name: 'Evidence' })
    expect(within(evidence).getAllByRole('columnheader').map((th) => th.textContent)).toEqual([
      'Time (UTC)',
      'User',
      'Source IP',
      'Country',
      'Outcome',
      'Failure reason',
      'User agent',
    ])
    expect(
      within(evidence).getAllByRole('row').slice(1).map((tr) => tr.textContent),
    ).toEqual([
      '2026-10-05 23:04:00admin2.57.122.53ROfailureunknown_usercurl/8.4.0',
      '2026-10-06 00:17:29test2.57.122.53ROfailureunknown_usercurl/8.4.0',
    ])
    // The explorer link carries the alert's IP and dates only, not the Alerts screen's filters.
    expect(within(panel).getByRole('link', { name: 'Open in Log explorer' })).toHaveAttribute(
      'href',
      '/explorer?ip=2.57.122.53&from=2026-10-05&to=2026-10-06',
    )
    const ask = new URL(
      within(panel).getByRole('link', { name: 'Investigate' }).getAttribute('href') ?? '',
      'http://localhost',
    )
    expect(ask.pathname).toBe('/investigator')
    expect(ask.searchParams.get('ask')).toBe(
      'Investigate the Password spraying alert: 2.57.122.53 against admin ' +
        'from 2026-10-05 23:04:00 to 2026-10-06 00:17:29 UTC.',
    )
  })

  test('an alert with every event shown says so, in the singular for one event', async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts')

    await userEvent.click(await screen.findByText('Sign-in from a new country'))

    const panel = await screen.findByRole('dialog', { name: 'Sign-in from a new country' })
    expect(within(panel).getByText('Showing 1 of 1 event.')).toBeInTheDocument()
  })

  test('the panel opens from the keyboard too', async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts')
    await screen.findByRole('table', { name: 'Alerts' })

    screen.getByText('Sign-in from a new country').closest('tr')?.focus()
    await userEvent.keyboard('{Enter}')

    expect(await screen.findByRole('dialog', { name: 'Sign-in from a new country' })).toBeInTheDocument()
  })
})

describe('How these rules work', () => {
  test('is collapsed at first and opens to the text the rules endpoint sent', async () => {
    fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts')

    const toggle = await screen.findByRole('button', { name: 'How these rules work' })
    expect(screen.queryByText('A list is worked through.')).not.toBeInTheDocument()

    await userEvent.click(toggle)

    expect(screen.getByText(paragraph('Brute force. Fires when: Twenty failures.'))).toBeInTheDocument()
    expect(screen.getByText(paragraph('Assumption: A list is worked through.'))).toBeInTheDocument()
    const guide = toggle.closest('[data-slot=collapsible]') as HTMLElement
    expect(within(guide).getAllByRole('listitem').map((li) => li.textContent)).toEqual([
      'Thresholds fit this dataset.',
      'Usernames ignore case.',
    ])
  })

  test('is there even when no alert matches, as in v1', async () => {
    fakeApi({ ...API, '/api/alerts': { body: { alerts: [] } } })
    openApp('/alerts?user=nobody')

    expect(
      await screen.findByText('No alerts match these filters. Widen the date range or reset the filters.'),
    ).toBeInTheDocument()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'How these rules work' })).toBeInTheDocument()
  })
})

describe('requests and failures', () => {
  test('the filters in the address travel on the alerts request; the rules take none', async () => {
    const api = fakeApi({ ...API, '/api/alerts': { body: ALERTS } })
    openApp('/alerts?user=alice.k&from=2026-10-07&outcome=failure')

    await screen.findByRole('table', { name: 'Alerts' })
    expect(api.requests()).toContain('/api/alerts?from=2026-10-07&outcome=failure&user=alice.k')
    expect(api.requests()).toContain('/api/rules')
  })

  test('a server failure is fixed text and never what the server sent', async () => {
    const LEAK = 'Traceback: KeyError at /Users/someone/secret.py'
    fakeApi({
      ...API,
      '/api/alerts': { status: 500, body: { error: { code: 'internal_error', message: LEAK } } },
    })
    openApp('/alerts')

    expect(
      await screen.findByText('The server could not answer. Try again in a moment.'),
    ).toBeInTheDocument()
    expect(document.body).not.toHaveTextContent('Traceback')
  })

  test('without the rules guide the table cannot name its rules, so the failure is told', async () => {
    fakeApi({
      '/api/dataset': { body: DATASET },
      '/api/rules': 'network-down',
      '/api/alerts': { body: ALERTS },
    })
    openApp('/alerts')

    expect(
      await screen.findByText('The API cannot be reached. Check that it is running.'),
    ).toBeInTheDocument()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()
  })
})

describe('log fields appear only in table cells', () => {
  test('a hostile summary, IP and username stay plain text inside cells', async () => {
    const hostile = '<img src=x onerror=alert(1)>**bold** [link](javascript:alert(1))'
    const alert = {
      ...ALERTS.alerts[0],
      summary: hostile,
      ips: [hostile],
      users: [hostile],
      evidence: [{ ...ALERTS.alerts[0].evidence[0], username: hostile, user_agent: hostile }],
    }
    fakeApi({ ...API, '/api/alerts': { body: { alerts: [alert] } } })
    openApp('/alerts')

    const table = await screen.findByRole('table', { name: 'Alerts' })
    await userEvent.click(within(table).getAllByText(hostile)[0])
    const panel = await screen.findByRole('dialog')

    // Nothing in the value became markup: no image, no bold, no link.
    expect(document.body.querySelector('img')).toBeNull()
    expect(document.body.querySelector('a[href^="javascript"]')).toBeNull()
    expect([...document.body.querySelectorAll('strong')].map((b) => b.textContent)).toEqual([
      '1 alert in the selected period',
    ])
    // Every place the value shows is a table cell.
    const shown = screen.getAllByText(hostile)
    expect(shown.length).toBe(5) // summary, IPs, users in the table; username, user agent in the panel
    expect(shown.every((node) => node.tagName === 'TD')).toBe(true)
    expect(within(panel).getAllByText(hostile)).toHaveLength(2)
  })
})
