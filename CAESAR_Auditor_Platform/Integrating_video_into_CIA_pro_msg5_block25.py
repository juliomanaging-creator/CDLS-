// CDLS_NextSteps.jsx
import { useState } from "react";

const phases = [
  {
    phase: "PHASE 1", label: "IMMEDIATE (March–April 2026)", color: "#ff2222",
    items: [
      { priority: "🔴 CRITICAL", task: "DFPI Banking Compliance Filing", who: "Julio + CA Securities Counsel", deadline: "April 15, 2026", why: "July 1, 2026 deadline — must file 75+ days early for processing", action: "Engage Pearlman Schneider or equiv CA securities attorney TODAY. File LP registration with DFPI." },
      { priority: "🔴 CRITICAL", task: "Lock In IRA §45W Pre-Certifications", who: "Julio + Tax Counsel", deadline: "April 30, 2026", why: "Federal rollback risk — lock in credits before EO implementation", action: "File IRS Form 8936 pre-certifications for all 20 pilot trucks. Engage tax counsel specializing in clean vehicle credits." },
      { priority: "🔴 CRITICAL", task: "HVIP Voucher Application Prep", who: "CDLS Operations", deadline: "September 9, 2026 (prep NOW)", why: "$330K/truck — first-come, first-served, funds run out fast", action: "Pre-register at HVIP portal. Have all truck specs, dealer agreements, and financial statements ready 30 days before opening." },
      { priority: "🟠 HIGH", task: "Engage Crypto/Securities Counsel for Token Legal Opinion", who: "Julio + Crypto Attorney", deadline: "May 15, 2026", why: "SEC regulation risk — Howey Test analysis needed before any token marketing", action: "Engage Perkins Coie, Cooley, or Fenwick for utility token legal opinion. Budget $25–50K. Critical before any investor or public token discussion." },
      { priority: "🟠 HIGH", task: "Implement Attorney-Client Privilege Protocol", who: "Julio + Outside Counsel", deadline: "April 30, 2026", why: "All regulatory strategy documents must be properly privileged", action: "Establish retainer with regulatory counsel. Restructure all sensitive communications through counsel. Brief team on privilege protocol." },
    ]
  },
  {
    phase: "PHASE 2", label: "SHORT-TERM (May–August 2026)", color: "#f39c12",
    items: [
      { priority: "🟠 HIGH", task: "SMUD V2G Interconnection Application", who: "CDLS Energy Team", deadline: "June 30, 2026", why: "First-mover advantage in dealer-owned VPP space — cannot wait", action: "Submit SMUD Rule 21 interconnection application for Sacramento pilot depot. Engage utility interconnection consultant." },
      { priority: "🟠 HIGH", task: "CalPERS Formal Investment Presentation", who: "Julio + Investment Counsel", deadline: "June 2026", why: "$5M anchor investment validates institutional credibility for all subsequent raises", action: "Deliver institutional-grade deck with blockchain-verified financial data. Structure as Emerging Manager Program application." },
      { priority: "🟡 MEDIUM", task: "UC System Academic Validation Partnership", who: "Julio + UC Liaison", deadline: "July 2026", why: "Protects IP, validates algorithms, prevents VC exposure risk", action: "Approach UC Davis EV Research Center, UC Berkeley Transportation Institute. Propose funded research partnership on AI routing algorithms." },
      { priority: "🟡 MEDIUM", task: "CNCDA Dealer Onboarding Campaign Launch", who: "CDLS Business Dev", deadline: "August 2026", why: "816 dealers targeted — need pipeline building 12+ months before scale", action: "Present at CNCDA annual conference. Deploy tokenized equity pitch: dealers own the platform they're paying for." },
      { priority: "🟡 MEDIUM", task: "CESAR AI Agent Deployment — Full 8-Agent Stack", who: "CDLS Tech Team", deadline: "July 2026", why: "HVIP requires operational documentation — AI must be live", action: "Complete Ollama deployment of all 8 agents. Run 30-day Monte Carlo simulation validation. Document for institutional audit trail." },
    ]
  },
  {
    phase: "PHASE 3", label: "MEDIUM-TERM (Sept 2026–Q2 2027)", color: "#27ae60",
    items: [
      { priority: "🟢 STRATEGIC", task: "HVIP Voucher Applications — September 9, 2026", who: "Julio + CDLS Operations", deadline: "Sept 9, 2026 OPEN", why: "$6.6M for first 20 trucks — this single event transforms capital structure", action: "Submit fully prepared applications at 8:00AM on September 9. Have backup submitter. This is the single most important day of 2026." },
      { priority: "🟢 STRATEGIC", task: "Token Launch — $CDLS Governance", who: "CDLS Tech + Legal", deadline: "Q4 2026", why: "Converts 5K dealer network from customer base to equity-holding community", action: "After legal opinion secured, deploy smart contracts. Initial distribution to founding 20 dealers. Set governance framework." },
      { priority: "🟢 STRATEGIC", task: "Series A Capital Raise — $12–15M", who: "Julio + Investment Bank", deadline: "Q1 2027", why: "Scale from 100 to 500 trucks requires institutional capital", action: "Target pension funds, family offices, green infrastructure funds. Use CalPERS participation as institutional validation anchor." },
      { priority: "🟡 MEDIUM", task: "National Resilience Initiative — Modular Housing Pilot", who: "Julio + Policy Partners", deadline: "Q2 2027", why: "$4.13B royalty projection requires national scale beyond CA logistics", action: "Submit federal HUD grant application. Partner with V2G housing developers. 300,000 unit target begins with 500-unit Sacramento pilot." },
      { priority: "🟡 MEDIUM", task: "Statewide Battery Pod Deployment", who: "CDLS + SMUD Partners", deadline: "Q1 2027", why: "Portable V2G units multiply grid income without adding trucks", action: "Deploy 50 portable battery pod units statewide. Establish charging depot network at dealer lots. Begin CAISO demand response enrollment." },
    ]
  },
];

