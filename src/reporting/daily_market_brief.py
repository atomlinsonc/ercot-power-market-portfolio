"""Generate a simple daily market brief from dashboard data."""

from __future__ import annotations

import pandas as pd

from src.analysis.market_summary import build_market_summary
from src.analysis.price_spike_detection import detect_price_spikes


def generate_daily_market_brief(data: pd.DataFrame, threshold: float = 150) -> str:
    """Return a Markdown market brief for the supplied dataset."""
    summary = build_market_summary(data, threshold)
    spikes = detect_price_spikes(data, threshold).head(5)

    spike_lines = [
        f"- {row.timestamp}: {row.settlement_point} at ${row.real_time_price:.2f}/MWh"
        for row in spikes.itertuples(index=False)
    ]
    if not spike_lines:
        spike_lines = ["- No intervals exceeded the selected threshold."]

    latest_date = pd.to_datetime(data["timestamp"]).max().date() if not data.empty else "N/A"

    return "\n".join(
        [
            "# ERCOT Daily Market Brief",
            "",
            f"Date: {latest_date}",
            "",
            "Mock-data notice: This generated brief uses mock ERCOT-style data until live data is connected.",
            "",
            "## Executive Summary",
            "",
            summary,
            "",
            "## Price Spike Alerts",
            "",
            *spike_lines,
            "",
            "## Items to Watch",
            "",
            "- Compare spike intervals across hubs and load zones.",
            "- Review large negative DA/RT spreads where real-time exceeded day-ahead.",
            "- Check whether actual load exceeded forecast during high-price intervals.",
        ]
    )

