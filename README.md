# Anthropic Knowledge Base — Multi-Agent System

A production-grade multi-agent system that scrapes, categorizes, indexes, and queries 
**everything Anthropic has publicly published** — documentation, research papers, model 
specs, API references, GitHub repos, safety research, and more.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│               ORCHESTRATOR AGENT                     │
│     orchestrator.py — coordinates all agents         │
└──────────┬──────────────────────────┬───────────────┘
           │                          │
  ┌────────▼────────┐      ┌──────────▼──────────┐
  │ INGESTION AGENT │      │ CATEGORIZATION AGENT │
  │ ingestion_agent │      │ categorization_agent │
  │                 │      │                      │
  │ • Web scraper   │      │ • Claude API tagging │
  │ • PDF parser    │      │ • Domain assignment  │
  │ • GitHub API    │      │ • Summary generation │
  │ • Deduplication │      │ • Key fact extraction│
  └────────┬────────┘      └──────────┬───────────┘
           └──────────┬───────────────┘
                      ▼
          ┌──────────────────────┐
          │     DATABASE LAYER   │
          │                      │
          │  SQLite/PostgreSQL   │  ← Structured metadata
          │  ChromaDB (vectors)  │  ← Semantic search
          └──────────┬───────────┘
                     │
          ┌──────────▼───────────┐
          │     QUERY AGENT      │
          │   query_agent.py     │
          │                      │
          │  RAG-powered Q&A     │
          │  Claude synthesis    │
          └──────────────────────┘
                     │
          ┌──────────▼───────────┐
          │      SCHEDULER       │
          │    scheduler.py      │
          │                      │
          │  Weekly full rebuild │
          │  Daily incremental   │
          │  6hr news check      │
          └──────────────────────┘
```

---

## Quick Start

### 1. Setup
```bash
cd anthropic_kb
python setup.py
```

### 2. Add your API key
```bash
# Edit .env file:
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the full pipeline
```bash
python orchestrator.py
```

### 4. Query the knowledge base
```python
import asyncio
from orchestrator import OrchestratorAgent
from config.settings import load_config

async def main():
    config = load_config()
    kb = OrchestratorAgent(config)
    
    # Initialize (if not already run)
    await kb.db.initialize()
    
    # Query
    answer = await kb.query("What is Claude's context window size?")
    print(answer)

asyncio.run(main())
```

### 5. Start the scheduler (continuous updates)
```bash
python scheduler.py
```

---

## What Gets Indexed

| Source | Type | Coverage |
|---|---|---|
| `docs.anthropic.com` | Documentation | Full API reference, guides, tutorials |
| `support.anthropic.com` | Support | Product features, FAQ, limits |
| `anthropic.com/research` | Research Papers | All published papers |
| `anthropic.com/news` | News | Releases, announcements |
| `anthropic.com/safety` | Safety | Policies, RSP, model cards |
| GitHub: `anthropics/*` | Code | SDKs, cookbook, model-spec |
| PDF Model Cards | PDFs | Claude 3, Claude 3.5 model cards |

---

## Knowledge Taxonomy

Every document gets tagged with:

```json
{
  "domain": "model_capabilities",
  "subdomain": "tool_use",
  "capability_tags": ["function_calling", "json_mode", "streaming"],
  "model_versions": ["claude-3-5-sonnet", "claude-opus-4"],
  "content_type": "documentation",
  "audience": "developer",
  "importance_score": 9,
  "summary": "...",
  "key_facts": ["..."]
}
```

**Domains:**
- `model_capabilities` — Vision, tool use, computer use, coding, reasoning
- `safety_and_alignment` — Constitutional AI, RSP, ASL levels, policies
- `api_and_integration` — REST API, SDKs, Bedrock, Vertex AI
- `products` — Claude.ai, Pro/Team/Enterprise, Claude Code, mobile
- `research` — Papers, interpretability, scaling laws
- `prompt_engineering` — System prompts, techniques, templates

---

## Configuration

All settings are in `config/settings.py` and can be overridden via `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
CATEGORIZATION_MODEL=claude-haiku-4-5-20251001   # Fast for bulk ops
QUERY_MODEL=claude-sonnet-4-20250514              # Smart for Q&A
SQLITE_PATH=./anthropic_kb.db
CHROMA_DIR=./chroma_db
BATCH_SIZE=10
LOG_LEVEL=INFO
```

For PostgreSQL (production):
```env
USE_POSTGRES=true
POSTGRES_DSN=postgresql://user:pass@localhost:5432/anthropic_kb
```

---

## File Structure

```
anthropic_kb/
├── orchestrator.py          # Master coordinator
├── scheduler.py             # Automated update scheduler
├── setup.py                 # Setup and dependency checker
├── requirements.txt         # Python dependencies
│
├── agents/
│   ├── ingestion_agent.py   # Web scraper and document fetcher
│   ├── categorization_agent.py  # Claude-powered tagger
│   └── query_agent.py       # RAG-powered Q&A engine
│
├── database/
│   ├── db_manager.py        # Database abstraction layer
│   └── schema.sql           # PostgreSQL schema (full)
│
├── config/
│   └── settings.py          # All configuration
│
└── utils/
    └── logger.py            # Shared logging setup
```

---

## Extending the System

### Add new sources
In `agents/ingestion_agent.py`, add URLs to `ANTHROPIC_SOURCES`:
```python
"documentation": [
    "https://docs.anthropic.com/new-page",
    ...
]
```

### Add custom categories
In `agents/categorization_agent.py`, extend `DOMAIN_TAXONOMY`:
```python
"your_domain": ["tag1", "tag2", "tag3"]
```

### Build a REST API
```python
from fastapi import FastAPI
from orchestrator import OrchestratorAgent

app = FastAPI()
kb = OrchestratorAgent(load_config())

@app.get("/query")
async def query(q: str):
    return {"answer": await kb.query(q)}

@app.get("/search")  
async def search(q: str, domain: str = None):
    return await kb.query_agent.search(q, domain)
```

---

## License

MIT — use freely for personal and commercial projects.
