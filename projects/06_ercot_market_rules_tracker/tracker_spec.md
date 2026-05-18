# ERCOT Market Rules Tracker Spec

## Purpose

The tracker organizes ERCOT rule-change research into a format that can support market commentary and desk questions. The first version is a manually maintained sample tracker using public ERCOT source links.

## Intended Audience

- Power market analyst
- Trading analyst
- Real-time trading support analyst
- Market operations analyst
- Scheduling analyst
- Risk analyst

## Core Questions Answered

- Which rule changes are worth watching?
- What topic or market workflow could each item affect?
- What is the current status or next step to verify?
- Which items are high priority for storage, ancillary services, scarcity, RUC, or capacity reporting?
- What should be summarized in a daily or weekly market note?

## Tracker Fields

- `rule_id`
- `title`
- `status`
- `next_step`
- `topic`
- `impact_area`
- `priority`
- `source_url`
- `last_checked`
- `analyst_note`

## Planned Future Improvements

- Add automated refresh from ERCOT public reports where practical.
- Add a last-updated check that flags stale records.
- Add more rule types beyond NPRRs.
- Add a weekly rules digest report.
- Link rule topics to dashboard sections such as storage, reserves, scarcity, and RUC.
- Add citations to market-observation blog posts.

## Trading-Desk Support Value

Rules tracking helps an analyst avoid treating market data as isolated numbers. A desk needs to know when product definitions, settlement mechanics, reliability commitments, or reporting requirements may change the interpretation of prices and operational conditions.
