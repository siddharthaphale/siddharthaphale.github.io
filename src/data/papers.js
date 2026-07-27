export const papers = [
  {
    id: 'contrastive-critic-limits',
    title:
      'Good Rankers, Bad Objectives: Bilinear Contrastive Critics under Expressive Policy Search',
    thumb: '/blog/assets/contrastive-critic-limits/critic_grid.png',
    alt: 'Toy critic surfaces for raw bilinear, cosine, TD Q, and hybrid objectives',
    paperUrl: 'https://arxiv.org/abs/2607.27422',
    authors: [{ name: 'Siddharth Aphale', me: true }, { name: 'Ayushman Singh' }],
    venue: 'Preprint',
    year: 2026,
    blurb:
      'Bilinear contrastive critics are great goal retrievers but poorly calibrated value objectives: an expressive policy maximizing the critic over many candidates reliably picks high-scoring, low-value actions. Bounding the score does not fix it; only a Bellman-calibrated scalar for selection does.',
    links: [{ label: 'arXiv', href: 'https://arxiv.org/abs/2607.27422' }],
  },
  {
    id: 'scout',
    title: 'SCOUT: Per-Context Reset Curricula for Sparse-Reward Reinforcement Learning',
    thumb: '/blog/assets/scout/tile_schematic.svg',
    alt: 'SCOUT: per-context success-calibrated scaffold frontiers for sparse-reward RL',
    paperUrl: 'https://arxiv.org/abs/2607.26417',
    authors: [{ name: 'Siddharth Aphale', me: true }, { name: 'Ayushman Singh' }],
    venue: 'Preprint',
    year: 2026,
    blurb:
      "A per-context, success-calibrated reverse curriculum for sparse-reward embodied RL: each context's scaffold frontier removes assisted resets as success rises and restores them when it falls. It solves tasks uniform training never does and stays robust when contexts must pace differently.",
    links: [
      { label: 'arXiv', href: 'https://arxiv.org/abs/2607.26417' },
      { label: 'blog', href: '/blog/2026/scout-per-context-scaffolds' },
    ],
  },
  {
    id: 'roborepair',
    title: "Compile, Don't Reflect: Rethinking Self-Repair in Code-as-Policy Agents",
    thumb: '/blog/assets/roborepair/tile_loop.svg',
    alt: 'Compile, do not reflect: failed program compiles to MUST/NEVER constraints, then a fresh program is regenerated, looped five times',
    authors: [{ name: 'Siddharth Aphale', me: true }, { name: 'Ayushman Singh' }],
    venue: 'Preprint',
    year: 2026,
    blurb:
      'Retry loops for robot coders are sold as feedback-grounded reflection. Compiling failures into MUST/NEVER constraints and regenerating from scratch beats budget-matched resampling by +17pp at lower cost, while self-reflection and previous-code repair trail both. Mismatched feedback works just as well, so the gain is a task prior.',
    // No paperUrl or links while the paper is in anonymous review: the card
    // announces the work without pointing at anything that identifies it.
    // Restore the blog link (and add arXiv) once the embargo lifts.
  },
  {
    id: 'passk-rl-readiness',
    title: 'SFT Overtraining Predicts Rank Inversion via Entropy Collapse Under RLVR',
    thumb: '/projects/passk-rl-readiness/static/images/thumb_collapse_cycle_v3.svg',
    alt: 'Self-reinforcing entropy-collapse cycle under GRPO',
    paperUrl: 'https://arxiv.org/abs/2606.18487',
    authors: [{ name: 'Siddharth Aphale', me: true }, { name: 'Kelly Liu' }],
    venue: 'Deep Learning for Code (DL4C) Workshop @ ICML',
    year: 2026,
    blurb:
      'The highest scoring SFT checkpoint can be the worst one to train with RL. Over training collapses output entropy, which inverts checkpoint rankings under RLVR, and a free pre RL entropy check predicts the failure before you spend any GRPO compute.',
    links: [
      { label: 'code', href: 'https://github.com/siddharthaphale/entropy-collapse-rlvr' },
      { label: 'arXiv', href: 'https://arxiv.org/abs/2606.18487' },
      { label: 'poster', href: '/projects/passk-rl-readiness/static/pdfs/poster-entropy-collapse-rlvr.pdf' },
      { label: 'blog', href: '/blog/2026/sft-checkpoint-rl-collapse' },
    ],
  },
]
