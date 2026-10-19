export type Theme = 'light' | 'dark' | 'system'
export const THEME_STORAGE_KEY = 'login-investigator-theme'

export function isTheme(value: unknown): value is Theme {
  return value === 'light' || value === 'dark' || value === 'system'
}

export function readTheme(): Theme {
  try {
    const saved = window.localStorage.getItem(THEME_STORAGE_KEY)
    return isTheme(saved) ? saved : 'system'
  } catch {
    return 'system'
  }
}
