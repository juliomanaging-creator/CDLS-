import { useState } from "react";

const NAVY = "#1B3A5C";
const GOLD = "#C8962E";
const RED = "#C0392B";
const GREEN = "#2E7D32";

const EMAILS = [
  {
    id: 1,
    recipient: "National Archives — Riverside, CA",
    to: "Archives1@nara.gov",
    subject: "Research Request: Naturalization Petition — John David McNeil, ca. 1880–1910",
    phase: "Phase 3",
    body: `Dear NARA Riverside Research Team,

I am writing to request access to naturalization records for a genealogical research project related to a Canadian citizenship application.

SUBJECT OF RESEARCH:
Name: John David McNeil (variants: McNeal, MacNeil, M'Neil)
Born: approximately 1860, Nova Scotia, Canada
Believed to have naturalized in California between approximately 1880 and 1910

RECORDS REQUESTED:
1. Declaration of Intent ("First Papers") for John David McNeil
2. Petition for Naturalization ("Second Papers") for John David McNeil
3. Certificate of Naturalization (if held by your facility)
4. Any index cards or supporting documentation in the naturalization file

PURPOSE:
This research is being conducted to support a formal citizenship application to Immigration, Refugees and Citizenship Canada (IRCC) under Form CIT 0001 (Application for a Citizenship Certificate). The naturalization petition, if found, will serve as primary evidence that Mr. McNeil was a Canadian citizen at the time of his entry to the United States.

Please advise on any applicable fees for certified copies and the expected turnaround time. If records cannot be located at Riverside, please advise whether records may be held at a different NARA facility.

I am happy to provide any additional identifying information to assist your search.

Thank you for your time and assistance.

Respectfully,`,
  },
  {
    id: 2,
    recipient: "Nova Scotia Archives",
    to: "nsarm@novascotia.ca",
    subject: "Genealogical Research Request: Birth Registration — John David McNeil (1860) + Delayed Registrations",
    phase: "Phase 3",
    body: `Dear Nova Scotia Archives Research Services,

I am conducting genealogical research to support a Canadian Citizenship Certificate application (IRCC Form CIT 0001) and require assistance locating vital records from your holdings.

RECORDS REQUESTED:

1. LONG-FORM Birth Registration for John David McNeil
   - Born: approximately 1860
   - County: Richmond County, Cape Breton, Nova Scotia
   - Parish/area: Arichat or West Arichat area
   - Note: Long-form is specifically needed as it contains parents' names and birthplaces

2. DELAYED Birth Registrations for McNeil children
   - Surname: McNeil (variants: MacNeil, MacNeal, M'Neil)
   - County: Richmond County, Cape Breton, Nova Scotia
   - Time period: Any delayed registrations for children born before 1908
   - Father's name: John David McNeil (born ~1860)

3. Any related vital records that may assist in establishing the family unit

PURPOSE:
These records are required to establish an unbroken documentary chain of descent for a Canadian Citizenship Certificate application under IRCC Form CIT 0001. The long-form birth registration is critical as it will confirm parentage and Canadian birthplace.

Please advise on your fees for certified copies, acceptable payment methods, and whether records can be provided with an official government seal or certification for use as legal evidence.

If records from this period are held at a county or church archive rather than the provincial archives, I would be grateful for any referral.

Thank you sincerely for your assistance.

Respectfully,`,
  },
  {
    id: 3,
    recipient: "Library and Archives Canada — ATIP Office",
    to: "atip.aiprp@bac-lac.gc.ca",
    subject: "ATIP Request — Bill McNeil CBC Radio Recordings and Personnel Records",
    phase: "Phase 3",
    body: `Dear Access to Information and Privacy Office,
Library and Archives Canada,

I am submitting a formal request under the Access to Information Act for records related to the following individual:

SUBJECT OF REQUEST:
Name: Bill McNeil (William McNeil)
Occupation: CBC Radio broadcaster, journalist, author
Active period: approximately 1950s–1990s
Known works: "Voice of the Pioneer" series (CBC Radio), various CBC documentary programs

RECORDS REQUESTED:
1. All CBC Radio recordings featuring or produced by Bill McNeil held by Library and Archives Canada
2. Any personnel or producer records, contracts, or correspondence for Bill McNeil held by LAC
3. Any finding aids, indexes, or catalogs that reference Bill McNeil's CBC work
4. Program schedules, production notes, or archival finding aids referencing "Voice of the Pioneer"

PURPOSE:
This request supports a Canadian Citizenship Certificate application under IRCC Form CIT 0001 (Application for a Citizenship Certificate). The records are required to demonstrate a substantial cultural and familial connection to Canada as supporting evidence in the citizenship application package.

I understand standard ATIP processing may take up to 30 days and I am prepared for any applicable fees under the Act.

Please confirm receipt of this request and advise of the assigned file number for tracking purposes.

Thank you for your time.

Respectfully,`,
  },
  {
    id: 4,
    recipient: "Cape Breton University — Beaton Institute",
    to: "beaton@cbu.ca",
    subject: "Genealogical Research Inquiry — McNeil Family Records, Richmond County / Cape Breton, NS",
    phase: "Phase 3 (Gap Identified)",
    body: `Dear Beaton Institute Archives,

I am conducting genealogical research for a family with deep roots in Cape Breton, Nova Scotia, and have been referred to the Beaton Institute as an outstanding resource for Cape Breton family history.

FAMILY BEING RESEARCHED:
Surname: McNeil (variants: MacNeil, MacNeal, M'Neil)
Key Individual: John David McNeil, born approximately 1860, Richmond County, Cape Breton
Location: Arichat / West Arichat area, Richmond County, Cape Breton Island

RECORDS / ASSISTANCE REQUESTED:
1. Any McNeil / MacNeil family records held in your collections relating to Richmond County
2. Community records, directories, or newspapers referencing the McNeil family in Arichat or West Arichat, ca. 1855–1915
3. Guidance on whether your collections include any records from Immaculate Conception Church (West Arichat) or Notre Dame de l'Assomption (Arichat)
4. Any photographs, oral history recordings, or community histories that may reference this family

PURPOSE:
These records are being gathered to support a Canadian Citizenship Certificate application (IRCC Form CIT 0001) and to construct a complete documentary record of the family's physical and cultural presence in Nova Scotia.

Please advise on your research services, fees, and any remote/mail-in research options available.

Thank you very much for your time and for the extraordinary work the Beaton Institute does in preserving Cape Breton heritage.

Respectfully,`,
  },
];

