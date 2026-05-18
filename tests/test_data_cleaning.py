import pandas as pd

from src.data_cleaning.clean_load import clean_load_data
from src.data_cleaning.clean_prices import clean_price_data


def test_clean_price_data_adds_spread_and_normalizes_point():
    data = pd.DataFrame(
        {
            "timestamp": ["2026-05-01 00:00:00"],
            "settlement_point": [" hb_north "],
            "real_time_price": ["55.5"],
            "day_ahead_price": ["50.0"],
        }
    )

    cleaned = clean_price_data(data)

    assert cleaned.loc[0, "settlement_point"] == "HB_NORTH"
    assert cleaned.loc[0, "da_rt_spread"] == -5.5


def test_clean_load_data_adds_forecast_error():
    data = pd.DataFrame(
        {
            "forecast_load_mw": [50000],
            "actual_load_mw": [51250],
        }
    )

    cleaned = clean_load_data(data)

    assert cleaned.loc[0, "load_forecast_error_mw"] == 1250

