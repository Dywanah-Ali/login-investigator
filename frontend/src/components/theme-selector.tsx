import { MonitorIcon, MoonIcon, SunIcon } from 'lucide-react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useTheme } from '@/hooks/use-theme'
import { isTheme } from '@/lib/theme'

export function ThemeSelector() {
  const { theme, setTheme } = useTheme()
  const Icon = theme === 'system' ? MonitorIcon : theme === 'dark' ? MoonIcon : SunIcon

  return (
    <Select value={theme} onValueChange={(value) => { if (isTheme(value)) setTheme(value) }}>
      <SelectTrigger aria-label="Theme" title="Theme" size="sm" className="shrink-0 gap-2">
        <Icon aria-hidden="true" />
        <SelectValue />
      </SelectTrigger>
      <SelectContent position="popper" align="end">
        <SelectItem value="light">Light</SelectItem>
        <SelectItem value="dark">Dark</SelectItem>
        <SelectItem value="system">System</SelectItem>
      </SelectContent>
    </Select>
  )
}
