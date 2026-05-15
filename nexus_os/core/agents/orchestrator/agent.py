from typing import Any, Dict
import uuid

from nexus_os.core.observability.event_bus import EventBus
from nexus_os.core.observability.tracer import Tracer
from nexus_os.core.observability.event_store import EventStore
from nexus_os.core.observability.log_sink import print_event

from nexus_os.core.memory.memory_store import MemoryStore
from nexus_os.core.memory.vector_store import VectorStore

from nexus_os.core.agents.orchestrator.state import initialize_state
from nexus_os.core.agents.orchestrator.executor import execute_graph
from nexus_os.core.agents.orchestrator.persistence import persist_memory
from nexus_os.core.agents.orchestrator.lifecycle import emit_agent_started, emit_agent_completed
from nexus_os.core.contracts.agent import AgentInput, AgentOutput

class AgentResult:
    def __init__(self, output: str, metadata: Dict[str, Any]):
        self.output = output
        self.metadata = metadata


class NexusAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = None

        # Observability
        self.event_bus = EventBus()
        self.trace_id = str(uuid.uuid4())
        self.tracer = Tracer(self.event_bus, trace_id=self.trace_id)
        self.event_store = EventStore()

        # Subscribers
        self.event_bus.subscribe("agent.started", print_event)
        self.event_bus.subscribe("node.started", print_event)
        self.event_bus.subscribe("node.completed", print_event)
        self.event_bus.subscribe("retry.triggered", print_event)
        self.event_bus.subscribe("fallback.executed", print_event)
        self.event_bus.subscribe("agent.completed", print_event)

        self.event_bus.subscribe("*", self.event_store.persist)

        # Memory
        self.memory_store = MemoryStore()
        self.vector_store = VectorStore()

    def run(self, input: AgentInput) -> AgentOutput:
        goal = input.goal

        self.state = initialize_state(self, goal)

        emit_agent_started(self, goal)

        execute_graph(self)

        persist_memory(self)

        emit_agent_completed(self)


        return AgentOutput(
            result=self.state.llm_output,
            steps=self.state.steps,
            status=self.state.status,
        )
