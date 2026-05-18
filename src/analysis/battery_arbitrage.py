"""Battery storage arbitrage simulation utilities."""

from __future__ import annotations

import math

import pandas as pd


REQUIRED_BATTERY_COLUMNS = {"timestamp", "settlement_point", "real_time_price"}


def _validate_price_data(data: pd.DataFrame) -> None:
    missing = REQUIRED_BATTERY_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required battery arbitrage columns: {sorted(missing)}")


def _format_currency(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def prepare_battery_price_series(
    data: pd.DataFrame,
    settlement_point: str = "HB_NORTH",
) -> pd.DataFrame:
    """Return an hourly price series for one settlement point."""
    _validate_price_data(data)
    prepared = data.copy()
    prepared["timestamp"] = pd.to_datetime(prepared["timestamp"])
    prepared = prepared.loc[prepared["settlement_point"] == settlement_point].copy()

    if prepared.empty:
        raise ValueError(f"No rows found for settlement point: {settlement_point}")

    return prepared.sort_values("timestamp").reset_index(drop=True)


def simulate_battery_arbitrage(
    data: pd.DataFrame,
    settlement_point: str = "HB_NORTH",
    capacity_mwh: float = 100.0,
    power_mw: float = 50.0,
    round_trip_efficiency: float = 0.86,
    initial_state_of_charge_mwh: float | None = None,
    charge_quantile: float = 0.30,
    discharge_quantile: float = 0.75,
) -> pd.DataFrame:
    """Simulate a simple price-threshold battery arbitrage strategy.

    The model is intentionally transparent for portfolio use: charge during
    lower-price intervals, discharge during higher-price intervals, and hold
    otherwise. It is not a production storage optimizer.
    """
    if capacity_mwh <= 0:
        raise ValueError("capacity_mwh must be positive.")
    if power_mw <= 0:
        raise ValueError("power_mw must be positive.")
    if not 0 < round_trip_efficiency <= 1:
        raise ValueError("round_trip_efficiency must be greater than 0 and less than or equal to 1.")
    if not 0 <= charge_quantile < discharge_quantile <= 1:
        raise ValueError("charge_quantile must be lower than discharge_quantile, both between 0 and 1.")

    prices = prepare_battery_price_series(data, settlement_point)
    charge_price = float(prices["real_time_price"].quantile(charge_quantile))
    discharge_price = float(prices["real_time_price"].quantile(discharge_quantile))
    charge_efficiency = math.sqrt(round_trip_efficiency)
    discharge_efficiency = math.sqrt(round_trip_efficiency)
    state_of_charge = (
        min(max(initial_state_of_charge_mwh, 0.0), capacity_mwh)
        if initial_state_of_charge_mwh is not None
        else capacity_mwh / 2
    )

    rows = []
    for row in prices.itertuples(index=False):
        action = "Hold"
        charge_from_grid_mwh = 0.0
        discharge_to_grid_mwh = 0.0
        interval_margin = 0.0

        if row.real_time_price <= charge_price and state_of_charge < capacity_mwh:
            action = "Charge"
            energy_added_to_battery = min(power_mw, capacity_mwh - state_of_charge)
            charge_from_grid_mwh = energy_added_to_battery / charge_efficiency
            state_of_charge += energy_added_to_battery
            interval_margin = -charge_from_grid_mwh * row.real_time_price
        elif row.real_time_price >= discharge_price and state_of_charge > 0:
            action = "Discharge"
            energy_removed_from_battery = min(power_mw, state_of_charge)
            discharge_to_grid_mwh = energy_removed_from_battery * discharge_efficiency
            state_of_charge -= energy_removed_from_battery
            interval_margin = discharge_to_grid_mwh * row.real_time_price

        rows.append(
            {
                "timestamp": row.timestamp,
                "settlement_point": row.settlement_point,
                "real_time_price": row.real_time_price,
                "action": action,
                "charge_from_grid_mwh": charge_from_grid_mwh,
                "discharge_to_grid_mwh": discharge_to_grid_mwh,
                "state_of_charge_mwh": state_of_charge,
                "interval_margin": interval_margin,
                "charge_price_threshold": charge_price,
                "discharge_price_threshold": discharge_price,
            }
        )

    return pd.DataFrame(rows)


def summarize_battery_arbitrage(dispatch: pd.DataFrame) -> dict[str, float]:
    """Return summary metrics for simulated battery dispatch."""
    required = {
        "action",
        "charge_from_grid_mwh",
        "discharge_to_grid_mwh",
        "state_of_charge_mwh",
        "interval_margin",
    }
    missing = required - set(dispatch.columns)
    if missing:
        raise ValueError(f"Missing required dispatch columns: {sorted(missing)}")

    discharge_rows = dispatch.loc[dispatch["action"] == "Discharge"]
    charge_rows = dispatch.loc[dispatch["action"] == "Charge"]
    capacity_proxy = max(dispatch["state_of_charge_mwh"].max(), 1.0)

    return {
        "gross_margin": float(dispatch["interval_margin"].sum()),
        "charge_intervals": int((dispatch["action"] == "Charge").sum()),
        "discharge_intervals": int((dispatch["action"] == "Discharge").sum()),
        "total_charge_mwh": float(dispatch["charge_from_grid_mwh"].sum()),
        "total_discharge_mwh": float(dispatch["discharge_to_grid_mwh"].sum()),
        "equivalent_cycles": float(dispatch["discharge_to_grid_mwh"].sum() / capacity_proxy),
        "average_charge_price": float(charge_rows["real_time_price"].mean()) if not charge_rows.empty else 0.0,
        "average_discharge_price": float(discharge_rows["real_time_price"].mean()) if not discharge_rows.empty else 0.0,
        "final_state_of_charge_mwh": float(dispatch["state_of_charge_mwh"].iloc[-1]),
    }


def build_battery_arbitrage_summary_text(dispatch: pd.DataFrame) -> str:
    """Create concise analyst-style commentary for a battery dispatch run."""
    if dispatch.empty:
        return "No battery dispatch results are available."

    summary = summarize_battery_arbitrage(dispatch)
    top_interval = dispatch.sort_values("interval_margin", ascending=False).iloc[0]

    return (
        "The mock battery arbitrage run produced "
        f"{_format_currency(summary['gross_margin'])} of gross margin across "
        f"{summary['charge_intervals']} charge intervals and {summary['discharge_intervals']} discharge intervals. "
        f"The strongest discharge interval occurred at {top_interval['settlement_point']} on "
        f"{top_interval['timestamp']} with a real-time price of "
        f"${top_interval['real_time_price']:.2f}/MWh. "
        "This is a simple threshold strategy for portfolio demonstration, not a production bid optimizer."
    )
