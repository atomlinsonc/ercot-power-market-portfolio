import { BookOpen, FileText, Github, LineChart } from "lucide-react";

const links = [
  { label: "View Live Dashboard", href: "#", icon: LineChart },
  { label: "View GitHub Repo", href: "https://github.com/atomlinsonc/ercot-power-market-portfolio", icon: Github },
  { label: "Read the Blog", href: "#blog", icon: BookOpen },
  { label: "Download Resume", href: "#", icon: FileText },
];

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-overlay" />
      <nav className="top-nav" aria-label="Primary navigation">
        <a href="#projects">Projects</a>
        <a href="#blog">Blog</a>
        <a href="#roadmap">Roadmap</a>
        <a href="#contact">Contact</a>
      </nav>
      <div className="hero-content">
        <p className="eyebrow hero-eyebrow">Austin, Texas | ERCOT analytics</p>
        <h1>ERCOT Power Market Analytics Portfolio</h1>
        <p className="hero-subtitle">
          Python, SQL, and dashboarding projects built to support power trading
          desk workflows in ERCOT: real-time prices, day-ahead spreads, load
          forecast error, price spikes, market commentary, and trading-desk
          reporting.
        </p>
        <div className="hero-actions" aria-label="Portfolio links">
          {links.map(({ label, href, icon: Icon }, index) => (
            <a className={index === 0 ? "button primary" : "button"} href={href} key={label}>
              <Icon size={18} aria-hidden="true" />
              <span>{label}</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
