from nexus_os.core.agent_state import AgentState


def planner_agent_node(state: AgentState) -> AgentState:
    tracer = state.tracer

    with tracer.span("planner"):
        state.steps.append("Planner agent")

        try:
            # ✅ SIMULAÇÃO DE GERAÇÃO DE PLANO (substituir por LLM depois)
            if not state.goal:
                raise ValueError("Empty goal")

            state.plan = {
                "steps": [
                    f"Analyze goal: {state.goal}",
                    "Decompose tasks",
                    "Prepare execution plan",
                ]
            }

            state.planner_failed = False

        except Exception as e:
            state.planner_retries += 1
            state.planner_failed = True

            tracer.event_bus.publish(
                "retry.triggered",
                {
                    "trace_id": tracer.trace_id,
                    "component": "planner",
                    "status": "retrying",
                    "metadata": {"attempt": state.planner_retries},
                },
            )

            return state

    return state