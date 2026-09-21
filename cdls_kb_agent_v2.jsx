import { useState, useEffect, useRef } from "react";

const CDLS_DOMAINS = {
  regulatory: {
    name: "Regulatory & Compliance",
    emoji: "⚖️",
    color: "#E8C547",
    question: "Summarize the CDLS compliance strategy: HVIP ($330K/truck, Sept 9 2026 deadline), incentive stacking ($720K gross → $325K net), CARB ACF milestones (40% ZEV 2024, 75% 2035), and IRA 45W/30C credits. What are the 3 most critical 2026 deadlines and 3 gaps in the current approach?"
  },
  financial: {
    name: "Financial & Investment",
    emoji: "💰",
    color: "#4CAF82",
    question: "Analyze the CDLS financial model: 18-24% IRR, $15M raise (20 dealers × $500K + CalPERS $5M), per-truck revenue $158-245K/yr across hauling/V2G/carbon/platform streams, LTV $12,347 at 8.2x LTV/CAC, tokenization scaling 1K to 5K dealers in 3 years, $10B+ national platform value. What are 3 key insights, 2 risks, and 3 improvements?"
  },
  technology: {
    name: "Technology & AI Systems",
    emoji: "🤖",
    color: "#5B8DEF",
    question: "Analyze the CDLS tech stack: CESAR controller with 7 AI agents (99.95% dispatch reliability), local Ollama llama3.2:3b ($149,500/yr API cost savings), Monte Carlo route optimization (97.3% accuracy), QIE energy arbitrage engine, Node.js/React/PostgreSQL/TimescaleDB/ChromaDB/Docker/K8s, three-token blockchain (ERC-20/ERC-721). What are 3 insights, 2 gaps, and 3 improvements?"
  },
  energy: {
    name: "Energy & V2G",
    emoji: "⚡",
    color: "#FF7043",
    question: "Analyze CDLS V2G strategy: $18K-$45K/truck/year revenue, trucks idle 4-9PM matching peak grid demand, SMUD anchor partner, CAISO real-time pricing integration, LCFS credits auto-calculated per haul, $CARBON NFT minted on completion, portable battery pods, S.A.L.S.A nonprofit for CC4A grants via GRID Alternatives. What are 3 insights, 2 gaps, and 3 improvements?"
  },
  market: {
    name: "Market & Dealer Network",
    emoji: "🏪",
    color: "#AB47BC",
    question: "Analyze CDLS market position: 5,000 CA dealers/$900M TAM, 4-phase GTM (Sacramento pilot → Bay Area/LA → statewide → 300K national), CNCDA access to 1,200+ dealers, 9-vehicle capacity vs competitor 6-7 (+28%), zero-capital + compliance + energy bundle as unique moat, 42% referral rate from founding cohort, LTV/CAC 8.2x. What are 3 insights, 2 gaps, and 3 improvements?"
  },
  operations: {
    name: "Operations & Field",
    emoji: "🚛",
    color: "#26C6DA",
    question: "Analyze CDLS operations: 48-hour dealer onboarding automation, 14.2 hauls/dealer/month baseline, driver pay $75K-$95K (25-35% premium), 85-90% retention vs 65-75% industry, smart contract auto-distribution within 24h of haul, field portal for HVIP grant filing, real-time CARB/FMCSA compliance tracking. What are 3 insights, 2 gaps, and 3 improvements to push hauls/dealer/month from 14.2 to 20+?"
  }
};

