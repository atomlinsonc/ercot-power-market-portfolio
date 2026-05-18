# Dashboard Specification: ERCOT Real-Time Market Dashboard

## Dashboard Purpose

The dashboard is designed to summarize ERCOT market conditions in a format that would be useful for a junior analyst or trading-desk support role. It focuses on price movement, day-ahead versus real-time differences, load forecast error, and spike intervals.

## Intended Audience

- Power market analysts
- Real-time trading support analysts
- Market operations analysts
- Asset optimization analysts
- Scheduling analysts
- Risk analysts
- Hiring managers reviewing practical analyst portfolio work

## Core Questions Answered

- What are real-time prices doing for the selected hub or load zone?
- How do real-time prices compare with day-ahead prices?
- When are DA/RT spreads largest?
- Is actual load above or below forecast?
- Did prices exceed a selected spike threshold?
- What should a trading desk pay attention to next?

## Data Fields

| Field | Description |
| --- | --- |
| timestamp | Market interval timestamp |
| settlement_point | ERCOT hub or load-zone identifier |
| real_time_price | Real-time settlement point price |
| day_ahead_price | Day-ahead settlement point price |
| da_rt_spread | Day-ahead price minus real-time price |
| forecast_load_mw | Forecasted load in MW |
| actual_load_mw | Actual load in MW |
| load_forecast_error_mw | Actual load minus forecast load |

## Planned Future Improvements

- Connect live public ERCOT data.
- Add optional GridStatus data pulls.
- Add historical day-ahead and real-time spread distributions.
- Add ranked price-spike event views.
- Add load forecast error diagnostics.
- Add generation mix, wind, solar, reserves, and scarcity indicators when reliable public sources are wired in.
- Add automated daily market brief generation.
- Add deployment instructions and production configuration.

## How This Helps a Trading Desk

A desk-support analyst needs to summarize changing market conditions quickly. This dashboard helps turn raw market data into a repeatable workflow: filter the relevant location, check price levels, compare day-ahead expectations with real-time outcomes, identify spike intervals, and produce a concise written summary for follow-up.

