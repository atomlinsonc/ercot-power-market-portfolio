import { ArrowUpRight } from "lucide-react";

export default function BlogPreview({ posts }) {
  return (
    <section className="section blog-section" id="blog">
      <div className="section-header">
        <p className="eyebrow">Build Log and Market Notes</p>
        <h2>Recent writing on the build process and ERCOT market questions.</h2>
      </div>
      <div className="blog-grid">
        {posts.map((post) => (
          <article className="blog-card" key={post.title}>
            <div className="blog-meta">
              <span>{post.date}</span>
              <span>{post.category}</span>
            </div>
            <h3>{post.title}</h3>
            <p>{post.summary}</p>
            <a href={post.href}>
              Read note
              <ArrowUpRight size={16} aria-hidden="true" />
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}

