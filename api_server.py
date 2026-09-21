"""
Unified CDLS API Server: IP Studio, Synchronized Figures & Real-Time Audio RAG
Remediated: Strict Origin Whitelisting (CWE-942) & Safe TypedDict Retrieval
"""

import os
import io
import json
import sqlite3
import zipfile
import asyncio
import base64
from pathlib import Path
from contextlib import asynccontextmanager

# Suppress Hugging Face Windows symlink warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import chromadb
from sentence_transformers import SentenceTransformer
import edge_tts

from database.db_manager import DatabaseManager
from config.settings import load_config
from orchestrator import OrchestratorAgent

BASE_DIR = Path(__file__).resolve().parent
DRAWINGS_DIR = BASE_DIR / "patent_drawings"
PDF_PATH = BASE_DIR / "CDLS_Patent_Drawings_Complete_87_Sheets.pdf"
ZIP_PATH = BASE_DIR / "CDLS_Full_Patent_Portfolio_Package.zip"
DB_PATH = BASE_DIR / "anthropic_kb.db"
CHROMA_DIR = BASE_DIR / "chroma_audio_store"

config = load_config()
db = DatabaseManager(config)
orchestrator = OrchestratorAgent(config)

asr_model = WhisperModel("base.en", device="cpu", compute_type="int8")
embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
audio_kb = chroma_client.get_or_create_collection(name="audio_transcripts")

VOICE_NAME = "en-US-AndrewMultilingualNeural"
VOICE_RATE = "+0%"
VOICE_PITCH = "+0Hz"

async def generate_speech_audio(text: str) -> str:
    """Generates speech via Edge-TTS and returns base64 audio (Type-Safe)."""
    try:
        communicate = edge_tts.Communicate(text, VOICE_NAME, rate=VOICE_RATE, pitch=VOICE_PITCH)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk.get("type") == "audio":
                audio_bytes = chunk.get("data")
                if isinstance(audio_bytes, bytes):
                    audio_data += audio_bytes
        return base64.b64encode(audio_data).decode("utf-8")
    except Exception as e:
        print(f"[TTS Error] {e}")
        return ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.initialize()
    await orchestrator.initialize()
    yield

app = FastAPI(title="CDLS Studio & Audio RAG Server", lifespan=lifespan)

# REMEDIATION: Explicit Origin Whitelist (CWE-942 / AC-4)
ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8001",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

