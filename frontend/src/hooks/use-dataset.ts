import { createContext, useContext } from 'react'

import type { Loaded } from '@/hooks/use-api'
import type { DatasetFacts } from '@/lib/api'

// The dataset facts are loaded once for the whole app (see DatasetProvider): the header and the
// filter toolbar read them.
export const DatasetContext = createContext<Loaded<DatasetFacts>>({ state: 'loading' })

export function useDataset() {
  return useContext(DatasetContext)
}
