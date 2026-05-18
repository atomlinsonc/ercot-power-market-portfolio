# Week 3: Price Spike Detection

Date: 2026-06
Category: Dashboard Improvement

## What I worked on

I added price-spike detection logic based on a user-selected threshold. The dashboard counts spike intervals, identifies the maximum price interval, and displays a table of intervals above the selected threshold.

## Why spike detection matters

Real-time power prices can move quickly. A support analyst needs to identify abnormal intervals, summarize when they occurred, and help the desk decide what to investigate next.

## What I learned

A threshold alert is simple, but it is still useful. The next version should compare spikes by settlement point, time of day, load conditions, and DA/RT spread.

## Questions for further analysis

- Did the spike occur in one settlement point or across the market?
- Was load above forecast during the spike?
- Did day-ahead prices anticipate the move?
- Were there system conditions that explain the interval?

