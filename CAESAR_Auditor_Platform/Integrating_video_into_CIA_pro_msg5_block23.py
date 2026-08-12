// CDLS_RegulatoryDatabase.jsx
import { useState } from "react";

const regulations = [
  { id: 1, name: "Advanced Clean Fleets (ACF)", agency: "CARB", type: "Mandate", status: "ACTIVE", threat: "Low", opportunity: "Critical", deadline: "40% ZEV 2024 / 75% 2035", impact: "Core compliance driver — CDLS IS the solution", section: "Sec. 17 CCR", privilege: "Attorney-Client" },
  { id: 2, name: "HVIP Voucher Program", agency: "CARB/CALSTA", type: "Incentive", status: "ACTIVE", threat: "None", opportunity: "Critical", deadline: "Sept 9, 2026", impact: "$330K/truck — 91% cost offset. First-mover essential.", section: "H&SC 44274", privilege: "Work Product" },
  { id: 3, name: "LCFS Credit Program", agency: "CARB", type: "Revenue", status: "ACTIVE", threat: "Low", opportunity: "High", deadline: "Ongoing quarterly", impact: "$24.68/haul passive income. Blockchain verification enhances value.", section: "17 CCR §95480", privilege: "Work Product" },
  { id: 4, name: "IRA §45W Clean Commercial Vehicle", agency: "IRS/Federal", type: "Tax Credit", status: "ACTIVE", threat: "Medium", opportunity: "Critical", deadline: "Through 2032", impact: "$7,500–$40K/truck federal credit stack.", section: "IRC §45W", privilege: "Attorney-Client" },
  { id: 5, name: "SMUD V2G Interconnection", agency: "SMUD", type: "Grid Program", status: "PENDING", threat: "Low", opportunity: "High", deadline: "Application ASAP", impact: "$18K–$45K/truck/year energy arbitrage revenue.", section: "CPUC Rule 21", privilege: "Work Product" },
  { id: 6, name: "SB 1 (Road Repair)", agency: "CA Legislature", type: "Fee Regulation", status: "ACTIVE", threat: "Low", opportunity: "Medium", deadline: "Ongoing", impact: "Diesel surcharges benefit ZEV operators competitively.", section: "SB 1 (2017)", privilege: "None" },
  { id: 7, name: "AB 2061 (Clean Fleet Tax Credit)", agency: "CA Legislature", type: "Tax Incentive", status: "MONITORING", threat: "Low", opportunity: "High", deadline: "TBD 2026", impact: "Proposed additional state credit stack layer.", section: "Pending", privilege: "Attorney-Client" },
  { id: 8, name: "CARB ACF Enforcement", agency: "CARB", type: "Enforcement", status: "ACTIVE", threat: "High", opportunity: "Medium", deadline: "Ongoing", impact: "Non-compliant fleets = our customers. Enforcement drives demand.", section: "13 CCR §2013", privilege: "Attorney-Client" },
  { id: 9, name: "Federal Motor Carrier Safety (FMCSA)", agency: "DOT/FMCSA", type: "Safety Reg", status: "ACTIVE", threat: "Medium", opportunity: "Low", deadline: "Ongoing", impact: "ELD mandates, Hours of Service — Tesla Semi autonomous compliance.", section: "49 CFR Part 395", privilege: "Work Product" },
  { id: 10, name: "CA Banking Compliance", agency: "DFPI", type: "Financial Reg", status: "CRITICAL", threat: "High", opportunity: "Medium", deadline: "July 1, 2026", impact: "LP structure must qualify. Delaware LP + CA registration required.", section: "CA Corp Code §15900", privilege: "Attorney-Client" },
  { id: 11, name: "Reg D / 506(c) Securities", agency: "SEC", type: "Securities", status: "ACTIVE", threat: "High", opportunity: "Low", deadline: "Per offering", impact: "Private placement structure. Accredited investor requirements.", section: "17 CFR §230.506", privilege: "Attorney-Client" },
  { id: 12, name: "ERISA Plan Asset Rules", agency: "DOL", type: "Fiduciary", status: "ACTIVE", threat: "High", opportunity: "Low", deadline: "Ongoing", impact: "CalPERS investment — must stay below 25% benefit plan investor threshold.", section: "ERISA §3(42)", privilege: "Attorney-Client" },
  { id: 13, name: "IRA §30C Alt Fuel Infrastructure", agency: "IRS", type: "Tax Credit", status: "ACTIVE", threat: "None", opportunity: "High", deadline: "Through 2032", impact: "30% credit on charging infrastructure installation.", section: "IRC §30C", privilege: "Work Product" },
  { id: 14, name: "CA SB 100 (100% Clean Energy)", agency: "CA Legislature", type: "Energy Policy", status: "ACTIVE", threat: "Low", opportunity: "High", deadline: "100% by 2045", impact: "V2G grid services become more valuable as grid decarbonizes.", section: "SB 100 (2018)", privilege: "None" },
  { id: 15, name: "CAISO Demand Response Programs", agency: "CAISO", type: "Grid Services", status: "ACTIVE", threat: "Low", opportunity: "High", deadline: "Enrollment windows", impact: "Peak load revenue $50-150/MWh during demand events.", section: "CAISO Tariff §34", privilege: "Work Product" },
  { id: 16, name: "AB 1279 (Climate Crisis Act)", agency: "CA Legislature", type: "Climate Mandate", status: "ACTIVE", threat: "Low", opportunity: "High", deadline: "Carbon neutral 2045", impact: "Strengthens LCFS credit value long-term.", section: "AB 1279 (2022)", privilege: "None" },
  { id: 17, name: "Federal Autonomous Vehicle Policy", agency: "NHTSA", type: "Safety/Tech", status: "EVOLVING", threat: "Medium", opportunity: "High", deadline: "2027-2030 expected", impact: "Tesla FSD commercial deployment — route efficiency gains.", section: "NHTSA AV Guidance", privilege: "Work Product" },
  { id: 18, name: "SEC Crypto Asset Guidance", agency: "SEC", type: "Securities", status: "EVOLVING", threat: "High", opportunity: "Medium", deadline: "2026 expected", impact: "$CDLS/$HAUL/$CARBON token classification — utility vs security distinction critical.", section: "SEC DAO Report", privilege: "Attorney-Client" },
  { id: 19, name: "CA SB 253 (Climate Disclosure)", agency: "CA Legislature", type: "Reporting", status: "ACTIVE", threat: "Low", opportunity: "Medium", deadline: "Annual reporting", impact: "CDLS blockchain records satisfy Scope 3 emissions reporting.", section: "SB 253 (2023)", privilege: "None" },
  { id: 20, name: "Trump EO — IRA Rollback Risk", agency: "Federal Executive", type: "Political Risk", status: "MONITORING", threat: "Critical", opportunity: "None", deadline: "Ongoing 2025-2026", impact: "IRA §45W credit rollback could reduce $40K/truck credit. Hedge via state programs.", section: "EO 14154 (2025)", privilege: "Attorney-Client" },
];

