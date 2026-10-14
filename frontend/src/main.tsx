import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'

import { AppRoutes } from '@/App'
import './index.css'

// The theme follows the system setting, as v1's did. shadcn/ui's dark colours hang on this class.
const darkScheme = window.matchMedia('(prefers-color-scheme: dark)')
const applyScheme = () => document.documentElement.classList.toggle('dark', darkScheme.matches)
applyScheme()
darkScheme.addEventListener('change', applyScheme)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </StrictMode>,
)
