import { AlertTriangle, BookOpenCheck, ExternalLink, ListChecks } from "lucide-react";
import { marketRules } from "../data/marketRules.js";

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="rules-stat">
      <div className="metric-icon">
        <Icon size={18} aria-hidden="true" />
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
        <span>{note}</span>
      </div>
    </div>
  );
}

export default function MarketRulesTracker() {
  const highPriorityRules = marketRules.filter((rule) => rule.priority === "High");
  const topics = new Set(marketRules.map((rule) => rule.topic));
  const pendingRules = marketRules.filter((rule) => rule.status.toLowerCase().includes("pending"));

  return (
    <section className="rules-section" id="market-rules">
      <div className="rules-shell">
        <div className="section-header">
          <p className="eyebrow">Project 6 rule research</p>
          <h2>ERCOT market rules and NPRR tracker.</h2>
          <p>
            A source-linked watchlist that organizes rule changes by topic, priority,
            market impact, and analyst notes before they are used in dashboard commentary.
          </p>
        </div>

        <div className="rules-stat-grid">
          <Stat
            icon={ListChecks}
            label="Tracked items"
            value={marketRules.length.toLocaleString()}
            note="Starter sample watchlist"
          />
          <Stat
            icon={AlertTriangle}
            label="High priority"
            value={highPriorityRules.length.toLocaleString()}
            note="Storage and reserve topics"
          />
          <Stat
            icon={BookOpenCheck}
            label="Topics covered"
            value={topics.size.toLocaleString()}
            note="NPRR learning categories"
          />
          <Stat
            icon={ExternalLink}
            label="Pending items"
            value={pendingRules.length.toLocaleString()}
            note="Verify on ERCOT before citing"
          />
        </div>

        <div className="rules-grid">
          <article className="rules-panel">
            <div>
              <h3>Priority watchlist</h3>
              <p>Starter records use public ERCOT source links and manual analyst notes.</p>
            </div>
            <div className="rules-list">
              {highPriorityRules.map((rule) => (
                <a className="rules-list-row" href={rule.sourceUrl} key={rule.ruleId}>
                  <span>{rule.ruleId}</span>
                  <div>
                    <strong>{rule.title}</strong>
                    <em>{rule.impactArea}</em>
                  </div>
                  <b>{rule.priority}</b>
                </a>
              ))}
            </div>
          </article>

          <article className="rules-panel">
            <div>
              <h3>Desk-support notes</h3>
              <p>Each note translates rule tracking into questions for market commentary.</p>
            </div>
            <div className="rules-note-list">
              {marketRules.slice(0, 4).map((rule) => (
                <div className="rules-note" key={rule.ruleId}>
                  <span>{rule.topic}</span>
                  <p>{rule.analystNote}</p>
                </div>
              ))}
            </div>
          </article>
        </div>

        <p className="rules-disclaimer">
          Source notice: statuses are starter sample records and should be verified on ERCOT source pages
          before publication or interview use.
        </p>
      </div>
    </section>
  );
}
