"""
Query Agent
RAG-powered agent that answers natural language questions about Anthropic
by retrieving relevant documents from the knowledge base and synthesizing answers.
"""

import anthropic
from utils.logger import setup_logger

logger = setup_logger("query_agent")

QUERY_SYSTEM_PROMPT = """You are an expert on Anthropic, Claude AI systems, and all Anthropic products and research.
You have access to a comprehensive knowledge base of Anthropic's public documentation, research papers, 
API docs, product information, and safety research.

When answering questions:
1. Be specific and accurate - cite model versions, API parameters, and exact capabilities
2. Structure your answer clearly with relevant sections
3. If something is uncertain or may have changed, say so
4. Provide practical examples where helpful
5. If asked about capabilities, be comprehensive and cover ALL relevant aspects

You represent the full depth of Anthropic's public knowledge."""

RAG_PROMPT_TEMPLATE = """Based on the following retrieved knowledge base documents, 
answer the user's question comprehensively and accurately.

RETRIEVED DOCUMENTS:
{context}

USER QUESTION: {question}

Provide a detailed, well-structured answer. If the documents don't fully cover the question, 
supplement with your general knowledge about Anthropic while clearly noting what comes from 
the retrieved documents vs general knowledge."""


class QueryAgent:
    """
    Answers questions about Anthropic using RAG over the knowledge base.
    Combines semantic search retrieval with Claude synthesis.
    """

    def __init__(self, config: dict, db_manager):
        self.config = config
        self.db = db_manager
        self.client = anthropic.Anthropic(api_key=config.get("anthropic_api_key"))
        self.model = config.get("query_model", "claude-sonnet-4-20250514")
        self.max_context_docs = config.get("max_context_docs", 8)

    async def answer(self, question: str) -> str:
        """
        Answer a question using RAG over the knowledge base.
        1. Retrieve relevant documents via semantic + keyword search
        2. Synthesize answer using Claude
        """
        logger.info(f"Query: {question[:80]}...")

        # Retrieve relevant documents
        relevant_docs = await self.db.semantic_search(
            query=question,
            top_k=self.max_context_docs,
        )

        if not relevant_docs:
            logger.warning("No relevant documents found, using pure model knowledge")
            return await self._answer_without_context(question)

        # Build context from retrieved docs
        context = self._build_context(relevant_docs)

        # Synthesize answer
        prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=QUERY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        answer = message.content[0].text
        logger.info(f"Answer generated ({len(answer)} chars, {len(relevant_docs)} docs used)")
        return answer

    async def _answer_without_context(self, question: str) -> str:
        """Fall back to pure model knowledge if no docs retrieved."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=QUERY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}],
        )
        return message.content[0].text

    def _build_context(self, documents: list) -> str:
        """Build a formatted context string from retrieved documents."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            part = f"""
--- Document {i} ---
Title: {doc.get('title', 'Unknown')}
Source: {doc.get('url', 'Unknown')}
Domain: {doc.get('domain', 'Unknown')}
Tags: {', '.join(doc.get('capability_tags', []))}
Summary: {doc.get('summary', '')}

Content:
{doc.get('content', '')[:1500]}
"""
            context_parts.append(part)
        return "\n".join(context_parts)

    async def search(self, query: str, domain: str = None, limit: int = 10) -> list:
        """
        Search the knowledge base and return matching documents.
        Optionally filter by domain.
        """
        docs = await self.db.semantic_search(query, top_k=limit, domain_filter=domain)
        return [
            {
                "title": d.get("title"),
                "url": d.get("url"),
                "domain": d.get("domain"),
                "summary": d.get("summary"),
                "tags": d.get("capability_tags", []),
                "importance": d.get("importance_score", 5),
            }
            for d in docs
        ]

    async def get_capabilities_overview(self) -> str:
        """Generate a comprehensive overview of all Claude capabilities."""
        question = """
        Provide a comprehensive, structured overview of ALL Claude capabilities including:
        1. All model versions and their specific capabilities/differences
        2. Vision and multimodal capabilities  
        3. Tool use and function calling
        4. Computer use
        5. API features (streaming, batch, caching, etc.)
        6. Context window sizes per model
        7. Languages supported
        8. Safety and constitutional AI features
        9. Integration options (Bedrock, Vertex, etc.)
        10. Products and interfaces available
        """
        return await self.answer(question)

    async def interactive_session(self):
        """Run an interactive Q&A session in the terminal."""
        print("\n" + "=" * 60)
        print("ANTHROPIC KNOWLEDGE BASE - Interactive Query Mode")
        print("Type 'quit' to exit, 'overview' for full capabilities overview")
        print("=" * 60 + "\n")

        while True:
            try:
                question = input("Your question: ").strip()
                if not question:
                    continue
                if question.lower() == "quit":
                    break
                if question.lower() == "overview":
                    answer = await self.get_capabilities_overview()
                else:
                    answer = await self.answer(question)

                print(f"\n{'─' * 60}")
                print(answer)
                print(f"{'─' * 60}\n")
            except KeyboardInterrupt:
                break

        print("Session ended.")
