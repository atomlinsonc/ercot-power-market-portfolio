"""Price-spike event-study utilities."""

from __future__ import annotations

import pandas as pd

from src.analysis.price_spike_detection import detect_price_spikes


REQUIRED_EVENT_COLUMNS = {
    "timestamp",
    "settlement_point",
    "real_time_price",
    "day_ahead_price",
    "da_rt_spread",
    "load_forecast_error_mw",
}


def _validate_event_data(data: pd.DataFrame) -> None:
    missing = REQUIRED_EVENT_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required price-spike event columns: {sorted(missing)}")


def _format_currency(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):.2f}/MWh"


def summarize_price_spike_events(
    data: pd.DataFrame,
    threshold: float = 150.0,
    limit: int = 10,
) -> pd.DataFrame:
    """Return one row per spike interval with context fields."""
    _validate_event_data(data)
    prepared = data.copy()
    prepared["timestamp"] = pd.to_datetime(prepared["timestamp"])

    spikes = detect_price_spikes(prepared, threshold).head(limit).copy()
    if spikes.empty:
        return pd.DataFrame(
            columns=[
                "event_id",
                "event_timestamp",
                "settlement_point",
                "event_price",
                "day_ahead_price",
                "da_rt_spread",
                "load_forecast_error_mw",
                "pre_event_avg_price",
                "post_event_avg_price",
            ]
        )

    rows = []
    for event_id, spike in enumerate(spikes.itertuples(index=False), start=1):
        point_rows = prepared.loc[prepared["settlement_point"] == spike.settlement_point]
        pre_rows = point_rows.loc[
            (point_rows["timestamp"] >= spike.timestamp - pd.Timedelta(hours=2))
            & (point_rows["timestamp"] < spike.timestamp)
        ]
        post_rows = point_rows.loc[
            (point_rows["timestamp"] > spike.timestamp)
            & (point_rows["timestamp"] <= spike.timestamp + pd.Timedelta(hours=2))
        ]

        rows.append(
            {
                "event_id": event_id,
                "event_timestamp": spike.timestamp,
                "settlement_point": spike.settlement_point,
                "event_price": spike.real_time_price,
                "day_ahead_price": spike.day_ahead_price,
                "da_rt_spread": spike.da_rt_spread,
                "load_forecast_error_mw": spike.load_forecast_error_mw,
                "pre_event_avg_price": pre_rows["real_time_price"].mean(),
                "post_event_avg_price": post_rows["real_time_price"].mean(),
            }
        )

    return pd.DataFrame(rows)


def build_event_window(
    data: pd.DataFrame,
    event_timestamp: str | pd.Timestamp,
    settlement_point: str,
    window_hours: int = 2,
) -> pd.DataFrame:
    """Return rows around a selected event for one settlement point."""
    _validate_event_data(data)
    prepared = data.copy()
    prepared["timestamp"] = pd.to_datetime(prepared["timestamp"])
    event_time = pd.to_datetime(event_timestamp)

    window = prepared.loc[
        (prepared["settlement_point"] == settlement_point)
        & (prepared["timestamp"] >= event_time - pd.Timedelta(hours=window_hours))
        & (prepared["timestamp"] <= event_time + pd.Timedelta(hours=window_hours))
    ].copy()
    window["relative_hour"] = ((window["timestamp"] - event_time).dt.total_seconds() / 3600).astype(int)
    window["is_event_interval"] = window["timestamp"].eq(event_time)
    return window.sort_values("timestamp").reset_index(drop=True)


def build_price_spike_event_study_text(data: pd.DataFrame, threshold: float = 150.0) -> str:
    """Create concise commentary for the highest price-spike event."""
    if data.empty:
        return "No market data is available for price-spike event study."

    events = summarize_price_spike_events(data, threshold=threshold, limit=1)
    if events.empty:
        return f"No real-time intervals exceeded the selected spike threshold of {_format_currency(threshold)}."

    event = events.iloc[0]
    return (
        f"The highest mock-data price spike occurred at {event['settlement_point']} on "
        f"{event['event_timestamp']} with a real-time price of {_format_currency(event['event_price'])}. "
        f"The DA/RT spread was {_format_currency(event['da_rt_spread'])}, which means the event can be "
        f"reviewed as a real-time premium when the value is negative. Load forecast error was "
        f"{event['load_forecast_error_mw']:,.0f} MW during the interval."
    )
