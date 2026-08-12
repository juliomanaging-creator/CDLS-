import { useState, useEffect, useRef, useCallback } from "react";

/* ─────────────────────────────────────────────────────────────────────────
   CDLS COMMAND CENTER  ×  MULTI-AGENT ORCHESTRATION PLATFORM
   Aesthetic: Obsidian command center + amber data streams + neural mesh
───────────────────────────────────────────────────────────────────────── */

const FONTS = `@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');`;

const T = {
  bg0:     "#06080E",
  bg1:     "#0A0D16",
  bg2:     "#0E1220",
  surface: "#111828",
  card:    "#131A28",
  border:  "#1A2540",
  borderA: "#2A3F6A",
  amber:   "#F59E0B",
  amberD:  "#92610A",
  amberL:  "#FCD34D",
  blue:    "#2563EB",
  blueL:   "#3B82F6",
  teal:    "#0891B2",
  tealL:   "#22D3EE",
  green:   "#059669",
  greenL:  "#10B981",
  red:     "#DC2626",
  redL:    "#EF4444",
  purple:  "#7C3AED",
  purpleL: "#A78BFA",
  text:    "#E2EBF8",
  textD:   "#8FA3C8",
  textF:   "#364B70",
  white:   "#FFFFFF",
};

// ── Sub-agents ──────────────────────────────────────────────────────────
const AGENTS = [
  { id:"COMMANDER", label:"Commander",    icon:"◈", color:T.amber,   desc:"Orchestrates all agents" },
  { id:"REPORT",    label:"Report",       icon:"◫", color:T.blueL,   desc:"Generates documents & reports" },
  { id:"TASK",      label:"Task",         icon:"◷", color:T.tealL,   desc:"Assigns tasks & owners" },
  { id:"CALENDAR",  label:"Calendar",     icon:"◉", color:T.greenL,  desc:"Maps regulatory deadlines" },
  { id:"CESAR",     label:"CESAR",        icon:"◬", color:T.purpleL, desc:"Links to platform data" },
  { id:"COMMS",     label:"Comms",        icon:"◎", color:T.redL,    desc:"Drafts communications" },
];

// ── Regulatory calendar ─────────────────────────────────────────────────
const REG_EVENTS = [
  { label:"HVIP Voucher Deadline",     date:"2026-09-09", color:T.redL,    value:"$330K/truck" },
  { label:"CA Banking Compliance",     date:"2026-07-01", color:T.amber,   value:"Treasury Prime" },
  { label:"CARB ACF Q2 Report",        date:"2026-06-30", color:T.tealL,   value:"Fleet data" },
  { label:"CalPERS Q2 Review",         date:"2026-07-15", color:T.blueL,   value:"$5M–$15M" },
  { label:"OperatorX LOI Target",      date:"2026-03-30", color:T.greenL,  value:"First deal" },
  { label:"S.A.L.S.A. Operator Event", date:"2026-04-15", color:T.purpleL, value:"20 operators" },
];

// ── Team members ────────────────────────────────────────────────────────
const TEAM = ["Julio (CEO)","Rebecca (COO/Auditor)","Dev Team","Legal/Compliance","S.A.L.S.A.","External Partner"];

