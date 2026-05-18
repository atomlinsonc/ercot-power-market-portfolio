# Development Notes

## 2026-05-17: Project start

Project 1 begins with a mock-data dashboard. The first milestone is to build the repo structure, sample data, Streamlit dashboard, analysis helpers, and documentation without pretending live market data is already connected.

The live data path will be added later through public ERCOT data sources where possible, with GridStatus as an optional convenience layer if it improves access and reliability.

Initial focus:

- Generate realistic ERCOT-style hourly sample data.
- Include hubs and load zones relevant to a first market dashboard.
- Add artificial price spikes so alert logic can be demonstrated.
- Keep calculations readable and testable.
- Create documentation that frames the project as trading-desk support preparation.