const threatColors = { "Critical": "#ff2222", "High": "#ff6b35", "Medium": "#f39c12", "Low": "#27ae60", "None": "#2ecc71" };
const oppColors = { "Critical": "#00d4ff", "High": "#00ff88", "Medium": "#f5c842", "Low": "#95a5a6" };
const statusColors = { "ACTIVE": "#27ae60", "CRITICAL": "#ff2222", "PENDING": "#f39c12", "MONITORING": "#3498db", "EVOLVING": "#9b59b6" };

export default function RegulatoryDatabase() {
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [sort, setSort] = useState("id");

  const filtered = regulations
    .filter(r => filter === "All" || r.threat === filter || r.opportunity === filter || r.status === filter)
    .filter(r => !search || r.name.toLowerCase().includes(search.toLowerCase()) || r.agency.toLowerCase().includes(search.toLowerCase()) || r.impact.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => a[sort] > b[sort] ? 1 : -1);

  const threatCount = { Critical: 0, High: 0, Medium: 0, Low: 0 };
  regulations.forEach(r => { if (threatCount[r.threat] !== undefined) threatCount[r.threat]++; });

  return (
    <div style={{ background: "#050a14", minHeight: "100vh", fontFamily: "Arial", color: "white", padding: "16px" }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0d1b33, #1a3a6e)", borderRadius: "12px", padding: "16px 20px", marginBottom: "16px", border: "1px solid #00d4ff" }}>
        <div style={{ fontSize: "20px", fontWeight: "bold", color: "#00d4ff" }}>⚖️ CDLS REGULATORY INTELLIGENCE DATABASE</div>
        <div style={{ color: "#80c8ff", fontSize: "12px", marginTop: "4px" }}>Legal Privilege Framework | California Investment Auto, LP | CONFIDENTIAL</div>
        <div style={{ display: "flex", gap: "20px", marginTop: "12px", flexWrap: "wrap" }}>
          {Object.entries(threatCount).map(([level, count]) => (
            <div key={level} style={{ background: "#0a1525", padding: "8px 14px", borderRadius: "8px", border: `1px solid ${threatColors[level]}` }}>
              <div style={{ color: threatColors[level], fontSize: "18px", fontWeight: "bold" }}>{count}</div>
              <div style={{ color: "#aaa", fontSize: "10px" }}>{level} Threat</div>
            </div>
          ))}
          <div style={{ background: "#0a1525", padding: "8px 14px", borderRadius: "8px", border: "1px solid #9b59b6" }}>
            <div style={{ color: "#cc88ff", fontSize: "18px", fontWeight: "bold" }}>{regulations.filter(r => r.privilege === "Attorney-Client").length}</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>Atty-Client Privileged</div>
          </div>
          <div style={{ background: "#0a1525", padding: "8px 14px", borderRadius: "8px", border: "1px solid #f39c12" }}>
            <div style={{ color: "#f5c842", fontSize: "18px", fontWeight: "bold" }}>{regulations.filter(r => r.privilege === "Work Product").length}</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>Work Product Protected</div>
          </div>
        </div>
      </div>

      {/* Legal Privilege Notice */}
      <div style={{ background: "#1a0505", border: "2px solid #ff2222", borderRadius: "8px", padding: "10px 14px", marginBottom: "14px", fontSize: "11px", color: "#ff9090" }}>
        <strong>⚠️ ATTORNEY-CLIENT PRIVILEGE NOTICE:</strong> Items marked "Attorney-Client" are prepared in anticipation of litigation or regulatory proceedings and are subject to legal privilege. Do not disclose without counsel authorization. Items marked "Work Product" are protected under the work product doctrine. This database constitutes privileged legal strategy analysis.
      </div>

      {/* Controls */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "14px", flexWrap: "wrap", alignItems: "center" }}>
        <input
          placeholder="🔍 Search regulations, agencies, impact..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, minWidth: "250px", padding: "8px 12px", background: "#0a1525", border: "1px solid #1e3a5f", borderRadius: "6px", color: "white", fontSize: "12px" }}
        />
        {["All", "Critical", "High", "ACTIVE", "MONITORING", "EVOLVING"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "6px 12px", borderRadius: "6px", border: `1px solid ${filter === f ? "#00d4ff" : "#333"}`, background: filter === f ? "#1a3a6e" : "#0a1525", color: filter === f ? "#00d4ff" : "#aaa", cursor: "pointer", fontSize: "11px" }}>
            {f}
          </button>
        ))}
      </div>

      {/* Table */}
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px" }}>
          <thead>
            <tr style={{ background: "#0d1b33", borderBottom: "2px solid #1e3a5f" }}>
              {["#", "Regulation / Bill", "Agency", "Type", "Status", "Threat Level", "Opportunity", "Key Deadline", "Privilege"].map(h => (
                <th key={h} style={{ padding: "10px 8px", textAlign: "left", color: "#00d4ff", whiteSpace: "nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((r, i) => (
              <tr key={r.id} onClick={() => setSelected(selected?.id === r.id ? null : r)}
                style={{ background: i % 2 === 0 ? "#070d1a" : "#090f1f", cursor: "pointer", borderBottom: "1px solid #111", transition: "background 0.2s" }}
                onMouseEnter={e => e.currentTarget.style.background = "#0d1b33"}
                onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? "#070d1a" : "#090f1f"}>
                <td style={{ padding: "8px", color: "#556" }}>{r.id}</td>
                <td style={{ padding: "8px", color: "#e0e0e0", fontWeight: "500", maxWidth: "200px" }}>{r.name}</td>
                <td style={{ padding: "8px", color: "#80c8ff" }}>{r.agency}</td>
                <td style={{ padding: "8px", color: "#aaa" }}>{r.type}</td>
                <td style={{ padding: "8px" }}><span style={{ background: statusColors[r.status] + "33", color: statusColors[r.status], padding: "2px 7px", borderRadius: "10px", fontSize: "10px", fontWeight: "bold" }}>{r.status}</span></td>
                <td style={{ padding: "8px" }}><span style={{ background: threatColors[r.threat] + "22", color: threatColors[r.threat], padding: "2px 7px", borderRadius: "10px", fontSize: "10px", fontWeight: "bold" }}>{r.threat}</span></td>
                <td style={{ padding: "8px" }}><span style={{ background: oppColors[r.opportunity] + "22", color: oppColors[r.opportunity], padding: "2px 7px", borderRadius: "10px", fontSize: "10px", fontWeight: "bold" }}>{r.opportunity}</span></td>
                <td style={{ padding: "8px", color: r.threat === "Critical" ? "#ff6b35" : "#aaa", fontSize: "10px" }}>{r.deadline}</td>
                <td style={{ padding: "8px" }}><span style={{ background: r.privilege === "Attorney-Client" ? "#9b59b622" : r.privilege === "Work Product" ? "#f39c1222" : "#33333322", color: r.privilege === "Attorney-Client" ? "#cc88ff" : r.privilege === "Work Product" ? "#f5c842" : "#666", padding: "2px 6px", borderRadius: "8px", fontSize: "9px" }}>{r.privilege || "None"}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detail Panel */}
      {selected && (
        <div style={{ marginTop: "16px", background: "#0d1b33", border: `2px solid ${threatColors[selected.threat]}`, borderRadius: "10px", padding: "16px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
            <div style={{ fontSize: "16px", fontWeight: "bold", color: "#00d4ff" }}>{selected.name}</div>
            <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", color: "#666", cursor: "pointer", fontSize: "16px" }}>✕</button>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px", fontSize: "12px" }}>
            <div><div style={{ color: "#556" }}>Agency</div><div style={{ color: "#80c8ff" }}>{selected.agency}</div></div>
            <div><div style={{ color: "#556" }}>Code Section</div><div style={{ color: "#aaa" }}>{selected.section}</div></div>
            <div><div style={{ color: "#556" }}>Privilege Status</div><div style={{ color: selected.privilege === "Attorney-Client" ? "#cc88ff" : "#f5c842" }}>{selected.privilege}</div></div>
            <div style={{ gridColumn: "1/-1" }}><div style={{ color: "#556", marginBottom: "4px" }}>Strategic Impact Analysis</div><div style={{ color: "#e0e0e0", lineHeight: "1.6", padding: "8px", background: "#050a14", borderRadius: "6px" }}>{selected.impact}</div></div>
            <div style={{ gridColumn: "1/-1", background: "#1a0505", padding: "8px", borderRadius: "6px", fontSize: "11px", color: "#ff9090" }}>
              ⚖️ <strong>Legal Action Required:</strong> Verify current status with outside counsel before acting. Regulatory landscape may have changed. This analysis is privileged strategy — not legal advice.
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: "20px", textAlign: "center", color: "#334", fontSize: "10px" }}>
        CONFIDENTIAL — Attorney-Client Privilege / Work Product Protection | CDLS / California Investment Auto, LP | Julio Umanzor, Managing Partner | March 2026
      </div>
    </div>
  );
}