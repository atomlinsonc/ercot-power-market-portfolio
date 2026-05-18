# ERCOT Power Market Analytics Portfolio

Practical ERCOT market analytics for power trading desk support roles.

This repository demonstrates a career-transition portfolio focused on practical ERCOT market analytics, trading-desk support workflows, and clear market communication. It combines Python, Streamlit, SQL-ready data workflows, dashboarding, technical writing, and market-observation notes using public or mock ERCOT-style data.

The first milestone uses realistic mock data while the project structure is prepared for live public ERCOT and optional GridStatus integration.

## Live Portfolio Site

[Live Portfolio Site](https://ercot-power-market-portfolio.vercel.app/)

## Project 1: ERCOT Real-Time Market Dashboard

The first project is a Streamlit dashboard designed to monitor ERCOT real-time market conditions. It tracks hub and load-zone prices, day-ahead versus real-time spreads, load forecast error, and price-spike intervals.

Run locally:

```bash
pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

## Project 2: Day-Ahead vs Real-Time Spread Analysis

The second project turns the dashboard's spread chart into a repeatable Python analysis workflow. It ranks ERCOT day-ahead versus real-time market misses by settlement point and operating hour, flags abnormal spread intervals, and translates the results into desk-style commentary.

The current version uses mock ERCOT-style data and is ready for live public ERCOT/GridStatus data integration.

Project folder:

[projects/02_da_rt_spread_analysis](projects/02_da_rt_spread_analysis/README.md)

## Project 3: Automated Morning Market Brief

The third project turns dashboard outputs into a repeatable Markdown morning brief. It summarizes hub and load-zone prices, price-spike intervals, DA/RT spread notes, load forecast error, and practical items to watch.

The current version uses mock ERCOT-style data and keeps that limitation visible in the generated report.

Project folder:

[projects/03_automated_morning_market_brief](projects/03_automated_morning_market_brief/README.md)

## Project 4: ERCOT Price Spike Event Studies

The fourth project reviews high real-time price intervals as events. It ranks spike intervals, adds pre-event and post-event context, compares day-ahead versus real-time outcomes, and turns the result into market-observation commentary.

The current version uses mock ERCOT-style data and is ready for live public ERCOT/GridStatus context fields later.

Project folder:

[projects/04_price_spike_event_studies](projects/04_price_spike_event_studies/README.md)

## Project 5: Battery Storage Arbitrage Simulator

The fifth project models a simple battery storage arbitrage workflow using ERCOT-style real-time prices. It tracks charge and discharge intervals, state of charge, gross margin, equivalent cycles, and analyst commentary with clear caveats around mock data and simplified assumptions.

The current version uses mock ERCOT-style data and is designed to become a live-price workflow after public ERCOT/GridStatus integration.

Project folder:

[projects/05_battery_arbitrage_simulator](projects/05_battery_arbitrage_simulator/README.md)

## Project 6: ERCOT Market Rules / NPRR Tracker

The sixth project creates a structured tracker for ERCOT rule changes and NPRRs. It organizes source links, status, next step, topic, priority, impact area, and analyst notes so market-rule research can support dashboard commentary and desk questions.

The current version is a manually curated starter tracker and should be verified against ERCOT source pages before public rule-status claims are made.

Project folder:

[projects/06_ercot_market_rules_tracker](projects/06_ercot_market_rules_tracker/README.md)

## Blog and Learning Log

The portfolio includes both technical development notes and ERCOT market observations. Technical posts explain how the dashboard, data pipeline, and reporting tools are built. Market notes explain what the dashboard shows and what questions a trading desk might ask next.

Early posts clearly label the dashboard as mock-data based until live public ERCOT or GridStatus data is connected.

## Portfolio Roadmap

- ERCOT Real-Time Market Dashboard
- Day-Ahead vs Real-Time Spread Analysis
- Automated Morning Market Brief
- ERCOT Price Spike Event Studies
- Battery Storage Arbitrage Simulator
- Load Forecast Error Model
- Basis Risk / Congestion Tracker
- ERCOT Market Rules / NPRR Tracker

## Skills Demonstrated

- Python
- SQL / DuckDB or SQLite
- API data ingestion
- Time-series analysis
- ERCOT market data
- Streamlit dashboarding
- Market reporting
- Data visualization
- Technical writing
- Energy market communication

## Target Roles

- Power Market Analyst
- Trading Analyst
- Real-Time Trading Support Analyst
- Energy Market Analyst
- Market Operations Analyst
- Asset Optimization Analyst
- Scheduling Analyst
- Risk Analyst

## Why This Portfolio Matters

Power trading desks need fast, clean, repeatable tools that summarize changing market conditions. A useful analyst workflow does more than collect data: it highlights what moved, where risk may be building, and which questions deserve attention before the next market interval or desk meeting.

This portfolio is built to show practical support skills: ingesting market data, cleaning time-series records, building readable dashboards, automating briefings, and communicating market observations clearly.
