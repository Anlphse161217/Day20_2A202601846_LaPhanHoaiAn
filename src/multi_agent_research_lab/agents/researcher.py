"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Fetch search results and update research notes."""
        from multi_agent_research_lab.services.search_client import SearchClient
        
        client = SearchClient()
        sources = client.search(state.request.query)
        state.sources.extend(sources)
        state.research_notes = f"Found {len(sources)} sources. Key insight: {sources[0].snippet}"
        return state
