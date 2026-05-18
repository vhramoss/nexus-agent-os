from nexus_os.core.agent_state import AgentState
from nexus_os.core.security.guarded import guarded
from nexus_os.core.security.capabilities import Capability
from nexus_os.core.observability.decorators import traced_node


def build_response(goal: str, context: str, analysis: str, tool_result: str) -> str:
    return (
        "[MULTI-AGENT RESPONSE]\n\n"
        f"Context:\n{context}\n\n"
        f"Analysis:\n{analysis}\n\n"
        f"Tool result:\n{tool_result}\n\n"
        f"Goal:\n{goal}"
    )


@guarded(Capability.USE_LLM)
@traced_node("llm")
def llm_node(state: AgentState) -> AgentState:
    tracer = state.tracer
    event_bus = tracer.event_bus

    state.steps.append("LLM final synthesis")

    analysis = state.analysis or "No analysis available"
    tool_result = state.tool_result or "No tool execution"

    context = "\n".join(
        r.get("text", "")
        for r in state.semantic_recall
        if r.get("text")
    ) if state.semantic_recall else ""

    state.llm_output = build_response(
        state.goal,
        context,
        analysis,
        tool_result,
    )

    event_bus.publish(
        "llm.generated",
        {
            "trace_id": tracer.trace_id,
            "component": "llm",
            "status": "generated",
            "metadata": {
                "has_context": bool(context),
                "has_analysis": bool(state.analysis),
                "has_tool_result": bool(state.tool_result),
            },
        },
    )

    return state
