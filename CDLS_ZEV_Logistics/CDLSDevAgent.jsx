import { useState, useEffect, useRef, useCallback } from "react";

// ── Palette & tokens ──────────────────────────────────────────────────────
const C = {
  bg:       "#090E18",
  panel:    "#0D1420",
  surface:  "#111827",
  border:   "#1E2D45",
  borderHi: "#2A4A7A",
  accent:   "#1E8FFF",
  accentDim:"#1260AA",
  green:    "#22D65F",
  gold:     "#F59E0B",
  teal:     "#0ECFD6",
  purple:   "#9B6DFF",
  red:      "#EF4444",
  orange:   "#F97316",
  text:     "#E2EAF8",
  textDim:  "#7B90B2",
  textFaint:"#3A4D68",
};

const STEPS = [
  { id:1, label:"Database Schema",         color:C.accent,  tag:"SQL"     },
  { id:2, label:"RBAC — Operator Role",    color:C.teal,    tag:"Auth"    },
  { id:3, label:"CESAR Agent 6",           color:C.green,   tag:"AI"      },
  { id:4, label:"CESAR Agent 7",           color:C.gold,    tag:"AI"      },
  { id:5, label:"Backend API",             color:C.orange,  tag:"API"     },
  { id:6, label:"Frontend Portal",         color:C.purple,  tag:"React"   },
  { id:7, label:"Audit → Acquisition",     color:C.red,     tag:"Pipeline"},
  { id:8, label:"Logistics Auto-Link",     color:C.accent,  tag:"Events"  },
  { id:9, label:"Token Path-to-Ownership", color:C.teal,    tag:"Web3"    },
  { id:10,label:"Testing & Go-Live",       color:"#64748B", tag:"DevOps"  },
];

const QUICK_ACTIONS = [
  { label:"Generate migration SQL",       prompt:"Generate the complete SQL migration file for the next incomplete step. Include all constraints, indexes, and triggers." },
  { label:"Write the API endpoint",       prompt:"Write the complete Node.js/Express route handler code for the current integration step. Include error handling, auth middleware, and JSDoc comments." },
  { label:"Create the React component",   prompt:"Write the complete React component with Tailwind classes for the current frontend integration step. Make it production-ready." },
  { label:"Write unit tests",             prompt:"Write comprehensive Jest unit tests for the current step. Include happy path, edge cases, and error scenarios." },
  { label:"Debug this error",             prompt:"I'm seeing an error in my integration. Help me debug it step by step. Ask me what the error message is." },
  { label:"Explain the architecture",     prompt:"Explain how this step fits into the overall CDLS platform architecture and how it connects to the other integration steps." },
  { label:"Check my implementation",      prompt:"I've implemented this step. Walk me through a code review checklist to make sure everything is correct before I move on." },
  { label:"Docker + CI/CD config",        prompt:"Generate the Docker and GitHub Actions CI/CD configuration needed for the current step to run in production." },
];

