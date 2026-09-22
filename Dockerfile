# CDLS Platform — Patched Dockerfile (api and vdr share same base)
# Adds: RUN apt-get upgrade to pull latest Debian patches into the image layer
# Addresses: 44 HIGH OS CVEs in debian 13.7 base (util-linux, ncurses, systemd family)
# Note: CVEs with status="affected" and no Fixed Version are tracked upstream —
# apt-get upgrade pulls whatever Debian has published as of build time.

FROM python:3.11-slim

ARG SERVICE=api
ARG PORT=8000
ENV SERVICE=${SERVICE}
ENV PORT=${PORT}

# ---------------------------------------------------------------
# OS-layer CVE mitigation:
# - apt-get update pulls latest package index
# - apt-get upgrade -y installs all available security patches
# - Addresses: util-linux CVEs (2026-76642, 78408, 78409, 78410)
#              ncurses CVE-2025-69720
#              systemd CVE-2026-16742
#              acl CVE-2026-54369
# - perl-base CVE-2026-9538 is "fix_deferred" by Debian — patched when available
# ---------------------------------------------------------------
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends \
    libmupdf-dev \
    ffmpeg \
    libsndfile1 \
    gcc \
    g++ \
    curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# ---------------------------------------------------------------
# Python package CVE mitigations:
# - jaraco.context: pin to >=6.1.0 (fixes CVE-2026-23949 path traversal)
# - wheel: pin to >=0.46.2 (fixes CVE-2026-24049 privilege escalation)
# - chromadb 1.5.9: 4 CVEs (2 CRITICAL) — no upstream fix yet published
#   Runtime mitigations in place: read-only rootfs, cap_drop ALL,
#   no-new-privileges, localhost-only binding
# ---------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "jaraco.context>=6.1.0" \
    "wheel>=0.46.2" && \
    pip install --no-cache-dir -r requirements.txt

COPY auth.py .
COPY api_server.py .
COPY vdr_server.py .
COPY database/ ./database/
COPY config/ ./config/
COPY orchestrator.py .

RUN mkdir -p patent_drawings secure_vault chroma_audio_store temp_audio && \
    groupadd -r cdls && useradd -r -g cdls cdls && \
    chown -R cdls:cdls /app
USER cdls

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE ${PORT:-8000}

CMD if [ "$SERVICE" = "vdr" ]; then \
        uvicorn vdr_server:app --host 0.0.0.0 --port 8001 --workers 2; \
    else \
        uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 2; \
    fi
