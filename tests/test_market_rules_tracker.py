import pandas as pd

from src.analysis.market_rules_tracker import (
    build_rules_tracker_summary_text,
    build_rules_watchlist,
    prepare_rules_tracker,
    summarize_rules_by_status,
)


def sample_rules_data():
    return pd.DataFrame(
        {
            "rule_id": ["NPRR1255", "NPRR1320", "NPRR1278"],
            "title": [
                "Introduction of Mitigation of ESRs",
                "Reserve Margin Reporting Changes",
                "Advanced Grid Support Service",
            ],
            "status": ["Pending", "Pending", "Committee review"],
            "next_step": ["PRS", "PRS", "PRS"],
            "topic": ["Energy Storage Resource", "Resource Adequacy", "Ancillary Services"],
            "impact_area": ["Battery dispatch", "Planning reserve margin", "Ancillary services"],
            "priority": ["High", "Medium", "High"],
            "source_url": [
                "https://www.ercot.com/mktrules/issues/NPRR1255",
                "https://www.ercot.com/mktrules/issues/NPRR1320",
                "https://www.ercot.com/mktrules/issues/NPRR1278",
            ],
            "last_checked": ["2026-05-18", "2026-05-18", "2026-05-18"],
            "analyst_note": [
                "Track potential implications for ESR offer behavior.",
                "Watch how capacity reporting changes market commentary.",
                "Monitor whether new service creates reporting or price context needs.",
            ],
        }
    )


def test_prepare_rules_tracker_sorts_high_priority_first():
    tracker = prepare_rules_tracker(sample_rules_data())

    assert tracker.loc[0, "priority"] == "High"
    assert "priority_rank" in tracker.columns


def test_summarize_rules_by_status_counts_items():
    summary = summarize_rules_by_status(sample_rules_data())

    assert summary["rule_count"].sum() == 3
    assert "high_priority_count" in summary.columns


def test_build_rules_watchlist_filters_priority_and_topic():
    watchlist = build_rules_watchlist(sample_rules_data(), priority="High", topic="storage")

    assert len(watchlist) == 1
    assert watchlist.loc[0, "rule_id"] == "NPRR1255"


def test_build_rules_tracker_summary_text_mentions_verification():
    text = build_rules_tracker_summary_text(sample_rules_data())

    assert "sample ERCOT rules tracker" in text
    assert "verified against ERCOT source pages" in text
