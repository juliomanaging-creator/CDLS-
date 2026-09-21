import { useState, useEffect, useRef } from "react";

const CDLS_DOMAINS = {
  regulatory: {
    name: "Regulatory & Compliance",
    emoji: "⚖️",
    color: "#E8C547",
    knowledge: `CARB ACF: 40% ZEV by 2024, 75% by 2035, 100% by 2040. $180K/truck compliance cost without CDLS.
HVIP: Up to $330,000/truck voucher. Deadline: September 9, 2026.
IRA 45W: $40,000 commercial clean vehicle credit. Section 30C: $100,000 EVSE credit.
LCFS: $18,000-$45,000/truck/year via V2G credits. Credit price $70-$120/ton CO2e.
Incentive stacking: Gross $720K → Net $325K per truck (54.9% reduction).
California Competes Tax Credit: Targeting $1.22M over 5 years.
Employment Tax Credits: Up to $125,000 per qualified employee (WOTC, CA New Employment Credit).
CDLS achieves 100% CARB compliance automation via AI Compliance Monitoring Agent.`,
    question: "What are the most critical compliance deadlines CDLS must hit in 2026 and what is the exact incentive stacking strategy per truck?"
  },
  financial: {
    name: "Financial & Investment",
    emoji: "💰",
    color: "#4CAF82",
    knowledge: `IRR: 18-24% projected. ROIC Year 3: 25-35% (vs 12-18% traditional logistics).
Capital structure: 20 founding dealers × $500K = $10M equity. CalPERS: $5M. Total: $15M.
Per-truck revenue: Hauling $120-160K + V2G $18-45K + Carbon $8-22K + Platform $12-18K = $158-245K annually.
Dealer LTV: $12,347. LTV/CAC: 8.2x. 42% referral rate (pilot finding).
Token economics: $CDLS governance, $HAUL utility (deflationary burn), $CARBON (ERC-721 NFT).
Tokenization accelerates: 1,000 dealers/10 years → 5,000 dealers/3 years.
Enterprise value: Sacramento pilot $50M → CA scale $2.5B → National $10B+.
CalPERS alignment: ESG mandate, Emerging Manager Program, infrastructure-like returns.`,
    question: "What is the detailed per-truck P&L model and how does the tokenization strategy accelerate dealer adoption to hit $10B+ platform value?"
  },
  technology: {
    name: "Technology & AI Systems",
    emoji: "🤖",
    color: "#5B8DEF",
    knowledge: `CESAR controller: 7 AI sub-agents, 99.95% dispatch reliability, <2s inference.
5 core agents: Dealer Onboarding, Route Optimization, Compliance Monitoring, Carbon Credit Calculation, Financial Analytics.
Local Ollama (llama3.2:3b): $0/token vs $0.015/1K cloud = $149,500/year saved.
Stack: Node.js/Express + React + PostgreSQL/TimescaleDB + ChromaDB + Docker/K8s on AWS.
QIE (Quantitative Intelligence Engine): Forex trading methods applied to CAISO energy arbitrage.
Blockchain: Solidity/Hardhat, OpenZeppelin ERC-20/ERC-721, Layer 2 gas optimization.
Route optimization: Monte Carlo simulation, 97.3% accuracy achieved in pilot.
LangChain for agent orchestration. MCMC risk analysis. Real-time CAISO API integration.`,
    question: "How does the CESAR controller coordinate all 7 AI agents and how does the QIE apply forex trading methodologies to maximize V2G revenue?"
  },
  energy: {
    name: "Energy & V2G",
    emoji: "⚡",
    color: "#FF7043",
    knowledge: `V2G revenue: $18,000-$45,000/truck/year. Trucks idle 4-9 PM = peak grid demand alignment.
SMUD anchor partner. Target: PG&E, SCE, SDG&E statewide expansion.
CAISO real-time pricing integration → CESAR autonomous dispatch.
LCFS credits auto-calculated per haul via Carbon Credit Agent.
EnergIIZE EVSE incentive + SGIP battery storage rebates.
Portable battery pod systems for flexible V2G beyond fixed depots.
$CARBON NFT minted automatically on haul completion.
S.A.L.S.A. nonprofit: CC4A grant access via GRID Alternatives. Community energy programs.
California High-Speed Rail Authority: Energy infrastructure co-development opportunity.`,
    question: "How does the V2G revenue model work hour-by-hour with CAISO integration and what is the complete LCFS credit generation and monetization flow?"
  },
  market: {
    name: "Market & Dealer Network",
    emoji: "🏪",
    color: "#AB47BC",
    knowledge: `TAM: 5,000 CA dealers, $900M total capital requirement.
Phase 1: Sacramento pilot (100 trailers, 20 dealers). Phase 4: National (300,000 units, $2.5B EV).
CNCDA partnership: Access to 1,200+ CA dealer network.
Founding cohort: 14.2 hauls/dealer/month, 42% referral rate, 100% CARB compliance.
Dealer tiers: A (100+ units/month), B (30-100), C (<30). All benefit from zero-capital model.
Competitive moat: 9 vehicles vs industry 6-7 (+28% capacity), only zero-capital + compliance + energy bundle.
LTV: $12,347, LTV/CAC: 8.2x. Driver earnings: $75K-$95K (25-35% premium).
National Resilience & Dignity Initiative: GlobalStake (Dr. Jordan Knecht), UC system validation.`,
    question: "What is the complete competitive moat analysis and how does the 42% referral rate signal reshape the dealer acquisition strategy?"
  },
  operations: {
    name: "Operations & Field",
    emoji: "🚛",
    color: "#26C6DA",
    knowledge: `48-hour dealer onboarding: Digital app → compliance verify → route baseline → first haul scheduled.
Payload: 9 vehicles/haul (vs 6-7 industry), GVWR 82,000 lbs Tesla Semi + aluminum trailer.
Driver retention: 85-90% (vs 65-75% industry). Satisfaction: 80-88%.
Smart contract: Revenue distributed within 24h of haul completion. $CARBON minted automatically.
Field operations portal: HVIP grant filing automation, compliance certificates, revenue dashboard.
Compliance automation: Real-time CARB docs, FMCSA HOS monitoring, ELD integration, CSA tracking.
S.A.L.S.A.: Community benefit programs, CC4A grants, GRID Alternatives coordination.
Revenue per haul distribution: Dealer share + driver payment + $HAUL rewards + $CARBON mint.`,
    question: "Walk through the complete automated revenue distribution flow from haul completion through smart contract execution and what field operations improvements would increase hauls per dealer per month from 14.2 to 20+?"
  }
};

