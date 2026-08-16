# Affiliate Program Tracker

Track applications, approvals, signed documents, and commission terms for each firm.

## Status Key
- `pending` — application submitted, awaiting response
- `approved` — approved, awaiting signed agreement
- `active` — agreement signed, tracking enabled
- `rejected` — declined or no response after follow-up
- `expired` — previously active, now lapsed

---

## Firms (machine-readable schema)

```yaml
# YAML mirrors the table below; edit this block for precision
firms:
  - slug: apex-trader-funding
    name: Apex Trader Funding
    apply_url: https://apextraderfunding.com/help-center/helpful-items/affiliate-program/
    applied_date: ""
    status: pending
    commission: "15% referral"
    terms: "Recurring commission on evaluation/subscription"
    notes: ""

  - slug: bulenox
    name: Bulenox
    apply_url: https://bulenox.com/member/aff/signup
    applied_date: ""
    status: pending
    commission: "Up to 15%"
    terms: "Revenue share per referral"
    notes: ""

  - slug: topstep
    name: Topstep
    apply_url: ""
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Currently uses TUNE; no public self-serve apply page confirmed"

  - slug: take-profit-trader
    name: Take Profit Trader
    apply_url: https://takeprofittrader.com/affiliate
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: trade-day
    name: TradeDay
    apply_url: https://www.tradeday.com/affiliate-program
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: my-funded-futures
    name: My Funded Futures
    apply_url: https://myfundedfutures.com/affiliate
    applied_date: ""
    status: pending
    commission: "12%"
    terms: "Commission on evaluation + reset fees"
    notes: ""

  - slug: earn2trade
    name: Earn2Trade
    apply_url: https://www.earn2trade.com/affiliates
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: ticktick-trader
    name: TickTickTrader
    apply_url: ""
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Affiliate program appears inactive after platform shutdown"

  - slug: trading-lucid
    name: Lucid
    apply_url: https://lucidtrading.com/affiliate/
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: fundingpips
    name: FundingPips
    apply_url: https://help.fundingpips.com/hc/en-us/articles/34447107645841-Become-an-Affiliate
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: bright-funded
    name: Bright Funded
    apply_url: https://brightfunded.com/affiliate-program
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: lark-funding
    name: Lark Funding
    apply_url: ""
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Help center lists affiliates, but no confirmed self-serve URL"

  - slug: funded-trading-p
    name: Funded Trading Plus
    apply_url: https://www.fundedtradingplus.com/affiliates
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: ""

  - slug: blue-guardian
    name: Blue Guardian
    apply_url: https://www.blueguardian.com/affiliates
    applied_date: ""
    status: pending
    commission: "Tier-based + bonus"
    terms: "Level 3 skip-tier option; free $5K funded account for first referral"
    notes: ""

  - slug: alpha-futures
    name: Alpha Futures
    apply_url: https://help.alpha-futures.com/en/articles/9619919-affiliate-program
    applied_date: ""
    status: pending
    commission: "15% recurring"
    terms: "Recurring on subscriptions via link/code"
    notes: ""

  - slug: top-one-futures
    name: Top One Futures
    apply_url: https://www.toponefutures.com/affiliate
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Established April 2025"

  - slug: funded-family
    name: Funded Family
    apply_url: https://www.fundedfuturesfamily.com/affiliate-inquiry/
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Inquiry form only"

  - slug: futures-elite
    name: Futures Elite
    apply_url: https://futureselite.com/affiliate
    applied_date: ""
    status: pending
    commission: ""
    terms: ""
    notes: "Established November 2024"
```

---

## Competitor

```yaml
competitors:
  - slug: propfirm-match
    name: PropFirmMatch
    url: https://propfirmmatch.com/
    priority: high
    note: "Do not apply for affiliate; monitor content and positioning"
```

---

## Documents

Store signed agreements and relevant docs in `docs/affiliate-docs/`:

```
docs/affiliate-docs/
├── apex-trader-funding/
│   └── agreement.pdf
├── topstep/
│   └── agreement.pdf
└── ...
```

## Process

1. Research firm’s affiliate program (look for “partners”, “affiliates”, “ambassadors”)
2. Add or update entry in the YAML schema above
3. **Do not submit applications automatically.**
4. Once you approve, submit application via their portal or email
5. Once approved, add agreement docs to `docs/affiliate-docs/<slug>/`
6. Update status to `active`
7. Add affiliate link to `backend/prop_firms.json` under `firm_information.affiliate_url`
8. Add tracking ID / referral code here

## Weekly Review

Review tracker during weekly data refresh cron:
- Follow up on `pending` applications >14 days old
- Verify `active` links are still valid
- Flag any firms that change terms or pause programs
