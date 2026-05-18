# Project 2: DA/RT Spread Analysis

Date: May 2026  
Category: Technical Devlog

## What I worked on

I turned the dashboard's day-ahead versus real-time spread chart into a focused analysis project. The first version uses mock ERCOT-style data and calculates spread as day-ahead price minus real-time price.

## Why it matters for a trading desk

Spread analysis helps identify where the market's day-ahead expectations differed from real-time outcomes. A support analyst can use that workflow to rank intervals that deserve follow-up commentary, especially when real-time prices settle far above day-ahead prices.

## What I learned technically

The useful artifact is not just a chart. The project needs reusable functions for spread calculation, ranking, grouping by settlement point, grouping by operating hour, and flagging abnormal intervals. That makes the analysis easier to rerun once live public ERCOT or GridStatus data is connected.

## What I would improve next

The next step is to replace the sample dataset with live public market data, then add context fields such as load, wind, solar, reserves, outages, congestion, or weather. Price spreads alone show what moved, but not why it moved.

## Resume relevance

This project demonstrates time-series analysis, market-data interpretation, desk-style reporting, and careful documentation of assumptions.
