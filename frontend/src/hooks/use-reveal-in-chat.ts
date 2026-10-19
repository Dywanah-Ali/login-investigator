import { useLayoutEffect, useRef } from 'react'

/** Follow an explicitly opened panel, without moving the page or chasing later chat turns. */
export function useRevealInChat(open: boolean, durationMs: number) {
  const content = useRef<HTMLDivElement>(null)

  useLayoutEffect(() => {
    if (!open) return
    const panel = content.current
    const viewport = panel?.closest<HTMLElement>('[data-slot="message-scroller-viewport"]')
    if (!panel || !viewport) return

    const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : durationMs
    const until = performance.now() + duration
    let frame = 0
    let following = true
    const interruptions = ['wheel', 'touchstart', 'pointerdown', 'keydown'] as const

    const stop = () => {
      following = false
      cancelAnimationFrame(frame)
      for (const event of interruptions) viewport.removeEventListener(event, stop)
    }

    const reveal = (now: number) => {
      if (!following) return
      const overflow = panel.getBoundingClientRect().bottom - viewport.getBoundingClientRect().bottom
      if (overflow > 0) {
        viewport.scrollTop = Math.min(
          viewport.scrollTop + overflow,
          Math.max(0, viewport.scrollHeight - viewport.clientHeight),
        )
      }
      if (now < until) frame = requestAnimationFrame(reveal)
      else stop()
    }

    for (const event of interruptions) viewport.addEventListener(event, stop, { passive: true })
    // Layout is ready for reduced motion; otherwise subsequent frames follow the CSS growth.
    reveal(performance.now())
    return stop
  }, [open, durationMs])

  return content
}
