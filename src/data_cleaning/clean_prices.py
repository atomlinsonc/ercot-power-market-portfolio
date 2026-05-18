"""Cleaning helpers for ERCOT-style price data."""

from __future__ import annotations

import pandas as pd


REQUIRED_PRICE_COLUMNS = {
    "timestamp",
    "settlement_point",
    "real_time_price",
    "day_ahead_price",
}


def clean_price_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean price data used by the dashboard."""
    missing = REQUIRED_PRICE_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required price columns: {sorted(missing)}")

    cleaned = data.copy()
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"])
    cleaned["settlement_point"] = cleaned["settlement_point"].astype(str).str.upper().str.strip()
    cleaned["real_time_price"] = pd.to_numeric(cleaned["real_time_price"], errors="coerce")
    cleaned["day_ahead_price"] = pd.to_numeric(cleaned["day_ahead_price"], errors="coerce")
    cleaned["da_rt_spread"] = cleaned["day_ahead_price"] - cleaned["real_time_price"]
    cleaned = cleaned.dropna(subset=["timestamp", "settlement_point", "real_time_price", "day_ahead_price"])
    return cleaned.sort_values(["settlement_point", "timestamp"]).reset_index(drop=True)

