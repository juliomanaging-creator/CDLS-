import { useState, useRef } from "react";

// ─────────────────────────────────────────────────────────────────
//  SACRAMENTO AUTO LEADERS SUPPORTING ALLIANCE (SALSA)
//  Administrative Compliance & Grant Management Platform
//  Volume-Based Service Fee Engine · Owner Dashboard
// ─────────────────────────────────────────────────────────────────

const FONTS = `
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#0B0F0E;font-family:'DM Sans',sans-serif;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:#2A3B2E;border-radius:2px;}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
@keyframes countUp{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.4;}}
@keyframes scanline{0%{transform:translateY(-100%);}100%{transform:translateY(100vh);}}
@keyframes blink{0%,100%{opacity:1;}49%{opacity:1;}50%{opacity:0;}}
.fade-up{animation:fadeUp .45s cubic-bezier(.22,1,.36,1) both;}
input,select,textarea{font-family:'DM Mono',monospace;}
`;

const C = {
  bg:      "#0B0F0E",
  bgCard:  "#121816",
  bgPanel: "#161E1A",
  bgHover: "#1C2820",
  border:  "#1E2E24",
  borderLt:"#2A3D30",
  green:   "#3DB868",
  greenLt: "#5FD485",
  greenDim:"rgba(61,184,104,.12)",
  gold:    "#C9922A",
  goldLt:  "#E6AA44",
  goldDim: "rgba(201,146,42,.12)",
  amber:   "#D97706",
  red:     "#C23B3B",
  redDim:  "rgba(194,59,59,.1)",
  teal:    "#2D9E8F",
  tealDim: "rgba(45,158,143,.1)",
  ink:     "#F2F0EC",
  inkMid:  "#B8B4AD",
  inkDim:  "#6B6860",
  inkFaint:"#2E342E",
  mono:    "#DFF5E5",
};

// ─── SERVICE TIERS ────────────────────────────────────────────────
const SERVICE_TIERS = [
  { id:"t1", num:1, label:"Starter",  range:"1–9 deals",   fee:750, color:C.amber,  colorDim:"rgba(217,119,6,.12)",
    note:"Entry rate. Dealers typically reach Tier 2 within 60 days of full onboarding.", target:"Monthly minimum to break even vs. hiring in-house" },
  { id:"t2", num:2, label:"Growth",   range:"10–19 deals", fee:599, color:C.gold,   colorDim:C.goldDim,
    note:"Discount activates automatically when the 10th funded deal is logged in the portal.", target:"Most dealers stabilize here within 90 days" },
  { id:"t3", num:3, label:"Partner",  range:"20–29 deals", fee:499, color:C.green,  colorDim:C.greenDim,
    note:"Strong volume. At this rate you're providing near-full-time compliance support.", target:"Equivalent to 1 funded deal per 1.5 days" },
  { id:"t4", num:4, label:"Elite",    range:"30+ deals",   fee:399, color:C.greenLt,colorDim:"rgba(95,212,133,.12)",
    note:'The "Preferred Partner Rate." Frame this as: less than a part-time clerk covering full compliance.', target:"1 funded deal per day — the target to reinforce" },
];

// ─── MOCK DEALERS ─────────────────────────────────────────────────
const INITIAL_DEALERS = [
  { id:"DLR-001", name:"Valley Ridge Auto Group",     gm:"Marcus Chen",      city:"Sacramento", tier:"t3", mtdDeals:24, prevDeals:22, ytdDeals:178, status:"active",   lastInvoice:"2026-02-01", outstanding:0,     notes:"Strong. Consistently Tier 3. Potential Tier 4 by Q2." },
  { id:"DLR-002", name:"Sunrise Motors Sacramento",    gm:"Patricia Okonkwo", city:"Sacramento", tier:"t2", mtdDeals:14, prevDeals:11, ytdDeals:94,  status:"active",   lastInvoice:"2026-02-01", outstanding:5993, notes:"Grew from Tier 1. Needs 6 more deals for Tier 3." },
  { id:"DLR-003", name:"Gold Country Kia",             gm:"Steve Delgado",    city:"Elk Grove",  tier:"t4", mtdDeals:33, prevDeals:30, ytdDeals:211, status:"active",   lastInvoice:"2026-02-01", outstanding:0,     notes:"Elite partner. Hitting 1 deal/day target consistently." },
  { id:"DLR-004", name:"Capital City Ford",            gm:"Janet Wu",         city:"Sacramento", tier:"t1", mtdDeals:6,  prevDeals:4,  ytdDeals:31,  status:"attention", lastInvoice:"2026-01-01", outstanding:3000, notes:"Tier 1 for 3 months. CEO should schedule a retrain." },
];

// ─── MOCK TRANSACTIONS ────────────────────────────────────────────
const MOCK_TXN = [
  { id:"CC4A-2026-8821", dealer:"DLR-001", customer:"J. Smith",    date:"2026-02-14", vin:"BZ3A1", grant:"$12,000", fee:499, status:"funded" },
  { id:"CC4A-2026-9045", dealer:"DLR-001", customer:"M. Garcia",   date:"2026-02-18", vin:"DX8P2", grant:"$14,000", fee:499, status:"funded" },
  { id:"CC4A-2026-9112", dealer:"DLR-001", customer:"T. Williams", date:"2026-02-20", vin:"KL4E7", grant:"$12,000", fee:499, status:"funded" },
  { id:"DCAP-2026-4421", dealer:"DLR-002", customer:"A. Reyes",    date:"2026-02-12", vin:"MN2R9", grant:"$7,500",  fee:599, status:"funded" },
  { id:"CC4A-2026-9201", dealer:"DLR-002", customer:"D. Park",     date:"2026-02-19", vin:"PP5T3", grant:"$12,000", fee:599, status:"funded" },
  { id:"CC4A-2026-9330", dealer:"DLR-003", customer:"L. Torres",   date:"2026-02-10", vin:"QR7Y1", grant:"$14,000", fee:399, status:"funded" },
  { id:"CC4A-2026-9404", dealer:"DLR-003", customer:"B. Nguyen",   date:"2026-02-15", vin:"SS4U8", grant:"$12,000", fee:399, status:"funded" },
  { id:"CC4A-2026-9501", dealer:"DLR-003", customer:"C. Johnson",  date:"2026-02-22", vin:"TV3W6", grant:"$14,000", fee:399, status:"funded" },
  { id:"DCAP-2026-5012", dealer:"DLR-004", customer:"R. Adams",    date:"2026-02-08", vin:"UX2Z4", grant:"$7,500",  fee:750, status:"funded" },
];

// ─────────────────────────────────────────────────────────────────
//  HELPERS
// ─────────────────────────────────────────────────────────────────
const getTier = (deals) => {
  if (deals >= 30) return SERVICE_TIERS[3];
  if (deals >= 20) return SERVICE_TIERS[2];
  if (deals >= 10) return SERVICE_TIERS[1];
  return SERVICE_TIERS[0];
};

const fmt = (n, decimals=0) => Number(n).toLocaleString("en-US", { minimumFractionDigits:decimals, maximumFractionDigits:decimals });
const fmtUSD = (n) => "$" + fmt(n);

