import { act, fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { StrictMode, useEffect } from 'react'
import { MemoryRouter, useNavigate, type NavigateFunction } from 'react-router'
import { afterEach, expect, test, vi } from 'vitest'
import { InvestigatorPage } from '@/pages/investigator'

const entries = Array.from({ length: 8 }, (_, i) => ({ id: `case-${i}`, started_at: '2026-10-16T09:00:00Z', first_question: `Question ${i}` }))
const empty = { ...entries[0], turns: [], report_offer: null }
function open(address = '/investigator', onNavigate?: (navigate: NavigateFunction) => void) {
  function Navigator() {
    const navigate = useNavigate()
    useEffect(() => onNavigate?.(navigate), [navigate])
    return null
  }
  return render(<StrictMode><MemoryRouter initialEntries={[address]}><InvestigatorPage /><Navigator /></MemoryRouter></StrictMode>)
}
function api(detail: object = empty) {
  const fetcher = vi.fn(async (url: string, _options?: RequestInit) => Response.json(url === '/api/investigations' ? { investigations: entries } : detail))
  vi.stubGlobal('fetch', fetcher)
  return fetcher
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks() })

test('history arrows expand by three and collapse back to the newest three', async () => {
  api()
  open()
  const list = await screen.findByRole('navigation', { name: 'Past investigations' })
  await screen.findByRole('button', { name: /Question 0/ })
  const questions = () => within(list).getAllByRole('button', { name: /Question/ })
  expect(questions()).toHaveLength(3)
  const expand = screen.getByRole('button', { name: 'Show 3 more investigations' })
  expect(expand.textContent).toBe('')
  await userEvent.click(expand)
  expect(questions()).toHaveLength(6)
  await userEvent.click(screen.getByRole('button', { name: 'Show 2 more investigations' }))
  expect(questions()).toHaveLength(8)
  expect(screen.queryByRole('button', { name: /Show .* more investigations/ })).not.toBeInTheDocument()
  const collapse = screen.getByRole('button', { name: 'Show fewer investigations' })
  expect(collapse.textContent).toBe('')
  await userEvent.click(collapse)
  expect(questions()).toHaveLength(3)
  expect(screen.getByRole('button', { name: 'Show 3 more investigations' })).toBeInTheDocument()
})

test('opening an older Investigation reveals a continuous prefix and collapse retains its selection', async () => {
  api({ ...empty, id: 'case-4' })
  open('/investigator?id=case-4')
  await screen.findByRole('button', { name: /Question 4/ })
  const list = screen.getByRole('navigation', { name: 'Past investigations' })
  const questions = () => within(list).getAllByRole('button', { name: /Question/ })
  expect(questions().map((button) => button.textContent?.split('16 Oct')[0])).toEqual(
    Array.from({ length: 6 }, (_, i) => `Question ${i}`),
  )
  await userEvent.click(screen.getByRole('button', { name: 'Show 2 more investigations' }))
  expect(questions()).toHaveLength(8)
  await userEvent.click(screen.getByRole('button', { name: 'Show fewer investigations' }))
  expect(questions()).toHaveLength(6)
  expect(screen.getByRole('button', { name: /Question 4/ })).toHaveAttribute('aria-current', 'true')
})

test('deep-linked oldest Investigation keeps every intervening entry visible', async () => {
  api({ ...empty, id: 'case-7' })
  open('/investigator?id=case-7')
  await screen.findByRole('button', { name: /Question 7/ })
  const list = screen.getByRole('navigation', { name: 'Past investigations' })
  expect(within(list).getAllByRole('button', { name: /Question/ })).toHaveLength(8)
  expect(screen.getByRole('button', { name: 'Show fewer investigations' })).toBeDisabled()
})

test('Investigate arrival prepares the question without creating or asking', async () => {
  const fetcher = api()
  open('/investigator?ask=Investigate+this+alert')
  expect(screen.getByRole('textbox', { name: 'Question' })).toHaveValue('Investigate this alert')
  await screen.findByRole('button', { name: /Question 0/ })
  expect(fetcher.mock.calls.every(([, options]) => !options?.method || options.method === 'GET')).toBe(true)
  expect(screen.getByText(/I only read: I cannot block/)).toBeInTheDocument()
})

