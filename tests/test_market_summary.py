import pandas as pd

from src.analysis.market_summary import build_market_summary


def test_build_market_summary_mentions_spike_count_and_average_spread():
    data = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-05-01 00:00:00", "2026-05-01 01:00:00"]),
            "settlement_point": ["HB_NORTH", "HB_NORTH"],
            "real_time_price": [45.0, 200.0],
            "day_ahead_price": [50.0, 100.0],
            "da_rt_spread": [5.0, -100.0],
        }
    )

    summary = build_market_summary(data, threshold=150)

    assert "1 intervals" in summary
    assert "average DA/RT spread" in summary