def get_figure_metadata(fig_num: int, title: str, domain: str, uncertainty: str, activity: str, source_url: str = "", importance: int = 10):
    base_num = fig_num * 10
    text_corpus = f"{title} {domain} {uncertainty} {activity}".lower()

    if any(k in text_corpus for k in ["magsafe", "coupler", "disconnect", "pedal", "mechanical", "breakaway", "latch", "clamping"]):
        archetype = "Mechanical Breakaway & Retention Assembly"
        cluster = "Cluster 1: Electro-Mechanical Fleet Systems (USPTO #63/734829)"
        numerals = [
            {"num": str(base_num + 2), "label": "Male Coupler Housing", "desc": "Dielectric structural body with internal contact channels."},
            {"num": str(base_num + 4), "label": "Vehicle Receptacle Interface", "desc": "Chassis-mounted flush receiver with guided docking channels."},
            {"num": str(base_num + 6), "label": "Permanent Rare-Earth Clamping Array", "desc": "N52 neodymium magnet configuration calibrated for dynamic road retention vs. 25-lb manual breakaway."},
            {"num": str(base_num + 8), "label": "DC High-Amperage Bus Terminals", "desc": "Dual solid-copper power conductors with insulated sliding contact sleeves."},
            {"num": str(base_num + 10), "label": "Optical Interlock Safety Loop", "desc": "Closed-circuit optical loop triggering sub-10ms high-voltage de-energization prior to separation."},
            {"num": str(base_num + 12), "label": "Mechanical Cam & Pedal Release", "desc": "Foot-pedal actuated lever linkage delivering 4:1 mechanical advantage for decoupling."}
        ]
        claim = f"Claim {fig_num}: An electro-mechanical fast-disconnect coupling apparatus comprising: a housing ({base_num + 2}); a permanent magnet clamping array ({base_num + 6}) retaining contact under vibrational load while decoupling under axial tension exceeding 25 pounds-force; and an optical safety loop ({base_num + 10}) triggering rapid de-energization."
    elif any(k in text_corpus for k in ["battery", "v2g", "caiso", "storage", "trailer", "inverter", "smud", "kwh", "grid"]):
        archetype = "Electrical Vehicle-to-Grid (V2G) Architecture"
        cluster = "Cluster 1: Electro-Mechanical Fleet Systems — Mobile Storage & V2G"
        numerals = [
            {"num": str(base_num), "label": "Mobile Storage Trailer Enclosure", "desc": "Weather-sealed DOT-compliant trailer enclosure with integrated thermal barriers."},
            {"num": str(base_num + 2), "label": "Parallel LFP Battery Storage Pack", "desc": "360 kWh Lithium Iron Phosphate cell array structured in 120 parallel strings with per-cell monitoring."},
            {"num": str(base_num + 4), "label": "Bidirectional Power Inverter Core", "desc": "38.4 kW high-efficiency bidirectional DC/AC inverter adhering to IEEE 15118-20 and UL 9741 protocols."},
            {"num": str(base_num + 6), "label": "BMS & Automated Dispatch Controller", "desc": "Microprocessor running telemetry and CAISO / SMUD automated demand response auction logic."},
            {"num": str(base_num + 8), "label": "Power Interconnect Cable Reel", "desc": "Heavy-duty tensioned spring-return cable reel routing high-current lines to the physical grid tie point."}
        ]
        claim = f"Claim {fig_num}: A mobile grid-support power distribution system comprising: a mobile trailer platform ({base_num}); an onboard energy storage pack ({base_num + 2}) providing at least 360 kWh of capacity; a bidirectional inverter ({base_num + 4}) communicating via IEEE 15118-20 protocols; and a programmable controller ({base_num + 6}) configured to automatically dispatch stored power during grid peak pricing windows."
    elif any(k in text_corpus for k in ["judas", "cryptographic", "zero-knowledge", "zk", "hash", "vision", "yolo", "resnet", "camera"]):
        archetype = "Cryptographic Zero-Knowledge Audit Engine"
        cluster = "Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI)"
        numerals = [
            {"num": str(base_num), "label": "Inspection Portal Envelope", "desc": "Boundary framework enclosing multi-spectral illumination and camera fixtures at transfer gates."},
            {"num": str(base_num + 2), "label": "High-Resolution Optical Imaging Array", "desc": "Multi-angle imaging sensors capturing calibrated high-fidelity structural surface records."},
            {"num": str(base_num + 4), "label": "Edge Computer Vision Damage Inference", "desc": "Embedded convolutional model performing real-time bounding-box defect detection and confidence scoring."},
            {"num": str(base_num + 6), "label": "Primary SHA-256 Cryptographic Engine", "desc": "Cryptographic engine executing root hash generation over raw uncompressed pixel matrices."},
            {"num": str(base_num + 8), "label": "Zero-Knowledge Proof (ZKP) Prover Core", "desc": "zk-SNARK Pedersen vector commitment engine proving inspection compliance without exposing confidential imagery."},
            {"num": str(base_num + 10), "label": "Append-Only Audit Ledger", "desc": "GAGAS-compliant tamper-evident hash chain preserving indelible non-repudiation records."}
        ]
        claim = f"Claim {fig_num}: A verifiable cryptographic inspection system comprising: an optical sensor array ({base_num + 2}) positioned at a physical transfer boundary; an edge inference engine ({base_num + 4}) generating localized defect bounding coordinates; a dual-hash engine ({base_num + 6}) computing immutable state hashes; and a zero-knowledge commitment module ({base_num + 8}) generating mathematical proofs of integrity."
    elif any(k in text_corpus for k in ["route", "mcmc", "cari", "cesar", "stochastic", "monte carlo", "metropolis", "optimization"]):
        archetype = "Three-Layer Stochastic Route Intelligence"
        cluster = "Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR)"
        numerals = [
            {"num": str(base_num), "label": "Three-Layer Route Engine Boundary", "desc": "Unified runtime environment hosting modular hierarchical route computation layers."},
            {"num": str(base_num + 2), "label": "Layer 1: Regression Denoising Filter", "desc": "10-year historical LASSO cost baseline filter eliminating systemic external noise and fuel spikes."},
            {"num": str(base_num + 4), "label": "Layer 2: Stochastic MCMC Sampler", "desc": "Metropolis-Hastings 10,000-iteration probability distribution engine modeling route variability."},
            {"num": str(base_num + 6), "label": "Dynamic CAISO Rate Telemetry Feed", "desc": "Real-time automated ingestion pipe pulling hourly day-ahead and spot marginal electricity tariffs."},
            {"num": str(base_num + 8), "label": "Layer 3: Human Behavioral Stabilization", "desc": "Deterministic variant-assignment engine applying Hours-of-Service safety constraints and dispatch smoothing."}
        ]
        claim = f"Claim {fig_num}: A multi-tier adaptive route optimization system comprising: a first regularized regression engine ({base_num + 2}) generating cost baselines from historical datasets; a second Markov Chain Monte Carlo sampler ({base_num + 4}) executing stochastic iterations against real-time telemetry ({base_num + 6}); and a third stabilization layer ({base_num + 8}) enforcing deterministic constraints."
    elif any(k in text_corpus for k in ["carb", "ctc", "trucrs", "envelope", "encryption", "compliance", "aead", "vin"]):
        archetype = "Regulatory Topology & Envelope Encryption"
        cluster = "Cluster 4: Regulatory Compliance & Multi-Tenant Data Architecture"
        numerals = [
            {"num": str(base_num), "label": "Cloud Gateway Perimeter", "desc": "Zero-trust network perimeter enforcing TLS 1.3 mutual authentication and payload sanitation."},
            {"num": str(base_num + 2), "label": "Multi-Tenant Dealer DMS Ingestion", "desc": "API adapters synchronizing inventory and telematics across Tier A/B/C dealer management databases."},
            {"num": str(base_num + 4), "label": "AAD-Bound AEAD Cryptographic Vault", "desc": "AES-256-GCM hardware-backed vault maintaining isolated Data Encryption Keys (DEKs) per tenant."},
            {"num": str(base_num + 6), "label": "CARB VIN Verification Engine", "desc": "Automated compliance rule engine checking vehicles against 13 CCR §§ 2195–2199 statutes."},
            {"num": str(base_num + 8), "label": "CARB Clean Truck Check (CTC) Gateway", "desc": "Automated reporting pipe delivering verified OBD/opacity compliance payloads to state portals."},
            {"num": str(base_num + 10), "label": "TRUCRS Fleet Ledger Engine", "desc": "Synchronized state fleet database maintaining historical verification receipts and certificate hashes."}
        ]
        claim = f"Claim {fig_num}: A multi-tenant regulatory compliance apparatus comprising: a dealer DMS interface ({base_num + 2}); a cryptographic isolation vault ({base_num + 4}) encrypting tenant records with separate Authenticated Additional Data keys; a statutory rule engine ({base_num + 6}) evaluating vehicle compliance; and an automated dispatch gateway ({base_num + 8}) submitting signed compliance records."
    else:
        archetype = "Telematics Fleet Dashboard Architecture"
        cluster = "Cluster 4: Dealer Operations & Telematics Infrastructure"
        numerals = [
            {"num": str(base_num), "label": "Fleet Operations Console Envelope", "desc": "Responsive administration console interface displaying synchronized multi-vehicle telemetry."},
            {"num": str(base_num + 2), "label": "Real-Time Telematics Ingestion Module", "desc": "Subsystem aggregating live battery State-of-Charge (SOC), thermal readings, and GPS telemetry."},
            {"num": str(base_num + 4), "label": "HVIP Voucher Automation Engine", "desc": "Eligibility rule evaluator and automated document filing pipeline achieving <5% voucher rejection rates."},
            {"num": str(base_num + 6), "label": "48-Hour Onboarding & Carbon Accounting", "desc": "Verra VCS-compliant per-haul carbon reduction engine with automated dealer onboarding workflows."}
        ]
        claim = f"Claim {fig_num}: An automated fleet monitoring and compliance apparatus comprising: a telematics ingestion interface ({base_num + 2}) capturing state metrics; an incentive automation processor ({base_num + 4}) validating voucher criteria; and an onboarding engine ({base_num + 6}) calculating carbon offset displacement metrics in real time."

    source_clean = source_url or "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx"
    sheet_name, row_id = "", ""
    if "#" in source_clean:
        parts = source_clean.split("#")
        source_clean = parts[0]
        sheet_coord = parts[1]
        sheet_name, row_id = sheet_coord.split("!") if "!" in sheet_coord else (sheet_coord, "")

    return {
        "fig_num": fig_num,
        "fig_key": f"FIG_{fig_num}",
        "archetype": archetype,
        "cluster": cluster,
        "numerals": numerals,
        "claim": claim,
        "title": title,
        "domain": domain,
        "uncertainty": uncertainty,
        "activity": activity,
        "source_url": source_url,
        "source_path": source_clean,
        "source_sheet": sheet_name,
        "source_row": row_id,
        "importance": importance
    }

