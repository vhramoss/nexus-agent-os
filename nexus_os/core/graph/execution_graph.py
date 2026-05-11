from langgraph.graph import StateGraph, END
from nexus_os.core.agent_state import AgentState, AgentStatus


def initialize_node(state: AgentState) -> AgentState:
    state.steps.append("Graph: initialize")
    return state

def decision_node(state: AgentState) -> AgentState:
    """
        Decide qual caminho seguir com base no objetivo.
        """
    if len(state.goal) < 30:
        state.steps.append("Decision: simple path")
        state.route = "simple"
        return state
    else:
        state.steps.append("Decision: complex path")
        state.route = "complex"
        return state
    
def simple_process_node(state: AgentState) -> AgentState:
    state.steps.append("Simple processing executed")
    return state

def complex_process_node(state: AgentState) -> AgentState:
    state.steps.append("Complex processing executed")
    return state

def build_execution_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("initialize", initialize_node)
    graph.add_node("decision", decision_node)
    graph.add_node("simple_process", simple_process_node)
    graph.add_node("complex_process", complex_process_node)

    graph.set_entry_point("initialize")
    graph.add_edge("initialize", "decision")
    graph.add_conditional_edges("decision", lambda state: state.route, {
        "simple": "simple_process",
        "complex": "complex_process",
    })

    graph.add_edge("simple_process", END)
    graph.add_edge("complex_process", END)

    return graph.compile()