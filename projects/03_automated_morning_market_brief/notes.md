# Project 3 Notes

## Initial Entry

Project 3 begins by turning the mock-data dashboard output into a repeatable Markdown brief. The goal is not to make a flashy report. The goal is to practice a desk-support workflow: collect the latest market fields, summarize the important movements, flag intervals that deserve attention, and write clearly enough that a trader or analyst can scan the result quickly.

The current version intentionally uses mock ERCOT-style data. Live public ERCOT/GridStatus integration is a future milestone.

## Development Decisions

- Keep the report generator in `src/reporting/morning_market_brief.py`.
- Reuse existing spread and spike-detection helpers instead of duplicating calculations.
- Keep the generated output as Markdown because it is portable, easy to version, and suitable for GitHub.
- Include mock-data labeling directly in the output.
