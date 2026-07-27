import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import Header from '../components/Header.jsx'
import PostCard from '../components/PostCard.jsx'
import { posts, getAllTags } from '../data/posts.js'

export default function Blog() {
  // Keep the active tab in the URL (?tag=research) so it is shareable and
  // survives navigating into a post and back.
  const [searchParams, setSearchParams] = useSearchParams()
  const tags = useMemo(() => getAllTags(), [])
  const requested = searchParams.get('tag') || 'all'
  const filter = tags.includes(requested) ? requested : 'all'
  const setFilter = (t) => setSearchParams(t === 'all' ? {} : { tag: t }, { replace: true })

  const sorted = [...posts].sort((a, b) => (a.date < b.date ? 1 : -1))
  const filtered = filter === 'all' ? sorted : sorted.filter((p) => p.tags.includes(filter))

  return (
    <div className="app-shell">
      <Header />

      <main className="writings-page">
        <div className="writings-header">
          <h1 className="page-title">blog</h1>
          <p className="page-subtitle">Notes on machine learning, research, and my publications.</p>
        </div>

        <div className="writing-tags">
          {tags.map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setFilter(t)}
              className={`writing-tag${filter === t ? ' writing-tag-active' : ''}`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="post-list">
          {filtered.length === 0 ? (
            <p className="writing-empty">
              {filter === 'all' ? 'No posts yet, check back soon.' : 'No posts under this tag yet.'}
            </p>
          ) : (
            filtered.map((p) => <PostCard key={p.slug} post={p} />)
          )}
        </div>
      </main>
    </div>
  )
}
