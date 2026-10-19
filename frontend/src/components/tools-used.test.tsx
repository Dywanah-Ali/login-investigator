import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'

import { ToolsUsed } from '@/components/tools-used'
import type { ToolView } from '@/lib/investigations'

const TOOLS: ToolView[] = [{
  name: 'search_logins', args: {}, title: 'Sign-in log', asked: 'All events',
  found: 'Ten rows found', columns: [], rows: null, raw: '{"total":10}',
}]

afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks() })

function panel(initialHeight = 20) {
  vi.useFakeTimers()
  const view = render(<div data-slot="message-scroller-viewport"><ToolsUsed tools={TOOLS} /></div>)
  const viewport = view.container.firstElementChild as HTMLDivElement
  // Supply geometry at the DOM boundary: CSS animation/layout does not run in jsdom.
  // Later messages extend the chat to 2,000px; they must not become the scroll target.
  Object.defineProperties(viewport, {
    clientHeight: { get: () => 100 },
    scrollHeight: { get: () => 2000 },
  })
  let height = initialHeight
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
    if (this === viewport) return new DOMRect(0, 0, 400, 100)
    if (this.dataset.slot === 'collapsible-content') return new DOMRect(0, 80 - viewport.scrollTop, 400, height)
    return new DOMRect()
  })
  const trigger = screen.getByRole('button', { name: 'Tools used (1)' })
  fireEvent.click(trigger)
  return { ...view, viewport, trigger, grow: (next: number) => { height = next } }
}

test('opening tools follows the selected evidence as it grows, then stops without jumping to later messages', () => {
  const { viewport, grow } = panel()
  act(() => vi.advanceTimersByTime(32))
  expect(viewport.scrollTop).toBe(0) // Already visible evidence does not move the reader.
  grow(200)
  act(() => vi.advanceTimersByTime(32))
  expect(viewport.scrollTop).toBe(180)
  grow(320)
  act(() => vi.advanceTimersByTime(32))
  expect(viewport.scrollTop).toBe(300)
  act(() => vi.advanceTimersByTime(1000))
  grow(600)
  act(() => vi.advanceTimersByTime(100))
  expect(viewport.scrollTop).toBe(300) // Expansion ended; no ongoing scroll lock.
})

test.each(['wheel', 'keydown'])('manual %s navigation stops following an opening panel', (event) => {
  const { viewport, grow, rerender } = panel()
  grow(200)
  act(() => vi.advanceTimersByTime(32))
  expect(viewport.scrollTop).toBe(180)
  fireEvent(viewport, new Event(event, { bubbles: true }))
  viewport.scrollTop = 15
  rerender(<div data-slot="message-scroller-viewport"><ToolsUsed tools={TOOLS} charactersPerSecond={40} /></div>)
  grow(600)
  act(() => vi.advanceTimersByTime(1000))
  expect(viewport.scrollTop).toBe(15)
})

test('closing or leaving the panel cancels the remaining expansion following', () => {
  const { viewport, trigger, grow, unmount } = panel()
  grow(200)
  act(() => vi.advanceTimersByTime(32))
  expect(viewport.scrollTop).toBe(180)
  fireEvent.click(trigger)
  viewport.scrollTop = 10
  grow(600)
  act(() => vi.advanceTimersByTime(1000))
  expect(viewport.scrollTop).toBe(10)
  fireEvent.click(trigger)
  const atUnmount = viewport.scrollTop
  unmount()
  grow(1000)
  act(() => vi.advanceTimersByTime(1000))
  expect(viewport.scrollTop).toBe(atUnmount)
})

test('reduced motion reveals full evidence once without following subsequent growth', () => {
  vi.spyOn(window, 'matchMedia').mockImplementation((query) => ({
    matches: query === '(prefers-reduced-motion: reduce)', media: query,
    onchange: null, addEventListener() {}, removeEventListener() {},
    addListener() {}, removeListener() {}, dispatchEvent: () => false,
  }))
  const { viewport, grow } = panel(200)
  expect(screen.getByText('Ten rows found')).toBeInTheDocument()
  expect(viewport.scrollTop).toBe(180)
  grow(600)
  act(() => vi.advanceTimersByTime(1000))
  expect(viewport.scrollTop).toBe(180)
})
