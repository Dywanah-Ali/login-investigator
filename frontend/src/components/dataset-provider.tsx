import type { ReactNode } from 'react'

import { useApi } from '@/hooks/use-api'
import { DatasetContext } from '@/hooks/use-dataset'
import type { DatasetFacts } from '@/lib/api'

export function DatasetProvider({ children }: { children: ReactNode }) {
  const dataset = useApi<DatasetFacts>('/api/dataset', '')
  return <DatasetContext.Provider value={dataset}>{children}</DatasetContext.Provider>
}
