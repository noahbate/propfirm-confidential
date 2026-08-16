import json
from pathlib import Path
from datetime import datetime
from typing import Any

PREFERENCES_PATH = Path(__file__).resolve().parents[1] / "user_preferences.json"


def _load_preferences() -> dict:
    if not PREFERENCES_PATH.exists():
        return {"users": {}}
    with open(PREFERENCES_PATH, "r") as f:
        return json.load(f)


def _save_preferences(data: dict) -> None:
    PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFERENCES_PATH, "w") as f:
        json.dump(data, f, indent=2)
