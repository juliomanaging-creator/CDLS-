import React, { useState, useMemo } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from 'recharts';

// CDLS Financial Model Data
const baseData = {
  assumptions: {
    haulRate: 1200,
    carbonPrice: 85,
    co2PerHaul: 0.29,
    vehicleCapacity: 9,
    truckCost: 180000,
    trailerCost: 65000,
    driverCost: 338,
    electricCost: 21,
    maintenanceCost: 15,
    insuranceCost: 8,
    dealerShare: 0.65,
    platformShare: 0.20,
    investorShare: 0.15,
    discountRate: 0.18,
    exitMultiple: 8,
  },
  yearlyData: [
    { year: 'Year 1', champions: 200, hauls: 28800, revenue: 34.9, co2Saved: 290, grossMargin: 0.683 },
    { year: 'Year 2', champions: 600, hauls: 86400, revenue: 106, co2Saved: 1158, grossMargin: 0.685 },
    { year: 'Year 3', champions: 1500, hauls: 216000, revenue: 264, co2Saved: 3522, grossMargin: 0.688 },
    { year: 'Year 4', champions: 3000, hauls: 432000, revenue: 528, co2Saved: 7610, grossMargin: 0.690 },
    { year: 'Year 5', champions: 5000, hauls: 720000, revenue: 880, co2Saved: 13390, grossMargin: 0.692 },
  ],
  monthlyY1: [
    { month: 'Jan', champions: 20, hauls: 240, revenue: 0.29 },
    { month: 'Feb', champions: 35, hauls: 420, revenue: 0.50 },
    { month: 'Mar', champions: 50, hauls: 600, revenue: 0.72 },
    { month: 'Apr', champions: 70, hauls: 840, revenue: 1.01 },
    { month: 'May', champions: 100, hauls: 1200, revenue: 1.44 },
    { month: 'Jun', champions: 120, hauls: 1440, revenue: 1.73 },
    { month: 'Jul', champions: 140, hauls: 1680, revenue: 2.02 },
    { month: 'Aug', champions: 160, hauls: 1920, revenue: 2.30 },
    { month: 'Sep', champions: 180, hauls: 2160, revenue: 2.59 },
    { month: 'Oct', champions: 190, hauls: 2280, revenue: 2.74 },
    { month: 'Nov', champions: 195, hauls: 2340, revenue: 2.81 },
    { month: 'Dec', champions: 200, hauls: 2400, revenue: 2.88 },
  ],
  scenarios: [
    { name: 'Bear', irr: 8.2, moic: 1.5, networkY5: 2500, exitMult: 5 },
    { name: 'Base', irr: 22.3, moic: 2.5, networkY5: 5000, exitMult: 8 },
    { name: 'Bull', irr: 78.4, moic: 120, networkY5: 7500, exitMult: 12 },
  ],
  tokenDistribution: [
    { name: 'Founders', value: 30, tokens: 1500000 },
    { name: 'Investors', value: 20, tokens: 1000000 },
    { name: 'Rewards', value: 30, tokens: 1500000 },
    { name: 'Treasury', value: 20, tokens: 1000000 },
  ],
  costBreakdown: [
    { name: 'Driver', value: 338, pct: 88.5 },
    { name: 'Electric', value: 21, pct: 5.5 },
    { name: 'Maintenance', value: 15, pct: 3.9 },
    { name: 'Insurance', value: 8, pct: 2.1 },
  ],
};

const COLORS = {
  primary: '#1a5f2a',
  secondary: '#2d8a4e',
  accent: '#f4a932',
  light: '#e8f5e9',
  blue: '#1976d2',
  purple: '#7b1fa2',
  orange: '#f57c00',
  red: '#d32f2f',
  teal: '#00897b',
};

const CHART_COLORS = ['#1a5f2a', '#2d8a4e', '#4caf50', '#81c784', '#a5d6a7'];
const PIE_COLORS = ['#1a5f2a', '#f4a932', '#1976d2', '#7b1fa2'];

