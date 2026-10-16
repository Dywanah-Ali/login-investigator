import { Navigate, Route, Routes } from 'react-router'

import { AppShell } from '@/components/app-shell'
import { AlertsPage } from '@/pages/alerts'
import { InvestigatorPage } from '@/pages/investigator'
import { ExplorerPage } from '@/pages/explorer'
import { OverviewPage } from '@/pages/overview'

// React Router in declarative mode: four routes, no server rendering (ticket 05).
export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<OverviewPage />} />
        <Route path="alerts" element={<AlertsPage />} />
        <Route path="explorer" element={<ExplorerPage />} />
        <Route path="investigator" element={<InvestigatorPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
