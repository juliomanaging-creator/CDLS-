import { useState } from "react";

// ─────────────────────────────────────────────────────────────────
//  SALSA OPERATIONS HUB
//  Fluxx Integration · Client Workflow · Dealer Connection
//  "This is how you run the whole thing"
// ─────────────────────────────────────────────────────────────────

const FONTS = `
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#F6F4F0;font-family:'Inter',sans-serif;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-thumb{background:#C9BCA8;border-radius:3px;}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.4;}}
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes checkPop{0%{transform:scale(0);}70%{transform:scale(1.2);}100%{transform:scale(1);}}
.fu{animation:fadeUp .45s cubic-bezier(.22,1,.36,1) both;}
.fi{animation:fadeIn .3s ease both;}
`;

const C = {
  bg:      "#F6F4F0",
  card:    "#FFFFFF",
  parch:   "#F0EBE1",
  sand:    "#E4DAC8",
  sandDk:  "#C9BCA8",
  sage:    "#2E5E38",
  sageMd:  "#4A8A58",
  sageLt:  "#7AB888",
  sageDim: "rgba(46,94,56,.09)",
  gold:    "#B07818",
  goldLt:  "#C89030",
  goldDim: "rgba(176,120,24,.1)",
  amber:   "#C05820",
  amberDim:"rgba(192,88,32,.09)",
  blue:    "#2858A0",
  blueDim: "rgba(40,88,160,.09)",
  purple:  "#6040A0",
  purpleDim:"rgba(96,64,160,.09)",
  ink:     "#1A1C18",
  inkMd:   "#3C3E38",
  inkFd:   "#6E7068",
  inkFaint:"#ECEAE4",
  border:  "#DDD8CE",
  success: "#2E6B42",
  successDim:"rgba(46,107,66,.1)",
  white:   "#FFFFFF",
};

