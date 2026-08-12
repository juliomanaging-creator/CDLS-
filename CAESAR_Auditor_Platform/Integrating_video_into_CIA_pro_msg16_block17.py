import { useState, useCallback, useRef } from "react";

const ITIL_AGENTS = [
  { id:"itil_foundation", name:"ITIL Foundation Agent", icon:"⚙️", color:"#00c8ff", role:"ITIL 4 SERVICE VALUE SYSTEM", task:"Design the complete ITIL 4 Service Value System for CDLS including all 4 dimensions, 34 practices prioritized by phase, SVS components mapped to CDLS operations, and KPI targets for each practice.",
    sys:`You are the CDLS ITIL 4 Foundation Agent. Design the complete ITIL 4 Service Value System for California Dealer Logistics Solutions.

CDLS CONTEXT: ZEV logistics cooperative, Tesla Semi fleet, BaaS banking, V2G energy, LCFS carbon credits, CESAR AI (8 agents, Ollama), CalPERS $5M anchor, 20 founding dealer partners. CEO: Julio Umanzor. Critical dates: July 1 2026 DFPI, Sept 9 2026 HVIP $330K/truck.

Design with:
1. FOUR DIMENSIONS applied to CDLS (Organizations/People, Info/Tech, Partners/Suppliers, Value Streams)
2. SERVICE VALUE CHAIN: Plan-Design-Transition-Deliver-Support-Improve mapped to CDLS services
3. 34 ITIL PRACTICES: Rank all 34 by priority for CDLS. Phase 1 (months 1-3): top 8 practices. Phase 2 (months 4-6): next 12. Phase 3 (months 7-12): remaining 14.
4. KPI DASHBOARD: Target metrics for each Phase 1 practice (e.g., "Incident Management: P1 response <15 min, P2 <4 hrs, P3 <24 hrs")
5. CONTINUAL IMPROVEMENT REGISTER: Template for monthly OKR reviews tied to ISO 9001 PDCA cycle
6. GOVERNANCE MODEL: How CalPERS oversight integrates with ITIL governance practices

Be specific. Include actual KPI numbers. This is for real implementation.`
  },
  { id:"iso_9001", name:"ISO 9001 Agent", icon:"📋", color:"#00e676", role:"QUALITY MANAGEMENT SPECIALIST", task:"Produce the complete ISO 9001:2015 implementation plan with every required document, who creates it, and exact step-by-step sequence for CDLS certification within 9 months.",
    sys:`You are the CDLS ISO 9001:2015 Quality Management Agent. Produce a complete implementation plan for ISO 9001 certification within 9 months.

CDLS CONTEXT: ZEV logistics + BaaS cooperative. Services: vehicle transport, dealer banking accounts, floor plan financing, V2G energy management, carbon credit generation. 20 founding dealer partners. CalPERS institutional investor. CEO: Julio Umanzor.

Produce:
1. COMPLETE DOCUMENT LIST: Every document required for ISO 9001 certification (Quality Manual, Scope Statement, Quality Policy, Risk Register, Process Maps, SLAs, Job Descriptions, Internal Audit Procedure, Nonconformance Procedure, Corrective Action Procedure, Management Review Procedure, Customer Satisfaction Procedure)
2. DOCUMENT TEMPLATES: For the 5 most critical documents, provide an actual template with CDLS-specific content filled in
3. PROCESS MAPS: Describe the process flow for (a) dealer onboarding, (b) vehicle dispatch, (c) billing/settlement — these are the core processes auditors will examine
4. RISK & OPPORTUNITY REGISTER: List 15 specific risks for CDLS with likelihood, impact, and treatment
5. AUDIT CHECKLIST: The exact questions a BSI auditor will ask at Stage 2 — and CDLS answers
6. TIMELINE: Week-by-week Gantt from Week 1 (gap analysis) through Week 36 (certificate received)
7. CONTACT SCRIPT: Exact words to say when calling BSI Group (1-800-862-4977) to request the gap analysis

Be completely specific. Include actual CDLS content, not placeholders.`
  },
  { id:"iso_27001", name:"ISO 27001 Agent", icon:"🔐", color:"#ff5252", role:"INFORMATION SECURITY SPECIALIST", task:"Build the ISO 27001:2022 ISMS for CDLS covering BaaS banking data, dealer financial records, and CESAR AI — with Statement of Applicability, security controls implementation, and DFPI compliance mapping.",
    sys:`You are the CDLS ISO 27001:2022 Information Security Agent. Build the complete ISMS for CDLS with specific focus on DFPI banking compliance (July 1, 2026 deadline).

CDLS CONTEXT: BaaS banking platform (dealer checking/savings, floor plan financing, settlement), CESAR AI system (8 agents, Ollama local deployment, PostgreSQL, Node.js/Express, React), fleet management (Tesla Fleet API), energy management (CAISO, SMUD). Dealer financial data is the most sensitive asset.

Produce:
1. INFORMATION ASSET REGISTER: All CDLS data assets classified by sensitivity (Confidential, Restricted, Internal, Public)
2. STATEMENT OF APPLICABILITY (SOA): For each of the 93 Annex A controls — applicable to CDLS? Yes/No + justification. Focus detail on the 25 most critical controls.
3. RISK TREATMENT PLAN: Top 10 information security risks for CDLS with risk scores and treatment
4. SECURITY CONTROLS IMPLEMENTATION CHECKLIST: Specific tools and configurations for CDLS (Okta for IAM, CrowdStrike for endpoint, Datadog for SIEM, Qualys for vulnerability scanning)
5. DFPI COMPLIANCE MAPPING: How ISO 27001 controls map to California DFPI banking security requirements — this is the critical link for the July 1 deadline
6. INCIDENT RESPONSE PLAN: Specific to CDLS — what happens if BaaS accounts are breached, if CESAR AI is compromised, if dealer financial data is exfiltrated
7. VENDOR SECURITY ASSESSMENT: How to evaluate Column Bank, Coastal Community, Tesla, SMUD as third-party processors under ISO 27001

Be specific with control numbers (e.g., A.9.2.1 User Registration). Include actual CDLS system names.`
  },
  { id:"iso_14001", name:"ISO 14001 Agent", icon:"🌱", color:"#f5c842", role:"ENVIRONMENTAL MANAGEMENT SPECIALIST", task:"Design the ISO 14001:2015 Environmental Management System for the CDLS ZEV fleet — integrating with CARB LCFS, ACF regulation, V2G energy, and carbon credit monetization.",
    sys:`You are the CDLS ISO 14001:2015 Environmental Management Agent. Design the complete EMS for CDLS's zero-emission fleet operations.

CDLS CONTEXT: Tesla Semi fleet with aluminum car haulers, V2G grid services (SMUD/CAISO), LCFS carbon credits ($24.68/haul), HVIP vouchers ($330K/truck), ACF compliance (40% ZEV by 2024, 100% by 2035), Sacramento pilot. CEO: Julio Umanzor.

Produce:
1. ENVIRONMENTAL ASPECT REGISTER: All CDLS environmental aspects and impacts (ZEV charging, grid discharge, route optimization, trailer materials, charging infrastructure, end-of-life batteries)
2. LEGAL COMPLIANCE REGISTER: Every environmental regulation CDLS must comply with (CARB ACF, LCFS, California Clean Air Act, EPA Clean Truck Plan, local air quality rules)
3. ENVIRONMENTAL OBJECTIVES: 5 specific, measurable environmental objectives for CDLS (e.g., "Achieve 100% zero-emission vehicle hours by Q4 2026" with metrics)
4. LCFS INTEGRATION: How ISO 14001 documentation strengthens LCFS credit credibility — the audit trail that makes credits unimpeachable
5. V2G ENVIRONMENTAL METRICS: How to calculate and document the grid decarbonization impact of V2G operations (tons CO2 displaced per event)
6. ACF COMPLIANCE DOCUMENTATION: The specific records CARB will want to see during an ACF audit — and how ISO 14001 provides them automatically
7. ENVIRONMENTAL EMERGENCY RESPONSE: What happens if a Tesla Semi battery fire occurs — environmental response protocol

Be specific. Use actual CARB program names and regulation numbers.`
  },
  { id:"simulation", name:"Full Simulation Agent", icon:"🎮", color:"#b388ff", role:"OPERATIONAL SIMULATION SPECIALIST", task:"Run a complete CDLS operational simulation across 8 scenarios testing ITIL processes against real operational challenges — truck breakdowns, SMUD grid events, DFPI audit, CalPERS review, BaaS outage, CARB inspection, HVIP application, and dealer dispute.",
    sys:`You are the CDLS Full Operational Simulation Agent. Run a complete simulation of CDLS operations across 8 critical scenarios, testing ITIL processes against real challenges.

CDLS CONTEXT: 10 Tesla Semi trucks, 20 founding dealer partners, CESAR AI (8 agents), BaaS banking, V2G/SMUD, LCFS, CalPERS oversight, DFPI banking compliance. CEO: Julio Umanzor.

Run detailed simulations for each scenario with: Trigger → Detection → ITIL Process Activated → Actions (who does what, in what order) → Resolution → Post-Event → KPI Impact:

SCENARIO 1: Tesla Semi breakdown on I-5 with 9 vehicles loaded, 3 hours from delivery
SCENARIO 2: SMUD calls a 2-hour V2G demand response event with 6 trucks available
SCENARIO 3: DFPI examiner arrives for surprise banking compliance inspection
SCENARIO 4: CalPERS quarterly portfolio review — underperformance vs projections
SCENARIO 5: BaaS system outage at 9 AM on auction Monday — 5 dealers trying to draw floor plan
SCENARIO 6: CARB inspector arrives to verify LCFS credits for last 90 days
SCENARIO 7: September 9, 2026 HVIP portal — minute-by-minute application process
SCENARIO 8: Founding dealer disputes $18,000 V2G revenue credit — claims underpayment

For each scenario: Who responds, what ITIL practice is activated, what documents are produced, what is the SLA target, what is the CESAR AI role, and what is the outcome. Use real people titles (SDM, Compliance Officer, CEO, Route Optimization Agent, etc.).

Include post-simulation analysis: Which ITIL practices were most tested? Where are the gaps? What processes need improvement?`
  },
  { id:"contacts_guide", name:"Contacts & Readiness Agent", icon:"📞", color:"#ff9100", role:"EXECUTION READINESS SPECIALIST", task:"Generate the complete who-to-call directory and readiness checklist for every step — Phase 0 through HVIP Day — with exact phone numbers, email addresses, what to say, what to have ready, and what each step costs.",
    sys:`You are the CDLS Execution Readiness Agent. Generate the most complete, actionable contact directory and readiness checklist possible for Julio Umanzor to execute the CDLS program.

For EVERY contact, provide: Organization name, specific department, phone number, email if public, website URL, what to ask for verbatim, what documents to have ready before calling, cost range, and typical response timeline.

PHASE 0 — WEEK 1 CONTACTS (most critical):
1. DFPI Banking Registration
2. ISO 27001 vCISO engagement
3. ISO 9001 consultant engagement  
4. BaaS bank partner (Column Bank primary, Coastal Community backup)
5. Master fleet insurance broker
6. IRA §45W tax credit counsel
7. HVIP program pre-verification

PHASE 1 — MONTHS 1-3 CONTACTS:
8. ITIL training provider
9. Service desk tool vendor
10. SMUD V2G interconnection
11. IntraFi Network enrollment
12. CalPERS Emerging Manager program
13. FMCSA motor carrier authority

PHASE 2 — MONTHS 4-6 CONTACTS:
14. ISO registrar (BSI Stage 1 scheduling)
15. Penetration testing firm
16. Securities/token counsel
17. LP closings attorney
18. CARB LCFS registration

SEPTEMBER 9 HVIP DAY:
19. HVIP helpline
20. Tesla commercial fleet delivery coordination
21. Backup contacts if primary HVIP portal fails

For each contact include the exact words to say in the opening of the call/email. Example: "Hi, I'm calling on behalf of California Investment Auto LP. We're a dealer-owned zero-emission vehicle logistics cooperative launching in California. We need to discuss [specific service]. Can I speak with someone who handles [specific department]?"

Also produce: Complete document readiness checklist — for each phase, exactly what documents must be finalized before proceeding.`
  },
  { id:"master_synthesis", name:"CESAR Master Orchestrator", icon:"🧠", color:"#1de9b6", role:"EXECUTIVE SYNTHESIS & COMMAND", task:"Synthesize all subagent outputs into the CEO executive briefing — prioritized action list, critical path, risk flags, and the single most important thing Julio must do today.",
    sys:`You are the CESAR Master Orchestrator — the coordinating intelligence for California Dealer Logistics Solutions. You synthesize inputs from all specialized subagents and produce the executive decision briefing for CEO Julio Umanzor.

CDLS CONTEXT: ZEV logistics cooperative + BaaS + V2G + LCFS + blockchain. CalPERS $5M anchor. 20 founding dealer partners. Critical deadlines: July 1 2026 (DFPI banking compliance), September 9 2026 (HVIP $330K/truck first-come-first-served). Current date: March 2026 — 4 months until DFPI deadline, 6 months until HVIP.

Based on the full CDLS program scope (ITIL implementation, ISO certifications, BaaS launch, fleet insurance, dealer signing, HVIP preparation, banking charter roadmap), produce:

1. CEO MORNING BRIEFING (one page equivalent):
   - What is the single most critical action this week?
   - What are the 3 things that could cause CDLS to fail if not addressed immediately?
   - What is working well that should be protected?

2. CRITICAL PATH ANALYSIS:
   - The exact sequence of decisions that unlock everything else
   - Where are the dependencies (e.g., "can't file DFPI without ISO 27001 evidence")
   - What can be parallelized vs what must be sequential

3. 30-60-90 DAY PLAN:
   - 30 days: Top 5 actions with owners and deadlines
   - 60 days: What must be true for CDLS to be on track
   - 90 days: What does "success" look like at the end of Q2 2026

4. RISK REGISTER (TOP 10):
   - Rank the 10 biggest risks to CDLS success
   - Likelihood × Impact score
   - Mitigation already in place vs still needed

5. CAPITAL DEPLOYMENT PLAN:
   - How the $10M dealer equity + $5M CalPERS gets deployed in Year 1
   - What each dollar buys in terms of moat-building
   - When CDLS becomes cash flow positive

6. THE ONE-SENTENCE CDLS PITCH:
   - The single sentence that captures why CDLS wins

Be direct. Be specific. This is for a CEO who needs to execute today.`
  },
];

