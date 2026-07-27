import { Link, useLocation } from 'react-router-dom'
import { postUrl } from '../data/posts.js'

export default function PostCard({ post }) {
  const href = postUrl(post)
  // Remember which filtered blog view this card was opened from, so the post's
  // "back to all posts" link can return to it (with the tab still selected).
  const { pathname, search } = useLocation()
  const backState = { backTo: `${pathname}${search}` }
  return (
    <article className="post-card">
      {post.cover ? (
        <Link to={href} state={backState} className="post-cover" aria-hidden="true">
          <img src={post.cover} alt="" loading="lazy" />
        </Link>
      ) : null}

      <div className="post-info">
        <h3 className="post-title">
          <Link to={href} state={backState}>{post.title}</Link>
        </h3>
        <p className="post-date">{post.date}</p>
        {post.excerpt ? <p className="post-excerpt">{post.excerpt}</p> : null}
        {post.tags?.length ? (
          <p className="post-tags">
            {/* The blog index filters from ?tag=, so a tag on a card can do the
                same thing the tabs above it do instead of being dead ink. */}
            {post.tags.map((t) => (
              <Link key={t} to={`/blog?tag=${encodeURIComponent(t)}`} className="post-tag">
                {t}
              </Link>
            ))}
          </p>
        ) : null}
      </div>
    </article>
  )
}