export default function NextSteps() {
  const [activePhase, setActivePhase] = useState(0);
  const [expanded, setExpanded] = useState(null);

  return (
    <div style={{ background: "#050a14", minHeight: "100vh", fontFamily: "Arial", color: "white", padding: "20px" }}>
      <div style={{ background: "linear-gradient(135deg, #0d1b33, #1a0d2a)", borderRadius: "12px", padding: "18px 24px", marginBottom: "20px", border: "1px solid #00d4ff" }}>
        <div style={{ fontSize: "22px", fontWeight: "bold", color: "#00d4ff" }}>🚀 CDLS NEXT STEPS — ACTION ROADMAP</div>
        <div style={{ color: "#80c8ff", fontSize: "12px", marginTop: "4px" }}>Implementing Regulatory Capture Wealth Strategy | CIA Program | March 2026</div>
        <div style={{ display: "flex", gap: "16px", marginTop: "14px" }}>
          <div style={{ background: "#1a0505", padding: "8px 14px", borderRadius: "8px", border: "1px solid #ff2222" }}>
            <div style={{ color: "#ff4444", fontSize: "20px", fontWeight: "bold" }}>3</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>Critical Actions</div>
          </div>
          <div style={{ background: "#1a0d00", padding: "8px 14px", borderRadius: "8px", border: "1px solid #f39c12" }}>
            <div style={{ color: "#f5c842", fontSize: "20px", fontWeight: "bold" }}>$6.6M</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>HVIP Potential (20 trucks)</div>
          </div>
          <div style={{ background: "#0d1a0d", padding: "8px 14px", borderRadius: "8px", border: "1px solid #27ae60" }}>
            <div style={{ color: "#2ecc71", fontSize: "20px", fontWeight: "bold" }}>Sept 9</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>HVIP Opens 2026</div>
          </div>
          <div style={{ background: "#1a0d2a", padding: "8px 14px", borderRadius: "8px", border: "1px solid #9b59b6" }}>
            <div style={{ color: "#cc88ff", fontSize: "20px", fontWeight: "bold" }}>July 1</div>
            <div style={{ color: "#aaa", fontSize: "10px" }}>Banking Deadline 2026</div>
          </div>
        </div>
      </div>

      {/* Phase tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
        {phases.map((p, i) => (
          <button key={i} onClick={() => setActivePhase(i)}
            style={{ flex: 1, padding: "12px", borderRadius: "8px", border: `2px solid ${activePhase === i ? p.color : "#1e3a5f"}`, background: activePhase === i ? p.color + "22" : "#070d1a", color: activePhase === i ? p.color : "#aaa", cursor: "pointer", fontWeight: activePhase === i ? "bold" : "normal", fontSize: "12px" }}>
            <div>{p.phase}</div>
            <div style={{ fontSize: "10px", marginTop: "2px", opacity: 0.8 }}>{p.label}</div>
          </button>
        ))}
      </div>

      {/* Action items */}
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {phases[activePhase].items.map((item, i) => (
          <div key={i} onClick={() => setExpanded(expanded === i ? null : i)}
            style={{ background: "#070d1a", border: `1px solid ${phases[activePhase].color}44`, borderRadius: "10px", padding: "14px 16px", cursor: "pointer" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", gap: "10px", alignItems: "center", marginBottom: "4px" }}>
                  <span style={{ fontSize: "11px" }}>{item.priority}</span>
                  <span style={{ fontSize: "13px", fontWeight: "bold", color: "#e0e0e0" }}>{item.task}</span>
                </div>
                <div style={{ display: "flex", gap: "16px", fontSize: "11px", color: "#556" }}>
                  <span>👤 {item.who}</span>
                  <span style={{ color: phases[activePhase].color }}>📅 {item.deadline}</span>
                </div>
              </div>
              <span style={{ color: "#556", fontSize: "14px", marginLeft: "12px" }}>{expanded === i ? "▲" : "▼"}</span>
            </div>
            {expanded === i && (
              <div style={{ marginTop: "12px", borderTop: `1px solid ${phases[activePhase].color}33`, paddingTop: "12px" }}>
                <div style={{ marginBottom: "8px" }}>
                  <div style={{ color: "#f5c842", fontSize: "11px", marginBottom: "4px" }}>WHY THIS MATTERS:</div>
                  <div style={{ color: "#c8d8f0", fontSize: "12px", lineHeight: "1.6" }}>{item.why}</div>
                </div>
                <div>
                  <div style={{ color: "#00d4ff", fontSize: "11px", marginBottom: "4px" }}>⚡ SPECIFIC ACTION:</div>
                  <div style={{ color: "#80ffb0", fontSize: "12px", lineHeight: "1.6", background: "#0a1f35", padding: "10px", borderRadius: "6px" }}>{item.action}</div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "24px", background: "#0d1b33", borderRadius: "10px", padding: "16px", border: "1px solid #1e3a5f" }}>
        <div style={{ color: "#00d4ff", fontSize: "13px", fontWeight: "bold", marginBottom: "8px" }}>🎬 VIDEO PRINCIPLE: "The Wealth Game Requires Positioning Before Capital"</div>
        <div style={{ color: "#80c8ff", fontSize: "12px", lineHeight: "1.8" }}>
          Every action above follows the video's core teaching: secure your position in the regulatory flow before spending your own capital. 
          HVIP vouchers, LCFS credits, V2G income, and IRA tax credits collectively represent <strong style={{color:"#00ff88"}}>$395K+ per truck in third-party funding</strong> — 
          the regulatory system is funding CDLS's fleet. Your job is to be the first to submit the paperwork, establish the relationships, and operate within the framework.
          This is the "wealth game from nothing" — not earning from scratch, but capturing what's already flowing.
        </div>
      </div>

      <div style={{ marginTop: "16px", textAlign: "center", color: "#334", fontSize: "10px" }}>
        CONFIDENTIAL — CDLS / California Investment Auto, LP | Julio Umanzor, CEO & Managing Partner | March 2026
      </div>
    </div>
  );
}