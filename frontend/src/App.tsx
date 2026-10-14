import { Navigate, Route, Routes } from 'react-router'

import { AppShell } from '@/components/app-shell'
import { ComingLater } from '@/pages/coming-later'
import { OverviewPage } from '@/pages/overview'

// React Router in declarative mode: four routes, no server rendering (ticket 05).
export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<OverviewPage />} />
        <Route path="alerts" element={<ComingLater />} />
        <Route path="explorer" element={<ComingLater />} />
        <Route path="investigator" element={<ComingLater />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
