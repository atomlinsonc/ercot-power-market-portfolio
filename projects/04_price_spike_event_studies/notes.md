# Project 4 Notes

## Initial Entry

Project 4 starts with a simple event-study workflow around mock ERCOT-style price spikes. The first goal is to identify the highest real-time price intervals, capture surrounding-hour context, and write a short market-observation note.

This project should stay honest about data limitations. The current sample can demonstrate the workflow, but it cannot explain real ERCOT market behavior until live public ERCOT/GridStatus data and additional context fields are connected.

## Development Decisions

- Keep event-study helpers in `src/analysis/price_spike_event_study.py`.
- Reuse the existing `detect_price_spikes` helper for threshold logic.
- Treat each spike interval as its own event in version one.
- Add pre-event and post-event average price context without claiming causality.