test('an empty chat contains its introduction and starter questions; choosing one only fills the input', async () => {
  const fetcher = api()
  open()
  const chat = screen.getByRole('region', { name: 'Investigation messages' })
  expect(within(chat).getByText(/I search the sign-in log/)).toBeInTheDocument()
  const starter = within(chat).getByRole('button', { name: 'Anything suspicious last night?' })
  await userEvent.click(starter)
  expect(screen.getByRole('textbox', { name: 'Question' })).toHaveValue('Anything suspicious last night?')
  expect(fetcher.mock.calls.every(([, options]) => !options?.method || options.method === 'GET')).toBe(true)
})

test('Enter sends the multiline question while Shift + Enter adds a newline and blank Enter does not send', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  const requests: { url: string; options?: RequestInit }[] = []
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    requests.push({ url, options })
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (options?.method === 'POST') return Response.json(empty)
    return Response.json(url === '/api/investigations' ? { investigations: entries } : empty)
  }))
  open()
  const input = screen.getByRole('textbox', { name: 'Question' })
  await userEvent.click(input)
  await userEvent.keyboard('{Enter}')
  expect(input).toHaveValue('')
  expect(requests.filter((request) => request.options?.method === 'POST')).toHaveLength(0)
  await userEvent.type(input, 'Check the log')
  await userEvent.keyboard('{Shift>}{Enter}{/Shift}Include the evidence')
  expect(input).toHaveValue('Check the log\nInclude the evidence')
  expect(requests.filter((request) => request.options?.method === 'POST')).toHaveLength(0)
  await userEvent.keyboard('{Enter}')
  await vi.waitFor(() => expect(stream).toBeDefined())
  expect(input).toBeDisabled()
  expect(input).toHaveValue('')
  const posts = requests.filter((request) => request.options?.method === 'POST')
  expect(posts.map((request) => request.url)).toEqual(['/api/investigations', '/api/investigations/case-0/ask'])
  expect(posts.map((request) => JSON.parse(String(request.options?.body)))).toEqual([
    { question: 'Check the log\nInclude the evidence' },
    { question: 'Check the log\nInclude the evidence' },
  ])
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n')); stream.close() })
  await vi.waitFor(() => expect(input).toBeEnabled())
})

test('Enter during input-method composition does not submit the question', async () => {
  const fetcher = api()
  open()
  const input = screen.getByRole('textbox', { name: 'Question' })
  await userEvent.type(input, 'Check the log')
  fireEvent.keyDown(input, { key: 'Enter', isComposing: true })
  expect(input).toHaveValue('Check the log')
  expect(fetcher.mock.calls.every(([, options]) => !options?.method || options.method === 'GET')).toBe(true)
})

test('create then ask locks input, streams tool progress and text, then redraws saved memory', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  let saved = false
  const requests: { url: string; options?: RequestInit }[] = []
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    requests.push({ url, options })
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (options?.method === 'POST') return Response.json(empty)
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json(saved ? { ...empty, turns: [{ question: 'Investigate', answer: 'Saved answer', tools: [], report: null }], report_offer: 'Write the incident report' } : empty)
  }))
  const view = open('/investigator?ask=Investigate')
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(stream).toBeDefined())
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeDisabled()
  expect(screen.getByRole('button', { name: 'Send question' })).toBeDisabled()
  const posts = requests.filter((r) => r.options?.method === 'POST')
  expect(posts.map((r) => r.url)).toEqual(['/api/investigations', '/api/investigations/case-0/ask'])
  expect(posts.map((r) => JSON.parse(String(r.options?.body)))).toEqual([{ question: 'Investigate' }, { question: 'Investigate' }])
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: tool\r\ndata: {"name":"search_logins","call_id":"search-1","phase":"start"}\r\n\r\nevent: text\r\ndata: {"text":"Live 🛡 answer"}\r\n\r\n')) })
  const progress = within(screen.getByRole('region', { name: 'Investigation messages' })).getByRole('status')
  expect(progress).toHaveTextContent('Searching the sign-in log…')
  expect(screen.getAllByRole('status')).toHaveLength(1)
  expect(screen.getByText('Live 🛡 answer')).toBeInTheDocument()
  saved = true
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n')); stream.close() })
  expect(await screen.findByText('Saved answer')).toBeInTheDocument()
  expect(screen.queryByText('Live 🛡 answer')).not.toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
  expect(screen.getByRole('button', { name: 'Write the incident report' })).toBeInTheDocument()
  expect(screen.queryByText(/I only read:/)).not.toBeInTheDocument()
  view.unmount()
})

