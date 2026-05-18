const roadmap = [
  ["Week 1", "Repo, landing page, sample data"],
  ["Week 2", "First Streamlit dashboard prototype"],
  ["Week 3", "Price spike detection"],
  ["Week 4", "DA/RT spread analysis"],
  ["Week 5", "Load forecast error"],
  ["Week 6", "Daily market brief automation"],
  ["Week 7", "Dashboard polish"],
  ["Week 8", "Final reflection and next project"],
];

export default function Roadmap() {
  return (
    <section className="section roadmap-section" id="roadmap">
      <div className="section-header">
        <p className="eyebrow">Two-month roadmap</p>
        <h2>Eight weeks from portfolio foundation to polished Project 1.</h2>
      </div>
      <div className="roadmap">
        {roadmap.map(([week, focus], index) => (
          <div className="roadmap-item" key={week}>
            <div className="roadmap-marker">{index + 1}</div>
            <div>
              <h3>{week}</h3>
              <p>{focus}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

