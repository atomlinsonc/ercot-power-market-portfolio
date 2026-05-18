import { FileText, Github, Linkedin, Mail } from "lucide-react";

const links = [
  { label: "email@example.com", href: "mailto:email@example.com", icon: Mail },
  { label: "LinkedIn placeholder", href: "#", icon: Linkedin },
  { label: "GitHub placeholder", href: "#", icon: Github },
  { label: "Resume placeholder", href: "#", icon: FileText },
];

export default function Contact() {
  return (
    <section className="section contact-section" id="contact">
      <div className="section-header">
        <p className="eyebrow">Contact</p>
        <h2>Resume, GitHub, and professional links.</h2>
      </div>
      <div className="contact-links">
        {links.map(({ label, href, icon: Icon }) => (
          <a href={href} key={label}>
            <Icon size={18} aria-hidden="true" />
            <span>{label}</span>
          </a>
        ))}
      </div>
    </section>
  );
}

