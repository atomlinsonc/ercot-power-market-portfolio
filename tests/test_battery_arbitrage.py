import pandas as pd

from src.analysis.battery_arbitrage import (
    build_battery_arbitrage_summary_text,
    prepare_battery_price_series,
    simulate_battery_arbitrage,
    summarize_battery_arbitrage,
)


def sample_battery_data():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-05-01 00:00:00",
                    "2026-05-01 01:00:00",
                    "2026-05-01 02:00:00",
                    "2026-05-01 03:00:00",
                    "2026-05-01 04:00:00",
                    "2026-05-01 00:00:00",
                ]
            ),
            "settlement_point": [
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "HB_HOUSTON",
            ],
            "real_time_price": [20.0, 18.0, 65.0, 120.0, 35.0, 90.0],
        }
    )


def test_prepare_battery_price_series_filters_one_settlement_point():
    series = prepare_battery_price_series(sample_battery_data(), settlement_point="HB_NORTH")

    assert len(series) == 5
    assert series["settlement_point"].nunique() == 1


def test_simulate_battery_arbitrage_creates_dispatch_rows():
    dispatch = simulate_battery_arbitrage(
        sample_battery_data(),
        settlement_point="HB_NORTH",
        capacity_mwh=100.0,
        power_mw=50.0,
        round_trip_efficiency=0.90,
    )

    assert len(dispatch) == 5
    assert "Charge" in set(dispatch["action"])
    assert "Discharge" in set(dispatch["action"])
    assert dispatch["state_of_charge_mwh"].between(0, 100).all()


def test_summarize_battery_arbitrage_reports_margin_and_intervals():
    dispatch = simulate_battery_arbitrage(sample_battery_data(), settlement_point="HB_NORTH")
    summary = summarize_battery_arbitrage(dispatch)

    assert summary["discharge_intervals"] >= 1
    assert summary["charge_intervals"] >= 1
    assert "gross_margin" in summary


def test_build_battery_arbitrage_summary_text_labels_mock_strategy():
    dispatch = simulate_battery_arbitrage(sample_battery_data(), settlement_point="HB_NORTH")
    text = build_battery_arbitrage_summary_text(dispatch)

    assert "mock battery arbitrage run" in text
    assert "not a production bid optimizer" in text
