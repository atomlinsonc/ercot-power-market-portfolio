# ERCOT Real-Time Market Dashboard

Project 1 in the ERCOT Power Market Analytics Portfolio is a Streamlit dashboard that monitors ERCOT market conditions using public-data-ready workflows.

The first version uses mock ERCOT-style data so the dashboard, analysis functions, and reporting workflow can be built before live public ERCOT or GridStatus data is connected.

## Goal

Create a dashboard that helps answer practical trading-desk support questions:

- What is happening in ERCOT right now?
- Which zones or hubs are moving?
- Are real-time prices separating from day-ahead expectations?
- Is load coming in above or below forecast?
- Are price spikes occurring?
- What should a desk pay attention to today?

## Planned Dashboard Coverage

- ERCOT real-time settlement point prices
- ERCOT day-ahead prices
- Hub and load-zone prices
- Real-time vs day-ahead spread
- Actual load
- Forecasted load
- Load forecast error
- Generation mix if available
- Wind and solar output if available
- Reserve/scarcity indicators if available
- Price spike alerts
- Daily market summary

## Data Source Strategy

The project starts with a flexible data-source design. Public ERCOT data should be used where possible. GridStatus is supported as an optional Python data source if it makes data access easier.

The code should not require paid or proprietary data. Placeholder functions are included so real ERCOT data can be added cleanly later.

## Current Status

- Mock ERCOT-style sample data generated for 10 settlement points over 7 days.
- Streamlit dashboard reads processed sample data.
- Price metrics, spike alerts, DA/RT spreads, and load forecast charts are working.
- Live data integration is planned but not yet complete.

## Run Locally

From the repository root:

```bash
pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

## Potential Resume Bullet

Built an ERCOT real-time market dashboard using Python and Streamlit to monitor hub/load-zone prices, day-ahead vs real-time spreads, load forecast error, and price-spike intervals; paired the dashboard with a technical devlog and market-observation blog to document trading-desk support workflows using public market data.