const statusColors = {
  "Not Sent": { bg: "#FFF0F0", color: RED, dot: RED },
  "Sent": { bg: "#F0FFF4", color: GREEN, dot: GREEN },
  "Sending...": { bg: "#FFF9EC", color: GOLD, dot: GOLD },
  "Error": { bg: "#FFF0F0", color: RED, dot: RED },
};

export default function GmailSender() {
  const [statuses, setStatuses] = useState({});
  const [selected, setSelected] = useState(null);
  const [sending, setSending] = useState(null);
  const [senderName, setSenderName] = useState("Rebecca's Research Team");
  const [logs, setLogs] = useState([]);

  const getStatus = (id) => statuses[id] || "Not Sent";

  const addLog = (msg, type = "info") => {
    setLogs(prev => [{ msg, type, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 20));
  };

  const sendEmail = async (email) => {
    setSending(email.id);
    setStatuses(s => ({ ...s, [email.id]: "Sending..." }));
    addLog(`Sending to ${email.recipient}...`, "info");

    try {
      const fullBody = email.body + `\n\n${senderName}\nProject Maple Lineage Research Team`;
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          mcp_servers: [{ type: "url", url: "https://gmail.mcp.claude.com/mcp", name: "gmail-mcp" }],
          messages: [{
            role: "user",
            content: `Please send an email using Gmail with exactly these details:
To: ${email.to}
Subject: ${email.subject}
Body: ${fullBody}

After sending, confirm with: SENT_SUCCESS`
          }]
        })
      });

      const data = await res.json();
      const textBlocks = (data.content || []).filter(b => b.type === "text").map(b => b.text).join(" ");
      
      if (textBlocks.includes("SENT_SUCCESS") || textBlocks.toLowerCase().includes("sent") || textBlocks.toLowerCase().includes("success")) {
        setStatuses(s => ({ ...s, [email.id]: "Sent" }));
        addLog(`✅ Email sent to ${email.recipient}`, "success");
      } else {
        setStatuses(s => ({ ...s, [email.id]: "Error" }));
        addLog(`⚠️ Unexpected response for ${email.recipient} — check Gmail Sent folder to verify`, "warn");
      }
    } catch (err) {
      setStatuses(s => ({ ...s, [email.id]: "Error" }));
      addLog(`❌ Error sending to ${email.recipient}: ${err.message}`, "error");
    } finally {
      setSending(null);
    }
  };

  const sendAll = async () => {
    for (const email of EMAILS) {
      if (getStatus(email.id) !== "Sent") {
        await sendEmail(email);
        await new Promise(r => setTimeout(r, 1500));
      }
    }
  };

  const sentCount = EMAILS.filter(e => getStatus(e.id) === "Sent").length;

  return (
    <div style={{ fontFamily: "Arial, sans-serif", maxWidth: 900, margin: "0 auto", background: "#f8f9fa", minHeight: "100vh", padding: 0 }}>
      {/* Header */}
      <div style={{ background: NAVY, padding: "20px 28px", color: "white" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
          <span style={{ fontSize: 28 }}>🍁</span>
          <div>
            <div style={{ fontSize: 20, fontWeight: "bold", letterSpacing: 1 }}>PROJECT MAPLE LINEAGE</div>
            <div style={{ fontSize: 12, color: "#c8c8c8", marginTop: 2 }}>Gmail Outreach Sender — Connected to Your Google Account</div>
          </div>
        </div>
        {/* Progress bar */}
        <div style={{ marginTop: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#aaa", marginBottom: 4 }}>
            <span>Emails sent</span>
            <span style={{ color: GOLD, fontWeight: "bold" }}>{sentCount} / {EMAILS.length}</span>
          </div>
          <div style={{ height: 6, background: "#ffffff22", borderRadius: 3, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${(sentCount / EMAILS.length) * 100}%`, background: GOLD, borderRadius: 3, transition: "width 0.4s" }} />
          </div>
        </div>
      </div>

      <div style={{ padding: "20px 28px" }}>
        {/* Sender name + Send All */}
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end", marginBottom: 20, flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 220 }}>
            <label style={{ fontSize: 11, fontWeight: "bold", color: "#555", display: "block", marginBottom: 4 }}>YOUR NAME (appears in email signature)</label>
            <input
              value={senderName}
              onChange={e => setSenderName(e.target.value)}
              style={{ width: "100%", padding: "8px 12px", border: `1px solid #ccc`, borderRadius: 6, fontSize: 13, fontFamily: "Arial", boxSizing: "border-box" }}
            />
          </div>
          <button
            onClick={sendAll}
            disabled={!!sending || sentCount === EMAILS.length}
            style={{ padding: "9px 22px", background: sentCount === EMAILS.length ? "#aaa" : GOLD, color: "white", border: "none", borderRadius: 6, fontWeight: "bold", fontSize: 13, cursor: sentCount === EMAILS.length ? "default" : "pointer", whiteSpace: "nowrap" }}
          >
            {sentCount === EMAILS.length ? "✅ All Sent" : `📤 Send All Pending (${EMAILS.length - sentCount})`}
          </button>
        </div>

        {/* Email cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {EMAILS.map(email => {
            const status = getStatus(email.id);
            const sc = statusColors[status] || statusColors["Not Sent"];
            const isExpanded = selected === email.id;
            return (
              <div key={email.id} style={{ background: "white", borderRadius: 10, border: `1px solid #e0e0e0`, overflow: "hidden", boxShadow: "0 1px 4px rgba(0,0,0,0.07)" }}>
                {/* Card header */}
                <div
                  onClick={() => setSelected(isExpanded ? null : email.id)}
                  style={{ display: "flex", alignItems: "center", gap: 14, padding: "14px 18px", cursor: "pointer", userSelect: "none" }}
                >
                  <div style={{ width: 32, height: 32, borderRadius: "50%", background: NAVY, color: GOLD, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold", fontSize: 14, flexShrink: 0 }}>{email.id}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: "bold", fontSize: 13, color: "#1a1a1a", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{email.recipient}</div>
                    <div style={{ fontSize: 11, color: "#777", marginTop: 2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{email.to}</div>
                    <div style={{ fontSize: 11, color: NAVY, marginTop: 2, fontStyle: "italic", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{email.phase}</div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "4px 10px", borderRadius: 20, background: sc.bg, fontSize: 11, fontWeight: "bold", color: sc.color }}>
                      <div style={{ width: 7, height: 7, borderRadius: "50%", background: sc.dot }} />
                      {status}
                    </div>
                    <span style={{ color: "#aaa", fontSize: 16 }}>{isExpanded ? "▲" : "▼"}</span>
                  </div>
                </div>

                {/* Expanded body */}
                {isExpanded && (
                  <div style={{ borderTop: "1px solid #f0f0f0", padding: "0 18px 18px" }}>
                    <div style={{ marginTop: 14, marginBottom: 8 }}>
                      <div style={{ fontSize: 11, fontWeight: "bold", color: "#555", marginBottom: 4 }}>SUBJECT</div>
                      <div style={{ fontSize: 12, color: NAVY, fontWeight: "bold", padding: "6px 10px", background: "#f0f4fa", borderRadius: 5 }}>{email.subject}</div>
                    </div>
                    <div style={{ marginBottom: 14 }}>
                      <div style={{ fontSize: 11, fontWeight: "bold", color: "#555", marginBottom: 4 }}>EMAIL BODY (preview)</div>
                      <pre style={{ fontSize: 11, color: "#444", background: "#fafafa", border: "1px solid #eee", borderRadius: 5, padding: "10px 12px", whiteSpace: "pre-wrap", wordBreak: "break-word", maxHeight: 220, overflowY: "auto", fontFamily: "Arial, sans-serif", lineHeight: 1.5 }}>
                        {email.body + `\n\n${senderName}\nProject Maple Lineage Research Team`}
                      </pre>
                    </div>
                    <div style={{ display: "flex", gap: 10 }}>
                      <button
                        onClick={() => sendEmail(email)}
                        disabled={!!sending || status === "Sent"}
                        style={{ flex: 1, padding: "10px", background: status === "Sent" ? "#e0f0e0" : sending === email.id ? GOLD : NAVY, color: "white", border: "none", borderRadius: 7, fontWeight: "bold", fontSize: 13, cursor: status === "Sent" || !!sending ? "default" : "pointer" }}
                      >
                        {status === "Sent" ? "✅ Sent" : sending === email.id ? "⏳ Sending..." : "📤 Send via Gmail"}
                      </button>
                      <button
                        onClick={() => navigator.clipboard?.writeText(email.body)}
                        style={{ padding: "10px 16px", background: "#f0f0f0", border: "1px solid #ddd", borderRadius: 7, fontSize: 12, cursor: "pointer", color: "#333" }}
                        title="Copy body to clipboard"
                      >📋</button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Activity Log */}
        {logs.length > 0 && (
          <div style={{ marginTop: 24 }}>
            <div style={{ fontSize: 12, fontWeight: "bold", color: "#555", marginBottom: 8 }}>📋 ACTIVITY LOG</div>
            <div style={{ background: "#1a1a2e", borderRadius: 8, padding: "12px 14px", maxHeight: 160, overflowY: "auto" }}>
              {logs.map((l, i) => (
                <div key={i} style={{ fontSize: 11, fontFamily: "monospace", color: l.type === "success" ? "#7fffd4" : l.type === "error" ? "#ff8080" : l.type === "warn" ? "#ffd580" : "#aaa", marginBottom: 3 }}>
                  <span style={{ color: "#666" }}>[{l.time}]</span> {l.msg}
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginTop: 20, padding: "12px 16px", background: "#FFF9EC", border: `1px solid ${GOLD}`, borderRadius: 8, fontSize: 11, color: "#665500" }}>
          <strong>📌 NOTE:</strong> This sender is connected to your Google account via Gmail MCP. Each email is sent from your Gmail address. After sending, verify delivery in your Gmail Sent folder. Log all send dates in the Excel tracker.
        </div>
      </div>
    </div>
  );
}