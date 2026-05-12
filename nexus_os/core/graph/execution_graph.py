from langgraph.graph import StateGraph, END
from nexus_os.core.agent_state import AgentState
from nexus_os.core.memory.memory_store import MemoryStore
from nexus_os.core.memory.vector_store import VectorStore


# =========================================================
# Inicialização das memórias
# =========================================================

memory_store = MemoryStore()
vector_store = VectorStore()


# =========================================================
# Nós do grafo
# =========================================================

def initialize_node(state: AgentState) -> AgentState:
    state.steps.append("Graph: initialize")
    return state


# -------------------------
# Recall estrutural (memória bruta)
# -------------------------

def recall_memory_node(state: AgentState) -> AgentState:
    state.steps.append("Recall memory")

    history = memory_store.load_all()

    related = [
        record for record in history
        if record.get("goal") == state.goal
    ]

    state.recall = related[-3:]  # últimas 3 execuções
    return state


# -------------------------
# RAG semântico (embeddings)
# -------------------------

def rag_recall_node(state: AgentState) -> AgentState:
    state.steps.append("RAG recall")

    results = vector_store.search(
        query=state.goal,
        k=3
    )

    state.semantic_recall = results
    return state


# -------------------------
# Decisão
# -------------------------

def decision_node(state: AgentState) -> AgentState:
    # Prioriza conhecimento semântico
    if state.semantic_recall:
        state.route = "simple"
        state.steps.append("Decision: semantic recall hit")
        return state

    # Depois memória estrutural
    if state.recall:
        state.route = "simple"
        state.steps.append("Decision: reused past knowledge")
        return state

    # Fallback heurístico
    if len(state.goal) < 30:
        state.route = "simple"
        state.steps.append("Decision: simple path")
    else:
        state.route = "complex"
        state.steps.append("Decision: complex path")

    return state


# -------------------------
# Processamento
# -------------------------

def simple_process_node(state: AgentState) -> AgentState:
    state.steps.append("Simple processing executed")
    return state


def complex_process_node(state: AgentState) -> AgentState:
    state.steps.append("Complex processing executed")
    return state


# -------------------------
# LLM STUB com retry (sem exceção)
# -------------------------

def llm_node(state: AgentState) -> AgentState:
    state.steps.append("LLM: attempt")

    if state.retries < state.max_retries:
        state.retries += 1
        state.llm_failed = True
        state.steps.append(f"LLM failed (retry {state.retries})")
        return state

    # Sucesso
    state.llm_failed = False

    semantic_context = "\n".join(
        r["text"] for r in state.semantic_recall
    ) if state.semantic_recall else ""

    state.llm_output = (
        "[SIMULATED RAG RESPONSE]\n\n"
        f"Contexto recuperado:\n{semantic_context}\n\n"
        f"Objetivo atual: {state.goal}"
    )

    state.steps.append("LLM succeeded")
    return state


# -------------------------
# Fallback final
# -------------------------

def fallback_node(state: AgentState) -> AgentState:
    state.steps.append("Fallback executed")

    state.llm_output = (
        "[FALLBACK RESPONSE]\n"
        "Não foi possível gerar resposta com o LLM.\n"
        "Resposta padrão retornada."
    )

    return state


# =========================================================
# Construção do grafo
# =========================================================

def build_execution_graph():
    graph = StateGraph(AgentState)

    # Registro dos nós
    graph.add_node("initialize", initialize_node)
    graph.add_node("recall_memory", recall_memory_node)
    graph.add_node("rag_recall", rag_recall_node)
    graph.add_node("decision", decision_node)
    graph.add_node("simple_process", simple_process_node)
    graph.add_node("complex_process", complex_process_node)
    graph.add_node("llm", llm_node)
    graph.add_node("fallback", fallback_node)

    # Entrada
    graph.set_entry_point("initialize")

    # Cadeia de memória
    graph.add_edge("initialize", "recall_memory")
    graph.add_edge("recall_memory", "rag_recall")
    graph.add_edge("rag_recall", "decision")

    # Ramificação por decisão
    graph.add_conditional_edges(
        "decision",
        lambda state: state.route,
        {
            "simple": "simple_process",
            "complex": "complex_process",
        },
    )

    # Execução
    graph.add_edge("simple_process", "llm")
    graph.add_edge("complex_process", "llm")

    # Retry + fallback
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

    graph.add_edge("fallback", END)

    return graph.compile()