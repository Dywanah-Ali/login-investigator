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

export function NavMain() {
  const { pathname } = useLocation()
  const { query } = useFilters()

  return (
    <nav aria-label="Screens">
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu>
            {SCREENS.map((screen) => {
              const Icon = screen.icon
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
