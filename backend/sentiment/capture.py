#!/usr/bin/env python3
"""Weekly sentiment capture for Prop Firm Confidential.

For each firm in backend/prop_firms.json:
  - query X via xurl for mentions containing firm name + keywords
  - query replies to firm's official X handle
  - store raw results in backend/sentiment/raw/<slug>/<YYYY-MM-DD>.json
  - compute weekly snapshot in backend/sentiment/snapshots/<YYYY-MM-DD>.json
  - prune raw files older than 13 weeks when disk >= 75%
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# CONFIG
KEYWORDS = ["payout", "delay", "scam", "funded", "withdrawal", "withdraw", "denied", "complaint"]
SENTIMENT_DIR = Path("/Users/hermes/projects/propfirm-confidential/backend/sentiment")
RAW_DIR = SENTIMENT_DIR / "raw"
SNAP_DIR = SENTIMENT_DIR / "snapshots"
PROP_FIRMS_PATH = Path("/Users/hermes/projects/propfirm-confidential/backend/prop_firms.json")
MIN_WEEKS = 13
DISK_THRESHOLD = 0.75
LEDGER_PATH = SENTIMENT_DIR / "ledger.json"


def load_firms() -> list[dict[str, Any]]:
    with open(PROP_FIRMS_PATH) as f:
        return json.load(f)


def xurl_search(query: str, days: int = 7) -> dict[str, Any]:
    """Run xurl search and return parsed JSON."""
    cmd = ["xurl", "search", query, "-n", "20"]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        return json.loads(out)
    except subprocess.CalledProcessError as exc:
        return {"error": exc.output, "query": query}
    except json.JSONDecodeError:
        return {"error": "invalid_json", "query": query}


def prune_old_raw(firm_slug: str) -> None:
    """Remove raw files older than MIN_WEEKS, then enforce 75% disk usage cap."""
    firm_raw = RAW_DIR / firm_slug
    if not firm_raw.exists():
        return
    cutoff = datetime.utcnow() - timedelta(weeks=MIN_WEEKS)
    for path in sorted(firm_raw.glob("*.json")):
        try:
            date_str = path.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if file_date < cutoff:
            path.unlink()

    # Enforce disk cap
    try:
        stat = os.statvfs(str(SENTIMENT_DIR))
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bfree * stat.f_frsize
        used = total - free
        usage = used / total if total > 0 else 0
    except (AttributeError, OSError):
        usage = 0

    if usage >= DISK_THRESHOLD:
        all_files = sorted(RAW_DIR.rglob("*.json"), key=lambda p: p.stat().st_mtime)
        for old in all_files:
            if old.exists():
                old.unlink()
            try:
                st = os.statvfs(str(SENTIMENT_DIR))
                tot = st.f_blocks * st.f_frsize
                fr = st.f_bfree * st.f_frsize
                u = tot - fr
                us = u / tot if tot > 0 else 0
            except (AttributeError, OSError):
                us = 0
            if us < DISK_THRESHOLD * 0.9:
                break


def score_firm(raw: dict[str, Any]) -> dict[str, Any]:
    """Derive weekly snapshot from raw X search results."""
    mentions: list[dict[str, Any]] = []
    seen_ids = set()
    for q in raw.get("queries", []):
        result = q.get("result") or {}
        data = result.get("data")
        if isinstance(data, list):
            for m in data:
                m_id = m.get("id")
                if m_id and m_id not in seen_ids:
                    seen_ids.add(m_id)
                    mentions.append(m)
        elif isinstance(result.get("results"), list):
            for m in result["results"]:
                m_id = m.get("id")
                if m_id and m_id not in seen_ids:
                    seen_ids.add(m_id)
                    mentions.append(m)

    volume = len(mentions)
    sentiment = {"positive": 0, "neutral": 0, "negative": 0}
    flags: list[str] = []
    concerns: list[str] = []
    samples: list[dict[str, Any]] = []

    for m in mentions:
        text = (m.get("text") or m.get("content") or "").lower()
        if any(k in text for k in ["great", "fast payout", "reliable", "legit"]):
            sentiment["positive"] += 1
        elif any(k in text for k in ["delay", "scam", "denied", "complaint", "issue"]):
            sentiment["negative"] += 1
            if "delay" in text or "withdraw" in text:
                flags.append("payout_delay")
                concerns.append("withdrawal time")
            if "scam" in text or "denied" in text:
                flags.append("scam_flag")
        else:
            sentiment["neutral"] += 1
        if len(samples) < 5:
            samples.append({"id": m.get("id"), "text": m.get("text") or m.get("content")})

    # Deduplicate flags
    flags = sorted(set(flags))

    return {
        "firm_slug": raw.get("firm_slug"),
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "volume": volume,
        "sentiment": sentiment,
        "flags": flags,
        "top_concerns": sorted(set(concerns))[:5],
        "sample_tweets": samples,
    }


def load_ledger() -> dict[str, Any]:
    if LEDGER_PATH.exists():
        with open(LEDGER_PATH) as f:
            return json.load(f)
    return {
        "last_run": {"date": None, "status": None, "firm_count": 0, "flag_count": 0, "duration_seconds": None},
        "firm_state": {},
        "gates": {"soft_skip": False, "hard_pass": False, "last_check": None},
        "history": [],
    }


def save_ledger(ledger: dict[str, Any]) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)


def main() -> int:
    ledger = load_ledger()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    last_run_date = ledger.get("last_run", {}).get("date")

    # Soft gate: skip if already ran today
    if last_run_date == today:
        print(f"Soft gate: sentiment already captured for {today}, skipping.")
        return 0

    firms = load_firms()
    snapshots: list[dict[str, Any]] = []
    start = time.time()

    for firm in firms:
        slug = firm.get("firm_slug")
        name = firm.get("firm_information", {}).get("firm_name", slug)
        handle = firm.get("firm_information", {}).get("x_handle")
        queries = [f'"{name}" ({" OR ".join(KEYWORDS)})']
        if handle:
            queries.append(f"to:{handle} (payout OR delay OR scam)")

        raw_results: dict[str, Any] = {"firm_slug": slug, "queries": [], "generated_at": today}
        for q in queries:
            res = xurl_search(q)
            raw_results["queries"].append({"query": q, "result": res})

        firm_raw_dir = RAW_DIR / slug
        firm_raw_dir.mkdir(parents=True, exist_ok=True)
        with open(firm_raw_dir / f"{today}.json", "w") as f:
            json.dump(raw_results, f, indent=2)

        snapshot = score_firm(raw_results)
        snapshots.append(snapshot)

        if isinstance(ledger, dict):
            ledger.setdefault("firm_state", {})
            ledger["firm_state"][slug] = {
                "last_volume": snapshot.get("volume", 0),
                "last_flags": snapshot.get("flags", []),
                "last_score": round(
                    (
                        snapshot.get("sentiment", {}).get("positive", 0)
                        - snapshot.get("sentiment", {}).get("negative", 0)
                    )
                    / max(snapshot.get("volume", 1), 1),
                    2,
                )
                if snapshot.get("volume", 0) > 0
                else 0.0,
                "last_date": today,
            }

        prune_old_raw(slug)

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    with open(SNAP_DIR / f"{today}.json", "w") as f:
        json.dump({"generated_at": today, "firms": snapshots}, f, indent=2)

    duration = round(time.time() - start, 2)
    firm_count = len(snapshots)
    flag_count = sum(1 for s in snapshots if s.get("flags"))
    ledger["last_run"] = {
        "date": today,
        "status": "ok",
        "firm_count": firm_count,
        "flag_count": flag_count,
        "duration_seconds": duration,
    }
    ledger["gates"] = {
        "soft_skip": False,
        "hard_pass": True,
        "last_check": datetime.utcnow().isoformat() + "Z",
    }
    ledger["history"].append(
        {
            "date": today,
            "status": "ok",
            "firm_count": firm_count,
            "flag_count": flag_count,
        }
    )
    if len(ledger["history"]) > 20:
        ledger["history"] = ledger["history"][-20:]
    save_ledger(ledger)
    print(f"Ledger updated: {firm_count} firms, {flag_count} flagged, {duration}s")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
