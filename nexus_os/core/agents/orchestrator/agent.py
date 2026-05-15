from typing import Any, Dict, Optional
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

from nexus_os.core.contracts.agent import AgentInput, AgentOutput
from nexus_os.core.telemetry.telemetry import Telemetry


class NexusAgent:

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state: Optional[Any] = None

        # -----------------------------
        # Observability
        # -----------------------------
        self.event_bus = EventBus()
        self.trace_id = str(uuid.uuid4())
        self.tracer = Tracer(self.event_bus, trace_id=self.trace_id)
        self.event_store = EventStore()

        # ✅ Telemetry 
        self.telemetry = Telemetry(self.event_bus)

        # -----------------------------
        # Subscribers
        # -----------------------------
        self.event_bus.subscribe("agent.started", print_event)
        self.event_bus.subscribe("node.started", print_event)
        self.event_bus.subscribe("node.completed", print_event)
        self.event_bus.subscribe("retry.triggered", print_event)
        self.event_bus.subscribe("fallback.executed", print_event)
        self.event_bus.subscribe("agent.completed", print_event)

        # ✅ Persistência de eventos
        self.event_bus.subscribe("*", self.event_store.persist)

        # -----------------------------
        # Memory
        # -----------------------------
        self.memory_store = MemoryStore()
        self.vector_store = VectorStore()

    # -----------------------------------------------------
    # Execução pública
    # -----------------------------------------------------
    def run(self, input: AgentInput) -> AgentOutput:
        try:
            goal = input.goal

            self.state = initialize_state(self, goal)

            self.telemetry.agent_started(self.trace_id, goal)

            execute_graph(self)

            persist_memory(self)

            self.telemetry.agent_completed(self.trace_id, self.state.status)

            return AgentOutput(
                result=self.state.llm_output,
                steps=self.state.steps,
                status=self.state.status,
            )

        except Exception as e:
            import traceback

            return AgentOutput(
                result=f"ERROR: {str(e)}\n{traceback.format_exc()}",
                steps=[],
                status="failed",
            )
