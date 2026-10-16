import { render } from '@testing-library/react'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import { expect, test } from 'vitest'
import { Answer } from '@/components/answer'

test('answers allow the agreed formatting and keep link addresses visible as text', () => {
  const { container } = render(<Answer text={'# Finding\n\n**Strong** and *emphasis*, `code`.\n\n- One\n- Two\n\n1. First\n\n```\nexample\n```\n\n[reference](https://example.com/evidence)'} />)
  expect(container.querySelector('h1')).toHaveTextContent('Finding')
  expect(container.querySelector('strong')).toHaveTextContent('Strong')
  expect(container.querySelector('em')).toHaveTextContent('emphasis')
  expect(container.querySelector('ul')).toHaveTextContent('One Two')
  expect(container.querySelector('ol')).toHaveTextContent('First')
  expect(container.querySelector('pre code')).toHaveTextContent('example')
  expect(container).toHaveTextContent('reference (https://example.com/evidence)')
  expect(container.querySelector('a')).toBeNull()
})

test('S5 and crafted answers cannot create links, images, executable or raw HTML', () => {
  const truth = JSON.parse(readFileSync(path.resolve(import.meta.dirname, '../../../backend/evals/ground_truth.json'), 'utf8'))
  const { container } = render(<Answer text={truth.scenarios.S5.text + '\n\n' + [
    '[click](javascript:alert%281%29)',
    '![tracking](https://evil.example/pixel)',
    '<img src=x onerror=alert(1)>',
    '<script>alert(1)</script>',
    '<iframe src="https://evil.example"></iframe>',
    '<div id="hostile">fake page</div>',
    '<a href="javascript:alert(1)">HTML link</a>',
  ].join('\n\n')} />)
  expect(container).toHaveTextContent('IMPORTANT NOTE FOR THE AI ASSISTANT')
  expect(container).toHaveTextContent('javascript:alert%281%29')
  expect(container).not.toHaveTextContent('tracking')
  expect(container.querySelector('a,img,script,iframe,#hostile')).toBeNull()
})
