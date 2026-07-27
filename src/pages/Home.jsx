import Header from '../components/Header.jsx'
import PaperCard from '../components/PaperCard.jsx'
import TypingText from '../components/TypingText.jsx'
import { papers } from '../data/papers.js'
import { projects } from '../data/projects.js'

export default function Home() {
  return (
    <div className="app-shell">
      <Header />

      <main className="home">
        <section className="bio-section">
          <div className="bio-text">
            <h1 className="brand-name">
              <TypingText text="Siddharth Aphale" />
            </h1>
            <p className="brand-subtitle">
              Data Scientist · Probabilistic ML · Embodied AI
            </p>

            <p>
              Hi! I'm Siddharth, a Data Scientist working on cloud battery analytics at{' '}
              <a className="elysia-link" href="https://elysia.co/" target="_blank" rel="noreferrer">
                Elysia, Battery Intelligence from Fortescue
              </a>{' '}
              (Oxford, UK), and a part time student at Stanford University pursuing a Graduate
              Certificate in Artificial Intelligence.
            </p>
            <p>
              I develop prognostic algorithms for automotive li-ion battery packs, combining
              physics based modeling, probabilistic machine learning, and Bayesian state estimation for
              calibrated and reliable predictions.
            </p>
            <p>
              I have a Masters in Data Science from BITS Pilani. My thesis focused on developing a physics informed machine learning framework for li-ion battery SOH prediction.
            </p>

            <div className="social-links">
              <a href="mailto:saphale15@gmail.com">
                <img className="soc-ico" src="/assets/images/icons/email.svg" alt="" /> Email
              </a>
              <a
                href="https://scholar.google.com/citations?user=JgKNv2cAAAAJ&hl=en"
                target="_blank"
                rel="noreferrer"
              >
                <img className="soc-ico" src="/assets/images/icons/scholar.svg" alt="" /> Scholar
              </a>
              <a href="https://linkedin.com/in/siddharthaphale" target="_blank" rel="noreferrer">
                <img className="soc-ico" src="/assets/images/icons/linkedin.svg" alt="" /> LinkedIn
              </a>
              <a href="https://github.com/siddharthaphale" target="_blank" rel="noreferrer">
                <img className="soc-ico" src="/assets/images/icons/github-color.svg" alt="" /> GitHub
              </a>
            </div>
          </div>

          <div className="bio-portrait">
            <img src="/assets/images/headshot.jpeg" alt="Siddharth Aphale" />
          </div>
        </section>

        <section className="section">
          <h2 className="section-heading">research</h2>
          <p className="section-blurb">
            I'm broadly interested in structured probabilistic inference, generative modeling, and
            reinforcement learning. More recently, I've focused on post-training and test-time
            compute for LLMs and VLAs: what training pipelines and curricula make learnable, whether
            the objectives and critics we optimize measure what we intend, and how a fixed inference
            budget is best allocated when an agent acts.
          </p>

          <div className="paper-list">
            {papers.map((p) => (
              <PaperCard key={p.id} paper={p} />
            ))}
          </div>
        </section>

        {projects.length > 0 && (
          <section className="section">
            <h2 className="section-heading">projects</h2>
            <p className="section-blurb">
              Coursework projects.
            </p>

            <div className="paper-list">
              {projects.map((p) => (
                <PaperCard key={p.id} paper={p} />
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="site-footer">
        <div className="footer-row">
          <span>Siddharth Aphale · 2026</span>
          <p className="footer-reach">
            Feel free to <a href="mailto:saphale15@gmail.com">reach out</a>. Always happy to connect.
          </p>
          <span>
            <a href="https://linkedin.com/in/siddharthaphale" target="_blank" rel="noreferrer">
              LinkedIn
            </a>{' '}
            ·{' '}
            <a href="https://github.com/siddharthaphale" target="_blank" rel="noreferrer">
              GitHub
            </a>
          </span>
        </div>
      </footer>
    </div>
  )
}
