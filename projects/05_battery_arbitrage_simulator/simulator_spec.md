# Battery Arbitrage Simulator Spec

## Purpose

The simulator demonstrates how real-time price time series can be converted into a simple battery dispatch and gross-margin analysis. The first version uses mock ERCOT-style data and is intended to become a live-data workflow after ERCOT/GridStatus integration.

## Intended Audience

- Power market analyst
- Trading analyst
- Real-time trading support analyst
- Asset optimization analyst
- Data science portfolio reviewer

## Core Questions Answered

- When would a simple battery charge or discharge?
- Which intervals created the highest simulated margin?
- How much energy was charged from the grid and discharged back to the market?
- What was the ending state of charge?
- How sensitive is the result to price thresholds, power rating, capacity, and efficiency?

## Strategy Definition

The initial strategy is a transparent threshold rule:

```text
charge when real_time_price <= selected low-price quantile
discharge when real_time_price >= selected high-price quantile
hold otherwise
```

Default assumptions:

- Capacity: 100 MWh
- Power: 50 MW
- Round-trip efficiency: 86%
- Starting state of charge: 50 MWh
- Charge threshold: 30th percentile price
- Discharge threshold: 75th percentile price

## Data Fields

- `timestamp`
- `settlement_point`
- `real_time_price`
- `action`
- `charge_from_grid_mwh`
- `discharge_to_grid_mwh`
- `state_of_charge_mwh`
- `interval_margin`

## Planned Future Improvements

- Add configurable duration, degradation cost, variable O&M, and end-of-day state-of-charge target.
- Compare hub and load-zone results side by side.
- Add day-ahead versus real-time spread inputs.
- Add perfect-foresight optimization as a benchmark.
- Integrate live public ERCOT/GridStatus prices.
- Add ancillary service revenue placeholders after market-rule research.

## Trading-Desk Support Value

The portfolio value is the workflow: price signal, dispatch rule, margin summary, and clear caveats. It shows the ability to translate market data into a practical support tool while avoiding false precision.
