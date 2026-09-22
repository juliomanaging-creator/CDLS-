import React, { useState, useEffect } from 'react';

export default function GrantDashboard() {
  const [metrics, setMetrics] = useState({
    total_grants: 0,
    active_grants: 0,
    total_allocated_usd: 0,
    remaining_balance_usd: 0
  });
  const [grants, setGrants] = useState([]);

  useEffect(() => {
    // Fetch metrics and grant listings from your FastAPI backend
    fetch('/api/dashboard/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error("Error fetching metrics:", err));

    fetch('/api/grants')
      .then(res => res.json())
      .then(data => setGrants(data))
      .catch(err => console.error("Error fetching grants:", err));
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">CDLS Grant Command Center</h1>
        <p className="text-slate-400">Secure institutional grant tracking and automated RAG vetting.</p>
      </header>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <p className="text-sm font-medium text-slate-400">Total Allocated</p>
          <p className="text-2xl font-semibold mt-2">${metrics.total_allocated_usd.toLocaleString()}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <p className="text-sm font-medium text-slate-400">Remaining Balance</p>
          <p className="text-2xl font-semibold mt-2 text-emerald-400">${metrics.remaining_balance_usd.toLocaleString()}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <p className="text-sm font-medium text-slate-400">Active Grants</p>
          <p className="text-2xl font-semibold mt-2">{metrics.active_grants}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <p className="text-sm font-medium text-slate-400">Security Sentinel</p>
          <p className="text-2xl font-semibold mt-2 text-blue-400">100 / 100</p>
        </div>
      </div>

      {/* Grant Table Section */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden shadow-xl">
        <div className="p-6 border-b border-slate-700">
          <h2 className="text-xl font-semibold">Active Pilot Disbursals</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-wider">
                <th className="p-4">Grant Name</th>
                <th className="p-4">Agency Source</th>
                <th className="p-4">Amount</th>
                <th className="p-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700 text-sm">
              {grants.length > 0 ? (
                grants.map((g) => (
                  <tr key={g.id} className="hover:bg-slate-700/50 transition-colors">
                    <td className="p-4 font-medium">{g.grant_name}</td>
                    <td className="p-4 text-slate-300">{g.agency_source}</td>
                    <td className="p-4 text-emerald-400">${Number(g.total_amount).toLocaleString()}</td>
                    <td className="p-4">
                      <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {g.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="p-6 text-center text-slate-400">No active records loaded. Connect backend database.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}