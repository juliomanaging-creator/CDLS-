"""
Configuration Settings
Central config management for the Anthropic Knowledge Base system.
Edit settings here or override via environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def load_config() -> dict:
    """Load and return the full system configuration."""
    return {
        # ── Anthropic API ───────────────────────────────────────────
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),

        # Models to use for each agent role
        "categorization_model": os.getenv(
            "CATEGORIZATION_MODEL", "claude-haiku-4-5-20251001"
        ),  # Fast + cheap for bulk categorization
        "query_model": os.getenv(
            "QUERY_MODEL", "claude-sonnet-4-20250514"
        ),  # Smart for Q&A synthesis

        # ── Database ────────────────────────────────────────────────
        "database": {
            "use_postgres": os.getenv("USE_POSTGRES", "false").lower() == "true",
            "postgres_dsn": os.getenv(
                "POSTGRES_DSN",
                "postgresql://" + os.getenv("DB_USER", "user") + ":" + os.getenv("DB_PASS", "pass") + "@localhost:5432/anthropic_kb",
                ),
            "sqlite_path": os.getenv("SQLITE_PATH", "./anthropic_kb.db"),
            "chroma_persist_dir": os.getenv("CHROMA_DIR", "./chroma_db"),
        },

        # ── Scraping ────────────────────────────────────────────────
        "scrape_timeout": int(os.getenv("SCRAPE_TIMEOUT", "30")),
        "max_crawl_depth": int(os.getenv("MAX_CRAWL_DEPTH", "3")),
        "respect_robots_txt": os.getenv("RESPECT_ROBOTS", "true").lower() == "true",
        "scrape_delay_seconds": float(os.getenv("SCRAPE_DELAY", "0.5")),

        # ── Pipeline ────────────────────────────────────────────────
        "batch_size": int(os.getenv("BATCH_SIZE", "10")),
        "max_context_docs": int(os.getenv("MAX_CONTEXT_DOCS", "8")),

        # ── Sources ─────────────────────────────────────────────────
        "sources": {
            "urls": [
                # Documentation
                "https://docs.anthropic.com",
                "https://support.anthropic.com",
                # Main site
                "https://www.anthropic.com/research",
                "https://www.anthropic.com/news",
                "https://www.anthropic.com/safety",
                # Products
                "https://www.anthropic.com/claude",
                "https://www.anthropic.com/api",
                # GitHub
                "https://github.com/anthropics/anthropic-cookbook",
                "https://github.com/anthropics/anthropic-sdk-python",
                "https://github.com/anthropics/model-spec",
            ],
            "sitemaps": [
                "https://docs.anthropic.com/sitemap.xml",
                "https://www.anthropic.com/sitemap.xml",
            ],
        },

        # ── Scheduling ──────────────────────────────────────────────
        "schedule": {
            "full_rebuild_day": "sunday",
            "full_rebuild_hour": 2,
            "incremental_hour": 0,
            "news_check_interval_hours": 6,
        },

        # ── Output ──────────────────────────────────────────────────
        "export_path": os.getenv("EXPORT_PATH", "./kb_export.json"),
        "report_path": os.getenv("REPORT_PATH", "./kb_summary_report.json"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }
 # pyright: ignore[reportCallIssue]