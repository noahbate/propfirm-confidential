export type Firm = {
  firm_information: { firm_name: string; firm_logo_url: string; firm_url: string; location: string };
  account_details: {
    account_name: string;
    account_size: number;
    price: number | null;
    sale_price: number | null;
    profit_split: number | null;
    profit_target: number;
    daily_drawdown: number | null;
    max_drawdown: number;
    drawdown_type: string;
    activation_fee: number | null;
  };
  rules_and_parameters: { min_trading_days: number | null; max_trading_days: number | null; allowed_instruments: string[]; scaling_plan: boolean };
  score?: number | null;
};

export const DRAW_TYPES: Record<string, number> = {
  EOD: 1,
  Static: 2,
  Trailing: 3,
};

export const STRICT_OVERHEAD_PENALTY = 80;
export const MIN_ACTIVATION_COMPARE = 85;

function num(v: number | null) {
  return typeof v === 'number' ? v : 0;
}

function clamp(v: number, lo: number, hi: number) {
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

export function computeScore(item: Firm): number {
  const price = num(item.account_details.price);
  const activation = num(item.account_details.activation_fee);
  const profitSplit = num(item.account_details.profit_split);
  const profitTarget = num(item.account_details.profit_target);
  const drawdown = num(item.account_details.max_drawdown);
  const days = num(item.rules_and_parameters.max_trading_days ?? item.rules_and_parameters.min_trading_days);

  if (!price || !accountSize(item)) return 0;

  const drawdownPenalty = DRAW_TYPES[item.account_details.drawdown_type] === 3 ? 100 : 0;
  const activationPenalty =
    (item.account_details.sale_price ?? null) == null && activation >= MIN_ACTIVATION_COMPARE
      ? STRICT_OVERHEAD_PENALTY
      : 0;
  const daysPenalty = clamp(days, 0, 30) * 2.5;
  const profitSplitPenalty = (1 - profitSplit) * 150;

  const raw = (profitTarget - drawdown) + activation + activationPenalty + daysPenalty + drawdownPenalty + profitSplitPenalty;
  return Math.max(0, Math.round(raw));
}

export function accountSize(item: Firm) {
  return num(item.account_details.account_size);
}

export type SortKey = 'account_size' | 'price' | 'sale_price' | 'profit_target' | 'max_drawdown' | 'score';
export type SortDir = 'asc' | 'desc';

export function getSortValue(item: Firm, key: SortKey) {
  switch (key) {
    case 'account_size':
      return accountSize(item);
    case 'price':
      return item.account_details.price;
    case 'sale_price':
      return item.account_details.sale_price;
    case 'profit_target':
      return item.account_details.profit_target;
    case 'max_drawdown':
      return item.account_details.max_drawdown;
    case 'score':
      return item.score ?? 0;
    default:
      return 0;
  }
}

export function isTradeFriendly(
  allow: string[],
  maxDrawdown: number | null,
  profitTarget: number,
  days: number | null,
  accountSize: number
) {
  const okInstruments = Array.isArray(allow) && allow.map((s) => s.toLowerCase()).includes('futures');
  const okDrawdown = typeof maxDrawdown === 'number' && maxDrawdown > 0;
  const okProfitTarget = typeof profitTarget === 'number' && profitTarget > 0 && accountSize > 0 && profitTarget <= accountSize;
  const okDays = days == null || days <= 30;
  return Boolean(okInstruments && okDrawdown && okProfitTarget && okDays);
}
