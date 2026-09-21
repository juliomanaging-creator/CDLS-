"""
Query Agent (Offline-Capable RAG Engine)
Searches the knowledge base and generates structured answers.
Operates fully locally if no valid Anthropic API key is provided.
"""

import logging
from typing import Any, Optional

try:
    from logger import setup_logger  # type: ignore
    logger = setup_logger("query_agent")
except ImportError:
    try:
        from utils.logger import setup_logger  # type: ignore
        logger = setup_logger("query_agent")
    except ImportError:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("query_agent")


class QueryAgent:
    """
    RAG Query Agent that handles retrieval from SQLite + ChromaDB
    and synthesizes answers with an offline fallback.
    """

    def __init__(self, config: dict, db_manager: Any):
        self.config = config
        self.db = db_manager
        self.api_key: str = str(config.get("anthropic_api_key") or "")
        self.model: str = str(config.get("query_model") or "claude-haiku-4-5-20251001")
        self.client: Any = None

        if self.api_key and not self.api_key.startswith("your-") and len(self.api_key) > 20:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Anthropic client: {e}. Defaulting to offline mode.")
        else:
            logger.info("QueryAgent operating in OFFLINE extractive mode (No API key).")

    async def answer(self, question: str, top_k: int = 5, domain_filter: Optional[str] = None) -> str:
        """
        Retrieves relevant context and produces an answer.
        """
        logger.info(f"Query: {question[:80]}...")

        # 1. Semantic + keyword search via DatabaseManager
        relevant_docs = await self.db.semantic_search(
            query=question,
            top_k=top_k,
            domain_filter=domain_filter,
        )

        if not relevant_docs:
            return f"No relevant documentation found in the local knowledge base for: '{question}'."

        # 2. Online synthesis with complete error trapping
        if self.client is not None:
            try:
                context_str = "\n\n".join([
                    f"--- Source: {doc.get('title') or 'Unknown'} ({doc.get('url') or ''}) ---\n"
                    f"Domain: {doc.get('domain') or 'general'}\n"
                    f"Summary: {doc.get('summary') or ''}\n"
                    f"Excerpt: {str(doc.get('content') or '')[:1500]}"
                    for doc in relevant_docs
                ])

                prompt = (
                    f"Answer the following question based ONLY on the provided context:\n\n"
                    f"Question: {question}\n\n"
                    f"Context:\n{context_str}\n\n"
                    f"Provide a clear, detailed, and structured response with citations."
                )

                response: Any = self.client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}],
                )

                text_parts: list[str] = []
                content_blocks: list[Any] = getattr(response, "content", [])
                for block in content_blocks:
                    val = getattr(block, "text", None)
                    if isinstance(val, str):
                        text_parts.append(val)

                if text_parts:
                    return "\n".join(text_parts)
            except Exception as e:
                logger.warning(f"Remote API synthesis bypassed ({e}). Falling back to local synthesis.")

        # 3. Offline Extractive Synthesis
        return self._offline_synthesize(question, relevant_docs)

    def _offline_synthesize(self, question: str, docs: list[dict]) -> str:
        """
        Synthesizes a structured answer directly from local DB records.
        """
        output: list[str] = [
            "### Query Response (Offline Knowledge Base)",
            f"**Question:** {question}\n",
            f"Found **{len(docs)}** matching sources in the local vector and relational index:\n",
        ]

        for i, doc in enumerate(docs, 1):
            title = str(doc.get("title") or "Anthropic Documentation")
            url = str(doc.get("url") or "")
            domain = str(doc.get("domain") or "General")
            summary = str(doc.get("summary") or (str(doc.get("content") or "")[:250] + "..."))
            
            raw_tags = doc.get("capability_tags")
            tags: list[str] = [str(t) for t in raw_tags] if isinstance(raw_tags, list) else []
            tag_str = f" | Tags: `{', '.join(tags)}`" if tags else ""

            output.append(f"#### {i}. {title}")
            output.append(f"- **Domain**: `{domain}`{tag_str}")
            if url:
                output.append(f"- **Source**: [{url}]({url})")
            output.append(f"- **Summary / Key Excerpt**:\n  > {summary}\n")

        output.append("---")
        output.append("*Generated locally via Multi-Agent RAG offline retrieval.*")
        return "\n".join(output)