// ── System prompt ───────────────────────────────────────────────────────
const SYSTEM = `You are the CDLS Command Center AI — the master orchestrator for California Dealer Logistics Solutions. You receive plain-language instructions (typed, spoken, or from uploaded documents) and transform them into structured, actionable deliverables.

## WHO YOU SERVE
Julio Umanzor — CEO & Managing Partner, CDLS / California Investment Auto LP. 14+ years automotive finance. Building California's first zero-emission vehicle hauling network + OperatorX Capital integration + National Resilience & Dignity (NRD) Initiative.

## YOUR TEAM
- Julio Matagi: CEO/Managing Partner — strategy, investor relations, key stakeholder outreach
- Rebecca McNeil: COO/Auditor — financial oversight, compliance, operations
- Dev Team: Node.js/React/PostgreSQL/Ollama/Blockchain engineers
- Legal/Compliance: Delaware LP structure, Wyoming trust, CARB reporting
- S.A.L.S.A.: Sacramento Auto Leaders Supporting Alliance (nonprofit arm)
- External Partners: CalPERS, SMUD, NVIDIA, UC Davis, Tesla Fleet, CNCDA

## CRITICAL REGULATORY DEADLINES
- September 9, 2026: HVIP voucher application deadline — $330,000 per Tesla Semi truck. ABSOLUTE HARD DEADLINE.
- July 1, 2026: California banking compliance (Treasury Prime BaaS integration)
- Ongoing: CARB Advanced Clean Fleets regulation compliance
- Q2 2026: CalPERS Emerging Manager Program review cycle

## PLATFORM CONTEXT
CDLS runs CESAR AI (Coordinated Energy & Social Asset Resource) with 7 agents:
1. Dealer Onboarding Agent, 2. Route Optimization Agent, 3. Compliance Monitoring Agent, 4. Carbon Credit Calculation Agent ($24.68/haul), 5. Financial Analytics Agent, 6. Operator Intake & OEM Verification (new), 7. Capital Deal Execution (new)

Tech stack: Node.js/Express, React/Tailwind, PostgreSQL, Ollama (llama3.2:3b local), Polygon Layer 2 blockchain ($CDLS, $HAUL, $CARBON tokens), Docker/Kubernetes, WebSocket, GitHub Actions.

Key numbers:
- Tesla Semi: $180K, 9-vehicle capacity (vs competitors' 6-7)
- Hauling rate: $356/vehicle (vs $450-533 market)
- V2G revenue: $18K-$45K/truck/year via CAISO
- LCFS carbon credits: $24.68/haul
- Federal incentives cover 91-97% of deployment costs
- Hidden dealer floorplan fees: $8K-$33K/year
- Target investors: CalPERS ($5M-$15M), 20 Founding Dealer LPs ($10M equity)
- IRR: 18-24% projected
- Exit path: $50M traditional → $2-3B tokenization path

OperatorX integration: Adding operator-capital acquisition portal. OEM-approved operators get matched to distressed dealers via CESAR audits. SBIC lenders + CalPERS capital stack.

## YOUR OUTPUT FORMAT
You MUST respond with ONLY valid JSON (no markdown wrapper, no explanation outside the JSON):

{
  "intent": "Brief plain-English description of what was requested",
  "complexity": "simple|moderate|complex",
  "agents_activated": ["COMMANDER", "REPORT", "TASK", "CALENDAR", "CESAR", "COMMS"],
  "summary": "One sentence: what was accomplished",
  "deliverables": [
    {
      "id": "del-001",
      "type": "task|report|email|analysis|code|memo|calendar_event|presentation|checklist",
      "title": "Specific descriptive title",
      "priority": "critical|high|medium|low",
      "assigned_to": "Person or team name",
      "deadline": "YYYY-MM-DD or null",
      "deadline_rationale": "Why this date",
      "regulatory_links": ["relevant regulation or deadline"],
      "cesar_nodes": ["relevant CESAR agent or data table"],
      "tags": ["finance","compliance","tech","operations","investors","community"],
      "content": "Full rich content in markdown. Be thorough. Include headers, bullet points, tables where relevant. For tasks include clear acceptance criteria. For reports include executive summary. For emails include subject line as first line prefixed with SUBJECT:. For code include full working code blocks."
    }
  ]
}

RULES:
1. Always generate at least 2 deliverables per request (usually 3-5).
2. Every task must have a specific assigned_to person and deadline.
3. Deadlines must account for the regulatory calendar above.
4. If HVIP or banking deadlines are relevant, flag as critical priority.
5. Content should be COMPLETE and IMMEDIATELY USABLE — not summaries or placeholders.
6. For code deliverables, write production-ready code.
7. For emails, write complete professional emails ready to send.
8. Link to CESAR nodes whenever platform data is involved.
9. If a document was uploaded, analyze it fully and generate deliverables from every action item found.`;

// ── Helpers ──────────────────────────────────────────────────────────────
function daysUntil(dateStr) {
  const d = new Date(dateStr);
  const now = new Date();
  return Math.ceil((d - now) / (1000 * 60 * 60 * 24));
}
function fmt(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-US", { month:"short", day:"numeric", year:"numeric" });
}
const PRIORITY_COLOR = { critical:T.redL, high:T.amber, medium:T.tealL, low:T.textD };
const TYPE_ICON = {
  task:"▶", report:"▣", email:"▷", analysis:"◈", code:"⌥",
  memo:"▤", calendar_event:"◉", presentation:"▦", checklist:"☰", default:"◫"
};

