from typing import Any, Dict
from nexus_os.core.agent_state import AgentState
from nexus_os.core.graph.execution_graph import build_execution_graph
from nexus_os.core.memory.memory_store import MemoryStore
from nexus_os.core.memory.vector_store import VectorStore

import uuid
from nexus_os.core.observability.event_bus import EventBus
from nexus_os.core.observability.tracer import Tracer
from nexus_os.core.observability.log_sink import print_event
from nexus_os.core.observability.event_store import EventStore
from nexus_os.core.security.agent_policy import DEFAULT_AGENT_POLICY
from nexus_os.core.security.sandbox import enforce
from nexus_os.core.security.capabilities import Capability



class AgentResult:
    def __init__(self, output: str, metadata: Dict[str, Any]):
        self.output = output
        self.metadata = metadata


class NexusAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state: AgentState | None = None

        # -----------------------------
        # Observability
        # -----------------------------
        self.event_bus = EventBus()
        self.trace_id = str(uuid.uuid4())
        self.tracer = Tracer(self.event_bus, trace_id=self.trace_id)

        # Event store (persistência)
        self.event_store = EventStore()


        # Log sinks (observability config)
        self.event_bus.subscribe("agent.started", print_event)
        self.event_bus.subscribe("node.started", print_event)
        self.event_bus.subscribe("node.completed", print_event)
        self.event_bus.subscribe("retry.triggered", print_event)
        self.event_bus.subscribe("fallback.executed", print_event)
        self.event_bus.subscribe("agent.completed", print_event)

        # -----------------------------
        # Memory systems
        # -----------------------------
        self.memory_store = MemoryStore()
        self.vector_store = VectorStore()


        # Persistir TODOS os eventos
        self.event_bus.subscribe("*", self.event_store.persist)


    # -----------------------------------------------------
    # Inicialização do estado
    # -----------------------------------------------------

    def _initialize_state(self, goal: str) -> None:
        self.state = AgentState(
            goal=goal,
            status="running",
            )

        self.state.capabilities = DEFAULT_AGENT_POLICY
        # Propagação de observability
        self.state.tracer = self.tracer
        self.state.event_bus = self.event_bus

        self.state.steps.append("Agent initialized")

    # -----------------------------------------------------
    # Execução do grafo
    # -----------------------------------------------------

    def _execute(self) -> None:
        graph = build_execution_graph()
        with self.tracer.span("graph.invoke"):
            graph.invoke(self.state)

    # -----------------------------------------------------
    # Execução pública
    # -----------------------------------------------------

    def run(self, goal: str) -> AgentResult:
        self._initialize_state(goal)

        # Evento de início do agente
        self.event_bus.publish(
            "agent.started",
            {"trace_id": self.trace_id, "goal": goal},
        )

        self._execute()

        assert self.state is not None
        self.state.status = "completed"

        # Persistência de memória
        enforce(self.state.capabilities, Capability.WRITE_MEMORY)

        record = {
            "agent_id": self.agent_id,
            "goal": self.state.goal,
            "steps": self.state.steps,
            "output": self.state.llm_output,
            "status": self.state.status,
        }

        self.memory_store.save(record)

        if self.state.llm_output:
            enforce(self.state.capabilities, Capability.WRITE_MEMORY)
            self.vector_store.add(
                text=self.state.llm_output,
                metadata={
                    "goal": self.state.goal,
                    "agent_id": self.agent_id,
                },
            )

        self.event_bus.publish(
            "agent.completed",
            {"trace_id": self.trace_id, "status": self.state.status},
        )

        return AgentResult(
            output=self.state.llm_output or "Execution completed with fallback",
            metadata={
                "agent_id": self.agent_id,
                "status": self.state.status,
                "steps": self.state.steps,
            },
        )
