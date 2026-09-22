# Threat Model & Mitigations (STRIDE Framework)

| Threat Category | Potential Vector | CDLS Mitigation Control |
|-----------------|------------------|-------------------------|
| **Spoofing** | API gateway impersonation | JWT + Role-Based Access Control (RBAC - NIST AC-3) |
| **Tampering** | Proposal text injection | NIST SI-10 sanitization & ChromaDB secure vector store |
| **Repudiation** | Unlogged grant disbursements | PostgreSQL foreign-key constraints & Cryptographic audit ledger |
| **Info Disclosure** | Environment variable leak | Hardened Docker secrets & strict .env exclusion via .gitignore |
| **Denial of Service** | Resource exhaustion via large payloads | FastAPI payload limits & Uvicorn worker timeouts |
| **Privilege Escalation**| Container root breakout | Non-root runtime enforcement (UID 10001) & cap_drop: ALL |