const KPICard = ({ title, value, subtitle, trend, trendValue, icon, color = COLORS.primary }) => (
  <div className="bg-white rounded-lg p-4 shadow-md" style={{ borderLeft: `4px solid ${color}` }}>
    <div className="flex justify-between items-start">
      <div>
        <div className="text-xs text-gray-500 uppercase tracking-wide">{title}</div>
        <div className="text-2xl font-bold mt-1" style={{ color }}>{value}</div>
        {subtitle && <div className="text-xs text-gray-400 mt-1">{subtitle}</div>}
      </div>
      <div className="text-2xl">{icon}</div>
    </div>
    {trend && (
      <div className={`mt-2 text-xs flex items-center gap-1 ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
        {trend === 'up' ? '↑' : '↓'} {trendValue}
      </div>
    )}
  </div>
);

const ChartCard = ({ title, children, height = 280 }) => (
  <div className="bg-white rounded-lg p-4 shadow-md" style={{ height }}>
    <div className="text-sm font-semibold text-gray-700 mb-3">{title}</div>
    {children}
  </div>
);

export default function CDLSDashboard() {
  const [selectedScenario, setSelectedScenario] = useState('Base');
  const [activeTab, setActiveTab] = useState('overview');

  const currentScenario = baseData.scenarios.find(s => s.name === selectedScenario);
  
  const totalRevenue = baseData.yearlyData.reduce((sum, d) => sum + d.revenue, 0);
  const totalCO2 = baseData.yearlyData.reduce((sum, d) => sum + d.co2Saved, 0);
  const avgMargin = baseData.yearlyData.reduce((sum, d) => sum + d.grossMargin, 0) / 5;

  const cumulativeData = baseData.yearlyData.map((d, i) => ({
    ...d,
    cumulativeRevenue: baseData.yearlyData.slice(0, i + 1).reduce((s, x) => s + x.revenue, 0),
    cumulativeCO2: baseData.yearlyData.slice(0, i + 1).reduce((s, x) => s + x.co2Saved, 0),
  }));

  const irrSensitivity = [
    { dealers: 2500, irr: 8.2 },
    { dealers: 3500, irr: 15.2 },
    { dealers: 5000, irr: 22.3 },
    { dealers: 6500, irr: 31.8 },
    { dealers: 8000, irr: 42.5 },
  ];

  const tabs = [
    { id: 'overview', label: '📊 Overview' },
    { id: 'financial', label: '💰 Financial' },
    { id: 'operations', label: '🚚 Operations' },
    { id: 'esg', label: '🌱 ESG Impact' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="text-white p-4" style={{ background: `linear-gradient(135deg, ${COLORS.primary} 0%, ${COLORS.secondary} 100%)` }}>
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold">🏆 CDLS Environmental Champions</h1>
            <p className="text-sm opacity-90">Financial Model Dashboard | California Dealer Logistics Solutions</p>
          </div>
          <div className="flex gap-3 items-center">
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="px-3 py-2 rounded text-sm bg-white/20 border-none text-white cursor-pointer"
            >
              <option value="Bear" className="text-gray-800">🐻 Bear Case</option>
              <option value="Base" className="text-gray-800">📊 Base Case</option>
              <option value="Bull" className="text-gray-800">🐂 Bull Case</option>
            </select>
            <div className="bg-white/20 px-3 py-2 rounded text-xs">Last Updated: Jan 2026</div>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white border-b flex px-4">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 text-sm transition-all ${
              activeTab === tab.id 
                ? 'font-semibold border-b-2' 
                : 'text-gray-500'
            }`}
            style={{ 
              color: activeTab === tab.id ? COLORS.primary : undefined,
              borderColor: activeTab === tab.id ? COLORS.primary : 'transparent'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div className="p-4">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
          <KPICard title="Projected IRR" value={`${currentScenario.irr}%`} subtitle={`${selectedScenario} Case`} trend="up" trendValue="vs 12% avg" icon="📈" color={COLORS.primary} />
          <KPICard title="MOIC" value={`${currentScenario.moic}x`} subtitle="Multiple on Capital" trend="up" trendValue="Target: 2.5x+" icon="💎" color={COLORS.accent} />
          <KPICard title="Y5 Network" value={currentScenario.networkY5.toLocaleString()} subtitle="Champions" trend="up" trendValue="25x growth" icon="🏆" color={COLORS.blue} />
          <KPICard title="CO₂ Saved" value={`${(totalCO2/1000).toFixed(1)}K MT`} subtitle="5-Year Total" trend="up" trendValue="$2.2M credits" icon="🌱" color={COLORS.teal} />
          <KPICard title="Gross Margin" value={`${(avgMargin*100).toFixed(1)}%`} subtitle="Platform Avg" trend="up" trendValue="vs 50% ind" icon="📊" color={COLORS.purple} />
        </div>

        {activeTab === 'overview' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
              <div className="md:col-span-2">
                <ChartCard title="📈 Revenue & Network Growth (5-Year)" height={300}>
                  <ResponsiveContainer width="100%" height="90%">
                    <ComposedChart data={baseData.yearlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                      <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                      <YAxis yAxisId="left" tick={{ fontSize: 11 }} tickFormatter={(v) => `$${v}M`} />
                      <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Legend />
                      <Bar yAxisId="left" dataKey="revenue" fill={COLORS.primary} name="Revenue ($M)" radius={[4,4,0,0]} />
                      <Line yAxisId="right" type="monotone" dataKey="champions" stroke={COLORS.accent} strokeWidth={3} name="Champions" dot={{ fill: COLORS.accent, r: 4 }} />
                    </ComposedChart>
                  </ResponsiveContainer>
                </ChartCard>
              </div>
              <ChartCard title="🎯 Scenario Analysis (IRR)" height={300}>
                <ResponsiveContainer width="100%" height="90%">
                  <BarChart data={baseData.scenarios} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                    <XAxis type="number" tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                    <YAxis type="category" dataKey="name" tick={{ fontSize: 11 }} width={45} />
                    <Tooltip formatter={(v) => [`${v}%`, 'IRR']} />
                    <Bar dataKey="irr" radius={[0,4,4,0]}>
                      {baseData.scenarios.map((entry, index) => (
                        <Cell key={index} fill={index === 0 ? COLORS.red : index === 1 ? COLORS.primary : COLORS.accent} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <ChartCard title="🪙 Token Distribution ($CDLS)" height={260}>
                <ResponsiveContainer width="100%" height="90%">
                  <PieChart>
                    <Pie data={baseData.tokenDistribution} cx="50%" cy="50%" innerRadius={45} outerRadius={75} paddingAngle={2} dataKey="value" label={({name, value}) => `${name}: ${value}%`} labelLine={{ stroke: '#999' }}>
                      {baseData.tokenDistribution.map((entry, index) => (<Cell key={index} fill={PIE_COLORS[index]} />))}
                    </Pie>
                    <Tooltip formatter={(v) => [`${v}%`, 'Share']} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="💵 Cost Structure (Per Haul)" height={260}>
                <ResponsiveContainer width="100%" height="90%">
                  <PieChart>
                    <Pie data={baseData.costBreakdown} cx="50%" cy="50%" innerRadius={45} outerRadius={75} paddingAngle={2} dataKey="value" label={({name, value}) => `${name}: $${value}`} labelLine={{ stroke: '#999' }}>
                      {baseData.costBreakdown.map((entry, index) => (<Cell key={index} fill={CHART_COLORS[index]} />))}
                    </Pie>
                    <Tooltip formatter={(v) => [`$${v}`, 'Cost']} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="📊 IRR Sensitivity (Dealers)" height={260}>
                <ResponsiveContainer width="100%" height="90%">
                  <AreaChart data={irrSensitivity}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                    <XAxis dataKey="dealers" tick={{ fontSize: 10 }} tickFormatter={(v) => `${(v/1000).toFixed(1)}K`} />
                    <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => `${v}%`} />
                    <Tooltip formatter={(v) => [`${v}%`, 'IRR']} labelFormatter={(v) => `${v.toLocaleString()} Champions`} />
                    <Area type="monotone" dataKey="irr" stroke={COLORS.primary} fill={COLORS.light} strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>
          </>
        )}

        {activeTab === 'financial' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
              <ChartCard title="💰 Cumulative Revenue Growth" height={280}>
                <ResponsiveContainer width="100%" height="90%">
                  <AreaChart data={cumulativeData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                    <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `$${v}M`} />
                    <Tooltip formatter={(v) => [`$${v.toFixed(0)}M`, 'Cumulative']} />
                    <Area type="monotone" dataKey="cumulativeRevenue" stroke={COLORS.primary} fill={COLORS.light} strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </ChartCard>
              <ChartCard title="📅 Year 1 Monthly Ramp" height={280}>
                <ResponsiveContainer width="100%" height="90%">
                  <ComposedChart data={baseData.monthlyY1}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                    <XAxis dataKey="month" tick={{ fontSize: 9 }} />
                    <YAxis yAxisId="left" tick={{ fontSize: 10 }} />
                    <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10 }} tickFormatter={(v) => `$${v}M`} />
                    <Tooltip />
                    <Bar yAxisId="left" dataKey="champions" fill={COLORS.secondary} name="Champions" radius={[2,2,0,0]} />
                    <Line yAxisId="right" type="monotone" dataKey="revenue" stroke={COLORS.accent} strokeWidth={2} name="Revenue" />
                  </ComposedChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>
            <ChartCard title="📋 Unit Economics Summary" height={140}>
              <div className="grid grid-cols-4 gap-3 pt-2">
                {[
                  { label: 'Revenue/Haul', value: '$1,204.94', sub: 'Base + Carbon' },
                  { label: 'Variable Cost', value: '$382.00', sub: 'All costs' },
                  { label: 'Gross Profit', value: '$822.94', sub: '68.3% Margin' },
                  { label: 'Contribution', value: '$42.94', sub: 'After dealer share' },
                ].map((m, i) => (
                  <div key={i} className="text-center p-3 rounded-lg" style={{ background: COLORS.light }}>
                    <div className="text-xs text-gray-500 mb-1">{m.label}</div>
                    <div className="text-lg font-bold" style={{ color: COLORS.primary }}>{m.value}</div>
                    <div className="text-xs text-gray-400">{m.sub}</div>
                  </div>
                ))}
              </div>
            </ChartCard>
          </>
        )}

        {activeTab === 'operations' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
              <div className="md:col-span-2">
                <ChartCard title="🚚 Haul Volume Projections" height={280}>
                  <ResponsiveContainer width="100%" height="90%">
                    <BarChart data={baseData.yearlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                      <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${(v/1000).toFixed(0)}K`} />
                      <Tooltip formatter={(v) => [v.toLocaleString(), 'Annual Hauls']} />
                      <Bar dataKey="hauls" fill={COLORS.blue} name="Hauls" radius={[4,4,0,0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>
              </div>
              <ChartCard title="⚡ Fleet Metrics" height={280}>
                <div className="pt-1">
                  {[
                    { label: 'Tesla Semi Trucks', value: '50', icon: '🚛' },
                    { label: 'Aluminum Trailers', value: '50', icon: '📦' },
                    { label: 'Vehicle Capacity', value: '9/load', icon: '🚗' },
                    { label: 'Avg Distance', value: '350 mi', icon: '📍' },
                    { label: 'Utilization', value: '85%', icon: '📊' },
                    { label: 'On-Time Rate', value: '97.3%', icon: '✅' },
                  ].map((item, i) => (
                    <div key={i} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                      <span className="flex items-center gap-2 text-xs text-gray-600">
                        <span>{item.icon}</span>{item.label}
                      </span>
                      <span className="font-semibold text-sm" style={{ color: COLORS.primary }}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </ChartCard>
            </div>
          </>
        )}

        {activeTab === 'esg' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
              <div className="md:col-span-2">
                <ChartCard title="🌱 Cumulative CO₂ Reduction (MT)" height={280}>
                  <ResponsiveContainer width="100%" height="90%">
                    <AreaChart data={cumulativeData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                      <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${(v/1000).toFixed(0)}K`} />
                      <Tooltip formatter={(v) => [`${v.toLocaleString()} MT`, 'CO₂ Saved']} />
                      <Area type="monotone" dataKey="cumulativeCO2" stroke={COLORS.teal} fill="#b2dfdb" strokeWidth={2} />
                    </AreaChart>
                  </ResponsiveContainer>
                </ChartCard>
              </div>
              <ChartCard title="🌍 ESG Impact" height={280}>
                <div className="pt-1">
                  {[
                    { label: '5-Year CO₂ Saved', value: '25,970 MT', icon: '🌱' },
                    { label: 'Equivalent Trees', value: '1.2M', icon: '🌳' },
                    { label: 'Carbon Credits', value: '$2.2M', icon: '💚' },
                    { label: 'Dealers Empowered', value: '5,000', icon: '🏆' },
                    { label: 'Capital Freed', value: '$900M', icon: '💰' },
                    { label: 'Jobs Created', value: '250+', icon: '👷' },
                  ].map((item, i) => (
                    <div key={i} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                      <span className="flex items-center gap-2 text-xs text-gray-600">
                        <span>{item.icon}</span>{item.label}
                      </span>
                      <span className="font-semibold text-sm" style={{ color: COLORS.teal }}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </ChartCard>
            </div>
          </>
        )}

        {/* Footer */}
        <div className="mt-4 p-3 bg-white rounded-lg flex justify-between items-center text-xs text-gray-500">
          <div><strong>CDLS Environmental Champions</strong> | California Dealer Logistics Solutions, LP</div>
          <div>Julio Umanzor, Managing Partner | Sacramento, CA | January 2026</div>
          <div className="px-3 py-1 rounded text-xs font-medium" style={{ background: COLORS.light, color: COLORS.primary }}>
            Prospective Analysis
          </div>
        </div>
      </div>
    </div>
  );
}