// ─── STAT CARD ────────────────────────────────────────────────────
function Stat({ label, value, sub, color=C.green, accent=false, delay=0 }) {
  return (
    <div className="fade-up" style={{ animationDelay:`${delay}ms`, background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:"20px 22px", position:"relative", overflow:"hidden" }}>
      {accent && <div style={{ position:"absolute", top:0, left:0, right:0, height:2, background:color }} />}
      <div style={{ fontSize:10, color:C.inkDim, textTransform:"uppercase", letterSpacing:".12em", fontFamily:"'DM Mono',monospace", marginBottom:8 }}>{label}</div>
      <div style={{ fontFamily:"'Syne',sans-serif", fontSize:32, fontWeight:800, color, lineHeight:1, marginBottom:6 }}>{value}</div>
      {sub && <div style={{ fontSize:12, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>{sub}</div>}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  OWNER DASHBOARD
// ─────────────────────────────────────────────────────────────────
function OwnerDashboard({ dealers }) {
  const totalMTD = dealers.reduce((s,d)=>s+d.mtdDeals,0);
  const totalMTDRevenue = dealers.reduce((s,d)=>s+(d.mtdDeals * getTier(d.mtdDeals).fee),0);
  const outstanding = dealers.reduce((s,d)=>s+d.outstanding,0);
  const eliteCount = dealers.filter(d=>getTier(d.mtdDeals).id==="t4").length;
  const attentionDeals = dealers.filter(d=>d.status==="attention");

  // 12-month projection based on current run rate
  const projected12 = dealers.reduce((s,d)=>{
    const t = getTier(d.mtdDeals);
    return s + (d.mtdDeals * t.fee * 12);
  },0);

  // Revenue by tier this month
  const revenueByTier = SERVICE_TIERS.map(tier=>{
    const tierDealers = dealers.filter(d=>getTier(d.mtdDeals).id===tier.id);
    const revenue = tierDealers.reduce((s,d)=>s+(d.mtdDeals*tier.fee),0);
    return { tier, dealers:tierDealers.length, deals:tierDealers.reduce((s,d)=>s+d.mtdDeals,0), revenue };
  });

  return (
    <div className="fade-up">
      {/* Top stats */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:12, marginBottom:20 }}>
        <Stat label="MTD Revenue" value={fmtUSD(totalMTDRevenue)} sub="February 2026" color={C.green} accent delay={0} />
        <Stat label="Funded Deals MTD" value={fmt(totalMTD)} sub="Across all partners" color={C.goldLt} delay={60} />
        <Stat label="Outstanding AR" value={fmtUSD(outstanding)} sub={outstanding>0?"Action required":"All current"} color={outstanding>0?C.red:C.green} delay={120} />
        <Stat label="12-Mo Projection" value={fmtUSD(projected12)} sub="At current run rate" color={C.teal} accent delay={180} />
      </div>

      {/* Revenue by tier */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:20 }}>
        <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
          <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:C.ink, marginBottom:16 }}>Revenue by Service Tier · February</div>
          {revenueByTier.map(row=>(
            <div key={row.tier.id} style={{ display:"flex", alignItems:"center", gap:12, padding:"10px 0", borderBottom:`1px solid ${C.border}` }}>
              <div style={{ width:8, height:8, borderRadius:"50%", background:row.tier.color, flexShrink:0, boxShadow:`0 0 8px ${row.tier.color}` }} />
              <div style={{ flex:1 }}>
                <div style={{ fontSize:13, fontWeight:700, color:C.ink }}>Tier {row.tier.num} — {row.tier.label}</div>
                <div style={{ fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>{row.dealers} dealer{row.dealers!==1?"s":""} · {row.deals} deals · ${row.tier.fee}/deal</div>
              </div>
              <div style={{ textAlign:"right" }}>
                <div style={{ fontFamily:"'DM Mono',monospace", fontSize:16, fontWeight:500, color:row.tier.color }}>{fmtUSD(row.revenue)}</div>
                {row.deals > 0 && (
                  <div style={{ width:80, height:4, background:C.bgPanel, borderRadius:2, marginTop:4 }}>
                    <div style={{ width:`${Math.min(100,(row.revenue/totalMTDRevenue)*100)}%`, height:4, background:row.tier.color, borderRadius:2 }} />
                  </div>
                )}
              </div>
            </div>
          ))}
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginTop:12, paddingTop:12 }}>
            <div style={{ fontSize:12, fontWeight:700, color:C.inkMid }}>Total MTD</div>
            <div style={{ fontFamily:"'Syne',sans-serif", fontSize:22, fontWeight:800, color:C.green }}>{fmtUSD(totalMTDRevenue)}</div>
          </div>
        </div>

        {/* Dealer health */}
        <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
          <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:C.ink, marginBottom:16 }}>Dealer Health Monitor</div>
          {dealers.map(d=>{
            const tier = getTier(d.mtdDeals);
            const prev = getTier(d.prevDeals);
            const moved = tier.id !== prev.id;
            const up = SERVICE_TIERS.indexOf(tier) > SERVICE_TIERS.indexOf(prev);
            return (
              <div key={d.id} style={{ display:"flex", alignItems:"center", gap:10, padding:"10px 0", borderBottom:`1px solid ${C.border}` }}>
                <div style={{ width:8, height:8, borderRadius:"50%", background:d.status==="attention"?C.red:C.green, flexShrink:0,
                               animation:d.status==="attention"?"pulse 2s ease infinite":"none" }} />
                <div style={{ flex:1 }}>
                  <div style={{ fontSize:13, fontWeight:700, color:C.ink, display:"flex", gap:8, alignItems:"center" }}>
                    {d.name.split(" ").slice(0,2).join(" ")}
                    {d.status==="attention" && <span style={{ fontSize:10, color:C.red, background:C.redDim, padding:"2px 6px", borderRadius:3, fontFamily:"'DM Mono',monospace" }}>NEEDS RETRAIN</span>}
                    {moved && <span style={{ fontSize:10, color:up?C.green:C.amber, background:up?C.greenDim:C.goldDim, padding:"2px 6px", borderRadius:3, fontFamily:"'DM Mono',monospace" }}>{up?"▲ TIER UP":"▼ TIER DOWN"}</span>}
                  </div>
                  <div style={{ fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>{d.mtdDeals} deals · {tier.label} · ${tier.fee}/deal</div>
                </div>
                <div style={{ textAlign:"right" }}>
                  <div style={{ fontFamily:"'DM Mono',monospace", fontSize:14, color:tier.color }}>{fmtUSD(d.mtdDeals*tier.fee)}</div>
                  {d.outstanding > 0 && <div style={{ fontSize:10, color:C.red, fontFamily:"'DM Mono',monospace" }}>AR: {fmtUSD(d.outstanding)}</div>}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Attention dealers */}
      {attentionDeals.length > 0 && (
        <div style={{ background:C.redDim, border:`1px solid rgba(194,59,59,.25)`, borderRadius:12, padding:20 }}>
          <div style={{ fontFamily:"'Syne',sans-serif", fontSize:15, fontWeight:700, color:C.red, marginBottom:12 }}>⚠️ Dealer Action Required</div>
          {attentionDeals.map(d=>(
            <div key={d.id} style={{ background:C.bgCard, borderRadius:8, padding:"12px 16px", marginBottom:8 }}>
              <div style={{ fontSize:14, fontWeight:700, color:C.ink, marginBottom:4 }}>{d.name} — {d.gm}</div>
              <div style={{ fontSize:13, color:C.inkMid, marginBottom:4 }}>{d.notes}</div>
              <div style={{ fontSize:12, color:C.red, fontFamily:"'DM Mono',monospace" }}>
                Tier 1 for {Math.floor(Math.random()*2)+2} months · Outstanding: {fmtUSD(d.outstanding)} · CEO should schedule site visit
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  SERVICE FEE SCHEDULE
// ─────────────────────────────────────────────────────────────────
function ServiceFeeSchedule() {
  const [hovered, setHovered] = useState(null);
  return (
    <div className="fade-up">
      <div style={{ marginBottom:28 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.green, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Master Service Agreement · Exhibit A</div>
        <h2 style={{ fontFamily:"'Syne',sans-serif", fontSize:36, fontWeight:800, color:C.ink, lineHeight:1.1, marginBottom:12 }}>
          Volume-Based Service<br/>Fee Schedule
        </h2>
        <p style={{ fontSize:15, color:C.inkMid, lineHeight:1.8, maxWidth:680 }}>
          Sacramento Auto Leaders Supporting Alliance (SALSA) charges a <strong style={{ color:C.ink }}>per-transaction administrative compliance fee</strong> for document vetting, Fluxx Portal management, and tax compliance certification. Fees are legally distinct from referral fees — they are professional services billed for compliance work performed.
        </p>
      </div>

      {/* Tier cards */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:14, marginBottom:32 }}>
        {SERVICE_TIERS.map((tier, i) => {
          const isHov = hovered === tier.id;
          const monthly = i===0?6750:i===1?11980:i===2?12475:i===3?15960:0;
          return (
            <div key={tier.id}
              onMouseEnter={()=>setHovered(tier.id)} onMouseLeave={()=>setHovered(null)}
              style={{ background:isHov?tier.colorDim:C.bgCard, border:`2px solid ${isHov?tier.color:C.border}`, borderRadius:14, padding:"22px 20px",
                        transition:"all .2s", cursor:"default", position:"relative", overflow:"hidden" }}>
              {tier.id==="t4" && (
                <div style={{ position:"absolute", top:10, right:10, background:C.green, color:"#0B0F0E", fontSize:9, fontWeight:800, padding:"3px 8px", borderRadius:3, textTransform:"uppercase", letterSpacing:".08em", fontFamily:"'DM Mono',monospace" }}>
                  Preferred
                </div>
              )}
              <div style={{ position:"absolute", top:0, left:0, right:0, height:3, background:isHov?tier.color:C.border, transition:"background .2s" }} />
              <div style={{ fontFamily:"'DM Mono',monospace", fontSize:11, color:C.inkDim, marginBottom:6, textTransform:"uppercase", letterSpacing:".1em" }}>Tier {tier.num}</div>
              <div style={{ fontFamily:"'Syne',sans-serif", fontSize:22, fontWeight:800, color:tier.color, marginBottom:4 }}>{tier.label}</div>
              <div style={{ fontFamily:"'DM Mono',monospace", fontSize:13, color:C.inkMid, marginBottom:20 }}>{tier.range} / month</div>
              <div style={{ fontFamily:"'Syne',sans-serif", fontSize:48, fontWeight:800, color:C.ink, lineHeight:1, marginBottom:4 }}>
                ${tier.fee}
              </div>
              <div style={{ fontSize:12, color:C.inkDim, marginBottom:20 }}>per funded transaction</div>
              <div style={{ borderTop:`1px solid ${C.borderLt}`, paddingTop:14 }}>
                <div style={{ fontSize:10, color:C.inkDim, fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".08em", marginBottom:6 }}>Mid-Volume Monthly Est.</div>
                <div style={{ fontFamily:"'DM Mono',monospace", fontSize:16, color:tier.color }}>{fmtUSD(monthly)}</div>
              </div>
              <div style={{ marginTop:14, fontSize:11, color:C.inkDim, lineHeight:1.65 }}>{tier.note}</div>
            </div>
          );
        })}
      </div>

      {/* Ladder visual */}
      <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:14, padding:28, marginBottom:20 }}>
        <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:C.ink, marginBottom:20 }}>Tier Progression Ladder</div>
        <div style={{ display:"flex", gap:0, alignItems:"stretch" }}>
          {SERVICE_TIERS.map((tier, i) => (
            <div key={tier.id} style={{ flex:1, position:"relative" }}>
              <div style={{ background:tier.colorDim, border:`1px solid ${tier.color}44`, borderRadius:i===0?"8px 0 0 8px":i===3?"0 8px 8px 0":"0", padding:"16px 14px", height:"100%" }}>
                <div style={{ fontSize:10, color:tier.color, fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".08em", marginBottom:4 }}>Tier {tier.num}</div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:18, fontWeight:800, color:C.ink, marginBottom:2 }}>{tier.label}</div>
                <div style={{ fontSize:12, color:C.inkMid, fontFamily:"'DM Mono',monospace", marginBottom:8 }}>{tier.range}</div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:28, fontWeight:800, color:tier.color }}>${tier.fee}</div>
                <div style={{ fontSize:10, color:C.inkDim, marginTop:2 }}>per deal</div>
                <div style={{ fontSize:11, color:C.inkDim, marginTop:10, lineHeight:1.6 }}>{tier.target}</div>
              </div>
              {i < 3 && (
                <div style={{ position:"absolute", right:-16, top:"50%", transform:"translateY(-50%)", zIndex:10, width:32, height:32, borderRadius:"50%",
                               background:C.bgCard, border:`1px solid ${C.borderLt}`, display:"flex", alignItems:"center", justifyContent:"center",
                               fontSize:16, color:C.green, fontWeight:800 }}>→</div>
              )}
            </div>
          ))}
        </div>
        <div style={{ marginTop:20, background:C.bgPanel, borderRadius:8, padding:"12px 16px", fontSize:13, color:C.inkMid, lineHeight:1.7 }}>
          <strong style={{ color:C.goldLt }}>🎯 CEO Strategy:</strong> Frame the $399 rate as the "Preferred Partner Rate." Remind dealers that hitting 30 deals/month means 1 funded deal per business day — a target that is very achievable once your staff is trained on the $12,000 grant pitch. A dealer averaging 30 deals pays <strong style={{ color:C.ink }}>$11,970/month</strong> in service fees vs. $22,500 at Tier 1 rates for the same volume.
        </div>
      </div>

      {/* Legal framing */}
      <div style={{ background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:12, padding:22 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.teal, letterSpacing:".12em", textTransform:"uppercase", marginBottom:12 }}>Legal Framing — Important</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:16 }}>
          {[
            ["Administrative Services","SALSA bills for professional compliance work: document review, portal submission, tax certification. NOT a finder's fee or referral.","📋"],
            ["Legally Distinct","Operating as a compliance firm ensures this fee structure is legal in California. The dealer pays for services rendered, not leads delivered.","⚖️"],
            ["Net-30 Billing","All invoices are due net-30 from the last funded transaction of the month. Automated via Stripe/QuickBooks Online.","💳"],
          ].map(([t,d,icon])=>(
            <div key={t} style={{ background:C.bgCard, borderRadius:8, padding:16 }}>
              <div style={{ fontSize:22, marginBottom:8 }}>{icon}</div>
              <div style={{ fontSize:13, fontWeight:700, color:C.ink, marginBottom:6 }}>{t}</div>
              <div style={{ fontSize:12, color:C.inkDim, lineHeight:1.65 }}>{d}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  INVOICE GENERATOR
// ─────────────────────────────────────────────────────────────────
function InvoiceGenerator({ dealers }) {
  const [selectedDealer, setSelectedDealer] = useState("DLR-001");
  const [month, setMonth] = useState("February");
  const [year, setYear] = useState("2026");
  const [preview, setPreview] = useState(false);

  const dealer = dealers.find(d=>d.id===selectedDealer);
  const tier = dealer ? getTier(dealer.mtdDeals) : SERVICE_TIERS[0];
  const dealerTxns = MOCK_TXN.filter(t=>t.dealer===selectedDealer);
  const totalFee = dealerTxns.length * tier.fee;
  const invoiceNum = `${year.slice(-2)}${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].indexOf(month.slice(0,3))+1 < 10 ? "0":""}{["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].indexOf(month.slice(0,3))+1}-${selectedDealer}`;

  return (
    <div className="fade-up">
      {!preview ? (
        <div>
          <div style={{ marginBottom:24 }}>
            <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.green, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Monthly Billing Engine</div>
            <h2 style={{ fontFamily:"'Syne',sans-serif", fontSize:32, fontWeight:800, color:C.ink, marginBottom:8 }}>Generate Invoice</h2>
            <p style={{ fontSize:14, color:C.inkMid, lineHeight:1.7 }}>Send on the 1st of every month for the previous month's funded transactions. Always attach the Transaction Detail Report.</p>
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:24 }}>
            <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
              <div style={{ fontSize:13, fontWeight:700, color:C.inkMid, marginBottom:14 }}>Invoice Parameters</div>
              <div style={{ display:"flex", flexDirection:"column", gap:14 }}>
                {[
                  ["Dealer", <select value={selectedDealer} onChange={e=>setSelectedDealer(e.target.value)}
                    style={{ width:"100%", padding:"10px 14px", background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:7, color:C.ink, fontSize:13, outline:"none" }}>
                    {dealers.map(d=><option key={d.id} value={d.id}>{d.name}</option>)}
                  </select>],
                  ["Billing Month", <select value={month} onChange={e=>setMonth(e.target.value)}
                    style={{ width:"100%", padding:"10px 14px", background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:7, color:C.ink, fontSize:13, outline:"none" }}>
                    {["January","February","March","April","May","June","July","August","September","October","November","December"].map(m=><option key={m}>{m}</option>)}
                  </select>],
                  ["Year", <select value={year} onChange={e=>setYear(e.target.value)}
                    style={{ width:"100%", padding:"10px 14px", background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:7, color:C.ink, fontSize:13, outline:"none" }}>
                    {["2026","2027"].map(y=><option key={y}>{y}</option>)}
                  </select>],
                ].map(([label, el])=>(
                  <div key={label}>
                    <label style={{ fontSize:10, color:C.inkDim, fontFamily:"'DM Mono',monospace", letterSpacing:".1em", textTransform:"uppercase", marginBottom:6, display:"block" }}>{label}</label>
                    {el}
                  </div>
                ))}
              </div>
            </div>

            {dealer && (
              <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
                <div style={{ fontSize:13, fontWeight:700, color:C.inkMid, marginBottom:14 }}>Invoice Preview</div>
                <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
                  {[
                    ["Dealer", dealer.name],
                    ["Attention", dealer.gm + " (GM / Controller)"],
                    ["Deals Funded", `${dealerTxns.length} transactions`],
                    ["Tier Active", `Tier ${tier.num} — ${tier.label} (${tier.range})`],
                    ["Rate Applied", `${fmtUSD(tier.fee)} per funded transaction`],
                    ["Invoice Total", fmtUSD(totalFee)],
                    ["Due Date", "Net-30 from invoice date"],
                  ].map(([k,v])=>(
                    <div key={k} style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", padding:"7px 0", borderBottom:`1px solid ${C.border}` }}>
                      <span style={{ fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".06em", flexShrink:0 }}>{k}</span>
                      <span style={{ fontSize:13, fontWeight:k==="Invoice Total"?800:500, color:k==="Invoice Total"?C.green:C.ink, textAlign:"right", maxWidth:"60%" }}>{v}</span>
                    </div>
                  ))}
                </div>
                <button onClick={()=>setPreview(true)}
                  style={{ marginTop:16, width:"100%", padding:"12px", background:C.green, color:"#0B0F0E", border:"none", borderRadius:8, fontFamily:"'Syne',sans-serif", fontSize:15, fontWeight:800, cursor:"pointer" }}>
                  Generate Invoice →
                </button>
              </div>
            )}
          </div>
        </div>
      ) : (
        // ─── INVOICE PREVIEW ─────────────────────────────────────
        <div>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:20 }}>
            <div style={{ fontFamily:"'DM Mono',monospace", fontSize:11, color:C.green }}>INVOICE GENERATED — READY TO SEND</div>
            <button onClick={()=>setPreview(false)} style={{ background:C.bgPanel, border:`1px solid ${C.borderLt}`, color:C.inkMid, padding:"8px 16px", borderRadius:6, fontSize:13, cursor:"pointer" }}>← Back</button>
          </div>
          <div style={{ background:"#FFFFFF", borderRadius:14, overflow:"hidden", boxShadow:"0 24px 64px rgba(0,0,0,.4)" }}>
            {/* Invoice header */}
            <div style={{ background:"#1A2E1F", padding:"36px 40px", display:"flex", justifyContent:"space-between", alignItems:"flex-start" }}>
              <div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:22, fontWeight:800, color:"#FFFFFF", marginBottom:4 }}>Sacramento Auto Leaders<br/>Supporting Alliance</div>
                <div style={{ fontFamily:"'DM Mono',monospace", fontSize:11, color:"rgba(255,255,255,.5)", lineHeight:1.8 }}>
                  Administrative Compliance &amp; Grant Management<br/>
                  Sacramento, CA 95820<br/>
                  compliance@saclsa.org
                </div>
              </div>
              <div style={{ textAlign:"right" }}>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:32, fontWeight:800, color:"#C9922A" }}>INVOICE</div>
                <div style={{ fontFamily:"'DM Mono',monospace", fontSize:12, color:"rgba(255,255,255,.5)", marginTop:4 }}>
                  #{invoiceNum}<br/>
                  Date: {month} 1, {year}<br/>
                  Due: Net-30
                </div>
              </div>
            </div>

            {/* Bill to */}
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", padding:"28px 40px", borderBottom:"2px solid #F0F0F0", background:"#F9FAF8" }}>
              <div>
                <div style={{ fontSize:10, color:"#888", textTransform:"uppercase", letterSpacing:".12em", fontFamily:"'DM Mono',monospace", marginBottom:8 }}>Bill To</div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:"#1A2E1F", marginBottom:2 }}>{dealer?.name}</div>
                <div style={{ fontSize:13, color:"#555" }}>Attn: {dealer?.gm} — General Manager / Controller</div>
                <div style={{ fontSize:12, color:"#888", marginTop:4 }}>Dealer ID: {selectedDealer}</div>
              </div>
              <div style={{ textAlign:"right" }}>
                <div style={{ fontSize:10, color:"#888", textTransform:"uppercase", letterSpacing:".12em", fontFamily:"'DM Mono',monospace", marginBottom:8 }}>Service Period</div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:"#1A2E1F" }}>{month} {year}</div>
                <div style={{ fontSize:12, color:"#888", marginTop:4 }}>Batch Tier: Tier {tier.num} ({tier.label}) · {tier.range}</div>
              </div>
            </div>

            {/* Line item */}
            <div style={{ padding:"0 40px", background:"#FFFFFF" }}>
              <table style={{ width:"100%", borderCollapse:"collapse" }}>
                <thead>
                  <tr style={{ borderBottom:"2px solid #E8E8E8" }}>
                    {["Description","Quantity","Unit Price","Total"].map(h=>(
                      <th key={h} style={{ padding:"14px 0", fontSize:10, color:"#888", textAlign:h==="Total"||h==="Unit Price"?"right":"left", fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".1em" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr style={{ borderBottom:"1px solid #F0F0F0" }}>
                    <td style={{ padding:"16px 0", fontSize:13, color:"#1A2E1F", maxWidth:320 }}>
                      <div style={{ fontWeight:700, marginBottom:4 }}>Professional Administrative Services</div>
                      <div style={{ fontSize:11, color:"#888", lineHeight:1.6 }}>Document vetting, Fluxx Portal submission, state application management, CDTFA-230-ZEV compliance certification, NHTSA recall verification, and grant transaction coordination for state-funded ZEV transactions completed in {month} {year}.</div>
                    </td>
                    <td style={{ padding:"16px 0", fontSize:13, color:"#1A2E1F", textAlign:"center", fontFamily:"'DM Mono',monospace", fontWeight:700 }}>{dealerTxns.length}</td>
                    <td style={{ padding:"16px 0", fontSize:13, color:"#1A2E1F", textAlign:"right", fontFamily:"'DM Mono',monospace", fontWeight:700 }}>{fmtUSD(tier.fee)}</td>
                    <td style={{ padding:"16px 0", fontSize:16, color:"#1A2E1F", textAlign:"right", fontFamily:"'DM Mono',monospace", fontWeight:700 }}>{fmtUSD(totalFee)}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Total */}
            <div style={{ padding:"20px 40px 28px", display:"flex", justifyContent:"flex-end", background:"#FFFFFF" }}>
              <div style={{ width:280 }}>
                {[["Subtotal", fmtUSD(totalFee)],["Tax (0% — Professional Services)",fmtUSD(0)]].map(([l,v])=>(
                  <div key={l} style={{ display:"flex", justifyContent:"space-between", padding:"6px 0", fontSize:12, color:"#888" }}>
                    <span>{l}</span><span style={{ fontFamily:"'DM Mono',monospace" }}>{v}</span>
                  </div>
                ))}
                <div style={{ display:"flex", justifyContent:"space-between", padding:"12px 0", borderTop:"2px solid #1A2E1F", marginTop:4 }}>
                  <span style={{ fontFamily:"'Syne',sans-serif", fontSize:18, fontWeight:800, color:"#1A2E1F" }}>Total Amount Due</span>
                  <span style={{ fontFamily:"'Syne',sans-serif", fontSize:22, fontWeight:800, color:"#3DB868" }}>{fmtUSD(totalFee)}</span>
                </div>
              </div>
            </div>

            {/* Transaction detail */}
            <div style={{ padding:"0 40px 28px", background:"#F9FAF8" }}>
              <div style={{ fontSize:12, fontWeight:700, color:"#1A2E1F", marginBottom:12, paddingTop:20 }}>Transaction Detail Report (Attachment A)</div>
              <table style={{ width:"100%", borderCollapse:"collapse", fontSize:12 }}>
                <thead>
                  <tr style={{ background:"#1A2E1F" }}>
                    {["Applicant Name","App ID (Fluxx)","Funding Date","VIN (Last 6)","Program","Grant"].map(h=>(
                      <th key={h} style={{ padding:"8px 12px", color:"rgba(255,255,255,.6)", textAlign:"left", fontFamily:"'DM Mono',monospace", fontSize:10, textTransform:"uppercase", letterSpacing:".06em" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {dealerTxns.map((t,i)=>(
                    <tr key={t.id} style={{ background:i%2===0?"#FFFFFF":"#F4F5F2" }}>
                      <td style={{ padding:"9px 12px", color:"#1A2E1F", fontWeight:600 }}>{t.customer}</td>
                      <td style={{ padding:"9px 12px", color:"#555", fontFamily:"'DM Mono',monospace" }}>{t.id}</td>
                      <td style={{ padding:"9px 12px", color:"#555", fontFamily:"'DM Mono',monospace" }}>{t.date}</td>
                      <td style={{ padding:"9px 12px", color:"#555", fontFamily:"'DM Mono',monospace" }}>{t.vin}</td>
                      <td style={{ padding:"9px 12px", color:"#555" }}>{t.grant.includes("7")?"DCAP":"CC4A"}</td>
                      <td style={{ padding:"9px 12px", color:"#3DB868", fontFamily:"'DM Mono',monospace", fontWeight:700 }}>{t.grant}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div style={{ marginTop:20, fontSize:11, color:"#888", lineHeight:1.7, borderTop:"1px solid #E8E8E8", paddingTop:16 }}>
                <strong style={{ color:"#1A2E1F" }}>Remittance:</strong> ACH/Zelle to SALSA operating account. <strong style={{ color:"#1A2E1F" }}>Reference:</strong> Invoice #{invoiceNum}.<br/>
                Questions? Contact your SALSA account manager. This invoice is issued by Sacramento Auto Leaders Supporting Alliance, an administrative compliance firm. This fee is not a commission or referral payment.
              </div>
            </div>
          </div>
          <div style={{ display:"flex", gap:10, marginTop:16 }}>
            <button style={{ padding:"11px 24px", background:C.green, color:"#0B0F0E", border:"none", borderRadius:7, fontSize:14, fontWeight:800, cursor:"pointer" }}>📤 Send via Email</button>
            <button style={{ padding:"11px 24px", background:C.bgPanel, border:`1px solid ${C.borderLt}`, color:C.inkMid, borderRadius:7, fontSize:14, fontWeight:600, cursor:"pointer" }}>🖨️ Print / PDF</button>
            <button style={{ padding:"11px 24px", background:C.bgPanel, border:`1px solid ${C.borderLt}`, color:C.inkMid, borderRadius:7, fontSize:14, fontWeight:600, cursor:"pointer" }}>📊 Add to QuickBooks</button>
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  REVENUE PROJECTIONS
// ─────────────────────────────────────────────────────────────────
function RevenueProjections() {
  const [scenario, setScenario] = useState("current");

  const SCENARIOS = {
    current: {
      label:"Current Portfolio", subtitle:"3 dealers Tier 2–4, 1 dealer Tier 1",
      dealers:[
        { name:"Valley Ridge Auto",  tier:3, deals:24 },
        { name:"Sunrise Motors",     tier:2, deals:14 },
        { name:"Gold Country Kia",   tier:4, deals:33 },
        { name:"Capital City Ford",  tier:1, deals:6  },
      ]
    },
    target: {
      label:"90-Day Target", subtitle:"All 4 dealers at Tier 2+, 1 at Elite",
      dealers:[
        { name:"Valley Ridge Auto",  tier:4, deals:31 },
        { name:"Sunrise Motors",     tier:3, deals:22 },
        { name:"Gold Country Kia",   tier:4, deals:35 },
        { name:"Capital City Ford",  tier:2, deals:12 },
      ]
    },
    growth: {
      label:"Year-End Goal", subtitle:"8 dealers, 2 at Elite, 3 at Partner",
      dealers:[
        { name:"Valley Ridge Auto",  tier:4, deals:32 },
        { name:"Sunrise Motors",     tier:3, deals:24 },
        { name:"Gold Country Kia",   tier:4, deals:38 },
        { name:"Capital City Ford",  tier:2, deals:15 },
        { name:"New Partner A",      tier:2, deals:12 },
        { name:"New Partner B",      tier:3, deals:20 },
        { name:"New Partner C",      tier:1, deals:7  },
        { name:"New Partner D",      tier:2, deals:11 },
      ]
    },
  };

  const sc = SCENARIOS[scenario];
  const monthlyRev = sc.dealers.reduce((s,d)=>s+(d.deals * SERVICE_TIERS[d.tier-1].fee),0);
  const annualRev = monthlyRev * 12;
  const totalDeals = sc.dealers.reduce((s,d)=>s+d.deals,0);
  const avgFee = totalDeals > 0 ? (monthlyRev/totalDeals) : 0;

  // Month-by-month ramp (simplified)
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const monthlyData = months.map((m,i)=>{
    const ramp = scenario==="current"?1:scenario==="target"?Math.min(1+i*0.03,1.15):Math.min(1+i*0.08,1.6);
    return { month:m, rev:Math.round(monthlyRev*ramp) };
  });
  const maxRev = Math.max(...monthlyData.map(d=>d.rev));

  return (
    <div className="fade-up">
      <div style={{ marginBottom:24 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.green, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Financial Projections</div>
        <h2 style={{ fontFamily:"'Syne',sans-serif", fontSize:32, fontWeight:800, color:C.ink, marginBottom:8 }}>Revenue Forecast</h2>
        <p style={{ fontSize:14, color:C.inkMid, lineHeight:1.7 }}>Based on the Gemini-recommended portfolio: 3 dealers in Tier 2 bracket and 1 dealer in Tier 4.</p>
      </div>

      {/* Scenario selector */}
      <div style={{ display:"flex", gap:8, marginBottom:24 }}>
        {Object.entries(SCENARIOS).map(([id,sc])=>(
          <button key={id} onClick={()=>setScenario(id)}
            style={{ padding:"10px 20px", borderRadius:8, border:`1.5px solid ${scenario===id?C.green:C.border}`,
                      background:scenario===id?C.greenDim:C.bgCard, color:scenario===id?C.greenLt:C.inkMid,
                      fontSize:13, fontWeight:700, cursor:"pointer", transition:"all .15s" }}>
            {sc.label}
          </button>
        ))}
      </div>

      {/* Top stats */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:12, marginBottom:24 }}>
        {[
          ["Monthly Revenue", fmtUSD(monthlyRev), `${sc.dealers.length} active partners`, C.green],
          ["Annual Revenue", fmtUSD(annualRev), "Projected at current run rate", C.goldLt],
          ["Total Monthly Deals", fmt(totalDeals), "Funded transactions", C.teal],
          ["Avg Fee Per Deal", fmtUSD(Math.round(avgFee)), "Blended rate across tiers", C.inkMid],
        ].map(([l,v,s,c])=>(
          <div key={l} style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:20 }}>
            <div style={{ fontSize:10, color:C.inkDim, fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".12em", marginBottom:8 }}>{l}</div>
            <div style={{ fontFamily:"'Syne',sans-serif", fontSize:30, fontWeight:800, color:c, lineHeight:1, marginBottom:4 }}>{v}</div>
            <div style={{ fontSize:11, color:C.inkDim }}>{s}</div>
          </div>
        ))}
      </div>

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:20 }}>
        {/* Bar chart */}
        <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
          <div style={{ fontFamily:"'Syne',sans-serif", fontSize:15, fontWeight:700, color:C.ink, marginBottom:16 }}>12-Month Revenue Chart</div>
          <div style={{ display:"flex", gap:4, alignItems:"flex-end", height:120 }}>
            {monthlyData.map((d,i)=>(
              <div key={d.month} style={{ flex:1, display:"flex", flexDirection:"column", alignItems:"center", gap:4 }}>
                <div style={{ width:"100%", background:`linear-gradient(to top, ${C.green}, ${C.greenLt})`, borderRadius:"3px 3px 0 0",
                               height:`${(d.rev/maxRev)*100}px`, minHeight:4, transition:"height .5s ease", opacity:.8+i*.015 }} />
                <div style={{ fontSize:8, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>{d.month}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:12, display:"flex", justifyContent:"space-between", fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>
            <span>Low: {fmtUSD(Math.min(...monthlyData.map(d=>d.rev)))}</span>
            <span>High: {fmtUSD(Math.max(...monthlyData.map(d=>d.rev)))}</span>
          </div>
        </div>

        {/* Per-dealer breakdown */}
        <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, padding:22 }}>
          <div style={{ fontFamily:"'Syne',sans-serif", fontSize:15, fontWeight:700, color:C.ink, marginBottom:16 }}>Dealer Contribution</div>
          {sc.dealers.map((d,i)=>{
            const t = SERVICE_TIERS[d.tier-1];
            const rev = d.deals * t.fee;
            const pct = ((rev/monthlyRev)*100).toFixed(0);
            return (
              <div key={i} style={{ marginBottom:12 }}>
                <div style={{ display:"flex", justifyContent:"space-between", marginBottom:4 }}>
                  <div>
                    <span style={{ fontSize:12, fontWeight:700, color:C.ink }}>{d.name}</span>
                    <span style={{ fontSize:10, color:t.color, marginLeft:8, fontFamily:"'DM Mono',monospace" }}>{t.label}</span>
                  </div>
                  <div style={{ fontFamily:"'DM Mono',monospace", fontSize:13, color:t.color }}>{fmtUSD(rev)}</div>
                </div>
                <div style={{ background:C.bgPanel, borderRadius:3, height:6 }}>
                  <div style={{ width:`${pct}%`, height:6, background:t.color, borderRadius:3, transition:"width .5s ease" }} />
                </div>
                <div style={{ fontSize:10, color:C.inkDim, marginTop:3, fontFamily:"'DM Mono',monospace" }}>{d.deals} deals × ${t.fee} = {pct}% of revenue</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Year-end projection table from the Gemini recommendation */}
      <div style={{ background:C.bgCard, border:`1px solid ${C.borderLt}`, borderRadius:12, padding:24 }}>
        <div style={{ fontFamily:"'Syne',sans-serif", fontSize:16, fontWeight:700, color:C.ink, marginBottom:6 }}>
          Year-End Revenue Projection — Gemini Recommended Mix
        </div>
        <div style={{ fontSize:12, color:C.inkDim, marginBottom:18 }}>3 dealers in Tier 2 bracket + 1 dealer in Tier 4 bracket (as recommended)</div>
        <table style={{ width:"100%", borderCollapse:"collapse" }}>
          <thead>
            <tr style={{ borderBottom:`2px solid ${C.borderLt}` }}>
              {["Dealer Segment","Count","Monthly Deals","Fee Rate","Monthly Rev","Annual Rev"].map(h=>(
                <th key={h} style={{ padding:"8px 12px", fontSize:10, color:C.inkDim, textAlign:"left", fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".06em" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              ["Tier 2 Partners", 3, 15, 599, 3, 26955, 323460, C.gold],
              ["Tier 4 Elite",    1, 30, 399, 1, 11970, 143640, C.greenLt],
            ].map(([seg,cnt,deals,rate,mult,monthly,annual,color])=>(
              <tr key={seg} style={{ borderBottom:`1px solid ${C.border}` }}>
                <td style={{ padding:"12px", fontSize:13, fontWeight:700, color:C.ink }}>{seg}</td>
                <td style={{ padding:"12px", fontFamily:"'DM Mono',monospace", fontSize:13, color:C.inkMid }}>{cnt}</td>
                <td style={{ padding:"12px", fontFamily:"'DM Mono',monospace", fontSize:13, color:C.inkMid }}>{deals}/dealer</td>
                <td style={{ padding:"12px", fontFamily:"'DM Mono',monospace", fontSize:14, color, fontWeight:700 }}>${rate}</td>
                <td style={{ padding:"12px", fontFamily:"'DM Mono',monospace", fontSize:14, color, fontWeight:700 }}>{fmtUSD(monthly)}</td>
                <td style={{ padding:"12px", fontFamily:"'DM Mono',monospace", fontSize:14, color, fontWeight:700 }}>{fmtUSD(annual)}</td>
              </tr>
            ))}
            <tr style={{ background:C.greenDim }}>
              <td style={{ padding:"12px", fontFamily:"'Syne',sans-serif", fontSize:14, fontWeight:800, color:C.ink }} colSpan={4}>Total — 4-Dealer Portfolio</td>
              <td style={{ padding:"12px", fontFamily:"'Syne',sans-serif", fontSize:18, fontWeight:800, color:C.green }}>{fmtUSD(26955+11970)}</td>
              <td style={{ padding:"12px", fontFamily:"'Syne',sans-serif", fontSize:20, fontWeight:800, color:C.green }}>{fmtUSD(323460+143640)}</td>
            </tr>
          </tbody>
        </table>
        <div style={{ marginTop:14, background:C.bgPanel, borderRadius:8, padding:"12px 16px", fontSize:13, color:C.inkDim, lineHeight:1.7 }}>
          💡 <strong style={{ color:C.goldLt }}>Owner's Note:</strong> If the Tier 1 dealer (Capital City Ford) reaches Tier 2 within 60 days through staff retraining, annual revenue increases by approximately <strong style={{ color:C.ink }}>$36,000</strong> ({fmtUSD(9*599*12)} → {fmtUSD(12*599*12)}). That one retrain is worth scheduling this month.
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  COLLECTION SCRIPTS
// ─────────────────────────────────────────────────────────────────
function CollectionScripts() {
  const [copied, setCopied] = useState(null);
  const copy = (id, text) => { navigator.clipboard.writeText(text); setCopied(id); setTimeout(()=>setCopied(null), 2000); };

  const SCRIPTS = [
    {
      id:"no_friction",
      label:"No-Friction Collection Response",
      icon:"💬",
      context:"Use when a dealer questions the fee or tiered structure",
      script:`"The tiered structure is designed to reward our high-volume partners. At the $399 rate — which you're just ${31 - 30} deals away from — we're essentially providing a full-time compliance and F&I support team for less than the cost of a single part-time clerk.

This fee covers:
• The security and infrastructure of our document portal
• On-site community events we host to find qualified buyers in your trade area
• The guarantee that your 553-CA-ARB contracts will pass state audit without rejection
• Daily monitoring of every open application in the Fluxx portal

A single compliance mistake on a CC4A deal can cost you $12,000 in rejected reimbursement. One prevented rejection pays for six months of our service."`
    },
    {
      id:"tier1_retrain",
      label:"Tier 1 Retrain Call Script",
      icon:"📞",
      context:"CEO uses this when a dealer has been Tier 1 for 2+ consecutive months",
      script:`"Hi [GM Name], this is [CEO Name] from Sacramento Auto Leaders. I'm looking at our portal data for [Dealer Name] and I noticed your team has been doing about 6 funded deals per month over the last few months.

I want to be transparent — at your current volume, you're at our Tier 1 rate. The good news is you're only 4 deals away from Tier 2, which drops your fee to $599 per transaction.

Here's what I'd like to do: I want to schedule a 90-minute session with your sales floor this month. I'll walk your team through the updated 'Trade-Up Grant' pitch — specifically why the $12,000 Clean Cars 4 All grant is so easy to close if you identify the right customers upfront.

Three dealers who went through this training moved from Tier 1 to Tier 3 within 45 days. Can we find a Tuesday morning this month?"`
    },
    {
      id:"ar_collection",
      label:"Outstanding AR Follow-Up",
      icon:"📋",
      context:"Send when payment is 10+ days past due",
      script:`Subject: Invoice #[Invoice Number] — Payment Reminder

Hi [GM/Controller Name],

I hope you're doing well. I'm following up on Invoice #[Invoice Number] for [Month] services, totaling $[Amount], which was due on [Due Date].

Per our service agreement, all funded transaction fees are due net-30 from invoice date. I've attached the Transaction Detail Report for your records showing the [X] funded deals this covers.

To avoid any interruption to your lead pipeline, please arrange payment by [Date + 5 days]. You can use ACH transfer, Zelle, or our QuickBooks payment link: [Link].

If there's a question about any specific transaction on the report, I'm happy to pull the Fluxx confirmation and VIN documentation for your records.

Thank you,
[CEO Name]
Sacramento Auto Leaders Supporting Alliance"`
    },
    {
      id:"preferred_pitch",
      label:"Preferred Partner Upgrade Pitch",
      icon:"⭐",
      context:"Use with any Tier 2–3 dealer who is 3–5 deals away from the next tier",
      script:`"I want to show you something in the portal. You're currently at [X] funded deals this month, which puts you in our [Tier Name] bracket at $[Rate] per transaction.

If you close [Y] more deals before the end of the month, you automatically drop to $[Next Rate] — and that applies retroactively to the entire month's transactions.

That means [Y] more deals saves you $[Savings] on this month's invoice alone, and every month after that.

The best candidates are customers who already have a 2009 or older car — your own lot records and trade-in inquiries are the best source. We can also run a targeted mailer to [Zip Code] on your behalf, which typically produces 8–12 qualified prospects within 30 days.

Want me to set that up this week?"`
    },
  ];

  return (
    <div className="fade-up">
      <div style={{ marginBottom:24 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.green, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>CEO Playbook</div>
        <h2 style={{ fontFamily:"'Syne',sans-serif", fontSize:32, fontWeight:800, color:C.ink, marginBottom:8 }}>Collection & Retention Scripts</h2>
        <p style={{ fontSize:14, color:C.inkMid, lineHeight:1.7 }}>Ready-to-use scripts for your CEO to handle billing objections, retrain underperforming dealers, and upgrade partners to higher tiers.</p>
      </div>
      <div style={{ display:"flex", flexDirection:"column", gap:14 }}>
        {SCRIPTS.map(s=>(
          <div key={s.id} style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:12, overflow:"hidden" }}>
            <div style={{ padding:"16px 22px", display:"flex", justifyContent:"space-between", alignItems:"center", borderBottom:`1px solid ${C.border}` }}>
              <div style={{ display:"flex", gap:12, alignItems:"center" }}>
                <span style={{ fontSize:22 }}>{s.icon}</span>
                <div>
                  <div style={{ fontFamily:"'Syne',sans-serif", fontSize:15, fontWeight:700, color:C.ink }}>{s.label}</div>
                  <div style={{ fontSize:11, color:C.inkDim, marginTop:2 }}>📌 {s.context}</div>
                </div>
              </div>
              <button onClick={()=>copy(s.id, s.script)}
                style={{ padding:"7px 16px", background:copied===s.id?C.greenDim:C.bgPanel, border:`1px solid ${copied===s.id?C.green:C.borderLt}`,
                          color:copied===s.id?C.green:C.inkMid, borderRadius:6, fontSize:12, fontWeight:700, cursor:"pointer", fontFamily:"'DM Mono',monospace" }}>
                {copied===s.id ? "✓ Copied!" : "Copy"}
              </button>
            </div>
            <div style={{ padding:"18px 22px" }}>
              <pre style={{ fontFamily:"'DM Mono',monospace", fontSize:12, color:C.inkMid, lineHeight:1.85, whiteSpace:"pre-wrap", wordBreak:"break-word" }}>
                {s.script}
              </pre>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  MAIN APP
// ─────────────────────────────────────────────────────────────────
export default function SALSAAdminDashboard() {
  const [tab, setTab] = useState("dashboard");
  const [dealers] = useState(INITIAL_DEALERS);

  const TABS = [
    { id:"dashboard",   label:"📊 Owner Dashboard" },
    { id:"schedule",    label:"💼 Service Fee Schedule" },
    { id:"invoice",     label:"🧾 Invoice Generator" },
    { id:"projections", label:"📈 Revenue Projections" },
    { id:"scripts",     label:"💬 CEO Scripts" },
  ];

  const mtdRev = dealers.reduce((s,d)=>s+(d.mtdDeals*getTier(d.mtdDeals).fee),0);

  return (
    <>
      <style>{FONTS}</style>
      <div style={{ background:C.bg, minHeight:"100vh" }}>

        {/* Header */}
        <div style={{ background:C.bgCard, borderBottom:`1px solid ${C.border}`, padding:"0 32px" }}>
          <div style={{ maxWidth:1400, margin:"0 auto", height:60, display:"flex", alignItems:"center", gap:16 }}>
            <div style={{ display:"flex", alignItems:"center", gap:10 }}>
              <div style={{ width:34, height:34, borderRadius:8, background:`linear-gradient(135deg,#1A3D22,#2D6840)`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:18 }}>⚖️</div>
              <div>
                <div style={{ fontFamily:"'Syne',sans-serif", fontSize:14, fontWeight:800, color:C.ink, letterSpacing:".02em" }}>SALSA</div>
                <div style={{ fontSize:9, color:C.inkDim, fontFamily:"'DM Mono',monospace", letterSpacing:".12em", textTransform:"uppercase" }}>Sacramento Auto Leaders · Admin Portal</div>
              </div>
            </div>

            {/* Live ticker */}
            <div style={{ marginLeft:20, display:"flex", alignItems:"center", gap:8, background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:6, padding:"5px 12px" }}>
              <div style={{ width:6, height:6, borderRadius:"50%", background:C.green, animation:"pulse 2s ease infinite" }} />
              <span style={{ fontFamily:"'DM Mono',monospace", fontSize:11, color:C.green }}>MTD Revenue: {fmtUSD(mtdRev)}</span>
            </div>

            <div style={{ marginLeft:"auto", display:"flex", gap:6 }}>
              {dealers.filter(d=>d.outstanding>0).length > 0 && (
                <div style={{ background:C.redDim, border:`1px solid rgba(194,59,59,.3)`, borderRadius:6, padding:"5px 12px", fontSize:11, color:C.red, fontFamily:"'DM Mono',monospace" }}>
                  ⚠️ {dealers.filter(d=>d.outstanding>0).length} AR outstanding
                </div>
              )}
              <div style={{ background:C.bgPanel, border:`1px solid ${C.borderLt}`, borderRadius:6, padding:"5px 12px", fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>
                🔒 Owner View
              </div>
            </div>
          </div>
        </div>

        {/* Sub nav */}
        <div style={{ background:C.bgCard, borderBottom:`1px solid ${C.border}`, padding:"0 32px" }}>
          <div style={{ maxWidth:1400, margin:"0 auto", display:"flex", gap:2, overflowX:"auto" }}>
            {TABS.map(t=>(
              <button key={t.id} onClick={()=>setTab(t.id)}
                style={{ padding:"14px 20px", background:"transparent", border:"none",
                          borderBottom:`2px solid ${tab===t.id?C.green:"transparent"}`,
                          color:tab===t.id?C.green:C.inkDim, fontSize:13, fontWeight:600,
                          cursor:"pointer", whiteSpace:"nowrap", transition:"all .15s", fontFamily:"'DM Sans',sans-serif" }}>
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div style={{ maxWidth:1400, margin:"0 auto", padding:"32px 32px" }}>
          {tab==="dashboard"   && <OwnerDashboard dealers={dealers} />}
          {tab==="schedule"    && <ServiceFeeSchedule />}
          {tab==="invoice"     && <InvoiceGenerator dealers={dealers} />}
          {tab==="projections" && <RevenueProjections />}
          {tab==="scripts"     && <CollectionScripts />}
        </div>

        <div style={{ borderTop:`1px solid ${C.border}`, padding:"16px 32px", textAlign:"center" }}>
          <div style={{ fontSize:11, color:C.inkDim, fontFamily:"'DM Mono',monospace" }}>
            Sacramento Auto Leaders Supporting Alliance (SALSA) · Administrative Compliance & Grant Management ·{" "}
            <a href="tel:5308659275" style={{ color:C.green }}>(530) 865-9275</a>
          </div>
        </div>
      </div>
    </>
  );
}
