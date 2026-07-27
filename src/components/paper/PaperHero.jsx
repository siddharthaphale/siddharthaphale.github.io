const ICON_BASE = '/assets/images/icons'
function iconForLabel(label = '') {
  const k = label.trim().toLowerCase()
  if (k === 'code' || k === 'github') return `${ICON_BASE}/github.svg`
  if (k === 'arxiv' || k === 'paper') return `${ICON_BASE}/arxiv-red.svg`
  if (k === 'poster' || k === 'pdf' || k === 'slides') return `${ICON_BASE}/pdf-red.svg`
  return null
}

export default function PaperHero({
  title,
  kicker,
  authors,
  affiliation,
  affiliations,
  equalLabel,
  venue,
  links,
}) {
  const hasNumberedAffiliations = Array.isArray(affiliations) && affiliations.length >= 1

  return (
    <header className="paper-hero">
      {kicker ? <div className="paper-kicker">{kicker}</div> : null}
      <h1 className="paper-title">{title}</h1>

      {authors?.length ? (
        <p className="paper-authors-line">
          {authors.map((a, i) => {
            const affIdx = hasNumberedAffiliations
              ? affiliations.findIndex((aff) => aff.name === a.aff)
              : -1
            const supNum = affIdx >= 0 ? affIdx + 1 : null
            return (
              <span key={`${a.name}-${i}`} className={a.me ? 'author-me' : undefined}>
                {a.url ? (
                  <a href={a.url} target="_blank" rel="noreferrer">
                    {a.name}
                  </a>
                ) : (
                  a.name
                )}
                {supNum ? <sup>{supNum}</sup> : null}
                {a.equal ? <sup>*</sup> : null}
              </span>
            )
          })}
        </p>
      ) : null}

      {hasNumberedAffiliations ? (
        <p className="paper-affiliations">
          {affiliations.map((aff, i) => (
            <span key={aff.name}>
              <sup>{i + 1}</sup>
              {aff.name}
              {i < affiliations.length - 1 ? ', ' : ''}
            </span>
          ))}
          {equalLabel ? <span> &nbsp;<sup>*</sup>{equalLabel}</span> : null}
        </p>
      ) : affiliation ? (
        <p className="paper-affiliations">
          {affiliation}
          {equalLabel ? <span> &nbsp;<sup>*</sup>{equalLabel}</span> : null}
        </p>
      ) : null}

      {venue ? <p className="paper-venue-line">{venue}</p> : null}

      {links?.length ? (
        <div className="paper-actions">
          {links.map((l) => {
            const iconSrc = l.icon || iconForLabel(l.label)
            return (
              <a key={l.href} className="paper-link" href={l.href} target="_blank" rel="noreferrer">
                {iconSrc ? <img className="paper-link-ico" src={iconSrc} alt="" aria-hidden="true" /> : null}
                {l.label}
              </a>
            )
          })}
        </div>
      ) : null}
    </header>
  )
}
