// CDLS_VideoFrameworkExplanations.jsx
import { useState } from "react";

const sections = [
  {
    id: 1, icon: "🎬", title: "VIDEO CONCEPT: The Wealth Game from Nothing",
    color: "#00ff88",
    content: `The video "If You Start With Nothing, This is the Only Wealth Game That Works" presents a foundational wealth-building principle: when you lack starting capital, your competitive edge must come from capturing systemic advantages others overlook — specifically, regulatory flows, institutional incentives, and structural arbitrage opportunities that are publicly available but require positioning to access.

The key insight is: regulations create cash flows. Most entrepreneurs see regulations as obstacles. The sophisticated player sees them as rivers of money — HVIP vouchers, tax credits, carbon markets, grid incentives — all flowing toward whoever positions first.

The "wealth game from nothing" becomes: Position your company inside the regulatory framework so that compliance mandates create your revenue, rather than cost.`,
  },
  {
    id: 2, icon: "⚡", title: "HOW CDLS ALREADY IMPLEMENTS THIS",
    color: "#00d4ff",
    content: `CDLS has intuited this principle and built an entire platform around it. Here is the direct mapping:

VIDEO PRINCIPLE → CDLS IMPLEMENTATION:

1. "Start with regulatory incentives as free capital"
   → HVIP vouchers cover $330K/truck | IRA §45W adds $40K | LCFS generates $24.68/haul
   → Net result: $720K Tesla Semi costs $325K after stacking = 55% funded by regulation

2. "Become the solution to the regulatory problem"
   → Advanced Clean Fleets mandates 40% ZEV by 2024, 75% by 2035
   → 1,200 CA dealers need to comply — CDLS IS the compliance infrastructure
   → Dealers don't just use CDLS — they NEED it to stay legal

3. "Create recurring income from regulatory participation"
   → SMUD V2G interconnection: $18K–$45K/truck/year passive income
   → CAISO demand response: grid services revenue during peak events
   → LCFS credits: ongoing passive carbon income per haul

4. "Build network effects that compound like equity"
   → Each dealer who joins reduces costs for all (network effect)
   → Blockchain tokenomics ($CDLS, $HAUL, $CARBON) convert network to tradeable equity
   → 1,000 dealers in 10 years traditional → 5,000 dealers in 3 years with tokens`,
  },
  {
    id: 3, icon: "🏛️", title: "LEGAL PRIVILEGE FRAMEWORK",
    color: "#9b59b6",
    content: `LEGAL PRIVILEGE NOTICE: This section constitutes attorney-client privileged strategy prepared in anticipation of regulatory proceedings.

The "regulatory capture" concept from the video must be implemented with a clear legal privilege framework. There are two forms of capture relevant to CDLS:

1. LEGITIMATE REGULATORY CAPTURE (Legal & Beneficial)
   — Becoming so embedded in CARB, CALSTA, SMUD processes that regulations are written around your operational model
   — CNCDA partnership creates lobbying influence over ACF implementation timing
   — Academic UC validation protects IP while shaping regulatory narrative
   — Institutional investor presence (CalPERS) signals regulatory legitimacy

2. LEGAL PRIVILEGE CAPTURE (Protective Strategy)
   — All regulatory analysis structured through outside counsel
   — Regulatory database classifications: Attorney-Client (litigation anticipation) vs. Work Product (strategy)
   — Rolling privilege review quarterly with transactional attorneys
   — Communications about threat regulations to always cc: counsel

3. PROACTIVE REGULATORY ENGAGEMENT
   — File comments on all relevant CARB rulemakings (builds record)
   — Maintain direct relationships with CARB, CALSTA, DFPI staff
   — Structure every dealer contract to reference regulatory compliance as purpose
   — This creates a legal moat: competitors cannot copy compliance relationships`,
  },
  {
    id: 4, icon: "🔴", title: "CRITICAL THREAT ANALYSIS: Bills That Could Stop Us",
    color: "#ff6b35",
    content: `ATTORNEY-CLIENT PRIVILEGED — FOR LEGAL REVIEW

Current Priority Threats Requiring Counsel Monitoring:

1. FEDERAL IRA ROLLBACK (Trump EO 14154 - CRITICAL THREAT)
   Risk: IRA §45W credit ($40K/truck) may be reduced or eliminated
   Probability: 40% within 24 months based on political trajectory
   Mitigation: Accelerate HVIP applications before federal changes (CA state program is insulated)
   Action: Lock in all federal credits NOW via pre-certification with IRS

2. SEC CRYPTO REGULATION (Token Classification - HIGH THREAT)
   Risk: $CDLS/$HAUL/$CARBON tokens classified as securities = full SEC registration
   Probability: 60% broader crypto legislation passes by 2027
   Mitigation: Structure tokens as utility-first from day one; obtain legal opinion on Howey Test
   Action: Engage Perkins Coie or similar crypto-specialized counsel immediately

3. CARB ACF IMPLEMENTATION DELAYS (MEDIUM THREAT)
   Risk: Enforcement delays reduce dealer urgency to join CDLS
   Probability: 30% — CARB has delayed before (light-duty vehicle regs)
   Mitigation: Offer V2G income as value prop independent of compliance
   Action: Market the income story, not just the compliance story

4. CA BANKING COMPLIANCE FAILURE (CRITICAL - JULY 1, 2026)
   Risk: LP fails to register properly with DFPI by deadline
   Probability: Low if action taken now — HIGH if delayed past April 2026
   Mitigation: Engage CA-licensed securities attorney to handle DFPI registration
   Action: IMMEDIATE — File by April 15, 2026 to allow processing time`,
  },
  {
    id: 5, icon: "📈", title: "FINANCIAL PROJECTIONS — REGULATORY ARBITRAGE MODEL",
    color: "#f5c842",
    content: `The video's core financial model: "When you start with nothing, use other people's money (regulations, grants, incentives) to build your base, then layer recurring revenue on top."

CDLS REGULATORY ARBITRAGE FINANCIAL MODEL:

YEAR 1 — PILOT (Sacramento, 100 trailers):
• Hauling Revenue: $2.1M (estimated)
• HVIP Voucher Value Received: $6.6M (20 trucks × $330K)
• LCFS Credits: $180K (7,300 hauls × $24.68)
• V2G Income: $360K–$900K (20 trucks)
• Net Capital Required After Credits: ~$325K/truck vs $720K gross
• Effective Return on Capital: 280% adjusted

YEAR 3 — SCALE (5 regions):
• Hauling Revenue: $24M
• Carbon/LCFS Income: $2.2M
• V2G Revenue: $5.4M–$13.5M
• Token Value: $50M–$150M (network effect)
• Royalties to CA: $412M/year trajectory

10-YEAR PLATFORM:
• $4.13B total royalties to California
• $2–3B enterprise value (token appreciation)
• $389M CNCDA value created
• 60.7% reduction in CA state tax obligations
• 300,000 modular housing units (National Resilience Initiative)

KEY PRINCIPLE FROM VIDEO APPLIED:
"The first dollar is the hardest — after that, the system funds itself."
CDLS version: After first 20 trucks funded via HVIP, V2G income funds the next 20.`,
  },
];

