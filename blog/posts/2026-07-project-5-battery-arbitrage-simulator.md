# Project 5: Battery Arbitrage Simulator

Date: July 2026

Category: Technical Devlog

## What I Worked On

I built the first version of a battery storage arbitrage simulator using mock ERCOT-style real-time prices. The model charges during lower-price intervals, discharges during higher-price intervals, tracks state of charge, and summarizes gross margin.

## Why It Matters for a Trading Desk

Storage is a useful way to connect price volatility, operational constraints, and asset optimization. Even a simple model helps frame better questions: where did the value come from, how concentrated were the discharge intervals, and which assumptions would need to be improved before the result became useful for real analysis?

## What I Learned Technically

The biggest technical lesson was to keep the first model transparent. A threshold strategy is less sophisticated than optimization, but it is easier to explain and test. That matters for a portfolio because the goal is to show clean reasoning before adding complexity.

## What I Would Improve Next

The next version should compare settlement points, add degradation costs, enforce an end-of-day state-of-charge target, and add a perfect-foresight optimization benchmark. Live ERCOT/GridStatus price integration should come before any market observation is treated as real.

## Resume Relevance

This project shows Python, time-series analysis, storage analytics, market-data interpretation, and the discipline to separate a useful prototype from a production trading tool.
