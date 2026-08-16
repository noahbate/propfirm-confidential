'use client';

import { computeScore, type Firm, getSortValue } from '../firm-lib';
import { useEffect, useMemo, useState } from 'react';

type Slot = '' | 'A' | 'B' | 'C';

const COLUMNS = [
  { key: 'score', label: 'Score', path: (f: Firm) => [f.score ?? computeScore(f)] },
  { key: 'account_size', label: 'Account size', path: (f: Firm) => [f.account_details.account_size] },
  { key: 'price', label: 'Price', path: (f: Firm) => [f.account_details.price] },
  { key: 'sale_price', label: 'Sale price', path: (f: Firm) => [f.account_details.sale_price] },
  { key: 'profit_split', label: 'Profit split', path: (f: Firm) => [f.account_details.profit_split] },
  { key: 'profit_target', label: 'Profit target', path: (f: Firm) => [f.account_details.profit_target] },
  { key: 'daily_drawdown', label: 'Daily drawdown', path: (f: Firm) => [f.account_details.daily_drawdown] },
  { key: 'max_drawdown', label: 'Max drawdown', path: (f: Firm) => [f.account_details.max_drawdown] },
  { key: 'drawdown_type', label: 'Drawdown type', path: (f: Firm) => [f.account_details.drawdown_type] },
  { key: 'min_trading_days', label: 'Min trading days', path: (f: Firm) => [f.rules_and_parameters.min_trading_days] },
  { key: 'max_trading_days', label: 'Max trading days', path: (f: Firm) => [f.rules_and_parameters.max_trading_days] },
  { key: 'scaling_plan', label: 'Scaling plan', path: (f: Firm) => [f.rules_and_parameters.scaling_plan] },
  { key: 'allowed_instruments', label: 'Instruments', path: (f: Firm) => [f.rules_and_parameters.allowed_instruments] },
] as const;

function getNestedValue(obj: Record<string, unknown>, path: (string | number)[]) {
  return path.reduce((current: unknown, p) => (current as Record<string, unknown>)?.[p], obj);
}

function fmtValue(v: unknown): string {
  if (v === null || v === undefined) return '—';
  if (Array.isArray(v)) return v.join(', ');
  if (typeof v === 'boolean') return v ? 'Yes' : 'No';
  return `${v}`;
}

function pairwise<T extends readonly unknown[]>(values: readonly T[]): { key: string; values: T }[] {
  if (!values.length) return [];
  const headers: string[] = [
    ...new Set(
      values.flatMap((vs, idx) =>
        Array.isArray(vs) ? vs.map((v, i) => `${i}`) : []
      )
    ),
  ];
  return [
    { key: headers.join('>'), values: Array.isArray(values[0]) ? values[0] : values },
    ...values.slice(1).map((vs, idx) => ({ key: `item ${idx + 2}`, values: Array.isArray(vs) ? vs : [vs] })),
  ];
}

