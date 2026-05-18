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