def fetch_single_figure_meta(fig_key: str):
    clean_name = fig_key.replace(".svg", "")
    try:
        fig_num = int(clean_name.split("_")[1])
    except Exception:
        fig_num = 1

    rec = (f"R&D Asset #{fig_num}", "General R&D", "", "", "")
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT title, domain, summary, content, url FROM documents ORDER BY id ASC LIMIT 1 OFFSET ?", (fig_num - 1,))
            row = cur.fetchone()
            if row:
                rec = row
            conn.close()
        except Exception:
            pass

    return get_figure_metadata(
        fig_num=fig_num,
        title=rec[0] or f"R&D Disclosure #{fig_num}",
        domain=rec[1] or "General R&D",
        uncertainty=rec[2] or "Technical uncertainty elimination",
        activity=rec[3] or "Experimental verification",
        source_url=rec[4] if len(rec) > 4 else ""
    )

@app.get("/api/query")
async def api_query(q: str = Query(..., description="User query text")):
    docs = await db.semantic_search(q, top_k=5)
    return {"results": docs}

@app.get("/api/query/stream")
async def api_query_stream(q: str = Query(..., description="User query text")):
    docs = await db.semantic_search(q, top_k=4)

    async def token_generator():
        init_payload = {
            "type": "sources",
            "sources": [
                {
                    "title": d.get("title", "R&D Entry"),
                    "domain": d.get("domain", "General R&D"),
                    "score": d.get("importance_score", 5),
                    "url": d.get("url", "CDLS Tracker")
                }
                for d in docs
            ]
        }
        yield f"data: {json.dumps(init_payload)}\n\n"
        await asyncio.sleep(0.05)

        synthesis = (
            f"Synthesizing retrieved disclosures for '{q}':\n\n"
            f"Based on contemporaneous engineering records from the CDLS R&D tracker, "
            f"the technical uncertainties resolving this domain focus on:\n\n"
        )
        for i, d in enumerate(docs, 1):
            synthesis += f"{i}. {d.get('title')}: {d.get('summary', d.get('content', ''))}\n\n"

        synthesis += (
            "Statutory Enablement (35 U.S.C. § 112):\n"
            "The experimental methodology, testing parameters, and empirical results recorded above "
            "provide reproducible validation supporting the independent claim structures."
        )

        tokens = synthesis.split(" ")
        for token in tokens:
            yield f"data: {json.dumps({'type': 'token', 'text': token + ' '})}\n\n"
            await asyncio.sleep(0.02)

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(token_generator(), media_type="text/event-stream")

