from nexus_os.core.agent_state import AgentState
from nexus_os.observability.decorators import traced_node


@traced_node("initialize")
def initialize_node(state: AgentState) -> AgentState:
    state.steps.append("Graph: initialize")
    return state
