import type { ComponentProps } from 'react'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

/** Supporting information shares one quiet surface beneath the main table's contrast. */
export function QuietCard({ className, ...props }: ComponentProps<typeof Card>) {
  return <Card className={cn('bg-muted/40 shadow-none ring-foreground/5', className)} {...props} />
}
