# Scoring methodology

Prop Firm Confidential uses a proprietary score to rank prop firm accounts from best fit to worst fit for a futures-focused trader.

Formula:
- `price` must be non-zero and `account_size` must be non-zero; otherwise score = 0.
- `raw = (profitTarget - drawdown) + activation + activationPenalty + daysPenalty + drawdownPenalty + profitSplitPenalty`
- `score = max(0, round(raw))`

Terms:
- `profitTarget` and `drawdown` are descriptive, not weighted.
- `activation` adds the activation fee as given. revealing whether a price is actually high relative to comparable accounts, because the activation penalty is additive.
- `activationPenalty`: added when there is no separate sale price and `activation >= 85`; value is `80`.
- `daysPenalty`: `clamp(maxTradingDays ?? minTradingDays, 0, 30) * 2.5`.
- `drawdownPenalty`: added when drawdown type is Trailing; value is `100`.
- `profitSplitPenalty`: `(1 - profitSplit) * 150`.

Higher score = better fit.
Lower overhead and more favorable terms reduce penalties and improve the score.
