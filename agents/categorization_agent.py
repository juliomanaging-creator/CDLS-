"""
Universal Categorization Agent
Classifies arbitrary topics, extracts key concept tags, and summarizes
documents locally using statistical frequency and heuristic domain matching.
"""

import logging
import re
from collections import Counter
from datetime import datetime
from typing import Any

try:
    from logger import setup_logger  # type: ignore
    logger = setup_logger("categorization_agent")
except ImportError:
    try:
        from utils.logger import setup_logger  # type: ignore
        logger = setup_logger("categorization_agent")
    except ImportError:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("categorization_agent")

STOPWORDS = {
    "the", "and", "to", "of", "a", "in", "is", "that", "for", "it", "as", "was",
    "with", "on", "are", "by", "this", "be", "or", "from", "at", "an", "your",
    "all", "have", "new", "more", "can", "will", "about", "use", "into", "their",
    "which", "also", "then", "some", "them", "these", "other", "its",
    "than", "such", "there", "what", "so", "up", "out", "if", "when", "how", "they"
}

TAXONOMY_DOMAINS = {
    "technology_and_software": [
        "software", "api", "code", "python", "database", "git", "vector",
        "algorithm", "backend", "frontend", "architecture", "docker", "llm", "rag"
    ],
    "energy_and_infrastructure": [
        "energy", "grid", "battery", "storage", "nevi", "solar", "power",
        "megawatt", "ev", "charging", "infrastructure", "transmission", "utility"
    ],
    "logistics_and_transport": [
        "logistics", "freight", "fleet", "vehicle", "transit", "carrier",
        "shipping", "supply", "dispatch", "automotive", "dealership", "inventory"
    ],
    "finance_and_economics": [
        "finance", "credit", "rate", "loan", "portfolio", "margin", "capital",
        "underwriting", "yield", "balance", "risk", "revenue", "equity", "debt"
    ],
    "policy_and_legal": [
        "statute", "compliance", "policy", "regulation", "legal", "clause",
        "contract", "governance", "audit", "liability", "jurisdiction"
    ],
    "science_and_research": [
        "research", "paper", "experiment", "hypothesis", "analysis", "biology",
        "physics", "chemistry", "evaluation", "methodology", "empirical"
    ],
}


class CategorizationAgent:
    """Universal document categorizer operating locally on CPU."""

    def __init__(self, config: dict):
        self.config = config
        self.model = "local-universal-heuristics"
        logger.info("CategorizationAgent initialized in UNIVERSAL offline mode.")

    async def categorize(self, document: dict) -> dict:
        try:
            return self._universal_classify(document)
        except Exception as e:
            logger.error(f"Categorization error for {document.get('url', 'unknown')}: {e}")
            return self._safe_default(document)

    def _universal_classify(self, document: dict) -> dict:
        url = str(document.get("url", "")).lower()
        title = str(document.get("title", "")).lower()
        raw_content = str(document.get("content", ""))
        content = raw_content.lower()
        full_text = f"{title} {content[:6000]}"

        words = re.findall(r"\b[a-z]{3,20}\b", full_text)
        filtered = [w for w in words if w not in STOPWORDS and not w.isdigit()]
        counts = Counter(filtered)
        extracted_tags = [w for w, _ in counts.most_common(12)]

        domain_scores = {d: 0 for d in TAXONOMY_DOMAINS}
        for domain, keywords in TAXONOMY_DOMAINS.items():
            for kw in keywords:
                if kw in full_text:
                    domain_scores[domain] += 1

        best_domain = max(domain_scores.keys(), key=lambda k: domain_scores[k])
        domain = best_domain if domain_scores[best_domain] > 0 else "general_research"

        model_versions: list[str] = []
        for pattern in ["claude-3-5", "claude-3", "gpt-4", "llama", "deepseek", "gemini"]:
            if pattern in full_text:
                model_versions.append(pattern)

        sentences = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", raw_content)
            if len(s.strip()) > 30 and not s.strip().startswith("<")
        ]
        if sentences:
            candidate = " ".join(sentences[:2])
            summary = candidate[:277] + "..." if len(candidate) > 280 else candidate
        else:
            summary = str(document.get("title") or "No readable text.")

        content_type = document.get("doc_type", "article")
        if "github" in url or "code" in extracted_tags:
            content_type = "technical_repository"
        elif "paper" in full_text[:400] or "abstract" in full_text[:400]:
            content_type = "academic_research"

        importance = min(5 + len(extracted_tags) // 2, 10)

        document.update({
            "domain": domain,
            "subdomain": extracted_tags[0] if extracted_tags else "overview",
            "capability_tags": extracted_tags,
            "model_versions": model_versions,
            "content_type": content_type,
            "summary": summary,
            "key_facts": extracted_tags[:5],
            "importance_score": importance,
            "categorized_at": datetime.now().isoformat(),
            "categorization_method": "universal_heuristic_engine",
        })
        return document

    def _safe_default(self, document: dict) -> dict:
        document.update({
            "domain": "general_research",
            "subdomain": "overview",
            "capability_tags": [],
            "model_versions": [],
            "content_type": document.get("doc_type", "document"),
            "summary": str(document.get("content", ""))[:200] + "...",
            "key_facts": [],
            "importance_score": 5,
            "categorized_at": datetime.now().isoformat(),
            "categorization_method": "emergency_default",
        })
        return document

    async def batch_categorize(self, documents: list, batch_size: int = 10) -> list:
        results = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            batch_results = [await self.categorize(d) for d in batch]
            results.extend(batch_results)
            logger.info(f"Categorized {len(results)}/{len(documents)} documents.")
        return results