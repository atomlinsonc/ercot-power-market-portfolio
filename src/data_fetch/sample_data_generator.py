"""Generate realistic mock ERCOT-style market data for dashboard development."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import SAMPLE_MARKET_DATA_PATH


SETTLEMENT_POINTS = [
    "HB_NORTH",
    "HB_HOUSTON",
    "HB_WEST",
    "HB_SOUTH",
    "LZ_AEN",
    "LZ_CPS",
    "LZ_HOUSTON",
    "LZ_NORTH",
    "LZ_SOUTH",
    "LZ_WEST",
]


POINT_PRICE_ADJUSTMENTS = {
    "HB_NORTH": 0,
    "HB_HOUSTON": 3,
    "HB_WEST": -4,
    "HB_SOUTH": 2,
    "LZ_AEN": 4,
    "LZ_CPS": 2,
    "LZ_HOUSTON": 5,
    "LZ_NORTH": 1,
    "LZ_SOUTH": 3,
    "LZ_WEST": -2,
}


def generate_sample_market_data(
    *,
    start: str = "2026-05-01 00:00:00",
    periods: int = 24 * 7,
    frequency: str = "h",
    seed: int = 42,
) -> pd.DataFrame:
    """Create hourly mock ERCOT-style market data for multiple settlement points."""
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range(start=start, periods=periods, freq=frequency)
    rows: list[dict[str, object]] = []

    spike_hours = {
        pd.Timestamp("2026-05-02 17:00:00"): 165,
        pd.Timestamp("2026-05-04 18:00:00"): 240,
        pd.Timestamp("2026-05-06 16:00:00"): 135,
        pd.Timestamp("2026-05-06 19:00:00"): 310,
    }

    for timestamp in timestamps:
        hour = timestamp.hour
        day_index = (timestamp.normalize() - timestamps[0].normalize()).days
        daily_shape = 18 * np.sin((hour - 8) / 24 * 2 * np.pi) + 12 * np.sin((hour - 15) / 24 * 2 * np.pi)
        heat_ramp = max(hour - 12, 0) * 1.8 if 12 <= hour <= 20 else 0
        base_rt_price = 38 + daily_shape + heat_ramp + rng.normal(0, 4)
        base_da_price = 40 + daily_shape * 0.65 + heat_ramp * 0.55 + rng.normal(0, 3)

        forecast_load = 51500 + 5200 * np.sin((hour - 9) / 24 * 2 * np.pi) + day_index * 220
        actual_load = forecast_load + rng.normal(0, 700)
        if hour in {16, 17, 18, 19}:
            actual_load += 900

        for point in SETTLEMENT_POINTS:
            point_adjustment = POINT_PRICE_ADJUSTMENTS[point]
            congestion_noise = rng.normal(0, 2.5)
            real_time_price = base_rt_price + point_adjustment + congestion_noise
            day_ahead_price = base_da_price + point_adjustment * 0.7 + rng.normal(0, 2)

            if timestamp in spike_hours:
                spike_multiplier = 1 + (POINT_PRICE_ADJUSTMENTS[point] / 40)
                real_time_price += spike_hours[timestamp] * spike_multiplier + rng.normal(0, 12)

            real_time_price = round(max(real_time_price, -20), 2)
            day_ahead_price = round(max(day_ahead_price, -10), 2)
            point_forecast_load = forecast_load + rng.normal(0, 120)
            point_actual_load = actual_load + rng.normal(0, 160)

            rows.append(
                {
                    "timestamp": timestamp,
                    "settlement_point": point,
                    "real_time_price": real_time_price,
                    "day_ahead_price": day_ahead_price,
                    "da_rt_spread": round(day_ahead_price - real_time_price, 2),
                    "forecast_load_mw": round(point_forecast_load, 0),
                    "actual_load_mw": round(point_actual_load, 0),
                    "load_forecast_error_mw": round(point_actual_load - point_forecast_load, 0),
                }
            )

    return pd.DataFrame(rows)


def write_sample_market_data(path: Path = SAMPLE_MARKET_DATA_PATH) -> Path:
    """Write the sample market data CSV used by the dashboard."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = generate_sample_market_data()
    data.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    output_path = write_sample_market_data()
    print(f"Wrote sample ERCOT-style market data to {output_path}")

