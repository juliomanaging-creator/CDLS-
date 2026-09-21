"""
Categorization Agent
Uses Claude API to intelligently tag, summarize, and classify
every ingested Anthropic document. Runs in parallel batches.
"""

import anthropic
import json
import re
from utils.logger import setup_logger

logger = setup_logger("categorization_agent")

# Master taxonomy for Anthropic knowledge
DOMAIN_TAXONOMY = {
    "model_capabilities": [
        "vision", "tool_use", "computer_use", "code_generation", "reasoning",
        "multilingual", "long_context", "streaming", "batch_processing",
        "embeddings", "function_calling", "json_mode", "prompt_caching",
    ],
    "safety_and_alignment": [
        "constitutional_ai", "rlhf", "harmlessness", "helpfulness", "honesty",
        "responsible_scaling", "interpretability", "red_teaming", "model_cards",
        "usage_policies", "asl_levels",
    ],
    "api_and_integration": [
        "rest_api", "python_sdk", "typescript_sdk", "amazon_bedrock",
        "vertex_ai", "google_cloud", "rate_limits", "pricing", "authentication",
        "error_handling", "webhooks", "batch_api",
    ],
    "products": [
        "claude_ai", "claude_pro", "claude_team", "claude_enterprise",
        "claude_code", "claude_in_chrome", "api_platform", "mobile_app",
        "artifacts", "projects", "memory",
    ],
    "research": [
        "papers", "interpretability", "scaling_laws", "mechanistic_interpretability",
        "sparse_autoencoders", "superposition", "in_context_learning",
        "chain_of_thought", "emergent_capabilities",
    ],
    "prompt_engineering": [
        "system_prompts", "few_shot", "chain_of_thought", "xml_tags",
        "role_playing", "output_formatting", "context_window", "temperature",
    ],
}

CATEGORIZATION_PROMPT = """You are an expert knowledge classifier for Anthropic's AI systems.

Analyze this document and return a JSON object with the following structure:

{
  "domain": "<primary domain from: model_capabilities|safety_and_alignment|api_and_integration|products|research|prompt_engineering|company_info|other>",
  "subdomain": "<specific subdomain within the domain>",
  "capability_tags": ["<list of specific capabilities or topics covered>"],
  "model_versions": ["<list of Claude model versions mentioned, e.g. claude-3-opus, claude-sonnet-4, etc>"],
  "content_type": "<documentation|research_paper|blog_post|release_note|policy|tutorial|reference|interview>",
  "summary": "<2-3 sentence summary of what this document covers>",
  "key_facts": ["<list of 3-5 important specific facts, numbers, or claims>"],
  "audience": "<developer|researcher|end_user|enterprise|general>",
  "importance_score": <1-10 score for how central this is to Anthropic knowledge>,
  "date_context": "<any dates or version info mentioned>"
}

Document Title: {title}
Source URL: {url}
Source Category: {source_category}

Document Content (first 3000 chars):
{content}

Return ONLY valid JSON, no markdown, no explanation."""


class CategorizationAgent:
    """
    Uses Claude API to classify and enrich each ingested document.
    Adds semantic tags, summaries, and structured metadata.
    """

    def __init__(self, config: dict):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.get("anthropic_api_key"))
        self.model = config.get("categorization_model", "claude-haiku-4-5-20251001")

    async def categorize(self, document: dict) -> dict:
        """
        Categorize a single document using Claude.
        Returns the document enriched with categorization metadata.
        """
        try:
            content_preview = document["content"][:3000]
            prompt = CATEGORIZATION_PROMPT.format(
                title=document["title"],
                url=document["url"],
                source_category=document["source_category"],
                content=content_preview,
            )

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            categorization = self._parse_json_response(response_text)

            # Enrich document with categorization results
            document.update({
                "domain": categorization.get("domain", "other"),
                "subdomain": categorization.get("subdomain", ""),
                "capability_tags": categorization.get("capability_tags", []),
                "model_versions": categorization.get("model_versions", []),
                "content_type": categorization.get("content_type", "documentation"),
                "summary": categorization.get("summary", ""),
                "key_facts": categorization.get("key_facts", []),
                "audience": categorization.get("audience", "general"),
                "importance_score": categorization.get("importance_score", 5),
                "date_context": categorization.get("date_context", ""),
                "categorized_at": __import__("datetime").datetime.now().isoformat(),
            })

            logger.debug(f"Categorized: [{document['domain']}] {document['title'][:60]}")
            return document

        except anthropic.APIError as e:
            logger.error(f"Claude API error categorizing {document['url']}: {e}")
            return self._fallback_categorization(document)
        except Exception as e:
            logger.error(f"Categorization error for {document['url']}: {e}")
            return self._fallback_categorization(document)

    def _parse_json_response(self, text: str) -> dict:
        """Parse JSON from Claude's response, handling edge cases."""
        # Strip markdown fences if present
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise

    def _fallback_categorization(self, document: dict) -> dict:
        """
        Rule-based fallback categorization when Claude API is unavailable.
        Uses URL patterns and keywords to assign categories.
        """
        url = document["url"].lower()
        content = document["content"].lower()

        domain = "other"
        tags = []

        if "docs.anthropic.com" in url:
            domain = "api_and_integration"
            if "prompt" in url or "prompt" in content[:500]:
                domain = "prompt_engineering"
        elif "research" in url or "paper" in content[:200]:
            domain = "research"
        elif "safety" in url or "policy" in url:
            domain = "safety_and_alignment"
        elif "product" in url or "claude.ai" in url:
            domain = "products"

        # Extract model version mentions
        model_versions = []
        model_patterns = [
            "claude-3-opus", "claude-3-sonnet", "claude-3-haiku",
            "claude-3-5-sonnet", "claude-opus-4", "claude-sonnet-4",
            "claude-haiku-4", "claude 2", "claude instant",
        ]
        for model in model_patterns:
            if model in content:
                model_versions.append(model)

        document.update({
            "domain": domain,
            "subdomain": "",
            "capability_tags": tags,
            "model_versions": model_versions,
            "content_type": "documentation",
            "summary": document["content"][:300] + "...",
            "key_facts": [],
            "audience": "developer",
            "importance_score": 5,
            "date_context": "",
            "categorized_at": __import__("datetime").datetime.now().isoformat(),
            "categorization_method": "fallback_rules",
        })

        return document

    async def batch_categorize(self, documents: list, batch_size: int = 5) -> list:
        """Categorize multiple documents with rate limiting."""
        results = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            batch_results = [await self.categorize(doc) for doc in batch]
            results.extend(batch_results)
            logger.info(f"Batch {i//batch_size + 1} complete ({len(results)}/{len(documents)})")
        return results
