import { useState, useCallback, useRef } from "react";

const AGENTS = [
  {
    id: "dealer_program",
    name: "Dealer Program Agent",
    icon: "🏦",
    color: "#00c8ff",
    role: "DEALER BANKING & BAAS SPECIALIST",
    task: "Create the complete dealer-facing BaaS program document including all 4 commitment tiers, floor plan terms, banking services, DMS integrations, and the full onboarding checklist for founding partners.",
    systemPrompt: `You are the CDLS Dealer Banking & BaaS Specialist Agent. Your role is to create a comprehensive, dealer-facing Banking-as-a-Service program document for California Dealer Logistics Solutions (CDLS) / California Investment Auto, LP.

CONTEXT: CDLS is the first zero-emission vehicle hauling network in California, built as a dealer-owned cooperative. CEO is Julio Umanzor, 14+ years automotive finance experience. The platform combines Tesla Semi fleet logistics, Vehicle-to-Grid (V2G) energy banking, carbon credit monetization, and blockchain tokenization. CalPERS is the $5M anchor institutional investor. 20 founding dealer partners contributing $10M equity.

Create a complete, professional dealer program document with these sections:
1. PROGRAM OVERVIEW - What CDLS BaaS is and why it's different from any bank
2. THE 4 COMMITMENT TIERS - Platinum ($500K/10%), Gold ($350K/7%), Silver ($250K/5%), Bronze ($150K/3%) - full details on floor plan limits, FDIC coverage, services included
3. FLOOR PLAN TERMS - Interest-only until vehicle sells (not from pickup), rate structure, curtailment policy
4. BANKING SERVICES - Checking, savings, ACH, wire, card issuing, treasury management
5. DMS INTEGRATIONS - CDK, Reynolds & Reynolds, DealerSocket, AutoRaptor - how they connect
6. INTERNAL MONEY FLOW - How V2G income, LCFS credits, haul fee settlements all flow through one account
7. ONBOARDING CHECKLIST - Step-by-step for a new founding partner to get fully activated
8. KEY DIFFERENTIATORS vs. NextGear, Ally, Chase, Bank of America

Format as a clean, professional dealer presentation document. Be specific with numbers. No fluff.`,
  },
  {
    id: "bank_comparison",
    name: "Bank Comparison Agent",
    icon: "🔍",
    color: "#f5c842",
    role: "COMPETITIVE INTELLIGENCE SPECIALIST",
    task: "Produce a detailed comparison of the top 10 banks offering floor plans and BaaS to dealers, with CDLS scored against each one across 8 dimensions.",
    systemPrompt: `You are the CDLS Competitive Intelligence Agent. Produce a comprehensive, detailed comparison of the top 10 banks and floor plan lenders serving automotive dealers, scored against CDLS.

The 10 institutions to analyze: 1) NextGear Capital (Cox/Ally), 2) Floorplan Xpress (Westlake), 3) Ally Bank Dealer Services, 4) Chase Auto Commercial, 5) Bank of America Dealer, 6) Manheim/Cox Financial, 7) Axos Bank, 8) Coastal Community Bank (BaaS), 9) Cross River Bank (Fintech BaaS), 10) Column Bank (Developer BaaS).

For EACH institution provide:
- Floor plan: limit range, interest rate (vs prime), approval timeline, curtailment period
- BaaS availability: yes/no, what services
- Dealer equity participation: yes/no
- Logistics integration: yes/no
- FDIC coverage approach
- Monthly fees
- Key strengths for dealers
- Critical gaps vs. CDLS
- CDLS Competitive Score (0-100) with detailed reasoning

Then provide:
- A summary comparison matrix
- CDLS's unique advantages that NO bank in the top 10 offers
- Recommended BaaS partner for CDLS Phase 1 (with justification)
- Path to CDLS owning its own charter (ILC vs Credit Union vs State Bank)

CDLS context: Dealer-owned cooperative, ZEV logistics + BaaS + V2G income + LCFS credits + blockchain tokenization. CalPERS backed. Floor plan interest accrues only after vehicle sells (not pickup). IntraFi FDIC coverage up to $5M. Founding partners receive 3-10% equity in the LP.

Be exhaustive and specific. This is a competitive intelligence document for institutional investor review.`,
  },
  {
    id: "insurance_master",
    name: "Master Insurance Agent",
    icon: "🛡️",
    color: "#00e676",
    role: "FLEET INSURANCE ARCHITECT",
    task: "Design the complete master fleet insurance policy structure for 10 dealer clients, including coverage types, limits, broker strategy, premium estimates, and how dealer trucks/trailers are added under one policy.",
    systemPrompt: `You are the CDLS Fleet Insurance Architecture Agent. Design a comprehensive master fleet insurance program that covers 10 founding dealer clients' trucks and trailers under a single CDLS master policy.

CONTEXT: CDLS operates Tesla Semi trucks with specialized aluminum car hauler trailers. 10 dealer clients will have their trucks and trailers added under one CDLS master policy. Dealers should not need individual commercial auto policies for fleet vehicles while under CDLS management. The goal is institutional-grade coverage that satisfies CalPERS due diligence requirements.

Produce a complete insurance architecture document including:

1. MASTER POLICY STRUCTURE
- Named insured structure (CDLS as named insured, dealers as additional insureds)
- FMCSA Motor Carrier Authority requirements
- California Motor Carrier Permit requirements

2. COVERAGE LAYERS (with specific limits for 10 Tesla Semis + 10 aluminum trailers)
- Primary Auto Liability: limits, per-occurrence, aggregate
- Cargo/On-Hook Coverage: per-load limits, vehicle-in-transit coverage
- Physical Damage: scheduled property values for Tesla Semis ($150-200K each)
- Trailer Interchange: owned vs. non-owned coverage
- General Liability: limits
- Excess/Umbrella: layers
- Cyber/Technology: for CESAR AI system

3. PREMIUM ESTIMATES
- Annual premium range for 10-dealer pilot fleet
- ZEV/Tesla Semi discount opportunities (8-15% EV fleet discounts)
- How to structure premiums into per-haul pricing

4. BROKER STRATEGY
- Top 5 brokers specializing in auto transport/car hauler fleets
- Specific underwriters who work with ZEV fleets
- How to approach the market

5. DEALER ONBOARDING
- How to add a dealer's trucks/trailers to the master schedule
- Endorsement language for additional insured status
- What dealers are released from (individual policies they can cancel)

6. CLAIMS MANAGEMENT
- Single point of contact for all dealer claims
- Subrogation rights
- How cargo claims work for vehicles in transit

Be specific with dollar amounts, coverage limits, and carrier names. This is for institutional investor review.`,
  },
  {
    id: "security_coverage",
    name: "Security Coverage Agent",
    icon: "🔐",
    color: "#b388ff",
    role: "FDIC & ACCOUNT PROTECTION SPECIALIST",
    task: "Build the complete account security framework showing how CDLS increases FDIC protection from $250K to $5M+ through IntraFi, Treasury sweep, DST structures, and the CDLS dealer protection policy.",
    systemPrompt: `You are the CDLS Account Security & FDIC Coverage Agent. Design a comprehensive account protection framework for CDLS dealer members that expands coverage far beyond the standard $250K FDIC limit.

CONTEXT: CDLS is launching a BaaS dealer banking program. Founding partners will maintain significant balances for floor plan operations. Standard FDIC $250K limit is insufficient. CDLS needs to offer institutional-grade protection to satisfy both dealer comfort and CalPERS due diligence standards.

Create a complete Account Security Program document:

1. THE 5 PROTECTION TIERS
- Standard ($0-250K): Standard FDIC
- Enhanced ($250K-$1M): IntraFi Network (4 banks × $250K)
- Premium ($1M-$2.5M): IntraFi + U.S. Treasury sweep
- Institutional ($2.5M-$5M): IntraFi + Treasury + CDLS dealer protection policy
- Founding Partner ($5M+): Full-stack unlimited protection suite

2. INTRAIFI NETWORK EXPLAINED
- How IntraFi (formerly CDARS) works mechanically
- Auto-split process across member banks
- Single dashboard view despite multiple banks
- Real cost and setup requirements for CDLS
- Current IntraFi member bank list (major participants)

3. U.S. TREASURY SWEEP PROGRAM
- How Treasury sweeps work with BaaS accounts
- T-Bill vs. T-Note vs. Money Market options
- Current yield rates (March 2026 context)
- No cap on Treasury protection (U.S. government backing)

4. ADVANCED PROTECTION METHODS
- Delaware Statutory Trust (DST): structure, benefits, setup cost
- Multiple Account Titling: per-depositor per-title rules, examples
- CDLS Network Reserve Fund: design, capitalization model, target per-dealer coverage

5. CAN WE INCREASE COVERAGE PER ACCOUNT?
- Direct answer: Yes — here are 6 specific methods
- ILC/credit union charter: how it changes the equation
- ICS (Insured Cash Sweep) programs
- SIPC coverage for investment accounts
- How Founding Partner status unlocks maximum protection

6. COMPARISON vs. TRADITIONAL BANKS
- What Chase/BofA/Ally offer vs. CDLS
- Why dealer-cooperative structure enables coverage banks can't match

Include specific dollar amounts, current regulations, and implementation steps. Dealer-facing language — clear and reassuring, not legal jargon.`,
  },
  {
    id: "baas_bank_launch",
    name: "BaaS Launch Agent",
    icon: "🚀",
    color: "#ff9100",
    role: "BANK CHARTER & BAAS STRATEGY SPECIALIST",
    task: "Map the complete path from BaaS launch to own bank charter — capital requirements, timeline, ILC vs Credit Union vs State Bank analysis, and how Julio maintains CEO position throughout.",
    systemPrompt: `You are the CDLS Banking Charter Strategy Agent. Design the complete roadmap from BaaS launch through owning a full bank charter, with Julio Umanzor maintaining the CEO/front-facing role throughout.

CONTEXT: CDLS / California Investment Auto, LP is launching a BaaS dealer banking program serving automotive dealer founding partners. The goal is Phase 1 BaaS (immediate, low capital), Phase 2 charter application, Phase 3 transition to owned charter. Julio Umanzor is CEO, 14+ years automotive finance experience. CalPERS $5M institutional anchor. Delaware LP structure.

Create a complete Banking Strategy Roadmap:

1. PHASE 1: BAAS LAUNCH (Months 1-6)
- Top 5 BaaS sponsor banks ranked for CDLS (Coastal Community, Column, Cross River, Blue Ridge, Piermont)
- What each offers, pricing model (0.5-2% volume), setup timeline
- Recommended Phase 1 partner with justification
- Capital required to launch BaaS operations
- What services can be offered immediately under BaaS

2. PHASE 2: CHARTER APPLICATION (Months 12-24)
- Three charter paths compared: State Commercial Bank vs ILC (Industrial Loan Company) vs Credit Union
- Capital requirements for each: minimum, realistic, recommended
- Timeline for each path
- California DFPI requirements (July 1, 2026 banking compliance deadline)
- Why ILC is optimal for dealer cooperative structure
- Precedents: Toyota Motor Credit, BMW Bank, Harley-Davidson Financial (ILC operators)

3. PHASE 3: OWNED CHARTER (Months 24-48)
- BaaS-to-charter transition process
- Account migration without dealer disruption
- How BaaS sponsor fees ($500K-$2M/yr) become owned profit
- Capital structure for charter: Delaware LP as holding company

4. JULIO'S ROLE THROUGHOUT
- CEO/Chairman structure at each phase
- Bank President vs CEO distinction (regulatory preference)
- How Julio stays as public-facing CEO during charter transition
- Board composition requirements

5. CAPITAL REQUIREMENTS SUMMARY
- To launch BaaS: $___
- To apply for ILC charter: $___
- To fund credit union: $___
- To fund state commercial bank: $___
- How dealer partner equity ($10M) funds the banking strategy

6. FDIC/NCUA/OCC REGULATORY REQUIREMENTS
- Application process overview
- Timeline milestones
- Key regulatory contacts in California

Be specific with dollar amounts and timelines. This is for investor and regulatory review.`,
  },
  {
    id: "faq_dealer",
    name: "FAQ & Benefits Agent",
    icon: "❓",
    color: "#1de9b6",
    role: "DEALER EDUCATION & COMMUNICATION SPECIALIST",
    task: "Write the complete dealer FAQ covering internal money flow, equity benefits, BaaS advantages, FDIC coverage, V2G income, and every objection a dealer will raise in a sales meeting.",
    systemPrompt: `You are the CDLS Dealer Education & FAQ Agent. Write a comprehensive FAQ document that answers every question a dealer would ask during a sales meeting about the CDLS BaaS + logistics founding partner program.

CONTEXT: CDLS is a dealer-owned cooperative combining ZEV logistics (Tesla Semi trucks, aluminum trailers, 9 vehicles/load vs 6-7 industry standard), Banking-as-a-Service (floor plan financing, dealer checking/savings), V2G energy banking ($18K-$45K/truck/year), LCFS carbon credits ($24.68/haul), and blockchain tokenization ($CDLS governance, $HAUL utility, $CARBON credits). Founding partners invest $150K-$500K for 3-10% equity.

Create 30+ FAQ questions and answers organized in these categories:

CATEGORY 1: INTERNAL MONEY FLOW
- How does my money stay in the network vs. going to a bank/broker?
- Am I earning from other dealers' activity?
- What happens to floor plan interest I pay?
- How does the cash flow timing work (transport vs. sale timing)?
- How do V2G deposits and LCFS credits flow into my account?

CATEGORY 2: BAAS vs. TRADITIONAL BANKS  
- Why is CDLS BaaS better than Chase/Ally/BofA for my dealership?
- Can I keep my existing bank?
- What DMS systems integrate with CDLS?
- How fast do I get paid when a vehicle sells?
- What credit score/history do I need?

CATEGORY 3: FLOOR PLAN SPECIFICS
- How does your floor plan work vs. NextGear/Floorplan Xpress?
- What are your rates? How do they compare?
- What vehicles qualify?
- What happens if a vehicle sits longer than curtailment period?
- Can I use CDLS floor plan for auction purchases?

CATEGORY 4: FDIC & ACCOUNT SECURITY
- My balance exceeds $250K — am I protected?
- What is IntraFi and how does it protect me automatically?
- What happens to my money if CDLS fails?
- How is my LP equity separate from my deposit?

CATEGORY 5: EQUITY & RETURNS
- How is my equity stake valued?
- When do I start receiving distributions?
- What's the 5-year projection on my investment?
- What if CDLS grows to 5,000 dealers — what happens to my stake?
- Is my investment secured by physical assets?

CATEGORY 6: LOGISTICS & COMPLIANCE
- How does CDLS master insurance work for my trucks?
- Do I need separate carrier insurance?
- How does ACF compliance work through CDLS?
- What is V2G and how does my truck earn income while parked?
- What are LCFS credits and how do I earn them?

CATEGORY 7: OBJECTIONS & TOUGH QUESTIONS
- This sounds too good to be true — what's the catch?
- What if I need to exit the partnership?
- How is CDLS different from what Cox/Manheim offers?
- What happens when more dealers join — does my share dilute?
- Is CalPERS really involved?

Write in plain, direct dealer language. No jargon. Each answer should be 2-4 sentences. Be honest about risks where relevant.`,
  },
  {
    id: "next_steps",
    name: "Next Steps Agent",
    icon: "📋",
    color: "#ff5252",
    role: "OPERATIONS & EXECUTION SPECIALIST",
    task: "Generate the complete prioritized next steps action plan for signing 10 dealers, launching BaaS, securing master insurance, filing HVIP applications, and hitting the July 1 banking deadline.",
    systemPrompt: `You are the CDLS Operations & Execution Agent. Generate a comprehensive, prioritized next steps action plan for Julio Umanzor and CDLS to sign 10 founding dealer partners, launch BaaS operations, secure master fleet insurance, and hit all critical regulatory deadlines.

CONTEXT: 
- CDLS / California Investment Auto, LP - dealer-owned ZEV logistics + BaaS cooperative
- CEO: Julio Umanzor, Sacramento-based
- Current date: March 2026
- CRITICAL DEADLINES: July 1, 2026 (CA banking compliance/DFPI), September 9, 2026 (HVIP voucher applications open at $330K/truck)
- 20 target dealers identified across Sacramento, San Diego, Inland Empire, Bay Area
- Goal: Sign 10 founding partners, launch BaaS, secure master fleet insurance, file HVIP
- Capital available: CalPERS $5M anchor + dealer equity as it's signed

Generate a detailed action plan with:

1. WEEK 1-2: IMMEDIATE ACTIONS (March 2026)
- Legal: CA banking compliance filing with DFPI (CRITICAL - July 1 deadline)
- Insurance: Engage fleet insurance broker for master policy quote
- BaaS: Initiate conversations with Coastal Community Bank and Column Bank
- Dealer outreach: Send first 10 personalized emails to Priority 1 dealers
- Crypto counsel: Engage for token legal opinion

2. MONTH 1 (March-April 2026): FOUNDATION
- Full action list with owners, deadlines, costs
- Dealer pipeline development (meetings, proposals, closes)
- Insurance policy binding
- DFPI registration filing

3. MONTH 2-3 (April-May 2026): MOMENTUM  
- BaaS platform setup and testing
- First dealer signings and onboarding
- SMUD V2G interconnection application
- CalPERS formal presentation

4. MONTH 4-6 (June-August 2026): SCALE
- All 10 dealers signed
- BaaS operational with real accounts
- Master fleet policy fully bound
- HVIP application prep (September 9 is THE date)

5. SEPTEMBER 9, 2026: HVIP DAY
- Exactly what to do on this date
- Who submits, what documents, timing
- Backup plan

6. PARALLEL TRACKS
- Banking charter application timeline
- Dealer pipeline for dealers 11-20
- Series A capital raise preparation

For each action: Who does it, specific deadline, cost estimate, what happens if delayed.

Also include: How to structure the dealer signing ceremony/event, what documents they sign, and how to onboard them into the BaaS platform on day one.`,
  },
];