// ── CSS ──────────────────────────────────────────────────────────────────
const CSS = `
${FONTS}
*{box-sizing:border-box;margin:0;padding:0;}
:root{--amber:${T.amber};--blue:${T.blueL};--teal:${T.tealL};}
body{background:${T.bg0};color:${T.text};font-family:'DM Sans',sans-serif;overflow:hidden;height:100vh;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:${T.border};border-radius:2px;}

/* ── Layout ── */
.cc{display:grid;grid-template-rows:52px 1fr;height:100vh;overflow:hidden;}
.cc-body{display:grid;grid-template-columns:300px 1fr 340px;overflow:hidden;min-height:0;}

/* ── Top bar ── */
.topbar{background:${T.bg1};border-bottom:1px solid ${T.border};display:flex;align-items:center;padding:0 20px;gap:16px;position:relative;overflow:hidden;}
.topbar::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent,transparent 60px,${T.border}22 60px,${T.border}22 61px);pointer-events:none;}
.tb-logo{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:700;color:${T.amber};letter-spacing:.12em;display:flex;align-items:center;gap:8px;}
.tb-pulse{width:8px;height:8px;background:${T.greenL};border-radius:50%;box-shadow:0 0 8px ${T.greenL};animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 8px ${T.greenL};}50%{opacity:.4;box-shadow:0 0 16px ${T.greenL};}}
.tb-sep{width:1px;height:28px;background:${T.border};}
.tb-sub{font-family:'Space Mono',monospace;font-size:9px;color:${T.textD};letter-spacing:.08em;}
.tb-clocks{margin-left:auto;display:flex;gap:10px;align-items:center;}
.tb-clock{font-family:'Space Mono',monospace;font-size:9px;padding:4px 10px;border-radius:4px;border:1px solid;display:flex;align-items:center;gap:6px;white-space:nowrap;}
.tb-clock-days{font-weight:700;font-size:10px;}

/* ── Left panel ── */
.left-panel{background:${T.bg1};border-right:1px solid ${T.border};display:flex;flex-direction:column;overflow:hidden;}
.lp-section{padding:14px 16px 10px;border-bottom:1px solid ${T.border};}
.lp-label{font-family:'Space Mono',monospace;font-size:8.5px;letter-spacing:.12em;color:${T.textF};text-transform:uppercase;margin-bottom:10px;}

/* Command input */
.cmd-input-wrap{background:${T.surface};border:1px solid ${T.border};border-radius:8px;padding:10px 12px;transition:border-color .2s;}
.cmd-input-wrap:focus-within{border-color:${T.amber}66;}
.cmd-textarea{width:100%;background:transparent;border:none;outline:none;color:${T.text};font-family:'DM Sans',sans-serif;font-size:13px;resize:none;line-height:1.5;max-height:120px;overflow-y:auto;}
.cmd-textarea::placeholder{color:${T.textF};}
.cmd-actions{display:flex;gap:6px;margin-top:8px;align-items:center;}
.cmd-btn{height:30px;padding:0 10px;border-radius:5px;border:1px solid ${T.border};background:${T.card};color:${T.textD};font-family:'Space Mono',monospace;font-size:9px;cursor:pointer;display:flex;align-items:center;gap:5px;transition:all .15s;white-space:nowrap;}
.cmd-btn:hover{border-color:${T.amber};color:${T.amber};}
.cmd-btn.primary{background:${T.amber};border-color:${T.amber};color:${T.bg0};font-weight:700;}
.cmd-btn.primary:hover{background:${T.amberL};}
.cmd-btn.active{background:${T.redL}22;border-color:${T.redL};color:${T.redL};}
.cmd-btn:disabled{opacity:.4;cursor:not-allowed;}

/* Voice indicator */
.voice-wave{display:flex;align-items:center;gap:2px;height:16px;}
.voice-bar{width:2px;border-radius:1px;background:${T.redL};animation:wave .8s ease-in-out infinite;}
.voice-bar:nth-child(1){animation-delay:0s;}
.voice-bar:nth-child(2){animation-delay:.1s;height:10px;}
.voice-bar:nth-child(3){animation-delay:.2s;}
.voice-bar:nth-child(4){animation-delay:.3s;height:10px;}
.voice-bar:nth-child(5){animation-delay:.4s;}
@keyframes wave{0%,100%{height:4px;}50%{height:14px;}}

/* Upload */
.upload-zone{border:1.5px dashed ${T.border};border-radius:6px;padding:12px;text-align:center;cursor:pointer;transition:all .15s;}
.upload-zone:hover{border-color:${T.amber}66;background:${T.amber}08;}
.upload-zone.has-file{border-color:${T.greenL}66;background:${T.greenL}08;}
.upload-icon{font-size:20px;margin-bottom:4px;}
.upload-text{font-size:11px;color:${T.textD};}
.upload-text strong{color:${T.amber};}
.upload-file-name{font-family:'Space Mono',monospace;font-size:9px;color:${T.greenL};margin-top:4px;word-break:break-all;}

/* Suggestions */
.suggestion-list{display:flex;flex-direction:column;gap:5px;}
.suggestion{padding:8px 10px;background:${T.card};border:1px solid ${T.border};border-radius:6px;cursor:pointer;font-size:11.5px;color:${T.textD};transition:all .15s;line-height:1.4;}
.suggestion:hover{border-color:${T.amber}66;color:${T.text};background:${T.surface};}
.suggestion strong{color:${T.amber};font-size:9px;font-family:'Space Mono',monospace;display:block;margin-bottom:2px;letter-spacing:.05em;}

/* Job history */
.job-list{overflow-y:auto;flex:1;padding:8px 12px;display:flex;flex-direction:column;gap:4px;}
.job-item{padding:7px 10px;border-radius:5px;border:1px solid ${T.border};cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:8px;}
.job-item:hover{border-color:${T.borderA};background:${T.surface};}
.job-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.job-text{font-size:11px;color:${T.textD};flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.job-time{font-family:'Space Mono',monospace;font-size:8.5px;color:${T.textF};}

/* ── Center panel ── */
.center-panel{background:${T.bg0};display:flex;flex-direction:column;overflow:hidden;position:relative;}

/* Agent network */
.agent-network{padding:20px 24px 16px;flex-shrink:0;}
.an-title{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;color:${T.textF};text-transform:uppercase;margin-bottom:12px;}
.an-grid{display:flex;gap:8px;flex-wrap:wrap;}
.agent-node{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:6px;border:1.5px solid ${T.border};background:${T.bg1};transition:all .4s;position:relative;overflow:hidden;}
.agent-node.active{animation:nodeActivate .3s ease forwards;}
.agent-node.idle{opacity:.45;}
@keyframes nodeActivate{0%{transform:scale(.97);}50%{transform:scale(1.02);}100%{transform:scale(1);}}
.agent-node::before{content:'';position:absolute;inset:0;opacity:0;transition:opacity .3s;}
.agent-node.active::before{opacity:1;}
.an-icon{font-size:14px;font-family:'Space Mono',monospace;}
.an-name{font-family:'Space Mono',monospace;font-size:9px;font-weight:700;letter-spacing:.06em;}
.an-status{font-size:9px;color:${T.textF};font-family:'Space Mono',monospace;}
.an-spinner{width:10px;height:10px;border:1.5px solid transparent;border-radius:50%;animation:spin .6s linear infinite;flex-shrink:0;}
@keyframes spin{to{transform:rotate(360deg);}}

/* Processing display */
.processing-log{margin:0 24px 12px;background:${T.bg1};border:1px solid ${T.border};border-radius:8px;padding:12px 14px;font-family:'Space Mono',monospace;font-size:10.5px;color:${T.textD};min-height:60px;max-height:120px;overflow-y:auto;line-height:1.7;}
.pl-line{animation:fadeIn .2s ease;}
.pl-line.done{color:${T.greenL};}
.pl-line.working{color:${T.amber};}
.pl-caret{display:inline-block;animation:blink 1s step-end infinite;color:${T.amber};}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:0;}}
@keyframes fadeIn{from{opacity:0;transform:translateX(-4px);}to{opacity:1;transform:translateX(0);}}

/* Output area */
.output-area{flex:1;overflow-y:auto;padding:0 24px 20px;}
.oa-empty{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:12px;opacity:.5;}
.oa-empty-icon{font-size:40px;font-family:'Space Mono',monospace;color:${T.textF};}
.oa-empty-text{font-size:12px;color:${T.textF};text-align:center;font-family:'Space Mono',monospace;letter-spacing:.05em;}

/* Deliverable cards */
.del-grid{display:flex;flex-direction:column;gap:10px;}
.del-card{background:${T.card};border:1px solid ${T.border};border-radius:10px;overflow:hidden;animation:cardIn .3s ease forwards;opacity:0;}
@keyframes cardIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
.del-header{padding:10px 14px;display:flex;align-items:flex-start;gap:10px;cursor:pointer;}
.del-type-icon{font-size:16px;font-family:'Space Mono',monospace;flex-shrink:0;margin-top:1px;}
.del-meta{flex:1;min-width:0;}
.del-title{font-size:13px;font-weight:600;color:${T.text};margin-bottom:4px;line-height:1.3;}
.del-pills{display:flex;gap:5px;flex-wrap:wrap;align-items:center;}
.pill{font-family:'Space Mono',monospace;font-size:8.5px;padding:2px 7px;border-radius:3px;border:1px solid;white-space:nowrap;}
.del-expand{font-size:10px;color:${T.textF};margin-left:auto;flex-shrink:0;transition:transform .2s;padding-top:2px;}
.del-expand.open{transform:rotate(90deg);}
.del-body{padding:0 14px 14px;border-top:1px solid ${T.border};display:none;}
.del-body.open{display:block;}
.del-content{font-size:12.5px;color:${T.textD};line-height:1.7;white-space:pre-wrap;padding-top:12px;}
.del-content h1,.del-content h2,.del-content h3{color:${T.text};font-family:'Rajdhani',sans-serif;margin:10px 0 5px;letter-spacing:.03em;}
.del-content h2{font-size:14px;}
.del-content h3{font-size:12.5px;color:${T.textD};}
.del-content code{font-family:'Space Mono',monospace;font-size:10px;background:${T.surface};border:1px solid ${T.border};padding:1px 5px;border-radius:3px;color:${T.tealL};}
.del-content pre{font-family:'Space Mono',monospace;font-size:10px;background:${T.surface};border:1px solid ${T.border};border-left:3px solid ${T.amber};padding:12px;border-radius:0 6px 6px 0;overflow-x:auto;margin:8px 0;line-height:1.5;}
.del-content pre code{background:none;border:none;padding:0;color:${T.text};}
.del-footer{padding:8px 14px;background:${T.surface};border-top:1px solid ${T.border};display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
.del-assign{font-size:10.5px;color:${T.textD};display:flex;align-items:center;gap:5px;}
.del-assign strong{color:${T.text};}
.del-deadline{font-family:'Space Mono',monospace;font-size:9px;color:${T.textD};margin-left:auto;}
.del-copy{margin-left:auto;font-family:'Space Mono',monospace;font-size:8.5px;color:${T.textF};cursor:pointer;padding:3px 8px;border:1px solid ${T.border};border-radius:3px;background:transparent;transition:all .15s;}
.del-copy:hover{border-color:${T.amber};color:${T.amber};}

/* ── Right panel ── */
.right-panel{background:${T.bg1};border-left:1px solid ${T.border};overflow-y:auto;display:flex;flex-direction:column;}
.rp-section{padding:14px 16px;border-bottom:1px solid ${T.border};}
.rp-label{font-family:'Space Mono',monospace;font-size:8.5px;letter-spacing:.12em;color:${T.textF};text-transform:uppercase;margin-bottom:10px;}

/* Reg calendar */
.reg-event{padding:9px 10px;border-radius:6px;border:1px solid ${T.border};background:${T.card};margin-bottom:6px;cursor:default;transition:border-color .15s;}
.reg-event:hover{border-color:${T.borderA};}
.re-top{display:flex;align-items:center;gap:7px;margin-bottom:3px;}
.re-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.re-label{font-size:11.5px;font-weight:600;color:${T.text};flex:1;}
.re-days{font-family:'Space Mono',monospace;font-size:9.5px;font-weight:700;}
.re-bottom{display:flex;justify-content:space-between;align-items:center;padding-left:14px;}
.re-date{font-family:'Space Mono',monospace;font-size:9px;color:${T.textD};}
.re-value{font-family:'Space Mono',monospace;font-size:9px;}

/* CESAR nodes */
.cesar-node{padding:7px 10px;border-radius:5px;border:1px solid ${T.border};background:${T.card};margin-bottom:5px;display:flex;align-items:center;gap:8px;}
.cn-icon{font-size:11px;font-family:'Space Mono',monospace;}
.cn-label{font-size:11.5px;color:${T.text};}
.cn-sub{font-size:10px;color:${T.textD};margin-left:auto;font-family:'Space Mono',monospace;}

/* Summary box */
.summary-box{background:${T.surface};border:1px solid ${T.borderA};border-radius:6px;padding:10px 12px;font-size:12px;color:${T.textD};line-height:1.6;border-left:3px solid ${T.amber};}
.summary-box .sb-label{font-family:'Space Mono',monospace;font-size:8.5px;color:${T.amber};letter-spacing:.08em;margin-bottom:6px;text-transform:uppercase;}
`;

