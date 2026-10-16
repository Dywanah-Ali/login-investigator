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

test('past Investigations show three, three more per click, and always the open one', async () => {
  api({ ...empty, id: 'case-7' })
  open('/investigator?id=case-7')
  const list = await screen.findByRole('navigation', { name: 'Past investigations' })
  await screen.findByRole('button', { name: /Question 7/ })
  expect(within(list).getAllByRole('button').map((b) => b.textContent?.split('16 Oct')[0])).toEqual(['Question 0', 'Question 1', 'Question 2', 'Question 7', 'Show three more'])
  await userEvent.click(screen.getByRole('button', { name: 'Show three more' }))
  expect(screen.getByRole('button', { name: /Question 5/ })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: /Question 6/ })).not.toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: 'Show three more' }))
  expect(screen.getByRole('button', { name: /Question 6/ })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Show three more' })).not.toBeInTheDocument()
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
  await act(async () => { stream.enqueue(new TextEncoder().encode('event: tool\r\ndata: {"name":"search_logins"}\r\n\r\nevent: text\r\ndata: {"text":"Live 🛡 answer"}\r\n\r\n')) })
  expect(screen.getByRole('status')).toHaveTextContent('Searching the sign-in log…')
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
const turn = { question: 'Find attacks', answer: 'There were attacks.', report: null, tools: [{ title: 'Sign-in log', asked: 'User: <b>alice</b>', found: '10 rows found', columns: ['User', 'Outcome'], rows: [{ User: '<img src=x>', Outcome: 'failure' }], raw: '{"hostile":"<iframe>"}' }] }

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
  expect(screen.getByRole('status')).toHaveTextContent('Writing the incident report…')
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeDisabled()
  const sent = fetcher.mock.calls.find(([url]) => url.endsWith('/report'))
  expect(JSON.parse(String(sent?.[1]?.body))).toEqual({ request: 'Update the incident report' })
  written = true
  await act(async () => finish(Response.json(report)))
  expect(await screen.findByText('High severity')).toBeInTheDocument()
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
  vi.stubGlobal('fetch', vi.fn(async (url: string, options?: RequestInit) => {
    if (url.endsWith('/report')) {
      askSignal = options?.signal as AbortSignal
      return new Promise<Response>((_resolve, reject) => { askSignal.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError'))) })
    }
    if (url.endsWith('/ask')) {
      askSignal = options?.signal as AbortSignal
      return new Response(new ReadableStream({ start(controller) { askSignal.addEventListener('abort', () => controller.error(new DOMException('Aborted', 'AbortError'))) } }), { headers: { 'Content-Type': 'text/event-stream' } })
    }
    if (url === '/api/investigations') return Response.json({ investigations: entries })
    return Response.json(url.endsWith('case-1') ? { ...empty, id: 'case-1', turns: [{ ...turn, answer: 'Reopened investigation answer' }] } : { ...empty, report_offer: kind === 'report' ? 'Write the incident report' : null })
  }))
  open('/investigator?id=case-0&ask=Investigate', (go) => { navigate = go })
  await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Send question' })).toBeEnabled())
  await userEvent.click(screen.getByRole('button', { name: kind === 'report' ? 'Write the incident report' : 'Send question' }))
  await vi.waitFor(() => expect(askSignal).toBeDefined())
  await act(async () => { await navigate('/investigator?id=case-1') })
  expect(askSignal.aborted).toBe(true)
  expect(await screen.findByText('Reopened investigation answer')).toBeInTheDocument()
  expect(screen.getByRole('textbox', { name: 'Question' })).toBeEnabled()
  expect(screen.queryByText('Investigate')).not.toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
})