const SYSTEM_PROMPT = `You are the CDLS Integration Developer Agent — a senior full-stack engineer AI assistant embedded directly inside the California Dealer Logistics Solutions platform integration workflow.

You have deep, expert knowledge of the complete CDLS × OperatorX Capital integration across all 10 steps. You write production-ready code and give direct, precise technical answers.

## YOUR CONTEXT: THE PLATFORM

**Tech Stack:** Node.js/Express backend, React + Tailwind frontend, PostgreSQL database, Docker/Kubernetes, Ollama local AI (llama3.2:3b), Polygon/Arbitrum Layer 2 blockchain, WebSocket real-time, GitHub Actions CI/CD, Prometheus + Grafana.

**What CDLS Does:** California Dealer Logistics Solutions — zero-emission vehicle hauling network for automotive dealers. Tesla Semi trucks + lightweight aluminum 9-car trailers. CESAR AI system (5 existing agents). Triple arbitrage: IRS tax advantage ($2.66/mile deduction), capital efficiency (avoid $150K hauler purchase), regulatory compliance (CARB Advanced Clean Fleets).

**OperatorX Integration:** Adding an operator-capital acquisition portal on top of CDLS logistics. OEM-approved operators seeking dealership ownership get matched to distressed dealers via CESAR AI audits. Capital deals flow through SBIC lenders, CalPERS, and 20 Founding Dealer LPs.

## THE 10 INTEGRATION STEPS YOU KNOW IN DETAIL:

**STEP 1 — DATABASE SCHEMA EXPANSION**
- Migration 001: operators table (id UUID, user_id FK, full_name, oem_brands JSONB, oem_verified BOOLEAN, financial_capacity NUMERIC, acquisition_score SMALLINT 0-100, target_markets JSONB, status VARCHAR)
- Migration 002: capital_deals table (id, operator_id FK, dealer_id FK, stage VARCHAR [intro|diligence|term_sheet|credit_committee|closing|closed], purchase_price, equity_required, debt_required, lender_pipeline JSONB, term_sheet_url, diligence_room_id, cdls_contract_id, arrangement_fee, closed_at)
- Migration 003: diligence_documents table (id, deal_id FK, uploaded_by FK, document_type VARCHAR, file_name, file_url, file_size_kb, cesar_analyzed BOOLEAN, cesar_summary TEXT)
- Migration 004: ALTER TABLE hauls ADD operator_id FK + ownership_hours_credited NUMERIC + trigger credit_operator_hours() that increments hours on status='completed'
- All indexes: idx_operators_status, idx_operators_user, idx_deals_stage, idx_deals_operator, idx_deals_dealer, idx_hauls_operator

**STEP 2 — RBAC UPGRADE**
- Add enum values: 'operator' and 'capital_deal_exec' to user_role
- OPERATOR_PERMISSIONS: operators[read:own, update:own], capital_deals[read:own, create, update:own], diligence_documents[read:own, create, delete:own], dealers[read:matched], hauls[read:own], audit_reports[read:matched], tokens[read:own]
- DEAL_EXEC_PERMISSIONS: extends operator permissions with read:all on operators, dealers, capital_deals
- POST /register/operator endpoint creates users row + operators row in a transaction, queues OEM verification

**STEP 3 — CESAR AGENT 6 (Operator Intake & OEM Verification)**
- File: src/agents/operatorIntakeAgent.js
- verifyOEMDocument(operatorId, documentPath): uses Ollama llama3.2:3b, extracts brands/name/date/territory/restrictions from document text, updates operators.oem_verified
- computeAcquisitionScore(operatorId): 4 factors — OEM Brand Score (30pts, premium brands: Toyota/Honda/BMW/Mercedes/Lexus), Financial Capacity Score (30pts, ratio to $2.5M median CA dealer), Market Overlap Score (25pts, distressed dealers in target markets with cesar_distress_score>60, 5pts each, max 25), Experience Score (15pts placeholder)
- matchOperatorToDealers(operatorId): queries dealers WHERE market IN target_markets AND oem_brand IN oem_brands AND cesar_distress_score>60 AND acquisition_available=true, ORDER BY distress DESC LIMIT 3, inserts to operator_dealer_matches, emits WebSocket 'matches_ready'

**STEP 4 — CESAR AGENT 7 (Capital Deal Execution)**
- File: src/agents/capitalDealAgent.js
- Cron at '0 7 * * 1-5' (7am Mon-Fri): finds deals updated_at < 5 days ago, not closed/cancelled, generates follow-up email draft via Ollama, inserts to deal_communications table with status='pending_send'
- analyzeDocumentAsync(docId, text, dealId): called non-blocking after upload, Ollama prompt for 2-3 sentence summary with red flags/key financials/approval conditions, updates cesar_analyzed=true + cesar_summary, emits WebSocket 'document_analyzed'
- generateCreditPackage(dealId): triggered when deal advances to credit_committee stage, calculates logistics savings = haul_volume × (450-356), assembles full credit memo via Ollama (Executive Summary, Operator Profile, Target Analysis, Capital Structure, CDLS Integration Benefit, Risk Factors, Recommendation)

**STEP 5 — BACKEND API**
- File: src/routes/operators.js
  - GET /api/operators/me — returns operator profile (requirePermission operators read:own)
  - PUT /api/operators/me — updates financial_capacity + target_markets, re-runs computeAcquisitionScore
  - POST /api/operators/me/match — triggers matchOperatorToDealers
  - POST /api/operators/me/oem-document — multipart upload, calls verifyOEMDocument
- File: src/routes/deals.js
  - GET /api/deals — returns deals for operator (own) or all (deal_exec)
  - POST /api/deals — creates deal at 'intro' stage
  - PUT /api/deals/:id/stage — advances stage with gate checks (credit_committee requires ≥3 docs, triggers generateCreditPackage), fires onDealClose webhook at 'closed'
  - PUT /api/deals/:id/lenders — pushes lender object to lender_pipeline JSONB array
  - POST /api/deals/:id/documents — file upload, extracts text, inserts doc record, calls analyzeDocumentAsync non-blocking

**STEP 6 — FRONTEND**
- src/pages/OperatorPortal.jsx: loads profile + matches on mount, renders AcquisitionScoreGauge (0-100 gauge), OEMVerificationBadge (green/yellow/red), MatchedDealerCard ×3 (shows dealer name, market, distress score, estimated price, annual floorplan waste), DealKanban
- src/components/DealKanban.jsx: uses @hello-pangea/dnd, 6 columns (intro/diligence/term_sheet/credit_committee/closing/closed), drag triggers PUT /stage API, cards show stall alert (red border + warning) if daysSince(updated_at) > 5
- DiligenceRoom modal per deal: file upload, list of docs with cesar_summary shown inline, lender pipeline tracker

**STEP 7 — AUDIT → ACQUISITION PIPELINE**
- Migration 006: ALTER TABLE dealers ADD acquisition_available BOOLEAN DEFAULT FALSE, acquisition_opted_in_at TIMESTAMPTZ, cesar_distress_score SMALLINT
- Trigger update_acquisition_flag(): sets acquisition_available=TRUE when cesar_distress_score>60 AND acquisition_opted_in_at IS NOT NULL
- generateAcquisitionPackage(dealerId, requestedBy): pulls dealer + audit data, calculates savings (floorplan fees + transport savings = haul_volume × $94), CDLS integration benefits (hvipEligible=true, hvipValue=$330K, v2gAnnualRevenue=$31.5K midpoint), renders PDF

**STEP 8 — LOGISTICS AUTO-LINK**
- src/services/contractAutoLink.js
- onDealClose(dealId): inserts dealer_contracts row (rate_per_vehicle=$356, zev_fleet_size=5, hvip_voucher_eligible=true, v2g_enabled=true, contract_type='acquisition_package', status='pending_signature'), updates capital_deals.cdls_contract_id, emits WebSocket 'contract_ready' to operator room, schedules HVIP reminder for Sept 9 2026
- Hook: db.on('capital_deals:stage_changed') fires onDealClose when newStage === 'closed'

**STEP 9 — TOKEN PATH-TO-OWNERSHIP**
- src/blockchain/operatorTokens.js: ethers.js v6, Polygon RPC, CDLSToken contract
- checkAndMintOwnershipTokens(operatorId): checks ownership_hours_credited >= 1000 AND !ownership_token_minted, mints 100 + floor(bonusHours/10) $CDLS tokens to operator wallet_address, updates operators table with token tx hash, emits WebSocket 'token_milestone'
- Cron job monitors operator hour milestones daily

**STEP 10 — TESTING & GO-LIVE**
- GitHub Actions CI workflow includes services for postgres:15 + ollama/ollama:latest
- Test suites: rbac.test.js, agent6.test.js, agent7.test.js, deals.test.js, acquisition.test.js, contractAutoLink.test.js, tokens.test.js, websocket.test.js
- 20-item master go-live checklist including Polygon testnet verification, HVIP Sept 9 2026 deadline scheduling, Rebecca Auditor RBAC spot-check

## HOW YOU BEHAVE:

1. **Be a senior engineer, not a teacher.** Give direct, production-ready answers. Don't explain basics unless asked.
2. **Write complete code.** No "// ... rest of implementation". Write the full thing.
3. **Reference the actual schema.** Use the exact table names, column names, and function names from this integration.
4. **Know the deadlines.** HVIP voucher deadline: September 9, 2026. California banking compliance: July 1, 2026.
5. **Be opinionated.** If there's a better way to implement something, say so directly.
6. **Format code cleanly** with proper syntax highlighting markers in your responses.
7. **Track context.** If the developer tells you they completed a step, acknowledge it and focus on the next.
8. When writing SQL, always include proper indexes. When writing API routes, always include error handling. When writing React, always include loading states.

You are the expert. The developer is building something real. Help them ship.`;

