from nexus_os.core.agent_state import AgentState
from nexus_os.core.security.agent_policy import DEFAULT_AGENT_POLICY


def initialize_state(agent, goal: str):
    state = AgentState(
        goal=goal,
        status="running",
    )

    state.capabilities = DEFAULT_AGENT_POLICY
    state.tracer = agent.tracer
    state.event_bus = agent.event_bus

    state.steps.append("Agent initialized")

    return state
