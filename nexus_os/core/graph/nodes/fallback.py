from nexus_os.core.agent_state import AgentState


def fallback_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("fallback"):
        state.steps.append("Global fallback executed")

        tracer.event_bus.publish(
            "fallback.executed",
            {"trace_id": tracer.trace_id},
        )

        state.llm_output = (
            "[GLOBAL FALLBACK]\n"
            "Execution completed via fallback."
        )

    return state