// ── Styles ────────────────────────────────────────────────────────────────
const styles = `
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=DM+Sans:wght@400;500;600;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: ${C.bg};
    color: ${C.text};
    font-family: 'DM Sans', sans-serif;
    height: 100vh;
    overflow: hidden;
  }

  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: ${C.border}; border-radius: 2px; }
  ::-webkit-scrollbar-thumb:hover { background: ${C.borderHi}; }

  .app {
    display: grid;
    grid-template-columns: 240px 1fr;
    grid-template-rows: 48px 1fr;
    height: 100vh;
    overflow: hidden;
  }

  /* ── Top bar ── */
  .topbar {
    grid-column: 1 / -1;
    background: ${C.panel};
    border-bottom: 1px solid ${C.border};
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 12px;
    position: relative;
  }
  .topbar-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    color: ${C.accent};
    letter-spacing: 0.05em;
  }
  .topbar-logo-dot {
    width: 8px; height: 8px;
    background: ${C.green};
    border-radius: 50%;
    box-shadow: 0 0 6px ${C.green};
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { opacity:1; box-shadow: 0 0 6px ${C.green}; }
    50% { opacity:0.5; box-shadow: 0 0 12px ${C.green}; }
  }
  .topbar-sep { width: 1px; height: 24px; background: ${C.border}; }
  .topbar-title {
    font-size: 12px;
    color: ${C.textDim};
    font-family: 'JetBrains Mono', monospace;
  }
  .topbar-right {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .progress-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: ${C.textDim};
    background: ${C.surface};
    border: 1px solid ${C.border};
    padding: 3px 10px;
    border-radius: 20px;
  }
  .progress-pill span { color: ${C.green}; font-weight: 700; }

  /* ── Sidebar ── */
  .sidebar {
    background: ${C.panel};
    border-right: 1px solid ${C.border};
    overflow-y: auto;
    padding: 12px 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .sidebar-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    color: ${C.textFaint};
    text-transform: uppercase;
    padding: 4px 16px 8px;
  }
  .step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 14px;
    cursor: pointer;
    border-left: 2px solid transparent;
    transition: all 0.15s;
    position: relative;
  }
  .step-item:hover { background: rgba(255,255,255,0.03); }
  .step-item.active {
    background: rgba(30,143,255,0.08);
    border-left-color: ${C.accent};
  }
  .step-item.done { opacity: 0.6; }
  .step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: ${C.textFaint};
    width: 14px;
    flex-shrink: 0;
  }
  .step-check {
    width: 16px; height: 16px;
    border-radius: 3px;
    border: 1.5px solid ${C.border};
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    cursor: pointer;
    transition: all 0.15s;
  }
  .step-check.checked {
    background: ${C.green};
    border-color: ${C.green};
  }
  .step-check svg { display: none; }
  .step-check.checked svg { display: block; }
  .step-label {
    font-size: 11.5px;
    color: ${C.text};
    flex: 1;
    line-height: 1.3;
  }
  .step-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid ${C.border};
    color: ${C.textDim};
  }
  .sidebar-divider {
    height: 1px;
    background: ${C.border};
    margin: 8px 14px;
  }
  .sidebar-footer {
    margin-top: auto;
    padding: 10px 14px 6px;
    border-top: 1px solid ${C.border};
  }
  .total-hours {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: ${C.textDim};
    text-align: center;
  }
  .total-hours span { color: ${C.gold}; }

  /* ── Chat area ── */
  .chat-area {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: ${C.bg};
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px 0;
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .message {
    padding: 0 24px;
    animation: fadeIn 0.2s ease;
  }
  @keyframes fadeIn {
    from { opacity:0; transform: translateY(4px); }
    to   { opacity:1; transform: translateY(0); }
  }
  .message-inner {
    max-width: 860px;
    margin: 0 auto;
  }

  /* User message */
  .msg-user .message-inner {
    display: flex;
    justify-content: flex-end;
    padding: 6px 0;
  }
  .msg-user .bubble {
    background: ${C.accentDim};
    border: 1px solid ${C.accent}44;
    padding: 10px 14px;
    border-radius: 12px 12px 2px 12px;
    max-width: 72%;
    font-size: 13.5px;
    line-height: 1.55;
    color: ${C.text};
    white-space: pre-wrap;
    word-break: break-word;
  }

  /* Assistant message */
  .msg-assistant {
    background: transparent;
    padding-top: 4px;
    padding-bottom: 4px;
  }
  .msg-assistant .message-inner {
    padding: 10px 0;
  }
  .agent-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: ${C.green};
    font-weight: 700;
    letter-spacing: 0.05em;
  }
  .agent-icon {
    width: 20px; height: 20px;
    background: ${C.green}22;
    border: 1px solid ${C.green}66;
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
  }
  .msg-content {
    font-size: 13.5px;
    line-height: 1.65;
    color: ${C.text};
    white-space: pre-wrap;
    word-break: break-word;
  }
  .msg-content code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    background: ${C.surface};
    border: 1px solid ${C.border};
    padding: 1px 5px;
    border-radius: 3px;
    color: ${C.teal};
  }
  .msg-content pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    background: ${C.surface};
    border: 1px solid ${C.border};
    border-left: 3px solid ${C.accent};
    padding: 14px 16px;
    border-radius: 0 6px 6px 0;
    overflow-x: auto;
    line-height: 1.5;
    color: ${C.text};
    margin: 10px 0;
    white-space: pre;
  }
  .msg-content pre code {
    background: none;
    border: none;
    padding: 0;
    color: inherit;
    font-size: inherit;
  }

  /* Streaming cursor */
  .streaming-cursor {
    display: inline-block;
    width: 2px;
    height: 14px;
    background: ${C.accent};
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blink 1s step-end infinite;
  }
  @keyframes blink {
    0%,100% { opacity:1; }
    50% { opacity:0; }
  }

  /* Quick actions */
  .quick-actions {
    padding: 10px 24px 6px;
    max-width: 908px;
    margin: 0 auto;
    width: 100%;
  }
  .qa-scroll {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 6px;
  }
  .qa-scroll::-webkit-scrollbar { height: 0; }
  .qa-btn {
    flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    color: ${C.textDim};
    background: ${C.surface};
    border: 1px solid ${C.border};
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.15s;
    white-space: nowrap;
  }
  .qa-btn:hover {
    background: ${C.panel};
    border-color: ${C.accent};
    color: ${C.accent};
  }

  /* Input area */
  .input-area {
    padding: 10px 24px 16px;
    border-top: 1px solid ${C.border};
    background: ${C.panel};
  }
  .input-wrap {
    max-width: 860px;
    margin: 0 auto;
    display: flex;
    gap: 10px;
    align-items: flex-end;
    background: ${C.surface};
    border: 1px solid ${C.border};
    border-radius: 8px;
    padding: 10px 12px;
    transition: border-color 0.15s;
  }
  .input-wrap:focus-within { border-color: ${C.accent}88; }
  .chat-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: ${C.text};
    font-family: 'DM Sans', sans-serif;
    font-size: 13.5px;
    line-height: 1.5;
    resize: none;
    max-height: 140px;
    overflow-y: auto;
  }
  .chat-input::placeholder { color: ${C.textFaint}; }
  .send-btn {
    width: 32px; height: 32px;
    background: ${C.accent};
    border: none;
    border-radius: 6px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: all 0.15s;
    align-self: flex-end;
  }
  .send-btn:hover { background: #2A9FFF; transform: scale(1.05); }
  .send-btn:disabled { background: ${C.border}; cursor: not-allowed; transform: none; }
  .send-btn svg { width:14px; height:14px; fill:white; }

  .input-hint {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: ${C.textFaint};
    margin-top: 6px;
  }

  /* Welcome state */
  .welcome {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 24px;
    text-align: center;
    gap: 16px;
  }
  .welcome-icon {
    width: 64px; height: 64px;
    background: ${C.accent}18;
    border: 1px solid ${C.accent}44;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    box-shadow: 0 0 40px ${C.accent}22;
  }
  .welcome h2 {
    font-size: 20px;
    font-weight: 700;
    color: ${C.text};
  }
  .welcome p {
    font-size: 13px;
    color: ${C.textDim};
    max-width: 420px;
    line-height: 1.6;
  }
  .welcome-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 8px;
    max-width: 500px;
    width: 100%;
  }
  .welcome-card {
    background: ${C.surface};
    border: 1px solid ${C.border};
    border-radius: 8px;
    padding: 12px 14px;
    cursor: pointer;
    text-align: left;
    transition: all 0.15s;
  }
  .welcome-card:hover {
    border-color: ${C.accent}66;
    background: ${C.panel};
  }
  .wc-label {
    font-size: 12px;
    font-weight: 600;
    color: ${C.text};
    margin-bottom: 3px;
  }
  .wc-desc {
    font-size: 11px;
    color: ${C.textDim};
    line-height: 1.4;
  }

  /* Step context bar */
  .step-context {
    padding: 6px 24px;
    background: ${C.panel};
    border-bottom: 1px solid ${C.border};
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: ${C.textDim};
  }
  .sc-badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.05em;
  }

  /* Error */
  .error-msg {
    background: ${C.red}18;
    border: 1px solid ${C.red}44;
    border-radius: 6px;
    padding: 10px 14px;
    color: ${C.red};
    font-size: 12.5px;
    font-family: 'JetBrains Mono', monospace;
    margin: 8px 0;
  }
`;

