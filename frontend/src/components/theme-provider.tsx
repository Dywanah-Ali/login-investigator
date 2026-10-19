import { useEffect, useState, type ReactNode } from 'react'
import { ThemeContext } from '@/hooks/use-theme'
import { readTheme, THEME_STORAGE_KEY, type Theme } from '@/lib/theme'

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setPreference] = useState<Theme>(readTheme)

  useEffect(() => {
    const system = window.matchMedia('(prefers-color-scheme: dark)')
    const apply = () => document.documentElement.classList.toggle('dark', theme === 'dark' || (theme === 'system' && system.matches))
    apply()
    system.addEventListener('change', apply)
    return () => system.removeEventListener('change', apply)
  }, [theme])

  useEffect(() => {
    const sync = (event: StorageEvent) => {
      if (event.key === THEME_STORAGE_KEY || event.key === null) setPreference(readTheme())
    }
    window.addEventListener('storage', sync)
    return () => window.removeEventListener('storage', sync)
  }, [])

  function setTheme(next: Theme) {
    setPreference(next)
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, next)
    } catch {
      // The choice still works for this session when browser storage is unavailable.
    }
  }

  return <ThemeContext value={{ theme, setTheme }}>{children}</ThemeContext>
}
