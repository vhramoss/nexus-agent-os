from nexus_os.core.agent_state import AgentState


def llm_node(state: AgentState) -> AgentState:
    state.steps.append("LLM final synthesis")

    context = "\n".join(
        r.get("text", "") for r in state.semantic_recall
    ) if state.semantic_recall else ""

    state.llm_output = (
        "[MULTI‑AGENT RESPONSE]\n\n"
        f"Context:\n{context}\n\n"
        f"Analysis:\n{state.analysis}\n\n"
        f"Tool result:\n{state.tool_result}\n\n"
        f"Goal:\n{state.goal}"
    )
    return state