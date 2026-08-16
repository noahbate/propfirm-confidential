# Prop Firm Confidential (PFC) — Prop Firm Platform

**A full-stack platform for tracking, analyzing, and comparing prop firm challenges — with integrated sentiment monitoring.**

Live at: [propfirmconfidential.com](https://propfirmconfidential.com) (prod) · [tempus.dpdns.org](http://tempus.dpdns.org) (staging)

Deployed via **Netlify** (frontend) + **Render** (backend API).

## Architecture

```
propfirm-confidential/
├── frontend/          # Next.js 16 (App Router, Tailwind CSS, TypeScript)
│   ├── src/           # Application pages and components
│   └── public/        # Static assets
├── backend/           # FastAPI Python backend
│   ├── src/           # API routes, business logic
│   ├── sentiment/     # Prop firm sentiment analysis pipeline
│   ├── scrape-cache/  # Cached scrape data
│   └── prop-firm-app/ # Alternative/legacy app entry
├── prop-firm-app/     # Netlify-deployed static app (Vite/vanilla)
├── docs/              # Architecture and infrastructure docs
├── planning/          # Implementation plans and strategy notes
├── scripts/           # Automation and data processing scripts
├── .hermes/           # Hermes agent configurations
├── netlify.toml       # Netlify deploy config
└── .cost.env          # Cost tracking
```

## Core Features

### Prop Firm Directory & Comparison
- Browse and compare prop firms side-by-side
- Challenge rules, pricing, payout structures
- Account sizing and scaling options

### Sentiment Monitoring (`backend/sentiment/`)
- Automated sentiment scraping for 18+ prop firms
- Snapshot-based tracking with cache-first refresh
- Daily scoring and trend detection
- Notion sync for status mirroring

### One-Page Sentiment Dashboard
- Clean daily layout of firm-level sentiment
- Lowest-scoring firms and clean signals
- Cache deduplication and refresh pipeline

## Tech Stack

| Layer | Stack |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| **Backend** | Python, FastAPI |
| **Deploy** | Netlify (frontend), Render (backend) |
| **Data** | In-memory + JSON cache, Notion integration |

## Related Projects

| Project | Relationship |
|---|---|
| [Prop Brain](../prop-brain/) | R&D for challenge strategies and account management |
| [Trading Systems Analysis](../trading-analysis/) | Cross-system methodology comparison |
| DeerFlow | Future MCP server — expose PFC data to agentic analysis workflows |
