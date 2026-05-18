# Price Spike Event Study Spec

## Purpose

The event-study workflow turns high real-time price intervals into structured review notes. The initial version uses mock ERCOT-style data and is intended to become a live-data workflow after ERCOT/GridStatus integration.

## Intended Audience

- Power market analyst
- Real-time trading support analyst
- Trading analyst
- Market operations analyst
- Data science portfolio reviewer

## Core Questions Answered

- Which intervals exceeded the selected real-time price threshold?
- Which event had the highest real-time price?
- What was the DA/RT spread during the event?
- What did prices look like before and after the event?
- Was load forecast error elevated during the event interval?
- What market questions should the analyst ask next?

## Event Definition

A price spike event is currently defined as:

```text
real_time_price >= selected_threshold
```

The default threshold in the project examples is $150/MWh.

## Data Fields

- `timestamp`
- `settlement_point`
- `real_time_price`
- `day_ahead_price`
- `da_rt_spread`
- `load_forecast_error_mw`

## Planned Future Improvements

- Add event clustering so adjacent spike intervals are grouped into one event.
- Add system-wide versus localized event classification.
- Join load, generation mix, renewable output, reserve, and outage context when available.
- Create event-study notebooks with charts around each event window.
- Add market-observation blog templates for event writeups.

## Trading-Desk Support Value

Event studies help analysts move from "a price spike happened" to "here is the context worth reviewing." That distinction matters because desks need fast explanations, follow-up questions, and repeatable documentation after abnormal intervals.
