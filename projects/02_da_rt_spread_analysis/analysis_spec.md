# Day-Ahead vs Real-Time Spread Analysis Spec

## Purpose

Project 2 turns the dashboard's DA/RT spread chart into a focused analysis artifact. The goal is to move from "the spread changed" to "which intervals, locations, and operating hours deserve attention."

## Intended Audience

- Trading-desk support analyst
- Real-time market analyst
- Market operations analyst
- Asset optimization analyst
- Risk or scheduling analyst reviewing exposure to real-time price outcomes

## Core Questions Answered

- Which settlement points had the largest average absolute DA/RT spread?
- Which intervals had the biggest real-time premium over day-ahead?
- Which intervals had the biggest day-ahead premium over real-time?
- Do large spreads cluster in evening ramp hours?
- Are high absolute spreads connected to real-time price spikes or load forecast error?
- What follow-up questions should be raised before treating a spread as tradable signal?

## Data Fields

Required fields:

- `timestamp`
- `settlement_point`
- `day_ahead_price`
- `real_time_price`

Useful fields for context:

- `da_rt_spread`
- `forecast_load_mw`
- `actual_load_mw`
- `load_forecast_error_mw`

Derived fields:

- `da_rt_spread`: day-ahead price minus real-time price
- `abs_da_rt_spread`: absolute value of DA/RT spread
- `spread_direction`: whether day-ahead or real-time was higher
- `operating_hour`: hour extracted from timestamp

## Analysis Views

- Settlement point summary ranked by average absolute spread.
- Largest absolute spread intervals.
- Largest negative spreads, where real-time prices exceeded day-ahead prices.
- Largest positive spreads, where day-ahead prices exceeded real-time prices.
- Hourly spread profile across the sample window.
- Threshold-based abnormal spread table.

## Desk-Support Interpretation

A negative DA/RT spread means real-time settled above day-ahead. In a desk-support context, those intervals may point to unexpected scarcity, congestion, forecast error, operational constraints, or other real-time drivers.

A positive DA/RT spread means day-ahead settled above real-time. Those intervals may point to day-ahead risk premiums, softer real-time conditions, lower-than-expected load, or supply conditions that were more favorable than expected.

This project does not claim causation from price data alone. It creates a disciplined queue of intervals for further review.

## Future Improvements

- Replace mock data with public ERCOT or GridStatus data.
- Add nodal settlement point coverage where public data access is practical.
- Join load, wind, solar, outages, and reserve indicators.
- Compare hub spreads against load-zone spreads.
- Add daily exportable spread reports.
- Add SQL models for repeatable filtering and ranking.
- Add annotations for known weather or system events.
