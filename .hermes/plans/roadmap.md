# Prop Firm Confidential: Master Implementation Plan

## ✅ Phase 0: Complete
- Git repo initialized (`/Users/hermes/projects/propfirm-confidential`, main protected)
- Astro + FastAPI app deployed (Netlify + Render)
- xurl authenticated
- Living SOP created (`.hermes/sops/000-living-sop.md`)
- Kanban board initialized (`propfirm-confidential`)

## Phase 1: X.com Launch (1–2 days)

- [ ] **Task 1.1:** Review launch post drafts (`docs/marketing-launch-plan.md`) and mark ready
- [ ] **Task 1.2:** Schedule Day 0 launch thread (`https://propfirmconfidential.netlify.app`)
- [ ] **Task 1.3:** Schedule Day 1–3 posts (feature highlight, evidence/screenshot, trust/data quality)
- [ ] **Task 1.4:** Day 7 engagement recap post

## Phase 2: Sentiment Page (3–5 days)

- [ ] **Task 2.1:** X.com mention ingestion — scrape/search mentions of each firm via xurl
- [ ] **Task 2.2:** Sentiment storage schema — add `sentiment_snapshots` + `bot_posts` tables or JSON files
- [ ] **Task 2.3:** Sentiment page (`/sentiment`) — per-firm payout reports, scam flags, mention volume
- [ ] **Task 2.4:** Reputation scoring — weighted blend of official rules + sentiment signals

## Phase 3: Product Expansion (3–5 days)

- [ ] **Task 3.1:** Side-by-side comparison view
- [ ] **Task 3.2:** Authentication + saved preferences
- [ ] **Task 3.3:** Proprietary scoring with documented methodology

## Phase 3: Data Pipeline (ongoing)

- [ ] **Task 3.1:** Weekly scrape + cache-first refresh (`backend/scrape_result.json` → review → `backend/prop_firms.json`)
- [ ] **Task 3.2:** GitHub Actions → Netlify deploy on main push
- [ ] **Task 3.3:** Daily/weekly agentic checks (site health, dependency scan)

## Phase 4: Full Autonomy (next sprint)

- [ ] **Task 4.1:** Self-healing deploy hooks + rollback
- [ ] **Task 4.2:** Cost dashboard (LLM + hosting)
- [ ] **Task 4.3:** Multi-channel expansion (Telegram, email)
