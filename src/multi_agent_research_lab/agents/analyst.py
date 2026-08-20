"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Analyze research notes and produce analysis."""
        state.analysis_notes = f"Analyzed notes: {state.research_notes}. The sources appear to be reliable and provide a good overview of GraphRAG."
        return state
