import pandas as pd

from src.analysis.price_spike_detection import count_price_spikes, detect_price_spikes


def test_detect_price_spikes_returns_rows_above_threshold_sorted_descending():
    data = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-05-01 00:00:00", "2026-05-01 01:00:00", "2026-05-01 02:00:00"]
            ),
            "real_time_price": [40, 300, 175],
        }
    )

    spikes = detect_price_spikes(data, threshold=150)

    assert len(spikes) == 2
    assert spikes.loc[0, "real_time_price"] == 300
    assert count_price_spikes(data, threshold=150) == 2

