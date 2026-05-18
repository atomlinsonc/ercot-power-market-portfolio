# ERCOT DA/RT Spread Analysis Report

Date: 2026-05-18  
Data status: Mock ERCOT-style sample data for portfolio development. This report does not use live ERCOT market data yet.

## Executive Summary

The sample data shows the largest day-ahead versus real-time differences during evening ramp hours, especially around 18:00 and 19:00. Because the spread is calculated as day-ahead minus real-time, the largest negative values indicate intervals where real-time prices settled materially above day-ahead prices.

Across the sample window, `LZ_AEN` had the highest average absolute spread at about `$12.85/MWh`, followed by `LZ_SOUTH`, `HB_HOUSTON`, `LZ_CPS`, and `LZ_HOUSTON`.

## Settlement Point Summary

| Settlement point | Average spread | Average absolute spread | Largest positive spread | Largest negative spread |
|---|---:|---:|---:|---:|
| LZ_AEN | -$6.82/MWh | $12.85/MWh | $18.54/MWh | -$360.92/MWh |
| LZ_SOUTH | -$5.55/MWh | $12.51/MWh | $23.04/MWh | -$322.57/MWh |
| HB_HOUSTON | -$5.86/MWh | $12.29/MWh | $20.44/MWh | -$315.33/MWh |
| LZ_CPS | -$5.32/MWh | $12.29/MWh | $20.73/MWh | -$335.46/MWh |
| LZ_HOUSTON | -$6.29/MWh | $12.24/MWh | $16.66/MWh | -$343.39/MWh |

## Largest Spread Intervals

| Timestamp | Settlement point | DA price | RT price | DA/RT spread | Load forecast error |
|---|---:|---:|---:|---:|---:|
| 2026-05-06 19:00 | LZ_AEN | $62.19 | $423.11 | -$360.92 | 1,093 MW |
| 2026-05-06 19:00 | LZ_HOUSTON | $59.52 | $402.91 | -$343.39 | 1,473 MW |
| 2026-05-06 19:00 | LZ_CPS | $56.94 | $392.40 | -$335.46 | 1,406 MW |
| 2026-05-06 19:00 | HB_SOUTH | $57.73 | $380.99 | -$323.26 | 733 MW |
| 2026-05-06 19:00 | LZ_SOUTH | $57.45 | $380.02 | -$322.57 | 934 MW |

## Hourly Pattern

The highest average absolute spreads in the mock dataset occurred in the evening:

- Hour 19: average absolute spread around `$54.29/MWh`
- Hour 18: average absolute spread around `$45.84/MWh`
- Hour 17: average absolute spread around `$31.26/MWh`
- Hour 16: average absolute spread around `$29.03/MWh`

This is directionally useful for the portfolio because it mirrors a real desk-support question: are the biggest misses clustered around ramp and peak-risk hours?

## Desk Questions

- Were the largest negative spreads connected to scarcity, congestion, forecast error, outages, renewable underperformance, or weather?
- Did load come in above forecast during the largest real-time premium intervals?
- Were the high-spread intervals broad across ERCOT, or isolated to specific zones?
- Would the same pattern appear in live public ERCOT data?
- What threshold should trigger an analyst note or alert?

## Next Improvement

Connect the spread workflow to public ERCOT/GridStatus data, then rerun the same ranking tables on recent market intervals with clear data-source notes.
