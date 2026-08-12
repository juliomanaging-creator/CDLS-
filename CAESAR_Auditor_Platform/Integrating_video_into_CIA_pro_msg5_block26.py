// CDLS_IncentiveTracker.jsx
import { useState } from "react";

const trucks = [
  { id: 1, vin: "CDLS-T001", model: "Tesla Semi", depot: "Sacramento HQ", status: "Active", hvip: 330000, ira45w: 40000, lcfs_annual: 18000, v2g_annual: 32000, acquisition: 720000 },
  { id: 2, vin: "CDLS-T002", model: "Tesla Semi", depot: "Sacramento HQ", status: "Active", hvip: 330000, ira45w: 40000, lcfs_annual: 18000, v2g_annual: 32000, acquisition: 720000 },
  { id: 3, vin: "CDLS-T003", model: "Tesla Semi", depot: "Sacramento HQ", status: "Pending", hvip: 330000, ira45w: 40000, lcfs_annual: 18000, v2g_annual: 32000, acquisition: 720000 },
];

const regulations_financial = [
  { id: 1, program: "HVIP Voucher", agency: "CARB/CALSTA", per_unit: 330000, units: 20, total: 6600000, timing: "At purchase", deadline: "Sept 9, 2026", status: "APPLY", risk: "Low", notes: "First-come, first-served. Funds deplete fast." },
  { id: 2, program: "IRA §45W Clean Veh. Credit", agency: "IRS Federal", per_unit: 40000, units: 20, total: 800000, timing: "Tax year", deadline: "Pre-certify now", status: "APPLY", risk: "Medium", notes: "Political rollback risk. Lock in ASAP." },
  { id: 3, program: "LCFS Credits (Annual)", agency: "CARB", per_unit: 18000, units: 20, total: 360000, timing: "Quarterly", deadline: "Ongoing", status: "ACTIVE", risk: "Low", notes: "$24.68/haul × ~730 hauls/year per truck." },
  { id: 4, program: "V2G / SMUD Income (Annual)", agency: "SMUD", per_unit: 31500, units: 20, total: 630000, timing: "Monthly", deadline: "Apply now", status: "PENDING", risk: "Low", notes: "Avg $18K–$45K/truck. Interconnect immediately." },
  { id: 5, program: "CAISO Demand Response", agency: "CAISO", per_unit: 8000, units: 20, total: 160000, timing: "Event-based", deadline: "Enroll Q3 2026", status: "PENDING", risk: "Low", notes: "$50–150/MWh during peak events." },
  { id: 6, program: "IRA §30C EV Infrastructure", agency: "IRS Federal", per_unit: 15000, units: 5, total: 75000, timing: "At install", deadline: "2032", status: "PLAN", risk: "Medium", notes: "30% credit on charging depot install." },
  { id: 7, program: "LCFS Credits — Carbon Offset", agency: "CARB", per_unit: 6468, units: 20, total: 129360, timing: "Quarterly", deadline: "Ongoing", status: "ACTIVE", risk: "Low", notes: "Blockchain tokenization ($CARBON) multiplies value." },
];

const fmt = n => "$" + n.toLocaleString();