test('typing a question in a new Investigation and clicking Send immediately shows the question', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (options?.method === 'POST') return Response.json(empty)
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json(empty)
  }))
  open('/investigator')
  await userEvent.click(screen.getByRole('button', { name: 'New investigation' }))
  await userEvent.type(screen.getByRole('textbox', { name: 'Question' }), 'Check the log')
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  expect(within(screen.getByRole('region', { name: 'Investigation messages' })).getByText('Check the log')).toBeInTheDocument()
  await vi.waitFor(() => expect(stream).toBeDefined())
  await act(async () => {
    stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n'))
    stream.close()
  })
})

test.each(['typed', 'starter'])('a new %s question appears once even when memory already contains the unfinished Turn', async (source) => {
  const question = 'Was any account compromised this week?'
  let stream!: ReadableStreamDefaultController<Uint8Array>
  let complete = false
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (options?.method === 'POST') return Response.json({ ...empty, first_question: question })
    if (url === '/api/investigations') return Response.json({ investigations: [] })
    // The core saves the human question before the answer finishes. Reopening mid-stream
    // can therefore return that question even though its streamed draft is still on screen.
    return Response.json({ ...empty, first_question: question, turns: [{ question, answer: complete ? 'Saved final answer' : '', tools: [], report: null }], report_offer: null })
  }))
  open()
  if (source === 'starter') await userEvent.click(screen.getByRole('button', { name: question }))
  else await userEvent.type(screen.getByRole('textbox', { name: 'Question' }), question)
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(stream).toBeDefined())
  await vi.waitFor(() => expect(screen.getByRole('button', { name: /Was any account compromised this week/ })).toHaveAttribute('aria-current', 'true'))
  const chat = () => within(screen.getByRole('region', { name: 'Investigation messages' }))
  expect(chat().getAllByText(question)).toHaveLength(1)
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: text\ndata: {"text":"Live partial answer"}\n\n')) })
  expect(chat().getByText('Live partial answer')).toBeInTheDocument()
  expect(chat().getAllByText(question)).toHaveLength(1)
  complete = true
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n')); stream.close() })
  expect(await chat().findByText('Saved final answer')).toBeInTheDocument()
  expect(chat().getAllByText(question)).toHaveLength(1)
  expect(chat().queryByText('Live partial answer')).not.toBeInTheDocument()
})

test('a failed final history reload keeps the single draft visible and unlocks a newly created Investigation', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (options?.method === 'POST') return Response.json({ ...empty, first_question: 'Check the log' })
    if (url === '/api/investigations') return Response.json({ investigations: [] })
    return Response.json({ error: { code: 'internal_error' } }, { status: 500 })
  }))
  open('/investigator?ask=Check+the+log')
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(screen.getByRole('button', { name: /Check the log/ })).toHaveAttribute('aria-current', 'true'))
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: text\ndata: {"text":"Live answer"}\n\nevent: done\ndata: {}\n\n')); stream.close() })
  expect(await screen.findByRole('alert')).toHaveTextContent('The server could not answer. Try again in a moment.')
  await vi.waitFor(() => expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled())
  const chat = within(screen.getByRole('region', { name: 'Investigation messages' }))
  expect(chat.getAllByText('Check the log')).toHaveLength(1)
  expect(chat.getByText('Live answer')).toBeInTheDocument()
  expect(chat.queryByText('Start an investigation')).not.toBeInTheDocument()
})

