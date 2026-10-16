import { useCallback, useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import { ApiFailure, FAILURE_TEXT, getJson } from '@/lib/api'
import { ask, investigationPath, postJson, type IncidentReport, type Investigation, type InvestigationEntry } from '@/lib/investigations'

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
  const [reportReveal, setReportReveal] = useState<{ id: string; number: number; charactersPerSecond: number } | null>(null)
  // Used when no sufficiently long streamed text sample has been observed on this page yet.
  const answerPace = useRef(200)
  const operation = useRef<{ id: string | null; controller: AbortController } | null>(null)
  const historyRequest = useRef<AbortController | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    getJson<{ investigations: InvestigationEntry[] }>('/api/investigations', '', controller.signal)
      .then((reply) => setEntries(reply.investigations))
      .catch((error) => { if (!controller.signal.aborted) setFailure(message(error)) })
    return () => { controller.abort(); operation.current?.controller.abort() }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    historyRequest.current = controller
    // Creating an Investigation changes its URL while the first ask is running. Its saved
    // human question can already exist, so loading history now would duplicate the draft.
    // finish() loads that history and replaces the draft when the operation ends.
    if (id && operation.current?.id !== id) getJson<Investigation>(investigationPath(id), '', controller.signal)
      .then((reply) => { if (!controller.signal.aborted) setHistory({ id, data: reply }) })
      .catch((error) => {
        if (!controller.signal.aborted) { setFailure(message(error)); setHistory({ id, data: null }) }
      })
    return () => {
      controller.abort()
      setReportReveal(null)
      // Browser Back/Forward bypasses disabled controls. A newly created ID has already
      // taken ownership before its URL changes, so that intentional transition continues.
      if (operation.current?.id === id) {
        operation.current.controller.abort()
        operation.current = null
        setBusy(false)
        setProgress('')
        setDraft(null)
      }
    }
  }, [id])

  async function refresh(currentId: string, signal: AbortSignal) {
    historyRequest.current?.abort()
    const reply = await getJson<Investigation>(investigationPath(currentId), '', signal)
    if (!signal.aborted) { setHistory({ id: currentId, data: reply }); setDraft(null) }
  }

  function begin(progressText: string) {
    const controller = new AbortController()
    const active = { id, controller }
    operation.current = active
    setBusy(true)
    setFailure(null)
    setProgress(progressText)
    setReportReveal(null)
    return active
  }

  async function finish(currentId: string | null, controller: AbortController) {
    if (controller.signal.aborted) return
    if (currentId) {
      try { await refresh(currentId, controller.signal) }
      catch (error) { if (!controller.signal.aborted) setFailure(message(error)) }
    }
    if (!controller.signal.aborted && operation.current?.controller === controller) {
      setBusy(false)
      setProgress('')
      operation.current = null
    }
  }

  async function send() {
    const text = question.trim()
    if (operation.current || loading || !text || text.length > 2000) return
    const active = begin('Thinking…')
    const { controller } = active
    setDraft({ question: text, answer: '' })
    setQuestion('')
    let currentId = id
    let lastTextAt: number | null = null
    let textMilliseconds = 0
    let textCharacters = 0
    try {
      if (!currentId) {
        const created = await postJson<InvestigationEntry>('/api/investigations', { question: text }, controller.signal)
        if (controller.signal.aborted) return
        currentId = created.id
        active.id = currentId
        // Create returns an empty record. Keep that known state without reading an in-flight
        // checkpoint, and avoid leaving loading stuck if the final history refresh fails.
        setHistory({ id: currentId, data: { ...created, turns: [], report_offer: null } })
        setEntries((old) => [created, ...old.filter((entry) => entry.id !== created.id)])
        setParams({ id: currentId }, { replace: true })
      }
      await ask(currentId, text, controller.signal, (event) => {
        if (event.kind === 'tool') {
          lastTextAt = null
          setProgress(PROGRESS[event.name] ?? 'Running an investigation tool…')
        }
        if (event.kind === 'text') {
          const now = performance.now()
          const elapsed = lastTextAt === null ? 0 : now - lastTextAt
          // Measure text delivery, excluding the initial wait, tools and long network pauses.
          if (elapsed > 0 && elapsed <= 1500) {
            textMilliseconds += elapsed
            textCharacters += Array.from(event.text).length
            if (textMilliseconds >= 250) answerPace.current = Math.max(40, Math.min(600, textCharacters * 1000 / textMilliseconds))
          }
          lastTextAt = now
          setDraft((old) => old ? { ...old, answer: old.answer + event.text } : old)
        }
        if (event.kind === 'error') setFailure(FAILURE_TEXT.agent_failed)
      })
    } catch (error) {
      if (!controller.signal.aborted) setFailure(message(error))
    } finally {
      if (!controller.signal.aborted && !currentId) { setDraft(null); setQuestion(text) }
      await finish(currentId, controller)
    }
  }

  function select(nextId?: string) {
    if (operation.current) return
    setParams(nextId ? { id: nextId } : {})
    setQuestion('')
    setDraft(null)
    setReportReveal(null)
    setFailure(null)
  }

  async function writeReport() {
    if (!id || !data?.report_offer || operation.current || loading) return
    const { controller } = begin('Writing the incident report…')
    try {
      const report = await postJson<IncidentReport>(`${investigationPath(id)}/report`, { request: data.report_offer }, controller.signal)
      if (!controller.signal.aborted) setReportReveal({ id, number: report.number, charactersPerSecond: answerPace.current })
    } catch (error) {
      if (!controller.signal.aborted) setFailure(message(error))
    } finally {
      await finish(id, controller)
    }
  }

  const completeReportReveal = useCallback((id: string, number: number) => {
    setReportReveal((current) => current?.id === id && current.number === number ? null : current)
  }, [])

  return { id, question, setQuestion, entries, data, failure, loading, busy, progress, draft, send, select, writeReport, reportReveal, completeReportReveal }
}
