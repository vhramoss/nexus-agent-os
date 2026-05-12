from nexus_os.core.agent_state import AgentState


def planner_agent_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("planner"):
        state.steps.append("Planner agent")

        if state.planner_retries < state.max_retries:
            state.planner_retries += 1
            state.planner_failed = True

            tracer.event_bus.publish(
                "retry.triggered",
                {
                    "trace_id": tracer.trace_id,
                    "node": "planner",
                    "attempt": state.planner_retries,
                },
            )

            return state

        state.planner_failed = False
        state.plan = {
            "steps": [
                f"Analyze goal: {state.goal}",
                "Decompose tasks",
                "Prepare execution plan",
            ]
        }

    return state
