# ⚠ Open Issue (resolved 2026-08-16): propfirmconfidential.com OFFLINE + deploys blocked

**Logged:** 2026-08-10 (fleet alignment loop catch) · **Updated:** 2026-08-16 (root causes corrected + resolution)
**Severity:** Production outage — site unreachable on custom domain; no new deploys since 2026-06-15.

## ✅ Resolution (2026-08-16): migrated to Vercel

- **Deploy unblocked:** site migrated from Netlify → **Vercel** (`hermes-nb` team, project `propfirmconfidential`, framework astro, rootDirectory `prop-firm-app`, git-connected to this repo → auto-deploys on push to main).
- **Live now:** https://propfirmconfidential.vercel.app — `/`, `/compare`, `/ev-calculator` all 200 (EV calculator was 404 on Netlify since July).
- **Why:** Netlify account credit-exhausted (`Account credit usage exceeded — new deploys are blocked`); Vercel free tier has no such wall and the account was already in use (floatersfocus).
- **Remaining:** register `propfirmconfidential.com` (domain does NOT exist — Verisign RDAP 404 / whois "No match"), then attach via Vercel → Domains (or NameSilo registrar + DNS). See below.

## Root cause 1 (historical) — Netlify deploys blocked: account credits exhausted

- `POST /api/v1/sites/.../deploys` → **403** `{"error":"Account credit usage exceeded - new deploys are blocked until credits are added"}`
- Site plan was `nf_team_dev` (free dev plan). Last Netlify deploy: 2026-06-15 (CLI).
- NOT a token problem (site-write scopes worked); NOT a git problem (hook fired but no build — same credit wall).
- Netlify site (`propfirmconfidential` netlify.app) left dormant after migration; repo webhook + build hook `6a821a74a694d2d30845f1df` still exist if ever needed.

## Root cause 2 (historical) — Custom domain NXDOMAIN: propfirmconfidential.com is NOT registered

- `whois propfirmconfidential.com` → **"No match for domain"**; Verisign RDAP → **404**.
- Earlier "domain status ACTIVE" reading (2026-08-10) was IANA boilerplate, not the domain — misread.
- Netlify site had `custom_domain: None`, no DNS zone. (Netlify `managed_dns: true` was set but irrelevant — domain never existed.)

## Monitoring

Fleet alignment loop (cron `8d2189f28030`, daily 08:45) watches `https://propfirmconfidential.com` — auto-stops flagging once the domain is registered and DNS points at Vercel.
