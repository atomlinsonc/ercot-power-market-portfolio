import BlogPreview from "./components/BlogPreview.jsx";
import Contact from "./components/Contact.jsx";
import Hero from "./components/Hero.jsx";
import ProjectCard from "./components/ProjectCard.jsx";
import Roadmap from "./components/Roadmap.jsx";
import { blogPosts } from "./data/blogPosts.js";
import { projects } from "./data/projects.js";

export default function App() {
  return (
    <main>
      <Hero />

      <section className="section about-section" id="about">
        <div className="section-header">
          <p className="eyebrow">Career-transition portfolio</p>
          <h2>Built around public ERCOT data and practical analyst workflows.</h2>
        </div>
        <div className="about-copy">
          <p>
            I am a high school economics teacher in Austin and a data science
            master's student building a focused portfolio for ERCOT
            power-market analytics and trading desk support roles.
          </p>
          <p>
            The work is intentionally practical: pull public market data, clean
            time-series records, monitor real-time conditions, explain price
            movement, automate repeatable reports, and communicate clearly with
            technical and non-technical audiences.
          </p>
        </div>
      </section>

      <section className="section" id="projects">
        <div className="section-header">
          <p className="eyebrow">Portfolio projects</p>
          <h2>Power-market analytics projects with trading-desk support framing.</h2>
        </div>
        <div className="project-grid">
          {projects.map((project) => (
            <ProjectCard key={project.title} project={project} />
          ))}
        </div>
      </section>

      <BlogPreview posts={blogPosts} />
      <Roadmap />
      <Contact />
    </main>
  );
}

