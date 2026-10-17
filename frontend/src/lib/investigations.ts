import { ApiFailure, request } from '@/lib/api'

export type InvestigationEntry = { id: string; started_at: string; first_question: string }
export type ToolView = { name: string; args: Record<string, unknown>; title: string; asked: string; found: string; columns: string[]; rows: Record<string, unknown>[] | null; raw: string }
export type IncidentReport = {
  title: string; severity: 'none' | 'low' | 'medium' | 'high' | 'critical'; summary: string
  attacker_ips: string[]; affected_users: string[]; timeline: { time_utc: string; event: string }[]
  evidence: string[]; recommended_next_steps: string[]; number: number
}
export type Turn = { question: string; answer: string; tools: ToolView[]; report: IncidentReport | null }
export type Investigation = InvestigationEntry & { turns: Turn[]; report_offer: string | null }

export const investigationPath = (id: string) => `/api/investigations/${encodeURIComponent(id)}`
export async function postJson<T>(path: string, body: object, signal: AbortSignal): Promise<T> {
  const response = await request(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal })
  return await response.json() as T
}

export type AnswerEvent = { kind: 'text'; text: string } | { kind: 'tool'; name: string } | { kind: 'done' | 'error' }

/** SSE frames can cross network chunks, UTF-8 characters and CRLF boundaries. */
export async function ask(id: string, question: string, signal: AbortSignal, onEvent: (event: AnswerEvent) => void) {
  const response = await request(`${investigationPath(id)}/ask`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question }), signal,
  })
  if (!response.body || !response.headers.get('Content-Type')?.includes('text/event-stream')) throw new ApiFailure('agent_failed')
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  try {
    while (true) {
      const { value, done } = await reader.read()
      if (signal.aborted) return
      buffer += decoder.decode(value, { stream: !done })
      let boundary: RegExpExecArray | null
      while ((boundary = /\r\n\r\n|\n\n|\r\r/.exec(buffer))) {
        const frame = buffer.slice(0, boundary.index)
        buffer = buffer.slice(boundary.index + boundary[0].length)
        const lines = frame.split(/\r\n|\n|\r/)
        const kind = lines.find((line) => line.startsWith('event:'))?.slice(6).trim()
        const payload = lines.filter((line) => line.startsWith('data:')).map((line) => line.slice(5).replace(/^ /, '')).join('\n')
        if (!kind || !payload) continue // keepalive comments
        const data = JSON.parse(payload) as { text?: unknown; name?: unknown }
        if (kind === 'text' && typeof data.text === 'string') onEvent({ kind, text: data.text })
        if (kind === 'tool' && typeof data.name === 'string') onEvent({ kind, name: data.name })
        if (kind === 'done' || kind === 'error') { onEvent({ kind }); return }
      }
      if (done) throw new ApiFailure('agent_failed')
    }
  } finally {
    await reader.cancel().catch(() => {})
    reader.releaseLock()
  }
}
