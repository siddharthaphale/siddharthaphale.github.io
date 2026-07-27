import { Link } from 'react-router-dom'

// Internal blog routes navigate in the same tab via React Router (no reload).
// External links and PDFs open in a new tab; other internal static pages
// (e.g. /projects/*, which are not SPA routes) use a normal same-tab anchor.
function CardLink({ href, className, children }) {
  const newTab = /^https?:\/\//.test(href) || href.endsWith('.pdf')
  if (newTab) {
    return (
      <a href={href} className={className} target="_blank" rel="noreferrer">
        {children}
      </a>
    )
  }
  if (href.startsWith('/blog/')) {
    return (
      <Link to={href} className={className}>
        {children}
      </Link>
    )
  }
  return (
    <a href={href} className={className}>
      {children}
    </a>
  )
}

export default function PaperCard({ paper }) {
  return (
    <article className={`paper-card${paper.wide ? ' paper-card-wide' : ''}`}>
      <div className={`paper-thumb-wrap${paper.wide ? ' is-wide' : ''}`}>
        <img className="paper-thumb" src={paper.thumb} alt={paper.alt} loading="lazy" />
      </div>

      <div className="paper-body">
        <p className="paper-venue-top">
          {paper.venue}, {paper.year}
          {paper.note ? <> &middot; {paper.note}</> : null}
          {paper.award ? <span className="paper-award"> &middot; {paper.award}</span> : null}
        </p>

        {/* No paperUrl (e.g. nothing public to link to yet) renders a plain,
            unclickable title instead of a dead link. */}
        {paper.paperUrl ? (
          <CardLink href={paper.paperUrl} className="paper-title">
            {paper.title}
          </CardLink>
        ) : (
          <span className="paper-title">{paper.title}</span>
        )}

        <p className="paper-authors">
          {paper.authors.map((a, i) => (
            <span key={`${a.name}-${i}`}>
              {a.me ? <strong>{a.name}</strong> : a.name}
              {a.equal ? '*' : ''}
              {i < paper.authors.length - 1 ? ', ' : ''}
            </span>
          ))}
        </p>

        {paper.blurb ? <p className="paper-blurb">{paper.blurb}</p> : null}

        {paper.links?.length ? (
          <p className="paper-links">
            {paper.links.map((l, i) => (
              <span key={l.href + i}>
                <CardLink href={l.href}>{l.label}</CardLink>
                {i < paper.links.length - 1 ? ' / ' : ''}
              </span>
            ))}
          </p>
        ) : null}
      </div>
    </article>
  )
}
