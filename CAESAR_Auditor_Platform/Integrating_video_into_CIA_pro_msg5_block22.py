// CDLS_MindMap.jsx
import { useState } from "react";

export default function CDLSMindMap() {
  const [hover, setHover] = useState(null);
  
  const nodes = {
    center: { x: 700, y: 450, label: ["REGULATORY", "CAPTURE", "WEALTH MOAT"], sub: "CDLS Core CIA Strategy" },
    incentive: { x: 350, y: 200, label: ["INCENTIVE", "STACKING"], color: "#00d4ff" },
    v2g: { x: 1050, y: 200, label: ["V2G ENERGY", "BANKING"], color: "#00ff88" },
    tokens: { x: 1150, y: 450, label: ["BLOCKCHAIN", "TOKENOMICS"], color: "#9b59b6" },
    legal: { x: 950, y: 710, label: ["LEGAL PRIVILEGE", "CAPTURE"], color: "#ff6b35" },
    dealer: { x: 450, y: 710, label: ["DEALER", "NETWORK MOAT"], color: "#f39c12" },
    arbitrage: { x: 250, y: 450, label: ["TRIPLE", "ARBITRAGE"], color: "#e74c3c" },
  };

  return (
    <div style={{ background: "#050a14", minHeight: "100vh", padding: "10px", fontFamily: "Arial" }}>
      <div style={{ textAlign: "center", color: "#00d4ff", fontSize: "18px", fontWeight: "bold", padding: "10px 0 4px" }}>
        CDLS / CIA PROGRAM — REGULATORY CAPTURE WEALTH STRATEGY
      </div>
      <div style={{ textAlign: "center", color: "#7ab0e0", fontSize: "11px", marginBottom: "8px" }}>
        Integrated from: "If You Start With Nothing, This is the Only Wealth Game That Works"
      </div>
      <svg viewBox="0 0 1400 880" style={{ width: "100%", height: "auto" }}>
        <defs>
          <radialGradient id="bg"><stop offset="0%" stopColor="#0d1b33"/><stop offset="100%" stopColor="#050a14"/></radialGradient>
          <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect width="1400" height="880" fill="url(#bg)"/>

        {/* Connection lines */}
        {[
          [700,420, 390,230], [700,420, 1010,230], [760,450, 1100,450],
          [760,500, 980,690], [640,500, 490,690], [600,450, 310,450]
        ].map(([x1,y1,x2,y2],i) => (
          <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#00d4ff" strokeWidth="2" strokeOpacity="0.4"/>
        ))}

        {/* Central Node */}
        <ellipse cx="700" cy="450" rx="110" ry="72" fill="#1a3a6e" stroke="#00d4ff" strokeWidth="3" filter="url(#glow)"/>
        <text x="700" y="432" fill="white" fontSize="13" fontWeight="bold" textAnchor="middle">REGULATORY</text>
        <text x="700" y="450" fill="white" fontSize="13" fontWeight="bold" textAnchor="middle">CAPTURE</text>
        <text x="700" y="468" fill="white" fontSize="13" fontWeight="bold" textAnchor="middle">WEALTH MOAT</text>
        <text x="700" y="484" fill="#00d4ff" fontSize="9" fontStyle="italic" textAnchor="middle">CDLS Core CIA Strategy</text>

        {/* INCENTIVE STACKING */}
        <ellipse cx="350" cy="200" rx="90" ry="50" fill="#0d2a4a" stroke="#00d4ff" strokeWidth="2" filter="url(#glow)"/>
        <text x="350" y="195" fill="#00d4ff" fontSize="11" fontWeight="bold" textAnchor="middle">INCENTIVE</text>
        <text x="350" y="212" fill="#00d4ff" fontSize="11" fontWeight="bold" textAnchor="middle">STACKING</text>
        {/* sub-items */}
        <rect x="60" y="72" width="185" height="54" rx="8" fill="#0a1f35" stroke="#38b6ff" strokeWidth="1.5"/>
        <text x="153" y="92" fill="#a0cfff" fontSize="9" textAnchor="middle">HVIP Vouchers</text>
        <text x="153" y="106" fill="#a0cfff" fontSize="9" textAnchor="middle">$330K/Tesla Semi Truck</text>
        <text x="153" y="118" fill="#ff6b35" fontSize="9" textAnchor="middle">Sept 9, 2026 Deadline</text>
        <line x1="245" y1="125" x2="290" y2="165" stroke="#38b6ff" strokeWidth="1" strokeOpacity="0.5"/>

        <rect x="250" y="65" width="185" height="54" rx="8" fill="#0a1f35" stroke="#38b6ff" strokeWidth="1.5"/>
        <text x="343" y="85" fill="#a0cfff" fontSize="9" textAnchor="middle">IRA §45W Tax Credit</text>
        <text x="343" y="99" fill="#a0cfff" fontSize="9" textAnchor="middle">$7,500–$40K per truck</text>
        <text x="343" y="113" fill="#a0cfff" fontSize="9" textAnchor="middle">Federal stacking layer</text>
        <line x1="343" y1="119" x2="343" y2="155" stroke="#38b6ff" strokeWidth="1" strokeOpacity="0.5"/>

        <rect x="440" y="68" width="165" height="54" rx="8" fill="#0a1f35" stroke="#38b6ff" strokeWidth="1.5"/>
        <text x="523" y="88" fill="#a0cfff" fontSize="9" textAnchor="middle">LCFS Credits</text>
        <text x="523" y="102" fill="#a0cfff" fontSize="9" textAnchor="middle">$24.68/haul passive</text>
        <text x="523" y="116" fill="#a0cfff" fontSize="9" textAnchor="middle">CARB verified income</text>
        <line x1="480" y1="122" x2="415" y2="165" stroke="#38b6ff" strokeWidth="1" strokeOpacity="0.5"/>

        {/* V2G ENERGY */}
        <ellipse cx="1050" cy="200" rx="90" ry="50" fill="#0d2a4a" stroke="#00ff88" strokeWidth="2" filter="url(#glow)"/>
        <text x="1050" y="195" fill="#00ff88" fontSize="11" fontWeight="bold" textAnchor="middle">V2G ENERGY</text>
        <text x="1050" y="212" fill="#00ff88" fontSize="11" fontWeight="bold" textAnchor="middle">BANKING</text>
        <rect x="950" y="65" width="195" height="54" rx="8" fill="#0a1f35" stroke="#00cc66" strokeWidth="1.5"/>
        <text x="1048" y="85" fill="#80ffb0" fontSize="9" textAnchor="middle">SMUD Virtual Power Plant</text>
        <text x="1048" y="99" fill="#80ffb0" fontSize="9" textAnchor="middle">$18K–$45K/truck/year</text>
        <text x="1048" y="113" fill="#80ffb0" fontSize="9" textAnchor="middle">First-mover dealer VPP</text>
        <line x1="1048" y1="119" x2="1048" y2="152" stroke="#00cc66" strokeWidth="1" strokeOpacity="0.5"/>

        {/* BLOCKCHAIN TOKENOMICS */}
        <ellipse cx="1150" cy="450" rx="88" ry="50" fill="#1a0d2a" stroke="#9b59b6" strokeWidth="2" filter="url(#glow)"/>
        <text x="1150" y="444" fill="#cc88ff" fontSize="11" fontWeight="bold" textAnchor="middle">BLOCKCHAIN</text>
        <text x="1150" y="461" fill="#cc88ff" fontSize="11" fontWeight="bold" textAnchor="middle">TOKENOMICS</text>
        {[
          [1240,350,"$CDLS Governance","5K dealer voting rights"],
          [1250,455,"$HAUL Utility","Route & load access"],
          [1240,550,"$CARBON Credits","ZK proof verified"],
        ].map(([x,y,t1,t2],i) => (
          <g key={i}>
            <rect x={x} y={y-18} width="148" height="44" rx="7" fill="#0a1f35" stroke="#7b2dbf" strokeWidth="1.5"/>
            <text x={x+74} y={y+2} fill="#e0c0ff" fontSize="9" textAnchor="middle">{t1}</text>
            <text x={x+74} y={y+18} fill="#c0a0ef" fontSize="8" textAnchor="middle">{t2}</text>
          </g>
        ))}
        {[[1230,365],[1238,458],[1228,552]].map(([x,y],i) => <line key={i} x1={x} y1={y} x2="1200" y2="450" stroke="#9b59b6" strokeWidth="1" strokeOpacity="0.4"/>)}

        {/* LEGAL PRIVILEGE CAPTURE */}
        <ellipse cx="950" cy="710" rx="100" ry="52" fill="#1a1a0d" stroke="#ff6b35" strokeWidth="2" filter="url(#glow)"/>
        <text x="950" y="703" fill="#ff8c55" fontSize="11" fontWeight="bold" textAnchor="middle">LEGAL PRIVILEGE</text>
        <text x="950" y="720" fill="#ff8c55" fontSize="11" fontWeight="bold" textAnchor="middle">CAPTURE</text>
        {[
          [820,795,"ACF Compliance Shield","40%→75% ZEV mandate"],
          [1000,800,"CARB Multi-Agency","July 1, 2026 banking deadline"],
          [1135,785,"Reg Threat Database","Bills that help vs block"],
        ].map(([x,y,t1,t2],i) => (
          <g key={i}>
            <rect x={x-90} y={y-16} width="180" height="44" rx="7" fill="#1a0d05" stroke="#cc4400" strokeWidth="1.5"/>
            <text x={x} y={y+4} fill="#ffaa80" fontSize="9" textAnchor="middle">{t1}</text>
            <text x={x} y={y+18} fill="#dd8860" fontSize="8" textAnchor="middle">{t2}</text>
          </g>
        ))}

        {/* DEALER NETWORK MOAT */}
        <ellipse cx="450" cy="710" rx="95" ry="52" fill="#1a1200" stroke="#f39c12" strokeWidth="2" filter="url(#glow)"/>
        <text x="450" y="703" fill="#f5c842" fontSize="11" fontWeight="bold" textAnchor="middle">DEALER</text>
        <text x="450" y="720" fill="#f5c842" fontSize="11" fontWeight="bold" textAnchor="middle">NETWORK MOAT</text>
        {[
          [195,792,"20 Founding Partners","$10M equity → 5K by 2027"],
          [400,798,"CNCDA 816 Dealers","$389M assoc. value by 2030"],
          [600,790,"CalPERS $5M Anchor","18–24% IRR | Emerging Mgr"],
        ].map(([x,y,t1,t2],i) => (
          <g key={i}>
            <rect x={x-90} y={y-16} width="180" height="44" rx="7" fill="#1a1000" stroke="#c47a00" strokeWidth="1.5"/>
            <text x={x} y={y+4} fill="#ffd280" fontSize="9" textAnchor="middle">{t1}</text>
            <text x={x} y={y+18} fill="#ddaa60" fontSize="8" textAnchor="middle">{t2}</text>
          </g>
        ))}

        {/* TRIPLE ARBITRAGE */}
        <ellipse cx="250" cy="450" rx="90" ry="50" fill="#1a0d0d" stroke="#e74c3c" strokeWidth="2" filter="url(#glow)"/>
        <text x="250" y="444" fill="#ff6b6b" fontSize="11" fontWeight="bold" textAnchor="middle">TRIPLE</text>
        <text x="250" y="461" fill="#ff6b6b" fontSize="11" fontWeight="bold" textAnchor="middle">ARBITRAGE</text>
        {[
          [60,340,"IRS Mileage Arb.","$2.66 vs $0.70/mile IRS rate"],
          [48,450,"Capital Efficiency","Avoid $150K hauler purchase"],
          [55,555,"Compliance Premium","$720K → $325K net truck cost"],
        ].map(([x,y,t1,t2],i) => (
          <g key={i}>
            <rect x={x} y={y-16} width="178" height="44" rx="7" fill="#1a0505" stroke="#c0392b" strokeWidth="1.5"/>
            <text x={x+89} y={y+4} fill="#ff9090" fontSize="9" textAnchor="middle">{t1}</text>
            <text x={x+89} y={y+18} fill="#dd7070" fontSize="8" textAnchor="middle">{t2}</text>
          </g>
        ))}

        {/* CESAR AI box */}
        <rect x="555" y="538" width="290" height="72" rx="10" fill="#0a1520" stroke="#00d4ff" strokeWidth="1" strokeDasharray="5,3"/>
        <text x="700" y="558" fill="#00d4ff" fontSize="9" fontWeight="bold" textAnchor="middle">⚙️ CESAR AI AUTONOMOUS CONTROLLER</text>
        <text x="700" y="574" fill="#80c8ff" fontSize="8" textAnchor="middle">8 Specialized Agents | Local Ollama Deployment (No API Cost)</text>
        <text x="700" y="588" fill="#80c8ff" fontSize="8" textAnchor="middle">Route Optimize • Carbon Verify • V2G Mgmt • Compliance Monitor</text>
        <text x="700" y="600" fill="#80c8ff" fontSize="8" textAnchor="middle">Monte Carlo 10,000 iterations | Zero-Knowledge Proof System</text>

        {/* Video Principle */}
        <rect x="560" y="625" width="280" height="90" rx="10" fill="#0d2a1a" stroke="#00ff88" strokeWidth="1.5"/>
        <text x="700" y="645" fill="#00ff88" fontSize="9" fontWeight="bold" textAnchor="middle">🎬 VIDEO PRINCIPLE: WEALTH GAME FROM NOTHING</text>
        <text x="700" y="662" fill="#80ffb0" fontSize="8" textAnchor="middle">"Capture regulatory flow before spending capital"</text>
        <text x="700" y="677" fill="#80ffb0" fontSize="8" textAnchor="middle">CDLS Implementation: 91–97% of ZEV deployment</text>
        <text x="700" y="691" fill="#80ffb0" fontSize="8" textAnchor="middle">covered by stacked incentives — start from near $0</text>
        <text x="700" y="705" fill="#00ff88" fontSize="8" textAnchor="middle" fontWeight="bold">Net Truck: $325K after $395K in stacked credits</text>

        {/* Metrics box */}
        <rect x="1180" y="640" width="205" height="155" rx="10" fill="#150d25" stroke="#9b59b6" strokeWidth="1.5"/>
        <text x="1283" y="660" fill="#cc88ff" fontSize="9" fontWeight="bold" textAnchor="middle">💰 PLATFORM METRICS</text>
        {[
          "$4.13B royalties → CA (10yr)",
          "$2–3B token exit valuation",
          "99.95% dispatch reliability",
          "9 vehicles/load vs 6–7",
          "97.3% route accuracy",
          "60.7% CA tax debt reduction",
          "$389M CNCDA value",
        ].map((t,i) => (
          <text key={i} x="1283" y={680+i*16} fill="#e0c0ff" fontSize="8" textAnchor="middle">{t}</text>
        ))}

        {/* Footer */}
        <text x="700" y="868" fill="#334466" fontSize="8" textAnchor="middle">CONFIDENTIAL — CDLS / California Investment Auto, LP | Julio Umanzor, CEO &amp; Managing Partner | March 2026</text>
      </svg>
    </div>
  );
}