const CESAR_NODES = [
  { icon:"◈", label:"Dealer Onboarding Agent", sub:"Agent 1", color:T.blueL },
  { icon:"◎", label:"Route Optimization Agent", sub:"Agent 2", color:T.tealL },
  { icon:"◉", label:"Compliance Monitor", sub:"Agent 3 · CARB", color:T.greenL },
  { icon:"◬", label:"Carbon Credit Agent", sub:"Agent 4 · $24.68/haul", color:T.amber },
  { icon:"◫", label:"Financial Analytics", sub:"Agent 5", color:T.purpleL },
  { icon:"◈", label:"Operator Intake Agent", sub:"Agent 6 · NEW", color:T.redL },
  { icon:"◷", label:"Deal Execution Agent", sub:"Agent 7 · NEW", color:T.amber },
];

const SUGGESTIONS = [
  { cat:"REPORT",    text:"Generate a CalPERS investor update memo covering the OperatorX integration and Q1 milestones" },
  { cat:"TASK",      text:"Create a complete HVIP voucher filing task list with deadlines for all 5 trucks" },
  { cat:"ANALYSIS",  text:"Analyze the hidden floorplan fee savings for our 20 founding dealers and build the pitch" },
  { cat:"EMAIL",     text:"Draft an outreach email to Brian Maas at CNCDA about the operator acquisition platform" },
  { cat:"CALENDAR",  text:"Map all remaining deliverables against the Sept 9 and July 1 hard deadlines" },
];

