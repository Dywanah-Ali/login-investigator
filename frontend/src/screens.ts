import { BellIcon, BotIcon, LayoutDashboardIcon, TableIcon } from 'lucide-react'

// The four screens, in sidebar order. The three dashboard screens share the filters; the
// Investigator is not filtered.
export const SCREENS = [
  { path: '/', title: 'Overview', icon: LayoutDashboardIcon, filtered: true },
  { path: '/alerts', title: 'Alerts', icon: BellIcon, filtered: true },
  { path: '/explorer', title: 'Log explorer', icon: TableIcon, filtered: true },
  { path: '/investigator', title: 'Investigator', icon: BotIcon, filtered: false },
] as const

export type Screen = (typeof SCREENS)[number]

export function screenFor(pathname: string): Screen {
  return SCREENS.find((screen) => screen.path === pathname) ?? SCREENS[0]
}
