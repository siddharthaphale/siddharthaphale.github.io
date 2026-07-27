import { Link, NavLink, useLocation } from 'react-router-dom'
import ThemeToggle from './ThemeToggle.jsx'

export default function Header() {
  const { pathname } = useLocation()
  const isHome = pathname === '/'

  return (
    <header className={`top-bar${isHome ? ' top-bar-home' : ''}`}>
      {/* The brand stays in the DOM on the home page and is only made invisible:
          removing it collapsed the bar, so the rule and the nav shifted
          vertically when moving between home and the other pages. */}
      <div className="name-block" aria-hidden={isHome || undefined}>
        <Link to="/" className="brand-link" tabIndex={isHome ? -1 : undefined}>
          <p className="brand">Siddharth Aphale</p>
        </Link>
      </div>
      <nav className="nav-links">
        <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' nav-link-active' : ''}`}>
          home
        </NavLink>
        <NavLink to="/blog" className={({ isActive }) => `nav-link${isActive ? ' nav-link-active' : ''}`}>
          blog
        </NavLink>
        <ThemeToggle />
      </nav>
    </header>
  )
}
