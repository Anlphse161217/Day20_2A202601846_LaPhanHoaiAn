"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Generate final answer using LLM."""
        from multi_agent_research_lab.services.llm_client import LLMClient
        
        llm = LLMClient()
        system_prompt = "You are an expert technical writer. Write a comprehensive summary with citations."
        user_prompt = f"Write a final answer based on the following analysis: {state.analysis_notes}\nSources: {state.sources}"
        
        response = llm.complete(system_prompt, user_prompt)
        state.final_answer = response.content
        return state
