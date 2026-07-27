import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import mdx from '@mdx-js/rollup'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { visit } from 'unist-util-visit'

// Give every heading an `id` slug (like rehype-slug, but dependency-free) so the
// in-post Table of Contents anchor links resolve and scroll to their section.
function rehypeSlugHeadings() {
  const slugify = (s) =>
    s
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
  const getText = (node) =>
    node.type === 'text' ? node.value : (node.children || []).map(getText).join('')
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (/^h[1-6]$/.test(node.tagName)) {
        node.properties = node.properties || {}
        if (!node.properties.id) node.properties.id = slugify(getText(node))
      }
    })
  }
}

// remark-math creates `math` (block) and `inlineMath` MDAST nodes but doesn't
// set the hast data that remark-rehype needs to produce the class names
// rehype-katex v7 looks for (`math-display` / `math-inline`). Without these,
// rehype-katex renders everything in inline mode — no katex-display wrapper.
function remarkMathHast() {
  return (tree) => {
    visit(tree, 'math', (node) => {
      node.data = node.data || {}
      node.data.hName = 'div'
      node.data.hProperties = { className: ['math', 'math-display'] }
      node.data.hChildren = [{ type: 'text', value: node.value }]
    })
    visit(tree, 'inlineMath', (node) => {
      node.data = node.data || {}
      node.data.hName = 'span'
      node.data.hProperties = { className: ['math', 'math-inline'] }
      node.data.hChildren = [{ type: 'text', value: node.value }]
    })
  }
}

export default defineConfig({
  base: '/',
  plugins: [
    {
      enforce: 'pre',
      ...mdx({
        providerImportSource: '@mdx-js/react',
        remarkPlugins: [remarkGfm, remarkMath, remarkMathHast],
        rehypePlugins: [rehypeSlugHeadings, rehypeKatex],
      }),
    },
    react({ include: /\.(jsx|js|mdx|md|tsx|ts)$/ }),
  ],
})
