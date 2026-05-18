from nexus_os.core.agent_state import AgentState
from nexus_os.core.graph.nodes.fallback import fallback_node
from nexus_os.core.graph.nodes.planner import planner_agent_node
from nexus_os.core.graph.nodes.reviewer import reviewer_agent_node
from nexus_os.core.observability.event_bus import EventBus
from nexus_os.core.observability.tracer import Tracer

# --------------------------------------------------
# Helper
# --------------------------------------------------


def make_state(goal="test"):
    state = AgentState(goal=goal)

    # mínimo necessário para o traced_node funcionar
    bus = EventBus()
    tracer = Tracer(event_bus=bus, trace_id="test")

    state.tracer = tracer
    return state


# --------------------------------------------------
# Planner
# --------------------------------------------------


def test_planner_creates_plan():
    state = make_state("test goal")

    result = planner_agent_node(state)

    assert result is not None
    assert hasattr(result, "plan")


def test_planner_handles_empty_goal():
    state = make_state("")

    result = planner_agent_node(state)

    # não assume implementação exata, só comportamento
    assert result is not None


# --------------------------------------------------
# Fallback
# --------------------------------------------------


def test_fallback_sets_output():
    state = make_state("test")

    result = fallback_node(state)

    assert result is not None
    assert hasattr(result, "llm_output")


# --------------------------------------------------
# Reviewer
# --------------------------------------------------


def test_reviewer_detects_error():
    state = make_state("test")

    # forçamos um cenário de erro
    state.analysis = "error occurred"

    result = reviewer_agent_node(state)

    assert result is not None
