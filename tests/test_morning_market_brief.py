import pandas as pd

from src.reporting.morning_market_brief import (
    build_items_to_watch,
    generate_morning_market_brief,
    summarize_settlement_points,
)


def sample_market_data():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-05-01 07:00:00", "2026-05-01 08:00:00", "2026-05-01 09:00:00"]
            ),
            "settlement_point": ["HB_NORTH", "HB_NORTH", "LZ_HOUSTON"],
            "real_time_price": [45.0, 225.0, 80.0],
            "day_ahead_price": [50.0, 90.0, 75.0],
            "da_rt_spread": [5.0, -135.0, -5.0],
            "forecast_load_mw": [51000.0, 52000.0, 51500.0],
            "actual_load_mw": [51200.0, 53300.0, 51100.0],
            "load_forecast_error_mw": [200.0, 1300.0, -400.0],
        }
    )


def test_summarize_settlement_points_ranks_by_max_real_time_price():
    summary = summarize_settlement_points(sample_market_data())

    assert summary.loc[0, "settlement_point"] == "HB_NORTH"
    assert summary.loc[0, "max_real_time_price"] == 225.0


def test_build_items_to_watch_mentions_spike_and_load_error():
    items = build_items_to_watch(sample_market_data(), threshold=150.0)

    assert any("HB_NORTH" in item for item in items)
    assert any("1,300 MW" in item for item in items)


def test_generate_morning_market_brief_includes_required_sections():
    brief = generate_morning_market_brief(sample_market_data(), threshold=150.0)

    assert "# ERCOT Morning Market Brief" in brief
    assert "Mock-data notice" in brief
    assert "## Price Spike Alerts" in brief
    assert "HB_NORTH" in brief
