import React, { useState, useEffect, useRef } from "react";

export default function UniversalResearchDashboard() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("System Ready (Offline Engine)");
  const [isSyncing, setIsSyncing] = useState(false);
  const [activeTab, setActiveTab] = useState("search");
  const searchInputRef = useRef(null);

  // Keyboard shortcut: Press "/" to focus search input
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "/" && document.activeElement !== searchInputRef.current) {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setStatus(`Searching local knowledge base for "${query}"...`);
    try {
      const res = await fetch(`/api/query?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data.results || []);
      setStatus(`Found ${data.results?.length || 0} matching sources.`);
    } catch {
      setStatus("Query error: Verify local backend is running.");
    }
  };

  const triggerPipelineSync = async () => {
    setIsSyncing(true);
    setStatus("Executing pipeline sync and compiling IP documents...");
    try {
      await fetch("/api/sync", { method: "POST" });
      setStatus("Pipeline completed: Research Index and IP Word doc refreshed.");
    } catch {
      setStatus("Sync failed: Check terminal logs.");
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Accessibility Skip Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:p-3 focus:bg-blue-700 focus:text-white focus:rounded focus:ring-2 focus:ring-offset-2 focus:ring-blue-900"
      >
        Skip to main content
      </a>

      {/* Top Application Bar */}
      <header className="border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">
              Universal Research Assistant & IP Portfolio Studio
            </h1>
            <p className="text-sm text-slate-600">
              CDLS Platform · Contemporaneous R&D & Patent Automation
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Live Accessibility Status Announcement */}
            <div
              role="status"
              aria-live="polite"
              className="text-xs px-3 py-1.5 rounded-full font-medium bg-slate-100 text-slate-700 border border-slate-200"
            >
              {status}
            </div>

            <button
              onClick={triggerPipelineSync}
              disabled={isSyncing}
              className="inline-flex items-center justify-center min-h-[44px] min-w-[44px] px-4 py-2 text-sm font-semibold rounded-lg bg-blue-700 text-white hover:bg-blue-800 focus:ring-4 focus:ring-blue-200 disabled:opacity-50 transition-colors"
              aria-busy={isSyncing}
            >
              {isSyncing ? "Syncing Pipeline..." : "Run Ingestion & Sync"}
            </button>
          </div>
        </div>
      </header>

      {/* Main Workspace Layout */}
      <main id="main-content" className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Search & Live Querying */}
        <section aria-labelledby="search-section-heading" className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h2 id="search-section-heading" className="text-lg font-bold text-slate-900 mb-2">
              Query Local Knowledge Base
            </h2>
            <p className="text-sm text-slate-600 mb-4">
              Search across technical uncertainties, experiment logs, and CARB/V2G specifications. Press <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-300 rounded text-xs font-mono">/</kbd> to focus.
            </p>

            <form onSubmit={handleSearch} className="space-y-4">
              <div>
                <label htmlFor="search-input" className="sr-only">
                  Search research logs, patents, and engineering work
                </label>
                <div className="relative">
                  <input
                    ref={searchInputRef}
                    id="search-input"
                    type="search"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g., What technical uncertainties were resolved for the MagSafe battery pod?"
                    className="w-full min-h-[48px] pl-4 pr-12 text-sm rounded-lg border border-slate-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-600 focus:outline-none transition-colors"
                  />
                  <button
                    type="submit"
                    aria-label="Submit search query"
                    className="absolute right-1.5 top-1.5 bottom-1.5 px-3 flex items-center justify-center rounded-md bg-slate-900 text-white hover:bg-slate-800 focus:ring-2 focus:ring-offset-1 focus:ring-slate-900"
                  >
                    Search
                  </button>
                </div>
              </div>
            </form>
          </div>

          {/* Search Results Region */}
          <div aria-live="polite" className="space-y-4">
            {results.length > 0 ? (
              results.map((item, idx) => (
                <article
                  key={idx}
                  className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-colors"
                >
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-50 text-blue-800 border border-blue-200">
                      {item.domain || "General R&D"}
                    </span>
                    <span className="text-xs text-slate-500 font-mono">
                      Importance: {item.importance_score || 5}/10
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mb-1">
                    {item.title}
                  </h3>
                  <p className="text-xs font-mono text-slate-500 mb-3 truncate">
                    Source: {item.url}
                  </p>
                  <blockquote className="text-sm text-slate-700 bg-slate-50 p-3 rounded border-l-4 border-blue-600 leading-relaxed">
                    {item.summary}
                  </blockquote>
                </article>
              ))
            ) : (
              <div className="p-8 text-center bg-white rounded-xl border border-dashed border-slate-300">
                <p className="text-sm text-slate-500">
                  Enter a query above to retrieve contemporaneous R&D records and patent claims.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Right Column: Generated Deliverables & Artifacts */}
        <aside aria-labelledby="artifacts-heading" className="space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h2 id="artifacts-heading" className="text-lg font-bold text-slate-900 mb-1">
              Generated Deliverables
            </h2>
            <p className="text-xs text-slate-600 mb-4">
              Real-time artifacts compiled from verified SQLite and ChromaDB data.
            </p>

            <ul className="space-y-3" role="list">
              <li className="p-3.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Patent Portfolio Word Document
                    </h3>
                    <p className="text-xs text-slate-600 mt-0.5">
                      USPTO-formatted specification with claims and R&D evidence table.
                    </p>
                  </div>
                </div>
                <a
                  href="/download/docx"
                  download="CDLS_IP_Patent_Portfolio_Submission.docx"
                  className="mt-3 inline-flex items-center text-xs font-semibold text-blue-700 hover:text-blue-900 underline focus:ring-2 focus:ring-blue-600 focus:outline-none"
                >
                  Download .docx File →
                </a>
              </li>

              <li className="p-3.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      UX Intelligence Report
                    </h3>
                    <p className="text-xs text-slate-600 mt-0.5">
                      Translates engineering uncertainties into human-centered UI mechanics.
                    </p>
                  </div>
                </div>
                <a
                  href="/download/ux"
                  download="UX_RESEARCH_FINDINGS.md"
                  className="mt-3 inline-flex items-center text-xs font-semibold text-blue-700 hover:text-blue-900 underline focus:ring-2 focus:ring-blue-600 focus:outline-none"
                >
                  Download UX_RESEARCH_FINDINGS.md →
                </a>
              </li>

              <li className="p-3.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Master Research Index
                    </h3>
                    <p className="text-xs text-slate-600 mt-0.5">
                      Categorized domain taxonomy and full asset catalog.
                    </p>
                  </div>
                </div>
                <a
                  href="/download/index"
                  download="RESEARCH_INDEX.md"
                  className="mt-3 inline-flex items-center text-xs font-semibold text-blue-700 hover:text-blue-900 underline focus:ring-2 focus:ring-blue-600 focus:outline-none"
                >
                  Download RESEARCH_INDEX.md →
                </a>
              </li>
            </ul>
          </div>

          {/* Ingested Source Status Card */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-sm font-bold text-slate-900 mb-2">Active Data Sources</h3>
            <ul className="text-xs text-slate-600 space-y-2 font-mono">
              <li className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-600" aria-hidden="true"></span>
                <span>CDLS_RD_Time_Tracker_MERGED_FULL.xlsx</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-600" aria-hidden="true"></span>
                <span>Wikipedia RAG & Transformer Docs</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-600" aria-hidden="true"></span>
                <span>Anthropic API & Cookbook Docs</span>
              </li>
            </ul>
          </div>
        </aside>
      </main>
    </div>
  );
}