import type { CSSProperties } from 'react'
import { Outlet, useLocation } from 'react-router'

import { AppSidebar } from '@/components/app-sidebar'
import { DatasetProvider } from '@/components/dataset-provider'
import { SiteHeader } from '@/components/site-header'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import { TooltipProvider } from '@/components/ui/tooltip'
import { screenFor } from '@/screens'

// dashboard-01's page layout: sidebar, header, and the screen below.
export function AppShell() {
  const { pathname } = useLocation()

  return (
    <DatasetProvider>
      <TooltipProvider>
        <SidebarProvider
          style={
            {
              '--sidebar-width': 'calc(var(--spacing) * 64)',
              '--header-height': 'calc(var(--spacing) * 12)',
            } as CSSProperties
          }
        >
          <AppSidebar variant="inset" />
          <SidebarInset>
            <SiteHeader title={screenFor(pathname).title} />
            <div className="@container/main flex flex-1 flex-col gap-4 p-4 md:gap-6 md:p-6">
              <Outlet />
            </div>
          </SidebarInset>
        </SidebarProvider>
      </TooltipProvider>
    </DatasetProvider>
  )
}
