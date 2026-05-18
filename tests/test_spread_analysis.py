import pandas as pd

from src.analysis.spread_analysis import (
    add_spread_columns,
    build_spread_summary_text,
    find_largest_spread_intervals,
    flag_spread_outliers,
    prepare_spread_data,
    summarize_spreads_by_hour,
    summarize_spreads_by_settlement_point,
)


def sample_spread_data():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-05-01 16:00:00",
                    "2026-05-01 17:00:00",
                    "2026-05-01 18:00:00",
                    "2026-05-01 18:00:00",
                ]
            ),
            "settlement_point": ["HB_NORTH", "HB_NORTH", "HB_NORTH", "LZ_HOUSTON"],
            "day_ahead_price": [55.0, 65.0, 80.0, 70.0],
            "real_time_price": [50.0, 95.0, 200.0, 40.0],
        }
    )


def test_add_spread_columns_uses_day_ahead_minus_real_time():
    result = add_spread_columns(sample_spread_data())

    assert result.loc[0, "da_rt_spread"] == 5.0
    assert result.loc[2, "da_rt_spread"] == -120.0
    assert result.loc[2, "abs_da_rt_spread"] == 120.0


def test_prepare_spread_data_adds_hour_and_direction():
    result = prepare_spread_data(sample_spread_data())

    assert result.loc[1, "operating_hour"] == 17
    assert result.loc[1, "spread_direction"] == "Real-time premium"
    assert result.loc[3, "spread_direction"] == "Day-ahead premium"


def test_summarize_spreads_by_settlement_point_ranks_by_abs_spread():
    summary = summarize_spreads_by_settlement_point(sample_spread_data())

    assert summary.loc[0, "settlement_point"] == "HB_NORTH"
    assert summary.loc[0, "interval_count"] == 3


def test_summarize_spreads_by_hour_ranks_evening_market_miss():
    summary = summarize_spreads_by_hour(sample_spread_data())

    assert summary.loc[0, "operating_hour"] == 18


def test_find_largest_spread_intervals_uses_absolute_spread_by_default():
    largest = find_largest_spread_intervals(sample_spread_data(), limit=1)

    assert largest.loc[0, "da_rt_spread"] == -120.0


def test_flag_spread_outliers_filters_on_absolute_threshold():
    outliers = flag_spread_outliers(sample_spread_data(), absolute_threshold=50.0)

    assert len(outliers) == 1
    assert outliers.loc[0, "settlement_point"] == "HB_NORTH"


def test_build_spread_summary_text_mentions_threshold_count():
    summary = build_spread_summary_text(sample_spread_data(), absolute_threshold=50.0)

    assert "average DA/RT spread" in summary
    assert "1 intervals exceeded" in summary
