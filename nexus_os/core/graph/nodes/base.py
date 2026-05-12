from nexus_os.core.agent_state import AgentState


def initialize_node(state: AgentState) -> AgentState:
    state.steps.append("Graph: initialize")
    return state


def simple_process_node(state: AgentState) -> AgentState:
    state.steps.append("Simple processing executed")
    return state


def complex_process_node(state: AgentState) -> AgentState:
    state.steps.append("Complex processing executed")
    return state