// ── Render deliverable content as formatted HTML ──────────────────────
function renderContent(text) {
  return text
    .split("\n")
    .map((line, i) => {
      if (line.startsWith("### ")) return <h3 key={i}>{line.slice(4)}</h3>;
      if (line.startsWith("## "))  return <h2 key={i}>{line.slice(3)}</h2>;
      if (line.startsWith("# "))   return <h1 key={i}>{line.slice(2)}</h1>;
      if (line.startsWith("```"))  return null;
      const parts = line.split(/(`[^`]+`)/g).map((p, j) =>
        p.startsWith("`") && p.endsWith("`") ? <code key={j}>{p.slice(1,-1)}</code> : p
      );
      if (line.startsWith("- ") || line.startsWith("• ")) {
        return <div key={i} style={{paddingLeft:12,display:"flex",gap:6}}><span style={{color:T.amber,flexShrink:0}}>›</span><span>{parts}</span></div>;
      }
      if (/^\d+\. /.test(line)) {
        return <div key={i} style={{paddingLeft:12,display:"flex",gap:6}}><span style={{color:T.amber,flexShrink:0,fontFamily:"Space Mono",fontSize:9}}>{line.match(/^\d+/)[0]}.</span><span>{parts}</span></div>;
      }
      if (line.startsWith("**") && line.endsWith("**")) return <strong key={i} style={{color:T.text,display:"block"}}>{line.slice(2,-2)}</strong>;
      if (line === "" || line === "---") return <div key={i} style={{height:8}} />;
      return <p key={i}>{parts}</p>;
    });
}

// ── Deliverable Card ─────────────────────────────────────────────────
function DelCard({ del, delay }) {
  const [open, setOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const pColor = PRIORITY_COLOR[del.priority] || T.textD;
  const typeIcon = TYPE_ICON[del.type] || TYPE_ICON.default;

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(del.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="del-card" style={{ animationDelay:`${delay}ms` }}>
      <div className="del-header" onClick={() => setOpen(!open)}>
        <div className="del-type-icon" style={{ color: pColor }}>{typeIcon}</div>
        <div className="del-meta">
          <div className="del-title">{del.title}</div>
          <div className="del-pills">
            <span className="pill" style={{ color:pColor, borderColor:pColor+"44", background:pColor+"12" }}>{del.priority?.toUpperCase()}</span>
            <span className="pill" style={{ color:T.textD, borderColor:T.border }}>{del.type}</span>
            {del.tags?.slice(0,2).map((t,i) => (
              <span key={i} className="pill" style={{ color:T.textF, borderColor:T.border }}>{t}</span>
            ))}
          </div>
        </div>
        <div className={`del-expand ${open?"open":""}`}>▶</div>
      </div>

      <div className={`del-body ${open?"open":""}`}>
        <div className="del-content">{renderContent(del.content)}</div>
        {del.regulatory_links?.length > 0 && (
          <div style={{ marginTop:10, display:"flex", gap:5, flexWrap:"wrap" }}>
            {del.regulatory_links.map((r,i) => (
              <span key={i} className="pill" style={{ color:T.amber, borderColor:T.amberD, background:T.amber+"10", fontSize:8.5 }}>◉ {r}</span>
            ))}
          </div>
        )}
        {del.cesar_nodes?.length > 0 && (
          <div style={{ marginTop:6, display:"flex", gap:5, flexWrap:"wrap" }}>
            {del.cesar_nodes.map((n,i) => (
              <span key={i} className="pill" style={{ color:T.purpleL, borderColor:T.purple+"55", background:T.purple+"10", fontSize:8.5 }}>◈ {n}</span>
            ))}
          </div>
        )}
      </div>

      <div className="del-footer">
        <div className="del-assign">
          <span>→</span><strong>{del.assigned_to || "Unassigned"}</strong>
        </div>
        {del.deadline && (
          <div className="del-deadline">
            Due {fmt(del.deadline)}
            {daysUntil(del.deadline) < 30 && daysUntil(del.deadline) > 0 && (
              <span style={{ color:T.redL }}> · {daysUntil(del.deadline)}d</span>
            )}
          </div>
        )}
        <button className="del-copy" onClick={handleCopy}>
          {copied ? "✓ COPIED" : "COPY"}
        </button>
      </div>
    </div>
  );
}

// ── Main Component ───────────────────────────────────────────────────
export default function CDLSCommandCenter() {
  const [input, setInput]               = useState("");
  const [loading, setLoading]           = useState(false);
  const [activeAgents, setActiveAgents] = useState([]);
  const [logLines, setLogLines]         = useState([]);
  const [deliverables, setDeliverables] = useState([]);
  const [jobs, setJobs]                 = useState([]);
  const [summary, setSummary]           = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadedB64, setUploadedB64]   = useState(null);
  const [isListening, setIsListening]   = useState(false);
  const [error, setError]               = useState(null);

  const textareaRef  = useRef(null);
  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);
  const logRef       = useRef(null);

  // ── Voice setup ────────────────────────────────────────────────────
  useEffect(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    const r = new SR();
    r.continuous = false;
    r.interimResults = true;
    r.lang = "en-US";
    r.onresult = (e) => {
      const t = Array.from(e.results).map(r => r[0].transcript).join("");
      setInput(t);
    };
    r.onend = () => setIsListening(false);
    recognitionRef.current = r;
  }, []);

  const toggleVoice = () => {
    if (!recognitionRef.current) return;
    if (isListening) { recognitionRef.current.stop(); setIsListening(false); }
    else             { recognitionRef.current.start(); setIsListening(true); }
  };

  // ── File upload ────────────────────────────────────────────────────
  const handleFile = (file) => {
    if (!file) return;
    setUploadedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      const b64 = e.target.result.split(",")[1];
      setUploadedB64(b64);
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  // ── Log helper ─────────────────────────────────────────────────────
  const addLog = useCallback((text, type="working") => {
    setLogLines(prev => [...prev.slice(-20), { text, type, id: Date.now() + Math.random() }]);
    setTimeout(() => logRef.current?.scrollTo(0, 99999), 50);
  }, []);

  // ── Activate agent sequence ────────────────────────────────────────
  const runAgentSequence = useCallback(async (agentIds) => {
    for (const id of agentIds) {
      setActiveAgents(prev => [...prev, id]);
      await new Promise(r => setTimeout(r, 280));
    }
  }, []);

  // ── Main submit ────────────────────────────────────────────────────
  const submit = useCallback(async (overrideText) => {
    const text = (overrideText || input).trim();
    if (!text || loading) return;

    setInput("");
    setLoading(true);
    setError(null);
    setDeliverables([]);
    setSummary(null);
    setLogLines([]);
    setActiveAgents(["COMMANDER"]);

    addLog("COMMANDER initializing...", "working");
    addLog(`Parsing intent: "${text.slice(0,60)}${text.length>60?"...":""}"`, "working");

    // Build messages
    const userContent = [];
    if (uploadedB64 && uploadedFile) {
      const isPDF = uploadedFile.type === "application/pdf";
      if (isPDF) {
        userContent.push({ type:"document", source:{ type:"base64", media_type:"application/pdf", data:uploadedB64 }});
      } else {
        userContent.push({ type:"image", source:{ type:"base64", media_type:uploadedFile.type, data:uploadedB64 }});
      }
      addLog(`Document loaded: ${uploadedFile.name}`, "working");
    }
    userContent.push({ type:"text", text });

    try {
      addLog("Dispatching to sub-agents...", "working");
      await new Promise(r => setTimeout(r, 400));

      const resp = await fetch("https://api.anthropic.com/v1/messages", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body:JSON.stringify({
          model:"claude-sonnet-4-20250514",
          max_tokens:4096,
          system:SYSTEM,
          messages:[{ role:"user", content:userContent }]
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.error?.message || `API error ${resp.status}`);
      }

      const data = await resp.json();
      const rawText = data.content?.find(b => b.type==="text")?.text || "";

      addLog("Response received — parsing deliverables...", "working");

      // Parse JSON
      let parsed;
      try {
        // Strip any markdown code fences if present
        const clean = rawText.replace(/^```json\s*/,"").replace(/^```\s*/,"").replace(/\s*```$/,"").trim();
        parsed = JSON.parse(clean);
      } catch {
        // Try to extract JSON from response
        const match = rawText.match(/\{[\s\S]+\}/);
        if (match) parsed = JSON.parse(match[0]);
        else throw new Error("Could not parse agent response as JSON.");
      }

      // Activate relevant agents
      const agentIds = (parsed.agents_activated || ["COMMANDER","REPORT","TASK","CALENDAR"]);
      await runAgentSequence(agentIds.filter(a => a !== "COMMANDER"));

      for (const a of agentIds) {
        addLog(`${a} Agent: processing complete`, "done");
        await new Promise(r => setTimeout(r, 180));
      }

      const dels = parsed.deliverables || [];
      addLog(`Generated ${dels.length} deliverable${dels.length!==1?"s":""}`, "done");
      addLog("All agents complete ✓", "done");

      setDeliverables(dels);
      setSummary(parsed.summary);

      // Save to job history
      setJobs(prev => [{
        id: Date.now(),
        text: text.slice(0,55) + (text.length>55?"...":""),
        count: dels.length,
        time: new Date().toLocaleTimeString("en-US",{hour:"2-digit",minute:"2-digit"}),
        color: T.greenL
      }, ...prev.slice(0,19)]);

      setUploadedFile(null);
      setUploadedB64(null);

    } catch (err) {
      setError(err.message);
      addLog(`Error: ${err.message}`, "working");
    } finally {
      setLoading(false);
    }
  }, [input, loading, uploadedB64, uploadedFile, addLog, runAgentSequence]);

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); }
  };
  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight,120)+"px";
  };

  return (
    <>
      <style>{CSS}</style>
      <div className="cc">

        {/* ── Top Bar ── */}
        <header className="topbar">
          <div className="tb-logo">
            <div className="tb-pulse"/>
            CDLS COMMAND CENTER
          </div>
          <div className="tb-sep"/>
          <div className="tb-sub">AI ORCHESTRATION PLATFORM</div>
          <div className="tb-clocks">
            {REG_EVENTS.slice(0,3).map((e,i) => {
              const d = daysUntil(e.date);
              const urgent = d < 60;
              return (
                <div key={i} className="tb-clock"
                  style={{ borderColor: urgent ? e.color+"66" : T.border, color: urgent ? e.color : T.textD, background: urgent ? e.color+"08" : "transparent" }}>
                  <span className="tb-clock-days" style={{ color: urgent ? e.color : T.textD }}>{d}d</span>
                  <span style={{ color:T.textF }}>{e.label.split(" ").slice(0,2).join(" ")}</span>
                </div>
              );
            })}
          </div>
        </header>

        <div className="cc-body">

          {/* ── Left Panel ── */}
          <div className="left-panel">

            {/* Command input */}
            <div className="lp-section">
              <div className="lp-label">Command Input</div>
              <div className="cmd-input-wrap">
                <textarea
                  ref={textareaRef}
                  className="cmd-textarea"
                  placeholder={isListening ? "Listening… speak your command" : "Describe any report, task, or deliverable in plain language…"}
                  value={input}
                  onChange={e => { setInput(e.target.value); autoResize(); }}
                  onKeyDown={handleKey}
                  rows={3}
                  disabled={loading}
                />
                <div className="cmd-actions">
                  <button
                    className={`cmd-btn ${isListening?"active":""}`}
                    onClick={toggleVoice}
                    disabled={loading || !recognitionRef.current}
                    title={recognitionRef.current ? "Voice input" : "Voice not supported in this browser"}
                  >
                    {isListening ? (
                      <div className="voice-wave">
                        {[1,2,3,4,5].map(n => <div key={n} className="voice-bar" style={{height:8}}/>)}
                      </div>
                    ) : "🎙 VOICE"}
                  </button>
                  <button
                    className="cmd-btn primary"
                    onClick={() => submit()}
                    disabled={loading || (!input.trim() && !uploadedFile)}
                  >
                    {loading ? "◈ PROCESSING" : "▶ EXECUTE"}
                  </button>
                </div>
              </div>
            </div>

            {/* Upload */}
            <div className="lp-section">
              <div className="lp-label">Upload Document</div>
              <div
                className={`upload-zone ${uploadedFile?"has-file":""}`}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={e => e.preventDefault()}
                onDrop={handleDrop}
              >
                <div className="upload-icon">{uploadedFile ? "◈" : "◫"}</div>
                {uploadedFile ? (
                  <div className="upload-file-name">{uploadedFile.name}</div>
                ) : (
                  <div className="upload-text">Drop <strong>Next Steps PDF</strong> or any doc<br/>to auto-generate tasks from it</div>
                )}
              </div>
              <input ref={fileInputRef} type="file" style={{display:"none"}} accept=".pdf,.doc,.docx,.txt,.png,.jpg"
                onChange={e => handleFile(e.target.files[0])}/>
            </div>

            {/* Suggestions */}
            <div className="lp-section">
              <div className="lp-label">Quick Commands</div>
              <div className="suggestion-list">
                {SUGGESTIONS.map((s,i) => (
                  <div key={i} className="suggestion" onClick={() => { setInput(s.text); setTimeout(() => textareaRef.current?.focus(),50); }}>
                    <strong>{s.cat}</strong>
                    {s.text}
                  </div>
                ))}
              </div>
            </div>

            {/* Job history */}
            {jobs.length > 0 && (
              <div style={{ borderTop:`1px solid ${T.border}`, padding:"10px 16px 6px" }}>
                <div className="lp-label">Recent Jobs</div>
              </div>
            )}
            {jobs.length > 0 && (
              <div className="job-list">
                {jobs.map(j => (
                  <div key={j.id} className="job-item">
                    <div className="job-dot" style={{ background:j.color }}/>
                    <div className="job-text">{j.text}</div>
                    <div className="job-time">{j.time}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ── Center Panel ── */}
          <div className="center-panel">

            {/* Agent network */}
            <div className="agent-network">
              <div className="an-title">Agent Orchestration Network</div>
              <div className="an-grid">
                {AGENTS.map(ag => {
                  const isActive = activeAgents.includes(ag.id);
                  return (
                    <div key={ag.id} className={`agent-node ${isActive?"active":"idle"}`}
                      style={{
                        borderColor: isActive ? ag.color+"88" : T.border,
                        background:  isActive ? ag.color+"10" : T.bg1,
                      }}>
                      <div style={{ position:"absolute", inset:0, background:`radial-gradient(ellipse at 30% 50%, ${ag.color}08 0%, transparent 70%)`, opacity:isActive?1:0, transition:"opacity .4s" }}/>
                      <span className="an-icon" style={{ color: isActive ? ag.color : T.textF }}>{ag.icon}</span>
                      <div>
                        <div className="an-name" style={{ color: isActive ? ag.color : T.textF }}>{ag.label}</div>
                        <div className="an-status">{ag.desc}</div>
                      </div>
                      {isActive && loading && (
                        <div className="an-spinner" style={{ borderTopColor:ag.color, borderRightColor:ag.color+"44" }}/>
                      )}
                      {isActive && !loading && <span style={{ color:ag.color, fontSize:10, fontFamily:"Space Mono" }}>✓</span>}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Processing log */}
            {(logLines.length > 0 || loading) && (
              <div className="processing-log" ref={logRef}>
                {logLines.map(l => (
                  <div key={l.id} className={`pl-line ${l.type}`}>
                    {l.type==="done" ? "✓" : "›"} {l.text}
                  </div>
                ))}
                {loading && <span className="pl-caret">█</span>}
              </div>
            )}

            {/* Output / deliverables */}
            <div className="output-area">
              {deliverables.length === 0 && !loading ? (
                <div className="oa-empty">
                  <div className="oa-empty-icon">◈</div>
                  <div className="oa-empty-text">
                    Speak or type a command<br/>Sub-agents will generate deliverables here
                  </div>
                </div>
              ) : (
                <div className="del-grid">
                  {error && (
                    <div style={{ background:T.redL+"15", border:`1px solid ${T.redL}44`, borderRadius:8, padding:"12px 16px", color:T.redL, fontFamily:"Space Mono", fontSize:11 }}>
                      ⚠ {error}
                    </div>
                  )}
                  {deliverables.map((d,i) => (
                    <DelCard key={d.id||i} del={d} delay={i*80}/>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* ── Right Panel ── */}
          <div className="right-panel">

            {/* Summary */}
            {summary && (
              <div className="rp-section">
                <div className="rp-label">Session Summary</div>
                <div className="summary-box">
                  <div className="sb-label">COMMANDER OUTPUT</div>
                  {summary}
                </div>
              </div>
            )}

            {/* Regulatory Calendar */}
            <div className="rp-section">
              <div className="rp-label">Regulatory Calendar</div>
              {REG_EVENTS.map((e,i) => {
                const d = daysUntil(e.date);
                const urgent = d < 60 && d > 0;
                return (
                  <div key={i} className="reg-event"
                    style={ urgent ? { borderColor:e.color+"55", background:e.color+"06" } : {} }>
                    <div className="re-top">
                      <div className="re-dot" style={{ background:e.color }}/>
                      <div className="re-label">{e.label}</div>
                      <div className="re-days" style={{ color: d<30 ? T.redL : d<60 ? T.amber : T.textD }}>
                        {d>0 ? `${d}d` : "PAST"}
                      </div>
                    </div>
                    <div className="re-bottom">
                      <div className="re-date">{fmt(e.date)}</div>
                      <div className="re-value" style={{ color:e.color }}>{e.value}</div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* CESAR Nodes */}
            <div className="rp-section">
              <div className="rp-label">CESAR Agent Network</div>
              {CESAR_NODES.map((n,i) => (
                <div key={i} className="cesar-node">
                  <span className="cn-icon" style={{ color:n.color }}>{n.icon}</span>
                  <span className="cn-label">{n.label}</span>
                  <span className="cn-sub">{n.sub}</span>
                </div>
              ))}
            </div>

            {/* Team quick reference */}
            <div className="rp-section">
              <div className="rp-label">Team · Assignment Reference</div>
              {TEAM.map((t,i) => (
                <div key={i} style={{ padding:"5px 8px", borderRadius:4, border:`1px solid ${T.border}`, marginBottom:4, fontSize:11.5, color:T.textD, display:"flex", alignItems:"center", gap:6, background:T.card }}>
                  <span style={{ color:T.amber, fontFamily:"Space Mono", fontSize:9 }}>→</span>
                  {t}
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
