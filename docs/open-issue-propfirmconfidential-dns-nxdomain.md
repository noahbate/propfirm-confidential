# ⚠ Open Issue: propfirmconfidential.com OFFLINE + deploys blocked

**Logged:** 2026-08-10 (fleet alignment loop catch) · **Updated:** 2026-08-16 (corrected root cause)
**Severity:** Production outage — site unreachable on custom domain; also no new deploys since 2026-06-15.
**Status:** OPEN — needs account-owner action (billing + domain registration). See "To fix" below.

## Root cause 1 — Deploys blocked: Netlify account credits exhausted

- `POST /api/v1/sites/.../deploys` → **403** `{"error":"Account credit usage exceeded - new deploys are blocked until credits are added"}`
- Site plan: `nf_team_dev` (free dev plan). Last successful deploy: 2026-06-15 (CLI).
- Build hooks fire (HTTP 200) but no build is created — same credit wall.
- NOT a token problem: the CLI token has working site-write scope (`updateSite`, `createSiteBuildHook` both succeed).
- **Fix:** add build credits / upgrade in Netlify → Billing (app.netlify.com → Billing). Once credits exist, deploy via:
  - `netlify deploy --prod --build` from repo root (netlify.toml: base=prop-firm-app), or
  - Build hook `https://api.netlify.com/build_hooks/6a821a74a694d2d30845f1df` (created 2026-08-16, "agent-deploy-hook").

## Root cause 2 — Custom domain NXDOMAIN: propfirmconfidential.com is NOT registered

- Corrected from earlier "domain ACTIVE, zero DNS records" misread (that WHOIS line was the IANA boilerplate, not the domain).
- `whois propfirmconfidential.com` → **"No match for domain"**
- Verisign RDAP → **404** (domain not in .com registry)
- Netlify site: `custom_domain: None`, `domain_aliases: []`, no Netlify DNS zone for the domain (only `flmedi.com` zone exists), though `managed_dns: true`.
- **Fix:** register the domain (~$10–18/yr) — Netlify Domains (same account, auto-managed DNS; dashboard → Domains → Register) or NameSilo (no local creds found; Cloudflare bot detection blocks automated login). After registration, attach via Netlify Domain management; DNS + SSL auto-provision on Netlify DNS.

## Monitoring

Fleet alignment loop (cron `8d2189f28030`, daily 08:45) watches `https://propfirmconfidential.com` — auto-stops flagging once DNS is restored.

## Related (resolved 2026-08-16)

- 32 uncommitted changes committed + pushed to main (`f4c358f..98b8122`, 5 grouped commits: EV calculator, sentiment pipeline, data refresh, Next.js compare page, docs/scripts).
- Runtime artifacts gitignored (scrape-cache, test.json, .cost.env, sentiment/raw).
- Working tree clean.