const CONTEXT = `CDLS/California Investment Auto LP: CEO Julio Umanzor, 14+ yrs automotive finance. First ZEV hauling network CA. Tesla Semi + aluminum trailers (9 vehicles/load vs 6-7 industry). V2G: $18K-$45K/truck/yr. LCFS: $24.68/haul. HVIP: $330K/truck Sept 9 2026. IRA §45W: $40K/truck. Net cost after incentives: $325K vs $720K gross. CESAR AI: 8 agents, Ollama local. Blockchain: $CDLS/$HAUL/$CARBON. 20 founding dealers, $10M equity, CalPERS $5M. Target 5K dealers 3yr via tokenization. DFPI deadline July 1 2026. Sacramento pilot hub. $4.13B royalties CA projected 10yr.`;

export default function CDLSFullSim() {
  const [results, setResults] = useState({});
  const [status, setStatus] = useState({});
  const [running, setRunning] = useState(false);
  const [selected, setSelected] = useState(null);
  const [completed, setCompleted] = useState(0);
  const [master, setMaster] = useState("");
  const [buildingMaster, setBuildingMaster] = useState(false);
  const completedRef = useRef(0);

  const runAgent = useCallback(async (agent) => {
    setStatus(p => ({ ...p, [agent.id]: "running" }));
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: agent.sys + "\n\nCDLS PLATFORM CONTEXT:\n" + CONTEXT,
          messages: [{ role: "user", content: "Execute your complete task now. Be comprehensive, specific, and actionable. Task: " + agent.task }],
        }),
      });
      const data = await res.json();
      const text = data.content?.map(b => b.text || "").join("") || "No response.";
      setResults(p => ({ ...p, [agent.id]: text }));
      setStatus(p => ({ ...p, [agent.id]: "complete" }));
    } catch (e) {
      setResults(p => ({ ...p, [agent.id]: "Error: " + e.message }));
      setStatus(p => ({ ...p, [agent.id]: "error" }));
    }
    completedRef.current += 1;
    setCompleted(completedRef.current);
  }, []);

  const runAll = async () => {
    setRunning(true);
    completedRef.current = 0;
    setCompleted(0);
    setResults({});
    setMaster("");
    const init = {};
    ITIL_AGENTS.forEach(a => { init[a.id] = "queued"; });
    setStatus(init);
    await Promise.all(ITIL_AGENTS.map(a => runAgent(a)));
    setRunning(false);
  };

  const buildMaster = async () => {
    setBuildingMaster(true);
    const summaries = ITIL_AGENTS.slice(0, -1).map(a =>
      `=== ${a.name} ===\n${(results[a.id] || "").slice(0, 400)}...`
    ).join("\n\n");
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{ role: "user", content: `CESAR MASTER SYNTHESIS for CDLS CEO Julio Umanzor.\n\nSubagent outputs:\n${summaries}\n\nProduce: (1) Single most critical action THIS WEEK, (2) Top 5 thirty-day priorities with owners, (3) Critical path dependencies, (4) Top 5 risks with scores, (5) One-sentence CDLS pitch. Be direct and executive-grade.` }],
        }),
      });
      const data = await res.json();
      setMaster(data.content?.map(b => b.text || "").join("") || "");
    } catch (e) { setMaster("Error: " + e.message); }
    setBuildingMaster(false);
  };

  const allDone = completed === ITIL_AGENTS.length && ITIL_AGENTS.length > 0;
  const progress = ITIL_AGENTS.length > 0 ? (completed / ITIL_AGENTS.length) * 100 : 0;
  const sColor = s => ({ queued:"#3a4a6a", running:"#f5c842", complete:"#00e676", error:"#ff5252" }[s] || "#3a4a6a");
  const sLabel = s => ({ queued:"Queued", running:"Running...", complete:"✓ Done", error:"Error" }[s] || "Ready");

  return (
    <div style={{ background:"#030810", minHeight:"100vh", fontFamily:"'Segoe UI',Arial,sans-serif", color:"#e8f0fe" }}>
      {/* HEADER */}
      <div style={{ background:"linear-gradient(135deg,#050d20,#0a1530)", borderBottom:"2px solid #00c8ff44", padding:"14px 20px" }}>
        <div style={{ maxWidth:"1300px", margin:"0 auto" }}>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", flexWrap:"wrap", gap:"12px" }}>
            <div>
              <div style={{ display:"flex", alignItems:"center", gap:"12px" }}>
                <div style={{ width:"44px", height:"44px", borderRadius:"10px", background:"#00c8ff22", border:"2px solid #00c8ff", display:"flex", alignItems:"center", justifyContent:"center", fontSize:"22px" }}>🧠</div>
                <div>
                  <div style={{ color:"#00c8ff", fontSize:"18px", fontWeight:900, letterSpacing:"1px" }}>CESAR ORCHESTRATOR — FULL SIM + ITIL + ISO</div>
                  <div style={{ color:"#4a6080", fontSize:"10px", marginTop:"1px" }}>7 Parallel Subagents · ITIL 4 · ISO 9001/27001/14001 · Operational Simulation · Step-by-Step Contacts</div>
                </div>
              </div>
            </div>
            <div style={{ display:"flex", gap:"10px", flexWrap:"wrap" }}>
              {[["7","Agents","#00c8ff"],[String(completed),"Done","#00e676"],[running?"ACTIVE":allDone?"COMPLETE":"READY","Status",running?"#f5c842":allDone?"#00e676":"#4a6080"]].map(([v,l,c])=>(
                <div key={l} style={{ background:c+"15", border:`1px solid ${c}44`, borderRadius:"8px", padding:"8px 14px", textAlign:"center" }}>
                  <div style={{ color:c, fontSize:"18px", fontWeight:800 }}>{v}</div>
                  <div style={{ color:"#4a6080", fontSize:"9px" }}>{l}</div>
                </div>
              ))}
            </div>
          </div>
          {(running||allDone) && (
            <div style={{ marginTop:"12px" }}>
              <div style={{ display:"flex", justifyContent:"space-between", marginBottom:"3px" }}>
                <span style={{ color:"#4a6080", fontSize:"9px" }}>PROGRESS</span>
                <span style={{ color:"#00c8ff", fontSize:"9px", fontWeight:700 }}>{Math.round(progress)}%</span>
              </div>
              <div style={{ height:"5px", background:"#0a1525", borderRadius:"3px" }}>
                <div style={{ height:"100%", width:`${progress}%`, background:"linear-gradient(90deg,#00c8ff,#00e676)", borderRadius:"3px", transition:"width 0.5s" }} />
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ maxWidth:"1300px", margin:"0 auto", padding:"18px 20px" }}>
        {/* LAUNCH */}
        {!running && !allDone && (
          <div style={{ background:"linear-gradient(135deg,#050d20,#0a1a30)", border:"1px solid #1a2d4a", borderRadius:"14px", padding:"32px", textAlign:"center", marginBottom:"20px" }}>
            <div style={{ fontSize:"44px", marginBottom:"14px" }}>🚀</div>
            <div style={{ color:"#00c8ff", fontSize:"20px", fontWeight:800, marginBottom:"6px" }}>Deploy All 7 Subagents — ITIL + ISO + Full Simulation</div>
            <div style={{ color:"#4a6080", fontSize:"12px", maxWidth:"600px", margin:"0 auto 24px", lineHeight:1.7 }}>
              Runs in parallel via Claude Sonnet API. Each agent produces a complete institutional-grade document. Files already generated: 10-slide PPTX + 50+ page DOCX guide. Subagents produce additional detailed content.
            </div>
            <div style={{ display:"flex", gap:"8px", justifyContent:"center", flexWrap:"wrap", marginBottom:"24px" }}>
              {ITIL_AGENTS.map(a => (
                <div key={a.id} style={{ display:"flex", alignItems:"center", gap:"5px", background:a.color+"15", border:`1px solid ${a.color}33`, borderRadius:"20px", padding:"4px 11px" }}>
                  <span style={{ fontSize:"12px" }}>{a.icon}</span>
                  <span style={{ color:a.color, fontSize:"9px", fontWeight:600 }}>{a.name}</span>
                </div>
              ))}
            </div>
            <button onClick={runAll} style={{ background:"linear-gradient(135deg,#00c8ff,#0070b3)", border:"none", borderRadius:"10px", padding:"14px 44px", color:"white", fontSize:"14px", fontWeight:800, cursor:"pointer", letterSpacing:"1px" }}>
              ⚡ DEPLOY ALL 7 AGENTS
            </button>
          </div>
        )}

        {/* AGENT GRID */}
        {(running || allDone) && (
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(360px,1fr))", gap:"12px", marginBottom:"20px" }}>
            {ITIL_AGENTS.map(agent => {
              const st = status[agent.id] || "queued";
              const res = results[agent.id] || "";
              const isSel = selected === agent.id;
              return (
                <div key={agent.id} style={{ background:"#070d1a", border:`1px solid ${st==="complete"?agent.color+"55":st==="running"?agent.color+"99":"#1a2d4a"}`, borderRadius:"12px", overflow:"hidden", transition:"border 0.3s" }}>
                  <div style={{ padding:"12px 14px", background:st==="running"?agent.color+"12":"transparent", borderBottom:"1px solid #0d1a2e" }}>
                    <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
                      <div style={{ display:"flex", gap:"9px", alignItems:"center" }}>
                        <div style={{ width:"34px", height:"34px", borderRadius:"8px", background:agent.color+"22", border:`1px solid ${agent.color}44`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:"16px" }}>
                          {st==="running"?"⏳":agent.icon}
                        </div>
                        <div>
                          <div style={{ color:agent.color, fontSize:"11px", fontWeight:700 }}>{agent.name}</div>
                          <div style={{ color:"#3a4a6a", fontSize:"9px", letterSpacing:"0.5px" }}>{agent.role}</div>
                        </div>
                      </div>
                      <div style={{ background:sColor(st)+"22", color:sColor(st), padding:"2px 9px", borderRadius:"10px", fontSize:"9px", fontWeight:700 }}>{sLabel(st)}</div>
                    </div>
                  </div>
                  <div style={{ padding:"9px 14px", borderBottom:"1px solid #0a1525" }}>
                    <div style={{ color:"#3a4a6a", fontSize:"9px", lineHeight:1.5 }}>{agent.task.slice(0,110)}...</div>
                  </div>
                  {res && (
                    <div style={{ padding:"9px 14px" }}>
                      <div style={{ color:"#7a90aa", fontSize:"9px", lineHeight:1.6, maxHeight:"70px", overflow:"hidden" }}>{res.slice(0,180)}...</div>
                      <button onClick={()=>setSelected(isSel?null:agent.id)}
                        style={{ marginTop:"7px", background:agent.color+"22", border:`1px solid ${agent.color}44`, borderRadius:"5px", padding:"4px 10px", color:agent.color, fontSize:"9px", cursor:"pointer", fontWeight:600 }}>
                        {isSel?"▲ Collapse":"▼ Full Output"}
                      </button>
                    </div>
                  )}
                  {isSel && res && (
                    <div style={{ padding:"10px 14px", borderTop:"1px solid #1a2d4a", background:"#040a12", maxHeight:"450px", overflowY:"auto" }}>
                      <pre style={{ color:"#b0c8e0", fontSize:"10px", lineHeight:1.7, whiteSpace:"pre-wrap", fontFamily:"inherit", margin:0 }}>{res}</pre>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* MASTER */}
        {allDone && (
          <div style={{ background:"#070d1a", border:"2px solid #1de9b6", borderRadius:"14px", overflow:"hidden", marginBottom:"18px" }}>
            <div style={{ background:"#050d20", padding:"14px 18px", borderBottom:"1px solid #1a2d4a", display:"flex", justifyContent:"space-between", alignItems:"center" }}>
              <div>
                <div style={{ color:"#1de9b6", fontSize:"15px", fontWeight:800 }}>🧠 CESAR MASTER SYNTHESIS — CEO EXECUTIVE BRIEFING</div>
                <div style={{ color:"#4a6080", fontSize:"9px", marginTop:"2px" }}>Synthesized from all 7 agents · For Julio Umanzor · March 2026</div>
              </div>
              {!master && <button onClick={buildMaster} disabled={buildingMaster}
                style={{ background:buildingMaster?"#1a2d4a":"linear-gradient(135deg,#1de9b6,#00a896)", border:"none", borderRadius:"8px", padding:"9px 18px", color:"white", fontSize:"11px", fontWeight:700, cursor:buildingMaster?"default":"pointer" }}>
                {buildingMaster?"⏳ Synthesizing...":"⚡ Generate CEO Brief"}
              </button>}
            </div>
            {master
              ? <div style={{ padding:"18px", maxHeight:"550px", overflowY:"auto" }}><pre style={{ color:"#c0d8f0", fontSize:"11px", lineHeight:1.8, whiteSpace:"pre-wrap", fontFamily:"inherit", margin:0 }}>{master}</pre></div>
              : !buildingMaster && <div style={{ padding:"28px", textAlign:"center", color:"#4a6080", fontSize:"11px" }}>All agents complete. Click "Generate CEO Brief" for the executive synthesis.</div>
            }
          </div>
        )}

        {/* DELIVERABLES PRODUCED */}
        <div style={{ background:"#070d1a", border:"1px solid #1a2d4a", borderRadius:"12px", padding:"18px", marginBottom:"16px" }}>
          <div style={{ color:"#00c8ff", fontSize:"13px", fontWeight:700, marginBottom:"12px" }}>📁 FILES ALREADY GENERATED & DOWNLOADABLE ABOVE</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"10px" }}>
            {[
              { icon:"📊", name:"CDLS_ITIL_ISO_Presentation.pptx", desc:"10-slide professional deck: ITIL SVS, ISO roadmap, Phase 0 critical actions, HVIP Day plan, Security Tiers, Simulation results, Budget, Contact directory, Competitive moat", color:"#00c8ff" },
              { icon:"📄", name:"CDLS_ITIL_ISO_Framework_Guide.docx", desc:"50+ page implementation guide: Every ITIL practice, all ISO standards with document lists, step-by-step contacts with phone numbers, simulation scenarios, complete budget, HVIP minute-by-minute plan", color:"#00e676" },
            ].map(f => (
              <div key={f.name} style={{ background:f.color+"10", border:`1px solid ${f.color}33`, borderRadius:"8px", padding:"12px" }}>
                <div style={{ display:"flex", gap:"8px", alignItems:"center", marginBottom:"5px" }}>
                  <span style={{ fontSize:"20px" }}>{f.icon}</span>
                  <div style={{ color:f.color, fontSize:"10px", fontWeight:700 }}>{f.name}</div>
                </div>
                <div style={{ color:"#7a90aa", fontSize:"9px", lineHeight:1.5 }}>{f.desc}</div>
              </div>
            ))}
          </div>
        </div>

        {allDone && <div style={{ textAlign:"center", paddingBottom:"16px" }}>
          <button onClick={()=>{ setResults({}); setStatus({}); setCompleted(0); setRunning(false); setSelected(null); setMaster(""); completedRef.current=0; }}
            style={{ background:"#0a1525", border:"1px solid #1a2d4a", borderRadius:"8px", padding:"9px 22px", color:"#4a6080", fontSize:"10px", cursor:"pointer" }}>
            ↺ Reset & Run Again
          </button>
        </div>}

        <div style={{ borderTop:"1px solid #0a1525", paddingTop:"14px", textAlign:"center" }}>
          <div style={{ color:"#1a2d4a", fontSize:"9px" }}>CESAR Multi-Agent System · CDLS / California Investment Auto, LP · Julio Umanzor, CEO · March 2026 · CONFIDENTIAL</div>
        </div>
      </div>
    </div>
  );
}