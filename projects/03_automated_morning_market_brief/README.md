# Project 3: Automated Morning Market Brief

This project turns the dashboard and analysis outputs into a repeatable morning brief that a junior analyst or trading-desk support analyst could prepare before the desk day starts.

The current version uses the portfolio's mock ERCOT-style sample data. It is structured so live public ERCOT or optional GridStatus data can replace the sample data later.

## Goal

Generate a concise Markdown market brief that summarizes price behavior, spike intervals, DA/RT spreads, load forecast error, and practical items to watch.

This matters for trading-desk support because the desk does not only need charts. It needs a repeatable way to answer:

- What moved since the last review?
- Which hubs or load zones deserve attention?
- Did real-time prices separate from day-ahead expectations?
- Were any intervals above the selected spike threshold?
- Was actual load materially above or below forecast?
- What should an analyst review before sending a desk note?

## Current Scope

- Summarize hub and load-zone prices.
- Identify intervals above a configurable real-time price threshold.
- Rank large DA/RT spread intervals.
- Highlight the largest absolute load forecast error.
- Generate a Markdown brief with analyst-style sections.
- Keep mock-data labeling visible until live data is connected.

## Files

- [brief_spec.md](brief_spec.md) explains the project design.
- [notes.md](notes.md) tracks development decisions.
- [sample_morning_market_brief.md](sample_outputs/sample_morning_market_brief.md) shows a sample desk-support brief using mock data.
- [morning_market_brief.py](../../src/reporting/morning_market_brief.py) contains the reusable Python report generator.

## How to Run the Tests Locally

```bash
pip install -r requirements.txt
pytest tests/test_morning_market_brief.py
```

## Potential Resume Bullet

Built an automated ERCOT morning market brief workflow in Python to summarize hub/load-zone prices, DA/RT spreads, price-spike alerts, and load forecast error; translated mock market data into a repeatable Markdown report designed for trading-desk support communication.
