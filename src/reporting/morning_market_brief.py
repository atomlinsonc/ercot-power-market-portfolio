"""Automated morning market brief helpers."""

from __future__ import annotations

import pandas as pd

from src.analysis.price_spike_detection import detect_price_spikes
from src.analysis.spread_analysis import find_largest_spread_intervals, summarize_spreads


REQUIRED_COLUMNS = {
    "timestamp",
    "settlement_point",
    "real_time_price",
    "day_ahead_price",
    "da_rt_spread",
    "forecast_load_mw",
    "actual_load_mw",
    "load_forecast_error_mw",
}


def _validate_market_data(data: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required market brief columns: {sorted(missing)}")


def _format_currency(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):.2f}/MWh"


def summarize_settlement_points(data: pd.DataFrame) -> pd.DataFrame:
    """Return price and spread statistics by hub or load zone."""
    _validate_market_data(data)
    prepared = data.copy()
    prepared["timestamp"] = pd.to_datetime(prepared["timestamp"])

    latest_timestamp = prepared["timestamp"].max()
    latest = prepared.loc[prepared["timestamp"] == latest_timestamp, ["settlement_point", "real_time_price"]]
    latest = latest.rename(columns={"real_time_price": "latest_real_time_price"})

    summary = (
        prepared.groupby("settlement_point")
        .agg(
            average_real_time_price=("real_time_price", "mean"),
            max_real_time_price=("real_time_price", "max"),
            average_da_rt_spread=("da_rt_spread", "mean"),
            average_load_forecast_error_mw=("load_forecast_error_mw", "mean"),
        )
        .reset_index()
        .merge(latest, on="settlement_point", how="left")
        .sort_values("max_real_time_price", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def build_items_to_watch(data: pd.DataFrame, threshold: float = 150.0) -> list[str]:
    """Create short desk-support watch items from market data."""
    _validate_market_data(data)
    spikes = detect_price_spikes(data, threshold)
    spreads = find_largest_spread_intervals(data, limit=1)
    load_error = data.loc[data["load_forecast_error_mw"].abs().idxmax()]

    items = []
    if not spikes.empty:
        top_spike = spikes.iloc[0]
        items.append(
            f"Review {top_spike['settlement_point']} after a "
            f"{_format_currency(top_spike['real_time_price'])} real-time interval."
        )
    else:
        items.append(f"Monitor whether any intervals clear above {_format_currency(threshold)}.")

    if not spreads.empty:
        top_spread = spreads.iloc[0]
        items.append(
            f"Check the largest DA/RT miss at {top_spread['settlement_point']} "
            f"({_format_currency(top_spread['da_rt_spread'])})."
        )

    items.append(
        f"Compare forecast assumptions where load error reached "
        f"{load_error['load_forecast_error_mw']:,.0f} MW at {load_error['settlement_point']}."
    )
    return items


def generate_morning_market_brief(data: pd.DataFrame, threshold: float = 150.0) -> str:
    """Generate a Markdown morning brief from ERCOT-style market data."""
    if data.empty:
        return "# ERCOT Morning Market Brief\n\nNo market data is available for the selected period."

    _validate_market_data(data)
    prepared = data.copy()
    prepared["timestamp"] = pd.to_datetime(prepared["timestamp"])

    latest_date = prepared["timestamp"].max().date()
    point_summary = summarize_settlement_points(prepared)
    spread_summary = summarize_spreads(prepared)
    spikes = detect_price_spikes(prepared, threshold)
    top_spikes = spikes.head(5)
    largest_spreads = find_largest_spread_intervals(prepared, limit=5)
    load_error = prepared.loc[prepared["load_forecast_error_mw"].abs().idxmax()]

    top_point = point_summary.iloc[0]
    executive_summary = (
        f"Across the mock ERCOT-style sample, {top_point['settlement_point']} recorded the highest "
        f"real-time price at {_format_currency(top_point['max_real_time_price'])}. "
        f"{len(spikes)} intervals cleared at or above the selected spike threshold of "
        f"{_format_currency(threshold)}. The average DA/RT spread was "
        f"{_format_currency(spread_summary['average_spread'])}."
    )

    point_lines = [
        (
            f"- {row.settlement_point}: latest RT {_format_currency(row.latest_real_time_price)}, "
            f"avg RT {_format_currency(row.average_real_time_price)}, "
            f"max RT {_format_currency(row.max_real_time_price)}"
        )
        for row in point_summary.head(6).itertuples(index=False)
    ]
    spike_lines = [
        f"- {row.timestamp}: {row.settlement_point} at {_format_currency(row.real_time_price)}"
        for row in top_spikes.itertuples(index=False)
    ] or ["- No intervals exceeded the selected threshold."]
    spread_lines = [
        f"- {row.timestamp}: {row.settlement_point} DA/RT spread {_format_currency(row.da_rt_spread)}"
        for row in largest_spreads.itertuples(index=False)
    ]
    watch_lines = [f"- {item}" for item in build_items_to_watch(prepared, threshold)]

    return "\n".join(
        [
            "# ERCOT Morning Market Brief",
            "",
            f"Date: {latest_date}",
            "",
            "Mock-data notice: This brief uses mock ERCOT-style data until live public ERCOT/GridStatus data is connected.",
            "",
            "## Executive Summary",
            "",
            executive_summary,
            "",
            "## Hub and Load Zone Price Summary",
            "",
            *point_lines,
            "",
            "## Price Spike Alerts",
            "",
            *spike_lines,
            "",
            "## DA/RT Spread Notes",
            "",
            *spread_lines,
            "",
            "## Load Forecast vs Actual Load",
            "",
            (
                f"The largest absolute load forecast error was "
                f"{load_error['load_forecast_error_mw']:,.0f} MW at "
                f"{load_error['settlement_point']} during {load_error['timestamp']}."
            ),
            "",
            "## Items to Watch",
            "",
            *watch_lines,
        ]
    )
