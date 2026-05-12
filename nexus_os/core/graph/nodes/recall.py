from nexus_os.core.agent_state import AgentState
from nexus_os.core.memory.memory_store import MemoryStore
from nexus_os.core.memory.vector_store import VectorStore


memory_store = MemoryStore()
vector_store = VectorStore()


def recall_memory_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("recall_memory"):
        state.steps.append("Recall memory")

        history = memory_store.load_all()
        state.recall = [
            r for r in history if r.get("goal") == state.goal
        ][-3:]

    return state


def rag_recall_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("rag_recall"):
        state.steps.append("RAG recall")

        state.semantic_recall = vector_store.search(
            state.goal,
            k=3,
        )

    return state