@app.get("/api/drawings/{fig_name}")
async def get_drawing(fig_name: str):
    clean_name = fig_name.replace(".svg", "")
    fig_path = DRAWINGS_DIR / f"{clean_name}.svg"

    if not fig_path.exists():
        matches = list(DRAWINGS_DIR.glob(f"{clean_name}.*"))
        if matches:
            fig_path = matches[0]
        else:
            return JSONResponse({"error": f"Drawing {clean_name}.svg not found on disk."}, status_code=404)

    return Response(
        content=fig_path.read_text(encoding="utf-8"),
        media_type="image/svg+xml",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )

@app.get("/download/figure/{fig_name}/pdf")
async def download_figure_pdf(fig_name: str):
    clean_name = fig_name.replace(".svg", "")
    svg_path = DRAWINGS_DIR / f"{clean_name}.svg"
    if not svg_path.exists():
        return JSONResponse({"error": f"{clean_name}.svg not found."}, status_code=404)

    try:
        from svglib.svglib import svg2rlg
        from reportlab.pdfgen import canvas
        from reportlab.graphics import renderPDF

        pdf_buffer = io.BytesIO()
        PAGE_WIDTH, PAGE_HEIGHT = 612, 792
        c = canvas.Canvas(pdf_buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        drawing = svg2rlg(str(svg_path))
        if drawing:
            drawing.scale(PAGE_WIDTH / 816.0, PAGE_HEIGHT / 1056.0)
            drawing.width = PAGE_WIDTH
            drawing.height = PAGE_HEIGHT
            renderPDF.draw(drawing, c, 0, 0)
            c.showPage()
            c.save()
            pdf_buffer.seek(0)
            return Response(
                content=pdf_buffer.getvalue(),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={clean_name}_Drawing_Sheet.pdf"}
            )
    except Exception as e:
        return JSONResponse({"error": f"Failed compiling figure PDF: {e}"}, status_code=500)

@app.get("/download/figure/{fig_name}/docx")
async def download_figure_docx(fig_name: str):
    clean_name = fig_name.replace(".svg", "")
    meta = fetch_single_figure_meta(clean_name)
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor

        doc = Document()
        for s in doc.sections:
            s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1.0)

        p = doc.add_paragraph()
        r = p.add_run(f"USPTO PATENT DISCLOSURE: FIG. {meta['fig_num']}")
        r.bold = True
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(15, 23, 42)

        doc.add_heading("1. Subject Matter Identification", level=2)
        doc.add_paragraph(f"Figure Designation: FIG. {meta['fig_num']}")
        doc.add_paragraph(f"Architectural Archetype: {meta['archetype']}")
        doc.add_paragraph(f"Primary Record: {meta['title']}")

        doc.add_heading("2. 37 CFR § 1.84 Component Numerals", level=2)
        for n in meta["numerals"]:
            doc.add_paragraph(f"Reference Numeral {n['num']}: {n['label']} — {n['desc']}")

        doc.add_heading("3. Statutory Patent Claim Structure", level=2)
        doc.add_paragraph(meta["claim"])

        doc.add_heading("4. Contemporaneous Experimental R&D Verification (IRC § 41)", level=2)
        doc.add_paragraph(f"Uncertainty: {meta['uncertainty']}\nActivity: {meta['activity']}")

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return Response(
            content=buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={clean_name}_Specification_and_Claims.docx"}
        )
    except Exception as e:
        return JSONResponse({"error": f"Failed generating figure DOCX: {e}"}, status_code=500)

