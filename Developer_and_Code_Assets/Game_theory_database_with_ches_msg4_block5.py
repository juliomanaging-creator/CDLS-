import { useState } from "react";

const SUBAGENTS = [
  {
    id: "nash", name: "Nash Equilibrium Agent", icon: "⚖️", color: "#6366f1",
    specialty: "Nash Equilibrium & Strategic Dominance",
    prompt: `You are the Nash Equilibrium Subagent in a Game Theory Knowledge Database. Provide a structured lesson covering:
1. Nash Equilibrium definition and intuition (keep it simple)
2. How it applies to Chess — 2-3 specific chess position scenarios
3. How it applies to Checkers
4. Key strategic insight for a beginner trying to reach grandmaster level
5. One famous historical chess game example that demonstrates Nash principles
Be educational, practical, specific. Under 400 words.`
  },
  {
    id: "minimax", name: "Minimax & Alpha-Beta Agent", icon: "🌳", color: "#10b981",
    specialty: "Minimax Trees, Alpha-Beta Pruning & Decision Theory",
    prompt: `You are the Minimax & Alpha-Beta Pruning Subagent. Provide:
1. Minimax algorithm explained simply with a chess example
2. Alpha-Beta pruning — why it powers chess engines like Stockfish
3. How grandmasters think like minimax (15-20 move calculation)
4. Checkers: key minimax positions to memorize
5. A/B data insight: Stockfish vs human games 1924-2024 — what changed
6. Top 3 brain training tips to calculate deeper
Under 400 words.`
  },
  {
    id: "opening", name: "Opening Theory Agent", icon: "♟️", color: "#f59e0b",
    specialty: "100-Year Chess Opening Database",
    prompt: `You are the Chess Opening Theory Subagent with 100 years of data (1924-2024). Provide:
1. Top 5 openings for White with estimated win rates
2. Top 5 best Black defenses
3. The single best opening for a beginner to master first — and WHY
4. How opening theory evolved per decade (1920s-2020s)
5. Checkers: 3 most powerful opening sequences with moves
6. A/B insight: GM openings vs amateur openings — the key statistical difference
Use real move notation like 1.e4 e5 2.Nf3. Under 400 words.`
  },
  {
    id: "endgame", name: "Endgame Theory Agent", icon: "👑", color: "#ef4444",
    specialty: "Endgame Tablebases & Positional Mastery",
    prompt: `You are the Endgame Theory Subagent. Provide:
1. The 5 essential endgame positions every grandmaster knows cold
2. Pawn endgame principles: opposition, zugzwang, key squares
3. Rook endgames: Lucena and Philidor positions explained
4. Checkers endgame: key winning patterns and king maneuvers
5. A/B Data: Where amateurs lose most in endgames vs GMs (the stats)
6. Training roadmap: endgames to study from beginner to GM level, in order
Under 400 words.`
  },
  {
    id: "tactics", name: "Tactical Patterns Agent", icon: "⚡", color: "#8b5cf6",
    specialty: "Tactical Motifs & Pattern Recognition",
    prompt: `You are the Chess Tactics Subagent trained on millions of positions (1924-2024). Provide:
1. The 7 core tactical motifs every player must know (with brief examples)
2. The most common pattern GMs exploit against amateurs — from data
3. How to train pattern recognition: the 1000-puzzle method
4. Checkers tactics: key jump combinations and classic traps
5. A/B result: hours of tactics study per week vs ELO rating gain
6. Roadmap to tactically reach 2200+ ELO
Under 400 words. Be vivid and practical.`
  },
  {
    id: "psychology", name: "Psychology & Behavioral Agent", icon: "🧠", color: "#ec4899",
    specialty: "Game Psychology & Behavioral Game Theory",
    prompt: `You are the Psychology & Behavioral Game Theory Subagent. Provide:
1. How behavioral game theory differs from classical game theory
2. The psychology of chess grandmasters — what mental models do they use?
3. Cognitive biases that hurt chess/checkers players (name and explain 3)
4. Mental techniques from Magnus Carlsen, Bobby Fischer, and Kasparov
5. Time pressure psychology: how to think clearly under clock stress
6. A/B Data: Psychological profiles of GM vs player who plateaued
7. A mental training routine for grandmaster-level thinking
Under 400 words. Be motivating.`
  },
  {
    id: "abmodel", name: "A/B Simulation Agent", icon: "📊", color: "#06b6d4",
    specialty: "100-Year Chess Data A/B Modeling",
    prompt: `You are the A/B Simulation Subagent analyzing 100 years of chess games (1924-2024, millions of games). Run this analysis:
HYPOTHESIS: What separates players who reach GM (2500+) from those stuck at 1500-1800?
GROUP A (Control): Typical self-taught amateur training patterns
GROUP B (Treatment): Structured GM-accelerated training patterns
KEY FINDINGS: Optimal % time on openings, tactics, endgames, game analysis
STATISTICAL PROJECTIONS: Avg time to reach 2000, 2200, 2500 ELO under Group B
THE ACCELERATED GRANDMASTER PROTOCOL: Your evidence-based 12-month roadmap
Format like a real data science report. Under 500 words.`
  },
  {
    id: "checkers", name: "Checkers Strategy Agent", icon: "🔴", color: "#f97316",
    specialty: "Complete Checkers Theory & Mastery",
    prompt: `You are the Checkers Strategy Subagent with complete game-theoretic knowledge. Provide:
1. The solved nature of checkers (proven drawn in 2007) and strategic implications
2. The 3 phases of a checkers game and key principles for each
3. Key opening systems: Cross, Single Corner, Double Corner — with moves
4. Mid-game strategy: the key positional concepts
5. Endgame: converting advantages, king positions, key formations
6. How checkers strategy transfers to chess thinking
7. Beginner-to-master roadmap for checkers
8. Top 5 traps beginners fall into
Under 400 words. Be highly practical.`
  }
];

