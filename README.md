# siddharthaphale.github.io

Personal academic site. React + Vite SPA with an MDX-powered blog.

## Stack

- React 18 + Vite 5
- React Router (clean URLs)
- MDX for blog posts (`@mdx-js/rollup`) with `remark-gfm`, `remark-math`, `rehype-katex`
- KaTeX for math rendering

## Local development

Requires Node 22 (matches the version CI builds with).

```bash
npm install
npm run dev        # local dev server with HMR (http://localhost:5173)
npm run build      # production build into dist/
npm run preview    # serve the built site locally
```

## Project layout

```
.
├── .github/workflows/deploy.yml   # GitHub Pages deploy on push to main
├── public/                        # static assets, served at /
│   ├── assets/                    # social icons, headshot, link-preview card
│   ├── projects/                  # per-paper figures + posters (no HTML pages left)
│   └── .nojekyll
├── src/
│   ├── main.jsx                   # entry
│   ├── App.jsx                    # routes
│   ├── index.css / App.css        # global styles (cardinal / warm-paper palette)
│   ├── components/                # Header, ThemeToggle, PaperCard, PostCard, TypingText
│   │   └── paper/                 # PaperHero, PaperBlocks (MDX building blocks)
│   ├── pages/                     # Home, Blog, PaperPostPage, NotFound
│   ├── data/                      # papers.js, posts.js, projects.js
│   └── posts/                     # MDX blog posts
├── index.html                     # Vite entry HTML
├── vite.config.js
└── package.json
```

## Adding a paper

Add an entry to `src/data/papers.js` with `thumb`, `title`, `authors`, `venue`, `year`, `links`,
and `blurb`. Author entries use `me: true` to bold your name and `equal: true` for shared
first-author asterisks. `paperUrl` may point to an internal `/projects/...` page or an external URL.

## Adding a blog post

1. Create `src/posts/<slug>.mdx`.
2. Register it in `src/data/posts.js` with a `load: () => import('../posts/<slug>.mdx')` entry.
   Every post renders through `PaperPostPage`; keep an entry in the `DRAFTS` array to hold it
   back from the live site while you write.

## Deploy

Pushing to `main` triggers `.github/workflows/deploy.yml`, which runs `npm ci && npm run build`,
copies `dist/index.html` to `dist/404.html` for SPA deep-link fallback, and deploys via
`actions/deploy-pages`. One-time setup: in repo Settings → Pages, set the source to
**GitHub Actions**.

## Licensing

Two licenses, because the code and the writing want different terms.

| | Covers | License |
|:---|:---|:---|
| Code | `src/` (except posts and data blurbs), `scripts/`, config | [MIT](LICENSE) |
| Content | `src/posts/`, `public/blog/assets/`, `public/projects/`, site imagery | [CC BY-NC 4.0](LICENSE-CONTENT) |

Reuse the code freely. The posts and figures may be shared and adapted with
attribution, but not commercially. Where a figure reproduces a result from a
paper published elsewhere, that publication's terms also apply.

## Credits

Site structure and layout adapted from [jaydenteoh/jaydenteoh.github.io](https://github.com/jaydenteoh/jaydenteoh.github.io)
(whose design is in turn inspired by [stephenkyang.github.io](https://github.com/stephenkyang/stephenkyang.github.io)).
Visual identity (typography, cardinal palette, icon buttons) is original.

Note: the upstream repository carries no license, so no redistribution rights
were granted by it. The adaptation here is limited to layout conventions, and
the MIT grant above covers only this repository's own code.
