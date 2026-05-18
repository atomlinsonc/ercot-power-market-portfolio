"""Market summary helpers for dashboards and written briefs."""

from __future__ import annotations

import pandas as pd

from src.analysis.price_spike_detection import detect_price_spikes
from src.analysis.spread_analysis import summarize_spreads


def build_market_summary(data: pd.DataFrame, threshold: float) -> str:
    """Create a short desk-style written summary for filtered data."""
    if data.empty:
        return "No market data is available for the selected filters."

    spikes = detect_price_spikes(data, threshold)
    spread_summary = summarize_spreads(data)
    spike_count = len(spikes)

    if spike_count:
        largest = spikes.iloc[0]
        spike_sentence = (
            f"Real-time prices exceeded the selected threshold during {spike_count} intervals. "
            f"The largest spike occurred at {largest['timestamp']} with a price of "
            f"${largest['real_time_price']:.2f}/MWh."
        )
    else:
        spike_sentence = (
            f"Real-time prices did not exceed the selected threshold of "
            f"${threshold:.2f}/MWh during the selected period."
        )

    return (
        f"{spike_sentence} The average DA/RT spread was "
        f"${spread_summary['average_spread']:.2f}/MWh, calculated as day-ahead minus real-time."
    )

