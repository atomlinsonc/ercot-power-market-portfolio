# Week 2: First Dashboard Prototype

Date: 2026-05
Category: Technical Devlog

## What I worked on

I built the first Streamlit dashboard prototype using mock ERCOT-style data. The dashboard includes a hub/load-zone selector, date filter, price threshold control, summary metrics, price charts, DA/RT spread charts, load forecast comparison, and a spike table.

## Why it matters for a trading desk

A desk-support dashboard should reduce the time needed to understand current market conditions. Even a mock-data prototype can clarify which controls, charts, and summary metrics are useful before live data is connected.

## What I learned technically

Streamlit works well for quickly turning a pandas dataset into interactive controls and charts. Plotly makes it possible to label price and load behavior clearly without building a custom frontend for the dashboard.

## What I would improve next

The next step is to improve spike detection and make the alert table more useful by showing the largest intervals and the timing of abnormal prices.

