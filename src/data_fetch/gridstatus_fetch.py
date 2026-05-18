"""Optional GridStatus integration boundary."""

from __future__ import annotations

import pandas as pd


def fetch_gridstatus_ercot_prices(*, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch ERCOT market data through GridStatus when configured.

    The first portfolio milestone does not depend on GridStatus. This function is
    a future integration point for public-data access.
    """
    try:
        import gridstatus  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "gridstatus is not installed. Install requirements.txt before using "
            "this optional data source."
        ) from exc

    raise NotImplementedError(
        "GridStatus integration is planned but not implemented in this milestone."
    )