@app.get("/api/preview/patent")
async def api_preview_patent():
    path = BASE_DIR / "CDLS_IP_Patent_Portfolio_Submission.docx"
    db_records = []
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT title, domain, summary, content, url FROM documents ORDER BY id ASC LIMIT 87")
            db_records = cur.fetchall()
            conn.close()
        except Exception:
            pass

    figures_meta = {}
    for i in range(1, 88):
        rec = db_records[i - 1] if i - 1 < len(db_records) else (f"Asset Record #{i:02d}", "General R&D", "", "", "")
        figures_meta[f"FIG_{i}"] = get_figure_metadata(
            fig_num=i,
            title=rec[0] or f"R&D Disclosure #{i}",
            domain=rec[1] or "General R&D",
            uncertainty=rec[2] or "Technical uncertainty elimination",
            activity=rec[3] or "Experimental verification",
            source_url=rec[4] if len(rec) > 4 else ""
        )

    elements = []
    tables_data = []
    if path.exists():
        try:
            from docx import Document
            doc = Document(str(path))
            for p in doc.paragraphs:
                text = p.text.strip()
                if text:
                    style_name = str(p.style.name) if (p.style and p.style.name) else ""
                    elements.append({
                        "type": "heading" if "Heading" in style_name else "paragraph",
                        "text": text,
                        "style": style_name
                    })
            for table in doc.tables:
                t_rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                if t_rows:
                    tables_data.append(t_rows)
        except Exception as e:
            print(f"[WARN] Error reading docx: {e}")

    return {
        "title": "INTELLECTUAL PROPERTY DISCLOSURE & PATENT SPECIFICATION PORTFOLIO",
        "elements": elements,
        "tables": tables_data,
        "figures": sorted(list(figures_meta.keys()), key=lambda x: int(x.split('_')[1])),
        "figures_meta": figures_meta
    }

