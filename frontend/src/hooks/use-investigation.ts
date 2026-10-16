import { useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import { ApiFailure, FAILURE_TEXT, getJson } from '@/lib/api'
import { ask, investigationPath, postJson, type Investigation, type InvestigationEntry } from '@/lib/investigations'

const PROGRESS: Record<string, string> = {
  find_suspicious_activity: 'Checking the detection rules…',
  search_logins: 'Searching the sign-in log…',
  lookup_ip_reputation: 'Looking up IP reputation…',
}
const message = (error: unknown) => error instanceof ApiFailure ? error.message : FAILURE_TEXT.failed

/** Owns each request until it completes or the screen unmounts. Saved history wins over drafts. */
export function useInvestigation() {
  const [params, setParams] = useSearchParams()
  const id = params.get('id')
  const prepared = params.get('ask')
  const [input, setInput] = useState({ prepared, text: prepared ?? '' })
  const question = input.prepared === prepared ? input.text : prepared ?? ''
  const setQuestion = (text: string) => setInput({ prepared, text })
  const [entries, setEntries] = useState<InvestigationEntry[]>([])
  const [history, setHistory] = useState<{ id: string | null; data: Investigation | null }>({ id: null, data: null })
  const data = history.id === id ? history.data : null
  const loading = id !== null && history.id !== id
  const [failure, setFailure] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [progress, setProgress] = useState('')
  const [draft, setDraft] = useState<{ question: string; answer: string } | null>(null)
  const operation = useRef<AbortController | null>(null)
  const historyRequest = useRef<AbortController | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    getJson<{ investigations: InvestigationEntry[] }>('/api/investigations', '', controller.signal)
      .then((reply) => setEntries(reply.investigations))
      .catch((error) => { if (!controller.signal.aborted) setFailure(message(error)) })
    return () => { controller.abort(); operation.current?.abort() }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    historyRequest.current = controller
    if (id) getJson<Investigation>(investigationPath(id), '', controller.signal)
      .then((reply) => { if (!controller.signal.aborted) setHistory({ id, data: reply }) })
      .catch((error) => {
        if (!controller.signal.aborted) { setFailure(message(error)); setHistory({ id, data: null }) }
      })
    return () => controller.abort()
  }, [id])

  async function refresh(currentId: string, signal: AbortSignal) {
    historyRequest.current?.abort()
    const reply = await getJson<Investigation>(investigationPath(currentId), '', signal)
    if (!signal.aborted) { setHistory({ id: currentId, data: reply }); setDraft(null) }
  }

  async function send() {
    const text = question.trim()
    if (operation.current || loading || !text || text.length > 2000) return
    const controller = new AbortController()
    operation.current = controller
    setBusy(true)
    setFailure(null)
    setProgress('Thinking…')
    setDraft({ question: text, answer: '' })
    setQuestion('')
    let currentId = id
    try {
      if (!currentId) {
        const created = await postJson<InvestigationEntry>('/api/investigations', { question: text }, controller.signal)
        if (controller.signal.aborted) return
        currentId = created.id
        setEntries((old) => [created, ...old.filter((entry) => entry.id !== created.id)])
        setParams({ id: currentId }, { replace: true })
      }
      await ask(currentId, text, controller.signal, (event) => {
        if (event.kind === 'tool') setProgress(PROGRESS[event.name] ?? 'Running an investigation tool…')
        if (event.kind === 'text') setDraft((old) => old ? { ...old, answer: old.answer + event.text } : old)
        if (event.kind === 'error') setFailure(FAILURE_TEXT.agent_failed)
      })
    } catch (error) {
      if (!controller.signal.aborted) setFailure(message(error))
    } finally {
      if (!controller.signal.aborted) {
        if (currentId) {
          try { await refresh(currentId, controller.signal) }
          catch (error) { if (!controller.signal.aborted) setFailure(message(error)) }
        } else { setDraft(null); setQuestion(text) }
        if (!controller.signal.aborted) { setBusy(false); setProgress(''); operation.current = null }
      }
    }
  }

  function select(nextId?: string) {
    if (operation.current) return
    setParams(nextId ? { id: nextId } : {})
    setQuestion('')
    setDraft(null)
    setFailure(null)
  }

  async function writeReport() {
    if (!id || !data?.report_offer || operation.current || loading) return
    const controller = new AbortController()
    operation.current = controller
    setBusy(true)
    setFailure(null)
    setProgress('Writing the incident report…')
    try {
      await postJson(`${investigationPath(id)}/report`, { request: data.report_offer }, controller.signal)
    } catch (error) {
      if (!controller.signal.aborted) setFailure(message(error))
    } finally {
      if (!controller.signal.aborted) {
        try { await refresh(id, controller.signal) }
        catch (error) { if (!controller.signal.aborted) setFailure(message(error)) }
        if (!controller.signal.aborted) { setBusy(false); setProgress(''); operation.current = null }
      }
    }
  }

  return { id, question, setQuestion, entries, data, failure, loading, busy, progress, draft, send, select, writeReport }
}
