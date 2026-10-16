import { useEffect, useRef, useState } from 'react'

import { Answer } from '@/components/answer'
import { IncidentReport } from '@/components/incident-report'
import { QuietCard } from '@/components/quiet-card'
import { ToolsUsed } from '@/components/tools-used'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Message, MessageContent, MessageGroup, MessageHeader } from '@/components/ui/message'
import { useInvestigation } from '@/hooks/use-investigation'
import { formatTimestamp } from '@/lib/format'

const STARTERS = [
  'Anything suspicious last night?',
  'Was any account compromised this week?',
  'Which IP addresses attacked us, and how bad are they?',
]

function QuestionAnswer({ question, answer }: { question: string; answer: string }) {
  return (
    <MessageGroup>
      <Message align="end">
        <MessageContent>
          <MessageHeader>You</MessageHeader>
          <p className="rounded-lg bg-muted p-3 whitespace-pre-wrap">{question}</p>
        </MessageContent>
      </Message>
      {answer && <Message>
        <MessageContent>
          <MessageHeader>Investigator</MessageHeader>
          <Answer text={answer} />
        </MessageContent>
      </Message>}
    </MessageGroup>
  )
}

export function InvestigatorPage() {
  const {
    id, question, setQuestion, entries, data, failure, loading, busy,
    progress, draft, send, select, writeReport,
  } = useInvestigation()
  const [limit, setLimit] = useState(3)
  const bottom = useRef<HTMLDivElement>(null)
  useEffect(() => {
    bottom.current?.scrollIntoView?.({ block: 'nearest' })
  }, [draft?.answer, data?.turns.length])

  const shown = entries.filter((entry, index) => index < limit || entry.id === id)
  return (
    <>
      <p className="text-sm text-muted-foreground">
        Investigations use the whole log. Dashboard filters do not apply.
      </p>
      {failure && <p role="alert">{failure}</p>}
      <div className="grid min-w-0 gap-6 xl:grid-cols-[minmax(0,1fr)_18rem]">
        <Card className="min-w-0">
          <CardContent className="space-y-6">
            <h2 className="text-lg font-semibold">{data?.first_question || 'New investigation'}</h2>
            {!loading && !busy && !data?.turns.length && <div className="space-y-4">
              <p>
                I search the sign-in log, run the detection rules and look up IP reputation,
                and I can write an incident report. I only read: I cannot block, change or delete anything.
              </p>
              <div className="flex flex-wrap gap-2">
                {STARTERS.map((starter) => (
                  <Button key={starter} variant="outline" onClick={() => setQuestion(starter)}>
                    {starter}
                  </Button>
                ))}
              </div>
            </div>}
            {loading && !busy && <p role="status">Loading investigation…</p>}
            <div role="region" aria-label="Investigation messages" className="max-h-[60vh] space-y-6 overflow-y-auto pr-2">
              {data?.turns.map((turn, index) => (
                <div key={index} className="space-y-4">
                  <QuestionAnswer question={turn.question} answer={turn.answer} />
                  <ToolsUsed tools={turn.tools} />
                  {turn.report && id && <IncidentReport id={id} report={turn.report} />}
                </div>
              ))}
              {draft && <QuestionAnswer question={draft.question} answer={draft.answer} />}
              <div ref={bottom} />
            </div>
            {busy && <p role="status" className="text-sm text-muted-foreground">{progress}</p>}
            {data?.report_offer && (
              <Button disabled={busy || loading} onClick={() => void writeReport()}>
                {data.report_offer}
              </Button>
            )}
            <form onSubmit={(event) => { event.preventDefault(); void send() }} className="space-y-3">
              <label htmlFor="question" className="text-sm font-medium">Question</label>
              <textarea
                id="question"
                disabled={busy || loading}
                className="min-h-24 w-full rounded-md border bg-background p-3"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                maxLength={2000}
              />
              <Button type="submit" disabled={busy || loading || !question.trim()}>Send question</Button>
              <p className="text-xs text-muted-foreground">
                Answers are AI-generated and can be wrong. Check them against the tool calls under each answer.
              </p>
            </form>
          </CardContent>
        </Card>
        <QuietCard className="h-fit min-w-0 text-sm text-muted-foreground">
          <CardContent className="space-y-4">
            <Button variant="outline" disabled={busy} onClick={() => select()}>New investigation</Button>
            <nav aria-label="Past investigations" className="space-y-2">
              <h2 className="font-medium">Past investigations</h2>
              {!entries.length && <p>No past investigations yet.</p>}
              {shown.map((entry) => (
                <button
                  key={entry.id}
                  aria-current={entry.id === id ? 'true' : undefined}
                  className="block w-full rounded-md border-l-2 border-transparent p-2 text-left hover:bg-muted aria-[current=true]:border-primary aria-[current=true]:bg-muted"
                  disabled={busy}
                  onClick={() => select(entry.id)}
                >
                  <span className="block break-words">{entry.first_question}</span>
                  <span className="text-xs">{formatTimestamp(entry.started_at)}</span>
                </button>
              ))}
              {entries.length > limit && (
                <Button variant="ghost" size="sm" onClick={() => setLimit(limit + 3)}>Show three more</Button>
              )}
            </nav>
          </CardContent>
        </QuietCard>
      </div>
    </>
  )
}
