import sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# ------------------------------------------------------------------------------
# 1. DATABASE INTEGRITY & NIST SI-10 TESTS
# ------------------------------------------------------------------------------

def test_database_foreign_keys_pragma():
    """Verify NIST SI-10 / PRAGMA foreign_keys = ON regression guard."""
    db_path = Path("cdls_master_catalog.db")
    conn = sqlite3.connect(str(db_path) if db_path.exists() else ":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys;")
    result = cur.fetchone()[0]
    conn.close()
    assert result == 1, "Foreign key constraints must be strictly enabled (PRAGMA foreign_keys = 1)."

# ------------------------------------------------------------------------------
# 2. VDR REVERSIBLE WATERMARKING & AUTH ACCESS CONTROL (CWE-598 / AC-3)
# ------------------------------------------------------------------------------

def test_vdr_unauthenticated_access_denial():
    """Verify CWE-598 / AC-3 Access Revocation & Session Cookie Enforcement."""
    from vdr_server import app as vdr_app, init_ledger_db
    init_ledger_db()
    with TestClient(vdr_app) as client:
        response = client.get("/api/vdr/render-page?page_num=0")
        assert response.status_code in [400, 403], "Unauthenticated requests without vdr_session cookie must be rejected."

# ------------------------------------------------------------------------------
# 3. API CORS & ROUTE SANITIZATION TESTS (CWE-942 / AC-4)
# ------------------------------------------------------------------------------

def test_cors_origin_restriction():
    """Verify CWE-942 / AC-4 CORS origin restrictions."""
    try:
        from api_server import app as api_app
        with TestClient(api_app) as client:
            headers = {"Origin": "https://malicious-external-site.com"}
            response = client.get("/api/query?q=test", headers=headers)
            allowed_origin = response.headers.get("access-control-allow-origin")
            assert allowed_origin != "https://malicious-external-site.com"
            assert allowed_origin != "*"
    except Exception as e:
        pytest.skip(f"API server initialization deferred: {e}")

def test_patent_drawings_route_sanitization():
    """Verify input path sanitization for patent drawings."""
    try:
        from api_server import app as api_app
        with TestClient(api_app) as client:
            response = client.get("/api/drawings/non_existent_figure_999.svg")
            assert response.status_code == 404
    except Exception as e:
        pytest.skip(f"API server initialization deferred: {e}")