export default function ExplanationsDoc() {
  const [active, setActive] = useState(1);
  const sec = sections.find(s => s.id === active);

  return (
    <div style={{ background: "#050a14", minHeight: "100vh", fontFamily: "Arial", color: "white", display: "flex" }}>
      {/* Sidebar */}
      <div style={{ width: "260px", minHeight: "100vh", background: "#070d1a", borderRight: "1px solid #1e3a5f", padding: "16px", flexShrink: 0 }}>
        <div style={{ fontSize: "14px", fontWeight: "bold", color: "#00d4ff", marginBottom: "6px" }}>CDLS FRAMEWORK</div>
        <div style={{ fontSize: "10px", color: "#556", marginBottom: "20px" }}>Video Integration + CIA Program</div>
        {sections.map(s => (
          <div key={s.id} onClick={() => setActive(s.id)}
            style={{ padding: "10px 12px", marginBottom: "6px", borderRadius: "8px", cursor: "pointer", background: active === s.id ? "#0d1b33" : "transparent", border: `1px solid ${active === s.id ? s.color : "#1e3a5f"}`, borderLeft: `3px solid ${active === s.id ? s.color : "#1e3a5f"}` }}>
            <div style={{ fontSize: "11px", fontWeight: active === s.id ? "bold" : "normal", color: active === s.id ? s.color : "#aaa" }}>{s.icon} {s.title.split(":")[0]}</div>
          </div>
        ))}
        <div style={{ marginTop: "30px", padding: "10px", background: "#0d1b33", borderRadius: "8px", fontSize: "10px", color: "#556" }}>
          <div style={{ color: "#ff9090", marginBottom: "4px" }}>⚖️ LEGAL NOTICE</div>
          Sections marked Attorney-Client are privileged. Do not share without counsel approval.
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, padding: "24px", overflowY: "auto" }}>
        <div style={{ maxWidth: "800px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "20px" }}>
            <div style={{ fontSize: "36px" }}>{sec.icon}</div>
            <div>
              <div style={{ fontSize: "20px", fontWeight: "bold", color: sec.color }}>{sec.title}</div>
              <div style={{ fontSize: "11px", color: "#556", marginTop: "2px" }}>CDLS / California Investment Auto, LP | CONFIDENTIAL</div>
            </div>
          </div>
          <div style={{ background: "#0a1525", border: `1px solid ${sec.color}30`, borderRadius: "10px", padding: "24px", lineHeight: "1.8", fontSize: "13px", color: "#c8d8f0", whiteSpace: "pre-wrap" }}>
            {sec.content}
          </div>

          {sec.id === 4 && (
            <div style={{ marginTop: "16px", background: "#1a0505", border: "2px solid #ff2222", borderRadius: "8px", padding: "14px", fontSize: "11px", color: "#ff9090" }}>
              <strong>ATTORNEY-CLIENT PRIVILEGE — PREPARED IN ANTICIPATION OF LITIGATION</strong><br/>
              This threat analysis was prepared at the direction of counsel in anticipation of potential regulatory enforcement proceedings. Distribution restricted to authorized personnel only. Contact Julio Umanzor before forwarding.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}