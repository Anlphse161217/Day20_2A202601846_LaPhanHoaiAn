"""LangGraph workflow skeleton."""

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> object:
        """Create a LangGraph graph."""
        from langgraph.graph import StateGraph, END
        from multi_agent_research_lab.agents.supervisor import SupervisorAgent
        from multi_agent_research_lab.agents.researcher import ResearcherAgent
        from multi_agent_research_lab.agents.analyst import AnalystAgent
        from multi_agent_research_lab.agents.writer import WriterAgent

        workflow = StateGraph(ResearchState)
        
        workflow.add_node("supervisor", SupervisorAgent().run)
        workflow.add_node("researcher", ResearcherAgent().run)
        workflow.add_node("analyst", AnalystAgent().run)
        workflow.add_node("writer", WriterAgent().run)

        workflow.set_entry_point("supervisor")
        
        def supervisor_router(state: ResearchState) -> str:
            return state.route_history[-1] if state.route_history else "done"

        workflow.add_conditional_edges(
            "supervisor",
            supervisor_router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "done": END
            }
        )

        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")

        return workflow.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        result = app.invoke(state)
        return ResearchState(**result)
