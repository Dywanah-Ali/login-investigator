import Markdown from 'react-markdown'

/** The only markdown boundary. Everything else, including report fields, stays plain text. */
export function Answer({ text }: { text: string }) {
  return (
    <div className="space-y-3 break-words [&_h1]:text-xl [&_h2]:text-lg [&_h3]:font-semibold [&_ul]:list-disc [&_ol]:list-decimal [&_li]:ml-6 [&_pre]:overflow-x-auto [&_pre]:rounded-md [&_pre]:bg-muted [&_pre]:p-3 [&_code]:text-sm">
      <Markdown
        skipHtml
        allowedElements={['p', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code', 'pre', 'a']}
        // URLs are only text in the custom component, including disallowed URL schemes.
        urlTransform={(url) => url}
        components={{ a: ({ children, href }) => <>{children} ({href})</> }}
      >{text}</Markdown>
    </div>
  )
}
