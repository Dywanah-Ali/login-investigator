import { BellIcon, BotIcon, LayoutDashboardIcon, TableIcon } from 'lucide-react'
import { NavLink, useLocation } from 'react-router'

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import { useFilters } from '@/hooks/use-filters'
import { SCREENS } from '@/screens'

const ICONS = {
  '/': LayoutDashboardIcon,
  '/alerts': BellIcon,
  '/explorer': TableIcon,
  '/investigator': BotIcon,
} as const

export function NavMain() {
  const { pathname } = useLocation()
  const { query } = useFilters()

  return (
    <nav aria-label="Screens">
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu>
            {SCREENS.map((screen) => {
              const Icon = ICONS[screen.path]
              // The filters follow the analyst between the dashboard screens, as in v1.
              const search = screen.filtered && query ? `?${query}` : ''
              return (
                <SidebarMenuItem key={screen.path}>
                  <SidebarMenuButton
                    asChild
                    tooltip={screen.title}
                    isActive={pathname === screen.path}
                  >
                    <NavLink to={{ pathname: screen.path, search }} end>
                      <Icon />
                      <span>{screen.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )
            })}
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </nav>
  )
}
