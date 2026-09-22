# CDLS Platform â€” Versioned Institutional Release Plan

## v0.1.0-alpha (Current State)
* **Core Functionality**: FastAPI backend endpoints (/api/dashboard/metrics, /api/grants, /api/grants/vet) fully operational.
* **Database**: SQLAlchemy models for Grant and Milestone configured with PostgreSQL persistence.
* **Security & CI/CD**: Automated Security Sentinel achieving 100/100 score in GitHub Actions.
* **Containerization**: Hardened multi-stage Dockerfiles with non-root user enforcement.

## v0.2.0-beta (Target: Q2 2026)
* **External Penetration Testing**: Engagement handoff to Bright Defense and Synack for white-box security review.
* **Advanced Multi-Agent RAG**: Integration of dedicated ChromaDB vector retrieval agents for automated state guideline cross-referencing.
* **Compliance Certification**: Finalization of California DGS SB/MB state procurement verification.

## v1.0.0-GA (Target: Q3 2026)
* **Pilot Deployment**: 90-day sandbox deployment with state agency partners (GO-Biz / CEC).
* **High-Availability Infrastructure**: Multi-region PostgreSQL replication and automated failover orchestration.
* **Enterprise SLA**: 99.9% uptime guarantee with 24/7 automated security telemetry monitoring.
