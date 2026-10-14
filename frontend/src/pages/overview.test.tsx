import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, describe, expect, test, vi } from 'vitest'

import { AppRoutes } from '@/App'
import { DATASET, EMPTY_OVERVIEW, OVERVIEW, fakeApi } from '@/test/fake-api'

function openApp(address: string) {
  return render(
    <MemoryRouter initialEntries={[address]}>
      <AppRoutes />
    </MemoryRouter>,
  )
}

function tile(label: string) {
  return within(screen.getByRole('main')).getByText(label).closest('[data-slot=card]') as HTMLElement
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('the shell', () => {
  test('the sidebar links to the four screens', async () => {
    fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: OVERVIEW } })
    openApp('/')

    const nav = await screen.findByRole('navigation', { name: 'Screens' })
    expect(within(nav).getAllByRole('link').map((link) => link.textContent)).toEqual([
      'Overview',
      'Alerts',
      'Log explorer',
      'Investigator',
    ])
  })

  test('the header shows the label and the capture time from the dataset endpoint', async () => {
    fakeApi({
      '/api/dataset': {
        body: { ...DATASET, label: 'Test label', captured_at: '2026-03-05T17:45:00Z' },
      },
      '/api/overview': { body: OVERVIEW },
    })
    openApp('/')

    expect(await screen.findByText('Test label')).toBeInTheDocument()
    expect(screen.getByText('Log captured 5 Mar 2026, 17:45 UTC')).toBeInTheDocument()
  })
})

describe('the Overview', () => {
  test('overview counts match the reply, with labels that say what they count', async () => {
    fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: OVERVIEW } })
    openApp('/')

    await screen.findByText('Sign-in attempts')
    expect(tile('Sign-in attempts')).toHaveTextContent('1,856')
    expect(tile('Failed attempts')).toHaveTextContent('156')
    expect(tile('Failed attempts')).toHaveTextContent('8.4% of attempts')
    expect(tile('Usernames seen')).toHaveTextContent('41')
    expect(tile('Alerts')).toHaveTextContent('5')
    expect(tile('Alerts')).toHaveTextContent('findings in this view')
    expect(screen.getByText('Sign-in attempts per hour')).toBeInTheDocument()
    expect(screen.getByText('Top source IPs by failed sign-ins')).toBeInTheDocument()
  })

  test('one alert reads in the singular', async () => {
    fakeApi({
      '/api/dataset': { body: DATASET },
      '/api/overview': { body: { ...OVERVIEW, alert_count: 1 } },
    })
    openApp('/')

    await screen.findByText('Sign-in attempts')
    expect(tile('Alerts')).toHaveTextContent('finding in this view')
    expect(tile('Alerts')).not.toHaveTextContent('findings')
  })

  test('the filters in the address travel on the request, so a reload shows the same view', async () => {
    const api = fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: OVERVIEW } })
    openApp('/?user=alice.k&from=2026-10-07&outcome=failure')

    await screen.findByText('Sign-in attempts')
    expect(api.requests()).toContain('/api/overview?from=2026-10-07&outcome=failure&user=alice.k')
  })

  test('an empty filter shows a clear message instead of the tiles', async () => {
    fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: EMPTY_OVERVIEW } })
    openApp('/?user=nobody')

    expect(
      await screen.findByText(
        'No sign-ins match these filters. Widen the date range or reset the filters.',
      ),
    ).toBeInTheDocument()
    expect(screen.queryByText('Sign-in attempts')).not.toBeInTheDocument()
  })

  test('reset restores the whole log', async () => {
    const api = fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: OVERVIEW } })
    openApp('/?user=alice.k&outcome=failure')
    await screen.findByText('Sign-in attempts')

    await userEvent.click(screen.getByRole('button', { name: 'Reset' }))

    await vi.waitFor(() => expect(api.requests().at(-1)).toBe('/api/overview'))
  })
})

describe('the filter toolbar', () => {
  test('with no date filter, the date range shows the whole log', async () => {
    fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: OVERVIEW } })
    openApp('/')

    expect(await screen.findByRole('button', { name: 'Date range (UTC)' })).toHaveTextContent(
      '1 Oct 2026 – 8 Oct 2026',
    )
  })

  test('a date that does not exist is never shown back as one', async () => {
    fakeApi({
      '/api/dataset': { body: DATASET },
      '/api/overview': { status: 422, body: { error: { code: 'invalid_filter', message: '' } } },
    })
    openApp('/?from=2026-13-45')

    const dates = await screen.findByRole('button', { name: 'Date range (UTC)' })
    expect(dates).not.toHaveTextContent('undefined')
    expect(dates).not.toHaveTextContent('45')
  })

  test('a user the dataset does not hold still shows in the box, so the analyst sees what filters the view', async () => {
    fakeApi({ '/api/dataset': { body: DATASET }, '/api/overview': { body: EMPTY_OVERVIEW } })
    openApp('/?user=nobody&country=ZZ')

    expect(await screen.findByRole('combobox', { name: 'User' })).toHaveTextContent('nobody')
    expect(screen.getByRole('combobox', { name: 'Country' })).toHaveTextContent('ZZ')
  })
})

describe('error messages are fixed text and never show what the server sent', () => {
  const LEAK = 'Traceback: KeyError at /Users/someone/secret.py'

  test('a server failure', async () => {
    fakeApi({
      '/api/dataset': { body: DATASET },
      '/api/overview': { status: 500, body: { error: { code: 'internal_error', message: LEAK } } },
    })
    openApp('/')

    expect(
      await screen.findByText('The server could not answer. Try again in a moment.'),
    ).toBeInTheDocument()
    expect(document.body).not.toHaveTextContent('Traceback')
  })

  test('a filter the API refuses', async () => {
    fakeApi({
      '/api/dataset': { body: DATASET },
      '/api/overview': { status: 422, body: { error: { code: 'invalid_filter', message: LEAK } } },
    })
    openApp('/?from=yesterday')

    expect(
      await screen.findByText('A filter in the address is not valid. Reset the filters to continue.'),
    ).toBeInTheDocument()
    expect(document.body).not.toHaveTextContent('Traceback')
    expect(document.body).not.toHaveTextContent('yesterday')
  })

  test('a log that failed to load', async () => {
    fakeApi({
      '/api/dataset': { status: 500, body: { error: { code: 'log_invalid', message: LEAK } } },
      '/api/overview': { status: 500, body: { error: { code: 'log_invalid', message: LEAK } } },
    })
    openApp('/')

    expect(
      (await screen.findAllByText('The log could not be loaded. The server log says why.')).length,
    ).toBeGreaterThan(0)
    expect(document.body).not.toHaveTextContent('Traceback')
  })

  test('the API cannot be reached', async () => {
    fakeApi({ '/api/dataset': 'network-down', '/api/overview': 'network-down' })
    openApp('/')

    expect(
      (await screen.findAllByText('The API cannot be reached. Check that it is running.')).length,
    ).toBeGreaterThan(0)
    expect(document.body).not.toHaveTextContent('connection refused')
  })
})