const report = { title: 'Incident <img src=x>', severity: 'high', summary: '**Plain summary**', attacker_ips: ['203.0.113.2'], affected_users: ['alice'], timeline: [{ time_utc: '2026-10-16T08:00:00Z', event: '<script>attack</script>' }], evidence: ['10 failures'], recommended_next_steps: ['Review the account'], number: 1 }
const turn = { question: 'Find attacks', answer: 'There were attacks.', report: null, tools: [{ name: 'search_logins', args: { user: '<b>alice</b>' }, title: 'Sign-in log', asked: 'User: <b>alice</b>', found: '10 rows found', columns: ['User', 'Outcome'], rows: [{ User: '<img src=x>', Outcome: 'failure' }], raw: '{"hostile":"<iframe>"}' }] }

test('reopened tools show asked and found, ordered table cells, and optional raw JSON', async () => {
  api({ ...empty, turns: [turn] })
  const { container } = open('/investigator?id=case-0')
  const toggle = await screen.findByRole('button', { name: 'Tools used (1)' })
  expect(screen.queryByText('10 rows found')).not.toBeInTheDocument()
  await userEvent.click(toggle)
  expect(screen.getByText('User: <b>alice</b>')).toBeInTheDocument()
  expect(screen.getByText('10 rows found')).toBeInTheDocument()
  expect(screen.getAllByRole('columnheader').map((cell) => cell.textContent)).toEqual(['User', 'Outcome'])
  expect(screen.getByRole('cell', { name: '<img src=x>' })).toBeInTheDocument()
  expect(screen.queryByText(turn.tools[0].raw)).not.toBeInTheDocument()
  await userEvent.click(screen.getByRole('switch', { name: 'Show raw JSON' }))
  expect(screen.getByText(turn.tools[0].raw)).toBeInTheDocument()
  expect(container.querySelector('img,iframe,b')).toBeNull()
})

test('Tools used counts calls, including repeated calls to the same tool', async () => {
  api({ ...empty, turns: [{ ...turn, tools: [turn.tools[0], turn.tools[0]] }] })
  open('/investigator?id=case-0')
  expect(await screen.findByRole('button', { name: 'Tools used (2)' })).toHaveAttribute('aria-expanded', 'false')
})

test('the core offer controls report wording, waiting, saved fields and numbered PDF download', async () => {
  let finish!: (response: Response) => void
  let written = false
  const fetcher = vi.fn(async (url: string, _options?: RequestInit) => {
    if (url.endsWith('/report')) return new Promise<Response>((resolve) => { finish = resolve })
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json({ ...empty, turns: written ? [turn, { question: 'Update the incident report', answer: '', tools: [], report }] : [turn], report_offer: written ? null : 'Update the incident report' })
  })
  vi.stubGlobal('fetch', fetcher)
  const { container } = open('/investigator?id=case-0')
  const writeButton = await screen.findByRole('button', { name: 'Update the incident report' })
  const viewport = screen.getByRole('region', { name: 'Investigation messages' })
  // Supply browser geometry at the DOM boundary. The DOM test environment has no layout engine.
  Object.defineProperties(viewport, {
    clientHeight: { configurable: true, get: () => 300 },
    scrollHeight: { configurable: true, get: () => written ? 1600 : 800 },
    scrollTo: { configurable: true, value: (options: ScrollToOptions) => { viewport.scrollTop = options.top ?? 0 } },
  })
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
    if (this === viewport) return new DOMRect(0, 0, 600, 300)
    if (this.dataset.slot === 'message-scroller-item') {
      const top = this.dataset.messageId === 'case-0-1' ? 800 : 0
      return new DOMRect(0, top - viewport.scrollTop, 600, 800)
    }
    return new DOMRect()
  })
  await act(async () => { await new Promise((resolve) => requestAnimationFrame(resolve)) })
  // The reader has left the bottom. The explicit report request must still reveal its result.
  fireEvent.wheel(viewport, { deltaY: -100 })
  viewport.scrollTop = 0
  fireEvent.scroll(viewport)
  await userEvent.click(writeButton)
  expect(within(viewport).getByRole('status')).toHaveTextContent('Writing the incident report…')
  expect(screen.getAllByRole('status')).toHaveLength(1)
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeDisabled()
  const sent = fetcher.mock.calls.find(([url]) => url.endsWith('/report'))
  expect(JSON.parse(String(sent?.[1]?.body))).toEqual({ request: 'Update the incident report' })
  written = true
  await act(async () => finish(Response.json(report)))
  expect(await screen.findByText('High severity')).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: 'Show full report' }))
  expect(screen.getByText('**Plain summary**')).toBeInTheDocument()
  expect(screen.getByText('2026-10-16T08:00:00Z: <script>attack</script>')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Download PDF' })).toHaveAttribute('href', '/api/investigations/case-0/reports/1.pdf')
  expect(viewport.scrollTop).toBe(1300)
  expect(screen.queryByRole('button', { name: 'Update the incident report' })).not.toBeInTheDocument()
  expect(container.querySelector('img,script')).toBeNull()
  // Automatic report reveal does not prevent the reader from scrolling back afterward.
  fireEvent.wheel(viewport, { deltaY: -100 })
  viewport.scrollTop = 0
  fireEvent.scroll(viewport)
  await userEvent.click(screen.getByRole('button', { name: 'Tools used (1)' }))
  expect(viewport.scrollTop).toBe(0)
})

