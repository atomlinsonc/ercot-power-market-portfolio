"""Load forecast error analysis."""

from __future__ import annotations

import pandas as pd


def add_load_forecast_error(data: pd.DataFrame) -> pd.DataFrame:
    """Add load forecast error as actual load minus forecast load."""
    required = {"actual_load_mw", "forecast_load_mw"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required load columns: {sorted(missing)}")

    result = data.copy()
    result["load_forecast_error_mw"] = result["actual_load_mw"] - result["forecast_load_mw"]
    return result


def summarize_load_error(data: pd.DataFrame) -> dict[str, float]:
    """Return key load forecast error summary statistics."""
    if "load_forecast_error_mw" not in data.columns:
        data = add_load_forecast_error(data)

    return {
        "average_error_mw": float(data["load_forecast_error_mw"].mean()),
        "max_error_mw": float(data["load_forecast_error_mw"].max()),
        "min_error_mw": float(data["load_forecast_error_mw"].min()),
        "mean_absolute_error_mw": float(data["load_forecast_error_mw"].abs().mean()),
    }

