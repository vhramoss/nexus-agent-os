from nexus_os.core.agent_state import AgentState

def executor_agent_node(state: AgentState) -> AgentState:
    state.steps.append("Executor agent")

    if state.executor_retries < state.max_retries:
        state.executor_retries += 1
        state.executor_failed = True
        state.steps.append(f"Executor failed (retry {state.executor_retries})")
        return state

    state.executor_failed = False
    state.execution_result = [
        f"Executed: {step}" for step in state.plan.get("steps", [])
    ]
    state.steps.append("Executor succeeded")
    return state