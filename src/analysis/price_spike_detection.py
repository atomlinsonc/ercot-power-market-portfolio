"""Price-spike detection utilities."""

from __future__ import annotations

import pandas as pd


def detect_price_spikes(data: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Return intervals where real-time price is at or above the threshold."""
    if "real_time_price" not in data.columns:
        raise ValueError("Input data must include real_time_price.")

    spikes = data.loc[data["real_time_price"] >= threshold].copy()
    return spikes.sort_values("real_time_price", ascending=False).reset_index(drop=True)


def count_price_spikes(data: pd.DataFrame, threshold: float) -> int:
    """Count price intervals at or above the selected threshold."""
    return int((data["real_time_price"] >= threshold).sum())