// ─── FLUXX PROCESS DATA ───────────────────────────────────────────
const FLUXX_STEPS = [
  {
    id:"cbo_reg", num:1, who:"SALSA",
    title:"Register SALSA as a CBO Partner with GRID Alternatives",
    desc:"This is your starting point. GRID Alternatives administers CC4A for Sacramento region. You register SALSA as a Community Based Organization — this gives you trained access to the program, direct contact with GRID case managers, and the ability to submit applications on clients' behalf.",
    action:"Email SacCleanCars@gridalternatives.org",
    actionLink:"mailto:SacCleanCars@gridalternatives.org",
    actionAlt:"Or call (279) 207-1122 — SMAQMD CC4A line",
    docs:["SALSA Articles of Incorporation or operating agreement","EIN/Tax ID letter","Description of services you provide to clients","Service area zip codes (95815, 95823, 95824, 95838, 95842, 95820)"],
    timeline:"2–4 weeks for approval",
    color:C.sage, colorDim:C.sageDim,
    icon:"🏛️",
    note:"Once GRID registers SALSA as a CBO partner, they assign you a dedicated case manager contact. That person becomes your direct line for every client application — bypassing the public call center entirely.",
  },
  {
    id:"fluxx_account", num:2, who:"SALSA",
    title:"Create SALSA's Fluxx Account at baaqmd.fluxx.io",
    desc:"The Fluxx portal is where CC4A applications live. While each CLIENT ultimately has their own Fluxx account, SALSA creates an organizational account to monitor applications, receive status updates, and coordinate with GRID. This is separate from individual client accounts.",
    action:"Create account at baaqmd.fluxx.io",
    actionLink:"https://baaqmd.fluxx.io",
    actionAlt:"Use compliance@saclsa.org as the account email",
    docs:["SALSA organization name (exact legal name)","EIN","Service address","Designated admin email (not personal Gmail)"],
    timeline:"Same day — account is immediate",
    color:C.blue, colorDim:C.blueDim,
    icon:"💻",
    note:"Use Chrome. Fluxx has known compatibility issues with other browsers. Create a shared SALSA email for this account — not your personal email — so Rebecca or James can also access it.",
  },
  {
    id:"client_intake", num:3, who:"SALSA + CLIENT",
    title:"Client Intake → Eligibility Screen → Fluxx Account Setup",
    desc:"When a client comes in (through your Keys Forward platform, an event, or a dealer referral), SALSA screens them for eligibility, collects their 6 required documents, and then creates their individual Fluxx account at baaqmd.fluxx.io. SALSA either fills the application WITH the client (in-person or via screen share) or submits on their behalf with written authorization.",
    action:"Open client's Fluxx at baaqmd.fluxx.io",
    actionLink:"https://baaqmd.fluxx.io",
    actionAlt:"Or use Keys Forward platform eligibility screener",
    docs:["IRS Tax Return Transcript (1040) OR Medi-Cal/CalFresh award letter","SMUD/PG&E utility bill (last 60 days) — service address","Vehicle title (pink slip) — 2+ years ownership","DMV registration — no gaps >120 days","Smog report (if BAR CAP)","2-year insurance backup (if registration gaps)"],
    timeline:"15–30 min per client intake",
    color:C.gold, colorDim:C.goldDim,
    icon:"👥",
    note:"CRITICAL: The utility bill must show the SERVICE ADDRESS, not a mailing address. This is the #1 rejection cause. Check this before submitting.",
  },
  {
    id:"application", num:4, who:"SALSA",
    title:"Submit CC4A Application in Fluxx on Client's Behalf",
    desc:"Once documents are verified and the client's Fluxx account exists, SALSA submits the full application. This includes uploading all documents, filling in vehicle information, confirming eligibility answers, and clicking Submit. SALSA gets a Case ID immediately. The GRID case manager assigned to Sacramento reviews within 5–15 business days.",
    action:"Submit via baaqmd.fluxx.io",
    actionLink:"https://baaqmd.fluxx.io",
    actionAlt:"Email case manager at SacCleanCars@gridalternatives.org with Case ID",
    docs:["Client's Fluxx account credentials (or submit under SALSA CBO access)","All 4–6 documents uploaded and verified","Vehicle inspection results (Pick-n-Pull) if upgrading","Written client authorization for SALSA to submit on their behalf"],
    timeline:"Submit same day as intake if docs are ready",
    color:C.amber, colorDim:C.amberDim,
    icon:"📤",
    note:"After submission, log the Case ID in your Keys Forward CRM immediately. This is what you use for all future communication with GRID about that client. No Case ID = no visibility.",
  },
  {
    id:"inspection", num:5, who:"SALSA + CLIENT",
    title:"Schedule & Coordinate Pick-n-Pull Vehicle Inspection",
    desc:"For CC4A upgrades (not DCAP or BAR CAP), the trade-in vehicle must pass a 'start and 25-foot drive' test at a GRID-approved dismantler. In Sacramento, this is Pick-n-Pull Happy Lane. SALSA schedules this appointment, accompanies the client or provides a checklist, and uploads the passing Dismantler Report to Fluxx.",
    action:"Call Pick-n-Pull: (916) 381-3800",
    actionLink:"tel:9163813800",
    actionAlt:"4075 Happy Lane, Sacramento CA 95827",
    docs:["Client's vehicle (must start and drive 25 feet)","DMV registration in client's name","SALSA appointment confirmation letter for client"],
    timeline:"Schedule 1–2 weeks out; same-week slots sometimes available",
    color:C.sage, colorDim:C.sageDim,
    icon:"🔧",
    note:"The car just needs to start and move. Even barely driveable vehicles pass. Coach your client: the dismantler is not a smog tech — they're just confirming the car is operable.",
  },
  {
    id:"award", num:6, who:"GRID → SALSA → DEALER",
    title:"Receive Award Letter → Notify Dealer → Close the Deal",
    desc:"When GRID issues the Award Letter (4–10 weeks from submission), SALSA receives notification. SALSA immediately: (1) notifies the client, (2) logs 'Award Ready' in the Keys Forward CRM, (3) the assigned dealer gets an alert in their dealer portal and has 30 days to complete the sale before the award expires.",
    action:"Update Keys Forward CRM status to 'Award Ready'",
    actionLink:"#",
    actionAlt:"Dealer sees ⭐ alert in their portal immediately",
    docs:["Award Letter (SALSA downloads from Fluxx, sends to dealer and client)","Dealer MOU reminder (553-CA-ARB labeling, 3-day return, no markup)","Fluxx Request for Payment — dealer uploads within 5 business days of sale"],
    timeline:"Award Letter valid for 90 days (some programs 60 days)",
    color:C.success, colorDim:C.successDim,
    icon:"🏆",
    note:"The dealer is NOT in Fluxx. The dealer handles the physical sale. SALSA handles the Fluxx Request for Payment submission after the dealer reports the VIN and delivery date. This is the step most dealers miss — SALSA covers it.",
  },
  {
    id:"payment", num:7, who:"SALSA",
    title:"Submit Request for Payment → Collect Dealer Fee",
    desc:"After the vehicle is delivered, SALSA submits the Fluxx Request for Payment (RFP) within 5 business days. GRID reviews and issues payment directly to the dealer within 30 days. Once SALSA confirms the RFP is submitted and the deal is marked 'Funded' in Fluxx, SALSA invoices the dealer for the transaction service fee ($399–$750 based on tier).",
    action:"Submit RFP in Fluxx within 5 business days of sale",
    actionLink:"https://baaqmd.fluxx.io",
    actionAlt:"Then invoice dealer via QuickBooks (net-30)",
    docs:["VIN of purchased vehicle","Date of delivery","Dealer's 553-CA-ARB (signed by customer)","CDTFA-230-ZEV form","Sales contract with grant labeled as 'CC4A Grant'"],
    timeline:"RFP due within 5 biz days; GRID pays dealer 14–30 days later",
    color:C.gold, colorDim:C.goldDim,
    icon:"💰",
    note:"This is your revenue trigger. No RFP = no dealer payment = no SALSA invoice. Build a daily check into your workflow: any deals closed yesterday that need an RFP today?",
  },
];

// ─── MOCK CLIENT PIPELINE ─────────────────────────────────────────
const CLIENTS = [
  { id:"KF-0841", name:"Maria G.",   zip:"95815", program:"CC4A",  stage:5, fluxxId:"CC4A-2026-9871", caseManager:"Rosa P.",      docsComplete:true,  inspectionDone:true,  awardIssued:true,  dealerNotified:true,  rfpSubmitted:false, dealer:"Valley Ridge",  grant:"$12,000", daysOpen:42 },
  { id:"KF-0838", name:"James T.",   zip:"95824", program:"DCAP",  stage:3, fluxxId:"DCAP-2026-4491", caseManager:"Marcus W.",     docsComplete:true,  inspectionDone:false, awardIssued:false, dealerNotified:false, rfpSubmitted:false, dealer:"Valley Ridge",  grant:"$7,500",  daysOpen:28 },
  { id:"KF-0827", name:"Sofia R.",   zip:"95838", program:"CC4A",  stage:2, fluxxId:"Pending",         caseManager:"TBD",           docsComplete:false, inspectionDone:false, awardIssued:false, dealerNotified:false, rfpSubmitted:false, dealer:"Sunrise Motors",grant:"$12,000", daysOpen:14 },
  { id:"KF-0815", name:"David L.",   zip:"95823", program:"BAR",   stage:7, fluxxId:"BAR-2025-7731",  caseManager:"SALSA/Direct",  docsComplete:true,  inspectionDone:true,  awardIssued:true,  dealerNotified:true,  rfpSubmitted:true,  dealer:"Valley Ridge",  grant:"$1,450",  daysOpen:61 },
  { id:"KF-0809", name:"Yolanda P.", zip:"95815", program:"CC4A",  stage:1, fluxxId:"Not yet started", caseManager:"TBD",           docsComplete:false, inspectionDone:false, awardIssued:false, dealerNotified:false, rfpSubmitted:false, dealer:"Unassigned",    grant:"$14,000", daysOpen:3  },
];