test('only the new report reveals at the observed answer pace; reopening shows the full saved report', async () => {
  vi.useFakeTimers()
  let stream!: ReadableStreamDefaultController<Uint8Array>
  let answered = false
  let written = false
  const oldReport = { ...report, title: 'Earlier saved report', summary: 'Earlier saved summary' }
  const newReport = { ...report, number: 2, title: 'A newly generated incident report with a detailed descriptive title' }
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (url.endsWith('/report') && options?.method === 'POST') { written = true; return Response.json(newReport) }
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json({ ...empty, turns: [
      { ...turn, report: oldReport },
      ...(answered ? [{ ...turn, question: 'Follow-up', answer: 'Follow-up answer' }] : []),
      ...(written ? [{ question: 'Update the incident report', answer: '', tools: [], report: newReport }] : []),
    ], report_offer: answered && !written ? 'Update the incident report' : null })
  }))
  try {
    await act(async () => { open('/investigator?id=case-0') })
    expect(screen.getByText('Earlier saved summary')).toBeInTheDocument()
    await act(async () => {
      fireEvent.change(screen.getByRole('textbox', { name: 'Question' }), { target: { value: 'Follow-up' } })
    })
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Send question' })) })
    await act(async () => { stream.enqueue(new TextEncoder().encode('event: text\ndata: {"text":"First chunk"}\n\n')) })
    act(() => vi.advanceTimersByTime(500))
    // 200 characters over 0.5 seconds gives a measured delivery pace of 400 characters/second.
    await act(async () => { stream.enqueue(new TextEncoder().encode(`event: text\ndata: ${JSON.stringify({ text: 'a'.repeat(200) })}\n\n`)) })
    answered = true
    await act(async () => { stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n')); stream.close() })
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Update the incident report' })) })
    expect(screen.queryByText(newReport.title)).not.toBeInTheDocument()
    expect(screen.getByText('Earlier saved summary')).toBeInTheDocument()
    act(() => vi.advanceTimersByTime(160))
    const partialTitle = screen.getByText(/^A newly generated/).textContent ?? ''
    expect(partialTitle.length).toBeGreaterThan(50)
    expect(partialTitle.length).toBeLessThan(newReport.title.length)
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'New investigation' })) })
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: /Question 0/ })) })
    expect(screen.getByText(newReport.title)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Show full report' })).not.toBeInTheDocument()
  } finally { vi.useRealTimers() }
})