const CDLS_CONTEXT = `CDLS (California Dealer Logistics Solutions) / California Investment Auto, LP:
- CEO: Julio Umanzor, 14+ years automotive finance experience, Sacramento CA
- First zero-emission vehicle hauling network in California for automotive dealers
- Tesla Semi trucks with aluminum car haulers (9 vehicles/load vs 6-7 industry standard)
- Vehicle-to-Grid (V2G) energy banking: $18K-$45K/truck/year passive income
- LCFS carbon credits: $24.68/haul passive income
- HVIP vouchers: $330K/Tesla Semi (deadline Sept 9, 2026)
- IRA §45W credits: $40K/truck
- Net truck cost after incentives: $325K vs $720K gross (55% funded by regulation)
- CESAR AI system: 8 specialized agents, local Ollama deployment
- Blockchain tokenomics: $CDLS governance, $HAUL utility, $CARBON credits
- 20 founding dealer partners, $10M equity pool, CalPERS $5M anchor investment
- Target: 5,000 dealers in 3 years via tokenization vs 1,000 in 10 years traditional
- Advanced Clean Fleets regulation: 40% ZEV by 2024, 75% by 2035
- Sacramento pilot: 100-trailer fleet, then statewide
- July 1, 2026: CA banking compliance deadline (DFPI)
- $4.13B projected royalties to California over 10 years`;

