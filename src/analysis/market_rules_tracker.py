"""ERCOT market rules tracker utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_RULE_COLUMNS = {
    "rule_id",
    "title",
    "status",
    "next_step",
    "topic",
    "impact_area",
    "priority",
    "source_url",
    "last_checked",
    "analyst_note",
}

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def validate_rules_tracker(data: pd.DataFrame) -> None:
    """Validate required columns for a market rules tracker table."""
    missing = REQUIRED_RULE_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required market rules tracker columns: {sorted(missing)}")


def load_rules_tracker(path: str | Path) -> pd.DataFrame:
    """Load a market rules tracker CSV and prepare dates."""
    data = pd.read_csv(path)
    validate_rules_tracker(data)
    data["last_checked"] = pd.to_datetime(data["last_checked"])
    return data


def prepare_rules_tracker(data: pd.DataFrame) -> pd.DataFrame:
    """Return a clean tracker sorted by priority and rule id."""
    validate_rules_tracker(data)
    prepared = data.copy()
    prepared["last_checked"] = pd.to_datetime(prepared["last_checked"])
    prepared["priority_rank"] = prepared["priority"].map(PRIORITY_ORDER).fillna(99)
    return prepared.sort_values(["priority_rank", "rule_id"]).reset_index(drop=True)


def summarize_rules_by_status(data: pd.DataFrame) -> pd.DataFrame:
    """Count tracked rules by current status."""
    prepared = prepare_rules_tracker(data)
    return (
        prepared.groupby("status")
        .agg(rule_count=("rule_id", "size"), high_priority_count=("priority", lambda rows: (rows == "High").sum()))
        .sort_values(["high_priority_count", "rule_count"], ascending=False)
        .reset_index()
    )


def build_rules_watchlist(
    data: pd.DataFrame,
    priority: str | None = None,
    topic: str | None = None,
    limit: int = 5,
) -> pd.DataFrame:
    """Return a prioritized market rules watchlist."""
    prepared = prepare_rules_tracker(data)
    if priority:
        prepared = prepared.loc[prepared["priority"].str.casefold() == priority.casefold()]
    if topic:
        prepared = prepared.loc[prepared["topic"].str.contains(topic, case=False, na=False)]

    return prepared.head(limit).drop(columns=["priority_rank"]).reset_index(drop=True)


def build_rules_tracker_summary_text(data: pd.DataFrame) -> str:
    """Create concise analyst-style commentary for the tracker."""
    if data.empty:
        return "No market rules are currently tracked."

    prepared = prepare_rules_tracker(data)
    high_priority = prepared.loc[prepared["priority"] == "High"]
    top_rule = prepared.iloc[0]

    return (
        f"The sample ERCOT rules tracker contains {len(prepared)} items, including "
        f"{len(high_priority)} high-priority watchlist items. The first item to review is "
        f"{top_rule['rule_id']}: {top_rule['title']}. The analyst note is: "
        f"{top_rule['analyst_note']} Status and next-step fields should be verified against ERCOT "
        "source pages before publication or interview use."
    )
