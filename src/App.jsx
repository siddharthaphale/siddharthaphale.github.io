import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Blog from './pages/Blog.jsx'
import PaperPostPage from './pages/PaperPostPage.jsx'
import NotFound from './pages/NotFound.jsx'
import './App.css'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/blog" element={<Blog />} />
      <Route path="/blog/:year/:slug" element={<PaperPostPage />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
