"""Day-ahead versus real-time spread analysis."""

from __future__ import annotations

import pandas as pd


def add_spread_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Add DA/RT spread fields using day-ahead minus real-time convention."""
    required = {"day_ahead_price", "real_time_price"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required spread columns: {sorted(missing)}")

    result = data.copy()
    result["da_rt_spread"] = result["day_ahead_price"] - result["real_time_price"]
    result["abs_da_rt_spread"] = result["da_rt_spread"].abs()
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