const IMPROVEMENTS_PROMPT = `You are the Chief Intelligence Officer for CDLS (California Dealer Logistics Solutions / California Investment Auto LP).

Six specialized subagents just analyzed their domains in parallel. Based on all their findings:

## TOP 10 PLATFORM IMPROVEMENTS (Priority Ranked)
For each: what it is, CDLS-specific implementation, projected impact on IRR/dealer growth.

## ⚡ QUICK WINS (Under 30 days)
3-5 specific items deployable immediately.

## 🔗 CROSS-DOMAIN SYNERGIES  
2-3 ways the 6 domains can better integrate to create compounding value.

## 🎯 NEXT 90 DAYS ROADMAP
Sprint plan for CDLS platform development.

Be specific — use actual CDLS numbers ($325K net truck cost, 14.2 hauls/month, 18-24% IRR, etc.).`;

export default function CDLSKnowledgeBase() {
  const [agents, setAgents] = useState({});
  const [synthesis, setSynthesis] = useState("");
  const [running, setRunning] = useState(false);
  const [phase, setPhase] = useState("idle"); // idle | running | synthesizing | complete
  const [startTime, setStartTime] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState("");
  const [querying, setQuerying] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const timerRef = useRef(null);
  const synthRef = useRef(null);

  useEffect(() => {
    if (running) {
      timerRef.current = setInterval(() => {
        setElapsed(prev => prev + 0.1);
      }, 100);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [running]);

  useEffect(() => {
    if (phase === "complete" && synthRef.current) {
      synthRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [phase]);

  const callAPI = async (systemPrompt, userMessage, streaming = false) => {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 1000,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }]
      })
    });
    const data = await res.json();
    return data.content?.[0]?.text || "";
  };

  const runSubagent = async (key, domain) => {
    const result = { status: "running", analysis: "", startTime: Date.now() };
    setAgents(prev => ({ ...prev, [key]: result }));

    try {
      const text = await callAPI(
        `You are the ${domain.name} Agent for CDLS (California Investment Auto LP / California Dealer Logistics Solutions).
Analyze the knowledge base and provide:
1. TOP 3 INSIGHTS from this domain
2. TOP 2 GAPS or risks
3. TOP 3 SPECIFIC IMPROVEMENTS (with CDLS numbers)
Be concise and specific.`,
        `CDLS ${domain.name} Knowledge Base:\n${domain.knowledge}\n\nPriority Question: ${domain.question}`
      );

      setAgents(prev => ({
        ...prev,
        [key]: {
          status: "complete",
          analysis: text,
          elapsed: ((Date.now() - result.startTime) / 1000).toFixed(1)
        }
      }));
    } catch (err) {
      setAgents(prev => ({
        ...prev,
        [key]: { status: "error", analysis: `Error: ${err.message}`, elapsed: 0 }
      }));
    }
  };

  const runSynthesis = async (agentResults) => {
    setPhase("synthesizing");
    const combined = Object.entries(CDLS_DOMAINS).map(([key, d]) => {
      const r = agentResults[key];
      return `=== ${d.emoji} ${d.name} ===\n${r?.analysis || "No data"}`;
    }).join("\n\n");

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 2000,
          system: IMPROVEMENTS_PROMPT,
          messages: [{ role: "user", content: `Subagent findings:\n\n${combined}` }]
        })
      });
      const data = await res.json();
      setSynthesis(data.content?.[0]?.text || "");
    } catch (err) {
      setSynthesis(`Synthesis error: ${err.message}`);
    }
  };

  const handleRun = async () => {
    setRunning(true);
    setPhase("running");
    setElapsed(0);
    setStartTime(Date.now());
    setAgents({});
    setSynthesis("");
    setActiveTab("agents");

    // Run ALL 6 subagents in parallel
    const keys = Object.keys(CDLS_DOMAINS);
    const promises = keys.map(key => runSubagent(key, CDLS_DOMAINS[key]));
    
    // Wait for all to complete
    await Promise.all(promises);
    
    setRunning(false);

    // Collect final results
    const finalResults = {};
    for (const key of keys) {
      // Small delay to ensure state is settled
      await new Promise(r => setTimeout(r, 100));
    }
    
    // Get current agent state for synthesis
    setAgents(prev => {
      runSynthesis(prev).then(() => setPhase("complete"));
      return prev;
    });
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    setQuerying(true);
    setQueryResult("");

    const context = Object.entries(CDLS_DOMAINS).map(([, d]) => 
      `${d.name}:\n${d.knowledge}`
    ).join("\n\n");

    const text = await callAPI(
      `You are the CDLS Knowledge Base AI for California Investment Auto LP. Answer questions about CDLS using specific numbers and details. Be comprehensive and actionable.`,
      `CDLS Knowledge:\n${context}\n\nQuestion: ${query}`
    );
    setQueryResult(text);
    setQuerying(false);
  };

  const getStatusColor = (status) => {
    if (status === "running") return "#E8C547";
    if (status === "complete") return "#4CAF82";
    if (status === "error") return "#EF5350";
    return "#3a3a4a";
  };

  const completedCount = Object.values(agents).filter(a => a.status === "complete").length;
  const totalAgents = Object.keys(CDLS_DOMAINS).length;

  return (
    <div style={{
      fontFamily: "'IBM Plex Mono', 'Courier New', monospace",
      background: "#0a0a0f",
      color: "#e0e0e0",
      minHeight: "100vh",
      padding: "0"
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0d1117 0%, #1a1a2e 100%)",
        borderBottom: "1px solid #E8C547",
        padding: "20px 28px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{
              background: "#E8C547",
              color: "#0a0a0f",
              padding: "4px 10px",
              fontSize: 10,
              fontWeight: 700,
              letterSpacing: 2
            }}>CDLS</div>
            <span style={{ color: "#E8C547", fontSize: 11, letterSpacing: 1 }}>CALIFORNIA INVESTMENT AUTO LP</span>
          </div>
          <div style={{ fontSize: 18, fontWeight: 700, marginTop: 4, letterSpacing: -0.5 }}>
            Multi-Agent Knowledge Base
          </div>
          <div style={{ fontSize: 11, color: "#666", marginTop: 2 }}>
            6 Parallel Domain Subagents · Real-Time Synthesis
          </div>
        </div>
        <button
          onClick={handleRun}
          disabled={running || phase === "synthesizing"}
          style={{
            background: running || phase === "synthesizing" ? "#1a1a2e" : "#E8C547",
            color: running || phase === "synthesizing" ? "#E8C547" : "#0a0a0f",
            border: `1px solid ${running || phase === "synthesizing" ? "#E8C547" : "#E8C547"}`,
            padding: "12px 24px",
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: 1,
            cursor: running || phase === "synthesizing" ? "not-allowed" : "pointer",
            transition: "all 0.2s"
          }}
        >
          {phase === "idle" ? "▶ RUN ALL AGENTS" :
           phase === "running" ? `⟳ RUNNING... (${elapsed.toFixed(1)}s)` :
           phase === "synthesizing" ? "⟳ SYNTHESIZING..." :
           "↺ RE-RUN AGENTS"}
        </button>
      </div>

      {/* Progress Bar */}
      {phase !== "idle" && (
        <div style={{ background: "#0d1117", padding: "8px 28px", borderBottom: "1px solid #1e1e2e" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4, fontSize: 10, color: "#666" }}>
            <span>AGENT PROGRESS</span>
            <span>{completedCount}/{totalAgents} COMPLETE · {elapsed.toFixed(1)}s</span>
          </div>
          <div style={{ background: "#1a1a2e", height: 3, borderRadius: 2 }}>
            <div style={{
              background: "linear-gradient(90deg, #E8C547, #4CAF82)",
              height: "100%",
              width: `${(completedCount / totalAgents) * 100}%`,
              borderRadius: 2,
              transition: "width 0.5s ease"
            }} />
          </div>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid #1e1e2e", background: "#0d1117" }}>
        {[
          { key: "dashboard", label: "DASHBOARD" },
          { key: "agents", label: `AGENTS (${completedCount}/${totalAgents})` },
          { key: "synthesis", label: "SYNTHESIS" },
          { key: "query", label: "QUERY KB" }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              background: "none",
              border: "none",
              borderBottom: activeTab === tab.key ? "2px solid #E8C547" : "2px solid transparent",
              color: activeTab === tab.key ? "#E8C547" : "#555",
              padding: "12px 20px",
              fontSize: 10,
              fontWeight: 700,
              letterSpacing: 1.5,
              cursor: "pointer"
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div style={{ padding: "24px 28px", maxWidth: 1200, margin: "0 auto" }}>

        {/* DASHBOARD TAB */}
        {activeTab === "dashboard" && (
          <div>
            <div style={{ marginBottom: 24, color: "#666", fontSize: 11, lineHeight: 1.8 }}>
              The CDLS Knowledge Base runs <strong style={{ color: "#E8C547" }}>6 specialized subagents in parallel</strong> — 
              each owning a domain of California Investment Auto LP / CDLS platform knowledge. 
              Click <strong style={{ color: "#E8C547" }}>▶ RUN ALL AGENTS</strong> to launch them simultaneously.
            </div>

            {/* Domain Cards Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
              {Object.entries(CDLS_DOMAINS).map(([key, domain]) => {
                const agent = agents[key];
                return (
                  <div key={key} style={{
                    background: "#0d1117",
                    border: `1px solid ${agent ? getStatusColor(agent.status) : "#1e1e2e"}`,
                    padding: 20,
                    transition: "border-color 0.3s",
                    position: "relative",
                    overflow: "hidden"
                  }}>
                    <div style={{
                      position: "absolute", top: 0, left: 0, right: 0, height: 2,
                      background: domain.color, opacity: 0.6
                    }} />
                    <div style={{ fontSize: 24, marginBottom: 8 }}>{domain.emoji}</div>
                    <div style={{ fontSize: 12, fontWeight: 700, color: domain.color, marginBottom: 4 }}>
                      {domain.name}
                    </div>
                    <div style={{ fontSize: 10, color: "#444", lineHeight: 1.6 }}>
                      {domain.knowledge.split("\n")[0]}
                    </div>
                    {agent && (
                      <div style={{
                        marginTop: 12, fontSize: 10, fontWeight: 700,
                        color: getStatusColor(agent.status),
                        letterSpacing: 1
                      }}>
                        {agent.status === "running" ? "⟳ ANALYZING..." :
                         agent.status === "complete" ? `✓ DONE ${agent.elapsed}s` :
                         agent.status === "error" ? "✗ ERROR" : ""}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Stats Row */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginTop: 20 }}>
              {[
                { label: "FOUNDING DEALERS", value: "20", sub: "$500K each" },
                { label: "PROJECTED IRR", value: "18-24%", sub: "CalPERS target" },
                { label: "NET TRUCK COST", value: "$325K", sub: "vs $720K gross" },
                { label: "V2G/TRUCK/YR", value: "$45K", sub: "peak revenue" }
              ].map(stat => (
                <div key={stat.label} style={{
                  background: "#0d1117",
                  border: "1px solid #1e1e2e",
                  padding: "16px 20px"
                }}>
                  <div style={{ fontSize: 10, color: "#555", letterSpacing: 1, marginBottom: 4 }}>{stat.label}</div>
                  <div style={{ fontSize: 22, fontWeight: 700, color: "#E8C547" }}>{stat.value}</div>
                  <div style={{ fontSize: 10, color: "#444", marginTop: 2 }}>{stat.sub}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AGENTS TAB */}
        {activeTab === "agents" && (
          <div>
            {Object.keys(CDLS_DOMAINS).length === 0 || Object.keys(agents).length === 0 ? (
              <div style={{ textAlign: "center", color: "#444", padding: 60, fontSize: 13 }}>
                Run the agents to see domain analyses here
              </div>
            ) : (
              Object.entries(CDLS_DOMAINS).map(([key, domain]) => {
                const agent = agents[key];
                return (
                  <div key={key} style={{
                    background: "#0d1117",
                    border: `1px solid ${agent ? getStatusColor(agent.status) : "#1e1e2e"}`,
                    marginBottom: 16,
                    overflow: "hidden"
                  }}>
                    <div style={{
                      background: "#0d1117",
                      borderBottom: `1px solid #1e1e2e`,
                      padding: "12px 16px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between"
                    }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <span style={{ fontSize: 18 }}>{domain.emoji}</span>
                        <span style={{ fontSize: 12, fontWeight: 700, color: domain.color }}>{domain.name.toUpperCase()}</span>
                      </div>
                      {agent && (
                        <span style={{
                          fontSize: 10, fontWeight: 700,
                          color: getStatusColor(agent.status),
                          letterSpacing: 1
                        }}>
                          {agent.status === "running" ? "⟳ RUNNING" :
                           agent.status === "complete" ? `✓ ${agent.elapsed}s` :
                           "✗ ERROR"}
                        </span>
                      )}
                    </div>
                    {agent?.status === "running" && (
                      <div style={{ padding: 20, color: "#E8C547", fontSize: 11, animation: "pulse 1s infinite" }}>
                        Analyzing {domain.name} knowledge base...
                      </div>
                    )}
                    {agent?.status === "complete" && (
                      <div style={{ padding: 20, fontSize: 12, lineHeight: 1.8, color: "#ccc", whiteSpace: "pre-wrap" }}>
                        {agent.analysis}
                      </div>
                    )}
                    {agent?.status === "error" && (
                      <div style={{ padding: 20, color: "#EF5350", fontSize: 12 }}>{agent.analysis}</div>
                    )}
                    {!agent && (
                      <div style={{ padding: 16, color: "#333", fontSize: 11 }}>Waiting to run...</div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        )}

        {/* SYNTHESIS TAB */}
        {activeTab === "synthesis" && (
          <div ref={synthRef}>
            {!synthesis && phase !== "synthesizing" ? (
              <div style={{ textAlign: "center", color: "#444", padding: 60, fontSize: 13 }}>
                Run all agents first to generate the master synthesis
              </div>
            ) : phase === "synthesizing" ? (
              <div style={{ textAlign: "center", color: "#E8C547", padding: 60, fontSize: 13 }}>
                ⟳ Master Synthesis Agent processing all 6 domain findings...
              </div>
            ) : (
              <div>
                <div style={{
                  background: "#0d1117",
                  border: "1px solid #E8C547",
                  padding: 24,
                  marginBottom: 20
                }}>
                  <div style={{ fontSize: 10, color: "#E8C547", letterSpacing: 2, marginBottom: 16, fontWeight: 700 }}>
                    ◆ CDLS MASTER SYNTHESIS — {new Date().toLocaleDateString()}
                  </div>
                  <div style={{ fontSize: 12, lineHeight: 1.9, color: "#ccc", whiteSpace: "pre-wrap" }}>
                    {synthesis}
                  </div>
                </div>
                <div style={{ fontSize: 10, color: "#444", textAlign: "right" }}>
                  Synthesized from {totalAgents} subagents · Total time: {elapsed.toFixed(1)}s
                </div>
              </div>
            )}
          </div>
        )}

        {/* QUERY TAB */}
        {activeTab === "query" && (
          <div>
            <div style={{ fontSize: 11, color: "#555", marginBottom: 16 }}>
              Query the full CDLS knowledge base with natural language
            </div>
            <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
              <input
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => e.key === "Enter" && !querying && handleQuery()}
                placeholder="e.g. How does HVIP stacking work with the IRA credits?"
                style={{
                  flex: 1,
                  background: "#0d1117",
                  border: "1px solid #2a2a3a",
                  color: "#e0e0e0",
                  padding: "12px 16px",
                  fontSize: 12,
                  fontFamily: "inherit",
                  outline: "none"
                }}
              />
              <button
                onClick={handleQuery}
                disabled={querying || !query.trim()}
                style={{
                  background: querying ? "#1a1a2e" : "#E8C547",
                  color: querying ? "#E8C547" : "#0a0a0f",
                  border: "1px solid #E8C547",
                  padding: "12px 20px",
                  fontSize: 11,
                  fontWeight: 700,
                  cursor: querying ? "not-allowed" : "pointer",
                  letterSpacing: 1,
                  fontFamily: "inherit"
                }}
              >
                {querying ? "⟳" : "ASK"}
              </button>
            </div>

            {/* Quick query chips */}
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24 }}>
              {[
                "What is the incentive stacking breakdown per truck?",
                "How does V2G revenue work during peak hours?",
                "What is the CalPERS investment thesis?",
                "How does CESAR coordinate the AI agents?",
                "What are the top 3 competitive moats?"
              ].map(q => (
                <button
                  key={q}
                  onClick={() => setQuery(q)}
                  style={{
                    background: "none",
                    border: "1px solid #2a2a3a",
                    color: "#555",
                    padding: "6px 12px",
                    fontSize: 10,
                    cursor: "pointer",
                    fontFamily: "inherit",
                    letterSpacing: 0.5
                  }}
                >
                  {q}
                </button>
              ))}
            </div>

            {querying && (
              <div style={{ color: "#E8C547", fontSize: 11, padding: 20 }}>
                ⟳ Querying knowledge base...
              </div>
            )}
            {queryResult && (
              <div style={{
                background: "#0d1117",
                border: "1px solid #4CAF82",
                padding: 24
              }}>
                <div style={{ fontSize: 10, color: "#4CAF82", letterSpacing: 2, marginBottom: 12, fontWeight: 700 }}>
                  ◆ ANSWER
                </div>
                <div style={{ fontSize: 12, lineHeight: 1.9, color: "#ccc", whiteSpace: "pre-wrap" }}>
                  {queryResult}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        * { box-sizing: border-box; }
      `}</style>
    </div>
  );
}
