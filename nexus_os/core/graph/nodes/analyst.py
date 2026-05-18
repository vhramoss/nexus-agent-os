from nexus_os.core.agent_state import AgentState
from nexus_os.core.observability.decorators import traced_node


@traced_node("analyst")
def analyst_agent_node(state: AgentState) -> AgentState:
    state.steps.append("Analyst agent")

    state.analysis = "Analysis of execution:\n" + "\n".join(state.execution_result)

    return state
