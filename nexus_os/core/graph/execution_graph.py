from langgraph.graph import StateGraph, END
from nexus_os.core.agent_state import AgentState


# =========================================================
# Nós do grafo
# =========================================================

def initialize_node(state: AgentState) -> AgentState:
    state.steps.append("Graph: initialize")
    return state


def decision_node(state: AgentState) -> AgentState:
    """
    Decide o caminho do grafo com base no objetivo.
    """
    if len(state.goal) < 30:
        state.route = "simple"
        state.steps.append("Decision: simple path")
    else:
        state.route = "complex"
        state.steps.append("Decision: complex path")

    return state


def simple_process_node(state: AgentState) -> AgentState:
    state.steps.append("Simple processing executed")
    return state


def complex_process_node(state: AgentState) -> AgentState:
    state.steps.append("Complex processing executed")
    return state


# =========================================================
# LLM STUB com retry controlado (SEM exceção)
# =========================================================

def llm_node(state: AgentState) -> AgentState:
    state.steps.append("LLM: attempt")

    # Simula falha controlada
    if state.retries < state.max_retries:
        state.retries += 1
        state.llm_failed = True
        state.steps.append(f"LLM failed (retry {state.retries})")
        return state

    # Sucesso após retries
    state.llm_failed = False
    state.llm_output = (
        "[SIMULATED LLM RESPONSE]\n"
        f"Objetivo: {state.goal}\n"
        "Resposta gerada após retries."
    )
    state.steps.append("LLM succeeded")

    return state


# =========================================================
# Fallback (quando retries se esgotam)
# =========================================================

def fallback_node(state: AgentState) -> AgentState:
    state.steps.append("Fallback executed")

    state.llm_output = (
        "[FALLBACK RESPONSE]\n"
        "Não foi possível gerar resposta com o LLM.\n"
        "Resposta padrão retornada."
    )

    return state


# =========================================================
# Construção do grafo com retry + fallback
# =========================================================

def build_execution_graph():
    graph = StateGraph(AgentState)

    # Registro dos nós
    graph.add_node("initialize", initialize_node)
    graph.add_node("decision", decision_node)
    graph.add_node("simple_process", simple_process_node)
    graph.add_node("complex_process", complex_process_node)
    graph.add_node("llm", llm_node)
    graph.add_node("fallback", fallback_node)

    # Ponto de entrada
    graph.set_entry_point("initialize")

    # Fluxo inicial
    graph.add_edge("initialize", "decision")

    # Ramificação por tipo de tarefa
    graph.add_conditional_edges(
        "decision",
        lambda state: state.route,
        {
            "simple": "simple_process",
            "complex": "complex_process",
        },
    )

    # Caminho até o LLM
    graph.add_edge("simple_process", "llm")
    graph.add_edge("complex_process", "llm")

    # Retry + fallback controlados pelo estado
    graph.add_conditional_edges(
        "llm",
        lambda state: (
            "retry"
            if state.llm_failed and state.retries < state.max_retries
            else "fallback"
            if state.llm_failed
            else "end"
        ),
        {
            "retry": "llm",
            "fallback": "fallback",
            "end": END,
        },
    )

    # Finalização
    graph.add_edge("fallback", END)

    return graph.compile()