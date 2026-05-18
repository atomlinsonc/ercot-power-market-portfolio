# Automated Morning Market Brief Spec

## Purpose

The morning brief converts ERCOT-style dashboard data into a concise written report. The first version uses mock sample data, but the report structure is designed for public ERCOT or optional GridStatus data once live ingestion is added.

## Intended Audience

- Power market analyst
- Trading analyst
- Real-time trading support analyst
- Market operations analyst
- Desk lead who needs a quick scan before the operating day

## Core Questions Answered

- Which settlement points had the highest real-time prices?
- How many intervals exceeded the selected price-spike threshold?
- Where did day-ahead and real-time prices separate most?
- Did actual load come in meaningfully above or below forecast?
- What should the desk review next?

## Report Sections

- Executive Summary
- Hub and Load Zone Price Summary
- Price Spike Alerts
- DA/RT Spread Notes
- Load Forecast vs Actual Load
- Items to Watch

## Data Fields

- `timestamp`
- `settlement_point`
- `real_time_price`
- `day_ahead_price`
- `da_rt_spread`
- `forecast_load_mw`
- `actual_load_mw`
- `load_forecast_error_mw`

## Planned Future Improvements

- Schedule a local or cloud job to generate the brief each morning.
- Pull current ERCOT public data instead of mock sample data.
- Add generation mix, renewable output, and reserve/scarcity context when available.
- Export briefs to Markdown, HTML, and PDF.
- Add configurable settlement-point watchlists.
- Add a one-click download from the portfolio dashboard.

## Trading-Desk Support Value

A morning brief helps turn changing market data into an operating routine. It gives the analyst a repeatable checklist, reduces manual chart scanning, and makes it easier to communicate risk areas clearly.