test('missing model configuration shows fixed text without leaking the server message', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => Response.json({ error: { code: 'agent_unavailable', message: 'secret traceback' } }, { status: 503 })))
  open()
  expect(await screen.findByRole('alert')).toHaveTextContent('OPENROUTER_API_KEY is not set. Copy env.example to .env and add the key.')
  expect(document.body).not.toHaveTextContent('secret traceback')
})

test('stream errors reload saved partial history and unlock the input without exposing error text', async () => {
  let failed = false
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.endsWith('/ask')) {
      failed = true
      return new Response('event: error\ndata: {"message":"secret traceback"}\n\n', { headers: { 'Content-Type': 'text/event-stream' } })
    }
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json({ ...empty, turns: failed ? [{ ...turn, answer: 'Saved partial answer' }] : [] })
  }))
  open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  expect(await screen.findByText('Saved partial answer')).toBeInTheDocument()
  expect(screen.getByRole('alert')).toHaveTextContent('The agent stopped before it finished.')
  expect(document.body).not.toHaveTextContent('secret traceback')
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
})

test('leaving during an answer aborts the fetch and does not reload history afterward', async () => {
  let askSignal: AbortSignal | undefined
  let historyReads = 0
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/ask')) {
      askSignal = options?.signal as AbortSignal
      return new Response(new ReadableStream({ start(controller) { askSignal?.addEventListener('abort', () => controller.error(new DOMException('Aborted', 'AbortError'))) } }), { headers: { 'Content-Type': 'text/event-stream' } })
    }
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    historyReads++
    return Response.json(empty)
  }))
  const view = open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(askSignal).toBeDefined())
  const reads = historyReads
  view.unmount()
  expect(askSignal?.aborted).toBe(true)
  await act(async () => {})
  expect(historyReads).toBe(reads)
})

test('text frames survive split delimiters and UTF-8 bytes; a missing done event is a fixed failure', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json(empty)
  }))
  open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(stream).toBeDefined())
  const bytes = new TextEncoder().encode(': keepalive\r\n\r\nevent: text\r\ndata: {"text":"🛡 evidence"}\r\n\r\n')
  await act(async () => { for (const byte of bytes) stream.enqueue(new Uint8Array([byte])) })
  expect(screen.getByText('🛡 evidence')).toBeInTheDocument()
  await act(async () => stream.close())
  expect(screen.getByRole('alert')).toHaveTextContent('The agent stopped before it finished.')
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
})

test.each(['answer', 'report'])('browser navigation during an %s aborts the old operation and opens usable saved history', async (kind) => {
  let navigate!: NavigateFunction
  let askSignal!: AbortSignal
  let toolStream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/report')) {
      askSignal = options?.signal as AbortSignal
      return new Promise<Response>((_resolve, reject) => { askSignal.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError'))) })
    }
    if (url.endsWith('/ask')) {
      askSignal = options?.signal as AbortSignal
      return new Response(new ReadableStream({ start(controller) { toolStream = controller; askSignal.addEventListener('abort', () => controller.error(new DOMException('Aborted', 'AbortError'))) } }), { headers: { 'Content-Type': 'text/event-stream' } })
    }
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json(url.endsWith('case-1') ? { ...empty, id: 'case-1', turns: [{ ...turn, answer: 'Reopened investigation answer' }] } : { ...empty, report_offer: kind === 'report' ? 'Write the incident report' : null })
  }))
  open('/investigator?id=case-0&ask=Investigate', (go) => { navigate = go })
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: kind === 'report' ? 'Write the incident report' : 'Send question' }))
  await vi.waitFor(() => expect(askSignal).toBeDefined())
  if (kind === 'answer') {
    await act(async () => toolStream.enqueue(new TextEncoder().encode(
      'event: tool\ndata: {"name":"lookup_ip_reputation","call_id":"old-case","phase":"start"}\n\n',
    )))
    expect(screen.getByRole('status')).toHaveTextContent('Looking up IP reputation…')
  }
  await act(async () => { await navigate('/investigator?id=case-1') })
  expect(askSignal.aborted).toBe(true)
  expect(await screen.findByText('Reopened investigation answer')).toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
  expect(screen.queryByText('Investigate')).not.toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
})

