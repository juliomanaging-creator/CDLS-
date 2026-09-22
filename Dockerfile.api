FROM python:3.11-slim

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Update base system packages to pull latest upstream security patches
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and explicitly ensure patched high-severity pins
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "jaraco.context>=6.1.0" "wheel>=0.46.2" && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Enforce secure non-root runtime
RUN useradd -u 10001 cdlsuser && chown -R cdlsuser:cdlsuser /app
USER cdlsuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
