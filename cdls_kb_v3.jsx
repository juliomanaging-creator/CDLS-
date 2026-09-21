import { useState, useRef } from "react";

const DOMAINS = {
  regulatory: {
    name: "Regulatory & Compliance", emoji: "⚖️", color: "#E8C547",
    prompt: "You are a CDLS regulatory expert. In 3 short paragraphs analyze: (1) Top 3 insights about CDLS HVIP/CARB/IRA incentive stacking strategy ($720K gross → $325K net per truck), (2) Top 2 compliance gaps, (3) Top 3 improvements for 2026."
  },
  financial: {
    name: "Financial & Investment", emoji: "💰", color: "#4CAF82",
    prompt: "You are a CDLS financial expert. In 3 short paragraphs analyze: (1) Top 3 insights about 18-24% IRR model, per-truck revenue $158-245K/yr, CalPERS $5M anchor, (2) Top 2 financial risks, (3) Top 3 improvements to strengthen investor returns."
  },
  technology: {
    name: "Technology & AI Systems", emoji: "🤖", color: "#5B8DEF",
    prompt: "You are a CDLS tech expert. In 3 short paragraphs analyze: (1) Top 3 insights about CESAR controller, 7 AI agents, Ollama local inference saving $149.5K/yr, (2) Top 2 tech gaps, (3) Top 3 system improvements."
  },
  energy: {
    name: "Energy & V2G", emoji: "⚡", color: "#FF7043",
    prompt: "You are a CDLS energy expert. In 3 short paragraphs analyze: (1) Top 3 insights about V2G $18-45K/truck/yr, CAISO integration, LCFS credits, (2) Top 2 energy revenue gaps, (3) Top 3 improvements to maximize grid revenue."
  },
  market: {
    name: "Market & Dealer Network", emoji: "🏪", color: "#AB47BC",
    prompt: "You are a CDLS market expert. In 3 short paragraphs analyze: (1) Top 3 insights about 5,000 CA dealer TAM, 42% referral rate, 9-vehicle moat vs competitor 6-7, (2) Top 2 market risks, (3) Top 3 dealer acquisition improvements."
  },
  operations: {
    name: "Operations & Field", emoji: "🚛", color: "#26C6DA",
    prompt: "You are a CDLS operations expert. In 3 short paragraphs analyze: (1) Top 3 insights about 48-hr onboarding, 14.2 hauls/dealer/month baseline, driver $75-95K pay, (2) Top 2 operational gaps, (3) Top 3 improvements to reach 20+ hauls/dealer/month."
  }
};

// Robust fetch with full debug info
async function fetchClaude(prompt) {
  const url = "https://api.anthropic.com/v1/messages";
  const body = {
    model: "claude-haiku-4-5-20251001",
    max_tokens: 600,
    messages: [{ role: "user", content: prompt }]
  };

  let rawText = "";
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    rawText = await res.text();  // Always get raw text first

    if (!res.ok) {
      return { ok: false, error: `HTTP ${res.status}`, raw: rawText };
    }

    let data;
    try {
      data = JSON.parse(rawText);
    } catch {
      return { ok: false, error: "JSON parse failed", raw: rawText.slice(0, 500) };
    }

    if (data?.content?.[0]?.text) {
      return { ok: true, text: data.content[0].text };
    }
    if (data?.error) {
      return { ok: false, error: data.error.message || data.error.type, raw: rawText.slice(0, 300) };
    }
    return { ok: false, error: "No content field", raw: rawText.slice(0, 400) };

  } catch (e) {
    return { ok: false, error: `Fetch failed: ${e.message}`, raw: rawText.slice(0, 300) };
  }
}