// ── Format message content ────────────────────────────────────────────────
function formatMessage(text) {
  const parts = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    const codeBlock = remaining.match(/^```[\s\S]*?```/);
    if (codeBlock) {
      const raw = codeBlock[0];
      const inner = raw.replace(/^```[^\n]*\n?/, "").replace(/```$/, "");
      parts.push(<pre key={key++}><code>{inner}</code></pre>);
      remaining = remaining.slice(raw.length);
      continue;
    }

    const nextCodeIdx = remaining.indexOf("```");
    const chunk = nextCodeIdx > -1 ? remaining.slice(0, nextCodeIdx) : remaining;

    const inlineParts = chunk.split(/(`[^`]+`)/g).map((p, i) =>
      p.startsWith("`") && p.endsWith("`")
        ? <code key={i}>{p.slice(1, -1)}</code>
        : p
    );
    parts.push(<span key={key++}>{inlineParts}</span>);

    if (nextCodeIdx > -1) {
      remaining = remaining.slice(nextCodeIdx);
    } else {
      break;
    }
  }
  return parts;
}

// ── Main component ────────────────────────────────────────────────────────
export default function CDLSDevAgent() {
  const [messages, setMessages]         = useState([]);
  const [input, setInput]               = useState("");
  const [loading, setLoading]           = useState(false);
  const [completed, setCompleted]       = useState({});
  const [activeStep, setActiveStep]     = useState(1);
  const [streamingText, setStreamingText] = useState("");
  const [isStreaming, setIsStreaming]   = useState(false);
  const [error, setError]               = useState(null);

  const messagesEndRef = useRef(null);
  const textareaRef    = useRef(null);

  const completedCount = Object.values(completed).filter(Boolean).length;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
  };

  const toggleStep = (id) => {
    setCompleted(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const sendMessage = useCallback(async (text) => {
    const userText = (text || input).trim();
    if (!userText || loading) return;

    setInput("");
    setError(null);
    if (textareaRef.current) textareaRef.current.style.height = "auto";

    const currentStep = STEPS.find(s => s.id === activeStep);
    const contextNote = currentStep
      ? `[Developer is currently working on Step ${activeStep}: ${currentStep.label}. Completed steps: ${Object.entries(completed).filter(([,v])=>v).map(([k])=>k).join(",")||"none"}]\n\n`
      : "";

    const newUserMsg = { role: "user", content: userText };
    const historyForAPI = [...messages, newUserMsg].map(m => ({
      role: m.role,
      content: m.content
    }));
    // Prepend context to latest user message
    historyForAPI[historyForAPI.length - 1].content = contextNote + userText;

    setMessages(prev => [...prev, newUserMsg]);
    setLoading(true);
    setIsStreaming(true);
    setStreamingText("");

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4096,
          system: SYSTEM_PROMPT,
          stream: true,
          messages: historyForAPI,
        }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error?.message || `API error ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulated = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6).trim();
          if (data === "[DONE]") continue;
          try {
            const parsed = JSON.parse(data);
            if (parsed.type === "content_block_delta" && parsed.delta?.type === "text_delta") {
              accumulated += parsed.delta.text;
              setStreamingText(accumulated);
            }
          } catch {}
        }
      }

      setMessages(prev => [
        ...prev,
        { role: "assistant", content: accumulated }
      ]);
      setStreamingText("");
      setIsStreaming(false);
    } catch (err) {
      setError(err.message);
      setStreamingText("");
      setIsStreaming(false);
    } finally {
      setLoading(false);
    }
  }, [input, messages, loading, activeStep, completed]);

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const WELCOME_CARDS = [
    { label:"Generate Step 1 SQL",    desc:"All 4 migration files ready to run",        prompt:"Generate all 4 complete SQL migration files for Step 1. Include every constraint, index, and trigger." },
    { label:"CESAR Agent 6 code",     desc:"Full OEM verification + scoring logic",      prompt:"Write the complete operatorIntakeAgent.js file — verifyOEMDocument, computeAcquisitionScore, and matchOperatorToDealers — all three functions, production-ready." },
    { label:"Deal API routes",         desc:"All endpoints with auth + error handling",  prompt:"Write the complete src/routes/deals.js file with all endpoints: GET, POST create, PUT stage advance with gate checks, PUT lenders, POST documents. Include all auth middleware and error handling." },
    { label:"React Deal Kanban",      desc:"Drag-drop 6-stage pipeline board",          prompt:"Write the complete DealKanban.jsx component using @hello-pangea/dnd. 6 columns, drag-to-advance-stage, stall alerts after 5 days, full Tailwind styling." },
  ];

  const currentStepInfo = STEPS.find(s => s.id === activeStep);

  return (
    <>
      <style>{styles}</style>
      <div className="app">

        {/* ── Top Bar ── */}
        <header className="topbar">
          <div className="topbar-logo">
            <div className="topbar-logo-dot" />
            CDLS DEV AGENT
          </div>
          <div className="topbar-sep" />
          <div className="topbar-title">OperatorX Integration · v1.0</div>
          <div className="topbar-right">
            <div className="progress-pill">
              <span>{completedCount}</span>/{STEPS.length} steps complete
            </div>
          </div>
        </header>

        {/* ── Sidebar ── */}
        <aside className="sidebar">
          <div className="sidebar-header">Integration Steps</div>

          {STEPS.map(step => (
            <div
              key={step.id}
              className={`step-item ${activeStep === step.id ? "active" : ""} ${completed[step.id] ? "done" : ""}`}
              onClick={() => setActiveStep(step.id)}
            >
              <span className="step-num">{step.id}</span>
              <div
                className={`step-check ${completed[step.id] ? "checked" : ""}`}
                onClick={e => { e.stopPropagation(); toggleStep(step.id); }}
                style={completed[step.id] ? { background: step.color, borderColor: step.color } : {}}
              >
                <svg viewBox="0 0 10 8" width="9" height="7" fill="none">
                  <path d="M1 4L3.5 6.5L9 1" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <span className="step-label" style={completed[step.id] ? { textDecoration:"line-through", color:C.textFaint } : {}}>
                {step.label}
              </span>
              <span className="step-tag" style={activeStep === step.id ? { borderColor: step.color + "88", color: step.color } : {}}>
                {step.tag}
              </span>
            </div>
          ))}

          <div className="sidebar-divider" />
          <div className="sidebar-footer">
            <div className="total-hours">Est. total: <span>51h</span> engineering</div>
          </div>
        </aside>

        {/* ── Chat ── */}
        <main className="chat-area">

          {/* Step context bar */}
          {currentStepInfo && (
            <div className="step-context">
              <span>Active:</span>
              <span
                className="sc-badge"
                style={{ background: currentStepInfo.color + "22", color: currentStepInfo.color, border: `1px solid ${currentStepInfo.color}44` }}
              >
                Step {currentStepInfo.id} · {currentStepInfo.label}
              </span>
              <span style={{ color: C.textFaint }}>·</span>
              <span>{currentStepInfo.tag}</span>
            </div>
          )}

          {/* Messages or Welcome */}
          {messages.length === 0 && !isStreaming ? (
            <div className="welcome">
              <div className="welcome-icon">⚡</div>
              <h2>CDLS Developer Agent</h2>
              <p>
                Senior engineer AI with full knowledge of the CDLS × OperatorX integration.
                Ask for code, debug issues, or generate any integration artifact.
              </p>
              <div className="welcome-grid">
                {WELCOME_CARDS.map((c, i) => (
                  <div key={i} className="welcome-card" onClick={() => sendMessage(c.prompt)}>
                    <div className="wc-label">{c.label}</div>
                    <div className="wc-desc">{c.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message msg-${msg.role}`}>
                  <div className="message-inner">
                    {msg.role === "assistant" ? (
                      <>
                        <div className="agent-header">
                          <div className="agent-icon">⚡</div>
                          CDLS DEV AGENT
                        </div>
                        <div className="msg-content">{formatMessage(msg.content)}</div>
                      </>
                    ) : (
                      <div className="bubble">{msg.content}</div>
                    )}
                  </div>
                </div>
              ))}

              {/* Streaming message */}
              {isStreaming && (
                <div className="message msg-assistant">
                  <div className="message-inner">
                    <div className="agent-header">
                      <div className="agent-icon">⚡</div>
                      CDLS DEV AGENT
                    </div>
                    <div className="msg-content">
                      {formatMessage(streamingText)}
                      <span className="streaming-cursor" />
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="message msg-assistant">
                  <div className="message-inner">
                    <div className="error-msg">⚠ {error}</div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Quick actions */}
          {messages.length > 0 && (
            <div className="quick-actions">
              <div className="qa-scroll">
                {QUICK_ACTIONS.map((qa, i) => (
                  <button
                    key={i}
                    className="qa-btn"
                    onClick={() => sendMessage(qa.prompt)}
                    disabled={loading}
                  >
                    {qa.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="input-area">
            <div className="input-wrap">
              <textarea
                ref={textareaRef}
                className="chat-input"
                placeholder="Ask for code, debug an error, or explain a concept…"
                value={input}
                onChange={e => { setInput(e.target.value); autoResize(); }}
                onKeyDown={handleKey}
                rows={1}
                disabled={loading}
              />
              <button
                className="send-btn"
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
              >
                <svg viewBox="0 0 16 16">
                  <path d="M1 8L15 1L8.5 15L7 9L1 8Z"/>
                </svg>
              </button>
            </div>
            <div className="input-hint">↵ send · ⇧↵ newline · click step to set active context</div>
          </div>

        </main>
      </div>
    </>
  );
}
