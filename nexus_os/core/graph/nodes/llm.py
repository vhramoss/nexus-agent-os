from nexus_os.core.agent_state import AgentState


def llm_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("llm"):
        state.steps.append("LLM final synthesis")

        context = "\n".join(
            r.get("text", "") for r in state.semantic_recall
        ) if state.semantic_recall else ""

        state.llm_output = (
            "[MULTI-AGENT RESPONSE]\n\n"
            f"Context:\n{context}\n\n"
            f"Analysis:\n{state.analysis}\n\n"
            f"Tool result:\n{state.tool_result}\n\n"
            f"Goal:\n{state.goal}"
        )

        tracer.event_bus.publish(
            "llm.generated",
            {
                "trace_id": tracer.trace_id,
                "has_context": bool(context),
                "has_analysis": bool(state.analysis),
                "has_tool_result": bool(state.tool_result),
            },
        )

    return state