from nexus_os.core.graph.execution_graph import AgentState

def planner_agent_node(state: AgentState) -> AgentState:
    state.steps.append("Planner agent")

    if state.planner_retries < state.max_retries:
        state.planner_retries += 1
        state.planner_failed = True
        state.steps.append(f"Planner failed (retry {state.planner_retries})")
        return state

    state.planner_failed = False
    state.plan = {
        "steps": [
            f"Analyze goal: {state.goal}",
            "Decompose tasks",
            "Prepare execution plan",
        ]
    }
    state.steps.append("Planner succeeded")
    return state