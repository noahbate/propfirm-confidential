# ⚠ Open Issue: propfirmconfidential.com is OFFLINE (DNS NXDOMAIN)

**Logged:** 2026-08-10 (by Hermes fleet alignment loop — first run catch)
**Severity:** Production outage — the site is unreachable for all visitors
**Status:** OPEN — requires Netlify/domain-owner action (credentials for this target not held in the floatersfocus session)

## Evidence

- `https://propfirmconfidential.com/` → `000` (could not resolve host)
- `https://www.propfirmconfidential.com/` → `000`
- `dig @8.8.8.8 propfirmconfidential.com` → **empty answer**
- `nslookup` → `NXDOMAIN` ("server can't find propfirmconfidential.com")
- WHOIS: domain status **ACTIVE** — i.e. registered, but **zero DNS records published**
- No CNAME / A records found anywhere

## Interpretation

The domain is paid up (not expired) but has **no DNS records at all**. Something removed the DNS zone or records — common causes:
- DNS records deleted from the registrar/Netlify DNS panel (e.g. during a migration or a panel cleanup)
- Nameservers pointed at a provider where the zone no longer exists
- The Netlify site's custom domain got detached and the auto-managed DNS was cleared

## To fix (owner of this project)

1. Log in to the domain registrar where `propfirmconfidential.com` is managed.
2. Confirm the nameservers: for Netlify DNS they should be the four `dns1.p01.nsone.net`–`dns4.p01.nsone.net` nameservers.
3. In Netlify → the propfirm site → **Domain management**, re-attach the custom domain if it's detached (Netlify will republish the needed DNS records).
4. Verify: `dig +short propfirmconfidential.com @8.8.8.8` returns the Netlify load balancer IP, then `curl -I https://propfirmconfidential.com` returns 200.

## Monitoring

The fleet alignment loop (cron `8d2189f28030`, daily 08:45) watches `https://propfirmconfidential.com` — it will automatically stop flagging the site once DNS is restored. No manual unsubscribe needed.

## Related (non-urgent, working-state noise — not action items)

- 32 uncommitted changes in this repo (`.hermes/plans/roadmap.md`, `backend/prop_firms.json`, `backend/src/main.py`, `frontend/src/app/page.tsx`, +27 more) — normal dev state, commit when ready.
- No local `.env` / `backend/.env` file — expected; env vars live in the Netlify dashboard.
