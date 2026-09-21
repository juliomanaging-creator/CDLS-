-- ============================================================
-- Anthropic Knowledge Base - PostgreSQL Schema
-- Run this to set up the full database structure
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "vector";     -- pgvector for embeddings (optional)

-- ── Core Documents Table ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS documents (
    id              TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    url             TEXT UNIQUE NOT NULL,
    title           TEXT,
    content         TEXT,
    content_hash    TEXT,
    doc_type        TEXT CHECK (doc_type IN ('webpage', 'pdf', 'github_repo', 'video_transcript', 'api_spec')),
    source_category TEXT,   -- documentation | research | support | github | model_cards

    -- Categorization fields (set by Categorization Agent)
    domain          TEXT,   -- model_capabilities | safety_and_alignment | api_and_integration | products | research | prompt_engineering
    subdomain       TEXT,
    content_type    TEXT,   -- documentation | research_paper | blog_post | release_note | policy | tutorial
    summary         TEXT,
    key_facts       JSONB   DEFAULT '[]',
    capability_tags TEXT[]  DEFAULT '{}',
    model_versions  TEXT[]  DEFAULT '{}',
    audience        TEXT,   -- developer | researcher | end_user | enterprise | general
    importance_score INTEGER DEFAULT 5 CHECK (importance_score BETWEEN 1 AND 10),
    date_context    TEXT,
    categorization_method TEXT DEFAULT 'claude_api',

    metadata        JSONB   DEFAULT '{}',

    -- Timestamps
    scraped_at      TIMESTAMPTZ,
    categorized_at  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ── Tags (normalized for fast tag-based queries) ────────────────────────────
CREATE TABLE IF NOT EXISTS tags (
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS document_tags (
    document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
    tag_id      INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (document_id, tag_id)
);

-- ── Model Version References ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS document_model_refs (
    id            SERIAL PRIMARY KEY,
    document_id   TEXT REFERENCES documents(id) ON DELETE CASCADE,
    model_version TEXT NOT NULL,
    UNIQUE (document_id, model_version)
);

-- ── Key Facts (for fast fact retrieval) ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS document_facts (
    id          SERIAL PRIMARY KEY,
    document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
    fact        TEXT NOT NULL,
    fact_order  INTEGER DEFAULT 0
);

-- ── Pipeline Run History ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id               SERIAL PRIMARY KEY,
    run_type         TEXT DEFAULT 'full',  -- full | incremental | news_check
    run_at           TIMESTAMPTZ DEFAULT NOW(),
    docs_ingested    INTEGER DEFAULT 0,
    docs_categorized INTEGER DEFAULT 0,
    docs_indexed     INTEGER DEFAULT 0,
    docs_updated     INTEGER DEFAULT 0,
    errors           INTEGER DEFAULT 0,
    duration_seconds REAL,
    notes            TEXT
);

-- ── Vector Embeddings (requires pgvector extension) ─────────────────────────
-- Uncomment if using pgvector instead of ChromaDB:
--
-- CREATE TABLE IF NOT EXISTS document_embeddings (
--     document_id TEXT PRIMARY KEY REFERENCES documents(id) ON DELETE CASCADE,
--     embedding   vector(1536),   -- OpenAI/Anthropic embedding dimensions
--     model_used  TEXT,
--     created_at  TIMESTAMPTZ DEFAULT NOW()
-- );
-- CREATE INDEX ON document_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ── Indexes ──────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_documents_domain        ON documents(domain);
CREATE INDEX IF NOT EXISTS idx_documents_content_type  ON documents(content_type);
CREATE INDEX IF NOT EXISTS idx_documents_importance    ON documents(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_documents_scraped_at    ON documents(scraped_at DESC);
CREATE INDEX IF NOT EXISTS idx_gin_capability_tags     ON documents USING GIN(capability_tags);
CREATE INDEX IF NOT EXISTS idx_gin_model_versions      ON documents USING GIN(model_versions);
CREATE INDEX IF NOT EXISTS idx_gin_metadata            ON documents USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_trgm_title              ON documents USING GIN(title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_trgm_summary            ON documents USING GIN(summary gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_model_refs_version      ON document_model_refs(model_version);

-- ── Full Text Search ─────────────────────────────────────────────────────────
ALTER TABLE documents ADD COLUMN IF NOT EXISTS fts_vector tsvector
    GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(summary, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(content, '')), 'C')
    ) STORED;

CREATE INDEX IF NOT EXISTS idx_fts ON documents USING GIN(fts_vector);

-- ── Useful Views ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW kb_summary AS
SELECT
    domain,
    COUNT(*) AS doc_count,
    ROUND(AVG(importance_score), 2) AS avg_importance,
    COUNT(DISTINCT unnest_tags) AS unique_tags
FROM documents, unnest(capability_tags) AS unnest_tags
GROUP BY domain
ORDER BY doc_count DESC;

CREATE OR REPLACE VIEW model_coverage AS
SELECT
    mr.model_version,
    COUNT(DISTINCT mr.document_id) AS doc_count,
    array_agg(DISTINCT d.domain) AS domains_covered
FROM document_model_refs mr
JOIN documents d ON d.id = mr.document_id
GROUP BY mr.model_version
ORDER BY doc_count DESC;

CREATE OR REPLACE VIEW top_documents AS
SELECT
    id, title, url, domain, content_type,
    capability_tags, model_versions,
    importance_score, summary, scraped_at
FROM documents
ORDER BY importance_score DESC, scraped_at DESC;

-- ── Auto-update timestamp trigger ────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Done!
COMMENT ON TABLE documents IS 'Core table: all Anthropic public knowledge documents';
COMMENT ON TABLE pipeline_runs IS 'History of all pipeline executions for auditing';
