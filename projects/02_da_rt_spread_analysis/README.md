# Project 2: Day-Ahead vs Real-Time Spread Analysis

This project analyzes the difference between ERCOT day-ahead prices and real-time prices using the convention:

```text
DA/RT spread = day-ahead price - real-time price
```

The first version uses the portfolio's mock ERCOT-style sample data. It is structured so public ERCOT or optional GridStatus data can replace the sample data later without changing the analysis questions.

## Goal

Build a repeatable workflow for identifying where and when day-ahead expectations differed from real-time outcomes across ERCOT hubs and load zones.

This matters for trading-desk support because DA/RT spread analysis helps answer:

- Where did real-time conditions come in higher than the day-ahead market expected?
- Which hubs or load zones showed the largest market misses?
- Did spread behavior cluster by hour, date, or settlement point?
- Were large negative spreads connected to high real-time prices or load forecast error?
- What intervals deserve follow-up market commentary?

## Current Scope

- Calculate DA/RT spread and absolute spread.
- Rank largest spread intervals.
- Summarize spread behavior by settlement point.
- Summarize spread behavior by operating hour.
- Flag abnormal spread intervals using an absolute-spread threshold.
- Generate a desk-style written summary from the filtered data.

## Files

- [analysis_spec.md](analysis_spec.md) explains the project design.
- [notes.md](notes.md) tracks development decisions.
- [sample_spread_analysis_report.md](sample_outputs/sample_spread_analysis_report.md) shows a sample desk-support report using mock data.
- [spread_analysis.py](../../src/analysis/spread_analysis.py) contains the reusable Python analysis helpers.

## How to Run the Analysis Locally

```bash
pip install -r requirements.txt
pytest tests/test_spread_analysis.py
```

The spread views are also represented on the landing page in the Project 2 section.

## Potential Resume Bullet

Built a day-ahead versus real-time spread analysis workflow in Python to identify ERCOT market misses by settlement point and operating hour, rank abnormal spread intervals, and translate price differences into desk-style commentary for power-market trading support.