async function callClaude(systemPrompt, userMessage, model = "claude-haiku-4-5-20251001") {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model,
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }]
    })
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API ${response.status}: ${errText.slice(0, 200)}`);
  }

  const data = await response.json();

  // Handle all possible response shapes
  if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
  if (data.content && Array.isArray(data.content) && data.content[0]?.text) {
    return data.content[0].text;
  }
  if (typeof data.content === "string") return data.content;
  throw new Error(`Unexpected shape: ${JSON.stringify(data).slice(0, 300)}`);
}

export default function CDLSKnowledgeBase() {
  const [agents, setAgents] = useState({});
  const [synthesis, setSynthesis] = useState("");
  const [phase, setPhase] = useState("idle");
  const [elapsed, setElapsed] = useState(0);
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState("");
  const [querying, setQuerying] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [running, setRunning] = useState(false);
  const timerRef = useRef(null);

  useEffect(() => {
    if (running) {
      timerRef.current = setInterval(() => setElapsed(e => +(e + 0.1).toFixed(1)), 100);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [running]);

  const runSubagent = async (key, domain) => {
    setAgents(prev => ({ ...prev, [key]: { status: "running", analysis: "", startMs: Date.now() } }));
    try {
      const text = await callClaude(
        `You are the ${domain.name} expert agent for CDLS (California Dealer Logistics Solutions / California Investment Auto LP). Provide sharp, specific analysis using real CDLS numbers. Format with clear sections: INSIGHTS, GAPS, IMPROVEMENTS.`,
        domain.question
      );
      setAgents(prev => ({
        ...prev,
        [key]: {
          status: "complete",
          analysis: text,
          elapsed: (( Date.now() - prev[key].startMs) / 1000).toFixed(1)
        }
      }));
      return text;
    } catch (err) {
      const msg = err.message || String(err);
      setAgents(prev => ({ ...prev, [key]: { status: "error", analysis: msg, elapsed: 0 } }));
      return null;
    }
  };

  const handleRun = async () => {
    setRunning(true);
    setPhase("running");
    setElapsed(0);
    setAgents({});
    setSynthesis("");
    setActiveTab("agents");

    // All 6 agents fire in parallel
    const keys = Object.keys(CDLS_DOMAINS);
    const results = await Promise.all(keys.map(k => runSubagent(k, CDLS_DOMAINS[k])));
    setRunning(false);
    setPhase("synthesizing");

    // Collect successful results
    const combined = keys.map((k, i) =>
      results[i] ? `=== ${CDLS_DOMAINS[k].emoji} ${CDLS_DOMAINS[k].name} ===\n${results[i]}` : null
    ).filter(Boolean).join("\n\n");

    if (!combined) {
      setSynthesis("No agent results to synthesize — check errors above.");
      setPhase("complete");
      return;
    }

    try {
      const synthText = await callClaude(
        `You are the Chief Intelligence Officer for CDLS / California Investment Auto LP. Synthesize multi-domain agent findings into a prioritized strategic plan. Use specific CDLS numbers ($325K net truck cost, 14.2 hauls/month baseline, 18-24% IRR, HVIP Sept 2026 deadline, etc.). Be direct and actionable.`,
        `Six parallel subagents analyzed CDLS domains. Synthesize into:\n\n## 🎯 TOP 10 PLATFORM IMPROVEMENTS (ranked by impact on IRR/growth)\n## ⚡ QUICK WINS (deployable <30 days)\n## 🔗 CROSS-DOMAIN SYNERGIES\n## 📅 90-DAY SPRINT ROADMAP\n\nAgent findings:\n\n${combined}`,
        "claude-sonnet-4-20250514"
      );
      setSynthesis(synthText);
    } catch (err) {
      setSynthesis(`Synthesis error: ${err.message}`);
    }
    setPhase("complete");
    setActiveTab("synthesis");
  };

  const handleQuery = async () => {
    if (!query.trim() || querying) return;
    setQuerying(true);
    setQueryResult("");
    try {
      const context = Object.values(CDLS_DOMAINS).map(d => `${d.name}:\n${d.question}`).join("\n\n");
      const ans = await callClaude(
        "You are the CDLS Knowledge Base AI for California Investment Auto LP. Answer questions using specific CDLS numbers, programs, and context. Be comprehensive and actionable.",
        `Context:\n${context}\n\nQuestion: ${query}`
      );
      setQueryResult(ans);
    } catch (err) {
      setQueryResult(`Error: ${err.message}`);
    }
    setQuerying(false);
  };

  const statusColor = s => s === "running" ? "#E8C547" : s === "complete" ? "#4CAF82" : s === "error" ? "#EF5350" : "#2a2a3a";
  const completedCount = Object.values(agents).filter(a => a.status === "complete").length;
  const errorCount = Object.values(agents).filter(a => a.status === "error").length;
  const total = Object.keys(CDLS_DOMAINS).length;

  const QUICK_QUERIES = [
    "What is the exact incentive stacking breakdown per truck?",
    "How does V2G revenue work during peak hours 4-9PM?",
    "What is the CalPERS investment thesis and fit?",
    "How does CESAR coordinate the 7 AI agents?",
    "What are the top 3 competitive moats vs traditional haulers?",
    "Walk through the 48-hour dealer onboarding automation"
  ];

  return (
    <div style={{ fontFamily: "'IBM Plex Mono', monospace", background: "#09090f", color: "#d0d0d0", minHeight: "100vh" }}>

      {/* Header */}
      <div style={{ background: "#0d1117", borderBottom: "2px solid #E8C547", padding: "18px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
            <span style={{ background: "#E8C547", color: "#09090f", fontSize: 9, fontWeight: 800, padding: "3px 8px", letterSpacing: 2 }}>CIA · CDLS</span>
            <span style={{ color: "#555", fontSize: 10, letterSpacing: 1 }}>CALIFORNIA INVESTMENT AUTO LP</span>
          </div>
          <div style={{ fontSize: 16, fontWeight: 700 }}>Multi-Agent Knowledge Base</div>
          <div style={{ fontSize: 10, color: "#444", marginTop: 2 }}>6 Domain Subagents · Parallel Execution · Live Synthesis</div>
        </div>
        <button
          onClick={handleRun}
          disabled={running || phase === "synthesizing"}
          style={{
            background: (running || phase === "synthesizing") ? "transparent" : "#E8C547",
            color: (running || phase === "synthesizing") ? "#E8C547" : "#09090f",
            border: "2px solid #E8C547",
            padding: "10px 22px",
            fontFamily: "inherit",
            fontSize: 11,
            fontWeight: 800,
            letterSpacing: 1,
            cursor: (running || phase === "synthesizing") ? "not-allowed" : "pointer"
          }}
        >
          {phase === "idle" ? "▶  RUN ALL AGENTS"
            : phase === "running" ? `⟳  RUNNING (${elapsed}s)`
            : phase === "synthesizing" ? "⟳  SYNTHESIZING..."
            : "↺  RE-RUN"}
        </button>
      </div>

      {/* Progress */}
      {phase !== "idle" && (
        <div style={{ background: "#0d1117", padding: "6px 24px", borderBottom: "1px solid #1a1a2a" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "#444", marginBottom: 4 }}>
            <span>{phase === "synthesizing" ? "MASTER SYNTHESIS IN PROGRESS" : `${completedCount} COMPLETE · ${errorCount} ERRORS · ${total - completedCount - errorCount} RUNNING`}</span>
            <span>{elapsed}s</span>
          </div>
          <div style={{ background: "#1a1a2a", height: 2 }}>
            <div style={{ background: errorCount > 0 ? "#EF5350" : "linear-gradient(90deg,#E8C547,#4CAF82)", height: "100%", width: `${(completedCount / total) * 100}%`, transition: "width 0.4s" }} />
          </div>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: "flex", background: "#0d1117", borderBottom: "1px solid #1a1a2a" }}>
        {[
          { k: "dashboard", l: "DASHBOARD" },
          { k: "agents", l: `AGENTS  ${completedCount}/${total}` },
          { k: "synthesis", l: "SYNTHESIS" },
          { k: "query", l: "QUERY" }
        ].map(t => (
          <button key={t.k} onClick={() => setActiveTab(t.k)}
            style={{ background: "none", border: "none", borderBottom: `2px solid ${activeTab === t.k ? "#E8C547" : "transparent"}`, color: activeTab === t.k ? "#E8C547" : "#444", padding: "11px 18px", fontSize: 10, fontWeight: 700, letterSpacing: 1.5, cursor: "pointer", fontFamily: "inherit" }}>
            {t.l}
          </button>
        ))}
      </div>

      <div style={{ padding: "24px", maxWidth: 1100, margin: "0 auto" }}>

        {/* DASHBOARD */}
        {activeTab === "dashboard" && (
          <div>
            <div style={{ color: "#444", fontSize: 11, lineHeight: 1.8, marginBottom: 20 }}>
              Press <strong style={{ color: "#E8C547" }}>▶ RUN ALL AGENTS</strong> to fire all 6 domain subagents simultaneously against the CDLS / California Investment Auto knowledge base. Each agent independently analyzes its domain, then the Master Synthesis Agent combines all findings.
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12, marginBottom: 20 }}>
              {Object.entries(CDLS_DOMAINS).map(([key, d]) => {
                const ag = agents[key];
                return (
                  <div key={key} style={{ background: "#0d1117", border: `1px solid ${ag ? statusColor(ag.status) : "#1a1a2a"}`, padding: 18, transition: "border-color 0.3s" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <span style={{ fontSize: 20 }}>{d.emoji}</span>
                        <span style={{ fontSize: 11, fontWeight: 700, color: d.color }}>{d.name}</span>
                      </div>
                      {ag && <span style={{ fontSize: 9, color: statusColor(ag.status), fontWeight: 700, letterSpacing: 1 }}>
                        {ag.status === "running" ? "⟳ RUNNING" : ag.status === "complete" ? `✓ ${ag.elapsed}s` : "✗ ERR"}
                      </span>}
                    </div>
                  </div>
                );
              })}
            </div>
            {/* KPI strip */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
              {[["IRR TARGET", "18–24%", "CalPERS benchmark"], ["NET/TRUCK", "$325K", "vs $720K gross"], ["V2G PEAK", "$45K/yr", "per truck"], ["DEALER LTV", "8.2x", "LTV/CAC ratio"]].map(([l, v, s]) => (
                <div key={l} style={{ background: "#0d1117", border: "1px solid #1a1a2a", padding: "14px 16px" }}>
                  <div style={{ fontSize: 9, color: "#444", letterSpacing: 1 }}>{l}</div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#E8C547", margin: "4px 0" }}>{v}</div>
                  <div style={{ fontSize: 9, color: "#333" }}>{s}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AGENTS */}
        {activeTab === "agents" && (
          <div>
            {Object.keys(agents).length === 0 && (
              <div style={{ color: "#333", textAlign: "center", padding: 60, fontSize: 12 }}>Run agents to see domain analyses</div>
            )}
            {Object.entries(CDLS_DOMAINS).map(([key, d]) => {
              const ag = agents[key];
              if (!ag) return null;
              return (
                <div key={key} style={{ background: "#0d1117", border: `1px solid ${statusColor(ag.status)}`, marginBottom: 14, overflow: "hidden" }}>
                  <div style={{ background: "#0d1117", borderBottom: "1px solid #1a1a2a", padding: "10px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span>{d.emoji}</span>
                      <span style={{ fontSize: 11, fontWeight: 700, color: d.color }}>{d.name.toUpperCase()}</span>
                    </div>
                    <span style={{ fontSize: 9, color: statusColor(ag.status), fontWeight: 700, letterSpacing: 1 }}>
                      {ag.status === "running" ? "⟳ ANALYZING" : ag.status === "complete" ? `✓ DONE  ${ag.elapsed}s` : "✗ ERROR"}
                    </span>
                  </div>
                  <div style={{ padding: "16px", fontSize: 11, lineHeight: 1.85, color: ag.status === "error" ? "#EF5350" : "#ccc", whiteSpace: "pre-wrap" }}>
                    {ag.status === "running" ? <span style={{ color: "#E8C547" }}>⟳ Analyzing {d.name} knowledge base...</span> : ag.analysis}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* SYNTHESIS */}
        {activeTab === "synthesis" && (
          <div>
            {!synthesis && phase !== "synthesizing" && (
              <div style={{ color: "#333", textAlign: "center", padding: 60, fontSize: 12 }}>Run agents first to generate synthesis</div>
            )}
            {phase === "synthesizing" && (
              <div style={{ color: "#E8C547", textAlign: "center", padding: 60, fontSize: 12 }}>⟳ Master Synthesis Agent combining all 6 domain findings...</div>
            )}
            {synthesis && (
              <div style={{ background: "#0d1117", border: "1px solid #E8C547", padding: 24 }}>
                <div style={{ fontSize: 9, color: "#E8C547", letterSpacing: 2, fontWeight: 700, marginBottom: 16 }}>
                  ◆ CDLS MASTER SYNTHESIS — {new Date().toLocaleString()}
                </div>
                <div style={{ fontSize: 12, lineHeight: 1.9, color: "#ccc", whiteSpace: "pre-wrap" }}>{synthesis}</div>
              </div>
            )}
          </div>
        )}

        {/* QUERY */}
        {activeTab === "query" && (
          <div>
            <div style={{ fontSize: 10, color: "#444", marginBottom: 12 }}>Natural language Q&A against the full CDLS knowledge base</div>
            <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
              <input
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleQuery()}
                placeholder="Ask anything about CDLS..."
                style={{ flex: 1, background: "#0d1117", border: "1px solid #2a2a3a", color: "#e0e0e0", padding: "11px 14px", fontSize: 12, fontFamily: "inherit", outline: "none" }}
              />
              <button
                onClick={handleQuery}
                disabled={querying || !query.trim()}
                style={{ background: querying ? "transparent" : "#E8C547", color: querying ? "#E8C547" : "#09090f", border: "2px solid #E8C547", padding: "11px 18px", fontSize: 11, fontWeight: 800, fontFamily: "inherit", cursor: querying ? "not-allowed" : "pointer" }}
              >
                {querying ? "⟳" : "ASK"}
              </button>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 20 }}>
              {QUICK_QUERIES.map(q => (
                <button key={q} onClick={() => setQuery(q)}
                  style={{ background: "none", border: "1px solid #1a1a2a", color: "#444", padding: "5px 10px", fontSize: 9, cursor: "pointer", fontFamily: "inherit", letterSpacing: 0.5 }}>
                  {q}
                </button>
              ))}
            </div>
            {queryResult && (
              <div style={{ background: "#0d1117", border: "1px solid #4CAF82", padding: 20 }}>
                <div style={{ fontSize: 9, color: "#4CAF82", letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>◆ ANSWER</div>
                <div style={{ fontSize: 12, lineHeight: 1.85, color: "#ccc", whiteSpace: "pre-wrap" }}>{queryResult}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
