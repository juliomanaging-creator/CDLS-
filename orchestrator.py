"""
Orchestrator Agent
Coordinates universal ingestion, categorization, database indexing,
generates a comprehensive Master Research Index, synthesizes UX findings,
compiles an IP patent disclosure Word document, and serves semantic queries.
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Optional

from agents.ingestion_agent import IngestionAgent
from agents.categorization_agent import CategorizationAgent
from agents.query_agent import QueryAgent
from agents.rd_insights_agent import RDInsightsAgent
from agents.ip_document_agent import IPDocumentAgent
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger("orchestrator")


class OrchestratorAgent:
    """Master controller for the Universal Multi-Agent RAG system."""

    def __init__(self, config: dict):
        self.config = config
        self.db = DatabaseManager(config)
        self.ingestion_agent = IngestionAgent(config)
        self.categorization_agent = CategorizationAgent(config)
        self.query_agent = QueryAgent(config, self.db)
        self.rd_insights_agent = RDInsightsAgent(config, self.db)
        self.ip_document_agent = IPDocumentAgent(config, self.db)
        self.stats = {
            "ingested": 0,
            "categorized": 0,
            "indexed": 0,
            "errors": 0,
        }

    async def initialize(self):
        await self.db.initialize()

    async def run_full_pipeline(self, custom_targets: Optional[list[str]] = None) -> dict:
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("UNIVERSAL KNOWLEDGE BASE - PIPELINE STARTING")
        logger.info("=" * 60)

        # 1. Initialize Database
        logger.info("[1/5] Initializing database schema...")
        await self.initialize()
        logger.info("      [OK] Database ready")

        # 2. Ingest Sources
        logger.info("[2/5] Starting ingestion agent...")
        raw_documents = await self.ingestion_agent.scrape_all(custom_targets)
        self.stats["ingested"] = len(raw_documents)
        logger.info(f"      [OK] Ingested {len(raw_documents)} items")

        if not raw_documents:
            logger.warning("No documents collected. Pipeline completed early.")
            return self.stats

        # 3. Categorize
        logger.info("[3/5] Starting categorization agent...")
        categorized_docs = await self.categorization_agent.batch_categorize(raw_documents)
        self.stats["categorized"] = len(categorized_docs)
        logger.info(f"      [OK] Categorized {len(categorized_docs)} items")

        # 4. Store in ChromaDB & SQLite
        logger.info("[4/5] Storing items in vector and relational databases...")
        for doc in categorized_docs:
            try:
                await self.db.store_document(doc)
                self.stats["indexed"] += 1
            except Exception as e:
                logger.error(f"Error storing document {doc.get('url')}: {e}")
                self.stats["errors"] += 1
        logger.info(f"      [OK] Stored {self.stats['indexed']} items")

        # 5. Compile Master Index, UX Findings, and IP Patent Document
        logger.info("[5/5] Generating Master Index, UX Findings, and Patent Portfolio Doc...")
        await self.generate_research_index("RESEARCH_INDEX.md")
        await self.generate_summary_report("kb_summary_report.json")
        await self.rd_insights_agent.generate_ux_findings_report("UX_RESEARCH_FINDINGS.md")
        self.ip_document_agent.generate_ip_word_doc("CDLS_IP_Patent_Portfolio_Submission.docx")
        logger.info("      [OK] Research Index, UX Report, and Patent Submission Doc generated")

        elapsed = round(time.time() - start_time, 2)
        logger.info("\n" + "=" * 60)
        logger.info(f"PIPELINE COMPLETE in {elapsed}s")
        logger.info(f"  Items ingested:        {self.stats['ingested']}")
        logger.info(f"  Items categorized:     {self.stats['categorized']}")
        logger.info(f"  Items indexed:         {self.stats['indexed']}")
        logger.info(f"  Errors:                {self.stats['errors']}")
        logger.info("=" * 60)

        return self.stats

    async def generate_research_index(self, output_path: str = "RESEARCH_INDEX.md"):
        if not self.db.sqlite_conn:
            return

        cursor = self.db.sqlite_conn.cursor()
        cursor.execute("SELECT domain, COUNT(*) FROM documents GROUP BY domain ORDER BY COUNT(*) DESC")
        domain_counts = cursor.fetchall()

        cursor.execute("""
            SELECT title, url, domain, summary, importance_score, scraped_at 
            FROM documents 
            ORDER BY domain, importance_score DESC
        """)
        all_docs = cursor.fetchall()

        lines = [
            "# Universal Research & Development Master Index",
            f"*Generated automatically on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
            "## 1. Domain Overview",
            "| Domain Category | Item Count |",
            "| :--- | :--- |",
        ]

        for domain, count in domain_counts:
            dom_name = str(domain).replace("_", " ").title() if domain else "Uncategorized"
            lines.append(f"| **{dom_name}** | {count} |")

        lines.append("\n## 2. Ingested Knowledge & Asset Catalog\n")

        current_domain = None
        for doc in all_docs:
            title, url, domain, summary, score, scraped_at = doc
            if domain != current_domain:
                current_domain = domain
                dom_title = str(domain).replace("_", " ").upper() if domain else "UNCATEGORIZED"
                lines.append(f"\n### [{dom_title}]\n")

            lines.append(f"#### {title}")
            lines.append(f"- **Source**: `{url}`")
            lines.append(f"- **Importance**: {score}/10 | **Indexed**: {str(scraped_at)[:10]}")
            lines.append(f"- **Summary**:\n  > {summary}\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    async def generate_summary_report(self, output_path: str = "kb_summary_report.json"):
        stats = await self.db.get_statistics()
        stats["generated_at"] = datetime.now().isoformat()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

    async def query(self, question: str, top_k: int = 5, domain_filter: Optional[str] = None) -> str:
        return await self.query_agent.answer(question, top_k=top_k, domain_filter=domain_filter)


async def main():
    custom_sources = [
        "./CDLS_RD_Time_Tracker_MERGED_FULL.xlsx",
        "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "https://docs.anthropic.com",
    ]

    config = {
        "sqlite_path": "./anthropic_kb.db",
        "chroma_persist_dir": "./chroma_db",
        "scrape_timeout": 25,
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    }

    orchestrator = OrchestratorAgent(config)
    await orchestrator.run_full_pipeline(custom_sources)

    print("\n" + "=" * 60)
    print("KNOWLEDGE BASE READY — Sample Query Demo")
    print("=" * 60)

    demo_query = "What technical uncertainties and experimentation were conducted for the MagSafe battery pod?"
    print(f"\nQ: {demo_query}\n")
    answer = await orchestrator.query(demo_query)
    print(f"A: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())