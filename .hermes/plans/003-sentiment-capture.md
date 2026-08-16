# Sentiment Capture Plan

Goal: Capture and serve X.com sentiment data per prop firm to power the `/sentiment` page and reputation scoring.

## Data Sources
- X posts mentioning each firm name/handle
- Replies to official firm posts
- Quote-tweets of firm announcements
- Keywords: payout, delay, scam, funded, withdrawal

## Capture Cadence
- Weekly batch via Hermes cron (same window as firm website scrape)
- Hermes cron runs Monday 00:00
- Raw JSON stored in `backend/sentiment/raw/<firm_slug>/<YYYY-MM-DD>.json`
- Scoring script produces weekly snapshot: `backend/sentiment/snapshots/<YYYY-MM-DD>.json`

## Retention Policy
- Retain raw data for **minimum 13 weeks**, but more is desirable
- Auto-prune when Render disk reaches 75% capacity
- Prune order: oldest raw first, beyond the 13-week minimum
- Monthly consolidation snapshots kept separately to preserve long-term trends

## Scoring Schema (per firm)
```json
{
  "firm_slug": "apex-trader-funding",
  "date": "2025-06-16",
  "volume": 42,
  "sentiment": {
    "positive": 8,
    "neutral": 25,
    "negative": 9
  },
  "flags": ["payout_delay", "multiple_complaints"],
  "top_concerns": ["withdrawal time", "verification holds"],
  "sample_tweets": [...]
}
```

## File Layout
```
backend/sentiment/
├── raw/                         # Gitignored, Render disk
│   └── <firm_slug>/
│       └── <YYYY-MM-DD>.json
├── snapshots/                   # Gitignored, Render disk
│   └── <YYYY-MM-DD>.json
└── README.md
```

## Serving
- FastAPI endpoint: `GET /api/sentiment?firm=<slug>`
- FastAPI endpoint: `GET /api/sentiment` (all firms)
- Frontend page: `/sentiment` Astro route

## Risks / Mitigations
| Risk | Mitigation |
|---|---|
| X rate limits | Weekly batch, ~14–20 calls total. Well within free tier. |
| Render disk space | 75% prune threshold. 10 firms × 52 weeks ≈ 5–10 MB raw. |
| X ToS compliance | Use xurl official API, not scraping. |
| False positives | Rule-based flags require threshold (≥3 negative mentions/week). |

## Implementation Order
1. Add `xurl search` queries to existing weekly scrape cron
2. Scoring script + FastAPI `/api/sentiment`
3. `/sentiment` Astro page
4. Integration into main comparison table (reputation column)