test('batched tool starts show one combined status and each terminal call removes only itself', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    return Response.json(url === '/api/investigations' ? { investigations: entries } : empty)
  }))
  open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(stream).toBeDefined())
  const emit = async (...payloads: object[]) => act(async () => {
    stream.enqueue(new TextEncoder().encode(payloads.map((data) => `event: tool\ndata: ${JSON.stringify(data)}\n\n`).join('')))
  })
  await emit(
    { name: 'lookup_ip_reputation', call_id: 'rep-1', phase: 'start' },
    { name: 'search_logins', call_id: 'log-1', phase: 'start' },
    { name: 'lookup_ip_reputation', call_id: 'rep-2', phase: 'start' },
  )
  expect(screen.getAllByRole('status')).toHaveLength(1)
  expect(screen.getByRole('status')).toHaveTextContent('Searching the sign-in log and looking up IP reputation…')
  await emit({ name: 'lookup_ip_reputation', call_id: 'rep-1', phase: 'end' })
  expect(screen.getByRole('status')).toHaveTextContent('Searching the sign-in log and looking up IP reputation…')
  await emit({ name: 'search_logins', call_id: 'log-1', phase: 'error' })
  expect(screen.getByRole('status')).toHaveTextContent('Looking up IP reputation…')
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  await emit({ name: 'lookup_ip_reputation', call_id: 'rep-2', phase: 'end' })
  expect(screen.getByRole('status')).toHaveTextContent('Thinking…')
  await act(async () => stream.enqueue(new TextEncoder().encode('event: text\ndata: {"text":"Answer"}\n\n')))
  expect(screen.getByRole('status')).toHaveTextContent('Writing the answer…')
  await act(async () => {
    stream.enqueue(new TextEncoder().encode('event: done\ndata: {}\n\n'))
    stream.close()
  })
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
})

test('a fast completed lookup does not leave a stale tool status while answer text streams', async () => {
  let stream!: ReadableStreamDefaultController<Uint8Array>
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.endsWith('/ask')) return new Response(new ReadableStream({ start(controller) { stream = controller } }), { headers: { 'Content-Type': 'text/event-stream' } })
    return Response.json(url === '/api/investigations' ? { investigations: entries } : empty)
  }))
  open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  await vi.waitFor(() => expect(stream).toBeDefined())
  await act(async () => stream.enqueue(new TextEncoder().encode(
    'event: tool\ndata: {"name":"lookup_ip_reputation","call_id":"fast","phase":"start"}\n\n'
    + 'event: tool\ndata: {"name":"lookup_ip_reputation","call_id":"fast","phase":"end"}\n\n'
    + 'event: text\ndata: {"text":"Evidence"}\n\n',
  )))
  expect(screen.getByRole('status')).toHaveTextContent('Writing the answer…')
  expect(screen.queryByText('Looking up IP reputation…')).not.toBeInTheDocument()
  await act(async () => {
    stream.enqueue(new TextEncoder().encode('event: error\ndata: {"code":"agent_failed"}\n\n'))
    stream.close()
  })
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
  expect(screen.getByRole('alert')).toHaveTextContent('The agent stopped before it finished.')
})


test.each([
  { name: '<img src=hostile>', call_id: 'one', phase: 'start' },
  { name: 'search_logins', call_id: 'one', phase: 'unknown' },
  { name: 'search_logins', phase: 'start' },
])('malformed tool lifecycle data produces a fixed error: %j', async (payload) => {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.endsWith('/ask')) return new Response(
      `event: tool\ndata: ${JSON.stringify(payload)}\n\n`,
      { headers: { 'Content-Type': 'text/event-stream' } },
    )
    return Response.json(url === '/api/investigations' ? { investigations: entries } : empty)
  }))
  open('/investigator?id=case-0&ask=Investigate')
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: 'Send question' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('The agent stopped before it finished.')
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
})
