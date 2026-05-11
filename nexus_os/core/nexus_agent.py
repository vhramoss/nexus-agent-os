from typing import Any, Dict
from datetime import datetime, timezone

from nexus_os.core.agent_state import AgentState, AgentStatus
from nexus_os.core.graph.execution_graph import build_execution_graph

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

    Agente stateful com ciclo de vida explícito.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state: AgentState | None = None


    def _initialize_state(self, goal: str) -> None:
        """
        Inicializa o estado do agente.
        """
        self.state = AgentState(
            goal=goal,
            status=AgentStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )

        self.state.steps.append("Agent initialized")

    def _execute(self) -> None:
        graph = build_execution_graph()
        graph.invoke(self.state)


    def run(self, goal: str) -> AgentResult:
        """
        Executa o agente respeitando o ciclo de vida.
        """
        self._initialize_state(goal)

        try:
            self._execute()

            # Finalização com sucesso
            assert self.state is not None  # segurança lógica

            self.state.status = AgentStatus.COMPLETED
            self.state.finished_at = datetime.now(timezone.utc)

            return AgentResult(
                output=f"Agent '{self.agent_id}' completed goal: {goal}",
                metadata={
                    "agent_id": self.agent_id,
                    "status": self.state.status,
                    "steps": self.state.steps,
                },
            )

        except Exception as e:
            assert self.state is not None

            self.state.status = AgentStatus.ERROR
            self.state.finished_at = datetime.now(timezone.utc)

            return AgentResult(
                output=str(e),
                metadata={
                    "agent_id": self.agent_id,
                    "status": self.state.status,
                },
            )


     