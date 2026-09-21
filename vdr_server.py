"""
CDLS Secure Virtual Data Room (VDR) Engine
Remediated: Persistent SQLite Ledger (CWE-662), HttpOnly Cookie Auth (CWE-598), Explicit CORS (CWE-942)
"""

import io
import time
import secrets
import sqlite3
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "secure_vault"
DOCUMENTS_DIR.mkdir(exist_ok=True)
LEDGER_DB = BASE_DIR / "vdr_ledger.db"

app = FastAPI(title="CDLS Secure Virtual Data Room")

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

def init_ledger_db():
    conn = sqlite3.connect(LEDGER_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS access_tokens (
            token TEXT PRIMARY KEY,
            recipient TEXT NOT NULL,
            doc_name TEXT NOT NULL,
            active INTEGER NOT NULL,
            created_at REAL NOT NULL,
            revoked_at REAL
        )
    """)
    conn.commit()
    conn.close()

init_ledger_db()

def get_session_from_db(token: str):
    if not token:
        return None
    conn = sqlite3.connect(LEDGER_DB)
    cur = conn.cursor()
    cur.execute("SELECT recipient, doc_name, active, created_at, revoked_at FROM access_tokens WHERE token = ?", (token,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "recipient": row[0],
            "doc_name": row[1],
            "active": bool(row[2]),
            "created_at": row[3],
            "revoked_at": row[4]
        }
    return None

def apply_forensic_watermark(page, viewer_email: str, client_ip: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    watermark_text = f"CONFIDENTIAL - CDLS IP VAULT\nLICENSED TO: {viewer_email}\nIP: {client_ip} | {timestamp}\nDO NOT COPY OR FORWARD"
    rect = page.rect
    page.insert_textbox(
        rect,
        watermark_text,
        fontsize=16,
        fontname="helv",
        color=(0.7, 0.2, 0.2),
        align=fitz.TEXT_ALIGN_CENTER,
        rotate=45,
        opacity=0.30
    )

@app.post("/api/vdr/create-link")
async def create_share_link(doc_name: str, recipient_email: str):
    doc_path = DOCUMENTS_DIR / doc_name
    if not doc_path.exists():
        raise HTTPException(status_code=404, detail="Requested file not found in secure_vault.")

    token = secrets.token_urlsafe(32)
    conn = sqlite3.connect(LEDGER_DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO access_tokens (token, recipient, doc_name, active, created_at) VALUES (?, ?, ?, 1, ?)",
        (token, recipient_email, doc_name, time.time())
    )
    conn.commit()
    conn.close()

    return {
        "exchange_url": f"http://127.0.0.1:8001/vdr/enter?exchange={token}",
        "recipient": recipient_email,
        "document": doc_name,
        "status": "Active (Persistent)"
    }

@app.get("/vdr/enter")
async def enter_viewer(exchange: str, response: Response):
    session = get_session_from_db(exchange)
    if not session or not session.get("active"):
        raise HTTPException(status_code=403, detail="ACCESS_REVOKED: Viewing token is invalid or rescinded.")

    resp = RedirectResponse(url="/vdr/viewer", status_code=302)
    resp.set_cookie(
        key="vdr_session",
        value=exchange,
        httponly=True,
        secure=False,  # Set to True when TLS (CIR-008) is active
        samesite="lax",
        max_age=7200
    )
    return resp

@app.post("/api/vdr/revoke")
async def revoke_access(request: Request):
    token = request.cookies.get("vdr_session")
    if not token:
        token = request.query_params.get("token")

    if not token:
        raise HTTPException(status_code=400, detail="Missing session or token.")

    conn = sqlite3.connect(LEDGER_DB)
    cur = conn.cursor()
    cur.execute("UPDATE access_tokens SET active = 0, revoked_at = ? WHERE token = ?", (time.time(), token))
    conn.commit()
    conn.close()

    resp = JSONResponse({"status": "success", "message": "Access revoked permanently."})
    resp.delete_cookie("vdr_session")
    return resp

@app.get("/api/vdr/render-page")
async def render_page(page_num: int, request: Request):
    token = request.cookies.get("vdr_session")
    session = get_session_from_db(token)
    if not session or not session.get("active"):
        raise HTTPException(status_code=403, detail="ACCESS_REVOKED: Permission rescinded.")

    doc_path = DOCUMENTS_DIR / session["doc_name"]
    if not doc_path.exists():
        raise HTTPException(status_code=404, detail="File missing.")

    client_ip = request.client.host if request.client else "127.0.0.1"
    doc = fitz.open(str(doc_path))

    if page_num < 0 or page_num >= len(doc):
        raise HTTPException(status_code=400, detail="Page index out of bounds.")

    page = doc[page_num]
    apply_forensic_watermark(page, session["recipient"], client_ip)
    pix = page.get_pixmap(dpi=140)
    img_bytes = pix.tobytes("png")
    doc.close()

    return Response(
        content=img_bytes,
        media_type="image/png",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )

@app.get("/api/vdr/doc-info")
async def get_doc_info(request: Request):
    token = request.cookies.get("vdr_session")
    session = get_session_from_db(token)
    if not session or not session.get("active"):
        raise HTTPException(status_code=403, detail="Access revoked or session expired.")

    doc_path = DOCUMENTS_DIR / session["doc_name"]
    doc = fitz.open(str(doc_path))
    count = len(doc)
    doc.close()

    return {
        "title": session["doc_name"],
        "pages": count,
        "recipient": session["recipient"],
        "active": session["active"]
    }

@app.get("/vdr/viewer", response_class=HTMLResponse)
async def serve_vdr_viewer():
    html_path = BASE_DIR / "vdr_viewer.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>vdr_viewer.html missing</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)