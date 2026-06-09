from nexus_os.core.agent_state import AgentState
from nexus_os.observability.decorators import traced_node


@traced_node("fallback")
def fallback_node(state: AgentState) -> AgentState:
    tracer = state.tracer
    event_bus = tracer.event_bus

    state.steps.append("Global fallback executed")

    event_bus.publish(
        "fallback.executed",
        {
            "trace_id": tracer.trace_id,
            "component": "runtime",
            "status": "fallback",
        },
    )

    state.llm_output = "[GLOBAL FALLBACK]\nExecution completed via fallback."

    return state
