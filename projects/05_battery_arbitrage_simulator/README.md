# Project 5: Battery Storage Arbitrage Simulator

This project models a simple ERCOT battery storage arbitrage workflow using the portfolio's mock ERCOT-style real-time price data. The simulator is intentionally transparent: it charges during lower-price intervals, discharges during higher-price intervals, tracks state of charge, and summarizes gross margin.

The first version is not a production bid optimizer. It is a portfolio artifact for showing how storage economics can be translated into clean Python logic, desk-style metrics, and market questions.

## Goal

Build a readable battery arbitrage simulator that connects ERCOT real-time price behavior to storage dispatch decisions.

This matters for trading-desk support because storage analysts need to answer practical questions:

- Which settlement point produced the strongest price signal?
- How often would a simple battery charge or discharge?
- What gross margin did the strategy produce before fees, degradation, and operational constraints?
- Which intervals drove most of the value?
- What assumptions would need to be tightened before using this for real analysis?

## Current Scope

- Filter mock ERCOT-style prices by settlement point.
- Run a threshold-based battery dispatch strategy.
- Track charge intervals, discharge intervals, state of charge, and interval margin.
- Summarize gross margin, discharged MWh, equivalent cycles, and average charge/discharge prices.
- Display a landing-page section with key metrics and a dispatch watchlist.

## Important Limitations

- Uses mock ERCOT-style data until live public ERCOT/GridStatus data is connected.
- Ignores nodal constraints, battery degradation, ancillary service revenue, bids/offers, outage status, tax treatment, and operating restrictions.
- Uses a transparent threshold rule rather than optimization.
- Gross margin is not net revenue.

## Files

- [simulator_spec.md](simulator_spec.md) explains the project design.
- [notes.md](notes.md) tracks development decisions.
- [sample_battery_arbitrage_report.md](sample_outputs/sample_battery_arbitrage_report.md) shows a sample report using mock data.
- [battery_arbitrage.py](../../src/analysis/battery_arbitrage.py) contains reusable Python helpers.

## How to Run the Tests Locally

```bash
pip install -r requirements.txt
pytest tests/test_battery_arbitrage.py
```

## Potential Resume Bullet

Built a Python battery storage arbitrage simulator for ERCOT-style real-time prices, modeling charge/discharge decisions, state of charge, gross margin, equivalent cycles, and analyst commentary while clearly separating mock-data assumptions from future live market-data integration.