const STAGE_LABELS = ["","CBO Intake","Fluxx Submitted","Docs Review","Inspection","Award Ready","Deal Closed","RFP Submitted"];
const STAGE_COLORS = ["",C.inkFd,C.blue,C.gold,C.amber,C.success,C.purple,C.sage];

// ─── STAT CARD ────────────────────────────────────────────────────
function Stat({ label, value, sub, color, icon, delay=0 }) {
  return (
    <div className="fu" style={{ animationDelay:`${delay}ms`, background:C.card, border:`1px solid ${C.border}`, borderRadius:12, padding:"18px 20px" }}>
      <div style={{ display:"flex", gap:10, alignItems:"flex-start" }}>
        <div style={{ fontSize:26, lineHeight:1 }}>{icon}</div>
        <div>
          <div style={{ fontSize:10, color:C.inkFd, textTransform:"uppercase", letterSpacing:".12em", fontFamily:"'DM Mono',monospace", marginBottom:6 }}>{label}</div>
          <div style={{ fontFamily:"'Lora',serif", fontSize:30, fontWeight:700, color, lineHeight:1, marginBottom:4 }}>{value}</div>
          {sub && <div style={{ fontSize:11, color:C.inkFd, lineHeight:1.5 }}>{sub}</div>}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  STARTING POINT — CRITICAL PATH
// ─────────────────────────────────────────────────────────────────
function StartingPoint() {
  const [done, setDone] = useState({ cbo:false, fluxx:false, docs:false, team:false, dealer:false });
  const complete = Object.values(done).filter(Boolean).length;

  const STEPS = [
    {
      id:"cbo", num:1, urgent:true,
      title:"Contact GRID Alternatives — Register as CBO Partner",
      detail:"This is your #1 starting point. Everything else — Fluxx access, application authority, program credibility — flows from this relationship.",
      action:"Email: SacCleanCars@gridalternatives.org",
      sub:"Subject: CBO Partnership Application — Sacramento Auto Leaders Supporting Alliance",
      time:"Do this today",
      color:C.sage,
    },
    {
      id:"fluxx", num:2, urgent:true,
      title:"Create SALSA organizational account at baaqmd.fluxx.io",
      detail:"Use compliance@saclsa.org as the account email. This is your master account for monitoring all client applications. Each client will also have their own individual account — this is SALSA's admin view.",
      action:"→ baaqmd.fluxx.io → Create Account → Organization type",
      sub:"Chrome browser only. Keep login credentials in a shared password manager.",
      time:"Same day as #1",
      color:C.blue,
    },
    {
      id:"docs", num:3, urgent:false,
      title:"Build your SALSA Document Checklist Packet",
      detail:"Create a single-page PDF document checklist you hand to every client at intake. The #1 rejection cause is wrong utility bills (mailing vs. service address). Pre-screen this before touching Fluxx.",
      action:"Use the 6-document checklist from Keys Forward portal",
      sub:"Print 50 copies. Use at every community event.",
      time:"This week",
      color:C.gold,
    },
    {
      id:"team", num:4, urgent:false,
      title:"Designate a Fluxx Submission Lead (Rebecca or James)",
      detail:"One person should own all Fluxx submissions. SALSA should not have multiple people submitting applications under different accounts — it creates audit confusion. Train one person completely, with a backup.",
      action:"Rebecca (COO/Auditor) is the natural fit — she owns compliance",
      sub:"Train on Fluxx at the GRID CBO orientation (they provide this after registration).",
      time:"Before first client event",
      color:C.amber,
    },
    {
      id:"dealer", num:5, urgent:false,
      title:"Connect Keys Forward CRM to Fluxx workflow — update dealer alerts",
      detail:"When you mark a client 'Award Ready' in the Keys Forward CRM, the assigned dealer gets notified automatically. This is already built in the dealer portal. You just need to make sure every client's Fluxx Case ID is logged in the CRM at Step 4 so the trail is complete.",
      action:"Log Fluxx Case ID in CRM immediately after submission",
      sub:"Format: CC4A-2026-XXXX or DCAP-2026-XXXX",
      time:"Built into workflow — just enforce the habit",
      color:C.purple,
    },
  ];

  return (
    <div className="fu">
      <div style={{ marginBottom:28 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.sage, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Your Critical Path</div>
        <h2 style={{ fontFamily:"'Lora',serif", fontSize:40, fontWeight:700, color:C.ink, lineHeight:1.1, marginBottom:10 }}>
          Starting Point —<br/><em style={{ color:C.gold }}>exactly where to begin</em>
        </h2>
        <p style={{ fontSize:15, color:C.inkFd, lineHeight:1.85, maxWidth:680 }}>
          These 5 actions, in this order, unlock your ability to operate Fluxx on behalf of clients. Nothing else in this system works until Step 1 is done.
        </p>
      </div>

      {/* Progress */}
      <div style={{ background:C.card, border:`1px solid ${C.border}`, borderRadius:12, padding:"16px 20px", marginBottom:24, display:"flex", justifyContent:"space-between", alignItems:"center" }}>
        <div>
          <div style={{ fontSize:13, fontWeight:700, color:C.ink, marginBottom:4 }}>Setup Progress</div>
          <div style={{ fontSize:12, color:C.inkFd }}>Check items off as you complete them</div>
        </div>
        <div style={{ textAlign:"right" }}>
          <div style={{ fontFamily:"'Lora',serif", fontSize:36, fontWeight:700, color:complete===5?C.success:C.gold }}>{complete}/5</div>
          <div style={{ width:120, height:6, background:C.parch, borderRadius:3, marginTop:6 }}>
            <div style={{ width:`${(complete/5)*100}%`, height:6, background:complete===5?C.success:C.gold, borderRadius:3, transition:"width .4s ease" }} />
          </div>
        </div>
      </div>

      <div style={{ display:"flex", flexDirection:"column", gap:14 }}>
        {STEPS.map(s => (
          <div key={s.id} onClick={() => setDone(d=>({...d,[s.id]:!d[s.id]}))}
            style={{ background:done[s.id]?C.successDim:C.card, border:`2px solid ${done[s.id]?C.success:s.urgent?"rgba(46,94,56,.3)":C.border}`, borderRadius:14, padding:"20px 22px", cursor:"pointer", transition:"all .2s" }}>
            <div style={{ display:"flex", gap:16, alignItems:"flex-start" }}>
              {/* Checkbox */}
              <div style={{ width:28, height:28, borderRadius:8, border:`2px solid ${done[s.id]?C.success:s.color}`, background:done[s.id]?C.success:"transparent", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, marginTop:2, transition:"all .2s" }}>
                {done[s.id] && <span style={{ color:C.white, fontSize:14, animation:"checkPop .25s ease" }}>✓</span>}
              </div>
              <div style={{ flex:1 }}>
                <div style={{ display:"flex", gap:10, alignItems:"center", flexWrap:"wrap", marginBottom:8 }}>
                  <div style={{ width:24, height:24, borderRadius:6, background:`${s.color}20`, display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'DM Mono',monospace", fontSize:11, fontWeight:800, color:s.color, flexShrink:0 }}>{s.num}</div>
                  <div style={{ fontFamily:"'Lora',serif", fontSize:18, fontWeight:600, color:done[s.id]?C.success:C.ink }}>{s.title}</div>
                  {s.urgent && !done[s.id] && <span style={{ fontSize:10, fontWeight:800, color:C.sage, background:C.sageDim, padding:"3px 8px", borderRadius:4, textTransform:"uppercase", letterSpacing:".08em" }}>Do first</span>}
                  <span style={{ fontSize:11, color:C.inkFd, fontFamily:"'DM Mono',monospace", marginLeft:"auto" }}>{s.time}</span>
                </div>
                <div style={{ fontSize:13, color:C.inkFd, lineHeight:1.75, marginBottom:10 }}>{s.detail}</div>
                <div style={{ background:done[s.id]?C.successDim:`${s.color}0E`, border:`1px solid ${s.color}33`, borderRadius:8, padding:"9px 14px" }}>
                  <div style={{ fontSize:13, fontWeight:700, color:s.color, marginBottom:3 }}>{s.action}</div>
                  <div style={{ fontSize:11, color:C.inkFd }}>{s.sub}</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {complete === 5 && (
        <div className="fu" style={{ background:C.successDim, border:`1.5px solid ${C.success}44`, borderRadius:12, padding:20, marginTop:20, textAlign:"center" }}>
          <div style={{ fontFamily:"'Lora',serif", fontSize:22, color:C.success, marginBottom:6 }}>✓ SALSA is fully operational</div>
          <div style={{ fontSize:13, color:C.inkFd, lineHeight:1.7 }}>All 5 setup steps complete. You can now accept clients, submit Fluxx applications, and issue dealer notifications through the Keys Forward platform.</div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  FLUXX PROCESS EXPLAINER
// ─────────────────────────────────────────────────────────────────
function FluxxProcess() {
  const [active, setActive] = useState("cbo_reg");
  const activeStep = FLUXX_STEPS.find(s => s.id === active);

  return (
    <div className="fu">
      <div style={{ marginBottom:28 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.sage, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>How It Works</div>
        <h2 style={{ fontFamily:"'Lora',serif", fontSize:40, fontWeight:700, color:C.ink, lineHeight:1.1, marginBottom:10 }}>
          The Full Fluxx<br/><em style={{ color:C.gold }}>7-Step Process</em>
        </h2>
        <p style={{ fontSize:15, color:C.inkFd, lineHeight:1.85, maxWidth:680 }}>
          Every CC4A, DCAP, and BAR CAP client follows this path. SALSA manages steps 1–4 and 7. The state (GRID Alternatives) manages steps 5–6. Dealers are only involved at the very end.
        </p>
      </div>

      {/* Three-party legend */}
      <div style={{ display:"flex", gap:10, marginBottom:24, flexWrap:"wrap" }}>
        {[["🏛️ SALSA does this","SALSA",C.sage],["👥 You + Client together","SALSA + CLIENT",C.gold],["🏆 State + Dealer","GRID → SALSA → DEALER",C.blue]].map(([l,who,c])=>(
          <div key={l} style={{ display:"flex", gap:8, alignItems:"center", background:`${c}12`, border:`1px solid ${c}33`, borderRadius:7, padding:"6px 12px" }}>
            <div style={{ width:8, height:8, borderRadius:"50%", background:c }} />
            <span style={{ fontSize:12, fontWeight:600, color:c }}>{l}</span>
          </div>
        ))}
      </div>

      <div style={{ display:"grid", gridTemplateColumns:"280px 1fr", gap:16 }}>
        {/* Step list */}
        <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
          {FLUXX_STEPS.map(step => (
            <div key={step.id} onClick={() => setActive(step.id)}
              style={{ background:active===step.id?step.colorDim:C.card, border:`1.5px solid ${active===step.id?step.color:C.border}`, borderRadius:10, padding:"12px 14px", cursor:"pointer", transition:"all .15s" }}
              onMouseEnter={e=>{ if(active!==step.id){ e.currentTarget.style.borderColor=step.color+"44"; }}}
              onMouseLeave={e=>{ if(active!==step.id){ e.currentTarget.style.borderColor=C.border; }}}>
              <div style={{ display:"flex", gap:10, alignItems:"center" }}>
                <span style={{ fontSize:20 }}>{step.icon}</span>
                <div>
                  <div style={{ fontSize:11, fontWeight:800, color:step.color, textTransform:"uppercase", letterSpacing:".08em", fontFamily:"'DM Mono',monospace", marginBottom:2 }}>Step {step.num}</div>
                  <div style={{ fontSize:13, fontWeight:active===step.id?700:500, color:C.ink, lineHeight:1.3 }}>{step.title.split("→")[0].split("—")[0].trim()}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {activeStep && (
          <div key={activeStep.id} className="fi" style={{ background:C.card, border:`1.5px solid ${activeStep.color}33`, borderRadius:14, padding:28 }}>
            <div style={{ display:"flex", gap:12, alignItems:"flex-start", marginBottom:20, paddingBottom:20, borderBottom:`1px solid ${C.border}` }}>
              <span style={{ fontSize:40, lineHeight:1 }}>{activeStep.icon}</span>
              <div>
                <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:activeStep.color, textTransform:"uppercase", letterSpacing:".12em", marginBottom:6 }}>Step {activeStep.num} — {activeStep.who}</div>
                <div style={{ fontFamily:"'Lora',serif", fontSize:22, fontWeight:700, color:C.ink, lineHeight:1.2, marginBottom:8 }}>{activeStep.title}</div>
                <div style={{ fontSize:14, color:C.inkFd, lineHeight:1.8 }}>{activeStep.desc}</div>
              </div>
            </div>

            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:20 }}>
              {/* Action */}
              <div style={{ background:activeStep.colorDim, border:`1px solid ${activeStep.color}33`, borderRadius:10, padding:"14px 16px" }}>
                <div style={{ fontSize:10, fontWeight:800, color:activeStep.color, textTransform:"uppercase", letterSpacing:".1em", fontFamily:"'DM Mono',monospace", marginBottom:8 }}>Your Action</div>
                <a href={activeStep.actionLink} target={activeStep.actionLink.startsWith("http")?"_blank":"_self"}
                  style={{ fontSize:14, fontWeight:700, color:activeStep.color, textDecoration:"none", lineHeight:1.5, display:"block", marginBottom:6 }}>
                  {activeStep.action} →
                </a>
                <div style={{ fontSize:11, color:C.inkFd }}>{activeStep.actionAlt}</div>
              </div>
              {/* Timeline */}
              <div style={{ background:C.parch, border:`1px solid ${C.border}`, borderRadius:10, padding:"14px 16px" }}>
                <div style={{ fontSize:10, fontWeight:800, color:C.inkFd, textTransform:"uppercase", letterSpacing:".1em", fontFamily:"'DM Mono',monospace", marginBottom:8 }}>Timeline</div>
                <div style={{ fontSize:14, fontWeight:700, color:C.ink }}>{activeStep.timeline}</div>
              </div>
            </div>

            {/* Docs needed */}
            <div style={{ marginBottom:20 }}>
              <div style={{ fontSize:12, fontWeight:700, color:C.inkMd, marginBottom:10, textTransform:"uppercase", letterSpacing:".08em", fontFamily:"'DM Mono',monospace" }}>Documents / Requirements</div>
              <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                {activeStep.docs.map((d,i) => (
                  <div key={i} style={{ display:"flex", gap:10, alignItems:"flex-start", fontSize:13, color:C.inkMd }}>
                    <span style={{ color:activeStep.color, marginTop:2, flexShrink:0, fontWeight:800 }}>→</span>
                    {d}
                  </div>
                ))}
              </div>
            </div>

            {/* Note */}
            <div style={{ background:C.parch, border:`1px solid ${C.sand}`, borderRadius:8, padding:"12px 16px", fontSize:13, color:C.inkFd, lineHeight:1.75 }}>
              <strong style={{ color:C.ink }}>💡 SALSA Note: </strong>{activeStep.note}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  WHO DOES WHAT — 3-WAY ROLE BREAKDOWN
// ─────────────────────────────────────────────────────────────────
function RoleBreakdown() {
  return (
    <div className="fu">
      <div style={{ marginBottom:28 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.sage, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Role Clarity</div>
        <h2 style={{ fontFamily:"'Lora',serif", fontSize:40, fontWeight:700, color:C.ink, lineHeight:1.1, marginBottom:10 }}>
          Who does what —<br/><em style={{ color:C.gold }}>SALSA vs. Dealers vs. State</em>
        </h2>
        <p style={{ fontSize:15, color:C.inkFd, lineHeight:1.85, maxWidth:680 }}>The reason this system works is that each party has exactly one job. Confusion comes from roles overlapping — this table eliminates that.</p>
      </div>

      {/* The three parties */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:16, marginBottom:28 }}>
        {[
          {
            who:"SALSA (You)", sub:"Sacramento Auto Leaders Supporting Alliance", color:C.sage, colorDim:C.sageDim, icon:"🏛️",
            does:[
              "Register as CBO with GRID Alternatives",
              "Screen clients for eligibility",
              "Collect and verify 6 required documents",
              "Create and submit Fluxx application",
              "Schedule Pick-n-Pull inspection",
              "Receive Award Letter from GRID",
              "Notify dealer through Keys Forward portal",
              "Submit Request for Payment post-sale",
              "Invoice dealer the service fee",
              "Track all clients in CRM"
            ],
            doesnt:["Touch the vehicle sale","Handle dealer financing","Process state payments to dealer","Guarantee grant approvals"]
          },
          {
            who:"Partner Dealers", sub:"Valley Ridge, Gold Country Kia, etc.", color:C.purple, colorDim:C.purpleDim, icon:"🚗",
            does:[
              "Receive award-ready buyer notification",
              "Welcome client to lot with confirmed grant",
              "Verify award letter amount",
              "Select vehicle (matching program requirements)",
              "Complete sale per compliance checklist",
              "Label grant as 'CC4A Grant' on 553-CA-ARB",
              "Honor no-markup and APR cap rules",
              "Give client 3-day return disclosure",
              "Report VIN and delivery date to SALSA",
              "Pay SALSA service fee within 30 days"
            ],
            doesnt:["Touch Fluxx — ever","Submit state applications","Create client accounts","Handle document collection"]
          },
          {
            who:"State / GRID Alternatives", sub:"SMAQMD + GRID Alternatives (CC4A)", color:C.blue, colorDim:C.blueDim, icon:"🏦",
            does:[
              "Administer the CC4A/DCAP/BAR CAP programs",
              "Review Fluxx applications",
              "Assign case managers",
              "Request missing documents",
              "Issue Award Letters",
              "Process vehicle inspections",
              "Pay dealers after RFP submission",
              "Audit compliance annually",
              "Run the Fluxx portal (baaqmd.fluxx.io)"
            ],
            doesnt:["Find clients — that's SALSA's job","Work with dealers directly","Manage post-sale paperwork","Invoice for compliance services"]
          }
        ].map(party => (
          <div key={party.who} style={{ background:C.card, border:`1.5px solid ${party.color}33`, borderRadius:14, padding:24 }}>
            <div style={{ display:"flex", gap:10, alignItems:"center", marginBottom:16, paddingBottom:16, borderBottom:`1px solid ${C.border}` }}>
              <span style={{ fontSize:32 }}>{party.icon}</span>
              <div>
                <div style={{ fontFamily:"'Lora',serif", fontSize:17, fontWeight:700, color:C.ink }}>{party.who}</div>
                <div style={{ fontSize:11, color:C.inkFd, marginTop:2 }}>{party.sub}</div>
              </div>
            </div>
            <div style={{ fontSize:11, fontWeight:800, color:party.color, textTransform:"uppercase", letterSpacing:".1em", fontFamily:"'DM Mono',monospace", marginBottom:10 }}>✓ Responsible for</div>
            {party.does.map(d => (
              <div key={d} style={{ display:"flex", gap:8, alignItems:"flex-start", fontSize:12, color:C.inkMd, padding:"4px 0", borderBottom:`1px solid ${C.inkFaint}` }}>
                <span style={{ color:party.color, flexShrink:0, fontWeight:800, fontSize:10, marginTop:3 }}>→</span>{d}
              </div>
            ))}
            <div style={{ fontSize:11, fontWeight:800, color:C.amber, textTransform:"uppercase", letterSpacing:".1em", fontFamily:"'DM Mono',monospace", marginTop:14, marginBottom:8 }}>✕ NOT responsible for</div>
            {party.doesnt.map(d => (
              <div key={d} style={{ fontSize:12, color:C.inkFd, padding:"3px 0", borderBottom:`1px solid ${C.inkFaint}` }}>
                <span style={{ marginRight:6, opacity:.5 }}>—</span>{d}
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Fluxx account breakdown */}
      <div style={{ background:C.card, border:`1px solid ${C.border}`, borderRadius:14, padding:24 }}>
        <div style={{ fontFamily:"'Lora',serif", fontSize:20, fontWeight:700, color:C.ink, marginBottom:16 }}>Fluxx Account Structure — Who Has What</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:12 }}>
          {[
            { who:"SALSA",   type:"Organization Account",    url:"baaqmd.fluxx.io", email:"compliance@saclsa.org", access:"Monitor all SALSA-assisted applications, receive status notifications, communicate with GRID case managers",  color:C.sage  },
            { who:"Clients", type:"Individual Grantee Account", url:"baaqmd.fluxx.io", email:"Client's personal email",     access:"Their own application is tied to their SSN and personal info. SALSA helps them create and fill this. SALSA does NOT log in as the client.",  color:C.gold  },
            { who:"Dealers", type:"NO Fluxx account needed",  url:"N/A",             email:"N/A",                           access:"Dealers have zero interaction with Fluxx. They receive award letters from SALSA, make the sale, and report VIN/delivery date back to SALSA. SALSA handles the RFP.",  color:C.inkFd },
          ].map(acct => (
            <div key={acct.who} style={{ background:C.parch, border:`1px solid ${C.sand}`, borderRadius:10, padding:18 }}>
              <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:acct.color, textTransform:"uppercase", letterSpacing:".1em", marginBottom:8 }}>{acct.who}</div>
              <div style={{ fontSize:14, fontWeight:700, color:C.ink, marginBottom:6 }}>{acct.type}</div>
              <div style={{ fontSize:12, fontWeight:600, color:acct.color, fontFamily:"'DM Mono',monospace", marginBottom:8 }}>{acct.url}</div>
              <div style={{ fontSize:12, color:C.inkFd, lineHeight:1.65 }}>{acct.access}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  CLIENT PIPELINE TRACKER
// ─────────────────────────────────────────────────────────────────
function ClientTracker() {
  const [selected, setSelected] = useState(null);

  const stageDesc = [
    "", "Client screened. Collecting documents.", "Fluxx application submitted. Awaiting review.",
    "GRID reviewing docs. May request additional info.", "Inspection at Pick-n-Pull scheduled/complete.",
    "Award Letter issued! Dealer notified.", "Vehicle sold. Awaiting RFP.", "RFP submitted. Dealer payment processing."
  ];

  return (
    <div className="fu">
      <div style={{ marginBottom:24 }}>
        <div style={{ fontFamily:"'DM Mono',monospace", fontSize:10, color:C.sage, letterSpacing:".15em", textTransform:"uppercase", marginBottom:8 }}>Live Pipeline</div>
        <h2 style={{ fontFamily:"'Lora',serif", fontSize:36, fontWeight:700, color:C.ink, lineHeight:1.1 }}>Client Fluxx Tracker</h2>
      </div>

      {/* Stats */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:12, marginBottom:20 }}>
        <Stat label="Active Clients"    value={CLIENTS.filter(c=>c.stage<7).length} sub="In Fluxx pipeline"     color={C.sage}  icon="👥" delay={0}  />
        <Stat label="Award Ready"       value={CLIENTS.filter(c=>c.stage===5).length} sub="Contact dealer now" color={C.success} icon="🏆" delay={60} />
        <Stat label="RFPs Needed"       value={CLIENTS.filter(c=>c.stage===6).length} sub="Submit within 5 days" color={C.amber} icon="📤" delay={120} />
        <Stat label="Completed"         value={CLIENTS.filter(c=>c.stage===7).length} sub="This month"          color={C.sage}  icon="✅" delay={180} />
      </div>

      {/* Table */}
      <div style={{ background:C.card, border:`1px solid ${C.border}`, borderRadius:14, overflow:"hidden" }}>
        <table style={{ width:"100%", borderCollapse:"collapse" }}>
          <thead>
            <tr style={{ background:C.ink }}>
              {["Client","ID","Program","Fluxx Case ID","Dealer","Grant","Stage","Fluxx Status","Action"].map(h=>(
                <th key={h} style={{ padding:"10px 14px", fontSize:10, color:"rgba(255,255,255,.4)", textAlign:"left", fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".06em", whiteSpace:"nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {CLIENTS.map((c,i)=>{
              const sc = STAGE_COLORS[c.stage];
              const sl = STAGE_LABELS[c.stage];
              const needsAction = c.stage===5?{ label:"Notify dealer", color:C.success } : c.stage===6?{ label:"Submit RFP",color:C.amber } : c.stage===2&&!c.docsComplete?{ label:"Fix docs",color:C.gold } : null;
              return (
                <tr key={c.id} onClick={()=>setSelected(selected?.id===c.id?null:c)} style={{ borderBottom:`1px solid ${C.border}`, cursor:"pointer" }}
                  onMouseEnter={e=>e.currentTarget.style.background=C.parch}
                  onMouseLeave={e=>e.currentTarget.style.background="transparent"}>
                  <td style={{ padding:"11px 14px", fontSize:13, fontWeight:700, color:C.ink }}>{c.name}</td>
                  <td style={{ padding:"11px 14px", fontFamily:"'DM Mono',monospace", fontSize:11, color:C.inkFd }}>{c.id}</td>
                  <td style={{ padding:"11px 14px", fontSize:12, color:C.inkMd }}>{c.program}</td>
                  <td style={{ padding:"11px 14px", fontFamily:"'DM Mono',monospace", fontSize:11, color:C.blue }}>{c.fluxxId}</td>
                  <td style={{ padding:"11px 14px", fontSize:12, color:C.inkMd }}>{c.dealer}</td>
                  <td style={{ padding:"11px 14px", fontFamily:"'DM Mono',monospace", fontSize:13, fontWeight:800, color:C.sage }}>{c.grant}</td>
                  <td style={{ padding:"11px 14px" }}>
                    <div style={{ display:"flex", alignItems:"center", gap:6 }}>
                      <div style={{ width:6, height:6, borderRadius:"50%", background:sc, flexShrink:0 }} />
                      <span style={{ fontSize:11, fontWeight:700, color:sc }}>{sl}</span>
                    </div>
                  </td>
                  <td style={{ padding:"11px 14px" }}>
                    <div style={{ display:"flex", flexDirection:"column", gap:2 }}>
                      {[["Docs",c.docsComplete],["Inspection",c.inspectionDone],["Award",c.awardIssued],["RFP",c.rfpSubmitted]].map(([l,d])=>(
                        <div key={l} style={{ display:"flex", gap:4, alignItems:"center", fontSize:10, color:d?C.success:C.inkFd }}>
                          <span>{d?"✓":"○"}</span>{l}
                        </div>
                      ))}
                    </div>
                  </td>
                  <td style={{ padding:"11px 14px" }}>
                    {needsAction && (
                      <button style={{ padding:"5px 10px", background:`${needsAction.color}12`, border:`1px solid ${needsAction.color}44`, color:needsAction.color, borderRadius:5, fontSize:11, fontWeight:800, cursor:"pointer" }}>
                        {needsAction.label}
                      </button>
                    )}
                    {c.stage===7 && <span style={{ fontSize:11, color:C.success, fontWeight:700 }}>Complete ✓</span>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Selected detail */}
      {selected && (
        <div className="fu" style={{ background:C.card, border:`1px solid ${C.sage}33`, borderRadius:12, padding:22, marginTop:12 }}>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:16 }}>
            <div style={{ fontFamily:"'Lora',serif", fontSize:18, color:C.ink }}>{selected.name} — Fluxx Detail</div>
            <button onClick={()=>setSelected(null)} style={{ background:"transparent", border:"none", color:C.inkFd, fontSize:20, cursor:"pointer" }}>×</button>
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(5,1fr)", gap:10, marginBottom:16 }}>
            {[["Fluxx ID",selected.fluxxId],["Case Manager",selected.caseManager],["Program",selected.program],["Days Open",selected.daysOpen+" days"],["Stage",STAGE_LABELS[selected.stage]]].map(([k,v])=>(
              <div key={k} style={{ background:C.parch, borderRadius:7, padding:"10px 12px" }}>
                <div style={{ fontSize:9, color:C.inkFd, textTransform:"uppercase", letterSpacing:".1em", fontFamily:"'DM Mono',monospace", marginBottom:3 }}>{k}</div>
                <div style={{ fontSize:12, fontWeight:700, color:C.ink }}>{v}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize:13, color:C.inkFd, lineHeight:1.7 }}>
            <strong style={{ color:C.inkMd }}>Next step: </strong>{stageDesc[selected.stage]}
            {selected.stage===5 && <span style={{ color:C.success, fontWeight:700 }}> → Log into Keys Forward portal and mark as Award Ready to trigger dealer notification.</span>}
            {selected.stage===6 && <span style={{ color:C.amber, fontWeight:700 }}> → Submit Request for Payment at baaqmd.fluxx.io within {5-((selected.daysOpen)%5)} business days.</span>}
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
//  MAIN APP
// ─────────────────────────────────────────────────────────────────
export default function SALSAFluxxHub() {
  const [view, setView] = useState("start");

  const TABS = [
    { id:"start",    label:"🚦 Starting Point"   },
    { id:"process",  label:"🔄 Fluxx Process"     },
    { id:"roles",    label:"👥 Who Does What"     },
    { id:"tracker",  label:"📊 Client Tracker"    },
  ];

  return (
    <>
      <style>{FONTS}</style>
      <div style={{ background:C.bg, minHeight:"100vh" }}>
        {/* Header */}
        <div style={{ background:C.card, borderBottom:`1px solid ${C.border}`, padding:"0 32px" }}>
          <div style={{ maxWidth:1300, margin:"0 auto", height:56, display:"flex", alignItems:"center", justifyContent:"space-between" }}>
            <div style={{ display:"flex", alignItems:"center", gap:10 }}>
              <div style={{ width:32, height:32, borderRadius:8, background:`linear-gradient(135deg,${C.sage},${C.sageMd})`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:16 }}>🔑</div>
              <div>
                <div style={{ fontFamily:"'Lora',serif", fontSize:15, fontWeight:700, color:C.ink }}>SALSA Operations Hub</div>
                <div style={{ fontSize:9, color:C.inkFd, fontFamily:"'DM Mono',monospace", textTransform:"uppercase", letterSpacing:".12em" }}>Fluxx Integration · Client Management · Dealer Pipeline</div>
              </div>
            </div>
            <div style={{ display:"flex", alignItems:"center", gap:16 }}>
              <a href="https://baaqmd.fluxx.io" target="_blank" style={{ fontSize:12, color:C.blue, fontWeight:700, textDecoration:"none", fontFamily:"'DM Mono',monospace" }}>baaqmd.fluxx.io ↗</a>
              <a href="mailto:SacCleanCars@gridalternatives.org" style={{ fontSize:12, color:C.sage, fontWeight:700, textDecoration:"none", fontFamily:"'DM Mono',monospace" }}>SacCleanCars@gridalternatives.org ↗</a>
            </div>
          </div>
        </div>

        {/* Nav */}
        <div style={{ background:C.card, borderBottom:`1px solid ${C.border}`, padding:"0 32px" }}>
          <div style={{ maxWidth:1300, margin:"0 auto", display:"flex", gap:2 }}>
            {TABS.map(t=>(
              <button key={t.id} onClick={()=>setView(t.id)}
                style={{ padding:"13px 20px", background:"transparent", border:"none", borderBottom:`2px solid ${view===t.id?C.sage:"transparent"}`,
                          color:view===t.id?C.sage:C.inkFd, fontSize:13, fontWeight:view===t.id?700:400,
                          cursor:"pointer", whiteSpace:"nowrap", transition:"all .15s" }}>
                {t.label}
              </button>
            ))}
          </div>
        </div>

        <div style={{ maxWidth:1300, margin:"0 auto", padding:"32px 32px" }}>
          {view==="start"   && <StartingPoint />}
          {view==="process" && <FluxxProcess />}
          {view==="roles"   && <RoleBreakdown />}
          {view==="tracker" && <ClientTracker />}
        </div>
      </div>
    </>
  );
}
