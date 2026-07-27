import { useEffect, useState } from 'react'
import { Link, useParams, useLocation } from 'react-router-dom'
import { MDXProvider } from '@mdx-js/react'
import Header from '../components/Header.jsx'
import PaperHero from '../components/paper/PaperHero.jsx'
import {
  TLDR,
  Abstract,
  TOC,
  Section,
  Takeaway,
  Grid,
  Figure,
  VideoFigure,
  BibTeX,
  Footnote,
  FootnoteProvider,
  Cite,
} from '../components/paper/PaperBlocks.jsx'
import { getPost } from '../data/posts.js'

const mdxComponents = {
  TLDR,
  Abstract,
  TOC,
  Section,
  Takeaway,
  Grid,
  Figure,
  VideoFigure,
  BibTeX,
  Footnote,
  Cite,
  PaperHero,
}

export default function PaperPostPage() {
  const { year, slug } = useParams()
  const location = useLocation()
  const post = getPost(year, slug)
  const [Mdx, setMdx] = useState(null)
  const [error, setError] = useState(null)
  // Where "back to all posts" returns to — the filtered blog view we came from,
  // captured on mount so later in-page hash navigation can't clear it.
  const [backTo] = useState(location.state?.backTo || '/blog')

  // On the initial render of a post, jump to the hash target if the page was
  // opened or refreshed directly on a section link (e.g. …#rank-inversion). The
  // browser's native jump fires before the async MDX mounts, so it misses. Keyed
  // on Mdx only (not the hash) so later in-page TOC clicks keep their smooth
  // CSS scroll instead of being overridden by this instant jump.
  useEffect(() => {
    if (!Mdx) return
    const id = decodeURIComponent(window.location.hash.slice(1))
    if (!id) return
    const raf = requestAnimationFrame(() => {
      document.getElementById(id)?.scrollIntoView({ behavior: 'instant', block: 'start' })
    })
    return () => cancelAnimationFrame(raf)
  }, [Mdx])

  // Scroll-spy: highlight the section currently in view in the sidebar TOC.
  useEffect(() => {
    if (!Mdx) return
    const scope = document.querySelector('.lilian-post')
    if (!scope) return
    const headings = Array.from(scope.querySelectorAll('.post-content :is(h1, h2, h3, h4)[id]'))
    const links = Array.from(scope.querySelectorAll('.toc a'))
    if (!headings.length || !links.length) return
    const linkByHash = new Map(links.map((a) => [a.getAttribute('href'), a]))

    let activeId = null
    const update = () => {
      const line = window.innerHeight * 0.2
      let current = headings[0]
      for (const h of headings) {
        if (h.getBoundingClientRect().top - line <= 1) current = h
        else break
      }
      if (current.id === activeId) return
      activeId = current.id
      links.forEach((a) => a.classList.remove('is-active'))
      linkByHash.get(`#${current.id}`)?.classList.add('is-active')
    }

    const observer = new IntersectionObserver(update, { rootMargin: '-20% 0px -75% 0px' })
    headings.forEach((h) => observer.observe(h))
    update()
    return () => observer.disconnect()
  }, [Mdx])

  useEffect(() => {
    if (!post) return
    let cancelled = false
    setMdx(null)
    setError(null)
    post
      .load()
      .then((mod) => {
        if (!cancelled) setMdx(() => mod.default)
      })
      .catch((e) => {
        if (!cancelled) setError(e)
      })
    return () => {
      cancelled = true
    }
  }, [post])

  if (!post) {
    return (
      <div className="app-shell">
        <Header />
        <main className="paper-page">
          <div className="paper-container">
            <p>post not found.</p>
            <Link to="/blog">back to blog</Link>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <Header />

      <main className="paper-page paper-page--sidebar">
        <p className="paper-back">
          <Link to={backTo}>← back to all posts</Link>
        </p>

        {error ? (
          <div className="paper-container">
            <p>failed to load post: {String(error.message || error)}</p>
          </div>
        ) : Mdx ? (
          <FootnoteProvider>
            <MDXProvider components={mdxComponents}>
              <Mdx components={mdxComponents} />
            </MDXProvider>
          </FootnoteProvider>
        ) : (
          <div className="paper-container">
            <p className="writing-loading">loading...</p>
          </div>
        )}
      </main>
    </div>
  )
}
