'use client';

import { useEffect, useMemo, useState } from 'react';

type Firm = {
  firm_information: { firm_name: string; firm_logo_url: string; firm_url: string; location: string };
  account_details: { account_name: string; account_size: number; price: number | null; sale_price: number | null; profit_split: number | null; profit_target: number; daily_drawdown: number | null; max_drawdown: number; drawdown_type: string };
  rules_and_parameters: { min_trading_days: number | null; max_trading_days: number | null; allowed_instruments: string[]; scaling_plan: boolean };
};

type SortKey = 'account_size' | 'price' | 'sale_price' | 'profit_target' | 'max_drawdown';
type SortDir = 'asc' | 'desc';

export default function Home() {
  const [firms, setFirms] = useState<Firm[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('account_size');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  useEffect(() => {
    const source = process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/api/prop-firms` : '/api/prop-firms';
    fetch(source)
      .then((res) => {
        if (!res.ok) throw new Error('API error');
        return res.json();
      })
      .then(setFirms)
      .catch(() => setFirms([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    const list = firms.filter((item) => {
      if (!q) return true;
      const text = [item.firm_information.firm_name, item.account_details.account_name].join(' ').toLowerCase();
      return text.includes(q);
    });

    return list.sort((a, b) => {
      const av = a.account_details[sortKey];
      const bv = b.account_details[sortKey];
      const aNum = typeof av === 'number' ? av : 0;
      const bNum = typeof bv === 'number' ? bv : 0;
      return sortDir === 'asc' ? aNum - bNum : bNum - aNum;
    });
  }, [firms, search, sortKey, sortDir]);

  const cycleSort = (key: SortKey) => {
    if (sortKey === key) setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <main className="max-w-6xl mx-auto p-4 sm:p-6">
      <h1 className="text-2xl font-semibold mb-4">Prop Firm Confidential</h1>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search firms or accounts"
          className="border rounded px-3 py-2 w-full sm:w-80"
        />
        <div className="text-sm text-gray-600">
          Sort by:{' '}
          <button className="underline" onClick={() => cycleSort('account_size')}>Account size</button>
          {' • '}
          <button className="underline" onClick={() => cycleSort('price')}>Price</button>
          {' • '}
          <button className="underline" onClick={() => cycleSort('sale_price')}>Sale price</button>
          {' • '}
          <button className="underline" onClick={() => cycleSort('profit_target')}>Profit target</button>
          {' • '}
          <button className="underline" onClick={() => cycleSort('max_drawdown')}>Max drawdown</button>
          {' '}
          ({sortDir})
        </div>
      </div>

      <div className="overflow-x-auto border rounded">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Firm</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Account</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sale</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit split</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit target</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max drawdown</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Drawdown</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filtered.length === 0 && (
              <tr>
                <td colSpan={8} className="px-4 py-4 text-center text-sm text-gray-500">No matching accounts.</td>
              </tr>
            )}
            {filtered.map((item, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <img src={item.firm_information.firm_logo_url} alt="" className="h-8 w-8 rounded-full object-cover" />
                    <div>
                      <div className="text-sm font-medium text-gray-900">{item.firm_information.firm_name}</div>
                      <div className="text-xs text-gray-500">{item.rules_and_parameters.allowed_instruments.join(', ')}</div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.account_name}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.price ?? '—'}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.sale_price ?? '—'}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.profit_split ? `${Math.round(item.account_details.profit_split * 100)}%` : '—'}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.profit_target}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.max_drawdown}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{item.account_details.drawdown_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
