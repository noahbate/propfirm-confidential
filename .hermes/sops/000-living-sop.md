# Living SOP: Prop Firm Confidential

## 1. Infrastructure Docs

### Secrets
- Store in **GitHub Secrets** + `secrets.env.example`.
- Hermes loads via `load-secrets`.

### Deployment Flow
```text
git push origin main
→ GitHub Action → Build & deploy to Netlify
→ Post-deploy: ping X-engine
```

### Domain
- Proxy: Cloudflare / Netlify
- Target: `propfirmconfidential.com`
- Document A records + CNAMEs.

---

## 2. Daily / Weekly Agentic Checks

### Daily
- `hermes health-check` (site up, X posting queue, LLM costs)
- Dependency scan: `npm audit`, `pip check`

### Weekly
- Update sweep: `npm update`, review PRs
- Content performance review: X analytics + web
- Backup critical DBs / configs

---

## 3. Self-Healing Rules

### Failure Patterns
| Failure | Response |
|---|---|
| Deploy fail | Rollback + notify |
| Credential expiry | Rotate via secrets manager |
| X rate limit | Exponential backoff + queue |
| LLM cost spike | Auto-switch to cheaper model + alert |

### Restart Loops
- Monitor PID + logs
- Kill / restart with cooldown

### Escalation
- If >3 failures, pause automation and alert human.
