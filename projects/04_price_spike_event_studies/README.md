# Project 4: ERCOT Price Spike Event Studies

This project studies high real-time price intervals as events. Instead of only listing spike intervals, it adds context around each event: what prices looked like before and after, how day-ahead prices compared, and whether load forecast error was elevated.

The first version uses the portfolio's mock ERCOT-style sample data. It is designed so live public ERCOT or optional GridStatus data can be connected later.

## Goal

Build a repeatable event-study workflow for reviewing abnormal ERCOT price intervals and turning them into clear market-observation notes.

This matters for trading-desk support because price spikes often require fast follow-up questions:

- Was the spike isolated to one hub/load zone or broad across ERCOT?
- How far above day-ahead did real-time clear?
- What happened in the hours before and after the event?
- Was load forecast error unusually high?
- Which intervals should be documented for later review?

## Current Scope

- Detect real-time price intervals above a configurable threshold.
- Rank spike events by real-time price.
- Add pre-event and post-event average price context.
- Build event windows around a selected spike.
- Generate concise event-study commentary for the highest mock-data spike.

## Files

- [event_study_spec.md](event_study_spec.md) explains the project design.
- [notes.md](notes.md) tracks development decisions.
- [sample_price_spike_event_study.md](sample_outputs/sample_price_spike_event_study.md) shows a sample event-study note using mock data.
- [price_spike_event_study.py](../../src/analysis/price_spike_event_study.py) contains the reusable Python helpers.

## How to Run the Tests Locally

```bash
pip install -r requirements.txt
pytest tests/test_price_spike_event_study.py
```

## Potential Resume Bullet

Built a Python price-spike event-study workflow for ERCOT-style real-time market data, ranking high-price intervals, adding pre/post event context, comparing day-ahead versus real-time outcomes, and producing concise market-observation commentary for trading-desk support.
