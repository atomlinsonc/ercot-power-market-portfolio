# Project 6: ERCOT Market Rules / NPRR Tracker

This project creates a structured tracker for ERCOT market rule changes, NPRRs, key dates, topics, and analyst notes. The first version is a starter research workflow, not a claim that the portfolio is automatically tracking live rule status.

The tracker is designed to help a trading-desk support analyst connect market rules to practical desk questions: storage behavior, ancillary services, scarcity/reserve products, RUC context, and longer-term capacity reporting.

## Goal

Build a repeatable market-rules watchlist that turns ERCOT rule documents into organized analyst notes.

This matters for trading-desk support because market rules can affect:

- which products are traded or monitored,
- how scarcity and reserve conditions are interpreted,
- how batteries and other resources participate,
- how daily market briefs explain operational context,
- and which rule changes deserve follow-up with traders, schedulers, or operations staff.

## Current Scope

- Store a starter CSV watchlist of selected ERCOT NPRR items.
- Track rule ID, title, status, next step, topic, impact area, priority, source URL, last-checked date, and analyst note.
- Provide Python helpers to validate, sort, summarize, and filter the tracker.
- Display a landing-page section with high-priority rules and rule-impact notes.

## Data Source Strategy

The initial tracker is manually curated from public ERCOT rule pages and must be verified before publication or interview use. Future work should automate source refreshes where practical.

Primary source pages:

- [ERCOT Nodal Protocol Revision Requests](https://www.ercot.com/mktrules/nprotocols/nprr)
- [ERCOT NPRR Submission Process](https://www.ercot.com/mktrules/nprotocols/nprr_process)
- [ERCOT Pending NPRR Report](https://www.ercot.com/mktrules/issues/reports/nprr/pending)

## Files

- [tracker_spec.md](tracker_spec.md) explains the project design.
- [notes.md](notes.md) tracks development decisions.
- [sample_market_rules_watchlist.md](sample_outputs/sample_market_rules_watchlist.md) shows a sample market-rules note.
- [ercot_market_rules_tracker_sample.csv](../../data/sample/ercot_market_rules_tracker_sample.csv) contains starter sample records.
- [market_rules_tracker.py](../../src/analysis/market_rules_tracker.py) contains reusable Python helpers.

## How to Run the Tests Locally

```bash
pip install -r requirements.txt
pytest tests/test_market_rules_tracker.py
```

## Potential Resume Bullet

Built a structured ERCOT market-rules tracker for NPRRs and related rule changes, organizing source links, statuses, priority, impact areas, and analyst notes to connect public rule updates to trading-desk support questions around storage, ancillary services, scarcity, RUC, and reserve reporting.
