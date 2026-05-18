# Battery Arbitrage Simulator Notes

## 2026-05-18 Initial Build

Project 5 starts with a mock-data simulator. The first version uses a simple threshold strategy rather than mathematical optimization so the assumptions are easy to inspect in an interview or portfolio review.

The key design choice is to treat the output as gross margin from a simplified dispatch, not as a trade recommendation or production revenue forecast. Future versions should connect live ERCOT/GridStatus prices, add storage-specific constraints, and compare the simple heuristic to an optimization benchmark.
