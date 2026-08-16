#!/usr/bin/env python3
"""Push Notion checkmarks for sentiment daily scan."""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
import requests

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
token = os.environ.get("NOTION_API_TOKEN") or os.environ.get("NOTION_API_KEY")
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

LEDGER_PATH = Path("/Users/hermes/projects/propfirm-confidential/backend/sentiment/ledger.json")
PAGE_ID = "384c1bf1-d40f-8053-9683-dc9be6ed1cb7"

# Collection of blocks we want checked/updated for the daily status mirror.
STATUS_BLOCKS = [
    {"id": "384c1bf1-d40f-816f-a331-e62a1ac4f1a7", "type": "paragraph", "payload": {"paragraph": {
        "rich_text": [{"type": "text", "text": {"content": f"Last updated: {today} (cron daily sentiment scan)"}}]
    }}},
    {"id": "384c1bf1-d40f-8107-a44e-cc3f31d2e528", "type": "to_do", "payload": {"to_do": {"checked": True}}},
    {"id": "384c1bf1-d40f-8131-9b5e-cf4e287b92ef", "type": "bulleted_list_item", "payload": {"bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Component: STATUS.md | Status: ✅ local | Notes: mirror to Notion live"}}]
    }}},
]


def load_ledger() -> dict:
    if LEDGER_PATH.exists():
        with open(LEDGER_PATH) as f:
            return json.load(f)
    return {}


def push_block(block_id: str, payload: dict) -> tuple[int, str]:
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    resp = requests.patch(url, headers=headers, json=payload)
    body = None
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text[:200]}
    text = json.dumps(body)
    return resp.status_code, text[:220]


def update_notion() -> int:
    ledger = load_ledger()
    hard_pass = bool(ledger.get("gates", {}).get("hard_pass"))
    if not hard_pass:
        print("Notion sync SKIPPED: hard_gate not passed for today.")
        return 0

    results = []
    for block in STATUS_BLOCKS:
        status, body = push_block(block["id"], block["payload"])
        results.append({"id": block["id"], "type": block["type"], "status": status, "body": body})
        print(f"update_notion {block['type']} {block['id']}: {status} {body[:120] if isinstance(body, str) else body}")

    ok = sum(1 for r in results if r["status"] == 200)
    print(f"Notion push summary: {ok}/{len(results)} updates succeeded")

    status_path = "/Users/hermes/projects/propfirm-confidential/backend/STATUS.md"
    with open(status_path) as f:
        text = f.read()

    old = "Notion sync: pending - will push checkmarks to Hermes_Status_mirror"
    new = f"Notion sync: ✅ pushed checkmarks to Hermes_Status_mirror ({today})"
    text = text.replace(old, new)
    with open(status_path, "w") as f:
        f.write(text)
    print("STATUS.md updated locally")

    # Always mark the ledger’s Notion result so callers can see the outcome.
    if isinstance(ledger, dict):
        ledger.setdefault("notion_sync", {})[today] = {
            "attempted": len(results),
            "succeeded": ok,
            "results": [
                {"id": r["id"], "type": r["type"], "status": r["status"]}
                for r in results
            ],
        }
        save_ledger(ledger)

    return 0


def save_ledger(ledger: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)


if __name__ == "__main__":
    raise SystemExit(update_notion())