export default function IncentiveTracker() {
  const [view, setView] = useState("incentives");

  const totalIncentives = regulations_financial.reduce((s, r) => s + r.total, 0);
  const perTruckGross = 720000;
  const perTruckIncentives = (330000 + 40000);
  const perTruckNet = perTruckGross - perTruckIncentives;
  const annualPassive = 360000 + 630000 + 160000;

  return (
    <div style={{ background: "#050a14", minHeight: "100vh", fontFamily: "'Courier New', monospace", color: "white", padding: "16px" }}>
      <div style={{ background: "#0d1b33", borderRadius: "10px", padding: "16px 20px", marginBottom: "16px", border: "1px solid #00d4ff" }}>
        <div style={{ fontSize: "18px", fontWeight: "bold", color: "#00d4ff" }}>📊 CDLS INCENTIVE STACKING FINANCIAL TRACKER</div>
        <div style={{ color: "#80c8ff", fontSize: "11px" }}>Regulatory Capture Wealth Model | California Investment Auto, LP | EXCEL EQUIVALENT</div>
        <div style={{ display: "flex", gap: "10px", marginTop: "12px", flexWrap: "wrap" }}>
          {[
            ["Total Incentives Available", fmt(totalIncentives), "#00ff88"],
            ["Per Truck: Gross Cost", fmt(perTruckGross), "#aaa"],
            ["Per Truck: After Credits", fmt(perTruckNet), "#00d4ff"],
            ["Net Cost Reduction", "55%", "#f5c842"],
            ["Annual Passive/Truck", fmt(annualPassive / 20), "#cc88ff"],
          ].map(([label, val, color]) => (
            <div key={label} style={{ background: "#070d1a", padding: "10px 16px", borderRadius: "8px", border: `1px solid ${color}44` }}>
              <div style={{ color, fontSize: "18px", fontWeight: "bold" }}>{val}</div>
              <div style={{ color: "#556", fontSize: "10px" }}>{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* View toggle */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "14px" }}>
        {[["incentives", "💰 Incentive Stack"], ["projections", "📈 10-Year Projection"]].map(([v, l]) => (
          <button key={v} onClick={() => setView(v)}
            style={{ padding: "8px 16px", borderRadius: "6px", border: `1px solid ${view === v ? "#00d4ff" : "#1e3a5f"}`, background: view === v ? "#0d1b33" : "#070d1a", color: view === v ? "#00d4ff" : "#aaa", cursor: "pointer", fontSize: "12px" }}>
            {l}
          </button>
        ))}
      </div>

      {view === "incentives" && (
        <div style={{ overflowX: "auto" }}>
          {/* Excel-style header */}
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1.5fr 1fr 1fr 1fr 1fr 1fr 1.5fr", gap: 0, fontSize: "10px", borderBottom: "2px solid #1e3a5f" }}>
            {["Program", "Agency", "Per Unit", "Units", "Total Value", "Timing", "Deadline", "Status"].map(h => (
              <div key={h} style={{ background: "#0d1b33", color: "#00d4ff", padding: "8px 10px", fontWeight: "bold", borderRight: "1px solid #1e3a5f" }}>{h}</div>
            ))}
          </div>
          {regulations_financial.map((r, i) => (
            <div key={r.id} style={{ display: "grid", gridTemplateColumns: "2fr 1.5fr 1fr 1fr 1fr 1fr 1fr 1.5fr", gap: 0, fontSize: "11px", background: i % 2 === 0 ? "#070d1a" : "#090f1f", borderBottom: "1px solid #111" }}>
              <div style={{ padding: "8px 10px", color: "#e0e0e0", borderRight: "1px solid #111" }}>
                <div style={{ fontWeight: "500" }}>{r.program}</div>
                <div style={{ color: "#445", fontSize: "9px", marginTop: "2px" }}>{r.notes}</div>
              </div>
              <div style={{ padding: "8px 10px", color: "#80c8ff", borderRight: "1px solid #111" }}>{r.agency}</div>
              <div style={{ padding: "8px 10px", color: "#00ff88", textAlign: "right", borderRight: "1px solid #111" }}>{fmt(r.per_unit)}</div>
              <div style={{ padding: "8px 10px", color: "#aaa", textAlign: "center", borderRight: "1px solid #111" }}>{r.units}</div>
              <div style={{ padding: "8px 10px", color: "#f5c842", fontWeight: "bold", textAlign: "right", borderRight: "1px solid #111" }}>{fmt(r.total)}</div>
              <div style={{ padding: "8px 10px", color: "#aaa", fontSize: "10px", borderRight: "1px solid #111" }}>{r.timing}</div>
              <div style={{ padding: "8px 10px", color: r.deadline.includes("2026") ? "#ff6b35" : "#aaa", fontSize: "10px", borderRight: "1px solid #111" }}>{r.deadline}</div>
              <div style={{ padding: "8px 10px" }}>
                <span style={{ background: r.status === "ACTIVE" ? "#27ae6022" : r.status === "APPLY" ? "#e74c3c22" : "#f39c1222", color: r.status === "ACTIVE" ? "#27ae60" : r.status === "APPLY" ? "#ff6b35" : "#f5c842", padding: "2px 8px", borderRadius: "10px", fontSize: "10px", fontWeight: "bold" }}>{r.status}</span>
              </div>
            </div>
          ))}
          {/* Totals row */}
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1.5fr 1fr 1fr 1fr 1fr 1fr 1.5fr", background: "#0d1b33", borderTop: "2px solid #00d4ff", fontSize: "12px", fontWeight: "bold" }}>
            <div style={{ padding: "10px", color: "#00d4ff", gridColumn: "1/5" }}>TOTAL INCENTIVE STACK (20 Trucks, Year 1)</div>
            <div style={{ padding: "10px", color: "#00ff88", textAlign: "right" }}>{fmt(totalIncentives)}</div>
            <div style={{ gridColumn: "6/-1" }}/>
          </div>
        </div>
      )}

      {view === "projections" && (
        <div>
          {[
            { yr: 1, trucks: 20, hauling: 2100000, lcfs: 360000, v2g: 630000, caiso: 160000, token: 0, note: "Pilot - Sacramento" },
            { yr: 2, trucks: 60, hauling: 6300000, lcfs: 1080000, v2g: 1890000, caiso: 480000, token: 5000000, note: "3-Region Expansion" },
            { yr: 3, trucks: 120, hauling: 12600000, lcfs: 2160000, v2g: 3780000, caiso: 960000, token: 25000000, note: "Series A Deployed" },
            { yr: 5, trucks: 300, hauling: 31500000, lcfs: 5400000, v2g: 9450000, caiso: 2400000, token: 150000000, note: "State-wide Coverage" },
            { yr: 10, trucks: 750, hauling: 78750000, lcfs: 13500000, v2g: 23625000, caiso: 6000000, token: 2000000000, note: "National Scale" },
          ].map((row, i) => {
            const total = row.hauling + row.lcfs + row.v2g + row.caiso + row.token;
            return (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "0.5fr 0.5fr 1fr 0.8fr 0.8fr 0.8fr 1.2fr 1.2fr 1fr", gap: 0, background: i % 2 === 0 ? "#070d1a" : "#090f1f", borderBottom: "1px solid #111", fontSize: "11px", alignItems: "center" }}>
                {i === 0 && false}
                <div style={{ padding: "10px 8px", color: "#00d4ff", fontWeight: "bold" }}>Yr {row.yr}</div>
                <div style={{ padding: "10px 8px", color: "#aaa" }}>{row.trucks}</div>
                <div style={{ padding: "10px 8px", color: "#80c8ff" }}>{fmt(row.hauling)}</div>
                <div style={{ padding: "10px 8px", color: "#27ae60" }}>{fmt(row.lcfs)}</div>
                <div style={{ padding: "10px 8px", color: "#00ff88" }}>{fmt(row.v2g)}</div>
                <div style={{ padding: "10px 8px", color: "#3498db" }}>{fmt(row.caiso)}</div>
                <div style={{ padding: "10px 8px", color: "#9b59b6" }}>{fmt(row.token)}</div>
                <div style={{ padding: "10px 8px", color: "#f5c842", fontWeight: "bold" }}>{fmt(total)}</div>
                <div style={{ padding: "10px 8px", color: "#445", fontSize: "10px" }}>{row.note}</div>
              </div>
            );
          })}
          <div style={{ marginTop: "4px", padding: "8px 10px", fontSize: "10px", color: "#445" }}>
            Columns: Year | Trucks | Hauling Rev | LCFS Credits | V2G Income | CAISO Demand Response | Token Value | TOTAL | Notes
          </div>
        </div>
      )}

      <div style={{ marginTop: "20px", background: "#0d1b33", borderRadius: "8px", padding: "14px", border: "1px solid #1e3a5f" }}>
        <div style={{ color: "#00d4ff", fontSize: "12px", fontWeight: "bold", marginBottom: "6px" }}>📌 KEY INSIGHT FROM VIDEO + CDLS DATA</div>
        <div style={{ color: "#80c8ff", fontSize: "11px", lineHeight: "1.8" }}>
          Starting from nothing means the first 20 trucks are 55% funded by HVIP + IRA credits ($7.4M of $14.4M fleet cost). 
          V2G + LCFS passive income then funds trucks 21–60 organically. By Year 3, token appreciation ($25M) exceeds total operational investment. 
          This is the "regulatory capture" wealth game — you don't earn your way to scale, you position into the incentive flow.
        </div>
      </div>
    </div>
  );
}