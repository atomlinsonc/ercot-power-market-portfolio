"""Streamlit dashboard for ERCOT real-time market analytics."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.market_summary import build_market_summary
from src.analysis.price_spike_detection import detect_price_spikes
from src.config import SAMPLE_MARKET_DATA_PATH
from src.data_fetch.sample_data_generator import write_sample_market_data


st.set_page_config(
    page_title="ERCOT Real-Time Market Dashboard",
    layout="wide",
)


@st.cache_data
def load_market_data(path: str) -> pd.DataFrame:
    """Load dashboard data, generating sample data when needed."""
    data_path = Path(path)
    if not data_path.exists():
        write_sample_market_data(data_path)

    data = pd.read_csv(data_path, parse_dates=["timestamp"])
    data["date"] = data["timestamp"].dt.date
    return data


def filter_data(
    data: pd.DataFrame,
    settlement_point: str,
    start_date,
    end_date,
) -> pd.DataFrame:
    """Apply settlement point and date filters."""
    mask = (
        (data["settlement_point"] == settlement_point)
        & (data["date"] >= start_date)
        & (data["date"] <= end_date)
    )
    return data.loc[mask].sort_values("timestamp").reset_index(drop=True)


data = load_market_data(str(SAMPLE_MARKET_DATA_PATH))

st.title("ERCOT Real-Time Market Dashboard")
st.caption(
    "Mock ERCOT-style data for portfolio development. Live public ERCOT/GridStatus integration is a future milestone."
)

with st.sidebar:
    st.header("Dashboard Controls")
    settlement_point = st.selectbox(
        "Hub / load zone",
        sorted(data["settlement_point"].unique()),
        index=sorted(data["settlement_point"].unique()).index("HB_NORTH"),
    )
    min_date = data["date"].min()
    max_date = data["date"].max()
    selected_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        start_date, end_date = selected_range
    else:
        start_date = end_date = selected_range

    spike_threshold = st.slider(
        "Price spike threshold ($/MWh)",
        min_value=50,
        max_value=500,
        value=150,
        step=10,
    )

filtered = filter_data(data, settlement_point, start_date, end_date)

if filtered.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()

latest_price = filtered.iloc[-1]["real_time_price"]
average_price = filtered["real_time_price"].mean()
max_price = filtered["real_time_price"].max()
spikes = detect_price_spikes(filtered, spike_threshold)

metric_cols = st.columns(4)
metric_cols[0].metric("Latest RT Price", f"${latest_price:,.2f}/MWh")
metric_cols[1].metric("Average RT Price", f"${average_price:,.2f}/MWh")
metric_cols[2].metric("Max RT Price", f"${max_price:,.2f}/MWh")
metric_cols[3].metric("Spike Intervals", f"{len(spikes):,}")

st.subheader("Market Summary")
st.info(build_market_summary(filtered, spike_threshold))

price_chart = px.line(
    filtered,
    x="timestamp",
    y="real_time_price",
    title=f"Real-Time Price Over Time: {settlement_point}",
    labels={
        "timestamp": "Timestamp",
        "real_time_price": "Real-Time Price ($/MWh)",
    },
)
price_chart.add_hline(
    y=spike_threshold,
    line_dash="dash",
    line_color="red",
    annotation_text="Spike threshold",
)
st.plotly_chart(price_chart, use_container_width=True)

chart_cols = st.columns(2)

with chart_cols[0]:
    comparison = filtered.melt(
        id_vars=["timestamp"],
        value_vars=["day_ahead_price", "real_time_price"],
        var_name="market",
        value_name="price",
    )
    comparison["market"] = comparison["market"].map(
        {
            "day_ahead_price": "Day-Ahead",
            "real_time_price": "Real-Time",
        }
    )
    da_rt_chart = px.line(
        comparison,
        x="timestamp",
        y="price",
        color="market",
        title="Day-Ahead vs Real-Time Price",
        labels={"timestamp": "Timestamp", "price": "Price ($/MWh)", "market": "Market"},
    )
    st.plotly_chart(da_rt_chart, use_container_width=True)

with chart_cols[1]:
    spread_chart = px.bar(
        filtered,
        x="timestamp",
        y="da_rt_spread",
        title="DA/RT Spread Over Time",
        labels={
            "timestamp": "Timestamp",
            "da_rt_spread": "DA minus RT Spread ($/MWh)",
        },
    )
    st.plotly_chart(spread_chart, use_container_width=True)

load_chart = px.line(
    filtered.melt(
        id_vars=["timestamp"],
        value_vars=["forecast_load_mw", "actual_load_mw"],
        var_name="load_type",
        value_name="load_mw",
    ).assign(
        load_type=lambda frame: frame["load_type"].map(
            {
                "forecast_load_mw": "Forecast Load",
                "actual_load_mw": "Actual Load",
            }
        )
    ),
    x="timestamp",
    y="load_mw",
    color="load_type",
    title="Load Forecast vs Actual Load",
    labels={"timestamp": "Timestamp", "load_mw": "Load (MW)", "load_type": "Load Type"},
)
st.plotly_chart(load_chart, use_container_width=True)

st.subheader("Price Spike Alerts")
if spikes.empty:
    st.success("No intervals exceeded the selected price threshold.")
else:
    st.dataframe(
        spikes[
            [
                "timestamp",
                "settlement_point",
                "real_time_price",
                "day_ahead_price",
                "da_rt_spread",
                "forecast_load_mw",
                "actual_load_mw",
                "load_forecast_error_mw",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
