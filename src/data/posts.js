// Blog posts. Add an entry here and a matching MDX file under src/posts/.
//
// {
//   slug: 'my-post',
//   title: 'My Post',
//   date: '2026-06-16',
//   tags: ['machine learning', 'research'],
//   excerpt: 'One-line summary.',
//   cover: '/blog/assets/<slug>/cover.png',   // optional
//   load: () => import('../posts/<slug>.mdx'),
// }
//
// To keep a post unpublished, put its entry in the DRAFTS array below instead
// of here: drafts are visible in `npm run dev` but never built into the live
// site. Move it up here when it's ready to release.
const ALL_POSTS = [
  {
    slug: 'scout-per-context-scaffolds',
    title: 'The best curriculum for your easy tasks is the worst for your hard ones',
    date: '2026-07-01',
    tags: ['research'],
    excerpt:
      'Easier starts get sparse-reward RL off the ground, but one global schedule for removing them abandons the contexts that learn slowest. SCOUT paces each one separately.',
    load: () => import('../posts/scout-per-context-scaffolds.mdx'),
  },
  {
    slug: 'sft-checkpoint-rl-collapse',
    title: 'Why your best SFT checkpoint can be the worst for RL',
    date: '2026-06-16',
    tags: ['my publications'],
    excerpt:
      "SFT overtraining collapses output entropy and silently kills GRPO's gradient. A free pre-RL entropy check predicts the failure before you spend any compute.",
    load: () => import('../posts/sft-checkpoint-rl-collapse.mdx'),
  },
  {
    slug: 'offline-to-online-rl',
    title: 'Offline to online RL: distribution shift, conservatism, and collapse',
    date: '2026-05-30',
    tags: ['machine learning'],
    excerpt:
      'Offline-to-online RL is a non-stationary handoff, not two phases in sequence: conservatism is necessary and temporary, and the first online updates can wreck a policy.',
    load: () => import('../posts/offline-to-online-rl.mdx'),
  },
]

// Drafts. Only bundled during local dev (`npm run dev`), where they show up in
// the list and are reachable by URL so you can keep editing. The whole array is
// dead-code-eliminated from the production build, so neither the metadata nor
// the post's content chunk is ever shipped or reachable on the live site.
// Add an unreleased post's entry here (with its MDX under src/posts/) to keep it
// off the live site until it's ready to move up into ALL_POSTS.
const DRAFTS = import.meta.env.DEV
  ? [
    ]
  : []

export const posts = [...ALL_POSTS, ...DRAFTS]

// Canonical filter tabs, always shown, even before any posts exist.
const CANONICAL_TAGS = ['machine learning', 'research', 'my publications']

export function postYear(post) {
  return post.date.slice(0, 4)
}

export function postUrl(post) {
  return `/blog/${postYear(post)}/${post.slug}`
}

export function getPost(year, slug) {
  return posts.find((p) => p.slug === slug && postYear(p) === year)
}

export function getAllTags() {
  const set = new Set(CANONICAL_TAGS)
  for (const p of posts) for (const t of p.tags) set.add(t)
  return ['all', ...Array.from(set)]
}
