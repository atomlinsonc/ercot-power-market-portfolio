"""Day-ahead versus real-time spread analysis."""

from __future__ import annotations

import pandas as pd

REQUIRED_PRICE_COLUMNS = {"day_ahead_price", "real_time_price"}


def _format_spread(value: float) -> str:
    """Format signed spread values as dollars per MWh."""
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):.2f}/MWh"


def add_spread_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Add DA/RT spread fields using day-ahead minus real-time convention."""
    missing = REQUIRED_PRICE_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required spread columns: {sorted(missing)}")

    result = data.copy()
    result["da_rt_spread"] = result["day_ahead_price"] - result["real_time_price"]
    result["abs_da_rt_spread"] = result["da_rt_spread"].abs()
    return result


def prepare_spread_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare spread data with timestamp, hour, and direction fields."""
    result = add_spread_columns(data)

    if "timestamp" in result.columns:
        result["timestamp"] = pd.to_datetime(result["timestamp"])
        result["operating_hour"] = result["timestamp"].dt.hour

    result["spread_direction"] = "Flat"
    result.loc[result["da_rt_spread"] > 0, "spread_direction"] = "Day-ahead premium"
    result.loc[result["da_rt_spread"] < 0, "spread_direction"] = "Real-time premium"
    return result


def summarize_spreads(data: pd.DataFrame) -> dict[str, float]:
    """Return key spread summary statistics."""
    if "da_rt_spread" not in data.columns:
        data = add_spread_columns(data)

    return {
        "average_spread": float(data["da_rt_spread"].mean()),
        "max_spread": float(data["da_rt_spread"].max()),
        "min_spread": float(data["da_rt_spread"].min()),
        "average_absolute_spread": float(data["da_rt_spread"].abs().mean()),
    }


def summarize_spreads_by_settlement_point(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize spread behavior by hub or load zone."""
    required = {"settlement_point"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required grouping columns: {sorted(missing)}")

    prepared = prepare_spread_data(data)
    summary = (
        prepared.groupby("settlement_point")
        .agg(
            interval_count=("da_rt_spread", "size"),
            average_spread=("da_rt_spread", "mean"),
            average_absolute_spread=("abs_da_rt_spread", "mean"),
            max_positive_spread=("da_rt_spread", "max"),
            max_negative_spread=("da_rt_spread", "min"),
            average_real_time_price=("real_time_price", "mean"),
            average_day_ahead_price=("day_ahead_price", "mean"),
        )
        .sort_values("average_absolute_spread", ascending=False)
        .reset_index()
    )
    return summary


def summarize_spreads_by_hour(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize spread behavior by operating hour."""
    if "timestamp" not in data.columns:
        raise ValueError("Input data must include timestamp for hourly spread analysis.")

    prepared = prepare_spread_data(data)
    summary = (
        prepared.groupby("operating_hour")
        .agg(
            interval_count=("da_rt_spread", "size"),
            average_spread=("da_rt_spread", "mean"),
            average_absolute_spread=("abs_da_rt_spread", "mean"),
            max_positive_spread=("da_rt_spread", "max"),
            max_negative_spread=("da_rt_spread", "min"),
        )
        .sort_values("average_absolute_spread", ascending=False)
        .reset_index()
    )
    return summary


def find_largest_spread_intervals(
    data: pd.DataFrame,
    limit: int = 10,
    use_absolute: bool = True,
) -> pd.DataFrame:
    """Return intervals with the largest spread values."""
    prepared = prepare_spread_data(data)
    sort_column = "abs_da_rt_spread" if use_absolute else "da_rt_spread"
    return prepared.sort_values(sort_column, ascending=False).head(limit).reset_index(drop=True)


def flag_spread_outliers(
    data: pd.DataFrame,
    absolute_threshold: float = 50.0,
) -> pd.DataFrame:
    """Return intervals where the absolute spread exceeds a selected threshold."""
    prepared = prepare_spread_data(data)
    outliers = prepared.loc[prepared["abs_da_rt_spread"] >= absolute_threshold].copy()
    return outliers.sort_values("abs_da_rt_spread", ascending=False).reset_index(drop=True)


def build_spread_summary_text(data: pd.DataFrame, absolute_threshold: float = 50.0) -> str:
    """Create a concise analyst-style written summary of DA/RT spreads."""
    if data.empty:
        return "No spread data is available for the selected filters."

    prepared = prepare_spread_data(data)
    spread_summary = summarize_spreads(prepared)
    largest = find_largest_spread_intervals(prepared, limit=1).iloc[0]
    outliers = flag_spread_outliers(prepared, absolute_threshold=absolute_threshold)

    settlement_phrase = ""
    if "settlement_point" in prepared.columns:
        top_point = summarize_spreads_by_settlement_point(prepared).iloc[0]
        settlement_phrase = (
            f" {top_point['settlement_point']} had the highest average absolute spread "
            f"at {_format_spread(top_point['average_absolute_spread'])}."
        )

    timestamp = largest["timestamp"] if "timestamp" in largest else "the selected period"
    return (
        f"The average DA/RT spread was {_format_spread(spread_summary['average_spread'])}, "
        f"with an average absolute spread of {_format_spread(spread_summary['average_absolute_spread'])}. "
        f"The largest market miss was {largest['spread_direction'].lower()} at {timestamp}, "
        f"with a spread of {_format_spread(largest['da_rt_spread'])}."
        f"{settlement_phrase} {len(outliers)} intervals exceeded the selected "
        f"absolute-spread threshold of {_format_spread(absolute_threshold)}."
    )
