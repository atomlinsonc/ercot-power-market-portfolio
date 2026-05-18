"""Placeholder ERCOT public-data integration helpers.

This module intentionally avoids pretending that live data is already wired up.
The functions define the interface expected by the rest of the project so public
ERCOT data sources can be added cleanly in a later milestone.
"""

from __future__ import annotations

import pandas as pd


def fetch_ercot_real_time_prices(*, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch ERCOT real-time price data.

    Parameters are included now so the dashboard and analysis code can call a
    stable interface once live public-data access is implemented.
    """
    raise NotImplementedError(
        "Live ERCOT price fetching is not implemented yet. Use the sample data "
        "generator or optional GridStatus integration during early development."
    )


def fetch_ercot_load_forecast(*, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch ERCOT load forecast and actual load data."""
    raise NotImplementedError(
        "Live ERCOT load fetching is not implemented yet. This placeholder keeps "
        "the future data-source boundary explicit."
    )

