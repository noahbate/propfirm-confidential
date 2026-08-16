from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USERS_PATH = Path(__file__).resolve().parents[1] / "user_accounts.json"
SESSIONS_PATH = Path(__file__).resolve().parents[1] / "user_sessions.json"


def _load(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def _save(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_users() -> dict[str, dict]:
    return _load(USERS_PATH)


def save_users(data: dict[str, dict]) -> None:
    _save(USERS_PATH, data)


def load_sessions() -> dict[str, dict]:
    return _load(SESSIONS_PATH)


def save_sessions(data: dict[str, dict]) -> None:
    _save(SESSIONS_PATH, data)


def create_session(user_id: str) -> str:
    token = uuid.uuid4().hex
    sessions = load_sessions()
    sessions[token] = {
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_sessions(sessions)
    return token


def invalidate_session(token: str) -> None:
    sessions = load_sessions()
    sessions.pop(token, None)
    save_sessions(sessions)


def user_id_from_token(token: str | None) -> str | None:
    if not token:
        return None
    sessions = load_sessions()
    rec = sessions.get(token)
    if not rec:
        return None
    return rec.get("user_id")
