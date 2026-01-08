# config.py
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_FILE = PROJECT_ROOT / "instagram_conversations.xlsx"

REPORTS_DIR = PROJECT_ROOT / "reports"
DAILY_REPORTS = REPORTS_DIR / "daily"
PRIORITY_REPORTS = REPORTS_DIR / "priority"
WEEKLY_REPORTS = REPORTS_DIR / "weekly"

ARCHIVE_DIR = PROJECT_ROOT / "archive"
LOGS_DIR = PROJECT_ROOT / "logs"

REQUIRED_COLUMNS = ['username', 'message', 'date']

INTENT_THRESHOLDS = {
    'very_high': 0.8,
    'high': 0.6,
    'medium': 0.4,
    'low': 0.0
}

def setup_directories():
    for d in [DAILY_REPORTS, PRIORITY_REPORTS, WEEKLY_REPORTS, ARCHIVE_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    return True