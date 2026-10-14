import { CircleAlertIcon } from 'lucide-react'

import { FAILURE_TEXT, type FailureKind } from '@/lib/api'

/** A failed request, told in fixed text. Nothing from the server or the exception is shown. */
export function FailureMessage({ kind }: { kind: FailureKind }) {
  return (
    <div
      role="alert"
      className="flex items-center gap-2 rounded-lg border border-destructive/40 px-4 py-3 text-sm text-destructive"
    >
      <CircleAlertIcon className="size-4 shrink-0" aria-hidden />
      <p>{FAILURE_TEXT[kind]}</p>
    </div>
  )
}
