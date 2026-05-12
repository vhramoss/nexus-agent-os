from typing import Any, Dict
from datetime import datetime, timezone

from nexus_os.core.agent_state import AgentState
from nexus_os.core.graph.execution_graph import build_execution_graph
from nexus_os.core.memory.memory_store import MemoryStore
from nexus_os.core.memory.vector_store import VectorStore


class AgentResult:
    """
    Resultado final da execução de um agente.
    """

    def __init__(self, output: str, metadata: Dict[str, Any]):
        self.output = output
        self.metadata = metadata


class NexusAgent:
    """
    Núcleo do Nexus Agent OS.

    Responsabilidades:
    - Inicializar estado
    - Executar o grafo
    - Persistir memória
    - Retornar resultado

    NÃO decide fluxo.
    NÃO faz retry.
    NÃO trata fallback.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state: AgentState | None = None

        # Memórias
        self.memory_store = MemoryStore()
        self.vector_store = VectorStore()

    # -----------------------------------------------------
    # Inicialização do estado
    # -----------------------------------------------------

    def _initialize_state(self, goal: str) -> None:
        self.state = AgentState(
            goal=goal,
            status="running",
        )

        self.state.steps.append("Agent initialized")

    # -----------------------------------------------------
    # Execução do grafo
    # -----------------------------------------------------

    def _execute(self) -> None:
        graph = build_execution_graph()
        graph.invoke(self.state)

    # -----------------------------------------------------
    # Execução pública
    # -----------------------------------------------------

    def run(self, goal: str) -> AgentResult:
        """
        Executa o agente.

        IMPORTANTE:
        - Se o grafo terminou, a execução é considerada COMPLETED
        - Retry e fallback são fluxo normal
        """
        self._initialize_state(goal)
        self._execute()

        assert self.state is not None

        # Finalização normal
        self.state.status = "completed"

        # -------------------------
        # Persistência de memória
        # -------------------------

        record = {
            "agent_id": self.agent_id,
            "goal": self.state.goal,
            "steps": self.state.steps,
            "output": self.state.llm_output,
            "status": self.state.status,
        }

        # Memória histórica (JSON)
        self.memory_store.save(record)

        # Memória semântica (vetorial)
        if self.state.llm_output:
            self.vector_store.add(
                text=self.state.llm_output,
                metadata={
                    "goal": self.state.goal,
                    "agent_id": self.agent_id,
                },
            )

        # -------------------------
        # Resultado final
        # -------------------------

        return AgentResult(
            output=self.state.llm_output or "Execution completed with fallback",
            metadata={
                "agent_id": self.agent_id,
                "status": self.state.status,
                "steps": self.state.steps,
            },
        )