export default function ComparePage() {
  const [firms, setFirms] = useState<Firm[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [activeSlot, setActiveSlot] = useState<Slot>('');

  useEffect(() => {
    const source = process.env.NEXT_PUBLIC_API_URL
      ? `${process.env.NEXT_PUBLIC_API_URL}/api/prop-firms`
      : '/api/prop-firms';
    fetch(source)
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((data) => {
        setFirms(data as Firm[]);
      })
      .catch(() => setFirms([]))
      .finally(() => setLoading(false));
  }, []);

  const idFor = (f: Firm) => `${f.firm_information.firm_name}|${f.account_details.account_name}`;

  const pick = (id: string) => {
    if (!selectedIds.includes(id) && selectedIds.length >= 3) return;
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const selected = useMemo(
    () => firms.filter((f) => selectedIds.includes(idFor(f))),
    [firms, selectedIds]
  );

  const winner = useMemo(() => {
    if (selected.length < 2) return null;
    const scored = selected.map((f, idx) => ({ idx, score: computeScore(f) })).sort((a, b) => b.score - a.score);
    return scored;
  }, [selected]);


  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <main className="max-w-6xl mx-auto p-4 sm:p-6">
      <div className="flex items-end justify-between mb-4 gap-3">
        <div className="flex items-center gap-3">
          <a href="/" className="text-sm text-gray-500 hover:text-gray-900">Back to all firms</a>
          <h1 className="text-2xl font-semibold">Compare firms</h1>
        </div>
        <div className="text-sm text-gray-600">
          Selected: {selected.length}/3
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {(['A', 'B', 'C'] as const).map((slot) => {
          const idx = slot === 'A' ? 0 : slot === 'B' ? 1 : 2;
          const selectedForSlot = selected[idx];
          return (
            <div key={slot} className="border rounded">
              <div className="flex items-center justify-between border-b px-3 py-2 bg-gray-50">
                <div className="text-sm font-medium">Firm {slot}</div>
                <div className="relative">
                  <button
                    className="text-sm border rounded px-2 py-1 bg-white"
                    onClick={(e) => {
                      e.stopPropagation();
                      setActiveSlot((prev) => (prev === slot ? '' : slot));
                    }}
                  >
                    {selectedForSlot ? 'Change' : 'Add firm'}
                  </button>
                  {activeSlot === slot && (
                    <div className="absolute right-0 mt-1 z-10 w-72 max-h-64 overflow-auto border rounded bg-white shadow">
                      {firms.map((f) => {
                        const id = idFor(f);
                        const alreadySelected = selectedIds.includes(id);
                        const isSelectedForSlot = selectedForSlot && idFor(selectedForSlot) === id;
                        return (
                          <button
                            key={id}
                            className={`block w-full text-left text-sm px-3 py-2 ${
                              isSelectedForSlot ? 'bg-gray-50 font-medium' : 'hover:bg-gray-50'
                            } ${alreadySelected && !isSelectedForSlot ? 'opacity-50' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              pick(id);
                            }}
                          >
                            {f.firm_information.firm_name} — {f.account_details.account_name}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>

              <div className="px-3 py-3 text-sm space-y-2">
                {selectedForSlot ? (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <img
                        src={selectedForSlot.firm_information.firm_logo_url}
                        alt=""
                        className="h-6 w-6 rounded-full object-cover"
                      />
                      <div className="font-medium">
                        {selectedForSlot.firm_information.firm_name}
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Account</div>
                      <div>{selectedForSlot.account_details.account_name}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Market</div>
                      <div>{selectedForSlot.rules_and_parameters.allowed_instruments.join(', ')}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Score</div>
                      <div className="font-medium">{computeScore(selectedForSlot)}</div>
                    </div>
                  </div>
                ) : (
                  <div className="text-gray-500">No firm selected.</div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {selected.length >= 1 && (
        <div className="mt-6 space-y-6">
          {winner && winner.length >= 2 && (
            <div className="border rounded bg-white p-4">
              <h2 className="text-lg font-medium mb-2">Recommendation</h2>
              <p className="text-sm text-gray-800">
                Based on the scoring model, the best option is{' '}
                <span className="font-medium">
                  {selected[winner[0].idx].firm_information.firm_name} —{' '}
                  {selected[winner[0].idx].account_details.account_name}
                </span>{' '}
                (score {winner[0].score}). This option balances cost, profit split, drawdown type, and time-based terms most favorably.
              </p>
            </div>
          )}

          <div>
            <h2 className="text-lg font-medium mb-2">Differences</h2>
            <div className="border rounded divide-y">
              {COLUMNS.map((col) => {
                const cellValues = selected.map((f) => {
                  const vs = col.path(f);
                  if (!vs.length) return null;
                  return vs[0];
                });
                const distinct = new Set(cellValues.map((v) => (v === undefined || v === null ? null : typeof v === 'object' ? JSON.stringify(v) : v)));
                if (distinct.size <= 1) return null;
                const winnerItem = winner && winner.length ? selected[winner[0].idx] : selected[0];
                return (
                  <div key={col.key} className="grid grid-cols-1 sm:grid-cols-3 gap-3 px-4 py-3">
                    <div className="text-sm font-medium text-gray-900 sm:col-span-1">{col.label}</div>
                    <div className="sm:col-span-2 text-sm">
                      <div className="grid grid-cols-3 gap-3">
                        {selected.map((f, i) => {
                          const vs = col.path(f);
                          const value = vs[0];
                          const best = f === winnerItem;
                          return (
                            <div
                              key={i}
                              className={`rounded border px-3 py-2 ${
                                best ? 'border-green-300 bg-green-50' : 'border-gray-200 bg-white'
                              }`}
                            >
                              <div className="text-xs text-gray-600 mb-1">
                                {f.firm_information.firm_name}
                              </div>
                              <div className={best ? 'text-green-900 font-medium' : 'text-gray-900'}>
                                {fmtValue(value)}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                      <div className="text-xs text-gray-600 mt-2">{diffHint(col.key, selected, winnerItem)}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-medium mb-2">Score breakdown</h2>
            <div className="border rounded overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Firm</th>
                    {selected.map((f) => (
                      <th key={idFor(f)} className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {f.firm_information.firm_name} — {f.account_details.account_name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-4 py-2 text-sm font-medium text-gray-900">Score</td>
                    {selected.map((f) => (
                      <td key={idFor(f)} className="px-4 py-2 text-sm text-gray-900">{computeScore(f)}</td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

function diffHint(key: string, firms: Firm[], winner: Firm) {
  const w = winner.score ?? computeScore(winner);
  return `Higher score = better fit; this view highlights where the leading option wins.`;
}
