import { Link } from 'react-router-dom'
import Header from '../components/Header.jsx'

export default function NotFound() {
  return (
    <div className="app-shell">
      <Header />
      <main className="not-found">
        <p className="not-found-text">Page not found.</p>
        <Link to="/" className="not-found-home">
          back home
        </Link>
      </main>
    </div>
  )
}