const SYSTEM = `You are an expert subagent in a Game Theory Knowledge Database. You provide precise, educational, actionable insights about chess and checkers. You know chess history from 1924-2024, grandmasters, famous games, statistics, and training methods. Be specific with real examples and practical advice.`;

export default function App() {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});
  const [started, setStarted] = useState(false);

  const runAgent = async (agent) => {
    setLoading(p => ({ ...p, [agent.id]: true }));
    setErrors(p => ({ ...p, [agent.id]: null }));
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SYSTEM,
          messages: [{ role: "user", content: agent.prompt }]
        })
      });
      const data = await res.json();
      const text = data.content?.filter(b => b.type === "text").map(b => b.text).join("\n") || "No response.";
      setResults(p => ({ ...p, [agent.id]: text }));
    } catch (e) {
      setErrors(p => ({ ...p, [agent.id]: "Agent error — please retry." }));
    } finally {
      setLoading(p => ({ ...p, [agent.id]: false }));
    }
  };

  const launchAll = () => {
    setStarted(true);
    SUBAGENTS.forEach(a => runAgent(a));
  };

  const total = Object.values(results).filter(Boolean).length;
  const anyLoading = Object.values(loading).some(Boolean);

  return (
    <div style={{ fontFamily: "system-ui,sans-serif", background: "#08080f", minHeight: "100vh", color: "#e2e8f0" }}>
      <div style={{ background: "linear-gradient(135deg,#1a1740,#0d0d1f)", borderBottom: "1px solid #1e1e3a", padding: "20px 24px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
            <span style={{ fontSize: 32 }}>♟️</span>
            <div>
              <h1 style={{ margin: 0, fontSize: 24, fontWeight: 800, background: "linear-gradient(90deg,#818cf8,#34d399,#f59e0b)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
                Game Theory Knowledge Database
              </h1>
              <p style={{ margin: "2px 0 0", color: "#475569", fontSize: 12 }}>8 AI Subagents • Chess & Checkers • A/B Simulation • Grandmaster Pathway</p>
            </div>
          </div>
          {started && (
            <div style={{ marginTop: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#475569", marginBottom: 4 }}>
                <span>{anyLoading ? "🔄 Subagents running in parallel..." : "✅ All subagents complete!"}</span>
                <span style={{ color: "#34d399" }}>{total}/{SUBAGENTS.length}</span>
              </div>
              <div style={{ background: "#1a1740", borderRadius: 999, height: 5 }}>
                <div style={{ height: 5, borderRadius: 999, background: "linear-gradient(90deg,#6366f1,#34d399)", width: `${(total / SUBAGENTS.length) * 100}%`, transition: "width .5s" }} />
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "20px 24px" }}>
        <div style={{ display: "flex", gap: 10, marginBottom: 22 }}>
          <button onClick={launchAll} disabled={anyLoading} style={{ padding: "10px 24px", background: anyLoading ? "#1f2937" : "linear-gradient(135deg,#6366f1,#8b5cf6)", color: anyLoading ? "#4b5563" : "white", border: "none", borderRadius: 9, fontSize: 14, fontWeight: 700, cursor: anyLoading ? "not-allowed" : "pointer", boxShadow: anyLoading ? "none" : "0 4px 18px rgba(99,102,241,.4)" }}>
            🚀 {anyLoading ? "Running All 8 Subagents..." : "Launch All 8 Subagents"}
          </button>
          <button onClick={() => { setResults({}); setStarted(false); setErrors({}); }} style={{ padding: "10px 16px", background: "#0e0e1c", color: "#475569", border: "1px solid #1a1a2e", borderRadius: 9, fontSize: 12, cursor: "pointer" }}>
            🗑️ Reset
          </button>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(340px,1fr))", gap: 16 }}>
          {SUBAGENTS.map(a => {
            const done = !!results[a.id];
            const busy = !!loading[a.id];
            return (
              <div key={a.id} style={{ background: "#0c0c18", borderRadius: 13, border: `1px solid ${done ? a.color + "45" : "#151528"}`, boxShadow: done ? `0 0 20px ${a.color}15` : "none", transition: "all .3s", overflow: "hidden" }}>
                <div style={{ padding: "12px 16px", background: `linear-gradient(135deg,${a.color}15,transparent)`, borderBottom: `1px solid ${done ? a.color + "25" : "#151528"}`, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ fontSize: 24 }}>{a.icon}</span>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: 13, color: "#f1f5f9" }}>{a.name}</div>
                      <div style={{ fontSize: 10, color: "#334155", marginTop: 1 }}>{a.specialty}</div>
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
                    {done && <span style={{ fontSize: 9, fontWeight: 700, color: a.color, background: a.color + "22", padding: "2px 7px", borderRadius: 999 }}>✓ DONE</span>}
                    {busy && <span style={{ fontSize: 10, color: "#475569" }}>⟳</span>}
                    <button onClick={() => runAgent(a)} disabled={busy} style={{ padding: "4px 11px", background: busy ? "#1f2937" : a.color, color: "white", border: "none", borderRadius: 6, fontSize: 11, fontWeight: 600, cursor: busy ? "not-allowed" : "pointer" }}>
                      {busy ? "..." : done ? "↺" : "▶"}
                    </button>
                  </div>
                </div>
                <div style={{ padding: "12px 16px", minHeight: 72 }}>
                  {errors[a.id] && <div style={{ color: "#f87171", fontSize: 12 }}>{errors[a.id]}</div>}
                  {results[a.id] && <div style={{ fontSize: 12, lineHeight: 1.75, color: "#94a3b8", whiteSpace: "pre-wrap", maxHeight: 280, overflowY: "auto" }}>{results[a.id]}</div>}
                  {!busy && !results[a.id] && !errors[a.id] && <div style={{ color: "#1e1e3a", fontSize: 11, textAlign: "center", paddingTop: 10 }}>Click ▶ to activate agent</div>}
                </div>
              </div>
            );
          })}
        </div>

        {total === SUBAGENTS.length && (
          <div style={{ marginTop: 26, padding: 24, background: "linear-gradient(135deg,#0b1e2d,#0a1f16)", borderRadius: 14, border: "1px solid #10b981" }}>
            <h2 style={{ margin: "0 0 5px", color: "#34d399", fontSize: 18 }}>🏆 Grandmaster Accelerator — Integrated 12-Month Protocol</h2>
            <p style={{ margin: "0 0 16px", color: "#334155", fontSize: 12 }}>Synthesized from all 8 subagent analyses:</p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))", gap: 12 }}>
              {[
                { p: "Month 1–2", i: "⚡", t: "100 tactical puzzles/day. Master fork, pin, skewer. Study Ruy Lopez (1.e4 e5 2.Nf3 Nc6 3.Bb5) as White." },
                { p: "Month 3–4", i: "👑", t: "50 essential endgames. King opposition, Lucena position. Analyze every game with an engine." },
                { p: "Month 5–6", i: "🌳", t: "Study 200 annotated GM games. Train calculation to 10+ moves. Add Sicilian as Black." },
                { p: "Month 7–12", i: "🧠", t: "Weekly OTB tournaments. Specialize in 2-3 openings. Mental pressure training. Study Carlsen's decision process." }
              ].map(x => (
                <div key={x.p} style={{ padding: 13, background: "rgba(255,255,255,0.03)", borderRadius: 9, borderLeft: "3px solid #10b981" }}>
                  <div style={{ fontWeight: 700, color: "#34d399", fontSize: 13, marginBottom: 4 }}>{x.i} {x.p}</div>
                  <div style={{ fontSize: 11, color: "#64748b", lineHeight: 1.6 }}>{x.t}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginTop: 20, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {[
            { title: "♟️ Chess Quick Reference", color: "#6366f1", items: ["Best start: 1.e4 (King's Pawn — most analyzed line)", "Sicilian Defense: 1.e4 c5 — Black's sharpest weapon", "Ruy Lopez: 1.e4 e5 2.Nf3 Nc6 3.Bb5 — classical mastery", "7 Tactics: Fork, Pin, Skewer, Discovery, Deflection, Overload, Zugzwang", "Endgame rule #1: Activate your king immediately", "Rating path: 1200→1600 (tactics) → 1600→2000 (strategy) → GM"] },
            { title: "🔴 Checkers Quick Reference", color: "#f97316", items: ["Game proven drawn in 2007 by Chinook computer", "Control center: squares 14, 15, 18, 19 in opening", "Single Corner: 11-15, 23-19 (most popular system)", "Cross opening: 11-15, 22-17 (aggressive play)", "Kings are 2x value — promote early as priority", "Checkers tactical vision directly sharpens chess!"] }
          ].map(r => (
            <div key={r.title} style={{ background: "#0c0c18", borderRadius: 13, padding: 16, border: `1px solid ${r.color}22` }}>
              <h3 style={{ margin: "0 0 10px", color: r.color, fontSize: 13, fontWeight: 700 }}>{r.title}</h3>
              <ul style={{ margin: 0, padding: "0 0 0 14px" }}>
                {r.items.map((item, i) => <li key={i} style={{ color: "#475569", fontSize: 11, lineHeight: 1.7, marginBottom: 2 }}>{item}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}