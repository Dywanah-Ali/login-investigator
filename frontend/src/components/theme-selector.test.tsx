import pageHtml from '../../index.html?raw'
import { runInNewContext } from 'node:vm'
import { act, cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, expect, test, vi } from 'vitest'
import { Link, MemoryRouter, Route, Routes } from 'react-router'
import { AppShell } from '@/components/app-shell'
import { ThemeProvider } from '@/components/theme-provider'
import { ThemeSelector } from '@/components/theme-selector'
import { THEME_STORAGE_KEY } from '@/lib/theme'

const originalScrollIntoView = Element.prototype.scrollIntoView
let systemDark = false
const listeners = new Set<() => void>()

beforeEach(() => {
  localStorage.clear()
  systemDark = false
  listeners.clear()
  vi.stubGlobal('matchMedia', vi.fn((query: string) => ({
    media: query,
    get matches() { return systemDark },
    addEventListener: (_event: string, callback: () => void) => listeners.add(callback),
    removeEventListener: (_event: string, callback: () => void) => listeners.delete(callback),
  })))
  vi.stubGlobal('fetch', vi.fn(async () => new Response('', { status: 503 })))
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
  Element.prototype.scrollIntoView = vi.fn()
})

afterEach(() => {
  cleanup()
  Element.prototype.scrollIntoView = originalScrollIntoView
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
  localStorage.clear()
  document.documentElement.classList.remove('dark')
})

function show() {
  return render(<ThemeProvider><ThemeSelector /></ThemeProvider>)
}

async function choose(label: 'Light' | 'Dark' | 'System') {
  const trigger = screen.getByRole('combobox', { name: 'Theme' })
  trigger.focus()
  await userEvent.keyboard('{Enter}')
  await userEvent.click(await screen.findByRole('option', { name: label }))
}

function changeSystem(dark: boolean) {
  act(() => { systemDark = dark; for (const callback of listeners) callback() })
}

test('System follows live operating-system changes and removes its listener on leaving', () => {
  const view = show()
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('System')
  expect(document.documentElement).not.toHaveClass('dark')
  changeSystem(true)
  expect(document.documentElement).toHaveClass('dark')
  changeSystem(false)
  expect(document.documentElement).not.toHaveClass('dark')
  view.unmount()
  expect(listeners.size).toBe(0)
})

test.each(['Light', 'Dark'] as const)('%s overrides the operating system and survives reopening', async (label) => {
  systemDark = label === 'Light'
  const view = show()
  await choose(label)
  expect(document.documentElement.classList.contains('dark')).toBe(label === 'Dark')
  changeSystem(!systemDark)
  changeSystem(!systemDark)
  expect(document.documentElement.classList.contains('dark')).toBe(label === 'Dark')
  view.unmount()
  show()
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent(label)
  expect(document.documentElement.classList.contains('dark')).toBe(label === 'Dark')
})

test('keyboard selection restores System and follows the operating system again', async () => {
  localStorage.setItem(THEME_STORAGE_KEY, 'light')
  systemDark = true
  show()
  expect(document.documentElement).not.toHaveClass('dark')
  screen.getByRole('combobox', { name: 'Theme' }).focus()
  await userEvent.keyboard('{Enter}{End}{Enter}')
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('System')
  expect(document.documentElement).toHaveClass('dark')
  changeSystem(false)
  expect(document.documentElement).not.toHaveClass('dark')
})

test('storage changes from another tab update the selected appearance', () => {
  show()
  act(() => {
    localStorage.setItem(THEME_STORAGE_KEY, 'dark')
    window.dispatchEvent(new StorageEvent('storage', { key: THEME_STORAGE_KEY }))
  })
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('Dark')
  expect(document.documentElement).toHaveClass('dark')
  act(() => {
    localStorage.clear()
    window.dispatchEvent(new StorageEvent('storage', { key: null }))
  })
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('System')
  expect(document.documentElement).not.toHaveClass('dark')
})

test('unavailable storage still allows switching for the current session', async () => {
  vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('Storage blocked') })
  vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('Storage blocked') })
  show()
  await choose('Dark')
  expect(document.documentElement).toHaveClass('dark')
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('Dark')
})

test('the header selector remains available across routes and dataset failures', async () => {
  render(<MemoryRouter><Routes><Route element={<AppShell />}>
    <Route index element={<Link to="/alerts">Open Alerts</Link>} />
    <Route path="alerts" element={<p>Alerts route</p>} />
  </Route></Routes></MemoryRouter>)
  await choose('Dark')
  await userEvent.click(screen.getByRole('link', { name: 'Open Alerts' }))
  expect(screen.getByText('Alerts route')).toBeInTheDocument()
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent('Dark')
  expect(document.documentElement).toHaveClass('dark')
})

const bootstrap = pageHtml.match(/<script>([\s\S]*?)<\/script>/)?.[1]

test.each([
  { saved: 'light', system: true, expected: false },
  { saved: 'dark', system: false, expected: true },
  { saved: 'system', system: true, expected: true },
  { saved: null, system: false, expected: false },
  { saved: 'invalid', system: true, expected: true },
  { saved: 'blocked', system: true, expected: true },
])('first-paint script matches the provider for $saved with system dark=$system', ({ saved, system, expected }) => {
  systemDark = system
  const blocked = saved === 'blocked'
  if (saved !== null && !blocked) localStorage.setItem(THEME_STORAGE_KEY, saved)
  if (blocked) vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('Storage blocked') })
  expect(bootstrap).toBeDefined()
  runInNewContext(bootstrap!, { document, localStorage, matchMedia: window.matchMedia })
  expect(document.documentElement.classList.contains('dark')).toBe(expected)
  show()
  expect(document.documentElement.classList.contains('dark')).toBe(expected)
  expect(screen.getByRole('combobox', { name: 'Theme' })).toHaveTextContent(saved === 'light' ? 'Light' : saved === 'dark' ? 'Dark' : 'System')
})
