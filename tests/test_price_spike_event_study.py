import pandas as pd

from src.analysis.price_spike_event_study import (
    build_event_window,
    build_price_spike_event_study_text,
    summarize_price_spike_events,
)


def sample_event_data():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-05-01 06:00:00",
                    "2026-05-01 07:00:00",
                    "2026-05-01 08:00:00",
                    "2026-05-01 09:00:00",
                    "2026-05-01 10:00:00",
                    "2026-05-01 08:00:00",
                ]
            ),
            "settlement_point": [
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "HB_NORTH",
                "LZ_HOUSTON",
            ],
            "real_time_price": [40.0, 55.0, 250.0, 95.0, 70.0, 175.0],
            "day_ahead_price": [45.0, 52.0, 90.0, 80.0, 75.0, 100.0],
            "da_rt_spread": [5.0, -3.0, -160.0, -15.0, 5.0, -75.0],
            "load_forecast_error_mw": [100.0, 200.0, 1200.0, 500.0, 250.0, 700.0],
        }
    )


def test_summarize_price_spike_events_returns_context_rows():
    events = summarize_price_spike_events(sample_event_data(), threshold=150.0)

    assert len(events) == 2
    assert events.loc[0, "settlement_point"] == "HB_NORTH"
    assert events.loc[0, "event_price"] == 250.0
    assert events.loc[0, "pre_event_avg_price"] == 47.5


def test_build_event_window_adds_relative_hour_and_event_flag():
    window = build_event_window(
        sample_event_data(),
        event_timestamp="2026-05-01 08:00:00",
        settlement_point="HB_NORTH",
        window_hours=1,
    )

    assert list(window["relative_hour"]) == [-1, 0, 1]
    assert window.loc[1, "is_event_interval"]


def test_build_price_spike_event_study_text_describes_top_event():
    text = build_price_spike_event_study_text(sample_event_data(), threshold=150.0)

    assert "highest mock-data price spike" in text
    assert "HB_NORTH" in text
    assert "$250.00/MWh" in text
