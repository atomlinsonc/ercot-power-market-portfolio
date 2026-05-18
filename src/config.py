"""Project configuration helpers."""

from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_MARKET_DATA_PATH = PROCESSED_DATA_DIR / "sample_ercot_market_data.csv"
SAMPLE_RULES_TRACKER_PATH = DATA_DIR / "sample" / "ercot_market_rules_tracker_sample.csv"


def load_environment() -> None:
    """Load local environment variables when a .env file is present."""
    load_dotenv(PROJECT_ROOT / ".env")
