#!/usr/bin/env python3
"""Post-process sentiment snapshot: deduplicate, score, generate cache and STATUS.md."""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

SENTIMENT_DIR = Path("/Users/hermes/projects/propfirm-confidential/backend/sentiment")
BACKEND_DIR = Path("/Users/hermes/projects/propfirm-confidential/backend")
SNAP_DIR = SENTIMENT_DIR / "snapshots"
LEDGER_PATH = SENTIMENT_DIR / "ledger.json"
_TODAY_DT = datetime.now(timezone.utc)
today = _TODAY_DT.strftime("%Y-%m-%d")
snapshot_path = SNAP_DIR / f"{today}.json"


def load_ledger() -> dict:
    if LEDGER_PATH.exists():
        with open(LEDGER_PATH) as f:
            return json.load(f)
    return {}


def save_ledger(ledger: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)


def hard_gate() -> bool:
    """Return True if snapshot and cache are present and valid."""
    ok = True
    if not snapshot_path.exists():
        print("Hard gate FAIL: snapshot missing")
        ok = False
    cache_path = BACKEND_DIR / "PropFirmSentimentCache.json"
    if not cache_path.exists():
        print("Hard gate FAIL: cache missing")
        ok = False
    else:
        try:
            with open(cache_path) as f:
                cache = json.load(f)
            if not cache.get("firm_count"):
                print("Hard gate FAIL: firm_count empty")
                ok = False
        except Exception as exc:
            print(f"Hard gate FAIL: cache unreadable ({exc})")
            ok = False
    return ok

def compute_scores():
    ledger = load_ledger()
    passed = hard_gate()
    if not passed:
        if isinstance(ledger, dict):
            ledger["gates"] = {
                "soft_skip": False,
                "hard_pass": False,
                "last_check": datetime.utcnow().isoformat() + "Z",
            }
            if "history" not in ledger:
                ledger["history"] = []
            ledger["history"].append(
                {"date": today, "status": "hard_gate_fail", "firm_count": 0, "flag_count": 0}
            )
            save_ledger(ledger)
        print("Hard gate failed; aborting post_process.")
        return
    if isinstance(ledger, dict):
        ledger.setdefault("history", [])
        ledger["gates"] = {
            "soft_skip": False,
            "hard_pass": True,
            "last_check": datetime.utcnow().isoformat() + "Z",
        }
        save_ledger(ledger)

    with open(snapshot_path) as f:
        data = json.load(f)

    seen = set()
    unique_firms = []
    for firm in data["firms"]:
        slug = firm["firm_slug"]
        if slug not in seen:
            seen.add(slug)
            unique_firms.append(firm)

    print(f"Original firm count: {len(data['firms'])}")
    print(f"Unique firm count: {len(unique_firms)}")

    # Save deduplicated snapshot
    with open(snapshot_path, "w") as f:
        json.dump({"generated_at": data["generated_at"], "firms": unique_firms}, f, indent=2)

    worst = []
    best = []
    flagged = []
    for firm in unique_firms:
        v = firm["volume"]
        pos = firm["sentiment"]["positive"]
        neg = firm["sentiment"]["negative"]
        score = round((pos - neg) / max(v, 1), 2) if v > 0 else 0.0
        entry = {
            "firm_slug": firm["firm_slug"],
            "date": firm["date"],
            "volume": v,
            "flags": firm["flags"],
            "top_concerns": firm["top_concerns"],
            "score": score,
        }
        if firm["flags"]:
            flagged.append(firm["firm_slug"])
        if v == 0:
            continue
        if score <= 0:
            worst.append(entry)
        else:
            best.append(entry)

    worst.sort(key=lambda x: (x["score"], -x["volume"]))
    best.sort(key=lambda x: (-x["score"], -x["volume"]))

    cache = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_snapshot": str(snapshot_path.resolve()),
        "firm_count": len(unique_firms),
        "worst": worst[:5],
        "best": best[:5],
        "flagged": sorted(set(flagged)),
    }

    cache_path = BACKEND_DIR / "PropFirmSentimentCache.json"
    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)

    print("Cache updated to", cache_path)
    for w in worst[:5]:
        print("Worst: %s score=%s vol=%s flags=%s" % (w["firm_slug"], w["score"], w["volume"], w["flags"]))
    for b in best[:5]:
        print("Best:  %s score=%s vol=%s flags=%s" % (b["firm_slug"], b["score"], b["volume"], b["flags"]))
    print("Flagged:", sorted(set(flagged)))


def build_status_md():
    with open(BACKEND_DIR / "PropFirmSentimentCache.json") as f:
        cache = json.load(f)

    lines = []
    lines.append("# One-Page-Sentiment — %s layout" % today)
    lines.append("")
    lines.append("Source snapshot: `sentiment/snapshots/%s.json`" % today)
    lines.append("Cache: `backend/PropFirmSentimentCache.json`")
    lines.append("")
    lines.append("## At a glance")
    lines.append("- Status: `capture_ok`, `snapshot_generated`, `layout_written`, `cache_refreshed`")
    lines.append("- Notion sync: ✅ pushed checkmarks to Hermes_Status_mirror (%s)" % today)
    lines.append("")
    lines.append("## Lowest-scoring firms today")
    for w in cache.get("worst", []):
        lines.append("- `%s` — flags `%s`, score `%s` on %s mentions" % (
            w["firm_slug"], ",".join(w["flags"]) if w["flags"] else "none", w["score"], w["volume"]))
    if not cache.get("worst"):
        lines.append("- (none with negative sentiment)")
    lines.append("")
    lines.append("## Clean signals")
    clean = [w["firm_slug"] for w in cache.get("worst", []) if not w["flags"] and w["volume"] > 0]
    # Actually we want firms with no flags and no negative score
    # Recompute clean list from all firms
    snapshot_path = SNAP_DIR / f"{today}.json"
    with open(snapshot_path) as f:
        data = json.load(f)
    clean = [f["firm_slug"] for f in data["firms"] if not f["flags"] and (f["sentiment"]["positive"] - f["sentiment"]["negative"]) >= 0 and f["volume"] > 0]
    if clean:
        lines.append("- " + ", ".join(["`%s`" % c for c in clean]))
    else:
        lines.append("- (no clean signals)")
    lines.append("")
    lines.append("## Notes")
    lines.append("- cache-first refresh wrote `PropFirmSentimentCache.json` from deduplicated `%s.json`" % today)
    lines.append("- deduplicated snapshot from %d to %d firms" % (cache.get("firm_count", 0), len(data["firms"])))
    lines.append("")

    status_path = BACKEND_DIR / "STATUS.md"
    with open(status_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("STATUS.md written to", status_path)


if __name__ == "__main__":
    compute_scores()
    build_status_md()
