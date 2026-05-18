# Project 2 Notes

## 2026-05-18: Project kickoff

Project 2 begins as a focused analysis layer on top of the existing mock ERCOT-style dataset. The goal is not to pretend the portfolio already has live market data; the goal is to show how a desk-support analyst would structure a repeatable DA/RT spread review once public ERCOT or GridStatus data is connected.

Initial implementation priorities:

- Keep the spread convention explicit: day-ahead minus real-time.
- Separate reusable Python logic from presentation.
- Rank the intervals that deserve analyst attention.
- Add a visible Project 2 section to the portfolio site.
- Keep written commentary honest about mock data.

Questions to revisit after live data is connected:

- Which ERCOT hub or load-zone products are most relevant for the target role?
- Should the dashboard treat RT premium intervals separately from DA premium intervals?
- What additional context best explains spread moves: load forecast error, renewables, reserves, outages, congestion, or weather?
- What threshold should define an abnormal spread in a production desk workflow?
