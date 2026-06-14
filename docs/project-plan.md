# Project Plan: Prop Firm Confidential

## Phase 1 — MVP
1. **Project scaffolding** — backend (`/Users/hermes/projects/propfirm-confidential/backend`) and frontend (`/Users/hermes/projects/propfirm-confidential/frontend`) initialized.
2. **Data modeling** — define JSON schema for firms, accounts, and rules.
3. **Backend API** — FastAPI endpoint to serve firm data in `/Users/hermes/projects/propfirm-confidential/backend`.
4. **Frontend table view** — Next.js page rendering accounts.
5. **Requirements + tracking docs** — `docs/requirements.md` + `docs/project-plan.md`.
6. **Filtering/sorting + search** — client-side controls mapped to schema fields.
7. **Deployment** — Netlify frontend + hosted backend.

## Phase 2 — Data Expansion
In progress.
- Firms populated: Apex Trader Funding, Bulenox, Topstep, Take Profit Trader, TradeDay, My Funded Futures, Earn2Trade, TickTickTrader, Lucid.
- Validation pending: confirm dynamic prices and rule changes continue to match the schema.

## Phase 3 — Users and Comparison Tools
1. Authentication and saved preferences.
2. Side-by-side comparison view.
3. Introduce proprietary scoring with documented methodology.
