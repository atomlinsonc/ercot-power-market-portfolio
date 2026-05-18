import { ExternalLink, Github, LayoutDashboard } from "lucide-react";

export default function ProjectCard({ project }) {
  const isActive = project.status === "Active";

  return (
    <article className="project-card">
      <div className="project-card-header">
        <span className={isActive ? "status active" : "status planned"}>
          {project.status}
        </span>
        <h3>{project.title}</h3>
      </div>
      <p>{project.description}</p>
      <div className="skill-list">
        {project.skills.map((skill) => (
          <span key={skill}>{skill}</span>
        ))}
      </div>
      <div className="card-actions">
        {project.links.dashboard && (
          <a href={project.links.dashboard}>
            <LayoutDashboard size={16} aria-hidden="true" />
            Dashboard
          </a>
        )}
        {project.links.report && (
          <a href={project.links.report}>
            <ExternalLink size={16} aria-hidden="true" />
            Report
          </a>
        )}
        {project.links.github && (
          <a href={project.links.github}>
            <Github size={16} aria-hidden="true" />
            GitHub
          </a>
        )}
      </div>
    </article>
  );
}

