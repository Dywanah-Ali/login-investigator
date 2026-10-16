import { useLayoutEffect, useRef, useState } from 'react'
import { Plus } from 'lucide-react'
import { useMessageScroller } from '@shadcn/react/message-scroller'

import { Answer } from '@/components/answer'
import { IncidentReport } from '@/components/incident-report'
import { QuietCard } from '@/components/quiet-card'
import { ToolsUsed } from '@/components/tools-used'
import { Bubble, BubbleContent } from '@/components/ui/bubble'
import { Button } from '@/components/ui/button'
import { CardContent } from '@/components/ui/card'
import { Message, MessageContent, MessageGroup } from '@/components/ui/message'
import {
  MessageScroller, MessageScrollerButton, MessageScrollerContent,
  MessageScrollerItem, MessageScrollerProvider, MessageScrollerViewport,
} from '@/components/ui/message-scroller'
import { useInvestigation } from '@/hooks/use-investigation'
import { formatTimestamp } from '@/lib/format'

const STARTERS = [
  'Anything suspicious last night?',
  'Was any account compromised this week?',
  'Which IP addresses attacked us, and how bad are they?',
]

/** A newly saved report explicitly returns the reader to the end, even after scrolling up. */
function RevealNewReport({ count }: { count: number }) {
  const previous = useRef(count)
  const { scrollToEnd } = useMessageScroller()
  useLayoutEffect(() => {
    if (count > previous.current) scrollToEnd({ behavior: 'auto' })
    previous.current = count
  }, [count, scrollToEnd])
  return null
}

function QuestionAnswer({ question, answer }: { question: string; answer: string }) {
  return (
    <MessageGroup className="gap-3">
      <Message align="end" aria-label="Your question">
        <MessageContent>
          <Bubble variant="tinted" align="end" className="max-w-[95%] sm:max-w-[80%]">
            <BubbleContent className="border-primary/10 whitespace-pre-wrap">{question}</BubbleContent>
          </Bubble>
        </MessageContent>
      </Message>
      {answer && <Message aria-label="Investigator answer">
        <MessageContent>
          <Bubble variant="muted" className="max-w-[95%] sm:max-w-[85%]">
            <BubbleContent className="border-border/60"><Answer text={answer} /></BubbleContent>
          </Bubble>
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
  const shown = entries.filter((entry, index) => index < limit || entry.id === id)
  const empty = !loading && !busy && !data?.turns.length

  return (
    <>
      <p className="text-xs text-muted-foreground">
        Investigations use the whole log. Dashboard filters do not apply.
      </p>
      {failure && <p role="alert">{failure}</p>}
      <div className="grid min-h-0 min-w-0 gap-4 lg:grid-cols-[15rem_minmax(0,1fr)]">
        <QuietCard className="h-fit min-w-0 gap-0 rounded-lg py-3 text-sm text-muted-foreground">
          <CardContent className="space-y-3 px-3">
            <Button className="w-full justify-start" disabled={busy} onClick={() => select()}>
              <Plus aria-hidden="true" />New investigation
            </Button>
            <nav aria-label="Past investigations" className="space-y-2">
              <h2 className="sr-only">Past investigations</h2>
              {!entries.length && <p className="px-2 py-3 text-xs">No past investigations yet.</p>}
              {shown.map((entry) => (
                <button
                  key={entry.id}
                  aria-current={entry.id === id ? 'true' : undefined}
                  className="block w-full rounded-md border border-border/60 p-2.5 text-left transition-colors hover:bg-muted aria-[current=true]:border-primary/60 aria-[current=true]:bg-primary/10 aria-[current=true]:text-foreground disabled:opacity-50"
                  disabled={busy}
                  onClick={() => select(entry.id)}
                >
                  <span className="block text-xs leading-relaxed break-words">{entry.first_question}</span>
                  <span className="mt-1 block text-[0.6875rem] text-muted-foreground">{formatTimestamp(entry.started_at)}</span>
                </button>
              ))}
              {entries.length > limit && (
                <Button className="w-full" variant="ghost" size="sm" onClick={() => setLimit(limit + 3)}>
                  Show three more
                </Button>
              )}
            </nav>
          </CardContent>
        </QuietCard>

        <section aria-label="Investigation" className="flex min-h-0 min-w-0 flex-col gap-3 lg:max-w-[54rem]">
          <h2 className="sr-only">{data?.first_question || 'New investigation'}</h2>
          {loading && !busy && <p role="status">Loading investigation…</p>}
          <MessageScrollerProvider key={id ?? 'new'} autoScroll>
            <MessageScroller className={empty ? 'h-auto' : 'h-[55vh] min-h-48'}>
              <MessageScrollerViewport role="region" aria-label="Investigation messages" className="pr-2">
                <MessageScrollerContent className="gap-5 pb-3">
                  {data?.turns.map((turn, index) => (
                    <MessageScrollerItem key={`${id}-${index}`} messageId={`${id}-${index}`} className="space-y-3">
                      <QuestionAnswer question={turn.question} answer={turn.answer} />
                      <div className="sm:max-w-[85%]"><ToolsUsed tools={turn.tools} /></div>
                      {turn.report && id && <div className="sm:max-w-[85%]">
                        <IncidentReport id={id} report={turn.report} />
                      </div>}
                    </MessageScrollerItem>
                  ))}
                  {draft && <MessageScrollerItem messageId="draft" scrollAnchor>
                    <QuestionAnswer question={draft.question} answer={draft.answer} />
                  </MessageScrollerItem>}
                </MessageScrollerContent>
              </MessageScrollerViewport>
              <RevealNewReport count={data?.turns.filter((turn) => turn.report !== null).length ?? 0} />
              <MessageScrollerButton />
            </MessageScroller>
          </MessageScrollerProvider>
          {empty && <div className="space-y-3 py-3">
            <p className="text-sm text-muted-foreground">
              I search the sign-in log, run the detection rules and look up IP reputation,
              and I can write an incident report. I only read: I cannot block, change or delete anything.
            </p>
            <div className="flex flex-wrap gap-2">
              {STARTERS.map((starter) => (
                <Button key={starter} variant="outline" size="sm" onClick={() => setQuestion(starter)}>
                  {starter}
                </Button>
              ))}
            </div>
          </div>}
          {busy && <p role="status" className="text-xs text-muted-foreground">{progress}</p>}
          {data?.report_offer && (
            <div><Button variant="outline" size="sm" disabled={busy || loading} onClick={() => void writeReport()}>
              {data.report_offer}
            </Button></div>
          )}
          <form onSubmit={(event) => { event.preventDefault(); void send() }} className="flex items-end gap-2 rounded-lg border bg-background p-2">
            <label htmlFor="question" className="sr-only">Question</label>
            <textarea
              id="question"
              rows={1}
              disabled={busy || loading}
              placeholder="Ask about the sign-in log…"
              className="field-sizing-content max-h-40 min-h-9 min-w-0 flex-1 resize-none rounded-md px-2 py-2 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              maxLength={2000}
            />
            <Button type="submit" size="sm" aria-label="Send question" disabled={busy || loading || !question.trim()}>Send</Button>
          </form>
          <p className="text-xs leading-relaxed text-muted-foreground">
            Answers are AI-generated and can be wrong. Check them against the tool calls under each answer.
          </p>
        </section>
      </div>
    </>
  )
}
