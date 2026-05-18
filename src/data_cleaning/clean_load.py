"""Cleaning helpers for load forecast data."""

from __future__ import annotations

import pandas as pd


REQUIRED_LOAD_COLUMNS = {
    "forecast_load_mw",
    "actual_load_mw",
}


def clean_load_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean load forecast columns."""
    missing = REQUIRED_LOAD_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required load columns: {sorted(missing)}")

    cleaned = data.copy()
    cleaned["forecast_load_mw"] = pd.to_numeric(cleaned["forecast_load_mw"], errors="coerce")
    cleaned["actual_load_mw"] = pd.to_numeric(cleaned["actual_load_mw"], errors="coerce")
    cleaned["load_forecast_error_mw"] = cleaned["actual_load_mw"] - cleaned["forecast_load_mw"]
    return cleaned.dropna(subset=["forecast_load_mw", "actual_load_mw"]).reset_index(drop=True)