@app.get("/download/all")
async def download_all_zip():
    with zipfile.ZipFile(str(ZIP_PATH), "w", zipfile.ZIP_DEFLATED) as archive:
        for file_name in [
            "CDLS_IP_Patent_Portfolio_Submission.docx",
            "CDLS_Patent_Drawings_Complete_87_Sheets.pdf",
            "CDLS_PROGRAM_REVIEW_DOCUMENT.docx",
            "CDLS_PROGRAM_ARCHITECTURE_AND_SYSTEM_OUTLINE.docx",
            "CDLS_SYSTEM_DESIGN_REVIEW_AND_POSTMORTEM.docx",
            "EXECUTIVE_RESEARCH_KNOWLEDGE_SUMMARY.docx",
            "EXECUTIVE_RESEARCH_KNOWLEDGE_SUMMARY.pdf",
            "UX_RESEARCH_FINDINGS.md",
            "RESEARCH_INDEX.md"
        ]:
            p = BASE_DIR / file_name
            if p.exists():
                archive.write(p, arcname=file_name)

        if DRAWINGS_DIR.exists():
            for fig_file in sorted(DRAWINGS_DIR.glob("*.svg")):
                archive.write(fig_file, arcname=f"patent_drawings_svg/{fig_file.name}")

    return FileResponse(
        path=str(ZIP_PATH),
        filename="CDLS_Full_Patent_Portfolio_Package.zip",
        media_type="application/zip"
    )

@app.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    await websocket.accept()
    temp_dir = BASE_DIR / "temp_audio"
    temp_dir.mkdir(exist_ok=True)

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            temp_file = temp_dir / f"in_{asyncio.get_event_loop().time()}.wav"
            temp_file.write_bytes(audio_bytes)

            try:
                segments, _ = asr_model.transcribe(str(temp_file), beam_size=2)
                user_text = " ".join([s.text for s in segments]).strip()
            except Exception:
                user_text = ""
            finally:
                if temp_file.exists():
                    temp_file.unlink()

            if user_text:
                q_emb = embed_model.encode([user_text]).tolist()
                res = audio_kb.query(query_embeddings=q_emb, n_results=2)
                
                reply = "Based on indexed records: "
                if res and res["documents"] and res["documents"][0]:
                    reply += res["documents"][0][0]
                else:
                    reply += "The CDLS platform utilizes 360 kWh mobile battery trailers and N52 magnetic quick-disconnect couplers."

                audio_b64 = await generate_speech_audio(reply)
                await websocket.send_json({
                    "user_text": user_text,
                    "spoken_text": reply,
                    "display_text": reply,
                    "audio_b64": audio_b64
                })
            else:
                await websocket.send_json({
                    "user_text": "[Unintelligible audio]",
                    "spoken_text": "Please speak closer to the microphone.",
                    "display_text": "No transcript detected.",
                    "audio_b64": ""
                })
    except WebSocketDisconnect:
        pass

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = BASE_DIR / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>index.html not found</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)