export default function CDLSSubagentOrchestrator() {
  const [agentResults, setAgentResults] = useState({});
  const [agentStatus, setAgentStatus] = useState({});
  const [running, setRunning] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [completedCount, setCompletedCount] = useState(0);
  const [masterReport, setMasterReport] = useState("");
  const [buildingMaster, setBuildingMaster] = useState(false);
  const completedRef = useRef(0);

  const runAgent = useCallback(async (agent) => {
    setAgentStatus(prev => ({ ...prev, [agent.id]: "running" }));
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: `${agent.systemPrompt}\n\nCDLS PLATFORM CONTEXT:\n${CDLS_CONTEXT}\n\nDeliver a comprehensive, detailed, professional document. Use clear headers and structure. Be specific with numbers, deadlines, and actionable steps. This is for real business use.`,
          messages: [{ role: "user", content: `Execute your assigned task for CDLS. Deliver the complete document now. Task: ${agent.task}` }],
        }),
      });
      const data = await response.json();
      const text = data.content?.map(b => b.text || "").join("") || "No response received.";
      setAgentResults(prev => ({ ...prev, [agent.id]: text }));
      setAgentStatus(prev => ({ ...prev, [agent.id]: "complete" }));
      completedRef.current += 1;
      setCompletedCount(completedRef.current);
    } catch (err) {
      setAgentResults(prev => ({ ...prev, [agent.id]: `Error: ${err.message}` }));
      setAgentStatus(prev => ({ ...prev, [agent.id]: "error" }));
      completedRef.current += 1;
      setCompletedCount(completedRef.current);
    }
  }, []);

  const runAllAgents = async () => {
    setRunning(true);
    completedRef.current = 0;
    setCompletedCount(0);
    setAgentResults({});
    setMasterReport("");
    const initialStatus = {};
    AGENTS.forEach(a => { initialStatus[a.id] = "queued"; });
    setAgentStatus(initialStatus);
    await Promise.all(AGENTS.map(agent => runAgent(agent)));
    setRunning(false);
  };

  const buildMasterReport = async () => {
    setBuildingMaster(true);
    const summaries = AGENTS.map(a => `=== ${a.name.toUpperCase()} ===\n${(agentResults[a.id] || "").slice(0, 300)}...`).join("\n\n");
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{
            role: "user",
            content: `You are the CESAR Master Orchestrator for CDLS (California Dealer Logistics Solutions). 
            
Seven specialized subagents have completed their work. Synthesize their outputs into a concise Executive Master Summary for Julio Umanzor.

SUBAGENT OUTPUTS (excerpts):
${summaries}

Create a structured Executive Summary with:
1. MISSION STATUS - What's been completed across all 7 agents
2. TOP 5 IMMEDIATE ACTIONS - Most critical things Julio must do THIS WEEK
3. CRITICAL PATH - The sequence of decisions that unlocks everything else
4. RISK FLAGS - Any conflicts or gaps identified across agent outputs
5. FINANCIAL SNAPSHOT - Total capital needed, total potential returns

Keep it tight. This is the CEO morning briefing.`
          }],
        }),
      });
      const data = await response.json();
      setMasterReport(data.content?.map(b => b.text || "").join("") || "");
    } catch (e) {
      setMasterReport("Error building master report: " + e.message);
    }
    setBuildingMaster(false);
  };

  const allComplete = completedCount === AGENTS.length && AGENTS.length > 0;
  const progress = (completedCount / AGENTS.length) * 100;

  const statusColor = (s) => ({ queued: "#4a6080", running: "#f5c842", complete: "#00e676", error: "#ff5252" }[s] || "#4a6080");
  const statusLabel = (s) => ({ queued: "Queued", running: "Running...", complete: "Complete ✓", error: "Error" }[s] || "Ready");

  return (
    <div style={{ background: "#040810", minHeight: "100vh", fontFamily: "'Segoe UI', Arial, sans-serif", color: "#e8f0fe" }}>
      
      {/* HEADER */}
      <div style={{ background: "linear-gradient(135deg, #050d20, #0a1830)", borderBottom: "1px solid #1a2d4a", padding: "16px 24px" }}>
        <div style={{ maxWidth: "1280px", margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px" }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ width: "40px", height: "40px", borderRadius: "10px", background: "#00c8ff22", border: "2px solid #00c8ff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "20px" }}>⚙️</div>
                <div>
                  <div style={{ color: "#00c8ff", fontSize: "18px", fontWeight: 900, letterSpacing: "1px" }}>CESAR MULTI-AGENT ORCHESTRATOR</div>
                  <div style={{ color: "#4a6080", fontSize: "11px" }}>Coordinated Energy & Social Asset Resource System · CDLS / California Investment Auto, LP</div>
                </div>
              </div>
            </div>
            <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
              {[
                [`${AGENTS.length}`, "Agents Deployed", "#00c8ff"],
                [completedCount.toString(), "Completed", "#00e676"],
                [running ? "ACTIVE" : allComplete ? "DONE" : "READY", "Status", running ? "#f5c842" : allComplete ? "#00e676" : "#4a6080"],
              ].map(([v, l, c]) => (
                <div key={l} style={{ background: c + "15", border: `1px solid ${c}44`, borderRadius: "8px", padding: "8px 14px", textAlign: "center" }}>
                  <div style={{ color: c, fontSize: "18px", fontWeight: 800 }}>{v}</div>
                  <div style={{ color: "#4a6080", fontSize: "9px" }}>{l}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Progress bar */}
          {(running || allComplete) && (
            <div style={{ marginTop: "14px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <span style={{ color: "#4a6080", fontSize: "10px" }}>OVERALL PROGRESS</span>
                <span style={{ color: "#00c8ff", fontSize: "10px", fontWeight: 700 }}>{Math.round(progress)}%</span>
              </div>
              <div style={{ height: "6px", background: "#0a1525", borderRadius: "3px", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${progress}%`, background: "linear-gradient(90deg, #00c8ff, #00e676)", borderRadius: "3px", transition: "width 0.5s ease" }} />
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "20px" }}>

        {/* LAUNCH BUTTON */}
        {!running && !allComplete && (
          <div style={{ background: "linear-gradient(135deg, #050d20, #0a1a30)", border: "1px solid #1a2d4a", borderRadius: "14px", padding: "36px", textAlign: "center", marginBottom: "24px" }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>🚀</div>
            <div style={{ color: "#00c8ff", fontSize: "22px", fontWeight: 800, marginBottom: "8px" }}>Launch All 7 Subagents in Parallel</div>
            <div style={{ color: "#4a6080", fontSize: "13px", maxWidth: "560px", margin: "0 auto 28px", lineHeight: 1.7 }}>
              All agents run simultaneously using Claude Sonnet. Each produces a complete, specialized document for the CDLS dealer program. Results appear as agents complete.
            </div>
            <div style={{ display: "flex", gap: "10px", justifyContent: "center", flexWrap: "wrap", marginBottom: "28px" }}>
              {AGENTS.map(a => (
                <div key={a.id} style={{ display: "flex", alignItems: "center", gap: "6px", background: a.color + "15", border: `1px solid ${a.color}33`, borderRadius: "20px", padding: "5px 12px" }}>
                  <span>{a.icon}</span>
                  <span style={{ color: a.color, fontSize: "10px", fontWeight: 600 }}>{a.name}</span>
                </div>
              ))}
            </div>
            <button onClick={runAllAgents}
              style={{ background: "linear-gradient(135deg, #00c8ff, #0080b3)", border: "none", borderRadius: "10px", padding: "16px 48px", color: "white", fontSize: "15px", fontWeight: 800, cursor: "pointer", letterSpacing: "1px" }}>
              ⚡ DEPLOY ALL AGENTS
            </button>
          </div>
        )}

        {/* AGENT GRID */}
        {(running || allComplete) && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))", gap: "14px", marginBottom: "24px" }}>
            {AGENTS.map(agent => {
              const status = agentStatus[agent.id] || "queued";
              const result = agentResults[agent.id] || "";
              const isSelected = selectedAgent === agent.id;
              return (
                <div key={agent.id}
                  style={{ background: "#070d1a", border: `1px solid ${status === "complete" ? agent.color + "55" : status === "running" ? agent.color + "88" : "#1a2d4a"}`, borderRadius: "12px", overflow: "hidden", transition: "all 0.3s" }}>
                  {/* Agent header */}
                  <div style={{ padding: "14px 16px", background: status === "running" ? agent.color + "12" : "transparent", borderBottom: "1px solid #1a2d4a" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                      <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                        <div style={{ width: "36px", height: "36px", borderRadius: "8px", background: agent.color + "22", border: `1px solid ${agent.color}44`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18px" }}>
                          {status === "running" ? "⏳" : agent.icon}
                        </div>
                        <div>
                          <div style={{ color: agent.color, fontSize: "12px", fontWeight: 700 }}>{agent.name}</div>
                          <div style={{ color: "#4a6080", fontSize: "9px", letterSpacing: "0.5px" }}>{agent.role}</div>
                        </div>
                      </div>
                      <div style={{ background: statusColor(status) + "22", color: statusColor(status), padding: "3px 10px", borderRadius: "10px", fontSize: "9px", fontWeight: 700 }}>
                        {status === "running" && <span style={{ animation: "pulse 1s infinite" }}>●</span>} {statusLabel(status)}
                      </div>
                    </div>
                  </div>

                  {/* Task preview */}
                  <div style={{ padding: "10px 16px", borderBottom: "1px solid #0a1525" }}>
                    <div style={{ color: "#4a6080", fontSize: "10px", lineHeight: 1.5 }}>{agent.task.slice(0, 120)}...</div>
                  </div>

                  {/* Result preview */}
                  {result && (
                    <div style={{ padding: "10px 16px" }}>
                      <div style={{ color: "#8ca0bc", fontSize: "10px", lineHeight: 1.6, maxHeight: "80px", overflow: "hidden" }}>
                        {result.slice(0, 200)}...
                      </div>
                      <button onClick={() => setSelectedAgent(isSelected ? null : agent.id)}
                        style={{ marginTop: "8px", background: agent.color + "22", border: `1px solid ${agent.color}44`, borderRadius: "6px", padding: "5px 12px", color: agent.color, fontSize: "10px", cursor: "pointer", fontWeight: 600 }}>
                        {isSelected ? "▲ Collapse" : "▼ Read Full Output"}
                      </button>
                    </div>
                  )}

                  {/* Full result expanded */}
                  {isSelected && result && (
                    <div style={{ padding: "12px 16px", borderTop: "1px solid #1a2d4a", background: "#050a15", maxHeight: "500px", overflowY: "auto" }}>
                      <pre style={{ color: "#c0d0e8", fontSize: "11px", lineHeight: 1.7, whiteSpace: "pre-wrap", fontFamily: "inherit", margin: 0 }}>{result}</pre>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* MASTER REPORT */}
        {allComplete && (
          <div style={{ background: "#070d1a", border: "2px solid #00c8ff", borderRadius: "14px", overflow: "hidden", marginBottom: "20px" }}>
            <div style={{ background: "#050d20", padding: "16px 20px", borderBottom: "1px solid #1a2d4a", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ color: "#00c8ff", fontSize: "16px", fontWeight: 800 }}>⚙️ CESAR MASTER SYNTHESIS REPORT</div>
                <div style={{ color: "#4a6080", fontSize: "10px", marginTop: "2px" }}>Executive summary compiled from all 7 agent outputs — for Julio Umanzor</div>
              </div>
              {!masterReport && (
                <button onClick={buildMasterReport} disabled={buildingMaster}
                  style={{ background: buildingMaster ? "#1a2d4a" : "linear-gradient(135deg, #00c8ff, #0080b3)", border: "none", borderRadius: "8px", padding: "10px 20px", color: "white", fontSize: "12px", fontWeight: 700, cursor: buildingMaster ? "default" : "pointer" }}>
                  {buildingMaster ? "⏳ Building..." : "⚡ Generate Master Report"}
                </button>
              )}
            </div>
            {masterReport && (
              <div style={{ padding: "20px", maxHeight: "600px", overflowY: "auto" }}>
                <pre style={{ color: "#c0d0e8", fontSize: "12px", lineHeight: 1.8, whiteSpace: "pre-wrap", fontFamily: "inherit", margin: 0 }}>{masterReport}</pre>
              </div>
            )}
            {!masterReport && !buildingMaster && (
              <div style={{ padding: "30px", textAlign: "center", color: "#4a6080", fontSize: "12px" }}>
                All {AGENTS.length} agents complete. Click "Generate Master Report" for the executive synthesis.
              </div>
            )}
          </div>
        )}

        {/* Reset */}
        {allComplete && (
          <div style={{ textAlign: "center", paddingBottom: "20px" }}>
            <button onClick={() => { setAgentResults({}); setAgentStatus({}); setCompletedCount(0); setRunning(false); setSelectedAgent(null); setMasterReport(""); completedRef.current = 0; }}
              style={{ background: "#0a1525", border: "1px solid #1a2d4a", borderRadius: "8px", padding: "10px 24px", color: "#4a6080", fontSize: "11px", cursor: "pointer" }}>
              ↺ Reset & Run Again
            </button>
          </div>
        )}

        {/* Footer */}
        <div style={{ borderTop: "1px solid #0a1525", paddingTop: "16px", textAlign: "center" }}>
          <div style={{ color: "#1a2d4a", fontSize: "10px" }}>CESAR Multi-Agent System · CDLS / California Investment Auto, LP · Julio Umanzor, CEO & Managing Partner · March 2026 · CONFIDENTIAL</div>
        </div>
      </div>
    </div>
  );
}