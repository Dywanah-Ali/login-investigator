import { NavLink, useLocation } from 'react-router'

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import { useFilters } from '@/hooks/use-filters'
import { SCREEN_ONLY_FILTERS } from '@/lib/filters'
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
              const target = new URLSearchParams(query)
              for (const [key, only] of Object.entries(SCREEN_ONLY_FILTERS)) {
                if (screen.path !== only) target.delete(key)
              }
              const search = screen.filtered && target.size ? `?${target}` : ''
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
