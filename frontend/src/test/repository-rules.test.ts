import { readdirSync, readFileSync, statSync } from 'node:fs'
import path from 'node:path'
import { expect, test } from 'vitest'

const FRONTEND = path.resolve(import.meta.dirname, '../..')

// Built from two halves so this file does not match its own search.
const RAW_HTML = 'dangerously' + 'SetInnerHTML'

function sourceFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = path.join(dir, name)
    if (statSync(full).isDirectory()) return sourceFiles(full)
    return /\.(tsx?|jsx?|html)$/.test(name) ? [full] : []
  })
}

test('no file in the frontend renders raw HTML', () => {
  const files = [...sourceFiles(path.join(FRONTEND, 'src')), path.join(FRONTEND, 'index.html')]
  const offenders = files
    .filter((file) => readFileSync(file, 'utf8').includes(RAW_HTML))
    .map((file) => path.relative(FRONTEND, file))

  expect(offenders).toEqual([])
})