export default function CDLSKBv3() {
  const [agents, setAgents] = useState({});
  const [synthesis, setSynthesis] = useState("");
  const [phase, setPhase] = useState("idle");
  const [elapsed, setElapsed] = useState(0);
  const [debugResult, setDebugResult] = useState(null);
  const [debugLoading, setDebugLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState("");
  const [querying, setQuerying] = useState(false);
  const [tab, setTab] = useState("dashboard");
  const [mode, setMode] = useState("sequential"); // parallel | sequential
  const timerRef = useRef(null);

  const tick = () => { timerRef.current = setInterval(() => setElapsed(e => +(e + 0.1).toFixed(1)), 100); };
  const stopTick = () => clearInterval(timerRef.current);

  // DEBUG: fire one minimal request and show raw response
  const runDebug = async () => {
    setDebugLoading(true);
    setDebugResult(null);
    const result = await fetchClaude("Say hello in one sentence.");
    setDebugResult(result);
    setDebugLoading(false);
  };

  const setAgent = (key, patch) => setAgents(prev => ({ ...prev, [key]: { ...(prev[key] || {}), ...patch } }));

  const runOneAgent = async (key) => {
    const domain = DOMAINS[key];
    setAgent(key, { status: "running", analysis: "", error: "", startMs: Date.now() });
    const result = await fetchClaude(domain.prompt);
    const elapsed = ((Date.now() - Date.now()) / 1000).toFixed(1); // approximate
    if (result.ok) {
      setAgent(key, { status: "complete", analysis: result.text });
    } else {
      setAgent(key, { status: "error", analysis: result.error, raw: result.raw || "" });
    }
    return result;
  };

  const runAllAgents = async () => {
    setPhase("running");
    setElapsed(0);
    setAgents({});
    setSynthesis("");
    setTab("agents");
    tick();

    const keys = Object.keys(DOMAINS);
    let results = {};

    if (mode === "parallel") {
      // All at once
      const promises = keys.map(async (k) => {
        const r = await runOneAgent(k);
        results[k] = r;
      });
      await Promise.all(promises);
    } else {
      // Sequential with small gap — avoids rate limiting
      for (const k of keys) {
        results[k] = await runOneAgent(k);
        await new Promise(r => setTimeout(r, 300));
      }
    }

    stopTick();

    // Build synthesis from successful results
    const goodResults = keys.filter(k => results[k]?.ok);
    if (goodResults.length === 0) {
      setSynthesis("❌ All agents failed — see raw errors in AGENTS tab. Try the DEBUG button first to test API connectivity.");
      setPhase("complete");
      setTab("synthesis");
      return;
    }

    setPhase("synthesizing");

    const combined = goodResults.map(k =>
      `=== ${DOMAINS[k].emoji} ${DOMAINS[k].name} ===\n${results[k].text}`
    ).join("\n\n");

    const synthPrompt = `You are the CDLS Chief Intelligence Officer for California Investment Auto LP. Based on these ${goodResults.length} domain agent reports, give:

TOP 5 PLATFORM IMPROVEMENTS (ranked by impact on IRR/dealer growth, with specific CDLS numbers)
QUICK WINS (under 30 days, actionable)
90-DAY SPRINT ROADMAP

Agent findings:
${combined}`;

    const synthResult = await fetchClaude(synthPrompt);

    if (synthResult.ok) {
      setSynthesis(synthResult.text);
    } else {
      setSynthesis(`Synthesis error: ${synthResult.error}\n\nRaw: ${synthResult.raw || ""}`);
    }

    setPhase("complete");
    setTab("synthesis");
  };

  const handleQuery = async () => {
    if (!query.trim() || querying) return;
    setQuerying(true);
    setQueryResult("");
    const result = await fetchClaude(
      `You are the CDLS Knowledge Base AI for California Investment Auto LP. Answer using specific CDLS numbers and programs.\n\nQuestion: ${query}`
    );
    setQueryResult(result.ok ? result.text : `Error: ${result.error}\n${result.raw || ""}`);
    setQuerying(false);
  };

  const sc = (s) => s === "running" ? "#E8C547" : s === "complete" ? "#4CAF82" : s === "error" ? "#EF5350" : "#2a2a3a";
  const completed = Object.values(agents).filter(a => a.status === "complete").length;
  const errors = Object.values(agents).filter(a => a.status === "error").length;
  const total = Object.keys(DOMAINS).length;

  return (
    <div style={{ fontFamily: "'IBM Plex Mono', 'Courier New', monospace", background: "#09090f", color: "#d0d0d0", minHeight: "100vh" }}>

      {/* Header */}
      <div style={{ background: "#0d1117", borderBottom: "2px solid #E8C547", padding: "16px 20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
              <span style={{ background: "#E8C547", color: "#09090f", fontSize: 9, fontWeight: 800, padding: "2px 7px", letterSpacing: 1 }}>CIA · CDLS</span>
              <span style={{ color: "#444", fontSize: 9 }}>CALIFORNIA INVESTMENT AUTO LP</span>
            </div>
            <div style={{ fontSize: 15, fontWeight: 700 }}>Multi-Agent Knowledge Base v3</div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6, alignItems: "flex-end" }}>
            {/* Mode toggle */}
            <div style={{ display: "flex", gap: 0, border: "1px solid #2a2a3a" }}>
              {["sequential", "parallel"].map(m => (
                <button key={m} onClick={() => setMode(m)}
                  style={{ background: mode === m ? "#2a2a3a" : "none", border: "none", color: mode === m ? "#E8C547" : "#444", padding: "4px 10px", fontSize: 9, fontFamily: "inherit", cursor: "pointer", letterSpacing: 0.5 }}>
                  {m.toUpperCase()}
                </button>
              ))}
            </div>
            <button onClick={runAllAgents} disabled={phase === "running" || phase === "synthesizing"}
              style={{ background: (phase === "running" || phase === "synthesizing") ? "transparent" : "#E8C547", color: (phase === "running" || phase === "synthesizing") ? "#E8C547" : "#09090f", border: "2px solid #E8C547", padding: "8px 16px", fontFamily: "inherit", fontSize: 10, fontWeight: 800, cursor: "pointer" }}>
              {phase === "idle" ? "▶  RUN ALL AGENTS" : phase === "running" ? `⟳  ${elapsed}s  ${completed}/${total}` : phase === "synthesizing" ? "⟳  SYNTHESIZING" : "↺  RE-RUN"}
            </button>
          </div>
        </div>

        {/* Debug bar */}
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #1a1a2a", display: "flex", alignItems: "center", gap: 12 }}>
          <button onClick={runDebug} disabled={debugLoading}
            style={{ background: "none", border: "1px solid #2a2a3a", color: "#555", padding: "5px 12px", fontSize: 9, fontFamily: "inherit", cursor: "pointer", letterSpacing: 1 }}>
            {debugLoading ? "⟳ TESTING..." : "🔍 DEBUG: TEST API"}
          </button>
          {debugResult && (
            <span style={{ fontSize: 9, color: debugResult.ok ? "#4CAF82" : "#EF5350" }}>
              {debugResult.ok
                ? `✓ API OK — "${debugResult.text?.slice(0, 60)}..."`
                : `✗ ${debugResult.error} | Raw: ${(debugResult.raw || "").slice(0, 100)}`}
            </span>
          )}
        </div>
      </div>

      {/* Progress */}
      {phase !== "idle" && (
        <div style={{ background: "#0d1117", padding: "5px 20px", borderBottom: "1px solid #1a1a2a" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "#444", marginBottom: 3 }}>
            <span>{completed} COMPLETE · {errors} ERRORS · {total - completed - errors} PENDING</span>
            <span>{elapsed}s · {mode.toUpperCase()}</span>
          </div>
          <div style={{ background: "#1a1a2a", height: 2 }}>
            <div style={{ background: errors === total ? "#EF5350" : "linear-gradient(90deg,#E8C547,#4CAF82)", height: "100%", width: `${(completed / total) * 100}%`, transition: "width 0.3s" }} />
          </div>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: "flex", background: "#0d1117", borderBottom: "1px solid #1a1a2a" }}>
        {[["dashboard", "DASHBOARD"], ["agents", `AGENTS ${completed}/${total}`], ["synthesis", "SYNTHESIS"], ["query", "QUERY"]].map(([k, l]) => (
          <button key={k} onClick={() => setTab(k)}
            style={{ background: "none", border: "none", borderBottom: `2px solid ${tab === k ? "#E8C547" : "transparent"}`, color: tab === k ? "#E8C547" : "#444", padding: "10px 16px", fontSize: 9, fontWeight: 700, letterSpacing: 1, cursor: "pointer", fontFamily: "inherit" }}>
            {l}
          </button>
        ))}
      </div>

      <div style={{ padding: 20, maxWidth: 900, margin: "0 auto" }}>

        {/* DASHBOARD */}
        {tab === "dashboard" && (
          <div>
            <div style={{ background: "#0d1117", border: "1px solid #1a1a2a", padding: 16, marginBottom: 16, fontSize: 10, lineHeight: 1.8, color: "#555" }}>
              <strong style={{ color: "#E8C547" }}>TROUBLESHOOTING:</strong> If agents show errors, click{" "}
              <strong style={{ color: "#fff" }}>🔍 DEBUG: TEST API</strong> above first. If debug passes ✓, use{" "}
              <strong style={{ color: "#fff" }}>SEQUENTIAL</strong> mode (avoids rate limits from 6 simultaneous calls).
              If debug fails, the API may be unavailable in this session.
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10, marginBottom: 16 }}>
              {Object.entries(DOMAINS).map(([k, d]) => {
                const ag = agents[k];
                return (
                  <div key={k} style={{ background: "#0d1117", border: `1px solid ${ag ? sc(ag.status) : "#1a1a2a"}`, padding: 16 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <span style={{ fontSize: 18 }}>{d.emoji}</span>
                      {ag && <span style={{ fontSize: 9, color: sc(ag.status), fontWeight: 700 }}>
                        {ag.status === "running" ? "⟳" : ag.status === "complete" ? "✓" : "✗"}
                      </span>}
                    </div>
                    <div style={{ fontSize: 10, fontWeight: 700, color: d.color, marginTop: 6 }}>{d.name}</div>
                  </div>
                );
              })}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8 }}>
              {[["IRR", "18-24%", "Target"], ["NET/TRUCK", "$325K", "After incentives"], ["V2G/YR", "$45K", "Per truck peak"], ["LTV/CAC", "8.2x", "Dealer ratio"]].map(([l, v, s]) => (
                <div key={l} style={{ background: "#0d1117", border: "1px solid #1a1a2a", padding: 12 }}>
                  <div style={{ fontSize: 8, color: "#444", letterSpacing: 1 }}>{l}</div>
                  <div style={{ fontSize: 18, fontWeight: 700, color: "#E8C547", margin: "3px 0" }}>{v}</div>
                  <div style={{ fontSize: 8, color: "#333" }}>{s}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AGENTS */}
        {tab === "agents" && (
          <div>
            {Object.keys(agents).length === 0 && (
              <div style={{ color: "#333", textAlign: "center", padding: 50, fontSize: 11 }}>
                Press ▶ RUN ALL AGENTS to start
              </div>
            )}
            {Object.entries(DOMAINS).map(([k, d]) => {
              const ag = agents[k];
              if (!ag) return null;
              return (
                <div key={k} style={{ background: "#0d1117", border: `1px solid ${sc(ag.status)}`, marginBottom: 12 }}>
                  <div style={{ borderBottom: "1px solid #1a1a2a", padding: "9px 14px", display: "flex", justifyContent: "space-between" }}>
                    <span style={{ fontSize: 10, fontWeight: 700, color: d.color }}>{d.emoji} {d.name.toUpperCase()}</span>
                    <span style={{ fontSize: 9, color: sc(ag.status), fontWeight: 700 }}>
                      {ag.status === "running" ? "⟳ RUNNING" : ag.status === "complete" ? "✓ DONE" : "✗ ERROR"}
                    </span>
                  </div>
                  <div style={{ padding: 14, fontSize: 11, lineHeight: 1.8, color: ag.status === "error" ? "#EF5350" : "#bbb", whiteSpace: "pre-wrap" }}>
                    {ag.status === "running"
                      ? <span style={{ color: "#E8C547" }}>⟳ Analyzing...</span>
                      : ag.analysis}
                    {/* Show raw response for errors */}
                    {ag.status === "error" && ag.raw && (
                      <div style={{ marginTop: 10, padding: 10, background: "#0a0a14", border: "1px solid #2a2a3a", fontSize: 9, color: "#555", wordBreak: "break-all" }}>
                        <div style={{ color: "#333", marginBottom: 4 }}>RAW RESPONSE:</div>
                        {ag.raw}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* SYNTHESIS */}
        {tab === "synthesis" && (
          <div>
            {!synthesis && <div style={{ color: "#333", textAlign: "center", padding: 50, fontSize: 11 }}>Run agents to generate synthesis</div>}
            {phase === "synthesizing" && <div style={{ color: "#E8C547", textAlign: "center", padding: 40, fontSize: 11 }}>⟳ Master Synthesis Agent running...</div>}
            {synthesis && (
              <div style={{ background: "#0d1117", border: "1px solid #E8C547", padding: 20 }}>
                <div style={{ fontSize: 9, color: "#E8C547", letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>
                  ◆ CDLS MASTER SYNTHESIS — {new Date().toLocaleString()}
                </div>
                <div style={{ fontSize: 11, lineHeight: 1.9, color: "#ccc", whiteSpace: "pre-wrap" }}>{synthesis}</div>
              </div>
            )}
          </div>
        )}

        {/* QUERY */}
        {tab === "query" && (
          <div>
            <div style={{ fontSize: 9, color: "#444", marginBottom: 10 }}>Ask anything about CDLS / California Investment Auto LP</div>
            <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
              <input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === "Enter" && handleQuery()}
                placeholder="e.g. How does HVIP stacking work?"
                style={{ flex: 1, background: "#0d1117", border: "1px solid #2a2a3a", color: "#e0e0e0", padding: "10px 12px", fontSize: 11, fontFamily: "inherit", outline: "none" }} />
              <button onClick={handleQuery} disabled={querying || !query.trim()}
                style={{ background: querying ? "transparent" : "#E8C547", color: querying ? "#E8C547" : "#09090f", border: "2px solid #E8C547", padding: "10px 16px", fontSize: 10, fontWeight: 800, fontFamily: "inherit", cursor: "pointer" }}>
                {querying ? "⟳" : "ASK"}
              </button>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16 }}>
              {["Incentive stacking per truck?", "V2G peak hour revenue?", "CalPERS investment thesis?", "CESAR agent coordination?", "48-hour onboarding flow?"].map(q => (
                <button key={q} onClick={() => setQuery(q)}
                  style={{ background: "none", border: "1px solid #1a1a2a", color: "#444", padding: "4px 9px", fontSize: 9, cursor: "pointer", fontFamily: "inherit" }}>
                  {q}
                </button>
              ))}
            </div>
            {queryResult && (
              <div style={{ background: "#0d1117", border: "1px solid #4CAF82", padding: 18 }}>
                <div style={{ fontSize: 9, color: "#4CAF82", letterSpacing: 2, fontWeight: 700, marginBottom: 10 }}>◆ ANSWER</div>
                <div style={{ fontSize: 11, lineHeight: 1.85, color: "#ccc", whiteSpace: "pre-wrap" }}>{queryResult}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
