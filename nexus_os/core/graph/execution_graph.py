from langgraph.graph import StateGraph, END
from nexus_os.core.agent_state import AgentState

from .nodes.base import initialize_node
from .nodes.recall import recall_memory_node, rag_recall_node
from .nodes.planner import planner_agent_node
from .nodes.executor import executor_agent_node
from .nodes.analyst import analyst_agent_node
from .nodes.tool import tool_agent_node
from .nodes.reviewer import reviewer_agent_node
from .nodes.llm import llm_node
from .nodes.fallback import fallback_node

from .policies.retry import retry_policy
from .policies.routing import routing_policy


def build_execution_graph():
    graph = StateGraph(AgentState)

    # --------------------------------------------------
    # Registro dos nós
    # --------------------------------------------------

    graph.add_node("initialize", initialize_node)
    graph.add_node("recall", recall_memory_node)
    graph.add_node("rag", rag_recall_node)

    graph.add_node("planner", planner_agent_node)
    graph.add_node("executor", executor_agent_node)
    graph.add_node("analyst", analyst_agent_node)
    graph.add_node("tool", tool_agent_node)
    graph.add_node("reviewer", reviewer_agent_node)
    graph.add_node("llm", llm_node)
    graph.add_node("fallback", fallback_node)

    # --------------------------------------------------
    # Entrada
    # --------------------------------------------------

    graph.set_entry_point("initialize")

    # --------------------------------------------------
    # Cadeia de memória
    # --------------------------------------------------

    graph.add_edge("initialize", "recall")
    graph.add_edge("recall", "rag")

    # --------------------------------------------------
    # DECISÃO (POLICY)
    # --------------------------------------------------

    graph.add_conditional_edges(
        "rag",
        routing_policy,
        {
            "direct": "llm",
            "plan": "planner",
        },
    )

    # --------------------------------------------------
    # Retry do planner
    # --------------------------------------------------

    graph.add_conditional_edges(
        "planner",
        lambda s: retry_policy(
            s.planner_failed,
            s.planner_retries,
            s.max_retries,
        ),
        {
            "retry": "planner",
            "next": "executor",
            "fallback": "fallback",
        },
    )

    # --------------------------------------------------
    # Pipeline de especialistas
    # --------------------------------------------------

    graph.add_edge("executor", "analyst")
    graph.add_edge("analyst", "tool")
    graph.add_edge("tool", "reviewer")
    graph.add_edge("reviewer", "llm")

    # --------------------------------------------------
    # Finalização
    # --------------------------------------------------

    graph.add_edge("llm", END)
    graph.add_edge("fallback", END)

    return graph.compile()