# ERCOT Price Spike Event Study

Mock-data notice: This note uses mock ERCOT-style data until live public ERCOT/GridStatus data is connected.

## Event Summary

The selected event is the highest real-time price interval in the mock sample data. LZ_AEN reached $423.11/MWh on 2026-05-06 19:00:00. The purpose of this study is to demonstrate a repeatable review format, not to explain an actual ERCOT market event.

## Event Details

- Settlement point: LZ_AEN
- Event timestamp: 2026-05-06 19:00:00
- Real-time price: $423.11/MWh
- Day-ahead price: $62.19/MWh
- DA/RT spread: -$360.92/MWh
- Load forecast error: 1,093 MW
- Pre-event average real-time price: $75.82/MWh
- Post-event average real-time price: $60.48/MWh

## Pre-Event Context

The event-study workflow reviews the two hours before the spike for the same settlement point. In a live-data version, this helps identify whether prices were already rising or whether the event appeared suddenly.

## Post-Event Context

The workflow also reviews the two hours after the spike. This helps separate a short isolated interval from a longer elevated-price period.

## Possible Market Questions

- Was the spike localized to one settlement point or broad across several hubs and load zones?
- Did actual load exceed forecast during the event?
- Were day-ahead prices already anticipating scarcity or congestion?
- Did neighboring intervals show elevated prices?
- What additional data would explain the move: reserves, outages, generation mix, renewable output, or constraints?

## Analyst Takeaway

The useful portfolio skill is not claiming to know the cause from price data alone. The useful skill is building a repeatable workflow that flags the event, adds context, and produces better follow-up questions.
