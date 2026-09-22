from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db_connection  # type: ignore
from agent_rag import GrantComplianceAgentOrchestrator  # type: ignore

app = FastAPI(title="CDLS Secure Grant Pilot API", version="2.0.0")
security = HTTPBearer()
agent_orchestrator = GrantComplianceAgentOrchestrator()

ROLE_PERMISSIONS = {
    "admin": ["read:grants", "write:grants", "audit:ledger"],
    "auditor": ["read:grants", "audit:ledger"],
    "viewer": ["read:grants"]
}

def verify_role(required_permission: str):
    def dependency(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        user_role = "admin" if token == "pilot-admin-token" else "viewer"
        
        if required_permission not in ROLE_PERMISSIONS.get(user_role, []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges for this government pilot tier."
            )
        return user_role
    return dependency

@app.get("/api/v1/grants")
def get_grants(role: str = Depends(verify_role("read:grants"))):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT grant_id, title, status, allocated, compliance_score FROM grants;")
    grants = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"status": "success", "grants": grants}

@app.post("/api/v1/grants/evaluate")
def evaluate_and_store_grant(grant_data: dict, role: str = Depends(verify_role("write:grants"))):
    evaluation = agent_orchestrator.evaluate_grant(grant_data)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO grants (grant_id, title, status, allocated, compliance_score)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (grant_id) DO UPDATE 
            SET compliance_score = EXCLUDED.compliance_score, status = 'Evaluated';
            """,
            (
                grant_data.get("grant_id"),
                grant_data.get("title"),
                "Evaluated",
                grant_data.get("allocated"),
                evaluation["compliance_score"]
            )
        )
        
        cursor.execute(
            """
            INSERT INTO agent_audit_logs (grant_id, agent_name, evaluation_summary, risk_level)
            VALUES (%s, %s, %s, %s);
            """,
            (
                grant_data.get("grant_id"),
                evaluation["agent_signature"],
                evaluation["evaluation_summary"],
                evaluation["risk_level"]
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
    return {"status": "success", "evaluation": evaluation}