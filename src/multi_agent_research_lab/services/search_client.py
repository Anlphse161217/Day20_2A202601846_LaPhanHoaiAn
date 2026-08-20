"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query."""
        return [
            SourceDocument(
                title="GraphRAG Overview",
                url="https://example.com/graphrag",
                snippet=f"GraphRAG is a state-of-the-art technique combining knowledge graphs and LLMs for: {query}"
            )
        ]
