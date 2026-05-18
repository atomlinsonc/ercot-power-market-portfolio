# ERCOT Daily Market Brief

Date: 2026-05-17

Mock-data notice: This sample brief uses mock ERCOT-style data generated for portfolio development. It does not represent live ERCOT market conditions.

## Executive Summary

Real-time prices in the sample dataset showed several artificial spike intervals designed to test dashboard alerting. The largest modeled moves appeared during high-load afternoon and early-evening periods.

## Hub and Load Zone Price Summary

HB_NORTH, HB_HOUSTON, HB_WEST, HB_SOUTH, and the included load zones can be compared in the dashboard by selecting a settlement point from the sidebar. Summary metrics include latest real-time price, average real-time price, maximum real-time price, and count of intervals above the selected spike threshold.

## Price Spike Alerts

The dashboard flags intervals where real-time prices exceed the selected threshold. In the mock dataset, artificial spikes are included so the alert workflow can be reviewed before live data integration.

## DA/RT Spread Notes

DA/RT spread is calculated as day-ahead price minus real-time price. Negative values indicate real-time prices exceeded day-ahead prices for the interval.

## Load Forecast vs Actual Load

The mock dataset includes forecast load, actual load, and load forecast error. Actual load above forecast may be worth monitoring because unexpected demand can contribute to price pressure.

## Items to Watch

- Intervals where real-time prices exceed the selected threshold.
- Settlement points with the largest DA/RT spread magnitude.
- Hours where actual load materially exceeds forecast load.
- Whether price spikes are isolated or broad across hubs and load zones.

## Questions for Further Analysis

- Did high prices occur at the same time across multiple settlement points?
- Did day-ahead prices anticipate the move?
- Was load forecast error positive during spike intervals?
- Which public ERCOT data products should be connected first for live monitoring?

